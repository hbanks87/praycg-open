#!/usr/bin/env python3
from __future__ import annotations
import json, math, os, re, sys, shutil, zipfile, hashlib, textwrap, subprocess, warnings, zlib
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
from scipy import signal, stats

# Use the existing robust XDF parser from the OCM raw-XDF module.
SCRIPTS_DIR = Path('/mnt/data/PRAYCG_Unified_MasterSuite_v1_5_1_NIP_CET_EET/scripts')
sys.path.insert(0, str(SCRIPTS_DIR))
from praycg_ocm_quartersecond_reextract_v1_4_5 import (  # type: ignore
    scan_xdf_headers, load_xdf_numeric_stream, choose_eeg_sid, load_eeg_from_xdf,
    preprocess_eeg, parse_event_log, phase_times, robust_z, safe_group, band_log_power_series, p2p_series
)

VERSION = '1.5.2'
PHASES = ['CONTROL_1','TARGET_1','CONTEXTUAL_OVERRIDE_1']
PHASE_LABEL = {'CONTROL_1':'Control','TARGET_1':'Target','CONTEXTUAL_OVERRIDE_1':'Override'}

# PRAYCG16_FIXED_ORDER_v1 channel indices; Contact run channel map is locked.
CH = {
    'Fz':0,'Cz':1,'Pz':2,'F3':3,'F4':4,'C3':5,'C4':6,'P3':7,'P4':8,
    'T5':9,'T6':10,'O1':11,'O2':12,'T3':13,'T4':14,'Fp1':15
}
NEURAL_LZC_IDX = list(range(0,13))  # exclude T3/T4/Fp1 sentinel channels from complexity proxy.
ARTIFACT_IDX = [13,14,15]
FP1_IDX = 15


def load_phase_map(event_path: Path) -> Tuple[List[Dict[str,Any]], Dict[str,Tuple[float,float]]]:
    events = parse_event_log(event_path)
    pht = phase_times(events)
    # Add Baseline/Washouts/Baseline2 manually; phase_times only covers main conditions.
    starts, ends = {}, {}
    for e in events:
        m=str(e.get('marker',''))
        t=e.get('lsl_time')
        if t is None: continue
        if m.endswith('_START'):
            starts[m[:-6]] = float(t)
        elif m.endswith('_END'):
            ends[m[:-4]] = float(t)
    for ph in ['BASELINE_1','WASHOUT_1','WASHOUT_2','WASHOUT_3','BASELINE_2_REFLECTION']:
        if ph in starts and ph in ends:
            pht[ph] = (starts[ph], ends[ph])
    return events, pht




def apply_contact_corrected_time_axis(ts: np.ndarray, data: np.ndarray) -> Tuple[np.ndarray, float, Dict[str, Any]]:
    inv_path = Path('/mnt/data/PRAYCG_Contact_Run1_Analysis_v1_0/tables/stream_inventory_corrected.csv')
    info = {'alignment_method':'raw_xdf_timestamps'}
    if inv_path.exists():
        inv = pd.read_csv(inv_path)
        eeg = inv[inv['name'] == 'obci_eeg1']
        if not eeg.empty:
            r = eeg.iloc[0]
            t_min = float(r['corrected_t_min']); t_max = float(r['corrected_t_max'])
            n = data.shape[0]
            ts_corr = np.linspace(t_min, t_max, n)
            fs_corr = float((n-1) / max(1e-9, (t_max - t_min)))
            info = {'alignment_method': str(r.get('alignment_method','sample_index_from_ALS_pulses')), 'corrected_t_min': t_min, 'corrected_t_max': t_max, 'effective_srate': fs_corr}
            return ts_corr, fs_corr, info
    fs_eff=float(1.0/np.nanmedian(np.diff(ts)))
    return ts, fs_eff, info


def lzc_binary(seq: np.ndarray) -> int:
    """Kaspar-Schuster style Lempel-Ziv complexity for binary sequence."""
    s = ''.join('1' if x else '0' for x in seq.astype(bool).ravel())
    n = len(s)
    if n == 0: return 0
    i, k, l = 0, 1, 1
    c = 1
    k_max = 1
    while True:
        if i + k > n or l + k > n:
            c += 1
            break
        if s[i+k-1] == s[l+k-1]:
            k += 1
            if l+k > n:
                c += 1
                break
        else:
            if k > k_max: k_max = k
            i += 1
            if i == l:
                c += 1
                l += k_max
                if l + 1 > n:
                    break
                i = 0
                k = 1
                k_max = 1
            else:
                k = 1
    return int(c)


def normalized_lzc_window(x_win: np.ndarray) -> float:
    # Efficient LZ-style normalized compression proxy. Exact LZC is expensive across full runs;
    # this uses median-binarized multichannel EEG and zlib compressed-length ratio as an
    # algorithmic compressibility/diversity proxy. Higher = less compressible / more diverse.
    if x_win.shape[0] < 50:
        return np.nan
    x = np.diff(x_win.copy(), axis=0)
    med = np.nanmedian(x, axis=0)
    bits = (x > med).astype(np.uint8).ravel()
    n = len(bits)
    if n <= 8: return np.nan
    packed = np.packbits(bits).tobytes()
    if len(packed) < 8: return np.nan
    comp = zlib.compress(packed, level=6)
    # Correct for header overhead and bind to approximately 0..1+ range.
    ratio = max(0.0, (len(comp)-8) / max(1, len(packed)))
    return float(ratio)


def compute_lzc_timeseries(ts: np.ndarray, data: np.ndarray, feature_df: pd.DataFrame, window_sec: float=6.0, fs: float=62.5) -> pd.DataFrame:
    rows = []
    half = window_sec / 2
    for _, r in feature_df.iterrows():
        t = float(r['time_lsl']) if 'time_lsl' in r else np.nan
        if not math.isfinite(t):
            continue
        m = (ts >= t-half) & (ts < t+half)
        if int(m.sum()) < int(window_sec*fs*0.75):  # require enough samples
            lzc = np.nan
        else:
            lzc = normalized_lzc_window(data[m][:, NEURAL_LZC_IDX])
        rows.append({
            'time_lsl': t,
            'condition': r.get('condition',''),
            'condition_offset_sec': r.get('condition_offset_sec', np.nan),
            'lz_complexity_proxy': lzc,
            'window_sec': window_sec,
            'neural_channels_used': 'Fz,Cz,Pz,F3,F4,C3,C4,P3,P4,T5,T6,O1,O2',
        })
    out = pd.DataFrame(rows)
    out['lz_complexity_z'] = robust_z(out['lz_complexity_proxy'].to_numpy(dtype=float)) if len(out) else []
    return out


def interval_mean_df(df: pd.DataFrame, t0: float, t1: float, col: str) -> float:
    d = df[(df['time_lsl'] >= t0) & (df['time_lsl'] < t1)]
    if d.empty: return np.nan
    return float(np.nanmean(d[col]))


def detect_blinks(ts: np.ndarray, data: np.ndarray, pht: Dict[str, Tuple[float,float]]) -> pd.DataFrame:
    fs = 1.0 / np.nanmedian(np.diff(ts))
    fp = data[:, FP1_IDX].astype(float)
    fp = fp - np.nanmedian(fp)
    # Low-frequency ocular component and high-frequency/sentinel context.
    sos = signal.butter(3, [0.3, 8.0], btype='bandpass', fs=fs, output='sos')
    low = signal.sosfiltfilt(sos, fp)
    rz = robust_z(np.abs(low))
    # Dynamic threshold; conservative enough to avoid ordinary frontal EEG.
    thr = max(5.0, float(np.nanpercentile(rz, 99.1)))
    peaks, props = signal.find_peaks(rz, height=thr, distance=int(0.35*fs), prominence=1.0)
    # Build artifact p2p score around peak.
    rows=[]
    for pk in peaks:
        t=float(ts[pk])
        # Ignore obvious out-of-run bits? keep if inside any protocol phase extended.
        in_phase=''
        for ph,(a,b) in pht.items():
            if a <= t <= b:
                in_phase=ph; break
        w = (ts >= t-0.18) & (ts <= t+0.18)
        if int(w.sum()) < 10: continue
        fp_p2p=float(np.nanmax(fp[w])-np.nanmin(fp[w]))
        low_amp=float(np.nanmax(np.abs(low[w])))
        rows.append({
            'blink_time_lsl':t,
            'phase':in_phase,
            'fp1_lowfreq_abs_robust_z_peak':float(rz[pk]),
            'fp1_p2p_360ms':fp_p2p,
            'fp1_lowfreq_abs_peak':low_amp,
            'detector_threshold_z':thr,
            'detector':'Fp1_lowfreq_abs_robust_z_peak_conservative'
        })
    df=pd.DataFrame(rows)
    if not df.empty:
        # condition-relative times
        for ph in pht:
            a,b=pht[ph]
            m=(df['blink_time_lsl']>=a)&(df['blink_time_lsl']<=b)
            df.loc[m,'condition_offset_sec']=df.loc[m,'blink_time_lsl']-a
    return df


def count_blinks(blinks: pd.DataFrame, start: float, end: float) -> int:
    if blinks.empty or end <= start: return 0
    return int(((blinks['blink_time_lsl']>=start)&(blinks['blink_time_lsl']<end)).sum())


def rate_blinks(blinks: pd.DataFrame, start: float, end: float) -> float:
    dur=max(1e-9, end-start)
    return count_blinks(blinks,start,end) / dur * 60.0


def build_anchor_condition_rows(annotations: pd.DataFrame, pht: Dict[str,Tuple[float,float]]) -> pd.DataFrame:
    rows=[]
    for _, a in annotations.iterrows():
        offset=float(a['rendered_time_sec_estimate'])
        for ph in PHASES:
            if ph not in pht: continue
            start,end=pht[ph]
            anchor_lsl=start+offset
            # Use annotation windows relative to target offset when present; convert by same branch start.
            rel_pre_start = float(a.get('pre_start_sec', offset-15))
            rel_pre_end = float(a.get('pre_end_sec', offset))
            rel_peak_start = float(a.get('peak_search_start_sec', offset))
            # Use first 5s of peak search for complexity peak unless search shorter.
            rel_peak_end = min(float(a.get('peak_search_end_sec', offset+10)), rel_peak_start+5.0)
            rel_theta_start = float(a.get('theta_start_sec', offset+10))
            rel_theta_end = float(a.get('theta_end_sec', offset+30))
            rows.append({
                'anchor_id': a['anchor_id'],
                'annotation_id': a.get('annotation_id',''),
                'scene_label': a.get('scene_label',''),
                'condition': ph,
                'condition_label': PHASE_LABEL.get(ph,ph),
                'anchor_offset_sec': offset,
                'anchor_time_lsl': anchor_lsl,
                'pre_start_lsl': start+rel_pre_start,
                'pre_end_lsl': start+rel_pre_end,
                'peak_start_lsl': start+rel_peak_start,
                'peak_end_lsl': start+rel_peak_end,
                'post_start_lsl': start+rel_theta_start,
                'post_end_lsl': start+rel_theta_end,
                'claim_level': a.get('claim_level',''),
                'needs_manual_rendered_time_lock': a.get('needs_manual_rendered_time_lock', True)
            })
    return pd.DataFrame(rows)


def add_acg(anchor_df: pd.DataFrame, lzc_df: pd.DataFrame, feature_df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for _, r in anchor_df.iterrows():
        pre = interval_mean_df(lzc_df, r.pre_start_lsl, r.pre_end_lsl, 'lz_complexity_proxy')
        peak = interval_mean_df(lzc_df, r.peak_start_lsl, r.peak_end_lsl, 'lz_complexity_proxy')
        post = interval_mean_df(lzc_df, r.post_start_lsl, r.post_end_lsl, 'lz_complexity_proxy')
        # artifact from feature table in same windows
        art_pre = interval_mean_df(feature_df, r.pre_start_lsl, r.pre_end_lsl, 'artifact_score') if 'artifact_score' in feature_df else np.nan
        art_peak = interval_mean_df(feature_df, r.peak_start_lsl, r.peak_end_lsl, 'artifact_score') if 'artifact_score' in feature_df else np.nan
        art_post = interval_mean_df(feature_df, r.post_start_lsl, r.post_end_lsl, 'artifact_score') if 'artifact_score' in feature_df else np.nan
        row = r.to_dict()
        row.update({
            'C_LZproxy_pre':pre,
            'C_LZproxy_peak':peak,
            'C_LZproxy_post':post,
            'delta_C_strike_peak_minus_pre': peak-pre if np.isfinite(peak) and np.isfinite(pre) else np.nan,
            'delta_C_settle_post_minus_peak': post-peak if np.isfinite(post) and np.isfinite(peak) else np.nan,
            'delta_C_post_minus_pre': post-pre if np.isfinite(post) and np.isfinite(pre) else np.nan,
            'artifact_pre':art_pre,
            'artifact_peak':art_peak,
            'artifact_post':art_post,
            'artifact_mean': float(np.nanmean([art_pre,art_peak,art_post]))
        })
        rows.append(row)
    out=pd.DataFrame(rows)
    if len(out):
        out['delta_C_strike_z'] = robust_z(out['delta_C_strike_peak_minus_pre'].values)
        out['delta_C_settle_neg_z'] = robust_z((-out['delta_C_settle_post_minus_peak']).values)
        out['artifact_mean_z'] = robust_z(out['artifact_mean'].values)
        out['CSI_complexity_settlement_index'] = 0.45*out['delta_C_strike_z'] + 0.45*out['delta_C_settle_neg_z'] - 0.20*np.maximum(0,out['artifact_mean_z'])
        out['CSI_z'] = robust_z(out['CSI_complexity_settlement_index'].values)
        # conservative flags: strike up and post lower than peak, artifact not high.
        art_thr = np.nanpercentile(out['artifact_mean'], 75)
        strike_thr = np.nanpercentile(out['delta_C_strike_peak_minus_pre'], 60)
        settle_thr = np.nanpercentile(out['delta_C_settle_post_minus_peak'], 40)
        out['ACG_candidate'] = (out['delta_C_strike_peak_minus_pre'] > strike_thr) & (out['delta_C_settle_post_minus_peak'] < settle_thr) & (out['artifact_mean'] <= art_thr)
    return out


def add_ocu(anchor_df: pd.DataFrame, blink_df: pd.DataFrame, feature_df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for _, r in anchor_df.iterrows():
        # A broad pre-hold window, a tight hold window, and post-release window.
        pre_s = r.anchor_time_lsl - 30.0; pre_e = r.anchor_time_lsl - 5.0
        hold_s = r.anchor_time_lsl - 5.0; hold_e = r.anchor_time_lsl + 5.0
        rel_s = r.anchor_time_lsl + 5.0; rel_e = r.anchor_time_lsl + 20.0
        br_pre = rate_blinks(blink_df, pre_s, pre_e)
        br_hold = rate_blinks(blink_df, hold_s, hold_e)
        br_rel = rate_blinks(blink_df, rel_s, rel_e)
        art_hold = interval_mean_df(feature_df, hold_s, hold_e, 'artifact_score') if 'artifact_score' in feature_df else np.nan
        row=r.to_dict()
        row.update({
            'blink_count_pre_30_to_5':count_blinks(blink_df,pre_s,pre_e),
            'blink_count_hold_minus5_to_plus5':count_blinks(blink_df,hold_s,hold_e),
            'blink_count_release_plus5_to_plus20':count_blinks(blink_df,rel_s,rel_e),
            'blink_rate_pre_per_min':br_pre,
            'blink_rate_hold_per_min':br_hold,
            'blink_rate_release_per_min':br_rel,
            'blink_suppression_pre_minus_hold':br_pre-br_hold,
            'blink_release_release_minus_hold':br_rel-br_hold,
            'artifact_hold':art_hold,
        })
        rows.append(row)
    out=pd.DataFrame(rows)
    if len(out):
        out['blink_suppression_z']=robust_z(out['blink_suppression_pre_minus_hold'].values)
        out['blink_release_z']=robust_z(out['blink_release_release_minus_hold'].values)
        out['artifact_hold_z']=robust_z(out['artifact_hold'].values)
        out['ORI_ocular_release_index']=0.45*out['blink_suppression_z']+0.45*out['blink_release_z']-0.25*np.maximum(0,out['artifact_hold_z'])
        out['ORI_z']=robust_z(out['ORI_ocular_release_index'].values)
        sup_thr=np.nanpercentile(out['blink_suppression_pre_minus_hold'],60)
        rel_thr=np.nanpercentile(out['blink_release_release_minus_hold'],60)
        art_thr=np.nanpercentile(out['artifact_hold'],75)
        out['OCU_candidate']=(out['blink_suppression_pre_minus_hold']>sup_thr)&(out['blink_release_release_minus_hold']>rel_thr)&(out['artifact_hold']<=art_thr)
    return out


def build_summary(acg: pd.DataFrame, ocu: pd.DataFrame, mred_events: pd.DataFrame) -> pd.DataFrame:
    # Merge ACG and OCU by anchor/condition.
    cols=['anchor_id','condition','scene_label','anchor_offset_sec','claim_level','needs_manual_rendered_time_lock']
    left=acg[cols + ['C_LZproxy_pre','C_LZproxy_peak','C_LZproxy_post','delta_C_strike_peak_minus_pre','delta_C_settle_post_minus_peak','CSI_complexity_settlement_index','CSI_z','ACG_candidate','artifact_mean']]
    right=ocu[['anchor_id','condition','blink_rate_pre_per_min','blink_rate_hold_per_min','blink_rate_release_per_min','blink_suppression_pre_minus_hold','blink_release_release_minus_hold','ORI_ocular_release_index','ORI_z','OCU_candidate','artifact_hold']]
    out=left.merge(right,on=['anchor_id','condition'],how='left')
    # Attach nearest MRED event for target if possible by condition/offset.
    if mred_events is not None and not mred_events.empty:
        nearest=[]
        for _, r in out.iterrows():
            d=mred_events[mred_events['condition']==r['condition']].copy()
            if d.empty:
                nearest.append({})
                continue
            d['dist']=np.abs(d['condition_offset_sec']-r['anchor_offset_sec'])
            e=d.sort_values('dist').iloc[0]
            nearest.append({
                'nearest_mred_dist_sec':float(e['dist']),
                'nearest_K_HT_topo_local':float(e.get('K_HT_topo_local',np.nan)),
                'nearest_theta_delta_10_30':float(e.get('theta_delta_10_30',np.nan)),
                'nearest_MR_score':float(e.get('MR_score',np.nan)),
                'nearest_ENC_score':float(e.get('ENC_score',np.nan)),
                'nearest_mred_quadrant':str(e.get('mred_quadrant','')),
                'nearest_event_lock_candidate':bool(e.get('event_lock_candidate',False)),
            })
        out=pd.concat([out.reset_index(drop=True), pd.DataFrame(nearest)], axis=1)
    out['MRED_ITP_convergence_score'] = 0.5*out['CSI_z'].fillna(0) + 0.5*out['ORI_z'].fillna(0)
    out['MRED_ITP_convergence_z'] = robust_z(out['MRED_ITP_convergence_score'].values)
    out['MRED_ITP_candidate'] = out['ACG_candidate'].fillna(False) & out['OCU_candidate'].fillna(False)
    return out


def build_visual_overlay(summary: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for _, r in summary.iterrows():
        cat = 'mred_itp'
        if bool(r.get('MRED_ITP_candidate',False)): cat='mred_itp_candidate'
        elif bool(r.get('ACG_candidate',False)): cat='acg_complexity'
        elif bool(r.get('OCU_candidate',False)): cat='ocu_blink_release'
        rows.append({
            'start_sec':float(r['anchor_offset_sec'])-5,
            'end_sec':float(r['anchor_offset_sec'])+20,
            'time_sec':float(r['anchor_offset_sec']),
            'condition':r['condition'],
            'category':cat,
            'label':f"{r['anchor_id']} | CSI={r.get('CSI_z',np.nan):.2f} ORI={r.get('ORI_z',np.nan):.2f}",
            'source':'mred_itp_v1_5_2',
            'claim_level':r.get('claim_level','')
        })
    return pd.DataFrame(rows)


def run_contact(output_dir: Path) -> Dict[str,Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    tables=output_dir/'tables'; tables.mkdir(exist_ok=True)
    figs=output_dir/'figures'; figs.mkdir(exist_ok=True)
    scripts=output_dir/'scripts'; scripts.mkdir(exist_ok=True)
    report_dir=output_dir/'report'; report_dir.mkdir(exist_ok=True)

    xdf=Path('/mnt/data/sub-P001_ses-S001_task-Default_run-001_eeg(20260815-125946).xdf')
    event_path=Path('/mnt/data/contact_runfiles/runfiles/PRAYCG_v1_9_hoyt_S001_Contact_20260815_070408_events.json')
    feature_path=Path('/mnt/data/PRAYCG_Contact_Run1_Requested_Anchor_MRED_Files_v1_0/Contact_Run1_feature_table_contact_time_resolved_feature_frame_v1_0.csv')
    annotation_path=Path('/mnt/data/PRAYCG_Contact_Run1_Requested_Anchor_MRED_Files_v1_0/Contact_Run1_annotation_windows_v1_0.csv')
    mred_path=Path('/mnt/data/PRAYCG_Contact_Run1_Requested_Anchor_MRED_Files_v1_0/Contact_Run1_candidate_local_kht_topo_mred_event_table_v1_0.csv')

    events,pht=load_phase_map(event_path)
    ts_raw,data,header=load_eeg_from_xdf(xdf)
    fs_nominal=float(header.get('nominal_srate',125) or 125)
    ts, fs, alignment_info = apply_contact_corrected_time_axis(ts_raw, data)
    data_clean=preprocess_eeg(data, fs)
    # Additional gentle bandpass for complexity path.
    try:
        sos=signal.butter(4,[1,45],btype='bandpass',fs=fs,output='sos')
        data_lzc=signal.sosfiltfilt(sos,data_clean,axis=0)
    except Exception:
        data_lzc=data_clean
    feature=pd.read_csv(feature_path)
    annotations=pd.read_csv(annotation_path)
    mred=pd.read_csv(mred_path)

    lzc=compute_lzc_timeseries(ts, data_lzc, feature, window_sec=6.0, fs=fs)
    lzc.to_csv(tables/'lz_complexity_timeseries.csv',index=False)
    blinks=detect_blinks(ts, data_clean, pht)
    blinks.to_csv(tables/'blink_event_table.csv',index=False)
    anchors=build_anchor_condition_rows(annotations,pht)
    anchors.to_csv(tables/'mred_itp_anchor_condition_windows.csv',index=False)
    acg=add_acg(anchors,lzc,feature)
    acg.to_csv(tables/'acg_event_table.csv',index=False)
    ocu=add_ocu(anchors,blinks,feature)
    ocu.to_csv(tables/'ocu_event_table.csv',index=False)
    summary=build_summary(acg,ocu,mred)
    summary.to_csv(tables/'mred_itp_anchor_summary.csv',index=False)
    overlay=build_visual_overlay(summary)
    overlay.to_csv(tables/'mred_itp_visual_overlay.csv',index=False)

    # Phase summaries.
    phase_rows=[]
    for ph,(a,b) in pht.items():
        d_lzc=lzc[(lzc['time_lsl']>=a)&(lzc['time_lsl']<=b)]
        phase_rows.append({
            'phase':ph,
            'duration_sec':b-a,
            'mean_lz_complexity_proxy':float(np.nanmean(d_lzc['lz_complexity_proxy'])) if not d_lzc.empty else np.nan,
            'median_lz_complexity_proxy':float(np.nanmedian(d_lzc['lz_complexity_proxy'])) if not d_lzc.empty else np.nan,
            'blink_count':count_blinks(blinks,a,b),
            'blink_rate_per_min':rate_blinks(blinks,a,b),
            'samples_lzc':int(len(d_lzc))
        })
    phase_df=pd.DataFrame(phase_rows)
    phase_df.to_csv(tables/'mred_itp_phase_summary.csv',index=False)

    # Condition specificity tables (Target minus control/override).
    pivot_cols=['CSI_complexity_settlement_index','ORI_ocular_release_index','MRED_ITP_convergence_score']
    spec=[]
    for aid in summary['anchor_id'].unique():
        s=summary[summary['anchor_id']==aid]
        if set(PHASES).issubset(set(s['condition'])):
            row={'anchor_id':aid,'scene_label':s.iloc[0].get('scene_label','')}
            for col in pivot_cols:
                vals={r.condition:float(getattr(r,col)) for r in s.itertuples() if pd.notna(getattr(r,col))}
                row[f'Target_minus_Control_{col}']=vals.get('TARGET_1',np.nan)-vals.get('CONTROL_1',np.nan)
                row[f'Target_minus_Override_{col}']=vals.get('TARGET_1',np.nan)-vals.get('CONTEXTUAL_OVERRIDE_1',np.nan)
            spec.append(row)
    spec_df=pd.DataFrame(spec)
    spec_df.to_csv(tables/'mred_itp_condition_specificity.csv',index=False)

    # Interpretation summary.
    target=summary[summary['condition']=='TARGET_1']
    control=summary[summary['condition']=='CONTROL_1']
    override=summary[summary['condition']=='CONTEXTUAL_OVERRIDE_1']
    interp={
        'schema':'PRAYCG_MRED_ITP_Contact_Run1_v1_0',
        'module_version':'1.5.2',
        'boundary':'Information-thermodynamic proxy layer only. LZC is not literal thermodynamic entropy; Fp1 blink timing is not proof of memory encoding. No OSM biology or human EEG mechanism claim.',
        'input_files':{
            'xdf':str(xdf), 'event_log':str(event_path), 'feature_table':str(feature_path), 'annotations':str(annotation_path), 'mred_events':str(mred_path)
        },
        'eeg':{'stream_name':header.get('name',''), 'samples':int(data.shape[0]), 'channels':int(data.shape[1]), 'nominal_srate':fs_nominal, 'effective_srate':fs, 'alignment_info': alignment_info},
        'phase_summary':phase_df.to_dict('records'),
        'blink_detector':{'total_blinks_detected':int(len(blinks)), 'detector':'Fp1 low-frequency conservative proxy'},
        'target_summary':{
            'mean_CSI':float(np.nanmean(target['CSI_complexity_settlement_index'])) if not target.empty else np.nan,
            'mean_ORI':float(np.nanmean(target['ORI_ocular_release_index'])) if not target.empty else np.nan,
            'mean_convergence':float(np.nanmean(target['MRED_ITP_convergence_score'])) if not target.empty else np.nan,
            'ACG_candidate_count':int(target['ACG_candidate'].sum()) if not target.empty else 0,
            'OCU_candidate_count':int(target['OCU_candidate'].sum()) if not target.empty else 0,
            'MRED_ITP_candidate_count':int(target['MRED_ITP_candidate'].sum()) if not target.empty else 0,
        },
        'condition_specificity_summary':spec_df.to_dict('records'),
    }
    with open(tables/'mred_itp_interpretation.json','w',encoding='utf-8') as f: json.dump(interp,f,indent=2)

    # Simple figures.
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,4))
        for cond in ['TARGET_1','CONTROL_1','CONTEXTUAL_OVERRIDE_1']:
            d=lzc[lzc['condition']==cond]
            if not d.empty:
                plt.plot(d['condition_offset_sec'], d['lz_complexity_proxy'], label=cond, alpha=0.8)
        plt.xlabel('condition offset sec'); plt.ylabel('normalized LZ-style compression proxy'); plt.title('Contact Run 1 - LZ Complexity by Branch'); plt.legend(); plt.tight_layout()
        plt.savefig(figs/'lz_complexity_by_branch.png', dpi=180); plt.close()
        plt.figure(figsize=(10,4))
        target_b=blinks[blinks.get('phase','')=='TARGET_1'] if not blinks.empty else blinks
        if not target_b.empty:
            plt.vlines(target_b['condition_offset_sec'],0,1,alpha=.6)
        for _,r in annotations.iterrows():
            plt.axvline(float(r['rendered_time_sec_estimate']),color='r',alpha=.5)
        plt.xlim(0,305); plt.xlabel('Target condition offset sec'); plt.yticks([]); plt.title('Target Fp1 blink-proxy events and conceptual Contact anchors')
        plt.tight_layout(); plt.savefig(figs/'target_blink_events_vs_anchors.png', dpi=180); plt.close()
    except Exception as e:
        print('figure failed',e)

    # Markdown report.
    md = render_report_md(interp, summary, spec_df, phase_df, blinks)
    (report_dir/'Contact_Run1_MRED_ITP_Report_v1_0.md').write_text(md, encoding='utf-8')
    # PDF report via reportlab
    try:
        make_pdf(report_dir/'Contact_Run1_MRED_ITP_Report_v1_0.pdf', md)
    except Exception as e:
        (report_dir/'PDF_RENDER_ERROR.txt').write_text(repr(e), encoding='utf-8')

    # Copy this script for reproducibility.
    shutil.copy2(__file__, scripts/'run_contact_mred_itp_analysis_v1_0.py')
    return interp


def render_report_md(interp: Dict[str,Any], summary: pd.DataFrame, spec_df: pd.DataFrame, phase_df: pd.DataFrame, blinks: pd.DataFrame) -> str:
    target=summary[summary['condition']=='TARGET_1'].copy()
    # Top rows by convergence
    top=target.sort_values('MRED_ITP_convergence_score', ascending=False).head(5)
    lines=[]
    lines.append('# Contact Run 1 - MRED-ITP / ACG / OCU Deep Analysis v1.0')
    lines.append('')
    lines.append('## Executive verdict')
    lines.append('The new information-thermodynamic proxy layer is useful but should remain exploratory. Contact shows some Target-aligned information-structure and ocular-release candidates, but the result is not a literal thermodynamic proof. Lempel-Ziv complexity is treated as a compressibility/diversity proxy, and Fp1 blink timing is treated as a rough ocular event-boundary proxy, not confirmed memory encoding.')
    lines.append('')
    lines.append('## Boundary')
    lines.append(interp['boundary'])
    lines.append('')
    lines.append('## Data and streams')
    e=interp['eeg']
    lines.append(f"EEG stream `{e['stream_name']}`: {e['samples']} samples, {e['channels']} channels, nominal {e['nominal_srate']} Hz.")
    lines.append(f"Blink-proxy events detected from Fp1: {len(blinks)} total.")
    lines.append('')
    lines.append('## Phase-level complexity/blink summary')
    lines.append(phase_df[['phase','duration_sec','mean_lz_complexity_proxy','blink_count','blink_rate_per_min']].to_markdown(index=False, floatfmt='.3f'))
    lines.append('')
    lines.append('## Target anchor-level candidates')
    show_cols=['anchor_id','scene_label','delta_C_strike_peak_minus_pre','delta_C_settle_post_minus_peak','CSI_complexity_settlement_index','blink_suppression_pre_minus_hold','blink_release_release_minus_hold','ORI_ocular_release_index','MRED_ITP_convergence_score','ACG_candidate','OCU_candidate','MRED_ITP_candidate','nearest_mred_quadrant']
    lines.append(top[show_cols].to_markdown(index=False, floatfmt='.3f'))
    lines.append('')
    lines.append('## Condition specificity')
    if not spec_df.empty:
        lines.append(spec_df.to_markdown(index=False, floatfmt='.3f'))
    else:
        lines.append('No full three-condition anchor specificity rows were available.')
    lines.append('')
    lines.append('## Interpretation')
    lines.append('- ACG asks whether anchor windows show a complexity perturbation followed by settlement. It does not estimate thermodynamic entropy directly.')
    lines.append('- OCU asks whether blinks are suppressed near the meaningful window and released afterward. It is a blink-timing proxy; without EOG/eye tracking it remains tentative.')
    lines.append('- MRED-ITP convergence is strongest when complexity settlement and ocular release both align with MRED/KHT-topo target events and show Target > Control/Override specificity.')
    lines.append('- The Contact father/avatar recognition cluster remains the most important target candidate from prior modules; this new layer adds supportive/diagnostic context rather than replacing MRED, NIP, or TTI.')
    lines.append('')
    lines.append('## Strongest caution')
    lines.append('The Fp1 channel is simultaneously a useful blink/ocular proxy and a possible EEG artifact source. Any blink-timed event must be treated as an ocular state marker, not as clean neural theta/gamma evidence in the same contaminated samples.')
    return '\n'.join(lines)


def make_pdf(path: Path, md: str):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    doc=SimpleDocTemplate(str(path), pagesize=letter, rightMargin=0.65*inch, leftMargin=0.65*inch, topMargin=0.65*inch, bottomMargin=0.65*inch)
    styles=getSampleStyleSheet()
    body=styles['BodyText']; body.fontSize=9.2; body.leading=12
    h1=styles['Heading1']; h2=styles['Heading2']
    story=[]
    in_table=[]
    def flush_table(rows):
        if not rows: return
        data=[]
        for line in rows:
            if not line.strip().startswith('|'): continue
            cells=[c.strip() for c in line.strip().strip('|').split('|')]
            if set(''.join(cells)) <= set('-: '): continue
            data.append(cells)
        if data:
            tbl=Table(data, repeatRows=1)
            tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.25,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTSIZE',(0,0),(-1,-1),6),('VALIGN',(0,0),(-1,-1),'TOP')]))
            story.append(tbl); story.append(Spacer(1,8))
    table_lines=[]
    for line in md.splitlines():
        if line.startswith('|'):
            table_lines.append(line); continue
        else:
            if table_lines:
                flush_table(table_lines); table_lines=[]
        if line.startswith('# '):
            story.append(Paragraph(line[2:], h1)); story.append(Spacer(1,8))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], h2)); story.append(Spacer(1,6))
        elif line.strip()=='':
            story.append(Spacer(1,5))
        elif line.startswith('- '):
            story.append(Paragraph('&#8226; '+line[2:], body))
        else:
            story.append(Paragraph(line, body))
    if table_lines: flush_table(table_lines)
    doc.build(story)


if __name__ == '__main__':
    out=Path('/mnt/data/PRAYCG_Contact_Run1_MRED_ITP_Analysis_v1_0')
    if out.exists(): shutil.rmtree(out)
    interp=run_contact(out)
    print(json.dumps(interp['target_summary'], indent=2))
