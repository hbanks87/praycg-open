#!/usr/bin/env python3
"""
PRAYCG StimulusFingerprint + CET/EET Regressor Builder v1.8

Purpose
-------
Generate continuous, analysis-ready exogenous stimulus regressors for PR-AYC-G:
  - visual luminance / motion / cut-train / flash proxies
  - audio RMS / envelope / derivative proxies
  - number-cue train and cue-phase regressors
  - ALS/fullscreen start-pulse regressors from cue/media-prep metadata
  - dominant-frequency / rhythm maps for CET
  - anchor-window stimulus vectors for EET

Boundary
--------
This script analyzes the *stimulus file*, not the participant. Pixel luminance is a
video proxy, audio dBFS/RMS is a digital audio proxy, and cue/ALS regressors belong
to the external input vector u(t). None of these outputs are biological hidden-Y,
OSM, meaning, immersion, or neural endpoint proof.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import cv2
import numpy as np
import pandas as pd
from scipy import signal
from scipy.io import wavfile

EPS = 1e-12
SCHEMA = "PRAYCG_StimulusFingerprint_CET_EET_v1_8"
VERSION = "1.8"


def now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def zscore(x: Sequence[float]) -> np.ndarray:
    arr = np.asarray(x, dtype=float)
    if arr.size == 0:
        return arr
    finite = np.isfinite(arr)
    if not np.any(finite):
        return np.zeros_like(arr, dtype=float)
    med = np.nanmedian(arr[finite])
    mad = np.nanmedian(np.abs(arr[finite] - med))
    scale = 1.4826 * mad if mad > EPS else np.nanstd(arr[finite])
    if not np.isfinite(scale) or scale < EPS:
        return np.zeros_like(arr, dtype=float)
    out = (arr - med) / scale
    out[~finite] = 0.0
    return out


def clamp01(x: float) -> float:
    try:
        if not np.isfinite(x):
            return 0.0
    except Exception:
        return 0.0
    return float(max(0.0, min(1.0, x)))


def trapz_safe(y, x=None) -> float:
    """NumPy-version-safe trapezoidal integration.

    NumPy 2.x favors np.trapezoid while some environments have deprecated or
    removed np.trapz. This helper avoids aborting a whole three-branch
    StimulusFingerprint run because one integration function name differs.
    """
    y = np.asarray(y, dtype=float)
    if x is not None:
        x = np.asarray(x, dtype=float)
    try:
        if hasattr(np, "trapezoid"):
            return float(np.trapezoid(y, x))
        if hasattr(np, "trapz"):
            return float(np.trapz(y, x))
    except Exception:
        pass
    # Conservative fallback for old/minimal NumPy-like installs.
    if y.size < 2:
        return 0.0
    if x is None:
        dx = 1.0
        return float(np.sum((y[:-1] + y[1:]) * 0.5 * dx))
    if x.size != y.size or x.size < 2:
        return 0.0
    dx = np.diff(x)
    return float(np.sum((y[:-1] + y[1:]) * 0.5 * dx))


def safe_write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys: List[str] = []
    for r in rows:
        for k in r.keys():
            if k not in keys:
                keys.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_json(path: Optional[Path]) -> Dict[str, Any]:
    if path is None:
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_cue_events(path: Optional[Path]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    obj = read_json(path)
    events = obj.get("cue_events") or []
    return events, obj


def load_anchor_events(path: Optional[Path]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    obj = read_json(path)
    if not obj:
        return [], {}
    anchors = obj.get("anchors") or obj.get("anchor_events") or []
    return anchors, obj


def extract_audio_to_wav(video_path: Path, wav_path: Path, sr: int = 48000) -> Tuple[bool, str]:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        return False, "ffmpeg not found on PATH"
    cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(video_path), "-vn", "-ac", "1", "-ar", str(sr), str(wav_path)]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        return False, proc.stderr.strip() or f"ffmpeg returned {proc.returncode}"
    if not wav_path.exists() or wav_path.stat().st_size <= 0:
        return False, "ffmpeg produced no audio WAV"
    return True, "ok"


def interpolate_to_grid(times: np.ndarray, values: np.ndarray, grid: np.ndarray) -> np.ndarray:
    if len(times) == 0 or len(values) == 0:
        return np.full_like(grid, np.nan, dtype=float)
    mask = np.isfinite(times) & np.isfinite(values)
    if np.sum(mask) < 2:
        return np.full_like(grid, np.nan, dtype=float)
    return np.interp(grid, times[mask], values[mask], left=np.nan, right=np.nan)


def bandpower_welch(values: np.ndarray, fs: float, lo: float, hi: float) -> float:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) < 8 or fs <= 0:
        return 0.0
    values = values - np.nanmean(values)
    nperseg = min(256, max(8, len(values)//2))
    freqs, psd = signal.welch(values, fs=fs, nperseg=nperseg, detrend="constant")
    mask = (freqs >= lo) & (freqs < hi)
    if not np.any(mask):
        return 0.0
    return float(trapz_safe(psd[mask], freqs[mask]))


def dominant_frequency(values: np.ndarray, fs: float, lo: float = 0.02, hi: float = 8.0) -> Dict[str, Any]:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) < 16 or fs <= 0:
        return {"dominant_freq_hz": np.nan, "dominant_power": 0.0, "band_power": 0.0, "rhythm_concentration_0_1": 0.0}
    values = values - np.nanmean(values)
    nperseg = min(512, max(16, len(values)//2))
    freqs, psd = signal.welch(values, fs=fs, nperseg=nperseg, detrend="constant")
    mask = (freqs >= lo) & (freqs <= min(hi, fs/2.0))
    if not np.any(mask):
        return {"dominant_freq_hz": np.nan, "dominant_power": 0.0, "band_power": 0.0, "rhythm_concentration_0_1": 0.0}
    f = freqs[mask]
    p = psd[mask]
    idx = int(np.argmax(p))
    total = float(trapz_safe(p, f) + EPS)
    dom_p = float(p[idx])
    # approximate concentration as power in +/- one frequency bin around peak divided by band power
    df = float(np.median(np.diff(f))) if len(f) > 2 else 0.05
    peak_mask = (f >= f[idx] - df) & (f <= f[idx] + df)
    peak_power = float(trapz_safe(p[peak_mask], f[peak_mask])) if np.any(peak_mask) else dom_p
    return {"dominant_freq_hz": float(f[idx]), "dominant_power": dom_p, "band_power": total, "rhythm_concentration_0_1": clamp01(peak_power / total)}


def make_time_grid(duration_sec: float, hz: float) -> np.ndarray:
    dt = 1.0 / float(hz)
    n = int(math.ceil(max(0.0, duration_sec) * hz)) + 1
    return np.arange(n, dtype=float) * dt


def get_video_props(path: Path) -> Dict[str, Any]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {path}")
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    cap.release()
    return {"fps": fps, "frame_count": frame_count, "width": width, "height": height, "duration_sec": frame_count / fps if fps > 0 else 0.0}


def analyze_visual(video_path: Path, sample_hz: float, resize_width: int) -> Tuple[pd.DataFrame, Dict[str, Any], List[float]]:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    duration = frame_count / fps if fps > 0 else 0.0
    step = max(1, int(round(fps / max(sample_hz, 0.1)))) if fps > 0 else 1
    eff_hz = fps / step if fps > 0 else sample_hz

    rows: List[Dict[str, Any]] = []
    prev_y: Optional[np.ndarray] = None
    prev_hist: Optional[np.ndarray] = None
    frame_idx = -1
    while True:
        ok, frame = cap.read()
        if not ok or frame is None:
            break
        frame_idx += 1
        if frame_idx % step != 0:
            continue
        h, w = frame.shape[:2]
        scale = resize_width / float(w) if w > resize_width else 1.0
        if scale != 1.0:
            frame_small = cv2.resize(frame, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)
        else:
            frame_small = frame
        b, g, r = cv2.split(frame_small.astype(np.float32))
        y = 0.2126*r + 0.7152*g + 0.0722*b
        lum_mean = float(np.mean(y))
        lum_std = float(np.std(y))
        hist = cv2.calcHist([np.clip(y,0,255).astype(np.uint8)], [0], None, [32], [0,256]).flatten()
        hist = hist / (np.sum(hist) + EPS)
        if prev_y is None:
            visual_change = 0.0
            hist_delta = 0.0
            optical_flow_proxy = 0.0
        else:
            diff = np.abs(y - prev_y)
            visual_change = float(np.mean(diff))
            optical_flow_proxy = float(np.percentile(diff, 90))
            hist_delta = float(0.5 * np.sum(np.abs(hist - prev_hist))) if prev_hist is not None else 0.0
        edges = cv2.Canny(np.clip(y,0,255).astype(np.uint8), 80, 160)
        edge_density = float(np.mean(edges > 0))
        rows.append({
            "time_sec": frame_idx / fps if fps > 0 else len(rows) / eff_hz,
            "frame_index": frame_idx,
            "luminance_mean": lum_mean,
            "luminance_std": lum_std,
            "visual_change_mean_abs": visual_change,
            "optical_flow_proxy_p90_absdiff": optical_flow_proxy,
            "histogram_delta": hist_delta,
            "edge_density": edge_density,
        })
        prev_y = y.copy()
        prev_hist = hist
    cap.release()
    df = pd.DataFrame(rows)
    if df.empty:
        return df, {"fps": fps, "frame_count": frame_count, "width": width, "height": height, "duration_sec": duration, "sample_hz_effective": eff_hz}, []
    # Robust cut detection
    cut_raw = zscore(df["visual_change_mean_abs"].values) + 0.75*zscore(df["histogram_delta"].values)
    th = max(float(np.nanpercentile(cut_raw, 97.5)), float(np.nanmean(cut_raw) + 2.5*np.nanstd(cut_raw))) if len(cut_raw) > 8 else np.inf
    df["cut_score_z"] = cut_raw
    df["cut_event"] = (cut_raw > th).astype(int)
    # Merge cuts closer than 0.35 s
    cut_times = df.loc[df["cut_event"] == 1, "time_sec"].tolist()
    kept: List[float] = []
    last = -1e9
    for t in cut_times:
        if t - last >= 0.35:
            kept.append(float(t)); last = float(t)
    df["cut_event"] = 0
    if kept:
        for t in kept:
            idx = int(np.argmin(np.abs(df["time_sec"].values - t)))
            df.loc[idx, "cut_event"] = 1
    lum_diff = np.abs(np.diff(df["luminance_mean"].values, prepend=df["luminance_mean"].values[0]))
    df["luminance_absdiff"] = lum_diff
    df["flash_event"] = ((lum_diff > 25.0) | (df["visual_change_mean_abs"].values > 45.0)).astype(int)
    metrics = {
        "fps": fps,
        "frame_count": frame_count,
        "width": width,
        "height": height,
        "duration_sec": duration,
        "sample_hz_effective": eff_hz,
        "sampled_frames": int(len(df)),
        "luminance_mean_avg": float(df["luminance_mean"].mean()),
        "luminance_mean_std_over_time": float(df["luminance_mean"].std()),
        "visual_change_mean": float(df["visual_change_mean_abs"].mean()),
        "optical_flow_proxy_mean": float(df["optical_flow_proxy_p90_absdiff"].mean()),
        "cut_count_estimated": int(df["cut_event"].sum()),
        "cut_rate_per_sec": float(df["cut_event"].sum() / max(duration, EPS)),
        "flash_event_count": int(df["flash_event"].sum()),
        "flash_risk_fraction": float(df["flash_event"].mean()),
    }
    return df, metrics, kept


def analyze_audio(video_path: Path, grid: np.ndarray, merge_hz: float) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    with tempfile.TemporaryDirectory() as td:
        wav_path = Path(td) / "audio.wav"
        ok, msg = extract_audio_to_wav(video_path, wav_path)
        if not ok:
            df = pd.DataFrame({"time_sec": grid, "audio_rms": np.nan, "audio_dbfs": np.nan, "audio_rms_derivative": np.nan})
            return df, {"has_audio": False, "reason": msg, "audio_duration_sec": 0.0}
        sr, x = wavfile.read(str(wav_path))
        if x.ndim > 1:
            x = np.mean(x, axis=1)
        if np.issubdtype(x.dtype, np.integer):
            x = x.astype(np.float32) / float(np.iinfo(x.dtype).max)
        else:
            x = x.astype(np.float32)
        win = max(1, int(round((1.0/merge_hz) * sr)))
        hop = win
        rows = []
        for start in range(0, len(x), hop):
            seg = x[start:min(len(x), start+win)]
            if len(seg) == 0: continue
            rms = float(np.sqrt(np.mean(seg.astype(float)**2)))
            t = (start + len(seg)/2.0) / float(sr)
            rows.append({"time_sec": t, "audio_rms": rms, "audio_dbfs": float(20*np.log10(rms+EPS))})
        raw = pd.DataFrame(rows)
        rms = interpolate_to_grid(raw["time_sec"].values, raw["audio_rms"].values, grid) if not raw.empty else np.full_like(grid, np.nan)
        db = 20*np.log10(rms+EPS)
        deriv = np.diff(rms, prepend=rms[0]) if np.any(np.isfinite(rms)) else np.full_like(rms, np.nan)
        out = pd.DataFrame({"time_sec": grid, "audio_rms": rms, "audio_dbfs": db, "audio_rms_derivative": deriv})
        finite_rms = np.isfinite(rms)
        finite_db = np.isfinite(db)
        metrics = {
            "has_audio": True,
            "sample_rate_hz": int(sr),
            "audio_duration_sec": float(len(x)/sr),
            "rms_mean": float(np.nanmean(rms)) if np.any(finite_rms) else 0.0,
            "rms_std": float(np.nanstd(rms)) if np.any(finite_rms) else 0.0,
            "dbfs_mean": float(np.nanmean(db)) if np.any(finite_db) else np.nan,
            "dbfs_peak": float(np.nanmax(db)) if np.any(finite_db) else np.nan,
            "silence_fraction_dbfs_lt_minus55": float(np.nanmean(db < -55.0)) if np.any(finite_db) else np.nan,
        }
        return out, metrics


def cue_regressors(grid: np.ndarray, cue_events: List[Dict[str, Any]], cue_obj: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any], pd.DataFrame]:
    cue_on = np.zeros_like(grid, dtype=float)
    cue_impulse = np.zeros_like(grid, dtype=float)
    cue_value = np.zeros_like(grid, dtype=float)
    cue_idx = np.zeros_like(grid, dtype=float)
    events_rows: List[Dict[str, Any]] = []
    for ev in cue_events:
        try:
            st = float(ev.get("start_sec")); en = float(ev.get("end_sec", st)); val = float(ev.get("value", 0)); idx = float(ev.get("cue_index", 0))
        except Exception:
            continue
        mask = (grid >= st) & (grid < en)
        cue_on[mask] = 1.0
        cue_value[mask] = val
        cue_idx[mask] = idx
        nearest = int(np.argmin(np.abs(grid - st))) if len(grid) else 0
        if 0 <= nearest < len(cue_impulse): cue_impulse[nearest] = 1.0
        events_rows.append({
            "cue_index": int(idx), "value": val, "start_sec": st, "end_sec": en,
            "duration_sec": en-st,
            "contrast_pre_badge_0_1": ev.get("contrast_pre_badge_0_1"),
            "pre_badge_background_luminance": ev.get("pre_badge_background_luminance"),
            "badge_x1": ev.get("badge_x1"), "badge_y1": ev.get("badge_y1"), "badge_x2": ev.get("badge_x2"), "badge_y2": ev.get("badge_y2"),
        })
    cue_design = cue_obj.get("cue_design", {}) if cue_obj else {}
    interval = float(cue_design.get("interval_sec", 3.0) or 3.0)
    cue_freq = 1.0 / interval if interval > 0 else np.nan
    phase = 2*np.pi*cue_freq*grid if np.isfinite(cue_freq) else np.zeros_like(grid)
    df = pd.DataFrame({
        "time_sec": grid,
        "cue_on": cue_on,
        "cue_impulse": cue_impulse,
        "cue_value": cue_value,
        "cue_index_active": cue_idx,
        "cue_phase_sin": np.sin(phase),
        "cue_phase_cos": np.cos(phase),
        "cue_nominal_frequency_hz": np.full_like(grid, cue_freq if np.isfinite(cue_freq) else np.nan, dtype=float),
    })
    events_df = pd.DataFrame(events_rows)
    summary = {
        "cue_count": int(len(events_rows)),
        "expected_sum": float(np.nansum([r["value"] for r in events_rows])) if events_rows else 0.0,
        "cue_interval_sec": interval,
        "cue_frequency_hz": cue_freq,
        "has_contrast_qc": bool(any(pd.notna(r.get("contrast_pre_badge_0_1")) for r in events_rows)),
        "mean_contrast_pre_badge": float(events_df["contrast_pre_badge_0_1"].dropna().mean()) if not events_df.empty and "contrast_pre_badge_0_1" in events_df else np.nan,
        "min_contrast_pre_badge": float(events_df["contrast_pre_badge_0_1"].dropna().min()) if not events_df.empty and "contrast_pre_badge_0_1" in events_df and len(events_df["contrast_pre_badge_0_1"].dropna()) else np.nan,
    }
    return df, summary, events_df


def als_regressor(grid: np.ndarray, cue_obj: Dict[str, Any]) -> pd.DataFrame:
    pulse = np.zeros_like(grid, dtype=float)
    events = cue_obj.get("sensor_timing_pulse_events") or []
    for ev in events:
        try:
            st = float(ev.get("start_sec", 0)); en = float(ev.get("end_sec", st+1))
        except Exception:
            continue
        pulse[(grid >= st) & (grid < en)] = 1.0
    return pd.DataFrame({"time_sec": grid, "als_start_pulse_regressor": pulse})


def merge_branch(video_path: Path, condition: str, out_dir: Path, args: argparse.Namespace, cue_events: List[Dict[str, Any]], cue_obj: Dict[str, Any], anchors: List[Dict[str, Any]]) -> Dict[str, Any]:
    props = get_video_props(video_path)
    duration = props["duration_sec"]
    grid = make_time_grid(duration, args.merge_hz)
    visual_df, visual_metrics, cut_times = analyze_visual(video_path, args.video_sample_hz, args.resize_width)
    audio_df, audio_metrics = analyze_audio(video_path, grid, args.merge_hz)
    cue_df, cue_summary, cue_events_df = cue_regressors(grid, cue_events, cue_obj)
    als_df = als_regressor(grid, cue_obj)

    # interpolate visual to analysis grid
    vcols = ["luminance_mean", "luminance_std", "visual_change_mean_abs", "optical_flow_proxy_p90_absdiff", "histogram_delta", "edge_density", "cut_score_z", "cut_event", "flash_event"]
    merged = pd.DataFrame({"time_sec": grid})
    if not visual_df.empty:
        for col in vcols:
            if col in visual_df.columns:
                if col in ["cut_event", "flash_event"]:
                    arr = np.zeros_like(grid)
                    times = visual_df.loc[visual_df[col] == 1, "time_sec"].values
                    for t in times:
                        idx = int(np.argmin(np.abs(grid - t)))
                        arr[idx] = 1.0
                    merged[col] = arr
                else:
                    merged[col] = interpolate_to_grid(visual_df["time_sec"].values, visual_df[col].values, grid)
    else:
        for col in vcols: merged[col] = np.nan
    # audio, cue, als
    for df in [audio_df, cue_df, als_df]:
        for col in df.columns:
            if col != "time_sec": merged[col] = df[col].values
    merged.insert(0, "condition", condition)
    merged.insert(1, "stimulus_file", str(video_path))

    # z/regressor columns
    for raw, zname in [
        ("luminance_mean", "luminance_z"), ("visual_change_mean_abs", "visual_change_z"),
        ("optical_flow_proxy_p90_absdiff", "optical_flow_z"), ("histogram_delta", "histogram_delta_z"),
        ("audio_rms", "audio_rms_z"), ("audio_rms_derivative", "audio_derivative_z")
    ]:
        merged[zname] = zscore(merged[raw].values) if raw in merged.columns else np.nan

    # CET-ready output
    cet_cols = ["condition", "time_sec", "luminance_z", "visual_change_z", "optical_flow_z", "histogram_delta_z", "cut_event", "flash_event", "audio_rms_z", "audio_derivative_z", "cue_on", "cue_impulse", "cue_value", "cue_phase_sin", "cue_phase_cos", "als_start_pulse_regressor"]
    for c in cet_cols:
        if c not in merged.columns:
            merged[c] = np.nan
    merged[cet_cols].to_csv(out_dir / f"cet_regressors_{condition}.csv", index=False)
    merged.to_csv(out_dir / f"stimulus_exogenous_regressor_frame_{condition}.csv", index=False)
    visual_df.to_csv(out_dir / f"stimulus_visual_timeseries_{condition}.csv", index=False)
    audio_df.to_csv(out_dir / f"stimulus_audio_timeseries_{condition}.csv", index=False)
    cue_df.to_csv(out_dir / f"stimulus_cue_regressors_{condition}.csv", index=False)
    if not cue_events_df.empty:
        cue_events_df.to_csv(out_dir / f"cue_visibility_and_schedule_qc_{condition}.csv", index=False)

    # rhythm summary
    rhythm_rows = []
    for col in ["luminance_mean", "visual_change_mean_abs", "optical_flow_proxy_p90_absdiff", "histogram_delta", "cut_event", "audio_rms", "audio_rms_derivative", "cue_impulse", "cue_on"]:
        if col in merged.columns:
            vals = merged[col].values.astype(float)
            res = dominant_frequency(vals, args.merge_hz, lo=args.freq_low, hi=args.freq_high)
            cue_freq = cue_summary.get("cue_frequency_hz", np.nan)
            cue_band = bandpower_welch(vals, args.merge_hz, max(0.001, cue_freq-0.05), cue_freq+0.05) if np.isfinite(cue_freq) else 0.0
            total_band = bandpower_welch(vals, args.merge_hz, args.freq_low, min(args.freq_high, args.merge_hz/2.0))
            rhythm_rows.append({"condition": condition, "regressor": col, **res, "cue_frequency_hz": cue_freq, "cue_band_power_pm_0_05hz": cue_band, "cue_band_fraction": float(cue_band/(total_band+EPS))})
    pd.DataFrame(rhythm_rows).to_csv(out_dir / f"stimulus_rhythm_summary_{condition}.csv", index=False)

    # STFT dominant freq map (simple rolling spectrogram rows)
    stft_rows = []
    for col in ["luminance_mean", "visual_change_mean_abs", "audio_rms", "cue_on"]:
        if col in merged.columns:
            vals = np.asarray(merged[col].fillna(0).values, dtype=float)
            if len(vals) >= 16:
                nperseg = min(max(16, int(args.stft_window_sec * args.merge_hz)), len(vals))
                noverlap = int(max(0, min(nperseg-1, nperseg - max(1, int(args.stft_step_sec * args.merge_hz)))))
                f, t, Sxx = signal.spectrogram(vals - np.nanmean(vals), fs=args.merge_hz, nperseg=nperseg, noverlap=noverlap, scaling="density", mode="psd")
                band = (f >= args.freq_low) & (f <= min(args.freq_high, args.merge_hz/2.0))
                for ti, tv in enumerate(t):
                    if np.any(band):
                        p = Sxx[band, ti]
                        fb = f[band]
                        if len(p) and np.nanmax(p) > 0:
                            di = int(np.nanargmax(p)); domf = float(fb[di]); domp = float(p[di])
                        else: domf, domp = np.nan, 0.0
                    else: domf, domp = np.nan, 0.0
                    stft_rows.append({"condition": condition, "regressor": col, "window_center_sec": float(tv), "dominant_freq_hz": domf, "dominant_power": domp})
    pd.DataFrame(stft_rows).to_csv(out_dir / f"stimulus_dominant_frequency_timeseries_{condition}.csv", index=False)

    # Anchor stimulus vectors for EET
    anchor_rows = []
    if anchors:
        for a in anchors:
            aid = a.get("anchor_id") or a.get("id") or "ANCHOR"
            t0 = a.get("rendered_time_sec") or a.get("rendered_time_sec_estimate") or a.get("time_sec")
            try: t0 = float(t0)
            except Exception: continue
            pre = a.get("pre_window_sec", [-10, 0]); peak = a.get("peak_search_window_sec", [0, 10]); theta = a.get("theta_carryover_window_sec", [10, 30])
            windows = {"pre": pre, "peak_search": peak, "carryover": theta}
            for wname, wr in windows.items():
                try: st = t0 + float(wr[0]); en = t0 + float(wr[1])
                except Exception: continue
                sel = merged[(merged["time_sec"] >= st) & (merged["time_sec"] < en)]
                row = {"condition": condition, "anchor_id": aid, "window_name": wname, "anchor_time_sec": t0, "window_start_sec": st, "window_end_sec": en, "n_bins": int(len(sel))}
                for col in ["luminance_z", "visual_change_z", "optical_flow_z", "audio_rms_z", "audio_derivative_z", "cut_event", "cue_on", "cue_impulse"]:
                    if col in sel.columns and len(sel):
                        row[f"{col}_mean"] = float(sel[col].mean())
                        row[f"{col}_std"] = float(sel[col].std())
                    else:
                        row[f"{col}_mean"] = np.nan; row[f"{col}_std"] = np.nan
                anchor_rows.append(row)
    if anchor_rows:
        pd.DataFrame(anchor_rows).to_csv(out_dir / f"anchor_stimulus_rhythm_vectors_{condition}.csv", index=False)

    branch_summary = {
        "condition": condition,
        "video_path": str(video_path),
        "sha256": sha256_file(video_path),
        "video_props": props,
        "visual_metrics": visual_metrics,
        "audio_metrics": audio_metrics,
        "cue_summary": cue_summary,
        "outputs": {
            "cet_regressors_csv": str(out_dir / f"cet_regressors_{condition}.csv"),
            "exogenous_regressor_frame_csv": str(out_dir / f"stimulus_exogenous_regressor_frame_{condition}.csv"),
            "visual_timeseries_csv": str(out_dir / f"stimulus_visual_timeseries_{condition}.csv"),
            "audio_timeseries_csv": str(out_dir / f"stimulus_audio_timeseries_{condition}.csv"),
            "cue_regressors_csv": str(out_dir / f"stimulus_cue_regressors_{condition}.csv"),
            "rhythm_summary_csv": str(out_dir / f"stimulus_rhythm_summary_{condition}.csv"),
            "dominant_frequency_timeseries_csv": str(out_dir / f"stimulus_dominant_frequency_timeseries_{condition}.csv"),
        },
        "boundary": "Stimulus fingerprint and exogenous regressor outputs only; not physiology, not meaning proof, not hidden-Y biology.",
    }
    (out_dir / f"stimulusfingerprint_manifest_{condition}.json").write_text(json.dumps(branch_summary, indent=2), encoding="utf-8")
    return branch_summary


def collect_branch_paths(args: argparse.Namespace) -> List[Tuple[str, Path]]:
    branches = []
    if args.video:
        branches.append((args.condition or "stimulus", Path(args.video)))
    for name in ["control", "target", "override"]:
        p = getattr(args, name)
        if p:
            branches.append((name, Path(p)))
    return branches


def main() -> int:
    ap = argparse.ArgumentParser(description="PRAYCG StimulusFingerprint/CET/EET v1.8")
    ap.add_argument("--video", default="", help="Single stimulus MP4")
    ap.add_argument("--condition", default="stimulus", help="Condition label for --video")
    ap.add_argument("--control", default="")
    ap.add_argument("--target", default="")
    ap.add_argument("--override", default="")
    ap.add_argument("--project-name", default="PRAYCG_Stimulus")
    ap.add_argument("--cue-schedule-json", default="")
    ap.add_argument("--anchor-json", default="")
    ap.add_argument("--out-root", default="stimulusfingerprint_outputs")
    ap.add_argument("--flat-output", action="store_true", help="Write directly inside out-root instead of dated subfolder")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--merge-hz", type=float, default=4.0, help="Output exogenous regressor grid Hz; 4 Hz = 0.25 s")
    ap.add_argument("--video-sample-hz", type=float, default=8.0)
    ap.add_argument("--resize-width", type=int, default=320)
    ap.add_argument("--freq-low", type=float, default=0.02)
    ap.add_argument("--freq-high", type=float, default=8.0)
    ap.add_argument("--stft-window-sec", type=float, default=32.0)
    ap.add_argument("--stft-step-sec", type=float, default=4.0)
    ap.add_argument("--fail-on-partial", action="store_true", help="Return nonzero if any requested branch fails. Default writes partial outputs and reports status.")
    args = ap.parse_args()

    branches = collect_branch_paths(args)
    if not branches:
        raise SystemExit("No video input supplied. Use --video or --control/--target/--override.")
    for cond, p in branches:
        if not p.exists():
            raise SystemExit(f"Missing {cond} video: {p}")

    cue_json = Path(args.cue_schedule_json) if args.cue_schedule_json else None
    anchor_json = Path(args.anchor_json) if args.anchor_json else None
    cue_events, cue_obj = load_cue_events(cue_json)
    anchors, anchor_obj = load_anchor_events(anchor_json)

    out_root = Path(args.out_root)
    out_dir = out_root if args.flat_output else out_root / f"{args.project_name}_StimulusFingerprint_CET_EET_v1_8_{now_iso().replace(':','').replace('-','')[:15]}"
    if out_dir.exists() and not args.overwrite:
        raise SystemExit(f"Output exists: {out_dir}. Use --overwrite or choose another out-root.")
    out_dir.mkdir(parents=True, exist_ok=True)

    branch_summaries = []
    branch_status_rows: List[Dict[str, Any]] = []
    error_log: List[Dict[str, Any]] = []
    for cond, p in branches:
        print(f"[v1.8] Processing {cond}: {p}", flush=True)
        try:
            summary = merge_branch(p, cond, out_dir, args, cue_events, cue_obj, anchors)
            summary["status"] = "PASS"
            branch_summaries.append(summary)
            branch_status_rows.append({
                "condition": cond, "video_path": str(p), "status": "PASS",
                "error": "", "exogenous_regressor_frame_csv": summary.get("outputs", {}).get("exogenous_regressor_frame_csv", ""),
                "cet_regressors_csv": summary.get("outputs", {}).get("cet_regressors_csv", ""),
                "rhythm_summary_csv": summary.get("outputs", {}).get("rhythm_summary_csv", ""),
            })
        except Exception as e:
            import traceback
            err = f"{type(e).__name__}: {e}"
            tb = traceback.format_exc()
            print(f"[v1.8] ERROR processing {cond}: {err}", flush=True)
            branch_summaries.append({
                "condition": cond, "video_path": str(p), "status": "FAIL", "error": err,
                "traceback_tail": tb.splitlines()[-12:],
                "boundary": "Branch failed during stimulus-side fingerprint extraction; no physiology or meaning inference should be made from this branch."
            })
            branch_status_rows.append({
                "condition": cond, "video_path": str(p), "status": "FAIL",
                "error": err, "exogenous_regressor_frame_csv": "", "cet_regressors_csv": "", "rhythm_summary_csv": "",
            })
            error_log.append({"condition": cond, "video_path": str(p), "error": err, "traceback": tb})
    safe_write_csv(out_dir / "stimulusfingerprint_branch_status.csv", branch_status_rows)
    (out_dir / "stimulusfingerprint_error_log.json").write_text(json.dumps(error_log, indent=2), encoding="utf-8")

    # Combined tables
    def concat_existing(pattern: str, out_name: str) -> None:
        dfs = []
        for p in sorted(out_dir.glob(pattern)):
            try:
                df = pd.read_csv(p)
                if not df.empty: dfs.append(df)
            except Exception:
                pass
        if dfs:
            pd.concat(dfs, ignore_index=True).to_csv(out_dir / out_name, index=False)
    concat_existing("cet_regressors_*.csv", "cet_regressors_all_conditions.csv")
    concat_existing("stimulus_exogenous_regressor_frame_*.csv", "stimulus_exogenous_regressor_frame_all_conditions.csv")
    concat_existing("stimulus_rhythm_summary_*.csv", "stimulus_rhythm_summary_all_conditions.csv")
    concat_existing("stimulus_dominant_frequency_timeseries_*.csv", "stimulus_dominant_frequency_timeseries_all_conditions.csv")
    concat_existing("anchor_stimulus_rhythm_vectors_*.csv", "anchor_stimulus_rhythm_vectors_all_conditions.csv")

    manifest = {
        "schema": SCHEMA,
        "version": VERSION,
        "created_utc": now_iso(),
        "project_name": args.project_name,
        "out_dir": str(out_dir),
        "cue_schedule_json": str(cue_json) if cue_json else None,
        "anchor_json": str(anchor_json) if anchor_json else None,
        "cue_count": len(cue_events),
        "anchor_count": len(anchors),
        "merge_hz": args.merge_hz,
        "video_sample_hz": args.video_sample_hz,
        "status": "PASS" if all(s.get("status") == "PASS" for s in branch_summaries) else ("PARTIAL_FAIL" if any(s.get("status") == "PASS" for s in branch_summaries) else "FAIL"),
        "branch_summaries": branch_summaries,
        "branch_status_csv": str(out_dir / "stimulusfingerprint_branch_status.csv"),
        "error_log_json": str(out_dir / "stimulusfingerprint_error_log.json"),
        "combined_outputs": {
            "cet_regressors_all_conditions": str(out_dir / "cet_regressors_all_conditions.csv"),
            "exogenous_regressor_frame_all_conditions": str(out_dir / "stimulus_exogenous_regressor_frame_all_conditions.csv"),
            "rhythm_summary_all_conditions": str(out_dir / "stimulus_rhythm_summary_all_conditions.csv"),
            "dominant_frequency_timeseries_all_conditions": str(out_dir / "stimulus_dominant_frequency_timeseries_all_conditions.csv"),
            "anchor_stimulus_rhythm_vectors_all_conditions": str(out_dir / "anchor_stimulus_rhythm_vectors_all_conditions.csv"),
        },
        "intended_downstream_use": ["CET", "CET-R", "EET", "NIP residualization", "TTI confound context", "visualizer exogenous overlays"],
        "boundary": "This is a stimulus-side exogenous-regressor package. It supports confound modeling. It does not certify meaning, immersion, OSM, or a biological mechanism.",
    }
    (out_dir / "stimulusfingerprint_cet_eet_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # README report
    lines = [
        f"# PRAYCG StimulusFingerprint/CET/EET v1.8 Report",
        "",
        f"Project: `{args.project_name}`",
        f"Created UTC: `{manifest['created_utc']}`",
        f"Status: `{manifest['status']}`",
        "",
        "## Outputs",
        "",
        "- `stimulus_exogenous_regressor_frame_all_conditions.csv` — merged visual/audio/cue/ALS regressors.",
        "- `cet_regressors_all_conditions.csv` — compact design matrix for CET/CET-R.",
        "- `stimulus_rhythm_summary_all_conditions.csv` — FFT/Welch dominant-frequency summary.",
        "- `stimulus_dominant_frequency_timeseries_all_conditions.csv` — STFT-like rolling dominant-frequency map.",
        "- `anchor_stimulus_rhythm_vectors_all_conditions.csv` — anchor-window vectors for EET, when anchor JSON is supplied.",
        "",
        "## Boundary",
        "",
        "These outputs belong to the stimulus/input side of the model: `u(t)`. They are not biological hidden-Y, not OSM, not proof of meaning, and not an EEG endpoint.",
        "",
        f"Overall status: `{manifest['status']}`",
        f"Branch errors: `{len(error_log)}`",
    ]
    (out_dir / "stimulusfingerprint_cet_eet_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[v1.8] DONE: {out_dir} status={manifest['status']}", flush=True)
    if args.fail_on_partial and manifest["status"] != "PASS":
        return 2
    return 0


def main_with_args(argv):
    """Programmatic entry point for wrappers/tests."""
    import sys as _sys
    old = _sys.argv
    try:
        _sys.argv = [old[0]] + list(argv)
        return main()
    finally:
        _sys.argv = old


if __name__ == "__main__":
    raise SystemExit(main())
