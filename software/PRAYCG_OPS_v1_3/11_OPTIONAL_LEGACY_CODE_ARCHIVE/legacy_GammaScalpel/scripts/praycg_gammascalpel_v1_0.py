#!/usr/bin/env python3
"""
PR-AYC-G GammaScalpel v1.0

Exploratory spatial x spectral x rigidity analysis for PR-AYC-G EEG runs.
This script intentionally avoids pyxdf by including a small XDF reader for float32 streams.
It is designed for OpenBCI 16-channel PRAYCG16_FIXED_ORDER_v1 runs with optional PolarHRV
and VernierRespirationBelt streams.

Allowed interpretation: exploratory decomposition of gamma-band work into task-like,
meaning-candidate, visual-control, and artifact-sensitive components.
Not allowed: proof that any gamma feature is meaning, consciousness, or a molecular mechanism.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import struct
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
from scipy import signal, stats
import matplotlib.pyplot as plt

# -----------------------------
# Defaults
# -----------------------------
CHANNEL_MAP = {
    1: "Fz", 2: "Cz", 3: "Pz", 4: "F3", 5: "F4", 6: "C3", 7: "C4", 8: "P3",
    9: "P4", 10: "T5", 11: "T6", 12: "O1", 13: "O2", 14: "T3", 15: "T4", 16: "Fp1",
}
ROIS = {
    "frontal_task": ["Fz", "F3", "F4"],
    "frontoparietal_task": ["Fz", "F3", "F4", "Pz", "P3", "P4"],
    "central": ["Cz", "C3", "C4"],
    "posterior_temporal": ["T5", "T6"],
    "meaning_candidate": ["Cz", "C3", "C4", "T5", "T6"],
    "parietal": ["Pz", "P3", "P4"],
    "visual_control": ["O1", "O2"],
    "artifact_sentinel": ["Fp1", "T3", "T4"],
    "jaw_temporal_sentinel": ["T3", "T4"],
    "blink_sentinel": ["Fp1"],
    "non_sentinel": ["Fz", "Cz", "Pz", "F3", "F4", "C3", "C4", "P3", "P4", "T5", "T6", "O1", "O2"],
    "primary_content_core": ["Fz", "Cz", "Pz", "F3", "F4", "C3", "C4", "P3", "P4", "T5", "T6"],
    "all_16": ["Fz", "Cz", "Pz", "F3", "F4", "C3", "C4", "P3", "P4", "T5", "T6", "O1", "O2", "T3", "T4", "Fp1"],
}
BANDS = {
    "theta_4_8": (4.0, 8.0),
    "alpha_8_12": (8.0, 12.0),
    "beta_13_30": (13.0, 30.0),
    "gamma_30_35": (30.0, 35.0),
    "gamma_35_40": (35.0, 40.0),
    "gamma_40_45": (40.0, 45.0),
    "low_gamma_30_45": (30.0, 45.0),
    "hf_proxy_45_55": (45.0, 55.0),
}
GAMMA_BINS = ["gamma_30_35", "gamma_35_40", "gamma_40_45", "low_gamma_30_45"]
MICRO_GAMMA_BINS = ["gamma_30_35", "gamma_35_40", "gamma_40_45"]
SYNC_ROIS = {"frontoparietal_task", "meaning_candidate", "visual_control", "artifact_sentinel", "primary_content_core", "non_sentinel"}

# -----------------------------
# XDF reader (minimal float32 stream support)
# -----------------------------
@dataclass
class XDFStream:
    stream_id: int
    name: str
    stype: str
    channel_count: int
    channel_format: str
    nominal_srate: float
    time_stamps: np.ndarray
    time_series: np.ndarray
    info_xml: str


def _read_varlen_int(f) -> Optional[int]:
    lb = f.read(1)
    if not lb:
        return None
    n = lb[0]
    if n == 0:
        return 0
    b = f.read(n)
    if len(b) != n:
        return None
    return int.from_bytes(b, "little", signed=False)


def _xml_text(root: ET.Element, tag: str, default: str = "") -> str:
    node = root.find(tag)
    return node.text if node is not None and node.text is not None else default


def _interp_nan_timestamps(ts: np.ndarray, fs: float) -> np.ndarray:
    ts = ts.astype(float)
    idx = np.arange(len(ts))
    mask = np.isfinite(ts)
    if mask.all():
        return ts
    if mask.sum() >= 2:
        filled = np.interp(idx, idx[mask], ts[mask])
        # Extrapolate edges using median spacing or nominal srate
        finite = ts[mask]
        d = np.median(np.diff(finite)) if len(finite) > 1 else (1.0 / fs if fs and fs > 0 else 0.0)
        first = idx[mask][0]
        last = idx[mask][-1]
        if first > 0:
            filled[:first] = filled[first] - (first - idx[:first]) * d
        if last < len(ts) - 1:
            filled[last+1:] = filled[last] + (idx[last+1:] - last) * d
        return filled
    if mask.sum() == 1:
        d = 1.0 / fs if fs and fs > 0 else 0.0
        anchor_i = idx[mask][0]
        anchor_t = ts[mask][0]
        return anchor_t + (idx - anchor_i) * d
    # No timestamps: fabricate from zero. This should not happen in valid XDF.
    d = 1.0 / fs if fs and fs > 0 else 1.0
    return idx * d


def load_xdf_minimal(xdf_path: str | Path) -> Dict[str, XDFStream]:
    xdf_path = Path(xdf_path)
    headers: Dict[int, dict] = {}
    samples: Dict[int, List[np.ndarray]] = {}
    stamps: Dict[int, List[np.ndarray]] = {}

    with xdf_path.open("rb") as f:
        magic = f.read(4)
        if magic != b"XDF:":
            raise ValueError(f"Not an XDF file: {xdf_path}")
        while True:
            pos = f.tell()
            length = _read_varlen_int(f)
            if length is None:
                break
            tag_b = f.read(2)
            if len(tag_b) != 2:
                break
            tag = struct.unpack("<H", tag_b)[0]
            payload = f.read(length - 2)
            if len(payload) != length - 2:
                break
            if tag == 2:  # StreamHeader
                sid = struct.unpack("<I", payload[:4])[0]
                xml = payload[4:].decode("utf-8", errors="replace")
                try:
                    root = ET.fromstring(xml)
                    name = _xml_text(root, "name", f"stream_{sid}")
                    stype = _xml_text(root, "type", "")
                    ch = int(float(_xml_text(root, "channel_count", "1")))
                    fmt = _xml_text(root, "channel_format", "float32")
                    fs = float(_xml_text(root, "nominal_srate", "0") or 0)
                except Exception:
                    name, stype, ch, fmt, fs = f"stream_{sid}", "", 1, "float32", 0.0
                headers[sid] = {"name": name, "type": stype, "channel_count": ch, "format": fmt, "fs": fs, "xml": xml}
            elif tag == 3:  # Samples
                if len(payload) < 9:
                    continue
                sid = struct.unpack("<I", payload[:4])[0]
                if sid not in headers:
                    continue
                h = headers[sid]
                if h["format"] not in {"float32", "double64", "int32", "int16"}:
                    # String streams can be added later; not required for present analysis.
                    continue
                nchan = h["channel_count"]
                pos2 = 4
                nlen = payload[pos2]
                pos2 += 1
                nsamp = int.from_bytes(payload[pos2:pos2+nlen], "little", signed=False)
                pos2 += nlen
                vals = []
                ts = []
                if h["format"] == "float32":
                    val_fmt = "<" + "f" * nchan
                    val_bytes = 4 * nchan
                elif h["format"] == "double64":
                    val_fmt = "<" + "d" * nchan
                    val_bytes = 8 * nchan
                elif h["format"] == "int32":
                    val_fmt = "<" + "i" * nchan
                    val_bytes = 4 * nchan
                else:
                    val_fmt = "<" + "h" * nchan
                    val_bytes = 2 * nchan
                for _ in range(nsamp):
                    if pos2 >= len(payload):
                        break
                    tlen = payload[pos2]
                    pos2 += 1
                    if tlen == 0:
                        t = np.nan
                    elif tlen == 8 and pos2 + 8 <= len(payload):
                        t = struct.unpack("<d", payload[pos2:pos2+8])[0]
                        pos2 += 8
                    elif tlen == 4 and pos2 + 4 <= len(payload):
                        t = struct.unpack("<f", payload[pos2:pos2+4])[0]
                        pos2 += 4
                    else:
                        # Unknown timestamp payload; skip declared bytes and mark nan
                        pos2 += max(tlen, 0)
                        t = np.nan
                    if pos2 + val_bytes > len(payload):
                        break
                    v = struct.unpack(val_fmt, payload[pos2:pos2+val_bytes])
                    pos2 += val_bytes
                    vals.append(v)
                    ts.append(t)
                if vals:
                    samples.setdefault(sid, []).append(np.asarray(vals, dtype=float))
                    stamps.setdefault(sid, []).append(np.asarray(ts, dtype=float))

    out: Dict[str, XDFStream] = {}
    for sid, h in headers.items():
        if sid in samples:
            data = np.vstack(samples[sid])
            ts = np.concatenate(stamps[sid])
            ts = _interp_nan_timestamps(ts, h["fs"])
            out[h["name"]] = XDFStream(
                stream_id=sid, name=h["name"], stype=h["type"], channel_count=h["channel_count"],
                channel_format=h["format"], nominal_srate=h["fs"], time_stamps=ts, time_series=data,
                info_xml=h["xml"]
            )
    return out

# -----------------------------
# Signal helpers
# -----------------------------

def robust_z(x: pd.Series | np.ndarray) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    med = np.nanmedian(a)
    mad = np.nanmedian(np.abs(a - med))
    scale = 1.4826 * mad if mad > 1e-12 else np.nanstd(a)
    if not np.isfinite(scale) or scale < 1e-12:
        return np.zeros_like(a, dtype=float)
    return (a - med) / scale


def butter_band(data: np.ndarray, fs: float, lo: float, hi: float, order: int = 4) -> np.ndarray:
    hi = min(hi, fs / 2 - 0.5)
    lo = max(lo, 0.5)
    if hi <= lo:
        raise ValueError(f"Invalid band {lo}-{hi} for fs={fs}")
    sos = signal.butter(order, [lo, hi], btype="band", fs=fs, output="sos")
    return signal.sosfiltfilt(sos, data, axis=0)


def analytic_phase_amp(filtered: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    h = signal.hilbert(filtered, axis=0)
    return np.angle(h), np.abs(h)


def mean_log_power(filtered_win: np.ndarray, idxs: List[int]) -> float:
    if len(idxs) == 0 or filtered_win.shape[0] < 8:
        return np.nan
    x = filtered_win[:, idxs]
    # variance of bandpassed signal is band-limited power proxy
    p = np.nanmedian(np.nanmean(x * x, axis=0))
    return float(np.log10(p + 1e-12))


def plv_roi(phase_win: np.ndarray, idxs: List[int]) -> float:
    if len(idxs) < 2 or phase_win.shape[0] < 8:
        return np.nan
    vals = []
    for a in range(len(idxs)):
        for b in range(a+1, len(idxs)):
            d = phase_win[:, idxs[a]] - phase_win[:, idxs[b]]
            vals.append(abs(np.nanmean(np.exp(1j * d))))
    return float(np.nanmedian(vals)) if vals else np.nan


def tort_mi(theta_phase: np.ndarray, gamma_amp: np.ndarray, n_bins: int = 18) -> float:
    mask = np.isfinite(theta_phase) & np.isfinite(gamma_amp)
    if mask.sum() < n_bins * 4:
        return np.nan
    ph = theta_phase[mask]
    amp = gamma_amp[mask]
    edges = np.linspace(-np.pi, np.pi, n_bins + 1)
    means = np.zeros(n_bins, dtype=float)
    for i in range(n_bins):
        m = (ph >= edges[i]) & (ph < edges[i+1])
        means[i] = np.nanmean(amp[m]) if m.any() else 0.0
    if np.sum(means) <= 0:
        return np.nan
    p = means / np.sum(means)
    p = np.clip(p, 1e-12, 1)
    ent = -np.sum(p * np.log(p))
    return float((np.log(n_bins) - ent) / np.log(n_bins))


def pac_roi(theta_phase_win: np.ndarray, gamma_amp_win: np.ndarray, idxs: List[int]) -> float:
    if len(idxs) == 0 or theta_phase_win.shape[0] < 100:
        return np.nan
    vals = []
    for idx in idxs:
        vals.append(tort_mi(theta_phase_win[:, idx], gamma_amp_win[:, idx]))
    return float(np.nanmedian(vals)) if len(vals) else np.nan

# -----------------------------
# Events/segments
# -----------------------------

def load_events(events_json: str | Path) -> pd.DataFrame:
    with open(events_json, "r", encoding="utf-8") as f:
        events = json.load(f)
    df = pd.DataFrame(events)
    df["lsl_time"] = pd.to_numeric(df["lsl_time"], errors="coerce")
    return df


def marker_time(events: pd.DataFrame, marker: str, prefer_last: bool = False) -> Optional[float]:
    x = events.loc[events["marker"] == marker, "lsl_time"].dropna()
    if len(x) == 0:
        return None
    return float(x.iloc[-1] if prefer_last else x.iloc[0])


def first_marker_matching(events: pd.DataFrame, patterns: Sequence[str]) -> Optional[float]:
    for p in patterns:
        t = marker_time(events, p)
        if t is not None:
            return t
    return None


def build_segments(events: pd.DataFrame) -> pd.DataFrame:
    rows = []
    def add(name, start_marker, end_markers):
        s = marker_time(events, start_marker)
        e = first_marker_matching(events, end_markers)
        if s is not None and e is not None and e > s:
            rows.append({"segment": name, "start": s, "end": e, "duration": e-s, "start_marker": start_marker, "end_marker": "/".join(end_markers)})
    add("Baseline_1", "BASELINE_1_START", ["BASELINE_1_END"])
    add("Control_1", "CONTROL_1_START", ["CONTROL_1_TIMEOUT_BREAK", "CONTROL_1_END"])
    add("Washout_1", "WASHOUT_1_START", ["WASHOUT_1_END"])
    add("Target_1", "TARGET_1_START", ["TARGET_1_TIMEOUT_BREAK", "TARGET_1_END"])
    add("Washout_2", "WASHOUT_2_START", ["WASHOUT_2_END"])
    add("Contextual_Override_1", "CONTEXTUAL_OVERRIDE_1_START", ["CONTEXTUAL_OVERRIDE_1_TIMEOUT_BREAK", "CONTEXTUAL_OVERRIDE_1_END"])
    add("Washout_3", "WASHOUT_3_START", ["WASHOUT_3_END"])
    seg = pd.DataFrame(rows)
    # derived windows
    for base in ["Control_1", "Target_1", "Contextual_Override_1"]:
        r = seg[seg.segment == base]
        if len(r):
            s = float(r.start.iloc[0]); e = float(r.end.iloc[0])
            for n in [20, 30, 40]:
                if e - s > n:
                    rows.append({"segment": f"{base}_final_{n}s", "start": e-n, "end": e, "duration": n, "start_marker": "derived", "end_marker": "derived"})
            if base == "Target_1" and e - s > 40:
                rows.append({"segment": "Target_1_early_excluding_final_40s", "start": s, "end": e-40, "duration": e-40-s, "start_marker": "derived", "end_marker": "derived"})
            if base == "Contextual_Override_1" and e - s > 40:
                rows.append({"segment": "Contextual_Override_1_early_excluding_final_40s", "start": s, "end": e-40, "duration": e-40-s, "start_marker": "derived", "end_marker": "derived"})
    # washout splits
    for w in ["Washout_1", "Washout_2", "Washout_3"]:
        r = seg[seg.segment == w]
        if len(r):
            s = float(r.start.iloc[0]); e = float(r.end.iloc[0])
            splits = [("0_30s", s, min(s+30, e)), ("30_90s", min(s+30, e), min(s+90, e)), ("90_120s", min(s+90, e), e)]
            for lab, a, b in splits:
                if b > a + 5:
                    rows.append({"segment": f"{w}_{lab}", "start": a, "end": b, "duration": b-a, "start_marker": "derived", "end_marker": "derived"})
    return pd.DataFrame(rows).drop_duplicates("segment")


def build_exclusions(events: pd.DataFrame, prepad: float, postpad: float) -> pd.DataFrame:
    rows = []
    # Generic pairs, include all occurrences by order.
    pair_prefixes = [
        ("REPORT_INPUT_START", "REPORT_INPUT_END", "report_input"),
        ("SUM_INPUT_START", "SUM_INPUT_END", "sum_input"),
        ("RETURN_TO_STILLNESS_START", "RETURN_TO_STILLNESS_END", "return_to_stillness"),
    ]
    for start_m, end_m, reason in pair_prefixes:
        starts = events[events.marker == start_m].reset_index(drop=True)
        ends = events[events.marker == end_m].reset_index(drop=True)
        n = min(len(starts), len(ends))
        for i in range(n):
            s = float(starts.loc[i, "lsl_time"]) - prepad
            e = float(ends.loc[i, "lsl_time"]) + postpad
            if e > s:
                rows.append({"reason": reason, "start": s, "end": e, "start_marker": start_m, "end_marker": end_m})
    return pd.DataFrame(rows)


def overlaps_any(start: float, end: float, excl: pd.DataFrame) -> bool:
    if excl.empty:
        return False
    return bool(((excl.start < end) & (excl.end > start)).any())


def make_windows(segments: pd.DataFrame, exclusions: pd.DataFrame, win_len: float, step: float) -> pd.DataFrame:
    rows = []
    for _, r in segments.iterrows():
        s = float(r.start); e = float(r.end)
        k = 0
        t = s
        while t + win_len <= e + 1e-6:
            if not overlaps_any(t, t+win_len, exclusions):
                rows.append({"segment": r.segment, "win_index": k, "start": t, "end": t+win_len, "mid": t+win_len/2})
            k += 1
            t += step
    return pd.DataFrame(rows)

# -----------------------------
# Feature extraction
# -----------------------------

def infer_fs(ts: np.ndarray) -> float:
    d = np.diff(ts)
    d = d[np.isfinite(d) & (d > 0)]
    return float(1.0 / np.median(d)) if len(d) else np.nan


def stream_inventory(streams: Dict[str, XDFStream]) -> pd.DataFrame:
    rows = []
    for name, s in streams.items():
        fs_eff = infer_fs(s.time_stamps)
        rows.append({
            "name": name, "type": s.stype, "stream_id": s.stream_id, "channel_count": s.channel_count,
            "channel_format": s.channel_format, "nominal_srate": s.nominal_srate,
            "effective_srate": fs_eff, "n_samples": len(s.time_stamps),
            "start_time": float(np.nanmin(s.time_stamps)), "end_time": float(np.nanmax(s.time_stamps)),
        })
    return pd.DataFrame(rows)


def find_stream(streams: Dict[str, XDFStream], contains: str) -> Optional[XDFStream]:
    contains_l = contains.lower()
    for name, s in streams.items():
        if contains_l in name.lower() or contains_l in s.stype.lower():
            return s
    return None


def parse_ratings(events: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    pat = re.compile(r"^RATING_(.+?)_([A-Za-z0-9]+)_([0-9]+)$")
    for _, row in events.iterrows():
        m = pat.match(str(row.marker))
        if m:
            phase, item, value = m.group(1), m.group(2), int(m.group(3))
            rows.append({"phase": phase, "item": item, "value": value, "lsl_time": row.lsl_time})
    long = pd.DataFrame(rows)
    wide = long.pivot_table(index="phase", columns="item", values="value", aggfunc="first").reset_index() if len(long) else pd.DataFrame()
    return long, wide


def load_cue_schedule(cue_json: Optional[str | Path]) -> Tuple[pd.DataFrame, dict]:
    if cue_json is None:
        return pd.DataFrame(), {}
    with open(cue_json, "r", encoding="utf-8") as f:
        meta = json.load(f)
    events = meta.get("cue_events", [])
    return pd.DataFrame(events), meta


def compute_features(streams: Dict[str, XDFStream], events: pd.DataFrame, cue_json: Optional[str | Path], out_dir: Path, win_len: float, step: float, prepad: float, postpad: float) -> dict:
    eeg = streams.get("obci_eeg1") or find_stream(streams, "eeg")
    if eeg is None:
        raise RuntimeError("Could not find EEG stream. Expected obci_eeg1 or type EEG.")
    data = np.asarray(eeg.time_series, dtype=float)[:, :16]
    ts = np.asarray(eeg.time_stamps, dtype=float)
    fs = infer_fs(ts)
    labels = [CHANNEL_MAP[i] for i in range(1, 17)]
    label_to_idx = {lab: i for i, lab in enumerate(labels)}
    roi_idx = {roi: [label_to_idx[x] for x in chans if x in label_to_idx] for roi, chans in ROIS.items()}

    # Detrend/simple robust scale per channel to remove DC offsets.
    data = signal.detrend(data, axis=0, type="constant")

    segments = build_segments(events)
    exclusions = build_exclusions(events, prepad, postpad)
    windows = make_windows(segments, exclusions, win_len, step)

    # Filtered bands and analytic transforms
    filt = {}
    phase = {}
    amp = {}
    for band, (lo, hi) in BANDS.items():
        try:
            fdat = butter_band(data, fs, lo, hi, order=4)
        except Exception:
            fdat = np.full_like(data, np.nan)
        filt[band] = fdat
        if band in ["theta_4_8"] + GAMMA_BINS:
            ph, am = analytic_phase_amp(fdat)
            phase[band] = ph
            amp[band] = am

    # Respiration stream
    resp = find_stream(streams, "VernierRespirationBelt") or find_stream(streams, "Resp")
    resp_ts = resp.time_stamps if resp is not None else np.array([])
    resp_x = resp.time_series[:, 0] if resp is not None and resp.time_series.ndim == 2 else np.array([])

    rows = []
    for _, w in windows.iterrows():
        s = float(w.start); e = float(w.end)
        idx = np.where((ts >= s) & (ts < e))[0]
        if len(idx) < int(fs * win_len * 0.5):
            continue
        raw_win = data[idx, :]
        row = {"segment": w.segment, "win_index": int(w.win_index), "start": s, "end": e, "mid": float(w.mid), "n_samples": len(idx)}
        # artifacts
        p2p_ch = np.nanmax(raw_win, axis=0) - np.nanmin(raw_win, axis=0)
        sentinel_idxs = roi_idx["artifact_sentinel"]
        row["median_p2p_all16"] = float(np.nanmedian(p2p_ch))
        row["max_p2p_all16"] = float(np.nanmax(p2p_ch))
        row["median_p2p_sentinel"] = float(np.nanmedian(p2p_ch[sentinel_idxs]))
        row["max_p2p_sentinel"] = float(np.nanmax(p2p_ch[sentinel_idxs]))
        # resp
        if len(resp_ts):
            ridx = np.where((resp_ts >= s) & (resp_ts < e))[0]
            if len(ridx) >= 3:
                rx = resp_x[ridx].astype(float)
                rt = resp_ts[ridx].astype(float)
                row["resp_mean"] = float(np.nanmean(rx))
                row["resp_std"] = float(np.nanstd(rx))
                slope = np.polyfit(rt - rt[0], rx, 1)[0] if len(rt) >= 2 else np.nan
                row["resp_slope"] = float(slope)
            else:
                row["resp_mean"] = row["resp_std"] = row["resp_slope"] = np.nan
        else:
            row["resp_mean"] = row["resp_std"] = row["resp_slope"] = np.nan
        # features by ROI/band
        for roi, idxs in roi_idx.items():
            row[f"{roi}_median_p2p"] = float(np.nanmedian(p2p_ch[idxs])) if idxs else np.nan
            for band in BANDS.keys():
                row[f"{roi}_{band}_logp"] = mean_log_power(filt[band][idx, :], idxs)
            if roi in SYNC_ROIS:
                for band in MICRO_GAMMA_BINS:
                    row[f"{roi}_{band}_plv"] = plv_roi(phase[band][idx, :], idxs)
                    # PAC is computed in a segment-level table, not per-window, for speed/stability.
        rows.append(row)

    feat = pd.DataFrame(rows)
    if feat.empty:
        raise RuntimeError("No valid windows were created.")
    # Add artifact composite robust z.
    for col in ["median_p2p_all16", "max_p2p_all16", "median_p2p_sentinel", "max_p2p_sentinel"]:
        feat[col + "_rz"] = robust_z(feat[col])
    feat["hf_proxy_core_rz"] = robust_z(feat["primary_content_core_hf_proxy_45_55_logp"])
    feat["hf_proxy_sentinel_rz"] = robust_z(feat["artifact_sentinel_hf_proxy_45_55_logp"])
    feat["artifact_composite"] = np.nanmean(np.vstack([
        feat["median_p2p_all16_rz"], feat["max_p2p_all16_rz"],
        feat["median_p2p_sentinel_rz"], feat["max_p2p_sentinel_rz"],
        feat["hf_proxy_core_rz"], feat["hf_proxy_sentinel_rz"],
    ]), axis=0)

    # Control z-scores for key power/PLV/PAC columns.
    control_mask = feat.segment == "Control_1"
    feature_cols = [c for c in feat.columns if c.endswith("_logp") or c.endswith("_plv") or c.endswith("_pac_mi")]
    for c in feature_cols:
        base = feat.loc[control_mask, c]
        mu = np.nanmedian(base) if base.notna().any() else np.nanmedian(feat[c])
        sd = 1.4826 * np.nanmedian(np.abs(base - mu)) if base.notna().any() else np.nanstd(feat[c])
        if not np.isfinite(sd) or sd < 1e-9:
            sd = np.nanstd(feat[c])
        if not np.isfinite(sd) or sd < 1e-9:
            feat[c + "_zcontrol"] = 0.0
        else:
            feat[c + "_zcontrol"] = (feat[c] - mu) / sd

    # GammaScalpel scores per micro-band
    for band in MICRO_GAMMA_BINS:
        feat[f"spatial_gamma_ratio_{band}"] = (
            feat[f"meaning_candidate_{band}_logp_zcontrol"] - feat[f"frontoparietal_task_{band}_logp_zcontrol"]
        )
        feat[f"taskgamma_{band}"] = (
            feat[f"frontoparietal_task_{band}_logp_zcontrol"]
            + feat[f"frontoparietal_task_{band}_plv_zcontrol"]
            - feat["artifact_composite"]
        )
        feat[f"meaninggamma_{band}"] = (
            feat[f"meaning_candidate_{band}_logp_zcontrol"]
            - feat[f"meaning_candidate_{band}_plv_zcontrol"]
            - 0.5 * feat[f"visual_control_{band}_logp_zcontrol"]
            - feat["artifact_composite"]
            - 0.5 * feat[f"taskgamma_{band}"]
        )
    feat["taskgamma_mean_30_45"] = feat[[f"taskgamma_{b}" for b in MICRO_GAMMA_BINS]].mean(axis=1)
    feat["meaninggamma_mean_30_45"] = feat[[f"meaninggamma_{b}" for b in MICRO_GAMMA_BINS]].mean(axis=1)
    feat["task_minus_meaning_gamma"] = feat["taskgamma_mean_30_45"] - feat["meaninggamma_mean_30_45"]

    # Cue/task scoring from events and cue metadata
    cue_df, cue_meta = load_cue_schedule(cue_json)
    scoring = []
    expected_sum = cue_meta.get("expected_sum")
    reported = None
    for m in events.marker.astype(str):
        mm = re.match(r"RESPONSE_CONTEXTUAL_OVERRIDE_1_SUM_(-?\d+)", m)
        if mm:
            reported = int(mm.group(1))
    if reported is None:
        # Older 1.6J marker might be RESPONSE_CONTEXTUAL_OVERRIDE_1_441
        for m in events.marker.astype(str):
            mm = re.match(r"RESPONSE_CONTEXTUAL_OVERRIDE_1_(-?\d+)$", m)
            if mm:
                reported = int(mm.group(1))
    scoring.append({
        "expected_sum": expected_sum,
        "reported_sum": reported,
        "absolute_error": None if expected_sum is None or reported is None else abs(int(expected_sum)-int(reported)),
        "signed_error": None if expected_sum is None or reported is None else int(reported)-int(expected_sum),
        "exact_correct": None if expected_sum is None or reported is None else int(expected_sum)==int(reported),
        "cue_count": cue_meta.get("cue_count", len(cue_df)),
        "cue_interval_sec": cue_meta.get("cue_design", {}).get("interval_sec"),
        "cue_duration_sec": cue_meta.get("cue_design", {}).get("display_duration_sec"),
        "cue_position": cue_meta.get("cue_design", {}).get("position"),
        "cue_visibility_qc_available": False,
    })

    out = {
        "features": feat,
        "segments": segments,
        "exclusions": exclusions,
        "cue_df": cue_df,
        "cue_meta": cue_meta,
        "task_scoring": pd.DataFrame(scoring),
        "ratings_long": parse_ratings(events)[0],
        "ratings_wide": parse_ratings(events)[1],
        "stream_inventory": stream_inventory(streams),
        "fs": fs,
    }
    return out

# -----------------------------
# Summaries / stats
# -----------------------------

def boot_ci_delta(a: np.ndarray, b: np.ndarray, n_boot: int = 500, seed: int = 0) -> Tuple[float, float, float, float]:
    rng = np.random.default_rng(seed)
    a = np.asarray(a, dtype=float); b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) == 0 or len(b) == 0:
        return np.nan, np.nan, np.nan, np.nan
    delta = float(np.nanmedian(a) - np.nanmedian(b))
    boots = []
    for _ in range(n_boot):
        boots.append(np.nanmedian(rng.choice(a, size=len(a), replace=True)) - np.nanmedian(rng.choice(b, size=len(b), replace=True)))
    lo, hi = np.nanpercentile(boots, [2.5, 97.5])
    try:
        p = stats.mannwhitneyu(a, b, alternative="two-sided").pvalue
    except Exception:
        p = np.nan
    return delta, float(lo), float(hi), float(p)


def contrast_table(feat: pd.DataFrame, seg_a: str, seg_b: str, metrics: List[str], label: str) -> pd.DataFrame:
    rows = []
    A = feat[feat.segment == seg_a]
    B = feat[feat.segment == seg_b]
    for metric in metrics:
        if metric not in feat.columns:
            continue
        d, lo, hi, p = boot_ci_delta(A[metric].to_numpy(), B[metric].to_numpy(), seed=hash(metric+label) % (2**32))
        rows.append({"contrast": label, "segA": seg_a, "segB": seg_b, "metric": metric,
                     "nA": int(A[metric].notna().sum()), "nB": int(B[metric].notna().sum()),
                     "delta_median_A_minus_B": d, "ci_low": lo, "ci_high": hi, "p_mwu": p})
    return pd.DataFrame(rows)


def make_segment_summary(feat: pd.DataFrame) -> pd.DataFrame:
    metrics = []
    for band in MICRO_GAMMA_BINS:
        metrics += [
            f"frontoparietal_task_{band}_logp_zcontrol", f"frontoparietal_task_{band}_plv_zcontrol",
            f"meaning_candidate_{band}_logp_zcontrol", f"meaning_candidate_{band}_plv_zcontrol",
            f"spatial_gamma_ratio_{band}", f"taskgamma_{band}", f"meaninggamma_{band}",
            f"visual_control_{band}_logp_zcontrol", f"artifact_sentinel_{band}_logp_zcontrol",
        ]
    metrics += ["taskgamma_mean_30_45", "meaninggamma_mean_30_45", "task_minus_meaning_gamma", "artifact_composite"]
    rows = []
    for seg, g in feat.groupby("segment"):
        for m in metrics:
            if m in g:
                rows.append({"segment": seg, "metric": m, "n": int(g[m].notna().sum()),
                             "median": float(np.nanmedian(g[m])) if g[m].notna().any() else np.nan,
                             "mean": float(np.nanmean(g[m])) if g[m].notna().any() else np.nan,
                             "std": float(np.nanstd(g[m])) if g[m].notna().any() else np.nan})
    return pd.DataFrame(rows)


def run_summaries(feat: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    metrics = []
    power_rois = ["frontoparietal_task", "meaning_candidate", "visual_control", "artifact_sentinel", "jaw_temporal_sentinel", "primary_content_core"]
    plv_rois = ["frontoparietal_task", "meaning_candidate", "visual_control", "artifact_sentinel"]
    for band in MICRO_GAMMA_BINS:
        for roi in power_rois:
            metrics.append(f"{roi}_{band}_logp_zcontrol")
        for roi in plv_rois:
            metrics.append(f"{roi}_{band}_plv_zcontrol")
        metrics += [f"spatial_gamma_ratio_{band}", f"taskgamma_{band}", f"meaninggamma_{band}"]
    metrics += ["taskgamma_mean_30_45", "meaninggamma_mean_30_45", "task_minus_meaning_gamma", "artifact_composite"]
    contrasts = []
    contrast_pairs = [
        ("Target_1", "Contextual_Override_1", "Target_vs_Override_whole"),
        ("Target_1", "Control_1", "Target_vs_Control_whole"),
        ("Contextual_Override_1", "Control_1", "Override_vs_Control_whole"),
        ("Target_1_final_30s", "Contextual_Override_1_final_30s", "TargetFinal30_vs_OverrideFinal30"),
        ("Target_1_final_30s", "Control_1_final_30s", "TargetFinal30_vs_ControlFinal30"),
        ("Washout_2", "Washout_1", "Washout2_vs_Washout1"),
        ("Washout_2", "Washout_3", "Washout2_vs_Washout3"),
    ]
    for a, b, lab in contrast_pairs:
        if a in set(feat.segment) and b in set(feat.segment):
            contrasts.append(contrast_table(feat, a, b, metrics, lab))
    contrast_df = pd.concat(contrasts, ignore_index=True) if contrasts else pd.DataFrame()
    segsum = make_segment_summary(feat)
    return {"contrasts": contrast_df, "segment_summary": segsum}

# -----------------------------
# Figures
# -----------------------------

def safe_savefig(path: Path):
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()


def make_figures(out_dir: Path, feat: pd.DataFrame, segsum: pd.DataFrame, contrasts: pd.DataFrame):
    figdir = out_dir / "figures"
    figdir.mkdir(exist_ok=True)
    # Task vs meaning score by main segment
    order = [s for s in ["Control_1", "Target_1", "Contextual_Override_1", "Target_1_final_30s", "Contextual_Override_1_final_30s", "Washout_2"] if s in set(feat.segment)]
    rows = []
    for seg in order:
        g = feat[feat.segment == seg]
        rows.append({"segment": seg, "TaskGamma": np.nanmedian(g["taskgamma_mean_30_45"]), "MeaningGamma": np.nanmedian(g["meaninggamma_mean_30_45"]), "Artifact": np.nanmedian(g["artifact_composite"])})
    s = pd.DataFrame(rows)
    if len(s):
        x = np.arange(len(s)); width = 0.35
        plt.figure(figsize=(10, 5))
        plt.bar(x-width/2, s["TaskGamma"], width, label="TaskGamma")
        plt.bar(x+width/2, s["MeaningGamma"], width, label="MeaningGamma")
        plt.xticks(x, s.segment, rotation=30, ha="right")
        plt.ylabel("median score (control-normalized / exploratory)")
        plt.title("GammaScalpel task-like vs meaning-candidate scores")
        plt.legend()
        safe_savefig(figdir / "gammascalpel_task_vs_meaning_scores.png")
    # Micro-band power heatmap by ROI and condition
    rois = ["frontoparietal_task", "meaning_candidate", "visual_control", "artifact_sentinel"]
    for band in MICRO_GAMMA_BINS:
        mat = []
        for roi in rois:
            row = []
            for seg in order[:3]:
                col = f"{roi}_{band}_logp_zcontrol"
                row.append(np.nanmedian(feat.loc[feat.segment == seg, col]) if col in feat else np.nan)
            mat.append(row)
        if len(mat):
            plt.figure(figsize=(6, 4))
            im = plt.imshow(np.array(mat), aspect="auto")
            plt.colorbar(im, label="median z vs control")
            plt.xticks(range(min(3, len(order))), order[:3], rotation=30, ha="right")
            plt.yticks(range(len(rois)), rois)
            plt.title(f"Micro-band power: {band}")
            safe_savefig(figdir / f"microband_power_heatmap_{band}.png")
    # Contrast forest selected metrics
    selected_metrics = ["taskgamma_mean_30_45", "meaninggamma_mean_30_45", "task_minus_meaning_gamma"]
    cd = contrasts[(contrasts.contrast == "Target_vs_Override_whole") & (contrasts.metric.isin(selected_metrics))].copy()
    if len(cd):
        plt.figure(figsize=(7, 3.8))
        y = np.arange(len(cd))
        plt.errorbar(cd["delta_median_A_minus_B"], y, xerr=[cd["delta_median_A_minus_B"]-cd["ci_low"], cd["ci_high"]-cd["delta_median_A_minus_B"]], fmt="o")
        plt.axvline(0, linestyle="--")
        plt.yticks(y, cd.metric)
        plt.xlabel("Target - Override median delta")
        plt.title("Target vs Override GammaScalpel score contrasts")
        safe_savefig(figdir / "target_vs_override_gammascalpel_forest.png")

# -----------------------------
# Main
# -----------------------------

def main():
    ap = argparse.ArgumentParser(description="PR-AYC-G GammaScalpel v1.0")
    ap.add_argument("xdf", help="XDF file")
    ap.add_argument("--events-json", required=True, help="Local PR-AYC-G events JSON")
    ap.add_argument("--cue-json", default=None, help="Number cue schedule JSON")
    ap.add_argument("--out", required=True, help="Output folder")
    ap.add_argument("--window-sec", type=float, default=6.0)
    ap.add_argument("--step-sec", type=float, default=3.0)
    ap.add_argument("--prepad-sec", type=float, default=3.0)
    ap.add_argument("--postpad-sec", type=float, default=5.0)
    args = ap.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    streams = load_xdf_minimal(args.xdf)
    events = load_events(args.events_json)
    outputs = compute_features(streams, events, args.cue_json, out_dir, args.window_sec, args.step_sec, args.prepad_sec, args.postpad_sec)
    summaries = run_summaries(outputs["features"])

    # Save files
    outputs["stream_inventory"].to_csv(out_dir / "stream_inventory.csv", index=False)
    outputs["segments"].to_csv(out_dir / "segments_used.csv", index=False)
    outputs["exclusions"].to_csv(out_dir / "excluded_report_sum_stillness_windows.csv", index=False)
    outputs["features"].to_csv(out_dir / "gammascalpel_window_features.csv", index=False)
    outputs["ratings_long"].to_csv(out_dir / "ratings_long.csv", index=False)
    outputs["ratings_wide"].to_csv(out_dir / "ratings_wide.csv", index=False)
    outputs["task_scoring"].to_csv(out_dir / "contextual_override_task_scoring.csv", index=False)
    if not outputs["cue_df"].empty:
        outputs["cue_df"].to_csv(out_dir / "cue_schedule_events.csv", index=False)
    pd.DataFrame([{
        "cue_visibility_qc_available": False,
        "cue_visibility_note": "Per-cue visibility cannot be computed because the rendered video frames were not supplied to GammaScalpel. White-on-bright background failures remain a design limitation unless visibility QC is added to the cue-embedding script.",
        "cue_output_hash_match": outputs["cue_meta"].get("output_cued_sha256") == outputs["cue_meta"].get("output_override_sha256") if outputs["cue_meta"] else None,
        "expected_sum": outputs["cue_meta"].get("expected_sum") if outputs["cue_meta"] else None,
        "cue_count": outputs["cue_meta"].get("cue_count") if outputs["cue_meta"] else None,
    }]).to_csv(out_dir / "cue_visibility_qc_status.csv", index=False)
    summaries["segment_summary"].to_csv(out_dir / "gammascalpel_segment_summary.csv", index=False)
    summaries["contrasts"].to_csv(out_dir / "gammascalpel_condition_contrasts.csv", index=False)

    # derive compact tables for report
    feat = outputs["features"]
    segs = ["Control_1", "Target_1", "Contextual_Override_1"]
    key_rows = []
    for seg in segs:
        g = feat[feat.segment == seg]
        if len(g):
            key_rows.append({
                "segment": seg,
                "n_windows": len(g),
                "TaskGamma_median": np.nanmedian(g["taskgamma_mean_30_45"]),
                "MeaningGamma_median": np.nanmedian(g["meaninggamma_mean_30_45"]),
                "TaskMinusMeaning_median": np.nanmedian(g["task_minus_meaning_gamma"]),
                "SpatialRatio_30_35_median": np.nanmedian(g["spatial_gamma_ratio_gamma_30_35"]),
                "SpatialRatio_35_40_median": np.nanmedian(g["spatial_gamma_ratio_gamma_35_40"]),
                "SpatialRatio_40_45_median": np.nanmedian(g["spatial_gamma_ratio_gamma_40_45"]),
                "ArtifactComposite_median": np.nanmedian(g["artifact_composite"]),
            })
    pd.DataFrame(key_rows).to_csv(out_dir / "gammascalpel_key_segment_scores.csv", index=False)

    make_figures(out_dir, outputs["features"], summaries["segment_summary"], summaries["contrasts"])

    # Summary JSON
    summary = {
        "analysis": "PR-AYC-G GammaScalpel v1.0",
        "xdf": str(args.xdf),
        "events_json": str(args.events_json),
        "cue_json": str(args.cue_json) if args.cue_json else None,
        "fs_eeg_estimated": outputs["fs"],
        "n_windows": int(len(outputs["features"])),
        "bands": {k: list(v) for k, v in BANDS.items()},
        "micro_gamma_bins": MICRO_GAMMA_BINS,
        "rois": ROIS,
        "limitations": [
            "Exploratory feature engineering; scores are not validated biomarkers.",
            "XDF-native StasisMarkers were not required for this run because local event JSON LSL timestamps were used; future 1.6K+ should verify markers in XDF.",
            "Cue visibility cannot be corrected without per-cue rendered-frame QC.",
            "Scalp gamma remains artifact-sensitive; 45-55 Hz proxy and sentinels are controls, not perfect EMG removal.",
        ],
    }
    with open(out_dir / "gammascalpel_analysis_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"GammaScalpel analysis complete: {out_dir}")

if __name__ == "__main__":
    main()
