#!/usr/bin/env python3
"""
PRAYCG MediaPrep GUI v1.6S - ALS-PT19 Fullscreen Start-Pulse Patch

One-master-MP4 media preparation pipeline for PR-AYC-G.

Given one master .mp4, this tool creates:
  1. optional cleaned master MP4 with source/watermark mask applied globally
  2. cue-embedded Target MP4
  3. bit-identical cue-embedded Contextual Override MP4
  4. phase-scrambled Control MP4 generated from the cue-embedded Target
  5. cue schedule JSON/CSV with expected running-sum answer
  6. media-prep manifest, report, and QC checklists

v1.6S patch focus:
  - Keeps v1.6P/Q visual source-stamp, control-audio, and GUI hardening logic.
  - Adds an optional ALS-PT19 / photodiode-style physical timing marker to all
    branch videos for display-onset validation.
  - New default timing mode is fullscreen_start_flash: a full-screen white
    flash followed by a short black guard before the original content begins.
    This is more robust than a small corner square because exact sensor placement
    is no longer required.
  - The added prefix is excluded from physiology interpretation and the cue
    schedule is shifted so protocol markers match the final rendered videos.

This is a preparation tool, not an experimental runner or analysis tool.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
import threading
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

try:
    import cv2
except Exception as exc:  # pragma: no cover
    raise RuntimeError("opencv-python is required. Install with: pip install opencv-python") from exc

try:
    from scipy import signal
    from scipy.io import wavfile
except Exception as exc:  # pragma: no cover
    raise RuntimeError("scipy is required. Install with: pip install scipy") from exc

try:
    from moviepy import VideoFileClip  # MoviePy 2.x
except Exception:  # pragma: no cover
    try:
        from moviepy.editor import VideoFileClip  # MoviePy 1.x
    except Exception as exc:
        raise RuntimeError("moviepy is required. Install with: pip install moviepy") from exc

SCHEMA = "PRAYCG_media_prep_suite_v1_6S_als_pt19_timing_pulse"
CUE_SCHEMA = "PRAYCG_number_cue_schedule_v1_6S"
DEFAULT_SEED = 20260724


@dataclass
class CueEvent:
    cue_index: int
    value: int
    start_sec: float
    end_sec: float
    duration_sec: float
    interval_sec: float
    position: str
    badge_x1: int = 0
    badge_y1: int = 0
    badge_x2: int = 0
    badge_y2: int = 0
    pre_badge_background_luminance: Optional[float] = None
    contrast_pre_badge_0_1: Optional[float] = None
    contrast_protected_badge: bool = True


@dataclass
class SensorPulseEvent:
    pulse_index: int
    pulse_type: str
    start_sec: float
    end_sec: float
    duration_sec: float
    position: str
    square_x1: int = 0
    square_y1: int = 0
    square_x2: int = 0
    square_y2: int = 0
    idle_level_0_255: int = 0
    pulse_level_0_255: int = 255


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def now_utc_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def sanitize_name(name: str) -> str:
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    out = "".join(c if c in allowed else "_" for c in name.strip())
    while "__" in out:
        out = out.replace("__", "_")
    return out.strip("_") or "PRAYCG_Stimulus"


def ffmpeg_exists() -> bool:
    return shutil.which("ffmpeg") is not None


def run_subprocess(cmd: List[str], *, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")


def get_video_props(path: Path) -> Dict[str, Any]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {path}")
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    duration = frame_count / fps if fps > 0 else 0.0
    cap.release()
    return {"fps": fps, "frame_count": frame_count, "width": width, "height": height, "duration_sec": duration}


def has_audio(input_mp4: Path) -> bool:
    try:
        clip = VideoFileClip(str(input_mp4))
        try:
            return clip.audio is not None
        finally:
            clip.close()
    except Exception:
        return False


def load_audio_array(input_mp4: Path, audio_fps: int = 44100) -> Optional[Tuple[np.ndarray, int]]:
    if not has_audio(input_mp4):
        return None
    clip = VideoFileClip(str(input_mp4))
    try:
        if clip.audio is None:
            return None
        arr = clip.audio.to_soundarray(fps=audio_fps)
    finally:
        try:
            clip.close()
        except Exception:
            pass
    arr = np.asarray(arr, dtype=np.float32)
    if arr.ndim == 1:
        arr = arr[:, None]
    # Keep finite values only.
    arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
    return arr, int(audio_fps)


def mux_original_audio(source_mp4: Path, video_no_audio_mp4: Path, output_mp4: Path, fps: float) -> None:
    """Attach original audio to a rendered no-audio video. Prefer ffmpeg; fallback to MoviePy."""
    if ffmpeg_exists():
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_no_audio_mp4),
            "-i", str(source_mp4),
            "-map", "0:v:0",
            "-map", "1:a?",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            str(output_mp4),
        ]
        subprocess.run(cmd, check=True)
        return

    src_clip = VideoFileClip(str(source_mp4))
    vid_clip = VideoFileClip(str(video_no_audio_mp4))
    try:
        if src_clip.audio is not None:
            out_clip = vid_clip.with_audio(src_clip.audio) if hasattr(vid_clip, "with_audio") else vid_clip.set_audio(src_clip.audio)
        else:
            out_clip = vid_clip
        out_clip.write_videofile(str(output_mp4), codec="libx264", audio_codec="aac", fps=fps)
    finally:
        for c in (src_clip, vid_clip):
            try: c.close()
            except Exception: pass




def mux_delayed_original_audio(source_mp4: Path, video_no_audio_mp4: Path, output_mp4: Path, delay_sec: float, fps: float) -> None:
    """Attach source audio to a video that has a visual prefix.

    The original audio must begin when original content begins, not during the
    ALS white/black timing prefix. This function inserts silence for delay_sec
    before the original audio.
    """
    delay_sec = max(0.0, float(delay_sec))
    if not has_audio(source_mp4):
        shutil.copy2(video_no_audio_mp4, output_mp4)
        return
    if ffmpeg_exists():
        delay_ms = int(round(delay_sec * 1000.0))
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_no_audio_mp4),
            "-i", str(source_mp4),
            "-filter_complex", f"[1:a]adelay={delay_ms}:all=1,apad[a]",
            "-map", "0:v:0",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            str(output_mp4),
        ]
        subprocess.run(cmd, check=True)
        return

    # MoviePy fallback. It is slower but avoids losing audio if ffmpeg is not in PATH.
    src_clip = VideoFileClip(str(source_mp4))
    vid_clip = VideoFileClip(str(video_no_audio_mp4))
    try:
        if src_clip.audio is not None:
            if hasattr(src_clip.audio, "with_start"):
                delayed_audio = src_clip.audio.with_start(delay_sec)
            else:
                delayed_audio = src_clip.audio.set_start(delay_sec)
            out_clip = vid_clip.with_audio(delayed_audio) if hasattr(vid_clip, "with_audio") else vid_clip.set_audio(delayed_audio)
        else:
            out_clip = vid_clip
        out_clip.write_videofile(str(output_mp4), codec="libx264", audio_codec="aac", fps=fps)
    finally:
        for c in (src_clip, vid_clip):
            try: c.close()
            except Exception: pass


def mux_wav_audio(video_no_audio_mp4: Path, wav_path: Path, output_mp4: Path) -> None:
    if ffmpeg_exists():
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_no_audio_mp4),
            "-i", str(wav_path),
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            str(output_mp4),
        ]
        subprocess.run(cmd, check=True)
        return

    try:
        from moviepy import AudioFileClip
    except Exception:
        from moviepy.editor import AudioFileClip
    vid_clip = VideoFileClip(str(video_no_audio_mp4))
    aud_clip = AudioFileClip(str(wav_path))
    try:
        out_clip = vid_clip.with_audio(aud_clip) if hasattr(vid_clip, "with_audio") else vid_clip.set_audio(aud_clip)
        out_clip.write_videofile(str(output_mp4), codec="libx264", audio_codec="aac", fps=vid_clip.fps)
    finally:
        for c in (vid_clip, aud_clip):
            try: c.close()
            except Exception: pass


def luminance_mean_bgr(region: np.ndarray) -> float:
    if region.size == 0:
        return float("nan")
    b = region[:, :, 0].astype(np.float32)
    g = region[:, :, 1].astype(np.float32)
    r = region[:, :, 2].astype(np.float32)
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return float(np.nanmean(y))


def contrast_0_1(text_luma: float, bg_luma: float) -> float:
    return float(abs(text_luma - bg_luma) / (text_luma + bg_luma + 1e-6))


def compute_mask_bbox(frame_shape: Tuple[int, int, int], preset: str, x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int, int, int]:
    h, w = frame_shape[:2]
    p = (preset or "upper_left").lower().strip()
    # If custom coords supplied with positive x2/y2, use those.
    if p == "custom" and x2 > x1 and y2 > y1:
        return max(0, x1), max(0, y1), min(w, x2), min(h, y2)
    # Conservative logo/stamp regions. User can enlarge if needed.
    bw = max(180, int(round(w * 0.18)))
    bh = max(80, int(round(h * 0.12)))
    margin = max(0, int(round(w * 0.005)))
    if p == "upper_right":
        return max(0, w - bw - margin), margin, min(w, w - margin), min(h, bh + margin)
    if p == "lower_left":
        return margin, max(0, h - bh - margin), min(w, bw + margin), min(h, h - margin)
    if p == "lower_right":
        return max(0, w - bw - margin), max(0, h - bh - margin), min(w, w - margin), min(h, h - margin)
    # default upper_left
    return margin, margin, min(w, bw + margin), min(h, bh + margin)


def apply_visual_mask_to_frame(frame: np.ndarray, bbox: Tuple[int, int, int, int], method: str, fill_rgb: Tuple[int, int, int]) -> np.ndarray:
    x1, y1, x2, y2 = bbox
    out = frame.copy()
    if x2 <= x1 or y2 <= y1:
        return out
    roi = out[y1:y2, x1:x2]
    method = (method or "blur").lower().strip()
    if method == "solid":
        # fill_rgb is RGB; frame is BGR
        r, g, b = fill_rgb
        out[y1:y2, x1:x2] = np.array([b, g, r], dtype=np.uint8)
    elif method == "median_patch":
        # Use border around ROI to estimate local color.
        h, w = out.shape[:2]
        pad = max(10, int(round(max(x2-x1, y2-y1) * 0.15)))
        bx1, by1 = max(0, x1-pad), max(0, y1-pad)
        bx2, by2 = min(w, x2+pad), min(h, y2+pad)
        border = out[by1:by2, bx1:bx2].reshape(-1, 3)
        med = np.median(border, axis=0).astype(np.uint8) if border.size else np.array([0,0,0], dtype=np.uint8)
        out[y1:y2, x1:x2] = med
    elif method == "inpaint":
        mask = np.zeros(out.shape[:2], dtype=np.uint8)
        mask[y1:y2, x1:x2] = 255
        try:
            out = cv2.inpaint(out, mask, 3, cv2.INPAINT_TELEA)
        except Exception:
            # fallback to blur
            k = max(31, (max(x2-x1, y2-y1)//2)|1)
            out[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (k, k), 0)
    else:  # blur
        k = max(31, (max(x2-x1, y2-y1)//2)|1)
        out[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (k, k), 0)
    return out


def render_cleaned_master(
    master_mp4: Path,
    output_cleaned_mp4: Path,
    mask_preset: str,
    mask_method: str,
    mask_x1: int,
    mask_y1: int,
    mask_x2: int,
    mask_y2: int,
    mask_fill_rgb: Tuple[int, int, int],
    overwrite: bool,
    progress_cb=None,
    max_seconds: Optional[float] = None,
) -> Dict[str, Any]:
    if output_cleaned_mp4.exists() and not overwrite:
        raise FileExistsError(f"Output exists: {output_cleaned_mp4}")
    props = get_video_props(master_mp4)
    fps, width, height, frame_count = props["fps"], props["width"], props["height"], props["frame_count"]
    frame_limit = min(frame_count, int(round(max_seconds * fps))) if max_seconds else frame_count
    cap = cv2.VideoCapture(str(master_mp4))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open {master_mp4}")
    tmp_dir = Path(tempfile.mkdtemp(prefix="praycg_v16Q_clean_"))
    tmp_video = tmp_dir / "cleaned_no_audio.mp4"
    writer = cv2.VideoWriter(str(tmp_video), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Could not open cv2 VideoWriter for cleaned master")
    bbox_final = None
    processed = 0
    try:
        for frame_idx in range(frame_limit):
            ok, frame = cap.read()
            if not ok:
                break
            bbox = compute_mask_bbox(frame.shape, mask_preset, mask_x1, mask_y1, mask_x2, mask_y2)
            bbox_final = bbox
            frame = apply_visual_mask_to_frame(frame, bbox, mask_method, mask_fill_rgb)
            writer.write(frame)
            processed += 1
            if progress_cb and (frame_idx % max(1, int(fps * 2)) == 0):
                progress_cb(f"Visual cleanup: frame {frame_idx+1}/{frame_limit}")
    finally:
        writer.release()
        cap.release()
    if progress_cb:
        progress_cb("Muxing original audio into cleaned master video...")
    mux_original_audio(master_mp4, tmp_video, output_cleaned_mp4, fps=fps)
    try: shutil.rmtree(tmp_dir)
    except Exception: pass
    return {**props, "rendered_frames": processed, "rendered_duration_sec": processed / fps if fps else None, "mask_bbox": bbox_final, "mask_method": mask_method, "mask_preset": mask_preset}


def make_cue_schedule(duration_sec: float, seed: int, interval_sec: float, display_duration_sec: float, start_delay_sec: float, min_value: int, max_value: int, position: str) -> List[CueEvent]:
    if interval_sec <= 0:
        raise ValueError("interval_sec must be > 0")
    if display_duration_sec <= 0:
        raise ValueError("display_duration_sec must be > 0")
    if display_duration_sec > interval_sec:
        raise ValueError("display_duration_sec should not exceed interval_sec")
    if min_value > max_value:
        raise ValueError("min_value cannot exceed max_value")
    rng = random.Random(int(seed))
    events: List[CueEvent] = []
    t = float(start_delay_sec)
    idx = 1
    while t + display_duration_sec <= duration_sec - 0.05:
        val = rng.randint(int(min_value), int(max_value))
        events.append(CueEvent(idx, val, round(t, 6), round(t + display_duration_sec, 6), float(display_duration_sec), float(interval_sec), position))
        idx += 1
        t += float(interval_sec)
    return events


def find_active_cue(t_sec: float, events: List[CueEvent]) -> Optional[CueEvent]:
    for ev in events:
        if ev.start_sec <= t_sec < ev.end_sec:
            return ev
    return None


def badge_geometry(frame_shape: Tuple[int, int, int], text: str, position: str, font_scale_factor: float) -> Tuple[int, int, int, int, float, int]:
    h, w = frame_shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = max(0.8, min(2.2, (h / 1080.0) * float(font_scale_factor)))
    thickness = max(2, int(round(h / 420)))
    (tw, th), baseline = cv2.getTextSize(str(text), font, font_scale, thickness)
    pad_x = max(16, int(round(w * 0.014)))
    pad_y = max(12, int(round(h * 0.014)))
    badge_w = tw + 2 * pad_x
    badge_h = th + baseline + 2 * pad_y
    margin_x = max(28, int(round(w * 0.035)))
    margin_y = max(28, int(round(h * 0.045)))
    pos = position.lower().strip()
    if pos == "upper_right":
        x2 = w - margin_x; x1 = x2 - badge_w; y1 = margin_y; y2 = y1 + badge_h
    elif pos == "upper_left":
        x1 = margin_x; x2 = x1 + badge_w; y1 = margin_y; y2 = y1 + badge_h
    elif pos == "lower_right":
        x2 = w - margin_x; x1 = x2 - badge_w; y2 = h - margin_y; y1 = y2 - badge_h
    elif pos == "lower_left":
        x1 = margin_x; x2 = x1 + badge_w; y2 = h - margin_y; y1 = y2 - badge_h
    else:
        raise ValueError(f"Unsupported cue position: {position}")
    return int(max(0, x1)), int(max(0, y1)), int(min(w, x2)), int(min(h, y2)), float(font_scale), int(thickness)


def draw_number_badge(frame_bgr: np.ndarray, number: int, position: str, alpha: float, font_scale_factor: float) -> Tuple[np.ndarray, Tuple[int, int, int, int], float, float]:
    out = frame_bgr.copy()
    text = str(number)
    x1, y1, x2, y2, font_scale, thickness = badge_geometry(out.shape, text, position, font_scale_factor)
    roi = out[y1:y2, x1:x2]
    bg_luma = luminance_mean_bgr(roi)
    pre_contrast = contrast_0_1(255.0, bg_luma)
    overlay = out.copy()
    # Dark contrast-protected badge.
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (12, 12, 12), -1)
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (220, 220, 220), max(1, thickness // 2))
    out = cv2.addWeighted(overlay, float(alpha), out, 1.0 - float(alpha), 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw, th), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    tx = x1 + (x2 - x1 - tw) // 2
    ty = y1 + (y2 - y1 + th) // 2 - baseline // 2
    # Black outline + white number.
    cv2.putText(out, text, (tx, ty), font, font_scale, (0, 0, 0), thickness + 3, cv2.LINE_AA)
    cv2.putText(out, text, (tx, ty), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
    return out, (x1, y1, x2, y2), bg_luma, pre_contrast


def render_cued_video(master_mp4: Path, output_cued_mp4: Path, events: List[CueEvent], position: str, badge_alpha: float, font_scale_factor: float, overwrite: bool, progress_cb=None, max_seconds: Optional[float] = None) -> Dict[str, Any]:
    if output_cued_mp4.exists() and not overwrite:
        raise FileExistsError(f"Output exists: {output_cued_mp4}")
    props = get_video_props(master_mp4)
    fps, width, height, frame_count = props["fps"], props["width"], props["height"], props["frame_count"]
    frame_limit = min(frame_count, int(round(max_seconds * fps))) if max_seconds else frame_count
    cap = cv2.VideoCapture(str(master_mp4))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open {master_mp4}")
    tmp_dir = Path(tempfile.mkdtemp(prefix="praycg_v16S_cued_"))
    tmp_video = tmp_dir / "cued_no_audio.mp4"
    writer = cv2.VideoWriter(str(tmp_video), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Could not open cv2 VideoWriter for cued video")
    cue_first_frame_seen: Dict[int, bool] = {}
    processed = 0
    try:
        for frame_idx in range(frame_limit):
            ok, frame = cap.read()
            if not ok:
                break
            t = frame_idx / fps
            ev = find_active_cue(t, events)
            if ev is not None:
                frame, bbox, bg_luma, pre_contrast = draw_number_badge(frame, ev.value, position=position, alpha=badge_alpha, font_scale_factor=font_scale_factor)
                if ev.cue_index not in cue_first_frame_seen:
                    ev.badge_x1, ev.badge_y1, ev.badge_x2, ev.badge_y2 = bbox
                    ev.pre_badge_background_luminance = bg_luma
                    ev.contrast_pre_badge_0_1 = pre_contrast
                    cue_first_frame_seen[ev.cue_index] = True
            writer.write(frame)
            processed += 1
            if progress_cb and (frame_idx % max(1, int(fps * 2)) == 0):
                progress_cb(f"Cue render: frame {frame_idx+1}/{frame_limit}")
    finally:
        writer.release(); cap.release()
    if progress_cb:
        progress_cb("Muxing audio into cued Target video...")
    mux_original_audio(master_mp4, tmp_video, output_cued_mp4, fps=fps)
    try: shutil.rmtree(tmp_dir)
    except Exception: pass
    return {**props, "rendered_frames": processed, "rendered_duration_sec": processed / fps if fps else None}




def make_sensor_pulse_schedule(
    duration_sec: float,
    cue_events: List[CueEvent],
    enabled: bool,
    mode: str,
    position: str,
    video_start_duration_sec: float,
    cue_pulse_duration_sec: float,
) -> List[SensorPulseEvent]:
    """Create display-timing pulses for an ALS-PT19/photodiode-style sensor.

    Default/recommended mode is video_start. Cue-start pulses are useful for
    hardware-validation runs but are not recommended as the default analysis stimulus
    because they introduce a regular external visual perturbation.
    """
    if not enabled:
        return []
    mode = (mode or "video_start").strip().lower()
    if mode not in {"fullscreen_start", "video_start", "cue_start", "both", "none"}:
        raise ValueError("sensor_pulse_mode must be one of: fullscreen_start, video_start, cue_start, both, none")
    if mode == "none":
        return []
    pulses: List[SensorPulseEvent] = []
    idx = 1
    if mode in {"fullscreen_start", "video_start", "both"}:
        dur = max(0.05, float(video_start_duration_sec))
        pulse_type = "fullscreen_start_flash" if mode == "fullscreen_start" else "video_start"
        pulse_position = "fullscreen" if mode == "fullscreen_start" else position
        pulses.append(SensorPulseEvent(idx, pulse_type, 0.0, min(dur, duration_sec), min(dur, duration_sec), pulse_position))
        idx += 1
    if mode in {"cue_start", "both"}:
        dur = max(0.02, float(cue_pulse_duration_sec))
        for ev in cue_events:
            st = float(ev.start_sec)
            en = min(float(ev.start_sec) + dur, duration_sec)
            if en > st:
                pulses.append(SensorPulseEvent(idx, "cue_start", round(st, 6), round(en, 6), round(en - st, 6), position))
                idx += 1
    return pulses


def find_active_sensor_pulse(t_sec: float, pulses: List[SensorPulseEvent]) -> Optional[SensorPulseEvent]:
    for ev in pulses:
        if ev.start_sec <= t_sec < ev.end_sec:
            return ev
    return None


def sensor_square_geometry(frame_shape: Tuple[int, int, int], position: str, size_px: int, margin_px: int, size_frac: float) -> Tuple[int, int, int, int]:
    h, w = frame_shape[:2]
    if int(size_px) > 0:
        size = int(size_px)
    else:
        # Default approx 3.5% of the smaller dimension; big enough for ALS-PT19,
        # small enough to hide under the sensor/tape shroud.
        size = int(round(min(w, h) * float(size_frac)))
    size = max(12, min(size, int(min(w, h) * 0.12)))
    margin = max(2, int(margin_px))
    pos = position.lower().strip()
    if pos == "lower_right":
        x2 = w - margin; x1 = x2 - size; y2 = h - margin; y1 = y2 - size
    elif pos == "lower_left":
        x1 = margin; x2 = x1 + size; y2 = h - margin; y1 = y2 - size
    elif pos == "upper_right":
        x2 = w - margin; x1 = x2 - size; y1 = margin; y2 = y1 + size
    elif pos == "upper_left":
        x1 = margin; x2 = x1 + size; y1 = margin; y2 = y1 + size
    else:
        raise ValueError(f"Unsupported sensor square position: {position}")
    return int(max(0, x1)), int(max(0, y1)), int(min(w, x2)), int(min(h, y2))


def draw_sensor_square(frame_bgr: np.ndarray, active: bool, position: str, size_px: int, margin_px: int, size_frac: float, idle_level: int, pulse_level: int) -> Tuple[np.ndarray, Tuple[int, int, int, int]]:
    out = frame_bgr.copy()
    x1, y1, x2, y2 = sensor_square_geometry(out.shape, position, size_px, margin_px, size_frac)
    val = int(pulse_level if active else idle_level)
    val = max(0, min(255, val))
    cv2.rectangle(out, (x1, y1), (x2, y2), (val, val, val), -1)
    return out, (x1, y1, x2, y2)


def render_sensor_timing_video(
    input_mp4: Path,
    output_mp4: Path,
    pulses: List[SensorPulseEvent],
    position: str,
    size_px: int,
    margin_px: int,
    size_frac: float,
    idle_level: int,
    pulse_level: int,
    overwrite: bool,
    progress_cb=None,
    max_seconds: Optional[float] = None,
) -> Dict[str, Any]:
    """Render a black/white square into a video for physical display timing.

    The square should be placed under the ALS-PT19 sensor and covered with a small
    opaque shroud/tape. It is a hardware timing channel, not a subject-facing cue.
    """
    if output_mp4.exists() and not overwrite:
        raise FileExistsError(f"Output exists: {output_mp4}")
    props = get_video_props(input_mp4)
    fps, width, height, frame_count = props["fps"], props["width"], props["height"], props["frame_count"]
    frame_limit = min(frame_count, int(round(max_seconds * fps))) if max_seconds else frame_count
    cap = cv2.VideoCapture(str(input_mp4))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open {input_mp4}")
    tmp_dir = Path(tempfile.mkdtemp(prefix="praycg_v16S_sensor_"))
    tmp_video = tmp_dir / "sensor_no_audio.mp4"
    writer = cv2.VideoWriter(str(tmp_video), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Could not open cv2 VideoWriter for sensor timing video")
    pulse_first_frame_seen: Dict[int, bool] = {}
    square_bbox = None
    processed = 0
    try:
        for frame_idx in range(frame_limit):
            ok, frame = cap.read()
            if not ok:
                break
            t = frame_idx / fps
            ev = find_active_sensor_pulse(t, pulses)
            frame, bbox = draw_sensor_square(frame, active=(ev is not None), position=position, size_px=size_px, margin_px=margin_px, size_frac=size_frac, idle_level=idle_level, pulse_level=pulse_level)
            square_bbox = bbox
            if ev is not None and ev.pulse_index not in pulse_first_frame_seen:
                ev.square_x1, ev.square_y1, ev.square_x2, ev.square_y2 = bbox
                ev.idle_level_0_255 = int(idle_level)
                ev.pulse_level_0_255 = int(pulse_level)
                pulse_first_frame_seen[ev.pulse_index] = True
            writer.write(frame)
            processed += 1
            if progress_cb and (frame_idx % max(1, int(fps * 2)) == 0):
                progress_cb(f"Sensor timing render: frame {frame_idx+1}/{frame_limit}")
    finally:
        writer.release(); cap.release()
    if progress_cb:
        progress_cb("Muxing audio into sensor-timing video...")
    mux_original_audio(input_mp4, tmp_video, output_mp4, fps=fps)
    try: shutil.rmtree(tmp_dir)
    except Exception: pass
    return {**props, "rendered_frames": processed, "rendered_duration_sec": processed / fps if fps else None, "sensor_square_bbox": square_bbox, "sensor_pulse_count": len(pulses)}




def render_fullscreen_start_pulse_video(
    input_mp4: Path,
    output_mp4: Path,
    white_duration_sec: float,
    black_guard_sec: float,
    pulse_level: int,
    idle_level: int,
    overwrite: bool,
    progress_cb=None,
    max_seconds: Optional[float] = None,
) -> Dict[str, Any]:
    """Prepend a full-frame white ALS pulse and black guard to a video.

    This is the robust ALS-PT19 mode. It does not require the sensor to be placed
    over a tiny corner square; any sensor placement over the active display should
    see the whole-screen transition from the preceding black settle screen to white.
    Original audio is delayed by the exact visual prefix duration so content audio
    remains aligned with original content frames.
    """
    if output_mp4.exists() and not overwrite:
        raise FileExistsError(f"Output exists: {output_mp4}")
    props = get_video_props(input_mp4)
    fps, width, height, frame_count = props["fps"], props["width"], props["height"], props["frame_count"]
    if fps <= 0:
        raise RuntimeError(f"Invalid FPS for {input_mp4}: {fps}")
    white_frames = max(1, int(round(float(white_duration_sec) * fps)))
    black_frames = max(0, int(round(float(black_guard_sec) * fps)))
    prefix_frames = white_frames + black_frames
    content_offset_sec = prefix_frames / fps
    frame_limit = min(frame_count, int(round(max_seconds * fps))) if max_seconds else frame_count
    cap = cv2.VideoCapture(str(input_mp4))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open {input_mp4}")
    tmp_dir = Path(tempfile.mkdtemp(prefix="praycg_v16S_fullscreen_als_"))
    tmp_video = tmp_dir / "fullscreen_als_no_audio.mp4"
    writer = cv2.VideoWriter(str(tmp_video), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Could not open cv2 VideoWriter for full-screen ALS timing video")
    pulse_val = int(max(0, min(255, pulse_level)))
    idle_val = int(max(0, min(255, idle_level)))
    white_frame = np.full((height, width, 3), pulse_val, dtype=np.uint8)
    black_frame = np.full((height, width, 3), idle_val, dtype=np.uint8)
    processed_content = 0
    try:
        if progress_cb:
            progress_cb(f"Writing full-screen ALS white pulse: {white_frames} frames")
        for _ in range(white_frames):
            writer.write(white_frame)
        if progress_cb and black_frames:
            progress_cb(f"Writing post-pulse black guard: {black_frames} frames")
        for _ in range(black_frames):
            writer.write(black_frame)
        for frame_idx in range(frame_limit):
            ok, frame = cap.read()
            if not ok:
                break
            writer.write(frame)
            processed_content += 1
            if progress_cb and (frame_idx % max(1, int(fps * 2)) == 0):
                progress_cb(f"Full-screen ALS prefix render: content frame {frame_idx+1}/{frame_limit}")
    finally:
        writer.release(); cap.release()
    if progress_cb:
        progress_cb("Muxing delayed original audio into full-screen ALS timing video...")
    mux_delayed_original_audio(input_mp4, tmp_video, output_mp4, delay_sec=content_offset_sec, fps=fps)
    try: shutil.rmtree(tmp_dir)
    except Exception: pass
    final_props = get_video_props(output_mp4)
    return {
        **final_props,
        "source_content_props": props,
        "rendered_content_frames": processed_content,
        "fullscreen_pulse": True,
        "white_frames": white_frames,
        "black_guard_frames": black_frames,
        "white_duration_sec_actual": white_frames / fps,
        "black_guard_sec_actual": black_frames / fps,
        "content_start_offset_sec": content_offset_sec,
        "analysis_exclusion_prefix_sec": content_offset_sec,
        "sensor_pulse_count": 1,
        "sensor_frame_mode": "fullscreen_start_flash",
    }


def phase_scramble_frame_bgr(frame_bgr: np.ndarray, rng: np.random.Generator, contrast_strength: float = 0.65) -> np.ndarray:
    frame = frame_bgr.astype(np.float32)
    out = np.zeros_like(frame)
    for ch in range(3):
        x = frame[:, :, ch]
        orig_mean = float(np.mean(x)); orig_std = float(np.std(x) + 1e-6)
        fft = np.fft.rfft2(x)
        amp = np.abs(fft)
        phase = rng.uniform(-np.pi, np.pi, size=fft.shape)
        phase[0, 0] = 0.0
        y = np.fft.irfft2(amp * np.exp(1j * phase), s=x.shape)
        y_std = float(np.std(y) + 1e-6)
        y = (y - float(np.mean(y))) * (orig_std / y_std) + orig_mean
        out[:, :, ch] = y
    out = 128.0 + float(contrast_strength) * (out - 128.0)
    return np.clip(out, 0, 255).astype(np.uint8)


def render_phase_scrambled_video_no_audio(input_mp4: Path, output_no_audio_mp4: Path, seed: int, contrast_strength: float, overwrite: bool, progress_cb=None, max_seconds: Optional[float] = None) -> Dict[str, Any]:
    if output_no_audio_mp4.exists() and not overwrite:
        raise FileExistsError(f"Output exists: {output_no_audio_mp4}")
    props = get_video_props(input_mp4)
    fps, width, height, frame_count = props["fps"], props["width"], props["height"], props["frame_count"]
    frame_limit = min(frame_count, int(round(max_seconds * fps))) if max_seconds else frame_count
    cap = cv2.VideoCapture(str(input_mp4))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open {input_mp4}")
    writer = cv2.VideoWriter(str(output_no_audio_mp4), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        cap.release(); raise RuntimeError("Could not open cv2 VideoWriter for scrambled video")
    processed = 0
    try:
        for frame_idx in range(frame_limit):
            ok, frame = cap.read()
            if not ok:
                break
            rng = np.random.default_rng(int(seed) + frame_idx * 1009)
            y = phase_scramble_frame_bgr(frame, rng, contrast_strength=contrast_strength)
            writer.write(y)
            processed += 1
            if progress_cb and (frame_idx % max(1, int(fps * 2)) == 0):
                progress_cb(f"Phase-scramble video: frame {frame_idx+1}/{frame_limit}")
    finally:
        writer.release(); cap.release()
    return {**props, "rendered_frames": processed, "rendered_duration_sec": processed / fps if fps else None}


def moving_rms_envelope(x: np.ndarray, frame_len: int) -> np.ndarray:
    frame_len = max(8, int(frame_len))
    kernel = np.ones(frame_len, dtype=np.float32) / float(frame_len)
    env = np.sqrt(np.convolve(x.astype(np.float32) ** 2, kernel, mode="same") + 1e-12)
    return env.astype(np.float32)


def smooth_magnitude(mag: np.ndarray, width: int = 101) -> np.ndarray:
    width = int(max(5, width))
    if width % 2 == 0:
        width += 1
    if mag.size < width:
        return mag
    try:
        return signal.medfilt(mag, kernel_size=width)
    except Exception:
        kernel = np.ones(width, dtype=np.float32) / width
        return np.convolve(mag, kernel, mode="same")


def write_float_audio_to_wav(path: Path, audio_fps: int, out: np.ndarray) -> Dict[str, Any]:
    out = np.asarray(out, dtype=np.float32)
    out = np.nan_to_num(out, nan=0.0, posinf=0.0, neginf=0.0)
    out = np.clip(out, -0.98, 0.98)
    wavfile.write(str(path), int(audio_fps), (out * 32767.0).astype(np.int16))
    return {"audio_fps": int(audio_fps), "channels": int(out.shape[1] if out.ndim > 1 else 1), "samples": int(out.shape[0]), "duration_sec": float(out.shape[0] / audio_fps), "rms": float(np.sqrt(np.mean(out ** 2)) + 1e-12)}


def audio_speech_shaped_noise_envelope_to_wav(input_mp4: Path, output_wav: Path, seed: int, audio_fps: int = 44100, envelope_sec: float = 0.05, progress_cb=None) -> Optional[Dict[str, Any]]:
    loaded = load_audio_array(input_mp4, audio_fps=audio_fps)
    if loaded is None:
        return None
    arr, audio_fps = loaded
    original_rms = float(np.sqrt(np.mean(arr ** 2)) + 1e-12)
    frame_len = max(16, int(round(float(envelope_sec) * audio_fps)))
    rng = np.random.default_rng(int(seed) + 91001)
    out_chs = []
    for ch in range(arr.shape[1]):
        if progress_cb:
            progress_cb(f"Speech-shaped envelope noise audio channel {ch+1}/{arr.shape[1]}...")
        x = arr[:, ch].astype(np.float32)
        mag = np.abs(np.fft.rfft(x))
        mag_smooth = smooth_magnitude(mag, width=max(31, int(len(mag) / 600)))
        random_phase = rng.uniform(-np.pi, np.pi, size=mag_smooth.shape)
        random_phase[0] = 0.0
        y = np.fft.irfft(mag_smooth * np.exp(1j * random_phase), n=len(x)).astype(np.float32)
        env_x = moving_rms_envelope(x, frame_len)
        env_y = moving_rms_envelope(y, frame_len)
        y = y * (env_x / (env_y + 1e-6))
        y = y - np.mean(y)
        out_chs.append(y.astype(np.float32))
    out = np.stack(out_chs, axis=1)
    out_rms = float(np.sqrt(np.mean(out ** 2)) + 1e-12)
    out = out * (original_rms / out_rms)
    summary = write_float_audio_to_wav(output_wav, audio_fps, out)
    summary.update({"mode": "speech_shaped_noise_envelope", "original_rms": original_rms, "processed_rms": summary["rms"], "envelope_sec": float(envelope_sec), "purpose": "Preserve digital loudness/envelope while destroying intelligible speech."})
    return summary


def audio_stft_phase_scramble_to_wav(input_mp4: Path, output_wav: Path, seed: int, audio_fps: int = 44100, nperseg: int = 4096, noverlap: int = 3072, progress_cb=None) -> Optional[Dict[str, Any]]:
    loaded = load_audio_array(input_mp4, audio_fps=audio_fps)
    if loaded is None:
        return None
    arr, audio_fps = loaded
    original_rms = float(np.sqrt(np.mean(arr ** 2)) + 1e-12)
    rng = np.random.default_rng(int(seed) + 777777)
    out_chs = []
    for ch in range(arr.shape[1]):
        if progress_cb:
            progress_cb(f"STFT phase-scrambling audio channel {ch+1}/{arr.shape[1]}...")
        x = arr[:, ch]
        f, t, Z = signal.stft(x, fs=audio_fps, window="hann", nperseg=nperseg, noverlap=noverlap, boundary="zeros", padded=True)
        mag = np.abs(Z)
        random_phase = rng.uniform(-np.pi, np.pi, size=Z.shape)
        random_phase[0, :] = 0.0
        Zs = mag * np.exp(1j * random_phase)
        _, y = signal.istft(Zs, fs=audio_fps, window="hann", nperseg=nperseg, noverlap=noverlap, input_onesided=True, boundary=True)
        out_chs.append(y[: len(x)].astype(np.float32))
    out = np.stack(out_chs, axis=1)
    out_rms = float(np.sqrt(np.mean(out ** 2)) + 1e-12)
    out = out * (original_rms / out_rms)
    summary = write_float_audio_to_wav(output_wav, audio_fps, out)
    summary.update({"mode": "stft_phase_scramble", "original_rms": original_rms, "processed_rms": summary["rms"], "purpose": "Legacy-like local phase scramble; manual intelligibility QC required."})
    return summary


def audio_full_fft_phase_scramble_to_wav(input_mp4: Path, output_wav: Path, seed: int, audio_fps: int = 44100, progress_cb=None) -> Optional[Dict[str, Any]]:
    loaded = load_audio_array(input_mp4, audio_fps=audio_fps)
    if loaded is None:
        return None
    arr, audio_fps = loaded
    original_rms = float(np.sqrt(np.mean(arr ** 2)) + 1e-12)
    rng = np.random.default_rng(int(seed) + 4444)
    out_chs = []
    for ch in range(arr.shape[1]):
        if progress_cb:
            progress_cb(f"Full-track FFT phase-scrambling audio channel {ch+1}/{arr.shape[1]}...")
        x = arr[:, ch]
        fft = np.fft.rfft(x)
        mag = np.abs(fft)
        phase = rng.uniform(-np.pi, np.pi, size=mag.shape)
        phase[0] = 0.0
        y = np.fft.irfft(mag * np.exp(1j * phase), n=len(x)).astype(np.float32)
        out_chs.append(y)
    out = np.stack(out_chs, axis=1)
    out_rms = float(np.sqrt(np.mean(out ** 2)) + 1e-12)
    out = out * (original_rms / out_rms)
    summary = write_float_audio_to_wav(output_wav, audio_fps, out)
    summary.update({"mode": "full_fft_phase_scramble_legacy", "original_rms": original_rms, "processed_rms": summary["rms"], "purpose": "Legacy whole-track phase scramble; may leave ghost intelligibility in some dialogue-heavy clips."})
    return summary


def audio_mute_to_wav(input_mp4: Path, output_wav: Path, audio_fps: int = 44100, progress_cb=None) -> Optional[Dict[str, Any]]:
    loaded = load_audio_array(input_mp4, audio_fps=audio_fps)
    if loaded is None:
        return None
    arr, audio_fps = loaded
    out = np.zeros_like(arr, dtype=np.float32)
    summary = write_float_audio_to_wav(output_wav, audio_fps, out)
    summary.update({"mode": "mute", "original_rms": float(np.sqrt(np.mean(arr ** 2)) + 1e-12), "processed_rms": 0.0, "purpose": "Diagnostic only; not recommended for matched sensory controls."})
    return summary


def make_control_audio_to_wav(input_mp4: Path, output_wav: Path, mode: str, seed: int, audio_fps: int, envelope_sec: float, progress_cb=None) -> Optional[Dict[str, Any]]:
    mode = (mode or "speech_shaped_noise_envelope").lower().strip()
    if mode == "speech_shaped_noise_envelope":
        return audio_speech_shaped_noise_envelope_to_wav(input_mp4, output_wav, seed=seed, audio_fps=audio_fps, envelope_sec=envelope_sec, progress_cb=progress_cb)
    if mode == "stft_phase_scramble":
        return audio_stft_phase_scramble_to_wav(input_mp4, output_wav, seed=seed, audio_fps=audio_fps, progress_cb=progress_cb)
    if mode == "full_fft_phase_scramble_legacy":
        return audio_full_fft_phase_scramble_to_wav(input_mp4, output_wav, seed=seed, audio_fps=audio_fps, progress_cb=progress_cb)
    if mode == "mute":
        return audio_mute_to_wav(input_mp4, output_wav, audio_fps=audio_fps, progress_cb=progress_cb)
    raise ValueError(f"Unknown control audio mode: {mode}")


def phase_scramble_media(input_cued_mp4: Path, output_control_mp4: Path, seed: int, contrast_strength: float, control_audio_mode: str, control_audio_fps: int, audio_envelope_sec: float, overwrite: bool, progress_cb=None, max_seconds: Optional[float] = None) -> Dict[str, Any]:
    if output_control_mp4.exists() and not overwrite:
        raise FileExistsError(f"Output exists: {output_control_mp4}")
    tmp_dir = Path(tempfile.mkdtemp(prefix="praycg_v16Q_scramble_"))
    tmp_vid = tmp_dir / "control_no_audio.mp4"
    tmp_wav = tmp_dir / "control_audio.wav"
    try:
        video_summary = render_phase_scrambled_video_no_audio(input_cued_mp4, tmp_vid, seed=seed, contrast_strength=contrast_strength, overwrite=True, progress_cb=progress_cb, max_seconds=max_seconds)
        audio_summary = make_control_audio_to_wav(input_cued_mp4, tmp_wav, mode=control_audio_mode, seed=seed, audio_fps=control_audio_fps, envelope_sec=audio_envelope_sec, progress_cb=progress_cb)
        if audio_summary is not None:
            if progress_cb:
                progress_cb(f"Muxing {control_audio_mode} control audio into phase-scrambled control...")
            mux_wav_audio(tmp_vid, tmp_wav, output_control_mp4)
        else:
            shutil.copy2(tmp_vid, output_control_mp4)
        return {"video": video_summary, "audio": audio_summary, "source": str(input_cued_mp4), "audio_mode": control_audio_mode, "manual_audio_unintelligibility_qc_required": True}
    finally:
        try: shutil.rmtree(tmp_dir)
        except Exception: pass




def clone_and_shift_cue_events(events: List[CueEvent], offset_sec: float) -> List[CueEvent]:
    """Return cue events shifted into final video time after an ALS prefix.

    Cue rendering happens in content time. If a full-screen white/black ALS prefix
    is prepended after cue rendering, the final MP4 cue times are content time
    plus the prefix duration. The protocol runner should use the shifted schedule
    so LSL cue markers line up with the physical cue frames.
    """
    offset_sec = float(offset_sec or 0.0)
    out: List[CueEvent] = []
    for ev in events:
        d = asdict(ev)
        d["content_start_sec"] = d.get("start_sec")
        d["content_end_sec"] = d.get("end_sec")
        d["start_sec"] = round(float(ev.start_sec) + offset_sec, 6)
        d["end_sec"] = round(float(ev.end_sec) + offset_sec, 6)
        out.append(CueEvent(**{k: v for k, v in d.items() if k in CueEvent.__dataclass_fields__}))
        # Attach extra attributes for JSON/CSV by setting them dynamically.
        setattr(out[-1], "content_start_sec", round(float(ev.start_sec), 6))
        setattr(out[-1], "content_end_sec", round(float(ev.end_sec), 6))
    return out


def cue_event_to_dict(ev: CueEvent) -> Dict[str, Any]:
    d = asdict(ev)
    if hasattr(ev, "content_start_sec"):
        d["content_start_sec"] = getattr(ev, "content_start_sec")
    if hasattr(ev, "content_end_sec"):
        d["content_end_sec"] = getattr(ev, "content_end_sec")
    return d


def write_schedule_files(events: List[CueEvent], json_path: Path, csv_path: Path, metadata: Dict[str, Any]) -> None:
    event_dicts = [cue_event_to_dict(ev) for ev in events]
    payload = {**metadata, "cue_count": len(events), "expected_sum": int(sum(ev.value for ev in events)), "cue_events": event_dicts}
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(event_dicts[0].keys()) if event_dicts else ["cue_index", "value"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in event_dicts:
            writer.writerow(row)


def make_qc_checklists(out_dir: Path, manifest: Dict[str, Any]) -> None:
    audio_mode = manifest.get("control_audio", {}).get("mode") or manifest.get("scramble_summary", {}).get("audio_mode")
    (out_dir / "CONTROL_AUDIO_QC_CHECKLIST_v1_6S.md").write_text(textwrap_dedent(f"""
    # PRAYCG v1.6S Control Audio QC Checklist

    Project: `{manifest.get('project_name')}`
    Control audio mode: `{audio_mode}`

    ## Required manual checks

    Listen to the full phase-scrambled control using the same headphones/speaker settings used for the protocol.

    Pass criteria:
    - No recognizable spoken words.
    - No intelligible sentence fragments.
    - No distinct musical melody that carries narrative recognition.
    - Loudness/envelope should rise and fall in a way that broadly tracks the original.
    - The control should sound like speech-shaped or scene-shaped noise, not like understandable dialogue.

    Record:
    - Audio intelligibility rating 0-9: ______
    - Any recognizable words? yes / no
    - Any recognizable music/melody? yes / no
    - QC verdict: PASS / FAIL / PILOT ONLY

    Boundary: this automated tool cannot certify unintelligibility. Human QC remains mandatory.
    """), encoding="utf-8")
    (out_dir / "VISUAL_SOURCE_STAMP_QC_CHECKLIST_v1_6S.md").write_text(textwrap_dedent(f"""
    # PRAYCG v1.6S Visual Source-Stamp / Watermark QC Checklist

    Project: `{manifest.get('project_name')}`

    ## Required manual checks

    Watch Target, Contextual Override, and Control.

    Pass criteria:
    - No readable source watermark, source stamp, platform logo, or subtitle artifact remains in Target or Override unless intentionally documented.
    - If a mask/cleanup was applied, it was applied before all branches were generated.
    - Target and Override remain bit-identical after cue rendering.
    - Control was generated from the cleaned cue-embedded Target.

    Record:
    - Upper-left stamp removed or neutralized? yes / no / not applicable
    - Other readable logo/stamp present? yes / no
    - Visual QC verdict: PASS / FAIL / PILOT ONLY

    Boundary: source-stamp cleanup is allowed only as a documented preprocessing step applied before branch generation.
    """), encoding="utf-8")

    sensor_design = manifest.get("sensor_timing_design", {})
    (out_dir / "ALS_PT19_SENSOR_TIMING_QC_CHECKLIST_v1_6S.md").write_text(textwrap_dedent(f"""
    # PRAYCG v1.6S ALS-PT19 / Photodiode Timing QC Checklist

    Project: `{manifest.get('project_name')}`
    Sensor timing enabled: `{sensor_design.get('enabled')}`
    Pulse mode: `{sensor_design.get('pulse_mode')}`
    White pulse duration: `{sensor_design.get('video_start_duration_sec')}` sec
    Black guard duration: `{sensor_design.get('fullscreen_black_guard_sec')}` sec
    Content start offset: `{sensor_design.get('content_start_offset_sec')}` sec

    ## Hardware placement

    - In `fullscreen_start` mode, place the ALS-PT19 anywhere securely over the active display area where it can see the full-screen white flash.
    - A black electrical tape / opaque shroud is still recommended to reduce room-light contamination.
    - The old lower-right square mode remains available, but exact corner placement is no longer required in fullscreen mode.
    - Confirm the sensor signal is recorded in the OpenBCI analog AUX / Analog Read LSL stream.

    ## Required test before real run

    1. Play the generated Target video for at least 10 seconds.
    2. Confirm a strong analog rise during the full-screen white pulse.
    3. Confirm the signal returns to baseline during the black guard.
    4. Repeat on Control and Override.

    ## Pass criteria

    - Pulse visible in AUX stream.
    - No clipping at maximum ADC value for the full pulse duration.
    - No pulse missed at video start.
    - Target, Override, and Control all contain the full-screen timing prefix.
    - Cue markers use the shifted v1.6S cue schedule.

    Boundary: this timing prefix validates physical display timing. It belongs to the external input vector u(t), not to any biological hidden variable Y(t).
    """), encoding="utf-8")


def textwrap_dedent(s: str) -> str:
    import textwrap
    return textwrap.dedent(s).strip() + "\n"


def make_report(out_dir: Path, manifest: Dict[str, Any]) -> None:
    lines = []
    lines.append("# PRAYCG MediaPrep Suite v1.6S ALS-PT19 Fullscreen Start-Pulse Patch Report")
    lines.append("")
    lines.append(f"Created UTC: `{manifest.get('created_utc')}`")
    lines.append(f"Project: `{manifest.get('project_name')}`")
    lines.append("")
    lines.append("## Outputs")
    for key in ["master_input", "cleaned_master", "target_cued", "override_cued", "control_phase_scrambled", "cue_schedule_json", "cue_schedule_csv"]:
        val = manifest.get("outputs", {}).get(key)
        if val:
            lines.append(f"- **{key}:** `{val}`")
    lines.append("")
    lines.append("## SHA-256")
    for key, val in manifest.get("sha256", {}).items():
        lines.append(f"- **{key}:** `{val}`")
    lines.append("")
    lines.append("## Cue Design")
    for k, v in manifest.get("cue_design", {}).items():
        lines.append(f"- **{k}:** `{v}`")
    lines.append("")
    lines.append("## Visual source-stamp cleanup")
    vc = manifest.get("visual_cleanup", {})
    if vc.get("enabled"):
        for k, v in vc.items():
            lines.append(f"- **{k}:** `{v}`")
    else:
        lines.append("- **enabled:** `False`")
    lines.append("")
    lines.append("## Control audio")
    ca = manifest.get("control_audio", {})
    for k, v in ca.items():
        lines.append(f"- **{k}:** `{v}`")
    lines.append("")
    lines.append("## ALS-PT19 / photodiode timing marker")
    st = manifest.get("sensor_timing_design", {})
    for k, v in st.items():
        lines.append(f"- **{k}:** `{v}`")
    lines.append(f"- **pulse_count:** `{len(manifest.get('sensor_timing_pulse_events', []))}`")
    lines.append("")
    lines.append("## Critical method rules")
    lines.append("")
    lines.append("1. Target and Contextual Override are generated from the same cue-embedded video. Only the participant instructions should differ.")
    lines.append("2. Any source-stamp/watermark cleanup must be applied to the master before Target, Override, and Control branches are generated.")
    lines.append("3. The phase-scrambled Control is generated from the cue-embedded Target so cue timing and low-level cue energy are represented in the control branch.")
    lines.append("4. Control audio must be manually QC-checked. If recognizable words remain, the control is invalid or pilot-only.")
    lines.append("5. The ALS timing marker is a physical display-timing channel. In fullscreen_start mode, exclude the white/black prefix from physiology interpretation and do not interpret it as biological photonic data.")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append("This tool prepares media. It does not certify meaning, empathy, neural endpoints, task compliance, or audio unintelligibility. The output should be followed by manual media QC, StimulusFingerprint QC, protocol acquisition, and the Master Comprehensive PR-AYC-G analysis suite.")
    (out_dir / "PRAYCG_MediaPrep_v1_6S_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_media_prep(args: argparse.Namespace, progress_cb=None) -> Path:
    master = Path(args.master).expanduser().resolve()
    if not master.exists():
        raise FileNotFoundError(master)
    project = sanitize_name(args.project_name or master.stem)
    out_root = Path(args.out_root).expanduser().resolve()
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"{project}_MediaPrep_v1_6S_{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    if progress_cb:
        progress_cb(f"Output folder: {out_dir}")

    props = get_video_props(master)
    effective_duration = float(props["duration_sec"] if args.max_seconds in (None, 0) else min(props["duration_sec"], args.max_seconds))
    events = make_cue_schedule(effective_duration, int(args.seed), float(args.cue_interval), float(args.cue_duration), float(args.start_delay), int(args.min_value), int(args.max_value), args.position)

    cleaned_master: Optional[Path] = None
    working_master = master
    visual_cleanup_summary: Dict[str, Any] = {"enabled": bool(args.clean_visual_mask)}
    if args.clean_visual_mask:
        cleaned_master = out_dir / f"stimulus_master_cleaned_{project}_v1_6S.mp4"
        if progress_cb:
            progress_cb("Applying documented visual source-stamp/watermark cleanup to master before branching...")
        fill_rgb = tuple(int(x) for x in str(args.mask_fill_rgb).split(",")) if isinstance(args.mask_fill_rgb, str) else (0, 0, 0)
        if len(fill_rgb) != 3:
            fill_rgb = (0, 0, 0)
        visual_cleanup_summary = render_cleaned_master(master, cleaned_master, args.mask_preset, args.mask_method, int(args.mask_x1), int(args.mask_y1), int(args.mask_x2), int(args.mask_y2), fill_rgb, bool(args.overwrite), progress_cb=progress_cb, max_seconds=args.max_seconds)
        visual_cleanup_summary["enabled"] = True
        visual_cleanup_summary["source_master"] = str(master)
        visual_cleanup_summary["cleaned_master"] = str(cleaned_master)
        working_master = cleaned_master

    target_cued = out_dir / f"stimulus_target_cued_{project}_v1_6S.mp4"
    override_cued = out_dir / f"stimulus_override_cued_{project}_v1_6S.mp4"
    control = out_dir / f"stimulus_control_cued_phase_scrambled_{project}_v1_6S.mp4"
    schedule_json = out_dir / f"cue_schedule_{project}_v1_6S.json"
    schedule_csv = out_dir / f"cue_schedule_{project}_v1_6S.csv"

    sensor_enabled = bool(getattr(args, "sensor_timing_enabled", False))
    sensor_mode = str(getattr(args, "sensor_pulse_mode", "fullscreen_start")).strip().lower()
    sensor_fullscreen_start = sensor_enabled and sensor_mode == "fullscreen_start"
    sensor_prefix_offset_sec = 0.0
    sensor_pulses = make_sensor_pulse_schedule(
        effective_duration,
        events,
        enabled=sensor_enabled,
        mode=str(getattr(args, "sensor_pulse_mode", "fullscreen_start")),
        position=str(getattr(args, "sensor_position", "lower_right")),
        video_start_duration_sec=float(getattr(args, "sensor_video_start_duration", 0.75)),
        cue_pulse_duration_sec=float(getattr(args, "sensor_cue_pulse_duration", 0.25)),
    )

    # If sensor timing is enabled, create number-cued working files first. The
    # readable sensor square is added AFTER the phase-scrambled control is
    # generated so Control, Target, and Override all contain identical, clean
    # timing pulses for the ALS-PT19.
    target_pre_sensor = out_dir / f"_working_target_number_cued_no_sensor_{project}_v1_6S.mp4"
    control_pre_sensor = out_dir / f"_working_control_phase_scrambled_no_sensor_{project}_v1_6S.mp4"
    cue_target_work = target_pre_sensor if sensor_enabled else target_cued

    if progress_cb:
        progress_cb("Rendering cue-embedded Target video...")
    cue_render_summary = render_cued_video(working_master, cue_target_work, events, position=args.position, badge_alpha=float(args.badge_alpha), font_scale_factor=float(args.font_scale_factor), overwrite=bool(args.overwrite), progress_cb=progress_cb, max_seconds=args.max_seconds)

    if sensor_enabled:
        if progress_cb:
            progress_cb("Rendering ALS-PT19 timing square into Target video...")
        if sensor_fullscreen_start:
            sensor_target_summary = render_fullscreen_start_pulse_video(
                cue_target_work, target_cued,
                white_duration_sec=float(args.sensor_video_start_duration),
                black_guard_sec=float(getattr(args, "sensor_fullscreen_black_guard", 0.50)),
                idle_level=int(args.sensor_idle_level),
                pulse_level=int(args.sensor_pulse_level),
                overwrite=True,
                progress_cb=progress_cb,
                max_seconds=args.max_seconds,
            )
            sensor_prefix_offset_sec = float(sensor_target_summary.get("content_start_offset_sec") or 0.0)
        else:
            sensor_target_summary = render_sensor_timing_video(
                cue_target_work, target_cued, sensor_pulses,
                position=str(args.sensor_position),
                size_px=int(args.sensor_size_px),
                margin_px=int(args.sensor_margin_px),
                size_frac=float(args.sensor_size_frac),
                idle_level=int(args.sensor_idle_level),
                pulse_level=int(args.sensor_pulse_level),
                overwrite=True,
                progress_cb=progress_cb,
                max_seconds=args.max_seconds,
            )
    else:
        sensor_target_summary = None

    if progress_cb:
        progress_cb("Copying cue-embedded Target to cue-embedded Contextual Override...")
    shutil.copy2(target_cued, override_cued)

    # The cue badges were rendered in content time. If a full-screen ALS prefix
    # was prepended, final cue times must be shifted so PRAYCG marker emission
    # matches the physical cue frames in the final MP4.
    schedule_events = clone_and_shift_cue_events(events, sensor_prefix_offset_sec) if sensor_prefix_offset_sec > 0 else events
    final_video_props = get_video_props(target_cued) if target_cued.exists() else props
    if sensor_fullscreen_start and sensor_pulses:
        for ev in sensor_pulses:
            if ev.pulse_type == "fullscreen_start_flash":
                ev.position = "fullscreen"
                ev.square_x1 = 0
                ev.square_y1 = 0
                ev.square_x2 = int(final_video_props.get("width") or 0)
                ev.square_y2 = int(final_video_props.get("height") or 0)
                ev.idle_level_0_255 = int(getattr(args, "sensor_idle_level", 0))
                ev.pulse_level_0_255 = int(getattr(args, "sensor_pulse_level", 255))

    metadata = {
        "schema": CUE_SCHEMA,
        "created_utc": now_utc_iso(),
        "input_video": str(master),
        "working_input_video": str(working_master),
        "input_sha256": sha256_file(master),
        "working_input_sha256": sha256_file(working_master),
        "output_cued_video": str(target_cued),
        "output_cued_sha256": sha256_file(target_cued),
        "output_override_video": str(override_cued),
        "output_override_sha256": sha256_file(override_cued),
        "video": final_video_props,
        "source_content_video": props,
        "cue_design": {
            "seed": int(args.seed),
            "interval_sec": float(args.cue_interval),
            "display_duration_sec": float(args.cue_duration),
            "start_delay_sec": float(args.start_delay),
            "min_value": int(args.min_value),
            "max_value": int(args.max_value),
            "position": args.position,
            "alpha": float(args.badge_alpha),
            "font_scale_factor": float(args.font_scale_factor),
            "contrast_protected_badge": True,
            "fixed_position_reason": "Fixed safe-zone placement reduces visual-search/saccade confounds relative to moving numbers.",
            "recommended_use": "Use the same cue-embedded stimulus for Target and Contextual Override. Only instructions should differ.",
            "control_generation": "Phase-scramble the cue-embedded Target to generate the Control.",
        },
        "sensor_timing_design": {
            "enabled": sensor_enabled,
            "sensor": "ALS-PT19 or equivalent photodiode/photoresistor-style analog light sensor",
            "position": str(getattr(args, "sensor_position", "lower_right")),
            "pulse_mode": str(getattr(args, "sensor_pulse_mode", "fullscreen_start")),
            "video_start_duration_sec": float(getattr(args, "sensor_video_start_duration", 0.75)),
            "fullscreen_black_guard_sec": float(getattr(args, "sensor_fullscreen_black_guard", 0.50)),
            "content_start_offset_sec": float(sensor_prefix_offset_sec),
            "analysis_exclusion_prefix_sec": float(sensor_prefix_offset_sec),
            "cue_pulse_duration_sec": float(getattr(args, "sensor_cue_pulse_duration", 0.25)),
            "size_px": int(getattr(args, "sensor_size_px", 0)),
            "size_frac": float(getattr(args, "sensor_size_frac", 0.035)),
            "margin_px": int(getattr(args, "sensor_margin_px", 16)),
            "idle_level_0_255": int(getattr(args, "sensor_idle_level", 0)),
            "pulse_level_0_255": int(getattr(args, "sensor_pulse_level", 255)),
            "interpretation": "Physical display-timing channel. It validates screen timing and belongs to the external input vector u(t), not to any biological hidden variable Y(t).",
        },
        "sensor_timing_pulse_events": [asdict(ev) for ev in sensor_pulses],
        "audio_muxed_from_working_input": True,
        "visual_cleanup": visual_cleanup_summary,
    }
    write_schedule_files(schedule_events, schedule_json, schedule_csv, metadata)

    scramble_summary = None
    sensor_control_summary = None
    if args.make_control:
        if progress_cb:
            progress_cb("Generating phase-scrambled Control from cue-embedded Target...")
        control_work = control_pre_sensor if sensor_enabled else control
        scramble_summary = phase_scramble_media(cue_target_work, control_work, seed=int(args.seed) + 31337, contrast_strength=float(args.scramble_contrast_strength), control_audio_mode=args.control_audio_mode, control_audio_fps=int(args.control_audio_fps), audio_envelope_sec=float(args.audio_envelope_sec), overwrite=bool(args.overwrite), progress_cb=progress_cb, max_seconds=args.max_seconds)
        if sensor_enabled and control_work.exists():
            if progress_cb:
                progress_cb("Rendering ALS-PT19 timing square into Control video...")
            if sensor_fullscreen_start:
                sensor_control_summary = render_fullscreen_start_pulse_video(
                    control_work, control,
                    white_duration_sec=float(args.sensor_video_start_duration),
                    black_guard_sec=float(getattr(args, "sensor_fullscreen_black_guard", 0.50)),
                    idle_level=int(args.sensor_idle_level),
                    pulse_level=int(args.sensor_pulse_level),
                    overwrite=True,
                    progress_cb=progress_cb,
                    max_seconds=args.max_seconds,
                )
            else:
                sensor_control_summary = render_sensor_timing_video(
                    control_work, control, sensor_pulses,
                    position=str(args.sensor_position),
                    size_px=int(args.sensor_size_px),
                    margin_px=int(args.sensor_margin_px),
                    size_frac=float(args.sensor_size_frac),
                    idle_level=int(args.sensor_idle_level),
                    pulse_level=int(args.sensor_pulse_level),
                    overwrite=True,
                    progress_cb=progress_cb,
                    max_seconds=args.max_seconds,
                )

    sha = {"master_input": sha256_file(master), "working_input": sha256_file(working_master), "target_cued": sha256_file(target_cued), "override_cued": sha256_file(override_cued)}
    if cleaned_master is not None and cleaned_master.exists():
        sha["cleaned_master"] = sha256_file(cleaned_master)
    if control.exists():
        sha["control_phase_scrambled"] = sha256_file(control)

    control_audio_summary = (scramble_summary or {}).get("audio") or {"mode": args.control_audio_mode, "note": "No audio generated or no audio present."}
    manifest = {
        "schema": SCHEMA,
        "created_utc": now_utc_iso(),
        "project_name": project,
        "outputs": {"output_dir": str(out_dir), "master_input": str(master), "cleaned_master": str(cleaned_master) if cleaned_master else None, "target_cued": str(target_cued), "override_cued": str(override_cued), "control_phase_scrambled": str(control) if control.exists() else None, "cue_schedule_json": str(schedule_json), "cue_schedule_csv": str(schedule_csv)},
        "sha256": sha,
        "video_props": final_video_props,
        "source_content_video_props": props,
        "cue_design": metadata["cue_design"],
        "sensor_timing_design": metadata.get("sensor_timing_design", {}),
        "sensor_timing_pulse_events": metadata.get("sensor_timing_pulse_events", []),
        "sensor_timing_render_summary": {"target": sensor_target_summary, "control": sensor_control_summary},
        "cue_count": len(events),
        "expected_sum": int(sum(ev.value for ev in events)),
        "cue_render_summary": cue_render_summary,
        "visual_cleanup": visual_cleanup_summary,
        "control_audio": control_audio_summary,
        "scramble_summary": scramble_summary,
        "qc_required": {"manual_audio_unintelligibility_qc": True, "manual_visual_source_stamp_qc": True, "stimulusfingerprint_qc_recommended": True},
        "boundary": "Media prep only. Requires manual QC, StimulusFingerprint QC, protocol acquisition, and physiology analysis before empirical claims.",
    }
    (out_dir / "media_prep_manifest_v1_6S.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    make_report(out_dir, manifest)
    make_qc_checklists(out_dir, manifest)

    if args.run_fingerprint:
        # Bundled batch script remains optional; if it fails, media generation is preserved.
        script_path = Path(__file__).resolve().parents[1] / "stimulus_fingerprint_v1_6" / "scripts" / "praycg_stimulus_fingerprint_batch_ui_v1_6.py"
        if script_path.exists() and control.exists():
            if progress_cb:
                progress_cb("Running StimulusFingerprint v1.6 on generated suite...")
            fp_out = out_dir / "qc"
            fp_out.mkdir(parents=True, exist_ok=True)
            cmd = [sys.executable, str(script_path), "--no-gui", "--project-name", project, "--control", str(control), "--target", str(target_cued), "--override", str(override_cued), "--cue-schedule-json", str(schedule_json), "--cue-schedule-csv", str(schedule_csv), "--out-root", str(fp_out), "--sample-fps", str(args.fingerprint_sample_fps), "--resize-width", str(args.fingerprint_resize_width), "--flat-output", "--overwrite"]
            (fp_out / "stimulusfingerprint_command.txt").write_text(" ".join(map(str, cmd)), encoding="utf-8")
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
            (fp_out / "stimulusfingerprint_stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
            (fp_out / "stimulusfingerprint_stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
            if proc.returncode != 0:
                msg = f"StimulusFingerprint returned non-zero exit status {proc.returncode}. Media files were still generated."
                (fp_out / "STIMULUSFINGERPRINT_FAILED_README.txt").write_text(msg + "\n", encoding="utf-8")
                if progress_cb: progress_cb(msg)
            else:
                if progress_cb: progress_cb(f"StimulusFingerprint complete: {fp_out}")
        else:
            if progress_cb:
                progress_cb("StimulusFingerprint script not found or control missing; skipped.")

    if progress_cb:
        progress_cb(f"DONE. Expected sum = {sum(ev.value for ev in events)}. Output = {out_dir}")
    return out_dir


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="PRAYCG MediaPrep GUI v1.6S ALS-PT19 Fullscreen Start-Pulse Patch")
    p.add_argument("--no-gui", action="store_true")
    p.add_argument("--master", default="", help="Master source MP4")
    p.add_argument("--out-root", default="outputs", help="Output root folder")
    p.add_argument("--project-name", default="", help="Project/stimulus suite name")
    p.add_argument("--seed", type=int, default=DEFAULT_SEED)
    p.add_argument("--start-delay", type=float, default=3.0)
    p.add_argument("--cue-interval", type=float, default=3.0)
    p.add_argument("--cue-duration", type=float, default=0.85)
    p.add_argument("--min-value", type=int, default=1)
    p.add_argument("--max-value", type=int, default=10)
    p.add_argument("--position", default="upper_right", choices=["upper_right", "upper_left", "lower_right", "lower_left"])
    p.add_argument("--badge-alpha", type=float, default=0.78)
    p.add_argument("--font-scale-factor", type=float, default=0.95)
    p.add_argument("--scramble-contrast-strength", type=float, default=0.65)
    p.add_argument("--control-audio-mode", default="speech_shaped_noise_envelope", choices=["speech_shaped_noise_envelope", "stft_phase_scramble", "full_fft_phase_scramble_legacy", "mute"])
    p.add_argument("--control-audio-fps", type=int, default=44100)
    p.add_argument("--audio-envelope-sec", type=float, default=0.05)
    p.add_argument("--clean-visual-mask", action="store_true", help="Apply documented visual source-stamp/watermark mask before all branches")
    p.add_argument("--mask-preset", default="upper_left", choices=["upper_left", "upper_right", "lower_left", "lower_right", "custom"])
    p.add_argument("--mask-method", default="blur", choices=["blur", "solid", "median_patch", "inpaint"])
    p.add_argument("--mask-x1", type=int, default=0)
    p.add_argument("--mask-y1", type=int, default=0)
    p.add_argument("--mask-x2", type=int, default=0)
    p.add_argument("--mask-y2", type=int, default=0)
    p.add_argument("--mask-fill-rgb", default="0,0,0", help="RGB fill for solid mask, e.g. 0,0,0")
    p.add_argument("--make-control", action="store_true", default=True)
    p.add_argument("--no-control", action="store_false", dest="make_control")
    p.add_argument("--run-fingerprint", action="store_true")
    p.add_argument("--fingerprint-sample-fps", type=float, default=5.0)
    p.add_argument("--fingerprint-resize-width", type=int, default=320)
    p.add_argument("--sensor-timing-enabled", action="store_true", help="Render a small black/white timing square for ALS-PT19/photodiode display timing")
    p.add_argument("--sensor-pulse-mode", default="fullscreen_start", choices=["fullscreen_start", "video_start", "cue_start", "both", "none"], help="ALS timing pulse mode. fullscreen_start prepends a whole-screen white flash plus black guard; video_start/cue_start use the legacy small corner square.")
    p.add_argument("--sensor-position", default="lower_right", choices=["lower_right", "lower_left", "upper_right", "upper_left"], help="Timing-square position. Lower-right is default; keep separate from number cue.")
    p.add_argument("--sensor-video-start-duration", type=float, default=0.75, help="Seconds of white timing pulse at the start of each video. In fullscreen_start mode this is a full-frame flash.")
    p.add_argument("--sensor-fullscreen-black-guard", type=float, default=0.50, help="Seconds of black guard after a fullscreen_start flash before original content begins")
    p.add_argument("--sensor-cue-pulse-duration", type=float, default=0.25, help="Seconds of white timing square at cue onset if cue_start/both is selected")
    p.add_argument("--sensor-size-px", type=int, default=0, help="Timing-square size in pixels. 0 = auto from sensor-size-frac")
    p.add_argument("--sensor-size-frac", type=float, default=0.035, help="Auto timing-square size as fraction of min(width,height)")
    p.add_argument("--sensor-margin-px", type=int, default=16, help="Margin from selected screen corner")
    p.add_argument("--sensor-idle-level", type=int, default=0, help="Idle square brightness 0-255")
    p.add_argument("--sensor-pulse-level", type=int, default=255, help="Pulse square brightness 0-255")
    p.add_argument("--max-seconds", type=float, default=None, help="Optional quick-test limit in seconds")
    p.add_argument("--overwrite", action="store_true")
    return p



def launch_gui(defaults: argparse.Namespace) -> None:
    """Launch a defensive Tk GUI.

    v1.6S patch: the Run button now gives immediate visible feedback, validates
    inputs before starting, disables/re-enables itself correctly, logs all worker
    output through a thread-safe queue, and writes crash details to disk when
    an output root is available. This prevents the confusing "I clicked Run and
    nothing happened" failure mode.
    """
    import queue
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    root = tk.Tk()
    root.title("PRAYCG MediaPrep Suite v1.6S - ALS-PT19 Fullscreen Start-Pulse Patch")
    root.geometry("1040x860")
    root.minsize(900, 680)

    q: "queue.Queue[tuple[str, str]]" = queue.Queue()
    vars: Dict[str, tk.StringVar] = {}
    bools: Dict[str, tk.BooleanVar] = {}
    state: Dict[str, Any] = {"running": False, "last_output": None}

    def enqueue(kind: str, msg: str) -> None:
        q.put((kind, msg))

    def poll_queue() -> None:
        try:
            while True:
                kind, msg = q.get_nowait()
                if kind == "log":
                    log.configure(state="normal")
                    log.insert("end", msg.rstrip() + "\n")
                    log.see("end")
                    log.configure(state="disabled")
                elif kind == "status":
                    status_var.set(msg)
                elif kind == "done":
                    status_var.set("Complete")
                    state["running"] = False
                    run_btn.configure(state="normal")
                    open_btn.configure(state="normal" if state.get("last_output") else "disabled")
                    messagebox.showinfo("PRAYCG MediaPrep complete", msg)
                elif kind == "error":
                    status_var.set("Error")
                    state["running"] = False
                    run_btn.configure(state="normal")
                    messagebox.showerror("PRAYCG MediaPrep error", msg)
        except queue.Empty:
            pass
        root.after(100, poll_queue)

    outer = ttk.Frame(root)
    outer.pack(fill="both", expand=True)
    canvas = tk.Canvas(outer, highlightthickness=0)
    scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    main = ttk.Frame(canvas, padding=10)
    main_window = canvas.create_window((0, 0), window=main, anchor="nw")

    def _on_main_configure(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_canvas_configure(event):
        canvas.itemconfigure(main_window, width=event.width)

    def _on_mousewheel(event):
        # Windows/macOS wheel support; Linux uses Button-4/5 bindings below.
        delta = -1 * int(event.delta / 120) if event.delta else 0
        canvas.yview_scroll(delta, "units")

    main.bind("<Configure>", _on_main_configure)
    canvas.bind("<Configure>", _on_canvas_configure)
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-3, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(3, "units"))

    header = ttk.Label(main, text="PRAYCG MediaPrep Suite v1.6S", font=("Segoe UI", 15, "bold"))
    header.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 4))
    sub = ttk.Label(main, text="One master MP4 -> cleaned/cued Target + identical Override + phase-scrambled Control + ALS fullscreen start pulse + QC files")
    sub.grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 10))

    def add_row(label: str, key: str, default: str, browse: Optional[str] = None, row: int = 0, width: int = 72):
        ttk.Label(main, text=label, anchor="w").grid(row=row, column=0, sticky="w", padx=(0, 8), pady=3)
        vars[key] = tk.StringVar(value=default)
        ent = ttk.Entry(main, textvariable=vars[key], width=width)
        ent.grid(row=row, column=1, sticky="we", padx=5, pady=3)
        if browse == "file":
            def _browse_file(k=key):
                path = filedialog.askopenfilename(title="Select MP4", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
                if path:
                    vars[k].set(path)
                    if k == "master" and not vars["project_name"].get().strip():
                        vars["project_name"].set(sanitize_name(Path(path).stem))
            ttk.Button(main, text="Browse", command=_browse_file).grid(row=row, column=2, padx=5, pady=3)
        elif browse == "dir":
            def _browse_dir(k=key):
                path = filedialog.askdirectory(title="Select output folder")
                if path:
                    vars[k].set(path)
            ttk.Button(main, text="Browse", command=_browse_dir).grid(row=row, column=2, padx=5, pady=3)

    r = 2
    add_row("Master MP4", "master", "", browse="file", row=r); r += 1
    add_row("Output root", "out_root", str(Path.cwd() / "outputs"), browse="dir", row=r); r += 1
    add_row("Project name", "project_name", "", row=r); r += 1
    add_row("Seed", "seed", str(DEFAULT_SEED), row=r); r += 1
    add_row("Cue start delay seconds", "start_delay", "3.0", row=r); r += 1
    add_row("Cue interval seconds", "cue_interval", "3.0", row=r); r += 1
    add_row("Cue display duration seconds", "cue_duration", "0.85", row=r); r += 1
    add_row("Minimum cue value", "min_value", "1", row=r); r += 1
    add_row("Maximum cue value", "max_value", "10", row=r); r += 1
    add_row("Cue position", "position", "upper_right", row=r); r += 1
    add_row("Badge opacity alpha", "badge_alpha", "0.78", row=r); r += 1
    add_row("Font scale factor", "font_scale_factor", "0.95", row=r); r += 1
    add_row("Control video scramble contrast", "scramble_contrast_strength", "0.65", row=r); r += 1
    add_row("Control audio mode", "control_audio_mode", "speech_shaped_noise_envelope", row=r); r += 1
    add_row("Audio envelope seconds", "audio_envelope_sec", "0.05", row=r); r += 1
    add_row("Control audio sample rate", "control_audio_fps", "44100", row=r); r += 1
    add_row("Mask preset", "mask_preset", "upper_left", row=r); r += 1
    add_row("Mask method", "mask_method", "blur", row=r); r += 1
    add_row("Custom mask x1,y1,x2,y2", "mask_coords", "0,0,0,0", row=r); r += 1
    add_row("Solid mask fill RGB", "mask_fill_rgb", "0,0,0", row=r); r += 1
    add_row("Quick-test max seconds (blank = full)", "max_seconds", "", row=r); r += 1
    add_row("Fingerprint sample FPS", "fingerprint_sample_fps", "5", row=r); r += 1
    add_row("Fingerprint resize width", "fingerprint_resize_width", "320", row=r); r += 1
    add_row("ALS sensor square position", "sensor_position", "lower_right", row=r); r += 1
    add_row("ALS pulse mode", "sensor_pulse_mode", "fullscreen_start", row=r); r += 1
    add_row("ALS white/fullscreen pulse seconds", "sensor_video_start_duration", "0.75", row=r); r += 1
    add_row("ALS fullscreen black guard seconds", "sensor_fullscreen_black_guard", "0.50", row=r); r += 1
    add_row("ALS cue-start pulse seconds", "sensor_cue_pulse_duration", "0.25", row=r); r += 1
    add_row("ALS square size px (0 = auto)", "sensor_size_px", "0", row=r); r += 1
    add_row("ALS square size fraction", "sensor_size_frac", "0.035", row=r); r += 1
    add_row("ALS square margin px", "sensor_margin_px", "16", row=r); r += 1

    bools["sensor_timing_enabled"] = tk.BooleanVar(value=True)
    bools["overwrite"] = tk.BooleanVar(value=True)
    bools["run_fingerprint"] = tk.BooleanVar(value=False)
    bools["make_control"] = tk.BooleanVar(value=True)
    bools["clean_visual_mask"] = tk.BooleanVar(value=False)
    ttk.Checkbutton(main, text="Add ALS-PT19 / photodiode timing square to all branch videos", variable=bools["sensor_timing_enabled"]).grid(row=r, column=1, columnspan=2, sticky="w", padx=5, pady=2); r += 1
    ttk.Checkbutton(main, text="Apply visual source-stamp/watermark mask BEFORE all branches", variable=bools["clean_visual_mask"]).grid(row=r, column=1, columnspan=2, sticky="w", padx=5, pady=2); r += 1
    ttk.Checkbutton(main, text="Generate phase-scrambled Control from cue-embedded Target", variable=bools["make_control"]).grid(row=r, column=1, columnspan=2, sticky="w", padx=5, pady=2); r += 1
    ttk.Checkbutton(main, text="Run StimulusFingerprint after media generation", variable=bools["run_fingerprint"]).grid(row=r, column=1, columnspan=2, sticky="w", padx=5, pady=2); r += 1
    ttk.Checkbutton(main, text="Overwrite outputs inside the new output folder if needed", variable=bools["overwrite"]).grid(row=r, column=1, columnspan=2, sticky="w", padx=5, pady=2); r += 1

    status_var = tk.StringVar(value="Ready. Select a master MP4 and output folder, then click Run.")
    ttk.Label(main, textvariable=status_var, foreground="#003366").grid(row=r, column=0, columnspan=4, sticky="we", padx=0, pady=(6, 4)); r += 1

    log_frame = ttk.Frame(main)
    log_frame.grid(row=r, column=0, columnspan=4, sticky="nsew", pady=(4, 8)); r += 1
    log = tk.Text(log_frame, height=12, width=118, wrap="word", state="disabled")
    yscroll = ttk.Scrollbar(log_frame, orient="vertical", command=log.yview)
    log.configure(yscrollcommand=yscroll.set)
    log.pack(side="left", fill="both", expand=True)
    yscroll.pack(side="right", fill="y")

    main.grid_columnconfigure(1, weight=1)
    main.grid_rowconfigure(r-1, weight=1)

    def progress(msg: str):
        enqueue("log", msg)
        enqueue("status", msg[:160])

    def build_args_from_gui() -> argparse.Namespace:
        ns = build_arg_parser().parse_args([])
        ns.no_gui = False
        ns.master = vars["master"].get().strip()
        ns.out_root = vars["out_root"].get().strip()
        ns.project_name = vars["project_name"].get().strip()
        if not ns.master:
            raise ValueError("Select a Master MP4 first.")
        if not Path(ns.master).exists():
            raise FileNotFoundError(f"Master MP4 not found: {ns.master}")
        if not ns.out_root:
            raise ValueError("Select an output root folder.")
        ns.seed = int(vars["seed"].get().strip())
        ns.start_delay = float(vars["start_delay"].get().strip())
        ns.cue_interval = float(vars["cue_interval"].get().strip())
        ns.cue_duration = float(vars["cue_duration"].get().strip())
        ns.min_value = int(vars["min_value"].get().strip())
        ns.max_value = int(vars["max_value"].get().strip())
        ns.position = vars["position"].get().strip()
        ns.badge_alpha = float(vars["badge_alpha"].get().strip())
        ns.font_scale_factor = float(vars["font_scale_factor"].get().strip())
        ns.scramble_contrast_strength = float(vars["scramble_contrast_strength"].get().strip())
        ns.control_audio_mode = vars["control_audio_mode"].get().strip()
        ns.audio_envelope_sec = float(vars["audio_envelope_sec"].get().strip())
        ns.control_audio_fps = int(vars["control_audio_fps"].get().strip())
        ns.clean_visual_mask = bool(bools["clean_visual_mask"].get())
        ns.mask_preset = vars["mask_preset"].get().strip()
        ns.mask_method = vars["mask_method"].get().strip()
        coords = [int(x.strip()) for x in vars["mask_coords"].get().split(",") if x.strip()]
        while len(coords) < 4:
            coords.append(0)
        ns.mask_x1, ns.mask_y1, ns.mask_x2, ns.mask_y2 = coords[:4]
        ns.mask_fill_rgb = vars["mask_fill_rgb"].get().strip()
        ns.overwrite = bool(bools["overwrite"].get())
        ns.run_fingerprint = bool(bools["run_fingerprint"].get())
        ns.make_control = bool(bools["make_control"].get())
        ns.fingerprint_sample_fps = float(vars["fingerprint_sample_fps"].get().strip())
        ns.fingerprint_resize_width = int(vars["fingerprint_resize_width"].get().strip())
        ns.sensor_timing_enabled = bool(bools["sensor_timing_enabled"].get())
        ns.sensor_position = vars["sensor_position"].get().strip()
        ns.sensor_pulse_mode = vars["sensor_pulse_mode"].get().strip()
        ns.sensor_video_start_duration = float(vars["sensor_video_start_duration"].get().strip())
        ns.sensor_fullscreen_black_guard = float(vars["sensor_fullscreen_black_guard"].get().strip())
        ns.sensor_cue_pulse_duration = float(vars["sensor_cue_pulse_duration"].get().strip())
        ns.sensor_size_px = int(vars["sensor_size_px"].get().strip())
        ns.sensor_size_frac = float(vars["sensor_size_frac"].get().strip())
        ns.sensor_margin_px = int(vars["sensor_margin_px"].get().strip())
        ns.sensor_idle_level = 0
        ns.sensor_pulse_level = 255
        ms = vars["max_seconds"].get().strip()
        ns.max_seconds = float(ms) if ms else None
        return ns

    def validate_inputs(show_success: bool = True) -> Optional[argparse.Namespace]:
        try:
            ns = build_args_from_gui()
            out_root = Path(ns.out_root).expanduser()
            out_root.mkdir(parents=True, exist_ok=True)
            if show_success:
                messagebox.showinfo("Inputs valid", "Inputs look valid. You can run the media suite.")
            enqueue("log", f"VALIDATED: master={ns.master}")
            enqueue("log", f"VALIDATED: output root={ns.out_root}")
            return ns
        except Exception as e:
            err = str(e)
            enqueue("log", "INPUT VALIDATION ERROR:\n" + traceback.format_exc())
            messagebox.showerror("Input validation error", err)
            return None

    def write_crash_file(ns: Optional[argparse.Namespace], tb: str) -> Optional[Path]:
        try:
            out_root = Path((ns.out_root if ns is not None else vars["out_root"].get().strip()) or Path.cwd()).expanduser()
            out_root.mkdir(parents=True, exist_ok=True)
            crash = out_root / f"PRAYCG_MediaPrep_v1_6S_CRASH_{_dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            crash.write_text(tb, encoding="utf-8")
            return crash
        except Exception:
            return None

    def worker(ns: argparse.Namespace) -> None:
        try:
            progress("RUN BUTTON CLICK CONFIRMED. MediaPrep worker started.")
            out = run_media_prep(ns, progress_cb=progress)
            state["last_output"] = str(out)
            enqueue("done", f"Media prep complete.\n\nOutput folder:\n{out}")
        except Exception as exc:
            tb = traceback.format_exc()
            crash = write_crash_file(ns, tb)
            enqueue("log", tb)
            if crash:
                enqueue("log", f"Crash log written to: {crash}")
                enqueue("error", f"{exc}\n\nCrash log written to:\n{crash}")
            else:
                enqueue("error", str(exc))

    def on_run() -> None:
        if state.get("running"):
            messagebox.showwarning("Already running", "MediaPrep is already running.")
            return
        log.configure(state="normal")
        log.delete("1.0", "end")
        log.configure(state="disabled")
        enqueue("log", "RUN BUTTON CLICKED.")
        ns = validate_inputs(show_success=False)
        if ns is None:
            return
        state["running"] = True
        run_btn.configure(state="disabled")
        open_btn.configure(state="disabled")
        status_var.set("Running media-prep suite...")
        threading.Thread(target=worker, args=(ns,), daemon=True).start()

    def open_last_output() -> None:
        folder = state.get("last_output")
        if not folder:
            return
        try:
            if sys.platform.startswith("win"):
                os.startfile(folder)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.run(["open", folder], check=False)
            else:
                subprocess.run(["xdg-open", folder], check=False)
        except Exception as exc:
            messagebox.showerror("Open folder error", str(exc))

    btn_frame = ttk.Frame(main)
    btn_frame.grid(row=r, column=0, columnspan=4, sticky="we", pady=(2, 10)); r += 1
    ttk.Button(btn_frame, text="Validate Inputs", command=lambda: validate_inputs(show_success=True)).pack(side="left", padx=(0, 8))
    run_btn = ttk.Button(btn_frame, text="Run Stimulus Media Suite v1.6S", command=on_run)
    run_btn.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=6)
    open_btn = ttk.Button(btn_frame, text="Open Last Output Folder", command=open_last_output, state="disabled")
    open_btn.pack(side="left")

    ttk.Label(main, text="Workflow: optional cleanup -> number-cued Target/Override -> phase-scrambled Control -> optional ALS fullscreen start pulse or legacy square on all branches.", anchor="w").grid(row=r, column=0, columnspan=4, sticky="w")

    poll_queue()
    root.mainloop()

def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    if args.no_gui:
        if not args.master:
            parser.error("--master is required with --no-gui")
        run_media_prep(args, progress_cb=lambda m: print(m, flush=True))
    else:
        launch_gui(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
