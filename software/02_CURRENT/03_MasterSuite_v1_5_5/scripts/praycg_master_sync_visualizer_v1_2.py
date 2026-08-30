#!/usr/bin/env python3
"""
PRAYCG Master Synchronization Visualizer v1.2.6

Creates a synchronized MP4 review artifact from a PR-AYC-G XDF recording,
optional stimulus MP4, optional precomputed feature tables, and optional event files.

This script is intentionally independent of prior draft code. It uses a practical
OpenCV frame renderer rather than MoviePy/Matplotlib animation so that long PR-AYC-G
runs can be rendered with fewer moving parts.

Core outputs:
  - master synchronized MP4
  - feature table used for rendering
  - event table used for rendering
  - JSON render report

Boundary:
  This is a visualization / audit tool. It does not certify meaning, OSM, hidden-Y,
  EEG mechanisms, task compliance, audio QC, or clinical/biological truth.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

try:
    import pandas as pd
except Exception as exc:  # pragma: no cover
    pd = None

try:
    import cv2
except Exception as exc:  # pragma: no cover
    cv2 = None

try:
    from scipy import signal
except Exception:  # pragma: no cover
    signal = None

try:
    import pyxdf
except Exception:  # pragma: no cover
    pyxdf = None


VERSION = "1.2.3"
DEFAULT_EVENT_CATEGORIES = [
    "protocol",
    "tsp",
    "gamma_scalpel",
    "g2theta",
    "postpeak_pncc",
    "annotation",
    "candidate_kht",
    "mred",
    "nast",
    "ocm",
    "als",
    "artifact",
    "other",
]

CATEGORY_COLORS_BGR = {
    "protocol": (120, 120, 120),
    "tsp": (255, 180, 70),        # light blue-ish in BGR
    "gamma_scalpel": (80, 80, 255),
    "g2theta": (255, 120, 255),
    "postpeak_pncc": (80, 255, 255),
    "annotation": (80, 210, 80),
    "candidate_kht": (60, 255, 170),
    "mred": (120, 255, 120),
    "nast": (255, 220, 80),
    "ocm": (80, 180, 255),
    "als": (255, 255, 255),
    "artifact": (50, 50, 180),
    "other": (160, 160, 160),
}

LINE_COLORS_BGR = {
    "theta": (255, 255, 0),       # cyan/yellow-ish
    "gamma": (255, 0, 255),
    "hr": (40, 80, 255),
    "hrv": (0, 180, 255),
    "api_a": (0, 220, 255),
    "resp": (0, 230, 90),
    "als": (255, 255, 255),
}


# ----------------------------- Data structures -----------------------------

@dataclass
class XDFStream:
    name: str
    stype: str
    channel_count: int
    nominal_srate: float
    time_stamps: np.ndarray
    time_series: Any
    labels: List[str]


@dataclass
class Event:
    start_sec: float
    end_sec: float
    label: str
    category: str = "other"
    source: str = "unknown"
    raw: Optional[Dict[str, Any]] = None


@dataclass
class FeatureTable:
    time_sec: np.ndarray
    theta: np.ndarray
    gamma: np.ndarray
    hr: np.ndarray
    hrv: np.ndarray
    api_a: np.ndarray
    resp: np.ndarray
    als: np.ndarray
    source: str = "unknown"
    notes: str = ""


# ----------------------------- Generic helpers -----------------------------

def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def ensure_imports_for_runtime() -> None:
    missing = []
    if cv2 is None:
        missing.append("opencv-python")
    if pd is None:
        missing.append("pandas")
    if signal is None:
        missing.append("scipy")
    if missing:
        raise RuntimeError(
            "Missing required package(s): " + ", ".join(missing) +
            ". Install with: pip install -r requirements_master_sync_visualizer_v1_0.txt"
        )


def robust_float_array(x: Any) -> np.ndarray:
    arr = np.asarray(x)
    if arr.dtype.kind in {"U", "S", "O"}:
        out = []
        for v in arr.reshape(-1):
            try:
                if isinstance(v, bytes):
                    v = v.decode("utf-8", errors="ignore")
                if isinstance(v, (list, tuple, np.ndarray)) and len(v) > 0:
                    v = v[0]
                out.append(float(v))
            except Exception:
                out.append(np.nan)
        return np.asarray(out, dtype=float).reshape(arr.shape)
    return arr.astype(float, copy=False)


def finite_or_nan(x: np.ndarray) -> np.ndarray:
    y = np.asarray(x, dtype=float)
    y[~np.isfinite(y)] = np.nan
    return y


def robust_z(x: np.ndarray, eps: float = 1e-9) -> np.ndarray:
    y = finite_or_nan(x)
    med = np.nanmedian(y) if np.any(np.isfinite(y)) else 0.0
    mad = np.nanmedian(np.abs(y - med)) if np.any(np.isfinite(y)) else 1.0
    if not np.isfinite(mad) or mad < eps:
        sd = np.nanstd(y)
        scale = sd if np.isfinite(sd) and sd > eps else 1.0
    else:
        scale = 1.4826 * mad
    z = (y - med) / (scale + eps)
    z[~np.isfinite(z)] = 0.0
    return z


def safe_interp(src_t: np.ndarray, src_x: np.ndarray, dst_t: np.ndarray, fill: float = np.nan) -> np.ndarray:
    src_t = np.asarray(src_t, dtype=float)
    src_x = np.asarray(src_x, dtype=float)
    dst_t = np.asarray(dst_t, dtype=float)
    mask = np.isfinite(src_t) & np.isfinite(src_x)
    if mask.sum() < 2:
        return np.full_like(dst_t, fill, dtype=float)
    order = np.argsort(src_t[mask])
    t = src_t[mask][order]
    x = src_x[mask][order]
    # Remove duplicate timestamps by averaging last occurrence via unique indices.
    unique_t, idx = np.unique(t, return_index=True)
    if len(unique_t) < 2:
        return np.full_like(dst_t, fill, dtype=float)
    unique_x = x[idx]
    out = np.interp(dst_t, unique_t, unique_x)
    out[dst_t < unique_t[0]] = fill
    out[dst_t > unique_t[-1]] = fill
    return out


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(s)).strip("_") or "item"


def get_video_info(video_path: str) -> Dict[str, float]:
    if cv2 is None:
        raise RuntimeError("opencv-python is required to read video files.")
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0.0
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0.0
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0.0
    duration = frames / fps if fps > 0 and frames > 0 else 0.0
    cap.release()
    return {"fps": float(fps), "frame_count": float(frames), "width": float(width), "height": float(height), "duration_sec": float(duration)}


def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str | Path, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


# ----------------------------- XDF parsing --------------------------------

def parse_channel_labels(info: Dict[str, Any]) -> List[str]:
    labels: List[str] = []
    try:
        desc = info.get("desc", [{}])[0]
        chans = desc.get("channels", [{}])[0].get("channel", [])
        for ch in chans:
            if isinstance(ch, dict):
                lab = ch.get("label", [""])[0]
                labels.append(str(lab))
    except Exception:
        pass
    return labels


def load_xdf_streams(xdf_path: str) -> List[XDFStream]:
    if pyxdf is None:
        raise RuntimeError("pyxdf is required for XDF loading. Install with: pip install pyxdf")
    streams, _header = pyxdf.load_xdf(str(xdf_path), dejitter_timestamps=True, synchronize_clocks=True)
    out: List[XDFStream] = []
    for s in streams:
        info = s.get("info", {})
        name = str(info.get("name", ["unknown"])[0])
        stype = str(info.get("type", [""])[0])
        try:
            cc = int(info.get("channel_count", [0])[0])
        except Exception:
            cc = 0
        try:
            sr = float(info.get("nominal_srate", [0])[0])
        except Exception:
            sr = 0.0
        ts = np.asarray(s.get("time_stamps", []), dtype=float)
        data = s.get("time_series", [])
        labels = parse_channel_labels(info)
        out.append(XDFStream(name=name, stype=stype, channel_count=cc, nominal_srate=sr,
                             time_stamps=ts, time_series=data, labels=labels))
    return out


def stream_score(st: XDFStream, role: str) -> int:
    name = st.name.lower()
    typ = st.stype.lower()
    cc = st.channel_count
    score = 0
    if role == "eeg":
        if "eeg" in typ: score += 6
        if "eeg" in name: score += 4
        if "obci" in name or "openbci" in name: score += 3
        if cc >= 8: score += 3
        if 100 <= st.nominal_srate <= 1000: score += 2
        if "aux" in name or "analog" in name or "marker" in typ: score -= 4
    elif role == "aux":
        if "aux" in name or "analog" in name or "gpio" in name: score += 6
        if "aux" in typ or "analog" in typ: score += 3
        if 1 <= cc <= 6: score += 3
        if "eeg" in typ and cc >= 8: score -= 5
    elif role == "als":
        if "als" in name or "light" in name or "photo" in name or "timing" in name: score += 8
        if "aux" in name or "analog" in name: score += 4
        if 1 <= cc <= 6: score += 2
    elif role == "hr":
        for k in ["polar", "hrv", "heart", "rr", "ecg", "cardiac"]:
            if k in name or k in typ: score += 3
        if 1 <= cc <= 8: score += 1
    elif role == "resp":
        for k in ["resp", "breath", "vernier", "belt"]:
            if k in name or k in typ: score += 4
        if 1 <= cc <= 4: score += 1
    elif role == "markers":
        if "marker" in name or "marker" in typ or "stasis" in name: score += 7
        if cc == 1: score += 1
    return score


def choose_stream(streams: Sequence[XDFStream], role: str, override_name: str = "") -> Optional[XDFStream]:
    if override_name:
        for st in streams:
            if st.name == override_name:
                return st
        # relaxed contains match
        for st in streams:
            if override_name.lower() in st.name.lower():
                return st
    candidates = sorted(streams, key=lambda s: stream_score(s, role), reverse=True)
    if not candidates or stream_score(candidates[0], role) <= 0:
        return None
    return candidates[0]


def stream_numeric_matrix(st: XDFStream) -> np.ndarray:
    arr = np.asarray(st.time_series)
    if arr.ndim == 0:
        arr = arr.reshape(0, 0)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)
    if arr.dtype.kind in {"U", "S", "O"}:
        # Mixed/string marker streams will become nan; caller should handle markers separately.
        out = np.full(arr.shape, np.nan, dtype=float)
        it = np.nditer(arr, flags=["multi_index", "refs_ok"], op_flags=["readonly"])
        for v in it:
            try:
                val = v.item()
                if isinstance(val, bytes):
                    val = val.decode("utf-8", errors="ignore")
                if isinstance(val, (list, tuple, np.ndarray)) and len(val) > 0:
                    val = val[0]
                out[it.multi_index] = float(val)
            except Exception:
                pass
        return out
    return arr.astype(float, copy=False)


def marker_values(st: XDFStream) -> List[str]:
    vals = []
    arr = np.asarray(st.time_series, dtype=object)
    if arr.ndim == 2 and arr.shape[1] >= 1:
        arr = arr[:, 0]
    for x in arr.reshape(-1):
        if isinstance(x, bytes):
            vals.append(x.decode("utf-8", errors="ignore"))
        elif isinstance(x, (list, tuple, np.ndarray)) and len(x) > 0:
            vals.append(str(x[0]))
        else:
            vals.append(str(x))
    return vals


def detect_als_onset(ts: np.ndarray, x: np.ndarray) -> Optional[float]:
    ts = np.asarray(ts, dtype=float)
    x = np.asarray(x, dtype=float)
    mask = np.isfinite(ts) & np.isfinite(x)
    if mask.sum() < 10:
        return None
    ts = ts[mask]
    x = x[mask]
    # Robust baseline from first 20% or first 5 seconds, whichever has enough samples.
    n0 = max(10, int(0.2 * len(x)))
    baseline = x[:n0]
    med = np.nanmedian(baseline)
    mad = np.nanmedian(np.abs(baseline - med))
    p95 = np.nanpercentile(x, 95)
    p05 = np.nanpercentile(x, 5)
    dynamic = p95 - p05
    threshold = max(med + 6.0 * 1.4826 * (mad if mad > 1e-12 else np.nanstd(baseline)), p05 + 0.35 * dynamic)
    if not np.isfinite(threshold) or dynamic <= 1e-12:
        return None
    above = x > threshold
    # Require a short run above threshold to avoid single-sample noise.
    run = 0
    for i, a in enumerate(above):
        run = run + 1 if a else 0
        if run >= 2:
            return float(ts[max(0, i - run + 1)])
    return None


def find_marker_time(streams: Sequence[XDFStream], pattern: str) -> Optional[float]:
    if not pattern:
        return None
    rgx = re.compile(pattern, flags=re.IGNORECASE)
    for st in sorted(streams, key=lambda s: stream_score(s, "markers"), reverse=True):
        if stream_score(st, "markers") <= 0 or len(st.time_stamps) == 0:
            continue
        vals = marker_values(st)
        for t, v in zip(st.time_stamps, vals):
            if rgx.search(v):
                return float(t)
    return None


def extract_marker_events(streams: Sequence[XDFStream], t0: float) -> List[Event]:
    events: List[Event] = []
    for st in streams:
        if stream_score(st, "markers") <= 0 or len(st.time_stamps) == 0:
            continue
        vals = marker_values(st)
        for t, val in zip(st.time_stamps, vals):
            rt = float(t - t0)
            if not np.isfinite(rt):
                continue
            cat = infer_event_category(str(val))
            events.append(Event(start_sec=rt, end_sec=rt + 0.25, label=str(val), category=cat, source=f"xdf:{st.name}"))
    return events


# ----------------------------- Feature extraction --------------------------

def sliding_bandpower(
    data: np.ndarray,
    ts_abs: np.ndarray,
    t0: float,
    duration_sec: float,
    band: Tuple[float, float],
    step_sec: float = 0.25,
    win_sec: float = 2.0,
    max_channels: int = 16,
) -> Tuple[np.ndarray, np.ndarray]:
    if signal is None:
        raise RuntimeError("scipy is required for bandpower extraction.")
    arr = np.asarray(data, dtype=float)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)
    if arr.shape[0] != len(ts_abs):
        raise ValueError("EEG stream data length does not match timestamps.")
    # Restrict channels and finite values.
    ch_n = min(arr.shape[1], max_channels)
    arr = arr[:, :ch_n]
    ts_rel = np.asarray(ts_abs, dtype=float) - float(t0)
    mask = np.isfinite(ts_rel) & (ts_rel >= -win_sec) & (ts_rel <= duration_sec + win_sec)
    if mask.sum() < 10:
        grid = np.arange(0, max(duration_sec, step_sec), step_sec)
        return grid, np.full_like(grid, np.nan, dtype=float)
    arr = arr[mask]
    ts_rel = ts_rel[mask]
    order = np.argsort(ts_rel)
    arr = arr[order]
    ts_rel = ts_rel[order]
    # Estimate sample rate.
    diffs = np.diff(ts_rel)
    diffs = diffs[np.isfinite(diffs) & (diffs > 0)]
    fs = 1.0 / np.median(diffs) if len(diffs) else 125.0
    if not np.isfinite(fs) or fs < 10:
        fs = 125.0
    # Resample to uniform grid to stabilize window indexing.
    uni_t = np.arange(max(0.0, ts_rel[0]), min(duration_sec, ts_rel[-1]), 1.0 / fs)
    if len(uni_t) < int(win_sec * fs):
        grid = np.arange(0, max(duration_sec, step_sec), step_sec)
        return grid, np.full_like(grid, np.nan, dtype=float)
    uni_data = np.empty((len(uni_t), arr.shape[1]), dtype=float)
    for c in range(arr.shape[1]):
        x = arr[:, c]
        finite = np.isfinite(x)
        if finite.sum() < 2:
            uni_data[:, c] = np.nan
        else:
            uni_data[:, c] = np.interp(uni_t, ts_rel[finite], x[finite])
    uni_data = signal.detrend(uni_data, axis=0, type="constant")
    grid = np.arange(0, duration_sec, step_sec)
    values = np.full_like(grid, np.nan, dtype=float)
    nperseg = max(32, int(win_sec * fs))
    noverlap = max(0, int(0.5 * nperseg))
    for i, center in enumerate(grid):
        start = center - win_sec / 2.0
        end = center + win_sec / 2.0
        idx = np.where((uni_t >= start) & (uni_t <= end))[0]
        if len(idx) < max(16, nperseg // 2):
            continue
        seg = uni_data[idx]
        seg = seg[:, np.nanstd(seg, axis=0) > 1e-12]
        if seg.size == 0:
            continue
        # Welch per channel along time axis.
        try:
            f, pxx = signal.welch(seg, fs=fs, axis=0, nperseg=min(nperseg, len(seg)), noverlap=min(noverlap, max(0, len(seg)//2 - 1)))
            bmask = (f >= band[0]) & (f <= band[1])
            if bmask.sum() == 0:
                continue
            bp = np.nanmean(np.trapz(pxx[bmask, :], f[bmask], axis=0))
            values[i] = math.log10(float(bp) + 1e-12)
        except Exception:
            continue
    return grid, values


def rolling_rmssd(rr_t: np.ndarray, rr_ms: np.ndarray, out_t: np.ndarray, window_sec: float = 30.0) -> np.ndarray:
    out = np.full_like(out_t, np.nan, dtype=float)
    rr_t = np.asarray(rr_t, dtype=float)
    rr_ms = np.asarray(rr_ms, dtype=float)
    for i, t in enumerate(out_t):
        mask = np.isfinite(rr_t) & np.isfinite(rr_ms) & (rr_t >= t - window_sec) & (rr_t <= t)
        vals = rr_ms[mask]
        if len(vals) >= 3:
            diff = np.diff(vals)
            out[i] = math.sqrt(float(np.nanmean(diff ** 2)))
    return out


def estimate_resp_rate(resp_t: np.ndarray, resp_x: np.ndarray, out_t: np.ndarray, window_sec: float = 20.0) -> np.ndarray:
    if signal is None:
        return safe_interp(resp_t, resp_x, out_t)
    resp_t = np.asarray(resp_t, dtype=float)
    resp_x = np.asarray(resp_x, dtype=float)
    mask = np.isfinite(resp_t) & np.isfinite(resp_x)
    out = np.full_like(out_t, np.nan, dtype=float)
    if mask.sum() < 20:
        return out
    t = resp_t[mask]
    x = resp_x[mask]
    # Robust normalized signal.
    xz = robust_z(x)
    for i, tt in enumerate(out_t):
        m = (t >= tt - window_sec) & (t <= tt)
        if m.sum() < 10:
            continue
        seg_t = t[m]
        seg_x = xz[m]
        # Find peaks with reasonable spacing: 1.2 sec min (<=50 bpm).
        diffs = np.diff(seg_t)
        sr = 1.0 / np.median(diffs[diffs > 0]) if np.any(diffs > 0) else 25.0
        distance = max(1, int(sr * 1.2))
        try:
            peaks, _ = signal.find_peaks(seg_x, distance=distance, prominence=0.2)
            if len(peaks) >= 2:
                out[i] = len(peaks) * 60.0 / max(1e-9, (seg_t[-1] - seg_t[0]))
        except Exception:
            pass
    return out


def extract_hr_hrv_from_stream(st: Optional[XDFStream], t0: float, out_t: np.ndarray) -> Tuple[np.ndarray, np.ndarray, str]:
    if st is None:
        return np.full_like(out_t, np.nan), np.full_like(out_t, np.nan), "No cardiac/RR stream detected."
    data = stream_numeric_matrix(st)
    ts = st.time_stamps - t0
    if data.size == 0 or len(ts) == 0:
        return np.full_like(out_t, np.nan), np.full_like(out_t, np.nan), f"Cardiac stream {st.name} empty."
    col0 = data[:, 0]
    med = np.nanmedian(col0)
    note = f"Cardiac stream: {st.name}; interpreted "
    if np.isfinite(med) and 250 <= med <= 2000:
        rr_ms = col0
        hr = 60000.0 / np.maximum(rr_ms, 1.0)
        hrv = rolling_rmssd(ts, rr_ms, out_t, window_sec=30.0)
        return safe_interp(ts, hr, out_t), hrv, note + "first column as RR milliseconds."
    if np.isfinite(med) and 30 <= med <= 220:
        hr = col0
        if data.shape[1] >= 2:
            hrv_raw = data[:, 1]
            hrv = safe_interp(ts, hrv_raw, out_t)
            return safe_interp(ts, hr, out_t), hrv, note + "first column as HR and second as HRV/RMSSD-like value."
        return safe_interp(ts, hr, out_t), np.full_like(out_t, np.nan), note + "first column as HR; no HRV column detected."
    # Fallback: try first column as generic cardiac signal, not reliable.
    return safe_interp(ts, col0, out_t), np.full_like(out_t, np.nan), note + "first column as generic cardiac signal; HRV unavailable."


def extract_resp_from_stream(st: Optional[XDFStream], t0: float, out_t: np.ndarray) -> Tuple[np.ndarray, str]:
    if st is None:
        return np.full_like(out_t, np.nan), "No respiration stream detected."
    data = stream_numeric_matrix(st)
    ts = st.time_stamps - t0
    if data.size == 0 or len(ts) == 0:
        return np.full_like(out_t, np.nan), f"Respiration stream {st.name} empty."
    x = data[:, 0]
    rate = estimate_resp_rate(ts, x, out_t, window_sec=20.0)
    if np.all(~np.isfinite(rate)):
        # If rate extraction failed, graph normalized raw belt signal.
        return safe_interp(ts, robust_z(x), out_t), f"Respiration stream: {st.name}; using normalized raw belt signal."
    return rate, f"Respiration stream: {st.name}; using rolling peak-derived breaths/min estimate where available."


def compute_api_a_proxy(hr: np.ndarray, hrv: np.ndarray, resp: np.ndarray) -> np.ndarray:
    have_hr = np.any(np.isfinite(hr))
    have_hrv = np.any(np.isfinite(hrv))
    have_resp = np.any(np.isfinite(resp))
    if not (have_hr or have_hrv or have_resp):
        return np.full_like(hr, np.nan, dtype=float)
    comp = np.zeros_like(hr, dtype=float)
    weights = 0.0
    if have_hr:
        comp += robust_z(hr)
        weights += 1.0
    if have_hrv:
        comp += -robust_z(hrv)
        weights += 1.0
    if have_resp:
        comp += 0.5 * robust_z(resp)
        weights += 0.5
    if weights <= 0:
        return np.full_like(hr, np.nan, dtype=float)
    comp = comp / weights
    # Map to 0..1 via logistic to make it easy to see.
    return 1.0 / (1.0 + np.exp(-comp))


def features_from_csv(path: str, duration_sec: Optional[float] = None, step_sec: float = 0.25) -> FeatureTable:
    if pd is None:
        raise RuntimeError("pandas required to read feature CSV files.")
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Feature CSV is empty: {path}")
    cols = {c.lower(): c for c in df.columns}
    def find_col(patterns: Sequence[str], exclude: Sequence[str] = ()) -> Optional[str]:
        for exact in patterns:
            if exact.lower() in cols:
                return cols[exact.lower()]
        for c in df.columns:
            cl = c.lower()
            if any(p.lower() in cl for p in patterns) and not any(e.lower() in cl for e in exclude):
                return c
        return None
    time_col = find_col(["time_sec", "rel_time_sec", "time", "t_sec", "seconds", "t"])
    if time_col is None:
        # Assume row index at step_sec.
        src_t = np.arange(len(df), dtype=float) * step_sec
    else:
        src_t = pd.to_numeric(df[time_col], errors="coerce").to_numpy(dtype=float)
    if duration_sec is None or duration_sec <= 0:
        duration_sec = float(np.nanmax(src_t)) if np.any(np.isfinite(src_t)) else len(df) * step_sec
    out_t = np.arange(0, max(step_sec, duration_sec), step_sec)
    def get_series(patterns: Sequence[str], exclude: Sequence[str] = ()) -> np.ndarray:
        col = find_col(patterns, exclude)
        if col is None:
            return np.full_like(out_t, np.nan)
        x = pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        return safe_interp(src_t, x, out_t)
    theta = get_series(["theta", "theta_power", "fm_theta"], exclude=["gamma"])
    gamma = get_series(["lower_gamma", "meaninggamma", "gamma_power", "gamma"], exclude=["theta"])
    hr = get_series(["heart_rate", "hr_bpm", "hr"], exclude=["hrv", "rmssd"])
    hrv = get_series(["rmssd", "hrv", "sdnn"])
    api = get_series(["api_a", "api", "autonomic"])
    resp = get_series(["respiration_rate", "resp_rate", "breath_rate", "respiration", "resp"])
    als = get_series(["als", "photodiode", "light", "OpenBCIAnalogAux"])
    if np.all(~np.isfinite(api)):
        api = compute_api_a_proxy(hr, hrv, resp)
    return FeatureTable(time_sec=out_t, theta=theta, gamma=gamma, hr=hr, hrv=hrv,
                        api_a=api, resp=resp, als=als, source=f"feature_csv:{path}",
                        notes="Feature CSV columns were auto-detected by name. Verify columns_used in the JSON report.")


def features_from_xdf(
    xdf_path: str,
    duration_sec: Optional[float] = None,
    step_sec: float = 0.25,
    theta_band: Tuple[float, float] = (4.0, 8.0),
    gamma_band: Tuple[float, float] = (30.0, 45.0),
    eeg_stream_name: str = "",
    aux_stream_name: str = "",
    cardiac_stream_name: str = "",
    resp_stream_name: str = "",
    anchor_marker_regex: str = "",
    align_mode: str = "auto",
    als_aux_channel: int = 1,
) -> Tuple[FeatureTable, List[Event], Dict[str, Any]]:
    streams = load_xdf_streams(xdf_path)
    stream_inventory = [
        {"name": s.name, "type": s.stype, "channel_count": s.channel_count, "nominal_srate": s.nominal_srate,
         "samples": int(len(s.time_stamps))}
        for s in streams
    ]
    eeg = choose_stream(streams, "eeg", eeg_stream_name)
    aux = choose_stream(streams, "aux", aux_stream_name)
    cardiac = choose_stream(streams, "hr", cardiac_stream_name)
    resp = choose_stream(streams, "resp", resp_stream_name)
    als_stream = choose_stream(streams, "als", aux_stream_name) or aux

    t0 = None
    t0_source = ""
    if anchor_marker_regex:
        mt = find_marker_time(streams, anchor_marker_regex)
        if mt is not None:
            t0 = mt
            t0_source = f"marker_regex:{anchor_marker_regex}"
    if t0 is None and align_mode in {"auto", "als"} and als_stream is not None:
        data = stream_numeric_matrix(als_stream)
        if data.size and data.ndim >= 2:
            ch = int(max(0, min(als_aux_channel, data.shape[1] - 1)))
            onset = detect_als_onset(als_stream.time_stamps, data[:, ch])
            if onset is not None:
                t0 = onset
                t0_source = f"als_edge:{als_stream.name}:channel_{ch}"
    if t0 is None and eeg is not None and len(eeg.time_stamps):
        t0 = float(eeg.time_stamps[0])
        t0_source = f"first_eeg_timestamp:{eeg.name}"
    if t0 is None:
        all_ts = np.concatenate([s.time_stamps for s in streams if len(s.time_stamps)])
        if len(all_ts):
            t0 = float(np.nanmin(all_ts))
            t0_source = "earliest_stream_timestamp"
        else:
            t0 = 0.0
            t0_source = "none_found"

    # Determine duration.
    if duration_sec is None or duration_sec <= 0:
        max_rel = 0.0
        for s in streams:
            if len(s.time_stamps):
                max_rel = max(max_rel, float(np.nanmax(s.time_stamps - t0)))
        duration_sec = max(1.0, max_rel)
    out_t = np.arange(0, max(step_sec, float(duration_sec)), step_sec)

    notes = []
    if eeg is not None:
        eeg_data = stream_numeric_matrix(eeg)
        theta_t, theta = sliding_bandpower(eeg_data, eeg.time_stamps, t0, duration_sec, theta_band, step_sec=step_sec)
        gamma_t, gamma = sliding_bandpower(eeg_data, eeg.time_stamps, t0, duration_sec, gamma_band, step_sec=step_sec)
        theta = safe_interp(theta_t, theta, out_t)
        gamma = safe_interp(gamma_t, gamma, out_t)
        notes.append(f"EEG stream: {eeg.name}; theta={theta_band}; gamma={gamma_band}.")
    else:
        theta = np.full_like(out_t, np.nan)
        gamma = np.full_like(out_t, np.nan)
        notes.append("No EEG stream detected; theta/gamma unavailable.")

    hr, hrv, note_hr = extract_hr_hrv_from_stream(cardiac, t0, out_t)
    notes.append(note_hr)
    resp_rate, note_resp = extract_resp_from_stream(resp, t0, out_t)
    notes.append(note_resp)
    api = compute_api_a_proxy(hr, hrv, resp_rate)

    if als_stream is not None:
        adata = stream_numeric_matrix(als_stream)
        if adata.size and adata.ndim >= 2:
            ch = int(max(0, min(als_aux_channel, adata.shape[1] - 1)))
            als = safe_interp(als_stream.time_stamps - t0, adata[:, ch], out_t)
            notes.append(f"ALS/light stream: {als_stream.name}; channel index {ch}.")
        else:
            als = np.full_like(out_t, np.nan)
            notes.append(f"ALS/light stream {als_stream.name} detected but not numeric.")
    else:
        als = np.full_like(out_t, np.nan)
        notes.append("No ALS/light stream detected.")

    marker_events = extract_marker_events(streams, t0)
    report = {
        "xdf_path": str(xdf_path),
        "t0_source": t0_source,
        "t0_absolute_lsl_time": t0,
        "stream_inventory": stream_inventory,
        "selected_streams": {
            "eeg": eeg.name if eeg else None,
            "aux": aux.name if aux else None,
            "als": als_stream.name if als_stream else None,
            "cardiac": cardiac.name if cardiac else None,
            "respiration": resp.name if resp else None,
        },
        "notes": notes,
    }
    ft = FeatureTable(out_t, theta, gamma, hr, hrv, api, resp_rate, als,
                      source=f"xdf:{xdf_path}", notes="; ".join(notes))
    return ft, marker_events, report


# ----------------------------- Event loading -------------------------------

def infer_event_category(label: str) -> str:
    l = str(label).lower()
    if any(k in l for k in ["tsp", "temporalsemantic", "temporal_semantic", "semanticproxy", "temporal semantic"]):
        return "tsp"
    if any(k in l for k in ["gammascalpel", "gamma_scalpel", "meaninggamma", "meaning_gamma", "lower_gamma", "gamma peak", "gamma_peak"]):
        return "gamma_scalpel"
    if any(k in l for k in ["g2theta", "gamma_to_theta", "gamma-to-theta", "handoff"]):
        return "g2theta"
    if any(k in l for k in ["candidate_local_kht", "local_kht", "k_ht", "kht", "candidate lock"]):
        return "candidate_kht"
    if any(k in l for k in ["postpeak", "post_peak", "pncc"]):
        return "postpeak_pncc"
    if any(k in l for k in ["annotation", "reveal", "climax", "threat", "startle", "dialogue", "face/body", "face", "body", "social-action"]):
        return "annotation"
    if any(k in l for k in ["als", "photodiode", "photo", "light", "video_start_pulse", "sensor_timing"]):
        return "als"
    if any(k in l for k in ["artifact", "blink", "jaw", "emg", "eog", "motion"]):
        return "artifact"
    if any(k in l for k in ["baseline", "control", "target", "override", "washout", "instruction", "rating", "protocol"]):
        return "protocol"
    return "other"


def event_from_row(row: Dict[str, Any], source: str) -> Optional[Event]:
    lower = {str(k).lower(): k for k in row.keys()}
    def val(cands: Sequence[str]) -> Any:
        for c in cands:
            if c.lower() in lower:
                return row[lower[c.lower()]]
        return None
    label = val(["label", "event", "event_label", "marker", "name", "type", "phase", "anchor", "description"])
    if label is None:
        label = source
    category = val(["category", "event_category", "class"])
    start = val(["start_sec", "onset_sec", "time_sec", "t_sec", "sec", "start", "onset", "peak_sec", "taper_sec", "event_time_sec"])
    end = val(["end_sec", "stop_sec", "offset_sec", "end", "stop", "offset"])
    duration = val(["duration_sec", "duration", "dur_sec"])
    try:
        start_f = float(start)
    except Exception:
        return None
    if end is not None and str(end) != "":
        try:
            end_f = float(end)
        except Exception:
            end_f = start_f
    elif duration is not None and str(duration) != "":
        try:
            end_f = start_f + float(duration)
        except Exception:
            end_f = start_f + 0.5
    else:
        end_f = start_f + 0.5
    if end_f < start_f:
        end_f = start_f + 0.5
    cat = str(category) if category not in [None, ""] else infer_event_category(str(label))
    if cat not in DEFAULT_EVENT_CATEGORIES:
        cat = infer_event_category(str(label))
    return Event(start_sec=start_f, end_sec=end_f, label=str(label), category=cat, source=source, raw=dict(row))


def flatten_json_events(obj: Any, source: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if isinstance(obj, list):
        for it in obj:
            if isinstance(it, dict):
                rows.append(it)
    elif isinstance(obj, dict):
        for key in ["events", "cue_events", "sensor_timing_pulse_events", "annotations", "anchors", "event_windows"]:
            if key in obj:
                rows.extend(flatten_json_events(obj[key], f"{source}:{key}"))
        # If dict itself looks like one event.
        if any(k in obj for k in ["start_sec", "time_sec", "onset_sec", "peak_sec", "taper_sec"]):
            rows.append(obj)
    return rows


def load_event_files(paths: Sequence[str]) -> List[Event]:
    events: List[Event] = []
    for path in paths:
        if not path:
            continue
        p = Path(path)
        if not p.exists():
            eprint(f"WARNING: event file not found: {path}")
            continue
        try:
            if p.suffix.lower() == ".csv":
                if pd is None:
                    raise RuntimeError("pandas required for CSV event files")
                df = pd.read_csv(p)
                for _, row in df.iterrows():
                    ev = event_from_row(row.to_dict(), source=str(p.name))
                    if ev:
                        events.append(ev)
            elif p.suffix.lower() in {".json", ".jsn"}:
                obj = read_json(str(p))
                for row in flatten_json_events(obj, source=str(p.name)):
                    ev = event_from_row(row, source=str(p.name))
                    if ev:
                        events.append(ev)
            else:
                eprint(f"WARNING: unsupported event file extension: {path}")
        except Exception as exc:
            eprint(f"WARNING: failed to load event file {path}: {exc}")
    events.sort(key=lambda e: (e.start_sec, e.end_sec, e.label))
    return events


def filter_events(events: Sequence[Event], categories: Sequence[str]) -> List[Event]:
    cats = set(c.lower() for c in categories)
    if "all" in cats:
        return list(events)
    return [e for e in events if e.category.lower() in cats]


# ----------------------------- Rendering ----------------------------------

def blend_rect(img: np.ndarray, x1: int, y1: int, x2: int, y2: int, color: Tuple[int, int, int], alpha: float) -> None:
    h, w = img.shape[:2]
    x1 = max(0, min(w, int(x1))); x2 = max(0, min(w, int(x2)))
    y1 = max(0, min(h, int(y1))); y2 = max(0, min(h, int(y2)))
    if x2 <= x1 or y2 <= y1:
        return
    overlay = img[y1:y2, x1:x2].copy()
    overlay[:, :] = color
    cv2.addWeighted(overlay, alpha, img[y1:y2, x1:x2], 1 - alpha, 0, dst=img[y1:y2, x1:x2])


def scale_values_for_panel(x: np.ndarray) -> Tuple[float, float]:
    y = np.asarray(x, dtype=float)
    if not np.any(np.isfinite(y)):
        return -1.0, 1.0
    lo = np.nanpercentile(y, 2)
    hi = np.nanpercentile(y, 98)
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        med = np.nanmedian(y)
        return med - 1.0, med + 1.0
    pad = 0.05 * (hi - lo)
    return float(lo - pad), float(hi + pad)


def prepare_draw_arrays(ft: FeatureTable) -> Dict[str, np.ndarray]:
    # Graph z-scores for cross-unit overlays, but keep arrays separate in report.
    return {
        "theta": robust_z(ft.theta),
        "gamma": robust_z(ft.gamma),
        "hr": robust_z(ft.hr),
        "hrv": robust_z(ft.hrv),
        "api_a": ft.api_a if np.any(np.isfinite(ft.api_a)) else np.zeros_like(ft.time_sec),
        "resp": robust_z(ft.resp),
        "als": robust_z(ft.als),
    }


def draw_panel(
    img: np.ndarray,
    panel: Tuple[int, int, int, int],
    title: str,
    t_current: float,
    window_sec: float,
    time_grid: np.ndarray,
    series: List[Tuple[str, np.ndarray, Tuple[int, int, int]]],
    events: Sequence[Event],
    y_range: Optional[Tuple[float, float]] = None,
) -> None:
    x1, y1, x2, y2 = panel
    cv2.rectangle(img, (x1, y1), (x2, y2), (45, 45, 45), 1)
    cv2.putText(img, title, (x1 + 8, y1 + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (230, 230, 230), 1, cv2.LINE_AA)
    plot_top = y1 + 30
    plot_bottom = y2 - 18
    plot_left = x1 + 44
    plot_right = x2 - 10
    cv2.rectangle(img, (plot_left, plot_top), (plot_right, plot_bottom), (30, 30, 30), -1)
    cv2.rectangle(img, (plot_left, plot_top), (plot_right, plot_bottom), (70, 70, 70), 1)
    t0 = max(0.0, t_current - window_sec)
    t1 = max(window_sec, t_current)
    if t_current < window_sec:
        t1 = window_sec
    # Event highlights.
    for ev in events:
        if ev.end_sec < t0 or ev.start_sec > t1:
            continue
        ex1 = plot_left + int((max(ev.start_sec, t0) - t0) / max(1e-9, (t1 - t0)) * (plot_right - plot_left))
        ex2 = plot_left + int((min(ev.end_sec, t1) - t0) / max(1e-9, (t1 - t0)) * (plot_right - plot_left))
        if ex2 <= ex1:
            ex2 = ex1 + 2
        color = CATEGORY_COLORS_BGR.get(ev.category, CATEGORY_COLORS_BGR["other"])
        blend_rect(img, ex1, plot_top, ex2, plot_bottom, color, alpha=0.18)
    # Current time cursor at right edge.
    cv2.line(img, (plot_right, plot_top), (plot_right, plot_bottom), (255, 255, 255), 1)
    # Determine y scaling for this panel based on all series if not provided.
    if y_range is None:
        vals = []
        for _name, y, _color in series:
            vals.append(y)
        if vals:
            ycat = np.concatenate([np.asarray(v, dtype=float) for v in vals])
            y_min, y_max = scale_values_for_panel(ycat)
        else:
            y_min, y_max = -1, 1
    else:
        y_min, y_max = y_range
    if not np.isfinite(y_min) or not np.isfinite(y_max) or y_max <= y_min:
        y_min, y_max = -1, 1
    # Draw lines.
    mask = (time_grid >= t0) & (time_grid <= t1)
    tx = time_grid[mask]
    for name, y, color in series:
        yy = np.asarray(y, dtype=float)[mask]
        pts = []
        for tt, vv in zip(tx, yy):
            if not np.isfinite(vv):
                continue
            px = plot_left + int((tt - t0) / max(1e-9, t1 - t0) * (plot_right - plot_left))
            py = plot_bottom - int((vv - y_min) / max(1e-9, y_max - y_min) * (plot_bottom - plot_top))
            py = max(plot_top, min(plot_bottom, py))
            pts.append((px, py))
        if len(pts) >= 2:
            cv2.polylines(img, [np.asarray(pts, dtype=np.int32)], isClosed=False, color=color, thickness=2, lineType=cv2.LINE_AA)
    # Legend.
    lx = plot_left + 4
    ly = y2 - 4
    for name, _y, color in series:
        cv2.line(img, (lx, ly - 5), (lx + 16, ly - 5), color, 2)
        cv2.putText(img, name, (lx + 20, ly), cv2.FONT_HERSHEY_SIMPLEX, 0.42, color, 1, cv2.LINE_AA)
        lx += 96
    cv2.putText(img, f"{t_current:7.2f}s", (plot_right - 90, y1 + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1, cv2.LINE_AA)


def render_graph_frame(
    ft: FeatureTable,
    draw_arrays: Dict[str, np.ndarray],
    events: Sequence[Event],
    t_current: float,
    width: int,
    height: int,
    window_sec: float,
    show_als: bool = True,
) -> np.ndarray:
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:, :] = (8, 8, 8)
    margin = 12
    panel_count = 5 if show_als else 4
    gap = 8
    usable_h = height - 2 * margin - gap * (panel_count - 1)
    ph = max(60, usable_h // panel_count)
    y = margin
    panels = []
    for _ in range(panel_count):
        panels.append((margin, y, width - margin, y + ph))
        y += ph + gap
    draw_panel(img, panels[0], "EEG bandpower z: theta 4-8 Hz + gamma band", t_current, window_sec, ft.time_sec,
               [("theta", draw_arrays["theta"], LINE_COLORS_BGR["theta"]), ("gamma", draw_arrays["gamma"], LINE_COLORS_BGR["gamma"])], events, y_range=(-3, 3))
    draw_panel(img, panels[1], "Cardiac z: HR + HRV/RMSSD", t_current, window_sec, ft.time_sec,
               [("HR", draw_arrays["hr"], LINE_COLORS_BGR["hr"]), ("HRV", draw_arrays["hrv"], LINE_COLORS_BGR["hrv"])], events, y_range=(-3, 3))
    draw_panel(img, panels[2], "API-A proxy / supplied API-A", t_current, window_sec, ft.time_sec,
               [("API-A", draw_arrays["api_a"], LINE_COLORS_BGR["api_a"])], events, y_range=(0, 1))
    draw_panel(img, panels[3], "Respiration z or breaths/min estimate", t_current, window_sec, ft.time_sec,
               [("resp", draw_arrays["resp"], LINE_COLORS_BGR["resp"])], events, y_range=(-3, 3))
    if show_als:
        draw_panel(img, panels[4], "ALS-PT19 / photodiode timing z", t_current, window_sec, ft.time_sec,
                   [("ALS", draw_arrays["als"], LINE_COLORS_BGR["als"])], events, y_range=(-3, 3))
    return img


def compose_frame(video_frame: Optional[np.ndarray], graph_frame: np.ndarray, out_width: int, video_height: int) -> np.ndarray:
    if video_frame is None:
        return graph_frame
    h, w = video_frame.shape[:2]
    if h <= 0 or w <= 0:
        top = np.zeros((video_height, out_width, 3), dtype=np.uint8)
    else:
        scale = min(out_width / w, video_height / h)
        nw = max(1, int(w * scale)); nh = max(1, int(h * scale))
        resized = cv2.resize(video_frame, (nw, nh), interpolation=cv2.INTER_AREA)
        top = np.zeros((video_height, out_width, 3), dtype=np.uint8)
        x = (out_width - nw) // 2
        y = (video_height - nh) // 2
        top[y:y+nh, x:x+nw] = resized
    return np.vstack([top, graph_frame])


def write_feature_csv(path: str | Path, ft: FeatureTable) -> None:
    if pd is None:
        return
    df = pd.DataFrame({
        "time_sec": ft.time_sec,
        "theta": ft.theta,
        "gamma": ft.gamma,
        "hr": ft.hr,
        "hrv": ft.hrv,
        "api_a": ft.api_a,
        "resp": ft.resp,
        "als": ft.als,
    })
    df.to_csv(path, index=False)


def write_events_csv(path: str | Path, events: Sequence[Event]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["start_sec", "end_sec", "category", "label", "source"])
        writer.writeheader()
        for e in events:
            writer.writerow({"start_sec": e.start_sec, "end_sec": e.end_sec, "category": e.category, "label": e.label, "source": e.source})


def render_master_video(
    ft: FeatureTable,
    events: Sequence[Event],
    out_mp4: str,
    stimulus_video: str = "",
    fps: float = 24.0,
    out_width: int = 1280,
    graph_height: int = 620,
    video_height: int = 540,
    rolling_window_sec: float = 30.0,
    duration_sec: Optional[float] = None,
    show_als: bool = True,
    progress_every: int = 100,
) -> Dict[str, Any]:
    ensure_imports_for_runtime()
    if duration_sec is None or duration_sec <= 0:
        duration_sec = float(np.nanmax(ft.time_sec)) if len(ft.time_sec) else 1.0
    if stimulus_video:
        vinfo = get_video_info(stimulus_video)
        if vinfo["duration_sec"] > 0:
            duration_sec = min(duration_sec, vinfo["duration_sec"]) if duration_sec > 0 else vinfo["duration_sec"]
        cap = cv2.VideoCapture(str(stimulus_video))
        if not cap.isOpened():
            raise RuntimeError(f"Could not open stimulus video: {stimulus_video}")
    else:
        cap = None
        video_height = 0
        vinfo = {}
    Path(out_mp4).parent.mkdir(parents=True, exist_ok=True)
    total_frames = int(math.ceil(duration_sec * fps))
    out_h = int(video_height + graph_height)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(out_mp4), fourcc, float(fps), (int(out_width), int(out_h)))
    if not writer.isOpened():
        raise RuntimeError(f"Could not open VideoWriter for {out_mp4}")
    draw_arrays = prepare_draw_arrays(ft)
    try:
        for i in range(total_frames):
            t = i / float(fps)
            vframe = None
            if cap is not None:
                cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000.0)
                ok, bgr = cap.read()
                if ok:
                    vframe = bgr
                else:
                    vframe = np.zeros((video_height, out_width, 3), dtype=np.uint8)
            graph = render_graph_frame(ft, draw_arrays, events, t, out_width, graph_height, rolling_window_sec, show_als=show_als)
            frame = compose_frame(vframe, graph, out_width=out_width, video_height=video_height)
            writer.write(frame)
            if progress_every and (i % progress_every == 0):
                print(f"Rendered {i}/{total_frames} frames ({100*i/max(1,total_frames):.1f}%)")
    finally:
        writer.release()
        if cap is not None:
            cap.release()
    print(f"Rendered {total_frames}/{total_frames} frames (100.0%)")
    return {
        "out_mp4": out_mp4,
        "fps": fps,
        "duration_sec": duration_sec,
        "total_frames": total_frames,
        "out_width": out_width,
        "out_height": out_h,
        "stimulus_video": stimulus_video,
        "stimulus_video_info": vinfo,
        "graph_height": graph_height,
        "video_height": video_height,
        "rolling_window_sec": rolling_window_sec,
        "event_count_rendered": len(events),
        "feature_source": ft.source,
        "feature_notes": ft.notes,
    }


# ----------------------------- Demo data ----------------------------------

def make_demo_features(duration_sec: float = 30.0, step_sec: float = 0.25) -> Tuple[FeatureTable, List[Event]]:
    t = np.arange(0, duration_sec, step_sec)
    rng = np.random.default_rng(20260805)
    theta = np.sin(2 * np.pi * t / 7.0) + 0.15 * rng.normal(size=len(t))
    gamma = 0.7 * np.sin(2 * np.pi * t / 3.0 + 0.7) + 0.2 * rng.normal(size=len(t))
    gamma += np.exp(-0.5 * ((t - 12) / 1.5) ** 2) * 2.0
    theta += np.exp(-0.5 * ((t - 17) / 2.5) ** 2) * 1.4
    hr = 70 + 4 * np.sin(2 * np.pi * t / 20.0) + 2 * rng.normal(size=len(t))
    hrv = 35 + 8 * np.sin(2 * np.pi * t / 17.0 + 1.5) + 2 * rng.normal(size=len(t))
    resp = 12 + 2 * np.sin(2 * np.pi * t / 10.0)
    api = compute_api_a_proxy(hr, hrv, resp)
    als = np.zeros_like(t)
    als[(t >= 0) & (t <= 1)] = 1.0
    events = [
        Event(0, 1, "ALS video-start pulse", "als", "demo"),
        Event(10, 14, "GammaScalpel demo peak", "gamma_scalpel", "demo"),
        Event(15, 22, "G2Theta demo handoff", "g2theta", "demo"),
        Event(17, 25, "PostPeak PNCC demo window", "postpeak_pncc", "demo"),
    ]
    return FeatureTable(t, theta, gamma, hr, hrv, api, resp, als, source="demo", notes="Synthetic demo data only."), events


# ----------------------------- GUI ----------------------------------------

def launch_gui() -> int:
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except Exception as exc:
        eprint("Tkinter GUI is unavailable on this Python installation.")
        return 2

    class App(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("PRAYCG Master Sync Visualizer v1.0")
            self.geometry("760x760")
            self.resizable(True, True)
            self.vars: Dict[str, Any] = {}
            canvas = tk.Canvas(self)
            scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
            frame = tk.Frame(canvas)
            frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            self.body = frame
            self.build()

        def row_path(self, label: str, key: str, filetypes: List[Tuple[str, str]], save: bool = False) -> None:
            row = tk.Frame(self.body); row.pack(fill="x", padx=10, pady=4)
            tk.Label(row, text=label, width=22, anchor="w").pack(side="left")
            var = tk.StringVar()
            self.vars[key] = var
            tk.Entry(row, textvariable=var, width=70).pack(side="left", padx=4, fill="x", expand=True)
            def browse():
                if save:
                    p = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=".mp4")
                else:
                    p = filedialog.askopenfilename(filetypes=filetypes)
                if p:
                    var.set(p)
            tk.Button(row, text="Browse", command=browse).pack(side="left")

        def row_entry(self, label: str, key: str, default: str) -> None:
            row = tk.Frame(self.body); row.pack(fill="x", padx=10, pady=4)
            tk.Label(row, text=label, width=22, anchor="w").pack(side="left")
            var = tk.StringVar(value=default)
            self.vars[key] = var
            tk.Entry(row, textvariable=var, width=30).pack(side="left", padx=4)

        def build(self):
            tk.Label(self.body, text="PRAYCG Master Synchronization Visualizer v1.2.6", font=("Arial", 15, "bold")).pack(pady=10)
            tk.Label(self.body, text="Creates a synchronized MP4: stimulus video on top, rolling physiology panels below.", anchor="w").pack(fill="x", padx=10)
            self.row_path("XDF file", "xdf", [("XDF", "*.xdf"), ("All", "*.*")])
            self.row_path("Stimulus MP4 (optional)", "video", [("MP4", "*.mp4"), ("All", "*.*")])
            self.row_path("Feature CSV (optional)", "features", [("CSV", "*.csv"), ("All", "*.*")])
            self.row_path("Event file 1 (optional)", "events1", [("CSV/JSON", "*.csv *.json"), ("All", "*.*")])
            self.row_path("Event file 2 (optional)", "events2", [("CSV/JSON", "*.csv *.json"), ("All", "*.*")])
            self.row_path("Output MP4", "out", [("MP4", "*.mp4")], save=True)
            self.row_entry("FPS", "fps", "24")
            self.row_entry("Output width px", "width", "1280")
            self.row_entry("Video panel height px", "video_height", "540")
            self.row_entry("Graph panel height px", "graph_height", "620")
            self.row_entry("Rolling window sec", "window", "30")
            self.row_entry("Anchor marker regex", "anchor", "")
            self.row_entry("ALS AUX channel", "als_ch", "1")
            tk.Label(self.body, text="Event categories to highlight", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(12, 2))
            self.category_vars: Dict[str, Any] = {}
            cat_frame = tk.Frame(self.body); cat_frame.pack(fill="x", padx=10)
            for i, cat in enumerate(DEFAULT_EVENT_CATEGORIES):
                v = tk.BooleanVar(value=True)
                self.category_vars[cat] = v
                tk.Checkbutton(cat_frame, text=cat, variable=v).grid(row=i//3, column=i%3, sticky="w", padx=8)
            tk.Button(self.body, text="RENDER MASTER MP4", bg="#8b0000", fg="white", font=("Arial", 12, "bold"), command=self.run_render).pack(pady=16)
            tk.Button(self.body, text="Render 30-sec DEMO", command=self.run_demo).pack(pady=4)
            self.status = tk.Text(self.body, height=10, width=90)
            self.status.pack(padx=10, pady=10, fill="both", expand=True)

        def log(self, msg: str):
            self.status.insert("end", msg + "\n")
            self.status.see("end")
            self.update_idletasks()

        def args_from_gui(self) -> argparse.Namespace:
            cats = [k for k, v in self.category_vars.items() if v.get()]
            return argparse.Namespace(
                xdf=self.vars["xdf"].get().strip(),
                video=self.vars["video"].get().strip(),
                features=self.vars["features"].get().strip(),
                events=",".join([self.vars["events1"].get().strip(), self.vars["events2"].get().strip()]),
                out=self.vars["out"].get().strip(),
                fps=float(self.vars["fps"].get()),
                width=int(self.vars["width"].get()),
                video_height=int(self.vars["video_height"].get()),
                graph_height=int(self.vars["graph_height"].get()),
                rolling_window=float(self.vars["window"].get()),
                anchor_marker=self.vars["anchor"].get().strip(),
                als_aux_channel=int(self.vars["als_ch"].get()),
                categories=",".join(cats),
                duration=0.0,
                demo=False,
                out_dir="",
                theta_band="4,8",
                gamma_band="30,45",
                eeg_stream="",
                aux_stream="",
                cardiac_stream="",
                resp_stream="",
                no_als_panel=False,
                feature_step=0.25,
            )

        def run_demo(self):
            out = self.vars["out"].get().strip()
            if not out:
                out = str(Path.cwd() / "PRAYCG_MasterSync_Demo.mp4")
                self.vars["out"].set(out)
            ns = self.args_from_gui(); ns.demo = True
            self.execute(ns)

        def run_render(self):
            ns = self.args_from_gui()
            if not ns.out:
                messagebox.showwarning("Missing output", "Please choose an output MP4 path.")
                return
            if not ns.xdf and not ns.features:
                messagebox.showwarning("Missing data", "Please choose an XDF file or a precomputed feature CSV.")
                return
            self.execute(ns)

        def execute(self, ns):
            try:
                self.log("Starting render...")
                result = run_pipeline(ns)
                self.log("DONE: " + result.get("out_mp4", ""))
                messagebox.showinfo("Render complete", "Output written:\n" + result.get("out_mp4", ""))
            except Exception as exc:
                tb = traceback.format_exc()
                self.log(tb)
                messagebox.showerror("Render failed", str(exc))
    app = App()
    app.mainloop()
    return 0


# ----------------------------- CLI pipeline --------------------------------

def parse_band(s: str, default: Tuple[float, float]) -> Tuple[float, float]:
    try:
        parts = [float(x.strip()) for x in str(s).split(",")]
        if len(parts) == 2 and parts[1] > parts[0]:
            return parts[0], parts[1]
    except Exception:
        pass
    return default


def run_pipeline(args: argparse.Namespace) -> Dict[str, Any]:
    ensure_imports_for_runtime()
    out_path = Path(args.out or "PRAYCG_MasterSync_Output.mp4").resolve()
    out_dir = Path(args.out_dir).resolve() if getattr(args, "out_dir", "") else out_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.demo:
        ft, events = make_demo_features(duration_sec=args.duration or 30.0, step_sec=args.feature_step)
        xdf_report: Dict[str, Any] = {"mode": "demo"}
    else:
        duration = float(args.duration) if getattr(args, "duration", 0) else None
        if args.video and (duration is None or duration <= 0):
            try:
                duration = get_video_info(args.video)["duration_sec"]
            except Exception:
                duration = None
        if args.features:
            ft = features_from_csv(args.features, duration_sec=duration, step_sec=float(args.feature_step))
            events = []
            xdf_report = {"mode": "feature_csv", "feature_csv": args.features}
        else:
            theta_band = parse_band(args.theta_band, (4.0, 8.0))
            gamma_band = parse_band(args.gamma_band, (30.0, 45.0))
            ft, events, xdf_report = features_from_xdf(
                args.xdf,
                duration_sec=duration,
                step_sec=float(args.feature_step),
                theta_band=theta_band,
                gamma_band=gamma_band,
                eeg_stream_name=getattr(args, "eeg_stream", ""),
                aux_stream_name=getattr(args, "aux_stream", ""),
                cardiac_stream_name=getattr(args, "cardiac_stream", ""),
                resp_stream_name=getattr(args, "resp_stream", ""),
                anchor_marker_regex=getattr(args, "anchor_marker", ""),
                als_aux_channel=int(getattr(args, "als_aux_channel", 1)),
            )
    # Event files.
    event_paths: List[str] = []
    event_paths.extend(collect_analysis_output_events(getattr(args, "analysis_out", "")))
    if getattr(args, "events", ""):
        for item in str(args.events).split(","):
            item = item.strip().strip('"')
            if item:
                event_paths.append(item)
    file_events = load_event_files(event_paths)
    all_events = list(events) + file_events
    cats = [c.strip().lower() for c in str(getattr(args, "categories", "all")).split(",") if c.strip()]
    if not cats:
        cats = ["all"]
    render_events = filter_events(all_events, cats)
    # Render.
    render_report = render_master_video(
        ft,
        render_events,
        out_mp4=str(out_path),
        stimulus_video=getattr(args, "video", "") or "",
        fps=float(args.fps),
        out_width=int(args.width),
        graph_height=int(args.graph_height),
        video_height=int(args.video_height),
        rolling_window_sec=float(args.rolling_window),
        duration_sec=float(args.duration) if getattr(args, "duration", 0) else None,
        show_als=not bool(getattr(args, "no_als_panel", False)),
    )
    # Write sidecars.
    feature_csv = out_dir / (out_path.stem + "_features_used.csv")
    events_csv = out_dir / (out_path.stem + "_events_used.csv")
    report_json = out_dir / (out_path.stem + "_render_report.json")
    write_feature_csv(feature_csv, ft)
    write_events_csv(events_csv, render_events)
    report = {
        "schema": "PRAYCG_MasterSync_Visualizer_Report_v1_0",
        "version": VERSION,
        "render": render_report,
        "xdf_or_feature_report": xdf_report,
        "input_resolution_warnings": input_warnings,
        "inputs": {
            "xdf": getattr(args, "xdf", ""),
            "feature_csv": getattr(args, "features", ""),
            "stimulus_video": getattr(args, "video", ""),
            "event_files": event_paths,
            "analysis_output_folder": getattr(args, "analysis_out", ""),
        },
        "sidecars": {
            "features_used_csv": str(feature_csv),
            "events_used_csv": str(events_csv),
            "render_report_json": str(report_json),
        },
        "boundary": "Visualization/audit only. Does not certify PR-AYC-G endpoint validity, meaning, OSM, hidden-Y biology, or human EEG mechanism.",
    }
    write_json(report_json, report)
    return {**render_report, "features_csv": str(feature_csv), "events_csv": str(events_csv), "report_json": str(report_json)}


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="PRAYCG Master Synchronization Visualizer v1.2.6")
    p.add_argument("--gui", action="store_true", help="Launch Tkinter GUI.")
    p.add_argument("--demo", action="store_true", help="Render a synthetic 30-second demo without XDF.")
    p.add_argument("--xdf", default="", help="Input XDF file.")
    p.add_argument("--features", default="", help="Optional precomputed feature CSV. If provided, raw XDF processing is skipped.")
    p.add_argument("--video", default="", help="Optional stimulus MP4 to place above graph panels.")
    p.add_argument("--events", default="", help="Comma-separated event CSV/JSON files to highlight.")
    p.add_argument("--analysis-out", default="", help="Optional Master Comprehensive output folder. CandidateLocal_KHT and state-locked tables are auto-added as visual overlays.")
    p.add_argument("--out", default="", help="Output MP4 path.")
    p.add_argument("--out-dir", default="", help="Directory for sidecar CSV/JSON outputs. Defaults to MP4 folder.")
    p.add_argument("--fps", type=float, default=24.0, help="Output video FPS.")
    p.add_argument("--duration", type=float, default=0.0, help="Optional render duration seconds. 0 = infer from video/features/XDF.")
    p.add_argument("--width", type=int, default=1280, help="Output width in pixels.")
    p.add_argument("--video-height", type=int, default=540, help="Top stimulus video panel height.")
    p.add_argument("--graph-height", type=int, default=620, help="Bottom graph panel height.")
    p.add_argument("--rolling-window", type=float, default=30.0, help="Seconds visible in rolling graph window.")
    p.add_argument("--categories", default="all", help="Event categories to show, comma-separated, or 'all'.")
    p.add_argument("--anchor-marker", default="", help="Regex for marker to define t=0 if no ALS alignment or to override it.")
    p.add_argument("--als-aux-channel", type=int, default=1, help="ALS channel index in analog AUX stream: 0=A5/D11, 1=A6/D12, 2=A7/D13.")
    p.add_argument("--feature-step", type=float, default=0.25, help="Feature time step seconds.")
    p.add_argument("--theta-band", default="4,8", help="Theta band as low,high Hz.")
    p.add_argument("--gamma-band", default="30,45", help="Gamma band as low,high Hz; default lower gamma 30-45.")
    p.add_argument("--eeg-stream", default="", help="Optional exact/partial EEG stream name override.")
    p.add_argument("--aux-stream", default="", help="Optional exact/partial analog AUX/ALS stream name override.")
    p.add_argument("--cardiac-stream", default="", help="Optional exact/partial cardiac stream name override.")
    p.add_argument("--resp-stream", default="", help="Optional exact/partial respiration stream name override.")
    p.add_argument("--no-als-panel", action="store_true", help="Hide ALS panel.")
    return p






# ----------------------- v1.2 Master Suite output event overlays -----------------------

def collect_analysis_output_events(analysis_out: str) -> List[str]:
    """Collect event-overlay CSV/JSON paths from a Master Comprehensive output folder.

    When CandidateLocal_KHT_v0.1 has been run, this builds a simplified overlay CSV so
    the event appears clearly in the synchronized visual review.
    """
    if not analysis_out:
        return []
    root = Path(analysis_out)
    if not root.exists():
        return []
    tables = root / "tables"
    paths: List[str] = []
    for name in [
        "candidate_local_kht_analysis.csv",
        "candidate_local_kht_visual_overlay.csv",
        "mred_event_table.csv",
        "mred_visual_overlay.csv",
        "nast_visual_overlay.csv",
        "ocm_visual_overlay.csv",
        "combined_nast_visual_overlay.csv",
        "combined_ocm_visual_overlay.csv",
        "rsm_visual_overlay.csv",
        "confound_visual_overlay.csv",
        "external_noise_visual_overlay.csv",
        "avsync_visual_overlay.csv",
        "topo_osm_visual_overlay.csv",
        "kht_topo_visual_overlay.csv",
        "subtitle_visual_overlay.csv",
        "lso_visual_overlay.csv",
        "spm_visual_overlay.csv",
        "tti_visual_overlay.csv",
        "thermodynamic_theft_visual_overlay.csv",
        "thresholded_state_update_candidate_windows.csv",
        "state_locked_anchor_summary.csv",
        "postpeak_pncc_theta_contrasts.csv",
        "annotation_locked_theta_carryover_contrasts.csv",
    ]:
        q = tables / name
        if q.exists() and q.stat().st_size > 5:
            paths.append(str(q))
    cand = tables / "candidate_local_kht_analysis.csv"
    if cand.exists() and pd is not None:
        try:
            df = pd.read_csv(cand)
            rows = []
            for _, r in df.iterrows():
                t = r.get("time_sec", r.get("analysis_time", r.get("peak_sec", None)))
                try:
                    tf = float(t)
                except Exception:
                    continue
                aid = str(r.get("anchor_id", "CandidateLocal_KHT"))
                k = r.get("K_local", "")
                h = r.get("delta_theta_10_30_vs_pre", r.get("delta_theta_0_10_vs_pre", ""))
                interp = str(r.get("interpretation", ""))
                label = f"CandidateLocal_KHT {aid} K={k} theta={h} {interp}"
                rows.append({"start_sec": tf, "end_sec": tf + 0.75, "label": label, "category": "candidate_kht", "source": "candidate_local_kht_analysis.csv"})
            if rows:
                out = tables / "candidate_local_kht_visual_overlay.csv"
                pd.DataFrame(rows).to_csv(out, index=False)
                if str(out) not in paths:
                    paths.append(str(out))
        except Exception as exc:
            eprint(f"WARNING: could not build candidate KHT visual overlay: {exc}")

    mred = tables / "mred_event_table.csv"
    if mred.exists() and pd is not None:
        try:
            df = pd.read_csv(mred)
            rows = []
            for _, r in df.iterrows():
                t = r.get("time_sec", r.get("analysis_time", None))
                try:
                    tf = float(t)
                except Exception:
                    continue
                aid = str(r.get("anchor_id", "MRED"))
                mr = r.get("MR_score", "")
                enc = r.get("ENC_score", "")
                quad = str(r.get("mred_quadrant", ""))
                label = f"MRED {aid} MR={mr} ENC={enc} {quad}"
                rows.append({"start_sec": tf, "end_sec": tf + 0.9, "label": label, "category": "mred", "source": "mred_event_table.csv"})
            if rows:
                out = tables / "mred_visual_overlay.csv"
                pd.DataFrame(rows).to_csv(out, index=False)
                if str(out) not in paths:
                    paths.append(str(out))
        except Exception as exc:
            eprint(f"WARNING: could not build MRED visual overlay: {exc}")

    # v1.2.3: NAST and OCM overlays. These modules already write visual_overlay CSVs,
    # but this fallback builds simple overlays when only the analysis tables are present.
    nast = tables / "combined_nast_absorption_onset_candidates.csv"
    if not nast.exists():
        # support per-run output folders too
        matches = list(tables.glob("*_nast_absorption_onset_candidates.csv"))
    else:
        matches = [nast]
    if pd is not None:
        try:
            rows = []
            for src in matches:
                df = pd.read_csv(src)
                for _, r in df.iterrows():
                    t = r.get("phase_time_sec", r.get("time_sec", r.get("analysis_time", None)))
                    try:
                        tf = float(t)
                    except Exception:
                        continue
                    ph = str(r.get("phase", "NAST"))
                    nas = r.get("NAS_z", "")
                    status = str(r.get("status", ""))
                    label = f"NAST {ph} NAS={nas} {status}"
                    rows.append({"start_sec": tf, "end_sec": tf + 1.2, "label": label, "category": "nast", "source": src.name})
            if rows:
                out = tables / "nast_visual_overlay.csv"
                pd.DataFrame(rows).to_csv(out, index=False)
                if str(out) not in paths:
                    paths.append(str(out))
        except Exception as exc:
            eprint(f"WARNING: could not build NAST visual overlay: {exc}")

        try:
            rows = []
            src = tables / "combined_ocm_cue_epoch_table.csv"
            if not src.exists():
                matches = list(tables.glob("*_ocm_cue_epoch_table.csv"))
            else:
                matches = [src]
            for src in matches:
                df = pd.read_csv(src)
                if "cue_update_event" in df.columns:
                    df = df[df["cue_update_event"].astype(str).str.lower().isin(["true", "1", "yes"])]
                else:
                    df = df.head(0)
                for _, r in df.iterrows():
                    t = r.get("cue_time", r.get("time_sec", None))
                    try:
                        tf = float(t)
                    except Exception:
                        continue
                    ci = r.get("cue_index", "")
                    wmu = r.get("working_memory_update_WMU", "")
                    dr = r.get("digit_recognition_DR", "")
                    label = f"OCM cue {ci} DR={dr} WMU={wmu}"
                    rows.append({"start_sec": tf, "end_sec": tf + 0.9, "label": label, "category": "ocm", "source": src.name})
            if rows:
                out = tables / "ocm_visual_overlay.csv"
                pd.DataFrame(rows).to_csv(out, index=False)
                if str(out) not in paths:
                    paths.append(str(out))
        except Exception as exc:
            eprint(f"WARNING: could not build OCM visual overlay: {exc}")


        # v1.4.8: TTI / Reception-Extraction Tradeoff overlays.
        try:
            src = tables / "tti_timewindow_paired_deltas.csv"
            if src.exists():
                df = pd.read_csv(src)
                rows = []
                if "time_sec" in df.columns and "tti_timewindow" in df.columns:
                    x = df.dropna(subset=["time_sec", "tti_timewindow"]).copy()
                    if not x.empty:
                        for _, r in x.sort_values("tti_timewindow", ascending=False).head(10).iterrows():
                            tf = float(r["time_sec"])
                            rows.append({"start_sec": tf, "end_sec": tf + 2.0, "label": f"TTI +{float(r['tti_timewindow']):.2f}", "category": "tti_positive", "source": "tti_timewindow_paired_deltas.csv"})
                        for _, r in x.sort_values("tti_timewindow", ascending=True).head(5).iterrows():
                            tf = float(r["time_sec"])
                            rows.append({"start_sec": tf, "end_sec": tf + 2.0, "label": f"TTI {float(r['tti_timewindow']):.2f}", "category": "tti_negative", "source": "tti_timewindow_paired_deltas.csv"})
                if rows:
                    out = tables / "tti_visual_overlay.csv"
                    pd.DataFrame(rows).to_csv(out, index=False)
                    event_files.append(str(out))
        except Exception as exc:
            eprint(f"WARNING: could not build TTI visual overlay: {exc}")

        # v1.4.7: Topo-OSM and LSO/Subtitles overlays.
        try:
            rows = []
            for src in [tables / "topo_osm_event_table.csv", tables / "kht_topo_event_table.csv"]:
                if not src.exists():
                    continue
                df = pd.read_csv(src)
                for _, r in df.iterrows():
                    t = r.get("time_sec", r.get("analysis_time", r.get("semantic_anchor_estimate_sec", None)))
                    try:
                        tf = float(t)
                    except Exception:
                        continue
                    score = r.get("topo_state_proxy_z", r.get("K_HT_topo", r.get("K_local", "")))
                    label = f"TopoOSM {src.stem} score={score}"
                    rows.append({"start_sec": tf, "end_sec": tf + 1.0, "label": label, "category": "topo_osm", "source": src.name})
            if rows:
                out = tables / "topo_osm_visual_overlay.csv"
                pd.DataFrame(rows).to_csv(out, index=False)
                if str(out) not in paths:
                    paths.append(str(out))
        except Exception as exc:
            eprint(f"WARNING: could not build Topo-OSM visual overlay: {exc}")

        try:
            rows = []
            for src in [tables / "subtitle_line_event_table.csv", tables / "subtitle_phase_shift_table.csv"]:
                if not src.exists():
                    continue
                df = pd.read_csv(src)
                for _, r in df.iterrows():
                    t = r.get("semantic_anchor_estimate_sec", r.get("subtitle_onset_sec", None))
                    try:
                        tf = float(t)
                    except Exception:
                        continue
                    lid = r.get("line_id", "")
                    lec = r.get("LEC", "")
                    label = f"LSO subtitle {lid} LEC={lec}"
                    rows.append({"start_sec": tf, "end_sec": tf + 1.0, "label": label, "category": "lso_subtitle", "source": src.name})
            if rows:
                out = tables / "subtitle_visual_overlay.csv"
                pd.DataFrame(rows).to_csv(out, index=False)
                if str(out) not in paths:
                    paths.append(str(out))
        except Exception as exc:
            eprint(f"WARNING: could not build LSO subtitle visual overlay: {exc}")

    return paths

# ----------------------- v1.1 condition slicing overrides -----------------------
# These definitions intentionally override selected v1.0 functions above while reusing
# the tested v1.0 feature extraction and OpenCV renderer. The goal is KISS: tell the
# visualizer which PR-AYC-G branch/video you selected, and it will cut the XDF-derived
# data to the matching branch markers before rendering.

CONDITION_CHOICES = ["full", "control", "target", "override", "auto"]
CONDITION_ALIASES = {
    "control": ["control", "control_1", "phase-scrambled", "scrambled"],
    "target": ["target", "target_1", "natural", "narrative"],
    "override": ["override", "contextual_override", "contextual override", "contextual", "analytic"],
}


def normalize_condition(value: str) -> str:
    v = str(value or "full").strip().lower().replace("-", "_")
    if v in {"", "none", "all", "whole", "entire", "full_session"}:
        return "full"
    if v in {"ctx", "contextual", "contextual_override", "contextual override", "override", "ovr", "analytic"}:
        return "override"
    if v in {"target", "natural", "narrative", "meaning"}:
        return "target"
    if v in {"control", "phase_scrambled", "phase scrambled", "scrambled"}:
        return "control"
    if v == "auto":
        return "auto"
    return v if v in CONDITION_CHOICES else "full"


def condition_start_end_patterns(condition: str) -> Tuple[List[str], List[str]]:
    c = normalize_condition(condition)
    if c == "control":
        starts = [r"\bCONTROL(?:_\d+)?_START\b"]
        ends = [r"\bCONTROL(?:_\d+)?_END\b"]
    elif c == "target":
        starts = [r"\bTARGET(?:_\d+)?_START\b"]
        ends = [r"\bTARGET(?:_\d+)?_END\b"]
    elif c == "override":
        starts = [
            r"\bCONTEXTUAL_OVERRIDE(?:_\d+)?_START\b",
            r"\bOVERRIDE(?:_\d+)?_START\b",
            r"\bCONTEXTUAL(?:_\d+)?_START\b",
        ]
        ends = [
            r"\bCONTEXTUAL_OVERRIDE(?:_\d+)?_END\b",
            r"\bOVERRIDE(?:_\d+)?_END\b",
            r"\bCONTEXTUAL(?:_\d+)?_END\b",
        ]
    else:
        starts, ends = [], []
    return starts, ends


def marker_is_phase_boundary(marker: str) -> bool:
    m = str(marker).upper()
    # Reject instruction/rating/setup/load/time-out markers. We only want actual stimulus branch START/END.
    bad = ["INSTRUCTION", "RATING", "RATINGS", "LOAD_OK", "TIMEOUT", "WASHOUT", "BASELINE", "SETUP", "MEDIA_SELECTED", "SHA256"]
    return not any(b in m for b in bad)


def collect_marker_rows_from_streams(streams: Sequence[XDFStream]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for st in streams:
        if stream_score(st, "markers") <= 0 or len(st.time_stamps) == 0:
            continue
        vals = marker_values(st)
        for t, val in zip(st.time_stamps, vals):
            rows.append({"marker": str(val), "lsl_time": float(t), "source_stream": st.name})
    rows.sort(key=lambda r: r["lsl_time"])
    return rows


def resolve_condition_phase_from_xdf(xdf_path: str, condition: str, prepad: float = 0.0, postpad: float = 0.0) -> Dict[str, Any]:
    c = normalize_condition(condition)
    info: Dict[str, Any] = {"condition": c, "found": False, "source": "none", "warnings": []}
    if c in {"full", "auto"} or not xdf_path:
        info["warnings"].append("No branch slicing requested; rendering full available timeline.")
        return info
    try:
        streams = load_xdf_streams(xdf_path)
    except Exception as exc:
        info["warnings"].append(f"Could not load XDF for condition slicing: {exc}")
        return info
    rows = collect_marker_rows_from_streams(streams)
    starts, ends = condition_start_end_patterns(c)
    start_row = None
    end_row = None
    for row in rows:
        marker = str(row["marker"])
        if not marker_is_phase_boundary(marker):
            continue
        if any(re.search(p, marker, flags=re.IGNORECASE) for p in starts):
            start_row = row
            break
    if start_row:
        for row in rows:
            marker = str(row["marker"])
            if float(row["lsl_time"]) <= float(start_row["lsl_time"]):
                continue
            if not marker_is_phase_boundary(marker):
                continue
            if any(re.search(p, marker, flags=re.IGNORECASE) for p in ends):
                end_row = row
                break
    if not start_row or not end_row:
        info["warnings"].append(f"Could not find clean {c} START/END markers in the XDF marker streams. Rendering will fall back to full available timeline unless duration is set manually.")
        info["markers_seen_sample"] = [r.get("marker", "") for r in rows[:20]]
        return info
    start_lsl_raw = float(start_row["lsl_time"])
    end_lsl_raw = float(end_row["lsl_time"])
    start_lsl = max(start_lsl_raw - float(prepad), 0.0)
    end_lsl = end_lsl_raw + float(postpad)
    if end_lsl <= start_lsl:
        info["warnings"].append(f"Resolved {c} markers, but end <= start. Rendering full timeline.")
        return info
    start_regex = "|".join(starts)
    info.update({
        "found": True,
        "source": "xdf_marker_stream",
        "start_marker": start_row["marker"],
        "end_marker": end_row["marker"],
        "start_lsl_raw": start_lsl_raw,
        "end_lsl_raw": end_lsl_raw,
        "start_lsl": start_lsl,
        "end_lsl": end_lsl,
        "duration_sec": end_lsl - start_lsl,
        "prepad_sec": float(prepad),
        "postpad_sec": float(postpad),
        "start_regex": start_regex,
    })
    return info


def detect_video_branch(video_path: str) -> str:
    v = str(video_path or "").lower()
    name = Path(v).name
    if "control" in name or "phase_scrambled" in name or "scrambled" in name:
        return "control"
    if "override" in name or "contextual" in name:
        return "override"
    if "target" in name:
        return "target"
    return "unknown"


def branch_mismatch_warning(video_path: str, condition: str) -> str:
    c = normalize_condition(condition)
    b = detect_video_branch(video_path)
    if c in {"full", "auto"} or b == "unknown" or not video_path:
        return ""
    if b != c:
        return f"Selected condition is {c}, but selected video filename looks like {b}. Verify you selected the matching branch MP4."
    return ""


def filter_feature_dataframe_for_condition(df, condition: str) -> Tuple[Any, str]:
    if pd is None:
        return df, "pandas unavailable"
    c = normalize_condition(condition)
    if c in {"full", "auto"}:
        return df, "No condition filter applied."
    cond_cols = [col for col in df.columns if col.lower() in {"condition", "phase", "branch", "arm", "block"}]
    if not cond_cols:
        return df, "Feature CSV has no condition/phase/branch column; no row filtering applied. Use XDF markers for branch slicing, or provide a feature table with condition labels."
    col = cond_cols[0]
    aliases = CONDITION_ALIASES.get(c, [c])
    pattern = "|".join(re.escape(a.lower()) for a in aliases)
    mask = df[col].astype(str).str.lower().str.contains(pattern, regex=True, na=False)
    if mask.sum() == 0:
        return df, f"Feature CSV condition column '{col}' exists but no rows matched {c}; no filter applied."
    out = df.loc[mask].copy()
    # Reset time to zero if a time column exists; makes selected-condition review videos start at t=0.
    for tcol in ["time_sec", "rel_time_sec", "time", "t_sec", "seconds", "t"]:
        if tcol in out.columns:
            try:
                out[tcol] = pd.to_numeric(out[tcol], errors="coerce")
                out[tcol] = out[tcol] - float(np.nanmin(out[tcol].to_numpy(dtype=float)))
            except Exception:
                pass
            break
    return out, f"Filtered feature CSV by column '{col}' for condition '{c}': {int(mask.sum())} rows kept."


def features_from_dataframe_v11(df, source: str, duration_sec: Optional[float] = None, step_sec: float = 0.25) -> FeatureTable:
    if pd is None:
        raise RuntimeError("pandas required to read feature CSV files.")
    if df.empty:
        raise ValueError(f"Feature table is empty after filtering: {source}")
    cols = {c.lower(): c for c in df.columns}
    def find_col(patterns: Sequence[str], exclude: Sequence[str] = ()) -> Optional[str]:
        for exact in patterns:
            if exact.lower() in cols:
                return cols[exact.lower()]
        for c in df.columns:
            cl = c.lower()
            if any(p.lower() in cl for p in patterns) and not any(e.lower() in cl for e in exclude):
                return c
        return None
    time_col = find_col(["time_sec", "rel_time_sec", "time", "t_sec", "seconds", "t"])
    if time_col is None:
        src_t = np.arange(len(df), dtype=float) * step_sec
    else:
        src_t = pd.to_numeric(df[time_col], errors="coerce").to_numpy(dtype=float)
        # Always make feature CSV playback relative to its first available row.
        if np.any(np.isfinite(src_t)):
            src_t = src_t - float(np.nanmin(src_t))
    if duration_sec is None or duration_sec <= 0:
        duration_sec = float(np.nanmax(src_t)) if np.any(np.isfinite(src_t)) else len(df) * step_sec
    out_t = np.arange(0, max(step_sec, duration_sec), step_sec)
    def get_series(patterns: Sequence[str], exclude: Sequence[str] = ()) -> np.ndarray:
        col = find_col(patterns, exclude)
        if col is None:
            return np.full_like(out_t, np.nan)
        x = pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        return safe_interp(src_t, x, out_t)
    theta = get_series(["theta", "theta_power", "fm_theta"], exclude=["gamma"])
    gamma = get_series(["lower_gamma", "meaninggamma", "gamma_power", "gamma"], exclude=["theta"])
    hr = get_series(["heart_rate", "hr_bpm", "hr"], exclude=["hrv", "rmssd"])
    hrv = get_series(["rmssd", "hrv", "sdnn"])
    api = get_series(["api_a", "api", "autonomic"])
    resp = get_series(["respiration_rate", "resp_rate", "breath_rate", "respiration", "resp"])
    als = get_series(["als", "photodiode", "light", "OpenBCIAnalogAux"])
    if np.all(~np.isfinite(api)):
        api = compute_api_a_proxy(hr, hrv, resp)
    return FeatureTable(time_sec=out_t, theta=theta, gamma=gamma, hr=hr, hrv=hrv, api_a=api, resp=resp, als=als,
                        source=source, notes="Feature CSV columns were auto-detected by name. Condition filtering, if requested, was applied before rendering.")




FEATURE_CSV_PRIORITY_NAMES = [
    "human_translation_kht_feature_frame.csv",
    "her_time_resolved_feature_frame.csv",
    "time_resolved_feature_frame.csv",
    "feature_frame.csv",
]

FEATURE_CSV_GLOB_PATTERNS = [
    "*_time_resolved_feature_frame.csv",
    "*time_resolved*feature*.csv",
    "*human_translation*kht*feature*.csv",
    "*feature_frame*.csv",
]


def normalize_analysis_folder_path(analysis_out: str) -> Tuple[str, List[str]]:
    """Return a likely Master Suite analysis root folder and warnings.

    Users sometimes click a CSV file into the Analysis folder field because the
    old GUI used a file picker. If a file is supplied, recover by using the
    parent folder, or the parent of `tables/` when appropriate.
    """
    warnings: List[str] = []
    if not analysis_out:
        return "", warnings
    p = Path(str(analysis_out).strip().strip('"'))
    if not str(p):
        return "", warnings
    if p.is_file():
        if p.parent.name.lower() == "tables":
            root = p.parent.parent
            warnings.append(f"Analysis folder pointed to a file in tables/; using its parent analysis folder: {root}")
        else:
            root = p.parent
            warnings.append(f"Analysis folder pointed to a file; using its parent folder: {root}")
        return str(root), warnings
    return str(p), warnings


def discover_feature_csv_from_analysis_folder(analysis_out: str) -> Tuple[str, str]:
    """Find the best continuous feature CSV inside a Master Suite output folder."""
    root_str, _ = normalize_analysis_folder_path(analysis_out)
    if not root_str:
        return "", "no analysis folder supplied"
    root = Path(root_str)
    search_roots = []
    if (root / "tables").exists():
        search_roots.append(root / "tables")
    search_roots.append(root)

    for folder in search_roots:
        for name in FEATURE_CSV_PRIORITY_NAMES:
            cand = folder / name
            if cand.exists() and cand.is_file():
                return str(cand), f"auto-detected feature CSV by priority: {cand}"

    for folder in search_roots:
        for pat in FEATURE_CSV_GLOB_PATTERNS:
            matches = sorted([m for m in folder.glob(pat) if m.is_file()])
            if matches:
                return str(matches[0]), f"auto-detected feature CSV by pattern {pat}: {matches[0]}"
    return "", f"no feature CSV found under {root}"


def resolve_analysis_and_feature_inputs(args: argparse.Namespace) -> Tuple[str, str, List[str]]:
    """Resolve analysis folder + feature CSV, with safe recovery from old GUI behavior."""
    warnings: List[str] = []
    analysis_out_raw = getattr(args, "analysis_out", "") or ""
    feature_raw = getattr(args, "features", "") or ""

    analysis_root, path_warnings = normalize_analysis_folder_path(analysis_out_raw)
    warnings.extend(path_warnings)

    # If the old file-picker placed a CSV into analysis_out and no Feature CSV was set,
    # use that CSV as the feature file while also recovering the parent analysis folder.
    if not feature_raw and analysis_out_raw:
        p = Path(str(analysis_out_raw).strip().strip('"'))
        if p.is_file() and p.suffix.lower() == ".csv":
            feature_raw = str(p)
            warnings.append(f"Analysis folder field contained a CSV; using it as Feature CSV: {p}")

    if not feature_raw and analysis_root:
        feature_raw, note = discover_feature_csv_from_analysis_folder(analysis_root)
        warnings.append(note)

    return analysis_root, feature_raw, warnings

def features_from_csv_v11(path: str, condition: str, duration_sec: Optional[float] = None, step_sec: float = 0.25) -> Tuple[FeatureTable, str]:
    if pd is None:
        raise RuntimeError("pandas required to read feature CSV files.")
    df = pd.read_csv(path)
    df2, note = filter_feature_dataframe_for_condition(df, condition)
    return features_from_dataframe_v11(df2, source=f"feature_csv:{path}", duration_sec=duration_sec, step_sec=step_sec), note


def filter_events_for_condition_v11(events: Sequence[Event], condition: str) -> List[Event]:
    c = normalize_condition(condition)
    if c in {"full", "auto"}:
        return list(events)
    out: List[Event] = []
    for ev in events:
        text = " ".join([str(ev.label), str(ev.category), str(ev.source), json.dumps(ev.raw or {}, default=str)]).lower()
        mentions_control = "control" in text or "scrambled" in text
        mentions_target = "target" in text
        mentions_override = "override" in text or "contextual" in text or "analytic" in text
        # Keep unlabeled cue schedules / general annotations; drop clearly other-branch events.
        if c == "control" and (mentions_target or mentions_override):
            continue
        if c == "target" and (mentions_control or mentions_override):
            continue
        if c == "override" and (mentions_control or mentions_target and not mentions_override):
            continue
        out.append(ev)
    return out


def run_pipeline(args: argparse.Namespace) -> Dict[str, Any]:
    ensure_imports_for_runtime()
    out_path = Path(args.out or "PRAYCG_MasterSync_Output.mp4").resolve()
    out_dir = Path(args.out_dir).resolve() if getattr(args, "out_dir", "") else out_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    condition = normalize_condition(getattr(args, "condition", "full"))
    analysis_root, resolved_feature_csv, input_warnings = resolve_analysis_and_feature_inputs(args)
    if analysis_root:
        args.analysis_out = analysis_root
    if resolved_feature_csv and not getattr(args, "features", ""):
        args.features = resolved_feature_csv
    event_paths: List[str] = []
    event_paths.extend(collect_analysis_output_events(getattr(args, "analysis_out", "")))
    if getattr(args, "events", ""):
        for item in str(args.events).split(","):
            item = item.strip().strip('"')
            if item:
                event_paths.append(item)
    phase_info: Dict[str, Any] = {"condition": condition, "found": False, "warnings": []}
    duration = float(args.duration) if getattr(args, "duration", 0) else None
    branch_warning = branch_mismatch_warning(getattr(args, "video", ""), condition)
    if getattr(args, "xdf", "") and condition not in {"full", "auto"}:
        phase_info = resolve_condition_phase_from_xdf(args.xdf, condition, prepad=float(getattr(args, "condition_prepad", 0.0)), postpad=float(getattr(args, "condition_postpad", 0.0)))
        if phase_info.get("found"):
            if duration is None or duration <= 0:
                duration = float(phase_info["duration_sec"])
            if not getattr(args, "anchor_marker", ""):
                args.anchor_marker = str(phase_info.get("start_regex", ""))
    if args.demo:
        ft, events = make_demo_features(duration_sec=duration or 30.0, step_sec=args.feature_step)
        xdf_report: Dict[str, Any] = {"mode": "demo"}
    else:
        if args.video and (duration is None or duration <= 0):
            try:
                duration = get_video_info(args.video)["duration_sec"]
            except Exception:
                duration = None
        if args.features:
            ft, filter_note = features_from_csv_v11(args.features, condition=condition, duration_sec=duration, step_sec=float(args.feature_step))
            events = []
            xdf_report = {"mode": "feature_csv", "feature_csv": args.features, "feature_filter_note": filter_note}
        else:
            theta_band = parse_band(args.theta_band, (4.0, 8.0))
            gamma_band = parse_band(args.gamma_band, (30.0, 45.0))
            ft, events, xdf_report = features_from_xdf(
                args.xdf,
                duration_sec=duration,
                step_sec=float(args.feature_step),
                theta_band=theta_band,
                gamma_band=gamma_band,
                eeg_stream_name=getattr(args, "eeg_stream", ""),
                aux_stream_name=getattr(args, "aux_stream", ""),
                cardiac_stream_name=getattr(args, "cardiac_stream", ""),
                resp_stream_name=getattr(args, "resp_stream", ""),
                anchor_marker_regex=getattr(args, "anchor_marker", ""),
                als_aux_channel=int(getattr(args, "als_aux_channel", 1)),
            )
    file_events = load_event_files(event_paths)
    file_events = filter_events_for_condition_v11(file_events, condition)
    all_events = list(events) + file_events
    cats = [c.strip().lower() for c in str(getattr(args, "categories", "all")).split(",") if c.strip()]
    if not cats:
        cats = ["all"]
    render_events = filter_events(all_events, cats)
    # Render: selected branch/video always begins at t=0 because XDF features have been anchored to branch start.
    render_report = render_master_video(
        ft,
        render_events,
        out_mp4=str(out_path),
        stimulus_video=getattr(args, "video", "") or "",
        fps=float(args.fps),
        out_width=int(args.width),
        graph_height=int(args.graph_height),
        video_height=int(args.video_height),
        rolling_window_sec=float(args.rolling_window),
        duration_sec=float(args.duration) if getattr(args, "duration", 0) else None,
        show_als=not bool(getattr(args, "no_als_panel", False)),
    )
    feature_csv = out_dir / (out_path.stem + "_features_used.csv")
    events_csv = out_dir / (out_path.stem + "_events_used.csv")
    report_json = out_dir / (out_path.stem + "_render_report.json")
    write_feature_csv(feature_csv, ft)
    write_events_csv(events_csv, render_events)
    warnings = list(input_warnings)
    if branch_warning:
        warnings.append(branch_warning)
    warnings.extend(phase_info.get("warnings", []))
    report = {
        "schema": "PRAYCG_MasterSync_Visualizer_Report_v1_2_2_mred_overlay",
        "version": VERSION,
        "condition_selected": condition,
        "detected_video_branch": detect_video_branch(getattr(args, "video", "")),
        "phase_window": phase_info,
        "warnings": warnings,
        "render": render_report,
        "xdf_or_feature_report": xdf_report,
        "inputs": {
            "xdf": getattr(args, "xdf", ""),
            "feature_csv": getattr(args, "features", ""),
            "stimulus_video": getattr(args, "video", ""),
            "event_files": event_paths,
            "analysis_output_folder": getattr(args, "analysis_out", ""),
        },
        "sidecars": {
            "features_used_csv": str(feature_csv),
            "events_used_csv": str(events_csv),
            "render_report_json": str(report_json),
        },
        "boundary": "Visualization/audit only. Condition slicing aligns selected branch video with matching XDF marker interval when markers are available. Does not certify PR-AYC-G endpoint validity, meaning, OSM, hidden-Y biology, or human EEG mechanism.",
    }
    write_json(report_json, report)
    return {**render_report, "condition_selected": condition, "phase_window_found": bool(phase_info.get("found")), "features_csv": str(feature_csv), "events_csv": str(events_csv), "report_json": str(report_json), "warnings": warnings}


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="PRAYCG Master Synchronization Visualizer v1.2.6 with Control/Target/Override condition slicing")
    p.add_argument("--gui", action="store_true", help="Launch Tkinter GUI.")
    p.add_argument("--demo", action="store_true", help="Render a synthetic 30-second demo without XDF.")
    p.add_argument("--xdf", default="", help="Input XDF file.")
    p.add_argument("--features", default="", help="Optional precomputed feature CSV. If provided, raw XDF processing is skipped.")
    p.add_argument("--video", default="", help="Stimulus branch MP4 to place above graph panels.")
    p.add_argument("--condition", default="full", choices=CONDITION_CHOICES, help="Which PR-AYC-G branch this video represents. If control/target/override, XDF is cut to matching START/END markers.")
    p.add_argument("--condition-prepad", type=float, default=0.0, help="Seconds before branch START to include in XDF slice. Default 0 for exact video sync.")
    p.add_argument("--condition-postpad", type=float, default=0.0, help="Seconds after branch END to include in XDF slice. Default 0 for exact video sync.")
    p.add_argument("--events", default="", help="Comma-separated event CSV/JSON files to highlight, e.g. cue_schedule.json,state_locked_anchor_summary.csv")
    p.add_argument("--analysis-out", default="", help="Optional Master Comprehensive output folder. CandidateLocal_KHT and state-locked tables are auto-added as visual overlays.")
    p.add_argument("--out", default="", help="Output MP4 path.")
    p.add_argument("--out-dir", default="", help="Directory for sidecar CSV/JSON outputs. Defaults to MP4 folder.")
    p.add_argument("--fps", type=float, default=24.0, help="Output video FPS.")
    p.add_argument("--duration", type=float, default=0.0, help="Optional render duration seconds. 0 = infer from selected condition/video/features/XDF.")
    p.add_argument("--width", type=int, default=1280, help="Output width in pixels.")
    p.add_argument("--video-height", type=int, default=540, help="Top stimulus video panel height.")
    p.add_argument("--graph-height", type=int, default=620, help="Bottom graph panel height.")
    p.add_argument("--rolling-window", type=float, default=30.0, help="Seconds visible in rolling graph window.")
    p.add_argument("--categories", default="all", help="Event categories to show, comma-separated, or 'all'.")
    p.add_argument("--anchor-marker", default="", help="Advanced: regex for marker to define t=0. Usually leave blank and use --condition.")
    p.add_argument("--als-aux-channel", type=int, default=1, help="ALS channel index in analog AUX stream: 0=A5/D11, 1=A6/D12, 2=A7/D13.")
    p.add_argument("--feature-step", type=float, default=0.25, help="Feature time step seconds.")
    p.add_argument("--theta-band", default="4,8", help="Theta band as low,high Hz.")
    p.add_argument("--gamma-band", default="30,45", help="Gamma band as low,high Hz; default lower gamma 30-45.")
    p.add_argument("--eeg-stream", default="", help="Optional exact/partial EEG stream name override.")
    p.add_argument("--aux-stream", default="", help="Optional exact/partial analog AUX/ALS stream name override.")
    p.add_argument("--cardiac-stream", default="", help="Optional exact/partial cardiac stream name override.")
    p.add_argument("--resp-stream", default="", help="Optional exact/partial respiration stream name override.")
    p.add_argument("--no-als-panel", action="store_true", help="Hide ALS panel.")
    return p


def launch_gui() -> int:
    ensure_imports_for_runtime()
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
    except Exception as exc:
        raise RuntimeError("Tkinter GUI unavailable; run from CLI instead.") from exc

    class App(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("PRAYCG MasterSync Visualizer v1.2.1 - Folder Picker + Auto Feature CSV")
            self.geometry("760x760")
            self.vars = {
                "xdf": tk.StringVar(), "features": tk.StringVar(), "video": tk.StringVar(), "events": tk.StringVar(), "analysis_out": tk.StringVar(),
                "out": tk.StringVar(value=str(Path.cwd() / "PRAYCG_MasterSync_condition_review.mp4")),
                "condition": tk.StringVar(value="target"), "fps": tk.StringVar(value="24"),
                "width": tk.StringVar(value="1280"), "video_height": tk.StringVar(value="540"), "graph_height": tk.StringVar(value="620"),
                "rolling": tk.StringVar(value="30"), "als_ch": tk.StringVar(value="1"),
            }
            self.build()
        def row_file(self, parent, label, key, ftypes=None, folder=False, save=False):
            fr = ttk.Frame(parent); fr.pack(fill="x", pady=4)
            ttk.Label(fr, text=label, width=18).pack(side="left")
            ttk.Entry(fr, textvariable=self.vars[key]).pack(side="left", fill="x", expand=True)
            def browse():
                if folder:
                    p = filedialog.askdirectory(title=f"Select {label}")
                elif save:
                    p = filedialog.asksaveasfilename(title=f"Select {label}", defaultextension=".mp4", filetypes=ftypes or [("MP4", "*.mp4"), ("All", "*.*")])
                else:
                    p = filedialog.askopenfilename(title=f"Select {label}", filetypes=ftypes or [("All", "*.*")])
                if p: self.vars[key].set(p)
            ttk.Button(fr, text=("Browse Folder" if folder else "Browse"), command=browse).pack(side="left", padx=3)
        def build(self):
            pad = ttk.Frame(self, padding=10); pad.pack(fill="both", expand=True)
            ttk.Label(pad, text="PRAYCG Master Synchronization Visualizer v1.2.6.1", font=("Arial", 15, "bold")).pack(anchor="w")
            ttk.Label(pad, text="Select the branch matching the MP4. The XDF is cut to CONTROL_1/TARGET_1/CONTEXTUAL_OVERRIDE markers when available.", wraplength=720).pack(anchor="w", pady=(0,8))
            self.row_file(pad, "XDF", "xdf", [("XDF", "*.xdf"), ("All", "*.*")])
            self.row_file(pad, "Feature CSV", "features", [("CSV", "*.csv"), ("All", "*.*")])
            self.row_file(pad, "Stimulus MP4", "video", [("MP4", "*.mp4"), ("All", "*.*")])
            self.row_file(pad, "Events", "events", [("Events", "*.csv *.json"), ("All", "*.*")])
            self.row_file(pad, "Analysis folder", "analysis_out", folder=True)
            ttk.Label(pad, text="Tip: choose the Master Comprehensive output folder. If Feature CSV is blank, the visualizer will auto-detect tables/human_translation_kht_feature_frame.csv or *_time_resolved_feature_frame.csv.", wraplength=720).pack(anchor="w", pady=(0,6))
            fr = ttk.Frame(pad); fr.pack(fill="x", pady=8)
            ttk.Label(fr, text="Branch / condition", width=18).pack(side="left")
            for val, txt in [("control", "Control"), ("target", "Target"), ("override", "Contextual Override"), ("full", "Full session")]:
                ttk.Radiobutton(fr, text=txt, value=val, variable=self.vars["condition"]).pack(side="left", padx=5)
            self.row_file(pad, "Output MP4", "out", [("MP4", "*.mp4"), ("All", "*.*")], save=True)
            grid = ttk.Frame(pad); grid.pack(fill="x", pady=6)
            for i,(lab,key) in enumerate([("FPS","fps"),("Width","width"),("Video H","video_height"),("Graph H","graph_height"),("Window sec","rolling"),("ALS ch","als_ch")]):
                ttk.Label(grid, text=lab).grid(row=i//3, column=(i%3)*2, sticky="e", padx=4, pady=3)
                ttk.Entry(grid, textvariable=self.vars[key], width=10).grid(row=i//3, column=(i%3)*2+1, sticky="w", padx=4, pady=3)
            btns = ttk.Frame(pad); btns.pack(fill="x", pady=10)
            ttk.Button(btns, text="Render selected branch", command=self.render).pack(side="left", padx=4)
            ttk.Button(btns, text="Render demo", command=self.demo).pack(side="left", padx=4)
            self.log = tk.Text(pad, height=16); self.log.pack(fill="both", expand=True)
        def ns(self, demo=False):
            return argparse.Namespace(gui=False, demo=demo, xdf=self.vars["xdf"].get(), features=self.vars["features"].get(),
                video=self.vars["video"].get(), events=self.vars["events"].get(), out=self.vars["out"].get(), out_dir="",
                condition=self.vars["condition"].get(), condition_prepad=0.0, condition_postpad=0.0, analysis_out=self.vars["analysis_out"].get(),
                fps=float(self.vars["fps"].get()), width=int(self.vars["width"].get()),
                video_height=int(self.vars["video_height"].get()), graph_height=int(self.vars["graph_height"].get()),
                rolling_window=float(self.vars["rolling"].get()), categories="all", anchor_marker="", als_aux_channel=int(self.vars["als_ch"].get()),
                feature_step=0.25, theta_band="4,8", gamma_band="30,45", eeg_stream="", aux_stream="", cardiac_stream="", resp_stream="", no_als_panel=False, duration=0.0)
        def execute(self, ns):
            try:
                self.log.insert("end", "Starting render...\n"); self.log.see("end"); self.update_idletasks()
                result = run_pipeline(ns)
                self.log.insert("end", json.dumps(result, indent=2) + "\n"); self.log.see("end")
                messagebox.showinfo("Done", "Rendered:\n" + result.get("out_mp4", ns.out))
            except Exception as exc:
                tb = traceback.format_exc(); self.log.insert("end", tb + "\n"); self.log.see("end")
                messagebox.showerror("Render failed", str(exc))
        def render(self):
            if not self.vars["xdf"].get() and not self.vars["features"].get() and not self.vars["analysis_out"].get():
                messagebox.showwarning("Missing data", "Choose an XDF, a Feature CSV, or an Analysis folder containing a feature table."); return
            if not self.vars["video"].get():
                messagebox.showwarning("Missing video", "Choose the matching Control, Target, or Override MP4."); return
            self.execute(self.ns(False))
        def demo(self):
            self.execute(self.ns(True))
    app = App(); app.mainloop(); return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    if args.gui or (not args.demo and not args.xdf and not args.features and not getattr(args, "analysis_out", "")):
        return launch_gui()
    if not args.out:
        parser.error("--out is required in CLI mode")
    try:
        result = run_pipeline(args)
        print(json.dumps(result, indent=2))
        return 0
    except Exception as exc:
        eprint("ERROR:", exc)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
