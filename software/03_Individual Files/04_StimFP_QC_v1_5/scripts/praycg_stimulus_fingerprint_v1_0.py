#!/usr/bin/env python3
"""
PRAYCG StimulusFingerprint v1.0

Analyze an MP4 stimulus for low-level visual and audio structure:
- visual luminance / contrast / motion / cut density / flash-risk proxies
- audio RMS / dBFS / dynamic range / envelope rhythm
- cue-visibility QC for PR-AYC-G number-cue schedules
- summary indices for stimulus categorization and exogenous entrainment risk

Important boundary:
This script does NOT measure true photons or true sound pressure level unless your display/audio chain
is externally calibrated. Pixel luminance is a digital visual-energy proxy. dBFS is digital full-scale
amplitude, not dB SPL at the ear.
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
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import cv2
from scipy import signal
from scipy.io import wavfile


EPS = 1e-12


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def clamp01(x: float) -> float:
    if not np.isfinite(x):
        return 0.0
    return float(max(0.0, min(1.0, x)))


def sigmoid(x: float) -> float:
    # numerically stable enough for this use
    x = max(-60.0, min(60.0, x))
    return 1.0 / (1.0 + math.exp(-x))


def band_power(freqs: np.ndarray, psd: np.ndarray, low: float, high: float) -> float:
    if freqs.size == 0:
        return 0.0
    mask = (freqs >= low) & (freqs < high)
    if not np.any(mask):
        return 0.0
    return float(np.trapz(psd[mask], freqs[mask]))


def safe_welch(x: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if x.size < 8 or fs <= 0:
        return np.array([]), np.array([])
    x = x - np.nanmean(x)
    nperseg = min(256, max(8, x.size))
    freqs, psd = signal.welch(x, fs=fs, nperseg=nperseg, detrend="constant")
    return freqs, psd


def load_cue_schedule(path: Optional[Path]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    if path is None:
        return [], {}
    with path.open("r", encoding="utf-8") as f:
        obj = json.load(f)
    events = obj.get("cue_events", [])
    return events, obj


def cue_roi_from_schedule_or_default(
    width: int,
    height: int,
    cue_position: str = "upper_right",
    roi_frac_w: float = 0.115,
    roi_frac_h: float = 0.095,
    margin_frac_x: float = 0.035,
    margin_frac_y: float = 0.055,
) -> Tuple[int, int, int, int]:
    """
    Default ROI approximates the upper-right badge zone.
    Returns x0, y0, x1, y1 in pixel coordinates.
    """
    rw = int(width * roi_frac_w)
    rh = int(height * roi_frac_h)
    mx = int(width * margin_frac_x)
    my = int(height * margin_frac_y)
    pos = (cue_position or "upper_right").lower()
    if pos == "upper_left":
        x0, y0 = mx, my
    elif pos == "lower_right":
        x0, y0 = width - mx - rw, height - my - rh
    elif pos == "lower_left":
        x0, y0 = mx, height - my - rh
    else:
        x0, y0 = width - mx - rw, my
    x0 = max(0, min(width - 1, x0))
    y0 = max(0, min(height - 1, y0))
    x1 = max(x0 + 1, min(width, x0 + rw))
    y1 = max(y0 + 1, min(height, y0 + rh))
    return x0, y0, x1, y1


def analyze_cue_visibility(
    video_path: Path,
    fps: float,
    width: int,
    height: int,
    cue_events: List[Dict[str, Any]],
    cue_position: str,
    visibility_threshold: float = 0.22,
    visibility_beta: float = 22.0,
) -> Dict[str, Any]:
    if not cue_events:
        return {
            "cue_visibility_available": False,
            "cue_count": 0,
            "expected_sum": None,
            "visibility_weighted_sum": None,
            "low_visibility_count": 0,
            "cue_visibility_events": [],
        }

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not reopen video for cue visibility: {video_path}")

    x0, y0, x1, y1 = cue_roi_from_schedule_or_default(width, height, cue_position)
    events_out: List[Dict[str, Any]] = []
    visible_sum = 0.0
    expected_sum = 0.0
    low_count = 0

    for ev in cue_events:
        try:
            start_sec = float(ev.get("start_sec"))
            end_sec = float(ev.get("end_sec", start_sec))
            value = float(ev.get("value"))
        except Exception:
            continue
        mid_sec = 0.5 * (start_sec + end_sec)
        frame_idx = int(round(mid_sec * fps))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, frame = cap.read()
        if not ok or frame is None:
            bg_lum = float("nan")
            contrast_white = 0.0
            visibility = 0.0
        else:
            crop = frame[y0:y1, x0:x1]
            # RGB luminance from BGR frame.
            b, g, r = cv2.split(crop.astype(np.float32))
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            bg_lum = float(np.mean(lum))
            # White-text contrast against local background. This approximates the
            # white-number problem. If a dark badge is present, bg_lum is low and contrast is high.
            contrast_white = float(abs(255.0 - bg_lum) / (255.0 + bg_lum + EPS))
            visibility = float(sigmoid(visibility_beta * (contrast_white - visibility_threshold)))
        expected_sum += value
        visible_sum += visibility * value
        low = contrast_white < visibility_threshold
        low_count += int(low)
        events_out.append({
            "cue_index": ev.get("cue_index"),
            "value": value,
            "start_sec": start_sec,
            "end_sec": end_sec,
            "mid_sec": mid_sec,
            "roi_x0": x0,
            "roi_y0": y0,
            "roi_x1": x1,
            "roi_y1": y1,
            "background_luminance_0_255": bg_lum,
            "white_text_contrast_proxy_0_1": contrast_white,
            "visibility_score_0_1": visibility,
            "visibility_pass": bool(not low),
        })
    cap.release()

    return {
        "cue_visibility_available": True,
        "cue_count": len(events_out),
        "expected_sum": expected_sum,
        "visibility_weighted_sum": visible_sum,
        "visibility_adjusted_error_if_reported": None,
        "mean_visibility_score_0_1": float(np.mean([e["visibility_score_0_1"] for e in events_out])) if events_out else 0.0,
        "min_visibility_score_0_1": float(np.min([e["visibility_score_0_1"] for e in events_out])) if events_out else 0.0,
        "low_visibility_count": low_count,
        "low_visibility_fraction": float(low_count / max(1, len(events_out))),
        "cue_roi": {"x0": x0, "y0": y0, "x1": x1, "y1": y1, "position": cue_position},
        "cue_visibility_events": events_out,
    }


def analyze_video(
    video_path: Path,
    sample_fps: float = 5.0,
    resize_width: int = 320,
    cue_schedule_json: Optional[Path] = None,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Optional[List[Dict[str, Any]]]]:
    cue_events, cue_obj = load_cue_schedule(cue_schedule_json)
    cue_position = (cue_obj.get("cue_design", {}) or {}).get("position", "upper_right")

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    duration = frame_count / fps if fps > 0 else 0.0
    step = max(1, int(round(fps / max(sample_fps, 0.1)))) if fps > 0 else 1
    effective_sample_fps = fps / step if fps > 0 else sample_fps

    rows: List[Dict[str, Any]] = []
    prev_gray_small = None
    prev_hist = None

    frame_idx = -1
    sampled = 0
    luminance_means = []
    luminance_stds = []
    saturation_means = []
    visual_changes = []
    hist_deltas = []
    edge_densities = []

    while True:
        ok, frame = cap.read()
        if not ok or frame is None:
            break
        frame_idx += 1
        if frame_idx % step != 0:
            continue

        h, w = frame.shape[:2]
        scale = resize_width / float(w) if w > resize_width else 1.0
        new_w = int(w * scale)
        new_h = int(h * scale)
        frame_small = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA) if scale != 1.0 else frame
        # OpenCV BGR -> luma
        b, g, r = cv2.split(frame_small.astype(np.float32))
        y = 0.2126 * r + 0.7152 * g + 0.0722 * b
        hsv = cv2.cvtColor(frame_small, cv2.COLOR_BGR2HSV)
        sat = hsv[:, :, 1].astype(float)

        lum_mean = float(np.mean(y))
        lum_std = float(np.std(y))
        sat_mean = float(np.mean(sat))
        edges = cv2.Canny(y.astype(np.uint8), 80, 160)
        edge_density = float(np.mean(edges > 0))

        if prev_gray_small is None:
            visual_change = 0.0
            hist_delta = 0.0
        else:
            visual_change = float(np.mean(np.abs(y - prev_gray_small)))
            hist = cv2.calcHist([y.astype(np.uint8)], [0], None, [32], [0, 256]).flatten()
            hist = hist / (np.sum(hist) + EPS)
            hist_delta = float(0.5 * np.sum(np.abs(hist - prev_hist))) if prev_hist is not None else 0.0
        hist = cv2.calcHist([y.astype(np.uint8)], [0], None, [32], [0, 256]).flatten()
        hist = hist / (np.sum(hist) + EPS)

        t = frame_idx / fps if fps > 0 else sampled / sample_fps
        row = {
            "time_sec": t,
            "frame_index": frame_idx,
            "luminance_mean_0_255": lum_mean,
            "luminance_std_0_255": lum_std,
            "saturation_mean_0_255": sat_mean,
            "visual_change_mean_abs_0_255": visual_change,
            "histogram_delta_0_1": hist_delta,
            "edge_density_0_1": edge_density,
        }
        rows.append(row)
        luminance_means.append(lum_mean)
        luminance_stds.append(lum_std)
        saturation_means.append(sat_mean)
        visual_changes.append(visual_change)
        hist_deltas.append(hist_delta)
        edge_densities.append(edge_density)
        prev_gray_small = y.copy()
        prev_hist = hist
        sampled += 1

    cap.release()

    lum = np.array(luminance_means, dtype=float)
    vchange = np.array(visual_changes, dtype=float)
    hdelta = np.array(hist_deltas, dtype=float)
    sat = np.array(saturation_means, dtype=float)

    # Cut heuristic using visual-change + histogram delta.
    if len(vchange) > 5:
        cut_score = 0.65 * (vchange / (np.nanmedian(vchange) + EPS)) + 0.35 * (hdelta / (np.nanmedian(hdelta) + EPS))
        threshold = max(float(np.nanpercentile(cut_score, 95)), float(np.nanmean(cut_score) + 2.5 * np.nanstd(cut_score)))
        cut_idx = np.where(cut_score > threshold)[0]
        # Enforce minimal separation.
        min_sep = max(1, int(round(0.25 * effective_sample_fps)))
        kept = []
        last = -10**9
        for idx in cut_idx:
            if idx - last >= min_sep:
                kept.append(int(idx))
                last = idx
        cuts = kept
    else:
        cuts = []
    cut_rate = len(cuts) / max(duration, EPS)

    # Flash risk: abrupt large luminance changes and high visual-change extremes.
    lum_diff = np.abs(np.diff(lum)) if len(lum) > 1 else np.array([])
    flash_events = int(np.sum((lum_diff > 25.0) | (vchange[1:] > 45.0))) if len(lum_diff) else 0
    flash_risk = float(flash_events / max(1, len(rows) - 1))

    freqs_lum, psd_lum = safe_welch(lum, effective_sample_fps)
    freqs_vf, psd_vf = safe_welch(vchange, effective_sample_fps)

    visual_metrics: Dict[str, Any] = {
        "duration_sec": duration,
        "fps": fps,
        "frame_count": frame_count,
        "width": width,
        "height": height,
        "sampled_frames": sampled,
        "sample_fps_effective": effective_sample_fps,
        "mean_luminance_0_255": float(np.nanmean(lum)) if len(lum) else 0.0,
        "std_luminance_over_time_0_255": float(np.nanstd(lum)) if len(lum) else 0.0,
        "mean_frame_contrast_luminance_std_0_255": float(np.nanmean(luminance_stds)) if len(luminance_stds) else 0.0,
        "mean_saturation_0_255": float(np.nanmean(sat)) if len(sat) else 0.0,
        "visual_change_mean_0_255": float(np.nanmean(vchange)) if len(vchange) else 0.0,
        "visual_change_std_0_255": float(np.nanstd(vchange)) if len(vchange) else 0.0,
        "histogram_delta_mean_0_1": float(np.nanmean(hdelta)) if len(hdelta) else 0.0,
        "edge_density_mean_0_1": float(np.nanmean(edge_densities)) if len(edge_densities) else 0.0,
        "cut_count_estimated": len(cuts),
        "cut_rate_per_sec": cut_rate,
        "cut_density_0_1": clamp01(cut_rate / 0.18),  # 0.18/s ~ 1 cut per 5.5 sec saturates
        "flash_event_count_estimated": flash_events,
        "flash_risk_0_1": clamp01(flash_risk),
        "luminance_envelope_power_0_1hz": band_power(freqs_lum, psd_lum, 0.0, 1.0),
        "luminance_envelope_power_1_4hz": band_power(freqs_lum, psd_lum, 1.0, 4.0),
        "luminance_envelope_power_4_8hz": band_power(freqs_lum, psd_lum, 4.0, 8.0),
        "visual_flux_power_4_8hz": band_power(freqs_vf, psd_vf, 4.0, 8.0),
        "cut_times_sec_estimated": [rows[i]["time_sec"] for i in cuts if 0 <= i < len(rows)],
    }

    cue_visibility = analyze_cue_visibility(
        video_path, fps=fps, width=width, height=height,
        cue_events=cue_events, cue_position=cue_position
    ) if cue_events else None

    return visual_metrics, rows, (cue_visibility["cue_visibility_events"] if cue_visibility else None), cue_visibility


def extract_audio_to_wav(video_path: Path, wav_path: Path) -> bool:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        return False
    cmd = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(video_path),
        "-vn", "-ac", "1", "-ar", "48000",
        str(wav_path)
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode == 0 and wav_path.exists() and wav_path.stat().st_size > 0


def analyze_audio(video_path: Path, out_dir: Path, hop_sec: float = 0.02, win_sec: float = 0.05) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    with tempfile.TemporaryDirectory() as td:
        wav_path = Path(td) / "audio.wav"
        ok = extract_audio_to_wav(video_path, wav_path)
        if not ok:
            metrics = {
                "has_audio": False,
                "reason": "ffmpeg unavailable or audio extraction failed",
                "audio_duration_sec": 0.0,
                "sample_rate_hz": 0,
                "rms_mean": 0.0,
                "rms_std": 0.0,
                "dbfs_mean": -120.0,
                "dbfs_peak": -120.0,
                "dynamic_range_db_p95_p5": 0.0,
                "silence_fraction": 1.0,
                "envelope_power_0_1hz": 0.0,
                "envelope_power_1_4hz": 0.0,
                "envelope_power_4_7hz": 0.0,
                "envelope_power_7_12hz": 0.0,
                "envelope_rhythm_concentration_0_1": 0.0,
                "crescendo_score_0_1": 0.0,
                "transient_rate_per_sec": 0.0,
            }
            return metrics, []

        sr, x = wavfile.read(str(wav_path))
        if x.ndim > 1:
            x = np.mean(x, axis=1)
        if np.issubdtype(x.dtype, np.integer):
            max_abs = np.iinfo(x.dtype).max
            x = x.astype(np.float32) / max_abs
        else:
            x = x.astype(np.float32)
            max_abs = max(float(np.max(np.abs(x))), 1.0)
            if max_abs > 2.0:
                x = x / max_abs
        duration = len(x) / float(sr)
        win = max(1, int(round(win_sec * sr)))
        hop = max(1, int(round(hop_sec * sr)))
        rows = []
        rms_vals = []
        for start in range(0, max(1, len(x) - win + 1), hop):
            seg = x[start:start+win]
            if len(seg) == 0:
                continue
            rms = float(np.sqrt(np.mean(seg.astype(float) ** 2)))
            dbfs = float(20.0 * np.log10(rms + EPS))
            t = (start + len(seg) / 2.0) / float(sr)
            rows.append({"time_sec": t, "audio_rms": rms, "audio_dbfs": dbfs})
            rms_vals.append(rms)
        rms = np.array(rms_vals, dtype=float)
        dbfs = 20.0 * np.log10(rms + EPS) if len(rms) else np.array([])
        env_fs = 1.0 / hop_sec if hop_sec > 0 else 50.0
        freqs, psd = safe_welch(rms, env_fs)

        if len(rms) > 5:
            dr = float(np.nanpercentile(dbfs, 95) - np.nanpercentile(dbfs, 5))
            silence_fraction = float(np.mean(dbfs < -55.0))
            # Transient/onset proxy: positive envelope derivative spikes.
            deriv = np.diff(rms, prepend=rms[0])
            th = np.nanmean(deriv) + 2.5 * np.nanstd(deriv)
            transient_count = int(np.sum(deriv > th))
            transient_rate = transient_count / max(duration, EPS)
            # Crescendo: slope of envelope in last third compared with whole; sigmoid-scaled
            thirds = np.array_split(rms, 3)
            crescendo = 0.0
            if len(thirds) == 3 and len(thirds[0]) and len(thirds[-1]):
                crescendo_raw = float(np.nanmean(thirds[-1]) - np.nanmean(thirds[0]))
                crescendo = clamp01((crescendo_raw + 0.02) / 0.08)
        else:
            dr, silence_fraction, transient_rate, crescendo = 0.0, 1.0, 0.0, 0.0

        low = band_power(freqs, psd, 0.0, 1.0)
        p1_4 = band_power(freqs, psd, 1.0, 4.0)
        p4_7 = band_power(freqs, psd, 4.0, 7.0)
        p7_12 = band_power(freqs, psd, 7.0, 12.0)
        total_env = band_power(freqs, psd, 0.0, min(12.0, env_fs/2.0))
        rhythm_concentration = float((p4_7 + p7_12) / (total_env + EPS)) if total_env > 0 else 0.0

        metrics = {
            "has_audio": True,
            "audio_duration_sec": duration,
            "sample_rate_hz": int(sr),
            "rms_mean": float(np.nanmean(rms)) if len(rms) else 0.0,
            "rms_std": float(np.nanstd(rms)) if len(rms) else 0.0,
            "dbfs_mean": float(np.nanmean(dbfs)) if len(dbfs) else -120.0,
            "dbfs_peak": float(np.nanmax(dbfs)) if len(dbfs) else -120.0,
            "dynamic_range_db_p95_p5": dr,
            "silence_fraction": silence_fraction,
            "envelope_power_0_1hz": low,
            "envelope_power_1_4hz": p1_4,
            "envelope_power_4_7hz": p4_7,
            "envelope_power_7_12hz": p7_12,
            "envelope_rhythm_concentration_0_1": clamp01(rhythm_concentration),
            "crescendo_score_0_1": crescendo,
            "transient_rate_per_sec": float(transient_rate),
        }
        return metrics, rows


def make_summary_indices(visual: Dict[str, Any], audio: Dict[str, Any], cue_visibility: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    # Visual normalized proxies
    lum_dyn = clamp01(visual.get("std_luminance_over_time_0_255", 0.0) / 64.0)
    frame_contrast = clamp01(visual.get("mean_frame_contrast_luminance_std_0_255", 0.0) / 80.0)
    visual_flux = clamp01(visual.get("visual_change_mean_0_255", 0.0) / 35.0)
    cut_density = clamp01(visual.get("cut_density_0_1", 0.0))
    flash = clamp01(visual.get("flash_risk_0_1", 0.0) * 5.0)
    sat = clamp01(visual.get("mean_saturation_0_255", 0.0) / 160.0)
    lum_4_8 = visual.get("luminance_envelope_power_4_8hz", 0.0)
    vflux_4_8 = visual.get("visual_flux_power_4_8hz", 0.0)
    # Normalize PSD powers crudely relative to typical digital luminance variance scale.
    visual_4_8_norm = clamp01((lum_4_8 + vflux_4_8) / 120.0)

    if audio.get("has_audio", False):
        # dBFS: -60 quiet, -12 strong
        audio_level = clamp01((audio.get("dbfs_mean", -120.0) + 60.0) / 48.0)
        audio_dyn = clamp01(audio.get("dynamic_range_db_p95_p5", 0.0) / 35.0)
        audio_rhythm = clamp01(audio.get("envelope_rhythm_concentration_0_1", 0.0) * 2.0)
        audio_crescendo = clamp01(audio.get("crescendo_score_0_1", 0.0))
        audio_transients = clamp01(audio.get("transient_rate_per_sec", 0.0) / 4.0)
        silence = clamp01(audio.get("silence_fraction", 1.0))
    else:
        audio_level = audio_dyn = audio_rhythm = audio_crescendo = audio_transients = 0.0
        silence = 1.0

    visual_energy = clamp01(0.25*lum_dyn + 0.25*frame_contrast + 0.25*visual_flux + 0.15*cut_density + 0.10*sat)
    audio_energy = clamp01(0.35*audio_level + 0.25*audio_dyn + 0.20*audio_rhythm + 0.10*audio_crescendo + 0.10*audio_transients)
    sensory_energy = clamp01(0.55*visual_energy + 0.45*audio_energy)

    exogenous_risk = clamp01(
        0.25*cut_density + 0.25*visual_4_8_norm + 0.20*audio_rhythm + 0.15*audio_transients + 0.15*flash
    )
    overload = clamp01(0.35*flash + 0.25*audio_level + 0.20*visual_flux + 0.20*audio_transients)

    cue_failure = None
    if cue_visibility and cue_visibility.get("cue_visibility_available"):
        cue_failure = cue_visibility.get("low_visibility_fraction", 0.0)

    # Mechanically inferred category only. Meaning is not estimated here.
    if sensory_energy < 0.20:
        sensory_class = "low sensory load"
    elif sensory_energy < 0.45:
        sensory_class = "moderate sensory load"
    else:
        sensory_class = "high sensory load"

    if exogenous_risk < 0.20:
        entrain_class = "low exogenous entrainment risk"
    elif exogenous_risk < 0.45:
        entrain_class = "moderate exogenous entrainment risk"
    else:
        entrain_class = "high exogenous entrainment risk"

    return {
        "visual_energy_proxy_0_1": visual_energy,
        "audio_energy_proxy_0_1": audio_energy,
        "sensory_energy_proxy_0_100": round(100.0 * sensory_energy, 3),
        "exogenous_entrainment_risk_0_1": exogenous_risk,
        "overload_risk_0_1": overload,
        "visual_4_8hz_entrainment_proxy_0_1": visual_4_8_norm,
        "audio_envelope_rhythm_proxy_0_1": audio_rhythm,
        "cue_visibility_failure_fraction": cue_failure,
        "sensory_class": sensory_class,
        "entrainment_risk_class": entrain_class,
        "interpretive_boundary": (
            "These are digital stimulus-delivery proxies. They do not measure meaning, "
            "true photons at the retina, or true dB SPL at the ear without external calibration."
        ),
    }


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = list(rows[0].keys())
    # Include any later keys.
    for r in rows:
        for k in r.keys():
            if k not in keys:
                keys.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def make_plots(out_dir: Path, video_rows: List[Dict[str, Any]], audio_rows: List[Dict[str, Any]], cue_rows: Optional[List[Dict[str, Any]]]) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(exist_ok=True)

    if video_rows:
        t = np.array([r["time_sec"] for r in video_rows], dtype=float)
        lum = np.array([r["luminance_mean_0_255"] for r in video_rows], dtype=float)
        chg = np.array([r["visual_change_mean_abs_0_255"] for r in video_rows], dtype=float)
        plt.figure(figsize=(10, 4))
        plt.plot(t, lum, label="Mean luminance")
        plt.xlabel("Time (s)")
        plt.ylabel("Digital luminance (0-255)")
        plt.title("Visual luminance timeline")
        plt.tight_layout()
        plt.savefig(fig_dir / "visual_luminance_timeline.png", dpi=160)
        plt.close()

        plt.figure(figsize=(10, 4))
        plt.plot(t, chg, label="Frame-to-frame visual change")
        plt.xlabel("Time (s)")
        plt.ylabel("Mean absolute change")
        plt.title("Visual change / motion-cut proxy")
        plt.tight_layout()
        plt.savefig(fig_dir / "visual_change_timeline.png", dpi=160)
        plt.close()

    if audio_rows:
        t = np.array([r["time_sec"] for r in audio_rows], dtype=float)
        db = np.array([r["audio_dbfs"] for r in audio_rows], dtype=float)
        plt.figure(figsize=(10, 4))
        plt.plot(t, db)
        plt.xlabel("Time (s)")
        plt.ylabel("dBFS")
        plt.title("Audio envelope timeline")
        plt.tight_layout()
        plt.savefig(fig_dir / "audio_dbfs_timeline.png", dpi=160)
        plt.close()

    if cue_rows:
        idx = np.array([r.get("cue_index", i+1) for i, r in enumerate(cue_rows)])
        vis = np.array([r.get("visibility_score_0_1", 0) for r in cue_rows], dtype=float)
        con = np.array([r.get("white_text_contrast_proxy_0_1", 0) for r in cue_rows], dtype=float)
        plt.figure(figsize=(10, 4))
        plt.plot(idx, vis, marker="o", linewidth=1)
        plt.xlabel("Cue index")
        plt.ylabel("Visibility score")
        plt.title("Number-cue visibility QC")
        plt.tight_layout()
        plt.savefig(fig_dir / "cue_visibility_scores.png", dpi=160)
        plt.close()


def analyze_file(args: argparse.Namespace) -> None:
    video_path = Path(args.input).resolve()
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    cue_schedule = Path(args.cue_schedule_json).resolve() if args.cue_schedule_json else None

    visual, video_rows, cue_rows, cue_visibility = analyze_video(
        video_path,
        sample_fps=args.sample_fps,
        resize_width=args.resize_width,
        cue_schedule_json=cue_schedule,
    )
    audio, audio_rows = analyze_audio(video_path, out_dir)
    summary = make_summary_indices(visual, audio, cue_visibility)

    result = {
        "schema": "PRAYCG_stimulus_fingerprint_v1_0",
        "input_file": str(video_path),
        "input_sha256": sha256_file(video_path),
        "cue_schedule_json": str(cue_schedule) if cue_schedule else None,
        "visual": visual,
        "audio": audio,
        "cue_visibility": cue_visibility,
        "summary": summary,
    }

    (out_dir / "stimulus_fingerprint_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_csv(out_dir / "stimulus_visual_timeseries.csv", video_rows)
    write_csv(out_dir / "stimulus_audio_timeseries.csv", audio_rows)
    if cue_rows:
        write_csv(out_dir / "cue_visibility_qc.csv", cue_rows)

    # Short markdown report
    md = [
        "# PRAYCG StimulusFingerprint v1.0 Report",
        "",
        f"Input: `{video_path.name}`",
        f"SHA-256: `{result['input_sha256']}`",
        "",
        "## Boundary",
        "This script reports digital stimulus-delivery proxies. It does not measure true photons at the retina or true dB SPL at the ear without external calibration.",
        "",
        "## Summary indices",
        f"- Sensory energy proxy: {summary['sensory_energy_proxy_0_100']}/100",
        f"- Visual energy proxy: {summary['visual_energy_proxy_0_1']:.3f}",
        f"- Audio energy proxy: {summary['audio_energy_proxy_0_1']:.3f}",
        f"- Exogenous entrainment risk: {summary['exogenous_entrainment_risk_0_1']:.3f} ({summary['entrainment_risk_class']})",
        f"- Overload risk: {summary['overload_risk_0_1']:.3f}",
        "",
        "## Video",
        f"- Duration: {visual['duration_sec']:.3f} s",
        f"- FPS: {visual['fps']:.3f}",
        f"- Resolution: {visual['width']} x {visual['height']}",
        f"- Mean luminance: {visual['mean_luminance_0_255']:.3f}",
        f"- Temporal luminance SD: {visual['std_luminance_over_time_0_255']:.3f}",
        f"- Visual change mean: {visual['visual_change_mean_0_255']:.3f}",
        f"- Estimated cut count: {visual['cut_count_estimated']}",
        f"- Estimated cut rate: {visual['cut_rate_per_sec']:.4f}/s",
        f"- Flash risk proxy: {visual['flash_risk_0_1']:.3f}",
        "",
        "## Audio",
        f"- Has audio: {audio.get('has_audio')}",
        f"- Mean dBFS: {audio.get('dbfs_mean', -120):.3f}",
        f"- Peak dBFS: {audio.get('dbfs_peak', -120):.3f}",
        f"- Dynamic range p95-p5: {audio.get('dynamic_range_db_p95_p5', 0):.3f} dB",
        f"- Silence fraction: {audio.get('silence_fraction', 1):.3f}",
        f"- Envelope rhythm concentration: {audio.get('envelope_rhythm_concentration_0_1', 0):.3f}",
        "",
    ]
    if cue_visibility and cue_visibility.get("cue_visibility_available"):
        md += [
            "## Cue visibility QC",
            f"- Cue count: {cue_visibility.get('cue_count')}",
            f"- Expected sum: {cue_visibility.get('expected_sum')}",
            f"- Visibility-weighted sum: {cue_visibility.get('visibility_weighted_sum'):.3f}",
            f"- Mean visibility score: {cue_visibility.get('mean_visibility_score_0_1'):.3f}",
            f"- Low-visibility count: {cue_visibility.get('low_visibility_count')} ({cue_visibility.get('low_visibility_fraction'):.3f})",
            "",
            "Low cue visibility means the number was physically present in the file but may not have been functionally decodable by the viewer.",
            "",
        ]
    (out_dir / "stimulus_fingerprint_report.md").write_text("\n".join(md), encoding="utf-8")

    if args.make_plots:
        make_plots(out_dir, video_rows, audio_rows, cue_rows)


def main() -> None:
    p = argparse.ArgumentParser(description="Analyze MP4 physical stimulus proxies for PR-AYC-G.")
    p.add_argument("input", help="Input MP4 file.")
    p.add_argument("--out", required=True, help="Output folder.")
    p.add_argument("--sample-fps", type=float, default=5.0, help="Video analysis sample rate. Default: 5 fps.")
    p.add_argument("--resize-width", type=int, default=320, help="Downsample width for frame metrics. Default: 320.")
    p.add_argument("--cue-schedule-json", default=None, help="Optional PRAYCG number-cue schedule JSON for cue-visibility QC.")
    p.add_argument("--make-plots", action="store_true", help="Create PNG plots.")
    args = p.parse_args()
    analyze_file(args)


if __name__ == "__main__":
    main()
