#!/usr/bin/env python3
"""
PRAYCG OCM v0.2 - 0.25-second raw-XDF re-extraction

Standalone analysis script for re-extracting raw OpenBCI EEG from XDF and
running Override Cue Microstate (OCM) analysis with quarter-second bins.

Boundary: exploratory working-memory/cue-update analysis only. This is not a
clinical tool and does not certify narrative meaning, OSM, hidden-Y biology, or
human EEG mechanism.
"""
from __future__ import annotations
import argparse, json, math, os, re, struct, csv, zipfile, shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
from scipy import signal, stats


FMT_SIZES = {
    'int8': 1, 'int16': 2, 'int32': 4, 'int64': 8,
    'float32': 4, 'float64': 8, 'double': 8, 'float': 4,
}
FMT_DTYPES = {
    'int8': '<i1', 'int16': '<i2', 'int32': '<i4', 'int64': '<i8',
    'float32': '<f4', 'float64': '<f8', 'double': '<f8', 'float': '<f4',
}

PHASES = ['CONTROL_1', 'TARGET_1', 'CONTEXTUAL_OVERRIDE_1']
PHASE_ALIASES = {'OVERRIDE_1': 'CONTEXTUAL_OVERRIDE_1'}

# PRAYCG16_FIXED_ORDER_v1, 0-indexed
CHANNEL_GROUPS = {
    'frontal_task': [0, 3, 4],       # Fz, F3, F4
    'frontoparietal_task': [0, 2, 3, 4, 7, 8], # Fz/Pz/F3/F4/P3/P4
    'central': [1, 5, 6],            # Cz, C3, C4
    'posterior_temporal': [9, 10],   # T5, T6
    'visual': [11, 12],              # O1, O2
    'jaw_temporal_sentinel': [13, 14], # T3, T4
}


def read_varint(f):
    b = f.read(1)
    if not b:
        return None
    n = b[0]
    if n == 0:
        return None
    data = f.read(n)
    if len(data) != n:
        return None
    if n == 1:
        return data[0]
    if n == 4:
        return struct.unpack('<I', data)[0]
    if n == 8:
        return struct.unpack('<Q', data)[0]
    raise ValueError(f'Unsupported XDF variable integer width: {n}')


def parse_info_xml(xml_bytes: bytes) -> Dict[str, Any]:
    txt = xml_bytes.decode('utf-8', errors='ignore')
    out: Dict[str, Any] = {'xml': txt}
    try:
        root = ET.fromstring(txt)
        for tag in ['name', 'type', 'channel_count', 'nominal_srate', 'channel_format', 'source_id', 'uid', 'created_at']:
            el = root.find(tag)
            if el is not None and el.text is not None:
                out[tag] = el.text.strip()
    except Exception as e:
        out['xml_parse_error'] = repr(e)
    return out


def scan_xdf_headers(path: Path) -> Dict[int, Dict[str, Any]]:
    streams: Dict[int, Dict[str, Any]] = {}
    with open(path, 'rb') as f:
        if f.read(4) != b'XDF:':
            raise ValueError(f'Not an XDF file: {path}')
        while True:
            ln = read_varint(f)
            if ln is None:
                break
            tag_bytes = f.read(2)
            if len(tag_bytes) < 2:
                break
            tag = struct.unpack('<H', tag_bytes)[0]
            payload_len = int(ln) - 2
            payload_start = f.tell()
            if tag == 2:  # StreamHeader
                sid_bytes = f.read(4)
                if len(sid_bytes) < 4:
                    break
                sid = struct.unpack('<I', sid_bytes)[0]
                xml = f.read(payload_len - 4)
                streams[sid] = parse_info_xml(xml)
                streams[sid]['stream_id'] = sid
            else:
                f.seek(payload_len, 1)
            end = payload_start + payload_len
            if f.tell() != end:
                f.seek(end)
    return streams


def choose_eeg_sid(headers: Dict[int, Dict[str, Any]], prefer_name: str = 'obci_eeg1') -> int:
    for sid, h in headers.items():
        if str(h.get('name', '')).lower() == prefer_name.lower():
            return sid
    for sid, h in headers.items():
        if str(h.get('type', '')).lower() == 'eeg':
            return sid
    raise ValueError('No EEG stream found in XDF headers.')


def load_xdf_numeric_stream(path: Path, sid_wanted: int, headers: Dict[int, Dict[str, Any]]) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    h = headers[sid_wanted]
    ch = int(float(h.get('channel_count', 0)))
    sr = float(h.get('nominal_srate', 0) or 0)
    cf = str(h.get('channel_format', '')).lower()
    if cf == 'string' or cf not in FMT_SIZES:
        raise ValueError(f'Stream is not supported numeric format: {cf}')
    fixed_size = FMT_SIZES[cf]
    dtype = np.dtype(FMT_DTYPES[cf])
    ts_list: List[float] = []
    vals: List[np.ndarray] = []
    last_ts: Optional[float] = None
    with open(path, 'rb') as f:
        if f.read(4) != b'XDF:':
            raise ValueError(f'Not an XDF file: {path}')
        while True:
            ln = read_varint(f)
            if ln is None:
                break
            tag_bytes = f.read(2)
            if len(tag_bytes) < 2:
                break
            tag = struct.unpack('<H', tag_bytes)[0]
            payload_len = int(ln) - 2
            payload_start = f.tell()
            if tag == 3:
                sid_bytes = f.read(4)
                if len(sid_bytes) < 4:
                    break
                sid = struct.unpack('<I', sid_bytes)[0]
                n_samples = read_varint(f) or 0
                if sid == sid_wanted:
                    for _ in range(int(n_samples)):
                        tb = f.read(1)
                        if not tb:
                            break
                        tbv = tb[0]
                        if tbv == 8:
                            t = struct.unpack('<d', f.read(8))[0]
                        elif tbv == 0:
                            if last_ts is not None and sr > 0:
                                t = last_ts + 1.0 / sr
                            else:
                                t = float('nan')
                        else:
                            raise ValueError(f'Bad timestamp byte count {tbv} at offset {f.tell()}')
                        raw = f.read(ch * fixed_size)
                        if len(raw) < ch * fixed_size:
                            break
                        x = np.frombuffer(raw, dtype=dtype, count=ch).astype(float)
                        if math.isfinite(t):
                            ts_list.append(float(t))
                            vals.append(x)
                            last_ts = float(t)
                else:
                    # Skip whole remaining sample chunk payload.
                    pass
            # Go to chunk end regardless; this also skips non-wanted sample chunks.
            end = payload_start + payload_len
            if f.tell() != end:
                f.seek(end)
    if not vals:
        raise ValueError(f'No samples loaded for stream {sid_wanted}')
    return np.asarray(ts_list, dtype=float), np.vstack(vals), h


def load_eeg_from_xdf(path: Path) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    headers = scan_xdf_headers(path)
    sid = choose_eeg_sid(headers)
    ts, data, h = load_xdf_numeric_stream(path, sid, headers)
    return ts, data, h


def safe_group(n_ch: int, names: List[str]) -> List[int]:
    idx: List[int] = []
    for name in names:
        idx.extend(CHANNEL_GROUPS.get(name, []))
    idx = sorted(set([i for i in idx if 0 <= i < n_ch]))
    if not idx:
        idx = list(range(min(n_ch, 16)))
    return idx


def robust_z(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    med = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - med))
    denom = 1.4826 * mad
    if not np.isfinite(denom) or denom <= 1e-12:
        denom = np.nanstd(x)
    if not np.isfinite(denom) or denom <= 1e-12:
        return np.zeros_like(x, dtype=float)
    return (x - med) / denom


def preprocess_eeg(data: np.ndarray, fs: float) -> np.ndarray:
    x = data.astype(float).copy()
    # Replace non-finite by channel median.
    for c in range(x.shape[1]):
        col = x[:, c]
        med = np.nanmedian(col[np.isfinite(col)]) if np.any(np.isfinite(col)) else 0.0
        col[~np.isfinite(col)] = med
        x[:, c] = col - np.nanmedian(col)
    # A gentle 60 Hz notch; close to Nyquist but still useful for line-noise attenuation.
    try:
        b, a = signal.iirnotch(60.0, Q=30.0, fs=fs)
        x = signal.filtfilt(b, a, x, axis=0)
    except Exception:
        pass
    return x


def band_log_power_series(data: np.ndarray, fs: float, lo: float, hi: float, ch_idx: List[int]) -> np.ndarray:
    hi = min(hi, fs / 2 - 1.0)
    lo = max(lo, 0.5)
    sos = signal.butter(4, [lo, hi], btype='bandpass', fs=fs, output='sos')
    filt = signal.sosfiltfilt(sos, data[:, ch_idx], axis=0)
    power = np.mean(filt ** 2, axis=1)
    return np.log1p(np.maximum(power, 0))


def p2p_series(data: np.ndarray, fs: float, ch_idx: List[int], window_s: float = 0.25) -> np.ndarray:
    # Compute approximate point-wise p2p by using rolling max/min over window samples.
    n = max(3, int(round(window_s * fs)))
    y = np.mean(data[:, ch_idx], axis=1)
    # Use pandas rolling for simplicity.
    s = pd.Series(y)
    return (s.rolling(n, center=True, min_periods=max(2, n//3)).max() - s.rolling(n, center=True, min_periods=max(2, n//3)).min()).bfill().ffill().values


def parse_event_log(path: Path) -> List[Dict[str, Any]]:
    if path.suffix.lower() == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and 'events' in data:
                return data['events']
    elif path.suffix.lower() == '.csv':
        return pd.read_csv(path).to_dict('records')
    raise ValueError(f'Unsupported event log: {path}')


def phase_times(events: List[Dict[str, Any]]) -> Dict[str, Tuple[float, float]]:
    starts: Dict[str, float] = {}
    ends: Dict[str, float] = {}
    for e in events:
        m = str(e.get('marker', ''))
        t = e.get('lsl_time')
        if t is None or (isinstance(t, float) and not math.isfinite(t)):
            continue
        for ph in PHASES:
            if m == f'{ph}_START':
                starts[ph] = float(t)
            elif m == f'{ph}_END':
                ends[ph] = float(t)
    return {ph: (starts[ph], ends[ph]) for ph in PHASES if ph in starts and ph in ends}


def load_cue_schedule(path: Optional[Path]) -> Optional[pd.DataFrame]:
    if not path or not path.exists():
        return None
    if path.suffix.lower() == '.json':
        obj = json.load(open(path, 'r', encoding='utf-8'))
        rows = obj.get('cue_events') or obj.get('cues') or []
        return pd.DataFrame(rows)
    if path.suffix.lower() == '.csv':
        return pd.read_csv(path)
    return None


def cue_table(events: List[Dict[str, Any]], phase_map: Dict[str, Tuple[float, float]], cue_sched: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    rows = []
    pat = re.compile(r'^(CONTROL_1|TARGET_1|CONTEXTUAL_OVERRIDE_1|OVERRIDE_1)_CUE_(\d+)_VALUE_(\d+)_START$')
    for e in events:
        marker = str(e.get('marker', ''))
        m = pat.match(marker)
        if not m: continue
        phase = PHASE_ALIASES.get(m.group(1), m.group(1))
        if phase not in PHASES: continue
        rows.append({
            'phase': phase,
            'cue_index': int(m.group(2)),
            'cue_value': int(m.group(3)),
            'lsl_time': float(e['lsl_time']),
            'relative_time_sec': float(str(e.get('note','')).replace('t=','')) if str(e.get('note','')).startswith('t=') else np.nan,
            'source': 'event_log_marker'
        })
    df = pd.DataFrame(rows)
    # Reconstruct missing phases (usually CONTROL_1) from cue schedule and phase start.
    if cue_sched is not None and not cue_sched.empty:
        sched = cue_sched.copy()
        # standardize columns
        idx_col = 'cue_index' if 'cue_index' in sched.columns else ('index' if 'index' in sched.columns else None)
        value_col = 'value' if 'value' in sched.columns else ('cue_value' if 'cue_value' in sched.columns else None)
        start_col = 'start_sec' if 'start_sec' in sched.columns else ('start' if 'start' in sched.columns else None)
        if value_col and start_col:
            for ph in PHASES:
                existing = 0 if df.empty else int((df['phase'] == ph).sum())
                if existing == 0 and ph in phase_map:
                    ph_start, ph_end = phase_map[ph]
                    for k, r in sched.iterrows():
                        rel = float(r[start_col])
                        lsl = ph_start + rel
                        if lsl < ph_start or lsl > ph_end + 1: continue
                        rows.append({
                            'phase': ph,
                            'cue_index': int(r[idx_col]) if idx_col else int(k+1),
                            'cue_value': int(r[value_col]) if value_col else np.nan,
                            'lsl_time': lsl,
                            'relative_time_sec': rel,
                            'source': 'reconstructed_from_cue_schedule'
                        })
                    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.sort_values(['phase','cue_index']).reset_index(drop=True)


def interval_mean(ts: np.ndarray, y: np.ndarray, start: float, end: float, min_samples: int = 3) -> float:
    m = (ts >= start) & (ts < end)
    if int(np.sum(m)) < min_samples:
        return float('nan')
    return float(np.nanmean(y[m]))


def run_ocm_for_run(run_name: str, xdf_path: Path, event_path: Path, cue_path: Optional[Path], out_dir: Path) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    events = parse_event_log(event_path)
    pht = phase_times(events)
    cue_sched = load_cue_schedule(cue_path) if cue_path else None
    cues = cue_table(events, pht, cue_sched)
    cues.to_csv(out_dir / f'{run_name}_cue_table_used.csv', index=False)

    ts, data, header = load_eeg_from_xdf(xdf_path)
    fs = float(header.get('nominal_srate', 125.0) or 125.0)
    data = preprocess_eeg(data, fs)
    n_ch = data.shape[1]
    task_idx = safe_group(n_ch, ['frontoparietal_task'])
    frontal_idx = safe_group(n_ch, ['frontal_task'])
    visual_idx = safe_group(n_ch, ['visual'])
    jaw_idx = safe_group(n_ch, ['jaw_temporal_sentinel'])
    all_idx = list(range(n_ch))

    feat = {
        'task_gamma_30_45': band_log_power_series(data, fs, 30, 45, task_idx),
        'task_gamma_35_40': band_log_power_series(data, fs, 35, 40, task_idx),
        'task_theta_4_8': band_log_power_series(data, fs, 4, 8, task_idx),
        'frontal_theta_4_8': band_log_power_series(data, fs, 4, 8, frontal_idx),
        'visual_gamma_30_45': band_log_power_series(data, fs, 30, 45, visual_idx),
        'jaw_hf_45_55': band_log_power_series(data, fs, 45, 55, jaw_idx),
        'global_p2p_025': p2p_series(data, fs, all_idx, 0.25),
    }
    # Artifact score proxy: robust positive z of jaw HF and p2p.
    artifact = 0.5 * np.maximum(0, robust_z(feat['jaw_hf_45_55'])) + 0.5 * np.maximum(0, robust_z(feat['global_p2p_025']))
    feat['artifact_score'] = artifact

    bin_rows = []
    cue_rows = []
    bin_edges = np.arange(-0.75, 3.0001, 0.25)
    for _, r in cues.iterrows():
        ph = r['phase']
        t0 = float(r['lsl_time'])
        ci = int(r['cue_index'])
        cv = int(r['cue_value']) if pd.notna(r['cue_value']) else np.nan
        base = {'run': run_name, 'phase': ph, 'cue_index': ci, 'cue_value': cv, 'cue_lsl_time': t0, 'cue_relative_time_sec': r.get('relative_time_sec', np.nan), 'cue_source': r.get('source','')}
        # micro bins
        for b0 in bin_edges[:-1]:
            b1 = b0 + 0.25
            row = {**base, 'bin_start_rel_sec': round(float(b0),3), 'bin_end_rel_sec': round(float(b1),3), 'bin_center_rel_sec': round(float((b0+b1)/2),3)}
            s = t0 + b0; e = t0 + b1
            for k,y in feat.items():
                row[k] = interval_mean(ts, y, s, e)
            bin_rows.append(row)
        # composite windows
        windows = {
            'pre': (-0.75, 0.0),
            'rec': (0.10, 0.85),
            'upd': (0.85, 2.25),
            'maint': (2.25, 3.00),
        }
        row = {**base}
        for w,(a,b) in windows.items():
            for k,y in feat.items():
                row[f'{w}_{k}'] = interval_mean(ts, y, t0+a, t0+b)
        # Deltas
        row['DR_taskgamma_30_45'] = row['rec_task_gamma_30_45'] - row['pre_task_gamma_30_45']
        row['DR_taskgamma_35_40'] = row['rec_task_gamma_35_40'] - row['pre_task_gamma_35_40']
        row['DR_visualgamma_30_45'] = row['rec_visual_gamma_30_45'] - row['pre_visual_gamma_30_45']
        row['WMU_tasktheta_4_8'] = row['upd_task_theta_4_8'] - row['pre_task_theta_4_8']
        row['WMU_frontaltheta_4_8'] = row['upd_frontal_theta_4_8'] - row['pre_frontal_theta_4_8']
        row['MAINT_tasktheta_4_8'] = row['maint_task_theta_4_8'] - row['pre_task_theta_4_8']
        row['mean_artifact_score'] = np.nanmean([row.get('pre_artifact_score', np.nan), row.get('rec_artifact_score', np.nan), row.get('upd_artifact_score', np.nan), row.get('maint_artifact_score', np.nan)])
        cue_rows.append(row)

    bin_df = pd.DataFrame(bin_rows)
    cue_df = pd.DataFrame(cue_rows)

    # Add within-run z-score score columns for cue rows.
    if not cue_df.empty:
        for col in ['DR_taskgamma_30_45','DR_taskgamma_35_40','WMU_tasktheta_4_8','WMU_frontaltheta_4_8','MAINT_tasktheta_4_8','DR_visualgamma_30_45','mean_artifact_score']:
            cue_df[col + '_z'] = robust_z(cue_df[col].values)
        cue_df['OCM_score'] = (
            0.35*cue_df['DR_taskgamma_35_40_z'] +
            0.35*cue_df['WMU_frontaltheta_4_8_z'] +
            0.15*cue_df['MAINT_tasktheta_4_8_z'] -
            0.10*np.maximum(0, cue_df['DR_visualgamma_30_45_z']) -
            0.25*np.maximum(0, cue_df['mean_artifact_score_z'])
        )
        cue_df['OCM_score_z'] = robust_z(cue_df['OCM_score'].values)

        # Specificity vs target/control by cue index.
        by_key = cue_df.pivot_table(index='cue_index', columns='phase', values=['DR_taskgamma_35_40','WMU_frontaltheta_4_8','OCM_score'], aggfunc='first')
        # flatten helper for deltas
        for metric in ['DR_taskgamma_35_40','WMU_frontaltheta_4_8','OCM_score']:
            for comp in ['TARGET_1','CONTROL_1']:
                if (metric, 'CONTEXTUAL_OVERRIDE_1') in by_key.columns and (metric, comp) in by_key.columns:
                    diff = by_key[(metric,'CONTEXTUAL_OVERRIDE_1')] - by_key[(metric,comp)]
                    for ci,val in diff.items():
                        cue_df.loc[(cue_df['phase']=='CONTEXTUAL_OVERRIDE_1') & (cue_df['cue_index']==ci), f'override_minus_{comp.lower()}_{metric}'] = val
        # Thresholds using target as null where available.
        target = cue_df[cue_df['phase']=='TARGET_1']
        if not target.empty:
            dr_thr = float(np.nanpercentile(target['DR_taskgamma_35_40'], 75))
            wmu_thr = float(np.nanpercentile(target['WMU_frontaltheta_4_8'], 75))
            ocm_thr = float(np.nanpercentile(target['OCM_score'], 90))
        else:
            dr_thr = float(np.nanpercentile(cue_df['DR_taskgamma_35_40'], 75))
            wmu_thr = float(np.nanpercentile(cue_df['WMU_frontaltheta_4_8'], 75))
            ocm_thr = float(np.nanpercentile(cue_df['OCM_score'], 90))
        art_thr = float(np.nanpercentile(cue_df['mean_artifact_score'], 75))
        cue_df['ocm_event_vs_target_null'] = (
            (cue_df['phase']=='CONTEXTUAL_OVERRIDE_1') &
            (cue_df['DR_taskgamma_35_40'] > dr_thr) &
            (cue_df['WMU_frontaltheta_4_8'] > wmu_thr) &
            (cue_df['OCM_score'] > ocm_thr) &
            (cue_df['mean_artifact_score'] <= art_thr)
        )
    else:
        dr_thr = wmu_thr = ocm_thr = art_thr = float('nan')

    cue_df.to_csv(out_dir / f'{run_name}_ocm_025_cue_epoch_table.csv', index=False)
    bin_df.to_csv(out_dir / f'{run_name}_ocm_025_microbin_table.csv', index=False)

    # Summaries.
    phase_summary = []
    for ph in PHASES:
        d = cue_df[cue_df['phase']==ph]
        if d.empty: continue
        phase_summary.append({
            'run': run_name,
            'phase': ph,
            'n_cues': len(d),
            'mean_DR_taskgamma_35_40': float(np.nanmean(d['DR_taskgamma_35_40'])),
            'median_DR_taskgamma_35_40': float(np.nanmedian(d['DR_taskgamma_35_40'])),
            'mean_WMU_frontaltheta_4_8': float(np.nanmean(d['WMU_frontaltheta_4_8'])),
            'median_WMU_frontaltheta_4_8': float(np.nanmedian(d['WMU_frontaltheta_4_8'])),
            'mean_MAINT_tasktheta_4_8': float(np.nanmean(d['MAINT_tasktheta_4_8'])),
            'mean_OCM_score': float(np.nanmean(d['OCM_score'] if 'OCM_score' in d else np.nan)),
            'mean_artifact_score': float(np.nanmean(d['mean_artifact_score'])),
            'event_count_vs_target_null': int(np.nansum(d.get('ocm_event_vs_target_null', False))),
        })
    summary_df = pd.DataFrame(phase_summary)

    # Cue-index and running-sum correlations for override.
    ov = cue_df[cue_df['phase']=='CONTEXTUAL_OVERRIDE_1'].copy()
    corrs = {}
    if len(ov) >= 5:
        ov['running_sum'] = ov['cue_value'].cumsum()
        for ycol in ['DR_taskgamma_35_40','WMU_frontaltheta_4_8','OCM_score']:
            for xcol in ['cue_index','running_sum','cue_value']:
                valid = ov[[xcol,ycol]].dropna()
                if len(valid) >= 5:
                    rho,pv = stats.spearmanr(valid[xcol], valid[ycol])
                    corrs[f'{ycol}__rho_vs_{xcol}'] = float(rho)
                    corrs[f'{ycol}__p_vs_{xcol}'] = float(pv)
    # Override-minus target / control means.
    specific = {}
    if not ov.empty:
        for col in cue_df.columns:
            if col.startswith('override_minus_target_1_') or col.startswith('override_minus_control_1_'):
                specific[f'mean_{col}'] = float(np.nanmean(ov[col]))
    run_summary = {
        'run': run_name,
        'xdf_file': str(xdf_path),
        'event_log': str(event_path),
        'cue_schedule': str(cue_path) if cue_path else '',
        'eeg_stream_name': header.get('name',''),
        'eeg_samples': int(data.shape[0]),
        'eeg_channels': int(data.shape[1]),
        'eeg_nominal_srate': fs,
        'eeg_time_min': float(np.nanmin(ts)),
        'eeg_time_max': float(np.nanmax(ts)),
        'total_cues_used': int(len(cue_df)),
        'override_cues': int((cue_df['phase']=='CONTEXTUAL_OVERRIDE_1').sum()) if not cue_df.empty else 0,
        'target_cues': int((cue_df['phase']=='TARGET_1').sum()) if not cue_df.empty else 0,
        'control_cues': int((cue_df['phase']=='CONTROL_1').sum()) if not cue_df.empty else 0,
        'target_null_DR75_threshold': dr_thr,
        'target_null_WMU75_threshold': wmu_thr,
        'target_null_OCM90_threshold': ocm_thr,
        'artifact75_threshold': art_thr,
        'override_event_count_vs_target_null': int(np.nansum(ov.get('ocm_event_vs_target_null', False))) if not ov.empty else 0,
        **corrs,
        **specific,
        'method_boundary': 'Quarter-second binning uses continuous bandpass/Hilbert-style envelope proxies rather than independent 0.25-s Fourier PSD. Theta interpretation is aggregated over update/maintenance windows and remains exploratory.',
    }
    pd.DataFrame([run_summary]).to_csv(out_dir / f'{run_name}_ocm_025_run_summary.csv', index=False)
    summary_df.to_csv(out_dir / f'{run_name}_ocm_025_phase_summary.csv', index=False)
    with open(out_dir / f'{run_name}_ocm_025_interpretation.json','w',encoding='utf-8') as f:
        json.dump(run_summary, f, indent=2)
    return run_summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--run-spec-json', required=True, help='JSON list of {run_name,xdf,event_log,cue_schedule}')
    args = ap.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    specs = json.load(open(args.run_spec_json, 'r', encoding='utf-8'))
    summaries=[]
    for spec in specs:
        rn = spec['run_name']
        rd = out / rn
        print(f'Running {rn}...')
        summ = run_ocm_for_run(rn, Path(spec['xdf']), Path(spec['event_log']), Path(spec['cue_schedule']) if spec.get('cue_schedule') else None, rd)
        summaries.append(summ)
    pd.DataFrame(summaries).to_csv(out / 'combined_ocm_025_run_summary.csv', index=False)
    # Combined phase and cue tables
    all_phase=[]; all_cue=[]; all_bin=[]
    for spec in specs:
        rn=spec['run_name']; rd=out/rn
        for fn, coll in [(f'{rn}_ocm_025_phase_summary.csv', all_phase), (f'{rn}_ocm_025_cue_epoch_table.csv', all_cue), (f'{rn}_ocm_025_microbin_table.csv', all_bin)]:
            p=rd/fn
            if p.exists(): coll.append(pd.read_csv(p))
    if all_phase: pd.concat(all_phase, ignore_index=True).to_csv(out/'combined_ocm_025_phase_summary.csv', index=False)
    if all_cue: pd.concat(all_cue, ignore_index=True).to_csv(out/'combined_ocm_025_cue_epoch_table.csv', index=False)
    if all_bin: pd.concat(all_bin, ignore_index=True).to_csv(out/'combined_ocm_025_microbin_table.csv', index=False)
    print('Done:', out)

if __name__ == '__main__':
    main()
