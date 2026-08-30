#!/usr/bin/env python3
"""
PRAYCG Master Comprehensive Post-Processing Suite v1.4.3
======================================================

A GUI + command-line post-processing suite for PR-AYC-G datasets.

Core design goals:
- One entry point for the standard PR-AYC-G post-processing suite.
- Select an XDF, optional local event log, channel map, cue schedule, stimulus QC folder,
  stimulus style, and desired modules.
- Generate a structured output folder with tables, figures, logs, config, and a Markdown/HTML report.
- Be honest when streams, markers, channel maps, or data quality are insufficient.

This script is designed as a practical research tool, not as a claim generator. It can produce
exploratory endpoint summaries and sensitivity checks; it cannot prove meaning, consciousness,
clinical efficacy, or a hidden mechanism.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import math
import os
import re
import shutil
import sys
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple

# Optional GUI imports. The CLI still works if tkinter is unavailable.
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    TK_AVAILABLE = True
except Exception:  # pragma: no cover
    TK_AVAILABLE = False

# Scientific stack. Imported lazily in many functions, but these are normal requirements.
try:
    import numpy as np
    import pandas as pd
    from scipy import signal, stats, optimize
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    SCI_AVAILABLE = True
except Exception:  # pragma: no cover
    SCI_AVAILABLE = False

try:
    import pyxdf  # type: ignore
    PYXDF_AVAILABLE = True
except Exception:  # pragma: no cover
    PYXDF_AVAILABLE = False




# NumPy compatibility: np.trapz was deprecated in NumPy 2.0 and removed in later 2.x releases.
# Use np.trapezoid when available, falling back to np.trapz for older NumPy builds.
def integrate_trapezoid(y, x=None, dx=1.0, axis=-1):
    if not SCI_AVAILABLE:
        raise RuntimeError("Scientific Python stack unavailable; cannot integrate band power.")
    if hasattr(np, "trapezoid"):
        return np.trapezoid(y, x=x, dx=dx, axis=axis)
    return np.trapz(y, x=x, dx=dx, axis=axis)  # type: ignore[attr-defined]

VERSION = "1.4.3"
SUITE_NAME = "PRAYCG_Master_Comprehensive_Suite"

DEFAULT_MODULES = {
    "stream_inventory": True,
    "marker_validation": True,
    "channel_map_validation": True,
    "cue_schedule_validation": True,
    "override_task_scoring": True,
    "self_report_summary": True,
    "report_input_artifact_handling": True,
    "eeg_qc": True,
    "mapped_lower_gamma": True,
    "residualized_lower_gamma": True,
    "gammascalpel": True,
    "task_lock_plv": True,
    "pac_exploratory": False,
    "autonomic_api": True,
    "respiration_summary": True,
    "formal_pncc_theta": True,
    "tau_coh_theta": True,
    "surrogate_theta_carryover": True,
    "post_meaning_cascade": True,
    "temporal_semantic_proxy": True,
    "postpeak_pncc_theta": True,
    "annotation_locked_theta_carryover": True,
    "gamma_to_theta_handoff": True,
    "temporal_semantic_proxy_to_theta_handoff": True,
    "thresholded_state_update": True,
    "state_locked_handoff_alignment": True,
    "human_translation_kht": True,
    "candidate_local_kht": True,
    "meaning_recognition_encoding_dissociation": True,
    "media_covariate_inventory": True,
    "constrained_dtw_exploratory": False,
    "stimulus_style_windows": True,
    "master_endpoint_table": True,
    "figures": True,
}

STIMULUS_STYLES = [
    "delayed_reveal",             # Kiwi, Snack Attack, The Present-like terminal reveal / afterglow
    "steady_load_with_climax",    # In a Heartbeat, FreeBird-like steady meaning with a climax
    "sustained_early_peak",       # Arrival-like: strong early sustained meaning that tapers before formal washout
    "dark_valence_threat_reveal", # Tuck Me In-like threat/dread reveal
    "sustained_steady",           # sustained meaning throughout
    "weak_or_ambiguous",          # methods/shakedown or low meaning
    "custom",
]

PRAYCG16_FIXED_MAP = [
    (1, "Fz", "frontal_analytic_lock"),
    (2, "Cz", "central_anchor"),
    (3, "Pz", "parietal_integration"),
    (4, "F3", "left_frontal"),
    (5, "F4", "right_frontal"),
    (6, "C3", "left_central"),
    (7, "C4", "right_central"),
    (8, "P3", "left_parietal"),
    (9, "P4", "right_parietal"),
    (10, "T5", "left_posterior_temporal"),
    (11, "T6", "right_posterior_temporal"),
    (12, "O1", "left_visual_control"),
    (13, "O2", "right_visual_control"),
    (14, "T3", "left_jaw_temporal_sentinel"),
    (15, "T4", "right_jaw_temporal_sentinel"),
    (16, "Fp1", "blink_eye_sentinel"),
]

MARKIV_DEFAULT_MAP = [
    (1, "Fp1", "left_prefrontal_eye_sentinel"),
    (2, "Fp2", "right_prefrontal_eye_sentinel"),
    (3, "C3", "left_central"),
    (4, "C4", "right_central"),
    (5, "P7", "left_posterior_temporal"),
    (6, "P8", "right_posterior_temporal"),
    (7, "O1", "left_visual_control"),
    (8, "O2", "right_visual_control"),
    (9, "F7", "left_frontal_lateral"),
    (10, "F8", "right_frontal_lateral"),
    (11, "F3", "left_frontal"),
    (12, "F4", "right_frontal"),
    (13, "T7", "left_jaw_temporal_sentinel"),
    (14, "T8", "right_jaw_temporal_sentinel"),
    (15, "P3", "left_parietal"),
    (16, "P4", "right_parietal"),
]

BANDS = {
    "theta_4_8": (4.0, 8.0),
    "alpha_8_12": (8.0, 12.0),
    "lgamma_30_45": (30.0, 45.0),
    "g30_35": (30.0, 35.0),
    "g35_40": (35.0, 40.0),
    "g40_45": (40.0, 45.0),
    "hf_proxy_45_55": (45.0, 55.0),
}


@dataclass
class SuiteConfig:
    project_name: str = "PRAYCG_Run"
    xdf_path: str = ""
    event_log_path: str = ""
    channel_map_path: str = ""
    cue_schedule_json: str = ""
    cue_schedule_csv: str = ""
    stimulus_fingerprint_folder: str = ""
    annotation_csv: str = ""
    feature_table_path: str = ""
    media_manifest_json: str = ""
    predeclared_anchor_file: str = ""
    mred_familiarity_csv: str = ""
    mred_scene_map_csv: str = ""
    out_root: str = "outputs"
    stimulus_style: str = "delayed_reveal"
    channel_map_preset: str = "PRAYCG16_FIXED_ORDER_v1"
    channel_map_confidence: str = "LOCKED"
    preferred_marker_source: str = "auto"  # auto, xdf, event_log
    line_frequency_hz: float = 60.0
    eeg_window_sec: float = 2.0
    eeg_step_sec: float = 1.0
    report_prepad_sec: float = 3.0
    report_postpad_sec: float = 5.0
    washout_start_trim_sec: float = 2.0
    washout_end_trim_sec: float = 3.0
    reveal_windows_sec: str = "20,30,40,60,90"
    washout_splits_sec: str = "0-30,30-90,90-120"
    n_surrogates: int = 500
    random_seed: int = 20260724
    make_html: bool = True
    overwrite: bool = False
    modules: Dict[str, bool] = None  # type: ignore

    def __post_init__(self):
        if self.modules is None:
            self.modules = dict(DEFAULT_MODULES)


def sanitize_name(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_.-]+", "_", (s or "PRAYCG_Run").strip())
    return s.strip("_") or "PRAYCG_Run"


def now_stamp() -> str:
    return _dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def parse_num_list(text: str, default: Sequence[float]) -> List[float]:
    vals = []
    for part in (text or "").split(','):
        part = part.strip()
        if not part:
            continue
        try:
            vals.append(float(part))
        except Exception:
            pass
    return vals or list(default)


def parse_ranges(text: str, default: Sequence[Tuple[float, float]]) -> List[Tuple[float, float]]:
    vals = []
    for part in (text or "").split(','):
        part = part.strip()
        m = re.match(r"^([0-9.]+)\s*-\s*([0-9.]+)$", part)
        if m:
            vals.append((float(m.group(1)), float(m.group(2))))
    return vals or list(default)


def safe_json_dump(obj: Any, path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, default=str)


def read_json_maybe(path: str) -> Any:
    if not path or not Path(path).exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def zscore_series(x: "pd.Series") -> "pd.Series":
    mu = x.mean(skipna=True)
    sd = x.std(skipna=True)
    if not np.isfinite(sd) or sd == 0:
        return x * 0.0
    return (x - mu) / sd


def overlap(a0: float, a1: float, b0: float, b1: float) -> bool:
    return max(a0, b0) < min(a1, b1)


class RunLogger:
    def __init__(self, log_path: Path, progress_cb: Optional[Callable[[str], None]] = None):
        self.log_path = log_path
        self.progress_cb = progress_cb
        ensure_dir(log_path.parent)
        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write(f"{SUITE_NAME} v{VERSION} log started {now_stamp()}\n")

    def __call__(self, msg: str) -> None:
        line = f"[{_dt.datetime.now().strftime('%H:%M:%S')}] {msg}"
        print(line)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        if self.progress_cb:
            try:
                self.progress_cb(msg)
            except Exception:
                pass


# ---------------------------
# Loading streams and events
# ---------------------------

def load_xdf_streams(xdf_path: str, logger: RunLogger) -> Tuple[List[dict], dict]:
    if not xdf_path:
        logger("No XDF path supplied.")
        return [], {}
    if not PYXDF_AVAILABLE:
        raise RuntimeError("pyxdf is not installed. Install requirements_master_suite_v1_0.txt.")
    logger(f"Loading XDF: {xdf_path}")
    streams, header = pyxdf.load_xdf(xdf_path)  # type: ignore
    logger(f"Loaded {len(streams)} XDF streams.")
    return streams, header


def stream_name(s: dict) -> str:
    try:
        return s.get("info", {}).get("name", [""])[0]
    except Exception:
        return ""


def stream_type(s: dict) -> str:
    try:
        return s.get("info", {}).get("type", [""])[0]
    except Exception:
        return ""


def stream_channel_count(s: dict) -> int:
    try:
        return int(s.get("info", {}).get("channel_count", [0])[0])
    except Exception:
        try:
            arr = np.asarray(s.get("time_series", []))
            return 1 if arr.ndim == 1 else arr.shape[1]
        except Exception:
            return 0


def effective_fs(ts: np.ndarray) -> float:
    ts = np.asarray(ts, dtype=float)
    if len(ts) < 3:
        return float("nan")
    diffs = np.diff(ts)
    diffs = diffs[np.isfinite(diffs) & (diffs > 0)]
    if len(diffs) == 0:
        return float("nan")
    return float(1.0 / np.median(diffs))


def create_stream_inventory(streams: List[dict], out: Path) -> "pd.DataFrame":
    rows = []
    for i, s in enumerate(streams):
        ts = np.asarray(s.get("time_stamps", []), dtype=float)
        arr = np.asarray(s.get("time_series", []), dtype=object)
        rows.append({
            "stream_index": i,
            "name": stream_name(s),
            "type": stream_type(s),
            "channel_count": stream_channel_count(s),
            "sample_count": len(ts),
            "effective_srate_hz": effective_fs(ts),
            "first_timestamp": float(ts[0]) if len(ts) else np.nan,
            "last_timestamp": float(ts[-1]) if len(ts) else np.nan,
            "duration_sec": float(ts[-1] - ts[0]) if len(ts) > 1 else np.nan,
            "time_series_shape": str(arr.shape),
        })
    df = pd.DataFrame(rows)
    df.to_csv(out / "tables" / "stream_inventory.csv", index=False)
    return df


def choose_eeg_stream(streams: List[dict]) -> Optional[dict]:
    candidates = []
    for s in streams:
        name = stream_name(s).lower()
        typ = stream_type(s).lower()
        nchan = stream_channel_count(s)
        if ("eeg" in typ or "eeg" in name or "obci" in name or "openbci" in name) and nchan >= 2:
            candidates.append(s)
    if candidates:
        # prefer 16+ channel stream
        candidates.sort(key=lambda s: stream_channel_count(s), reverse=True)
        return candidates[0]
    return None


def choose_stream_by_keywords(streams: List[dict], keywords: Sequence[str]) -> Optional[dict]:
    keys = [k.lower() for k in keywords]
    for s in streams:
        name = stream_name(s).lower()
        typ = stream_type(s).lower()
        text = name + " " + typ
        if any(k in text for k in keys):
            return s
    return None


def extract_markers_from_xdf(streams: List[dict]) -> "pd.DataFrame":
    rows = []
    for s in streams:
        name = stream_name(s)
        typ = stream_type(s)
        if "marker" not in name.lower() and "marker" not in typ.lower() and name != "StasisMarkers":
            continue
        ts = np.asarray(s.get("time_stamps", []), dtype=float)
        series = s.get("time_series", [])
        for t, val in zip(ts, series):
            if isinstance(val, (list, tuple, np.ndarray)):
                marker = str(val[0]) if len(val) else ""
            else:
                marker = str(val)
            rows.append({"marker": marker, "lsl_time": float(t), "phase": "", "note": "", "source": f"xdf:{name}"})
    return pd.DataFrame(rows).sort_values("lsl_time").reset_index(drop=True) if rows else pd.DataFrame(columns=["marker","lsl_time","phase","note","source"])


def load_event_log(path: str) -> "pd.DataFrame":
    if not path or not Path(path).exists():
        return pd.DataFrame(columns=["marker","lsl_time","phase","note","source"])
    p = Path(path)
    rows: List[dict] = []
    if p.suffix.lower() == ".json":
        data = read_json_maybe(str(p))
        if isinstance(data, dict) and "events" in data:
            data = data["events"]
        if isinstance(data, list):
            for e in data:
                if not isinstance(e, dict):
                    continue
                rows.append({
                    "marker": str(e.get("marker", "")),
                    "lsl_time": float(e.get("lsl_time", np.nan)),
                    "unix_time": e.get("unix_time", np.nan),
                    "psychopy_time": e.get("psychopy_time", np.nan),
                    "phase": str(e.get("phase", "")),
                    "note": str(e.get("note", "")),
                    "source": "event_log_json",
                })
    elif p.suffix.lower() == ".csv":
        df = pd.read_csv(p)
        for _, r in df.iterrows():
            rows.append({
                "marker": str(r.get("marker", "")),
                "lsl_time": float(r.get("lsl_time", np.nan)),
                "unix_time": r.get("unix_time", np.nan),
                "psychopy_time": r.get("psychopy_time", np.nan),
                "phase": str(r.get("phase", "")),
                "note": str(r.get("note", "")),
                "source": "event_log_csv",
            })
    out = pd.DataFrame(rows)
    if len(out):
        out = out[np.isfinite(out["lsl_time"].astype(float))].sort_values("lsl_time").reset_index(drop=True)
    return out


def select_event_source(xdf_events: "pd.DataFrame", log_events: "pd.DataFrame", preferred: str, logger: RunLogger) -> "pd.DataFrame":
    preferred = (preferred or "auto").lower()
    if preferred == "xdf" and len(xdf_events):
        logger("Using XDF-native marker stream for segmentation.")
        return xdf_events.copy()
    if preferred == "event_log" and len(log_events):
        logger("Using local event log for segmentation.")
        return log_events.copy()
    if len(xdf_events):
        logger("Using XDF-native marker stream for segmentation (auto).")
        return xdf_events.copy()
    if len(log_events):
        logger("XDF marker stream unavailable; using local event log for segmentation (auto).")
        return log_events.copy()
    logger("No markers found in XDF or local event log.")
    return pd.DataFrame(columns=["marker","lsl_time","phase","note","source"])


def find_marker_time(events: "pd.DataFrame", marker: str) -> Optional[float]:
    if events is None or len(events) == 0:
        return None
    m = events[events["marker"] == marker]
    if len(m):
        return float(m.iloc[0]["lsl_time"])
    return None


def build_segments(events: "pd.DataFrame", out: Path, cfg: SuiteConfig, logger: RunLogger) -> "pd.DataFrame":
    phases = ["BASELINE_1", "CONTROL_1", "WASHOUT_1", "TARGET_1", "WASHOUT_2", "CONTEXTUAL_OVERRIDE_1", "WASHOUT_3"]
    rows = []
    for ph in phases:
        start = find_marker_time(events, f"{ph}_START")
        end = None
        # For videos, timeout break is often closer to true media endpoint than END marker.
        if ph in ["CONTROL_1", "TARGET_1", "CONTEXTUAL_OVERRIDE_1"]:
            end = find_marker_time(events, f"{ph}_TIMEOUT_BREAK") or find_marker_time(events, f"{ph}_END")
        else:
            end = find_marker_time(events, f"{ph}_END")
        if start is not None and end is not None and end > start:
            rows.append({"segment": ph, "start": start, "end": end, "duration_sec": end - start, "segment_type": "core"})
        else:
            rows.append({"segment": ph, "start": start, "end": end, "duration_sec": np.nan, "segment_type": "missing"})
    seg = pd.DataFrame(rows)

    # Add style-specific subwindows.
    reveal_windows = parse_num_list(cfg.reveal_windows_sec, [20, 30, 40, 60, 90])
    for base in ["CONTROL_1", "TARGET_1", "CONTEXTUAL_OVERRIDE_1"]:
        rr = seg[seg["segment"] == base]
        if not len(rr) or not pd.notna(rr.iloc[0]["start"]) or not pd.notna(rr.iloc[0]["end"]):
            continue
        s0, s1 = float(rr.iloc[0]["start"]), float(rr.iloc[0]["end"])
        dur = s1 - s0
        max_rev = min(max(reveal_windows), max(1.0, dur - 1.0)) if reveal_windows else 40.0
        early_end = max(s0, s1 - max_rev)
        if early_end > s0 + 5:
            rows.append({"segment": f"{base}_EARLY_EXCL_LAST_{int(max_rev)}S", "start": s0, "end": early_end, "duration_sec": early_end - s0, "segment_type": "stimulus_style"})
        for rw in reveal_windows:
            if dur > rw + 1:
                rows.append({"segment": f"{base}_FINAL_{int(rw)}S", "start": s1 - rw, "end": s1, "duration_sec": rw, "segment_type": "stimulus_style"})

    # Add washout split windows.
    wash_splits = parse_ranges(cfg.washout_splits_sec, [(0,30),(30,90),(90,120)])
    for base in ["WASHOUT_1", "WASHOUT_2", "WASHOUT_3"]:
        rr = seg[seg["segment"] == base]
        if not len(rr) or not pd.notna(rr.iloc[0]["start"]) or not pd.notna(rr.iloc[0]["end"]):
            continue
        s0, s1 = float(rr.iloc[0]["start"]), float(rr.iloc[0]["end"])
        for a, b in wash_splits:
            w0 = s0 + a
            w1 = min(s0 + b, s1)
            if w1 > w0 + 2:
                rows.append({"segment": f"{base}_{int(a)}_{int(b)}S", "start": w0, "end": w1, "duration_sec": w1 - w0, "segment_type": "washout_split"})
    allseg = pd.DataFrame(rows)
    allseg.to_csv(out / "tables" / "segments_used.csv", index=False)
    logger(f"Built {len(allseg)} segment/windows.")
    return allseg


# ---------------------------
# Channel maps and ROIs
# ---------------------------

def built_in_channel_map(preset: str, nchan: int) -> "pd.DataFrame":
    preset_l = (preset or "").lower()
    if "markiv" in preset_l:
        base = MARKIV_DEFAULT_MAP
        label = "OpenBCI_MarkIV_Default_16"
    elif "anonymous" in preset_l:
        base = [(i+1, f"Ch{i+1:02d}", "anonymous") for i in range(nchan)]
        label = "anonymous"
    else:
        base = PRAYCG16_FIXED_MAP
        label = "PRAYCG16_FIXED_ORDER_v1"
    rows = []
    for ch, elec, roi in base[:nchan]:
        rows.append({"channel": ch, "zero_index": ch-1, "electrode": elec, "roi_label": roi, "map_label": label})
    return pd.DataFrame(rows)


def load_channel_map(cfg: SuiteConfig, nchan: int, out: Path, logger: RunLogger) -> "pd.DataFrame":
    if cfg.channel_map_path and Path(cfg.channel_map_path).exists():
        df = pd.read_csv(cfg.channel_map_path)
        # Try to standardize column names.
        cols = {c.lower(): c for c in df.columns}
        ch_col = cols.get("channel") or cols.get("openbci_channel") or cols.get("pin")
        el_col = cols.get("electrode") or cols.get("electrode_location") or cols.get("location")
        roi_col = cols.get("roi") or cols.get("roi_label")
        rows = []
        for _, r in df.iterrows():
            ch = int(r[ch_col]) if ch_col else len(rows)+1
            elec = str(r[el_col]) if el_col else f"Ch{ch:02d}"
            roi = str(r[roi_col]) if roi_col else "custom"
            rows.append({"channel": ch, "zero_index": ch-1, "electrode": elec, "roi_label": roi, "map_label": "custom_csv"})
        cmap = pd.DataFrame(rows)
        logger(f"Loaded custom channel map CSV with {len(cmap)} entries.")
    else:
        cmap = built_in_channel_map(cfg.channel_map_preset, nchan)
        logger(f"Using built-in channel map preset: {cfg.channel_map_preset}")
    if len(cmap) < nchan:
        for ch in range(len(cmap)+1, nchan+1):
            cmap.loc[len(cmap)] = {"channel": ch, "zero_index": ch-1, "electrode": f"Ch{ch:02d}", "roi_label": "unmapped", "map_label": "padded"}
    cmap = cmap.iloc[:nchan].copy()
    cmap["confidence"] = cfg.channel_map_confidence
    cmap.to_csv(out / "tables" / "channel_map_used.csv", index=False)
    return cmap


def roi_sets(cmap: "pd.DataFrame") -> Dict[str, List[int]]:
    electrodes = {str(r["electrode"]): int(r["zero_index"]) for _, r in cmap.iterrows()}
    has = set(electrodes.keys())
    def idx(names: Sequence[str]) -> List[int]:
        return [electrodes[n] for n in names if n in electrodes]
    if {"Fz", "Cz", "Pz", "T5", "T6"}.intersection(has):
        return {
            "frontoparietal_task": idx(["Fz","F3","F4","Pz","P3","P4"]),
            "meaning_candidate": idx(["Cz","C3","C4","T5","T6"]),
            "central": idx(["Cz","C3","C4"]),
            "parietal": idx(["Pz","P3","P4"]),
            "posterior_temporal": idx(["T5","T6"]),
            "visual_control": idx(["O1","O2"]),
            "artifact_sentinel": idx(["Fp1","T3","T4"]),
            "jaw_temporal_sentinel": idx(["T3","T4"]),
            "primary_content_core": idx(["Fz","Cz","Pz","C3","C4","P3","P4","T5","T6"]),
            "all_channels": list(cmap["zero_index"].astype(int)),
        }
    if {"P7", "P8", "T7", "T8"}.intersection(has):
        return {
            "frontoparietal_task": idx(["F3","F4","F7","F8","P3","P4"]),
            "meaning_candidate": idx(["C3","C4","P7","P8"]),
            "central": idx(["C3","C4"]),
            "parietal": idx(["P3","P4"]),
            "posterior_temporal": idx(["P7","P8"]),
            "visual_control": idx(["O1","O2"]),
            "artifact_sentinel": idx(["Fp1","Fp2","T7","T8"]),
            "jaw_temporal_sentinel": idx(["T7","T8"]),
            "primary_content_core": idx(["C3","C4","P7","P8","F3","F4","P3","P4"]),
            "all_channels": list(cmap["zero_index"].astype(int)),
        }
    return {"all_channels": list(cmap["zero_index"].astype(int))}


# ---------------------------
# Ratings, cue schedule, exclusions
# ---------------------------

def parse_ratings(events: "pd.DataFrame", out: Path) -> Tuple["pd.DataFrame", "pd.DataFrame"]:
    rows = []
    pat = re.compile(r"^RATING_(.+)_([A-Za-z0-9]+)_(-?[0-9]+(?:\.[0-9]+)?)$")
    for _, r in events.iterrows():
        marker = str(r.get("marker", ""))
        m = pat.match(marker)
        if m:
            rows.append({
                "phase": m.group(1),
                "rating_name": m.group(2),
                "rating_value": float(m.group(3)),
                "lsl_time": float(r.get("lsl_time", np.nan)),
            })
    long = pd.DataFrame(rows)
    if len(long):
        wide = long.pivot_table(index="phase", columns="rating_name", values="rating_value", aggfunc="last").reset_index()
    else:
        wide = pd.DataFrame()
    long.to_csv(out / "tables" / "self_report_ratings_long.csv", index=False)
    wide.to_csv(out / "tables" / "self_report_ratings_wide.csv", index=False)
    return long, wide



def _as_dict(obj: Any) -> Dict[str, Any]:
    """Return obj if it is a dict; otherwise return an empty dict.

    This prevents the common Windows/JSON failure mode where a file path string,
    missing optional object, or CSV row is accidentally treated like a dictionary.
    """
    return obj if isinstance(obj, dict) else {}


def _as_list(obj: Any) -> List[Any]:
    if isinstance(obj, list):
        return obj
    if obj is None:
        return []
    return [obj]


def safe_get(obj: Any, key: str, default: Any = None) -> Any:
    return obj.get(key, default) if isinstance(obj, dict) else default


def first_present(obj: Any, paths: Sequence[Sequence[str]], default: Any = None) -> Any:
    """Safely read the first present nested value from a dict-like object."""
    for path in paths:
        cur: Any = obj
        ok = True
        for key in path:
            if not isinstance(cur, dict) or key not in cur:
                ok = False
                break
            cur = cur[key]
        if ok and cur not in (None, ""):
            return cur
    return default


def normalize_cue_schedule(raw: Any) -> Dict[str, Any]:
    """Normalize cue schedules across v1.6H/M/N/O/P/Q schemas.

    Fixes the observed '.get' failure class by never assuming that optional
    nested entries such as outputs/sha256/cue_design are dicts. It also supports
    both legacy top-level keys and newer MediaPrep-style nested manifest keys.
    """
    cue = _as_dict(raw)
    video = _as_dict(cue.get("video")) or _as_dict(cue.get("video_props"))
    cue_design = _as_dict(cue.get("cue_design"))
    cue_events = _as_list(cue.get("cue_events"))
    out = {
        "schema": safe_get(cue, "schema", "unknown"),
        "created_utc": safe_get(cue, "created_utc", ""),
        "cue_count": safe_get(cue, "cue_count", len(cue_events)),
        "expected_sum": safe_get(cue, "expected_sum", None),
        "output_cued_video": first_present(cue, [["output_cued_video"], ["outputs", "target_cued"], ["outputs", "output_cued_video"]], ""),
        "output_override_video": first_present(cue, [["output_override_video"], ["outputs", "override_cued"], ["outputs", "output_override_video"]], ""),
        "output_cued_sha256": first_present(cue, [["output_cued_sha256"], ["sha256", "target_cued"], ["sha256", "output_cued_sha256"]], ""),
        "output_override_sha256": first_present(cue, [["output_override_sha256"], ["sha256", "override_cued"], ["sha256", "output_override_sha256"]], ""),
        "control_phase_scrambled": first_present(cue, [["outputs", "control_phase_scrambled"], ["control_phase_scrambled"]], ""),
        "fps": safe_get(video, "fps", np.nan),
        "duration_sec": safe_get(video, "duration_sec", np.nan),
        "width": safe_get(video, "width", None),
        "height": safe_get(video, "height", None),
        "cue_interval_sec": safe_get(cue_design, "interval_sec", None),
        "cue_display_duration_sec": safe_get(cue_design, "display_duration_sec", None),
        "cue_position": safe_get(cue_design, "position", ""),
        "contrast_protected_badge": safe_get(cue_design, "contrast_protected_badge", None),
        "cue_events": cue_events,
    }
    if out["expected_sum"] is None and cue_events:
        vals = []
        for ev in cue_events:
            if isinstance(ev, dict) and "value" in ev:
                try:
                    vals.append(float(ev["value"]))
                except Exception:
                    pass
        if vals:
            out["expected_sum"] = int(sum(vals))
    if not out["cue_count"] and cue_events:
        out["cue_count"] = len(cue_events)
    return out


def normalize_media_manifest(raw: Any) -> Dict[str, Any]:
    m = _as_dict(raw)
    return {
        "schema": safe_get(m, "schema", "unknown"),
        "project_name": safe_get(m, "project_name", ""),
        "target_cued": first_present(m, [["outputs", "target_cued"], ["output_cued_video"]], ""),
        "override_cued": first_present(m, [["outputs", "override_cued"], ["output_override_video"]], ""),
        "control_phase_scrambled": first_present(m, [["outputs", "control_phase_scrambled"], ["control_phase_scrambled"]], ""),
        "target_cued_sha256": first_present(m, [["sha256", "target_cued"], ["output_cued_sha256"]], ""),
        "override_cued_sha256": first_present(m, [["sha256", "override_cued"], ["output_override_sha256"]], ""),
        "control_sha256": first_present(m, [["sha256", "control_phase_scrambled"]], ""),
        "control_audio_mode": first_present(m, [["control_audio", "mode"]], ""),
    }


def load_cue_schedule(cfg: SuiteConfig, out: Path, events: "pd.DataFrame") -> Tuple[Dict[str, Any], "pd.DataFrame"]:
    raw = read_json_maybe(cfg.cue_schedule_json) or {}
    cue = normalize_cue_schedule(raw)
    if cfg.media_manifest_json and Path(cfg.media_manifest_json).exists():
        manifest = normalize_media_manifest(read_json_maybe(cfg.media_manifest_json) or {})
        if not cue.get("output_cued_video"):
            cue["output_cued_video"] = manifest.get("target_cued", "")
        if not cue.get("output_override_video"):
            cue["output_override_video"] = manifest.get("override_cued", "")
        if not cue.get("output_cued_sha256"):
            cue["output_cued_sha256"] = manifest.get("target_cued_sha256", "")
        if not cue.get("output_override_sha256"):
            cue["output_override_sha256"] = manifest.get("override_cued_sha256", "")
        cue["media_manifest_project_name"] = manifest.get("project_name", "")
        cue["media_manifest_control_audio_mode"] = manifest.get("control_audio_mode", "")
        try:
            shutil.copy2(cfg.media_manifest_json, out / "provenance" / Path(cfg.media_manifest_json).name)
        except Exception:
            pass
    if cfg.cue_schedule_json and Path(cfg.cue_schedule_json).exists():
        try: shutil.copy2(cfg.cue_schedule_json, out / "provenance" / Path(cfg.cue_schedule_json).name)
        except Exception: pass
    if cfg.cue_schedule_csv and Path(cfg.cue_schedule_csv).exists():
        try: shutil.copy2(cfg.cue_schedule_csv, out / "provenance" / Path(cfg.cue_schedule_csv).name)
        except Exception: pass
    rows = []
    cue_pat = re.compile(r"^(TARGET_1|CONTEXTUAL_OVERRIDE_1)_CUE_(\d+)_VALUE_(-?\d+)_START")
    for _, r in events.iterrows():
        marker = str(r.get("marker", ""))
        m = cue_pat.match(marker)
        if m:
            rows.append({"phase": m.group(1), "cue_index": int(m.group(2)), "value": int(m.group(3)), "lsl_time": float(r.get("lsl_time", np.nan)), "source": r.get("source", "")})
    cue_events = pd.DataFrame(rows)
    cue_events.to_csv(out / "tables" / "cue_marker_events.csv", index=False)
    summary = {
        "cue_schedule_json": cfg.cue_schedule_json,
        "schema": cue.get("schema"),
        "cue_count_expected": cue.get("cue_count"),
        "expected_sum": cue.get("expected_sum"),
        "target_output_video": cue.get("output_cued_video"),
        "override_output_video": cue.get("output_override_video"),
        "target_output_sha256": cue.get("output_cued_sha256"),
        "override_output_sha256": cue.get("output_override_sha256"),
        "target_override_hash_match": bool(cue.get("output_cued_sha256") and cue.get("output_cued_sha256") == cue.get("output_override_sha256")),
        "cue_interval_sec": cue.get("cue_interval_sec"),
        "cue_display_duration_sec": cue.get("cue_display_duration_sec"),
        "cue_position": cue.get("cue_position"),
        "contrast_protected_badge": cue.get("contrast_protected_badge"),
        "cue_marker_count_target": int((cue_events["phase"] == "TARGET_1").sum()) if len(cue_events) else 0,
        "cue_marker_count_override": int((cue_events["phase"] == "CONTEXTUAL_OVERRIDE_1").sum()) if len(cue_events) else 0,
        "get_error_patch": "safe cue/manifest parser active; optional path strings are not treated as dicts",
    }
    pd.DataFrame([summary]).to_csv(out / "tables" / "cue_schedule_validation_summary.csv", index=False)
    return summary, cue_events

def score_override(events: "pd.DataFrame", cue_summary: Dict[str, Any], out: Path) -> "pd.DataFrame":
    expected = cue_summary.get("expected_sum")
    # Check event markers first.
    for _, r in events.iterrows():
        marker = str(r.get("marker", ""))
        m = re.match(r"^RESPONSE_CONTEXTUAL_OVERRIDE_1_EXPECTED_SUM_(-?\d+)", marker)
        if m:
            expected = int(m.group(1))
    reported = None
    for _, r in events.iterrows():
        marker = str(r.get("marker", ""))
        m = re.match(r"^RESPONSE_CONTEXTUAL_OVERRIDE_1_SUM_(-?\d+)", marker)
        if m:
            reported = int(m.group(1))
        m2 = re.match(r"^RESPONSE_CONTEXTUAL_OVERRIDE_1_(-?\d+)$", marker)
        if m2:
            reported = int(m2.group(1))
    correct = None
    if expected is not None and reported is not None:
        correct = int(int(expected) == int(reported))
    row = {
        "expected_sum": expected,
        "reported_sum": reported,
        "sum_error": (reported - expected) if expected is not None and reported is not None else np.nan,
        "abs_sum_error": abs(reported - expected) if expected is not None and reported is not None else np.nan,
        "exact_correct": correct,
        "interpretation": "not scored" if reported is None else ("exact correct" if correct else "not exact; interpret with effort/leakage/cue visibility"),
    }
    df = pd.DataFrame([row])
    df.to_csv(out / "tables" / "contextual_override_task_scoring.csv", index=False)
    return df


def build_exclusion_windows(events: "pd.DataFrame", cfg: SuiteConfig, out: Path) -> "pd.DataFrame":
    pairs = []
    markers = list(events["marker"].astype(str)) if len(events) else []
    times = list(events["lsl_time"].astype(float)) if len(events) else []

    def add_pair(start_re: str, end_re: str, label: str):
        starts = [(i, t) for i, (m, t) in enumerate(zip(markers, times)) if re.match(start_re, m)]
        ends = [(i, t) for i, (m, t) in enumerate(zip(markers, times)) if re.match(end_re, m)]
        for si, st in starts:
            et = None
            for ei, e in ends:
                if ei > si:
                    et = e
                    break
            if et is not None and et > st:
                pairs.append({"label": label, "start": st - cfg.report_prepad_sec, "end": et + cfg.report_postpad_sec, "raw_start": st, "raw_end": et, "prepad": cfg.report_prepad_sec, "postpad": cfg.report_postpad_sec})

    add_pair(r"^REPORT_INPUT_START$", r"^REPORT_INPUT_END$", "report_input")
    add_pair(r"^SUM_INPUT_START$", r"^SUM_INPUT_END$", "sum_input")
    add_pair(r"^RETURN_TO_STILLNESS_START$", r"^RETURN_TO_STILLNESS_END$", "return_to_stillness")
    add_pair(r"^RATINGS_.*_START$", r"^RATINGS_.*_END$", "ratings_input_legacy")
    add_pair(r"^RESPONSE_CONTEXTUAL_OVERRIDE_1_START$", r"^RESPONSE_CONTEXTUAL_OVERRIDE_1_END$", "sum_response_legacy")
    df = pd.DataFrame(pairs)
    if len(df):
        df = df.sort_values("start").reset_index(drop=True)
    df.to_csv(out / "tables" / "artifact_exclusion_windows.csv", index=False)
    return df


# ---------------------------
# EEG processing
# ---------------------------

def band_power_from_welch(x: np.ndarray, fs: float, band: Tuple[float, float]) -> np.ndarray:
    # x shape: samples x channels
    if x.shape[0] < 4:
        return np.full(x.shape[1], np.nan)
    nperseg = min(max(16, int(fs * 1.0)), x.shape[0])
    freqs, psd = signal.welch(x, fs=fs, axis=0, nperseg=nperseg, noverlap=nperseg//2)
    lo, hi = band
    mask = (freqs >= lo) & (freqs < hi)
    if not mask.any():
        return np.full(x.shape[1], np.nan)
    powv = integrate_trapezoid(psd[mask, :], freqs[mask], axis=0)
    return np.log10(powv + 1e-12)


def design_filter(fs: float, band: Tuple[float, float]):
    lo, hi = band
    nyq = fs / 2.0
    hi = min(hi, nyq * 0.95)
    lo = max(lo, 0.1)
    if lo >= hi:
        return None
    return signal.butter(4, [lo/nyq, hi/nyq], btype="bandpass", output="sos")


def compute_phase_amp(eeg: np.ndarray, fs: float, band: Tuple[float, float]) -> Tuple[np.ndarray, np.ndarray]:
    sos = design_filter(fs, band)
    if sos is None:
        return np.full_like(eeg, np.nan), np.full_like(eeg, np.nan)
    filt = signal.sosfiltfilt(sos, eeg, axis=0)
    analytic = signal.hilbert(filt, axis=0)
    return np.angle(analytic), np.abs(analytic)


def median_pair_plv(phases: np.ndarray, chans: List[int]) -> float:
    if len(chans) < 2:
        return np.nan
    vals = []
    for i in range(len(chans)):
        for j in range(i+1, len(chans)):
            d = phases[:, chans[i]] - phases[:, chans[j]]
            vals.append(abs(np.nanmean(np.exp(1j * d))))
    return float(np.nanmedian(vals)) if vals else np.nan


def pac_mvl(theta_phase: np.ndarray, gamma_amp: np.ndarray, chans: List[int]) -> float:
    if not chans:
        return np.nan
    vals = []
    for ch in chans:
        p = theta_phase[:, ch]
        a = gamma_amp[:, ch]
        if np.all(~np.isfinite(p)) or np.all(~np.isfinite(a)):
            continue
        vals.append(abs(np.nanmean(a * np.exp(1j * p))) / (np.nanmean(a) + 1e-12))
    return float(np.nanmedian(vals)) if vals else np.nan


def clean_window_ok(w0: float, w1: float, exclusions: "pd.DataFrame") -> bool:
    if exclusions is None or len(exclusions) == 0:
        return True
    for _, e in exclusions.iterrows():
        if overlap(w0, w1, float(e["start"]), float(e["end"])):
            return False
    return True


def extract_eeg_features(streams: List[dict], segments: "pd.DataFrame", exclusions: "pd.DataFrame", cmap: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> Tuple["pd.DataFrame", "pd.DataFrame"]:
    eeg_s = choose_eeg_stream(streams)
    if eeg_s is None:
        logger("No EEG stream found; EEG modules will be skipped.")
        return pd.DataFrame(), pd.DataFrame()
    eeg = np.asarray(eeg_s.get("time_series", []), dtype=float)
    ts = np.asarray(eeg_s.get("time_stamps", []), dtype=float)
    if eeg.ndim == 1:
        eeg = eeg[:, None]
    fs = effective_fs(ts)
    logger(f"EEG stream: {stream_name(eeg_s)} | shape={eeg.shape} | fs≈{fs:.3f} Hz")
    if not np.isfinite(fs) or fs < 20:
        logger("EEG sample rate too low/invalid; skipping EEG features.")
        return pd.DataFrame(), pd.DataFrame()

    rois = roi_sets(cmap)
    # Trim/censor windows and extract band powers.
    rows = []
    wsec = cfg.eeg_window_sec
    step = cfg.eeg_step_sec
    for _, seg in segments.iterrows():
        if not pd.notna(seg.get("start", np.nan)) or not pd.notna(seg.get("end", np.nan)):
            continue
        s0, s1 = float(seg["start"]), float(seg["end"])
        if str(seg["segment"]).startswith("WASHOUT"):
            s0 += cfg.washout_start_trim_sec
            s1 -= cfg.washout_end_trim_sec
        if s1 <= s0 + wsec:
            continue
        t = s0
        while t + wsec <= s1 + 1e-6:
            w0, w1 = t, t + wsec
            t += step
            if not clean_window_ok(w0, w1, exclusions):
                continue
            mask = (ts >= w0) & (ts < w1)
            if mask.sum() < max(8, int(fs * wsec * 0.5)):
                continue
            x = eeg[mask, :]
            x = signal.detrend(x, axis=0, type="linear")
            p2p = np.ptp(x, axis=0)
            row = {
                "segment": seg["segment"],
                "segment_type": seg.get("segment_type", ""),
                "window_start": w0,
                "window_end": w1,
                "window_mid": (w0+w1)/2,
                "n_samples": int(mask.sum()),
                "median_p2p": float(np.nanmedian(p2p)),
                "max_p2p": float(np.nanmax(p2p)),
            }
            band_chan_power: Dict[str, np.ndarray] = {}
            for bname, band in BANDS.items():
                bp = band_power_from_welch(x, fs, band)
                band_chan_power[bname] = bp
                for roi_name, chans in rois.items():
                    chans = [c for c in chans if c < len(bp)]
                    row[f"pow_{bname}_{roi_name}"] = float(np.nanmedian(bp[chans])) if chans else np.nan
            # Also save per-channel basic low gamma for QC.
            for _, cr in cmap.iterrows():
                zi = int(cr["zero_index"])
                if zi < eeg.shape[1]:
                    row[f"pow_lgamma_30_45_{cr['electrode']}"] = float(band_chan_power["lgamma_30_45"][zi])
            rows.append(row)
    feat = pd.DataFrame(rows)
    feat.to_csv(out / "tables" / "eeg_window_power_features.csv", index=False)

    # EEG channel QC over entire usable core range.
    qc_rows = []
    for _, cr in cmap.iterrows():
        zi = int(cr["zero_index"])
        if zi >= eeg.shape[1]:
            continue
        y = eeg[:, zi]
        qc_rows.append({
            "channel": int(cr["channel"]),
            "electrode": cr["electrode"],
            "roi_label": cr["roi_label"],
            "mean": float(np.nanmean(y)),
            "std": float(np.nanstd(y)),
            "median_abs": float(np.nanmedian(np.abs(y - np.nanmedian(y)))),
            "p2p_full": float(np.nanmax(y) - np.nanmin(y)),
            "flat_fraction": float(np.mean(np.abs(np.diff(y)) < 1e-12)) if len(y) > 1 else np.nan,
        })
    qc = pd.DataFrame(qc_rows)
    qc.to_csv(out / "tables" / "eeg_channel_qc.csv", index=False)

    # Optional phase features and PAC.
    if len(feat) and (cfg.modules.get("task_lock_plv") or cfg.modules.get("formal_pncc_theta") or cfg.modules.get("pac_exploratory") or cfg.modules.get("gammascalpel")):
        logger("Computing phase features (PLV/PAC) for selected bands.")
        phase_cache: Dict[str, np.ndarray] = {}
        amp_cache: Dict[str, np.ndarray] = {}
        phase_bands = ["theta_4_8", "alpha_8_12", "lgamma_30_45", "g30_35", "g35_40", "g40_45"]
        for b in phase_bands:
            ph, amp = compute_phase_amp(eeg, fs, BANDS[b])
            phase_cache[b] = ph
            amp_cache[b] = amp
        # Fill PLV and PAC columns by iterating windows.
        for idx, row in feat.iterrows():
            w0, w1 = float(row["window_start"]), float(row["window_end"])
            mask = (ts >= w0) & (ts < w1)
            if mask.sum() < max(8, int(fs * wsec * 0.5)):
                continue
            for b in ["theta_4_8", "alpha_8_12", "lgamma_30_45", "g30_35", "g35_40", "g40_45"]:
                ph = phase_cache[b][mask, :]
                for roi_name, chans in rois.items():
                    feat.at[idx, f"plv_{b}_{roi_name}"] = median_pair_plv(ph, chans)
            if cfg.modules.get("pac_exploratory"):
                th = phase_cache["theta_4_8"][mask, :]
                for gb in ["g30_35", "g35_40", "g40_45", "lgamma_30_45"]:
                    ga = amp_cache[gb][mask, :]
                    for roi_name, chans in rois.items():
                        feat.at[idx, f"pac_theta_to_{gb}_{roi_name}"] = pac_mvl(th, ga, chans)
        feat.to_csv(out / "tables" / "eeg_window_power_plv_pac_features.csv", index=False)
    return feat, qc


# ---------------------------
# Physiology
# ---------------------------

def summarize_hrv(streams: List[dict], segments: "pd.DataFrame", out: Path, logger: RunLogger) -> "pd.DataFrame":
    s = choose_stream_by_keywords(streams, ["polarhrv", "hrv", "rr", "polar"])
    if s is None:
        logger("No HRV/RR stream found.")
        return pd.DataFrame()
    ts = np.asarray(s.get("time_stamps", []), dtype=float)
    arr = np.asarray(s.get("time_series", []), dtype=float)
    if arr.ndim > 1:
        vals = arr[:, 0]
    else:
        vals = arr
    mode = "rr_ms" if np.nanmedian(vals) > 200 else "hr_bpm"
    rows = []
    for _, seg in segments[segments["segment_type"].isin(["core","stimulus_style","washout_split"])].iterrows():
        if not pd.notna(seg.get("start", np.nan)) or not pd.notna(seg.get("end", np.nan)):
            continue
        mask = (ts >= float(seg["start"])) & (ts <= float(seg["end"]))
        x = vals[mask]
        t = ts[mask]
        if len(x) < 3:
            continue
        if mode == "rr_ms":
            rr = x
            hr = 60000.0 / np.clip(rr, 250, 2000)
            rmssd = float(np.sqrt(np.mean(np.diff(rr) ** 2))) if len(rr) > 2 else np.nan
            sdnn = float(np.std(rr, ddof=1)) if len(rr) > 2 else np.nan
        else:
            hr = x
            rr = 60000.0 / np.clip(hr, 30, 220)
            rmssd = float(np.sqrt(np.mean(np.diff(rr) ** 2))) if len(rr) > 2 else np.nan
            sdnn = float(np.std(rr, ddof=1)) if len(rr) > 2 else np.nan
        slope = np.nan
        if len(t) > 3 and np.ptp(t) > 0:
            try:
                slope = float(np.polyfit(t - t[0], hr, 1)[0])
            except Exception:
                pass
        rows.append({"segment": seg["segment"], "mean_hr_bpm": float(np.mean(hr)), "median_hr_bpm": float(np.median(hr)), "rmssd_ms": rmssd, "sdnn_ms": sdnn, "abs_hr_slope_bpm_per_sec": abs(slope) if np.isfinite(slope) else np.nan, "n_samples": len(x), "stream_mode": mode})
    df = pd.DataFrame(rows)
    if len(df):
        for col in ["mean_hr_bpm", "rmssd_ms", "sdnn_ms", "abs_hr_slope_bpm_per_sec"]:
            df[f"z_{col}"] = zscore_series(df[col])
        df["API_A_v1"] = -0.35*df["z_mean_hr_bpm"] + 0.35*df["z_rmssd_ms"] + 0.15*df["z_sdnn_ms"] - 0.15*df["z_abs_hr_slope_bpm_per_sec"]
    df.to_csv(out / "tables" / "hrv_api_segment_summary.csv", index=False)
    return df


def summarize_respiration(streams: List[dict], segments: "pd.DataFrame", out: Path, logger: RunLogger) -> "pd.DataFrame":
    s = choose_stream_by_keywords(streams, ["vernier", "resp", "breath"])
    if s is None:
        logger("No respiration stream found.")
        return pd.DataFrame()
    ts = np.asarray(s.get("time_stamps", []), dtype=float)
    arr = np.asarray(s.get("time_series", []), dtype=float)
    vals = arr[:, 0] if arr.ndim > 1 else arr
    rows = []
    for _, seg in segments[segments["segment_type"].isin(["core","stimulus_style","washout_split"])].iterrows():
        if not pd.notna(seg.get("start", np.nan)) or not pd.notna(seg.get("end", np.nan)):
            continue
        mask = (ts >= float(seg["start"])) & (ts <= float(seg["end"]))
        x = vals[mask]
        t = ts[mask]
        if len(x) < 10:
            continue
        fs = effective_fs(t)
        bpm = np.nan
        if np.isfinite(fs) and fs > 1 and len(x) > fs * 8:
            y = x - np.nanmean(x)
            freqs, psd = signal.welch(y, fs=fs, nperseg=min(len(y), int(fs*30)))
            band = (freqs >= 0.08) & (freqs <= 0.5)
            if band.any():
                bpm = float(freqs[band][np.argmax(psd[band])] * 60.0)
        slope = np.nan
        if len(t) > 3 and np.ptp(t) > 0:
            try:
                slope = float(np.polyfit(t - t[0], x, 1)[0])
            except Exception:
                pass
        rows.append({"segment": seg["segment"], "resp_mean": float(np.nanmean(x)), "resp_std": float(np.nanstd(x)), "resp_p2p": float(np.nanmax(x)-np.nanmin(x)), "dominant_breath_rate_bpm": bpm, "resp_slope": slope, "n_samples": len(x)})
    df = pd.DataFrame(rows)
    df.to_csv(out / "tables" / "respiration_segment_summary.csv", index=False)
    return df


# ---------------------------
# Contrasts and endpoints
# ---------------------------

def artifact_score(df: "pd.DataFrame") -> "pd.Series":
    cols = [c for c in ["median_p2p", "max_p2p", "pow_hf_proxy_45_55_artifact_sentinel", "pow_hf_proxy_45_55_all_channels"] if c in df.columns]
    if not cols:
        return pd.Series(np.zeros(len(df)), index=df.index)
    z = pd.DataFrame({c: zscore_series(df[c]) for c in cols})
    return z.mean(axis=1)


def artifact_matched_delta(features: "pd.DataFrame", col: str, a_seg: str, b_seg: str, n_perm: int, seed: int) -> Dict[str, Any]:
    rng = np.random.default_rng(seed)
    a = features[features["segment"] == a_seg].copy()
    b = features[features["segment"] == b_seg].copy()
    a = a[np.isfinite(a[col])]
    b = b[np.isfinite(b[col])]
    if len(a) < 2 or len(b) < 2:
        return {"metric": col, "A": a_seg, "B": b_seg, "n_A": len(a), "n_B": len(b), "delta": np.nan, "ci_low": np.nan, "ci_high": np.nan, "perm_p_two_sided": np.nan, "status": "insufficient_windows"}
    a["artifact_score"] = artifact_score(a)
    b["artifact_score"] = artifact_score(b)
    n = min(len(a), len(b))
    a = a.sort_values("artifact_score").iloc[:n]
    b = b.sort_values("artifact_score").iloc[:n]
    diffs = a[col].to_numpy() - b[col].to_numpy()
    delta = float(np.nanmean(diffs))
    boots = []
    for _ in range(max(100, min(n_perm, 1000))):
        ii = rng.integers(0, n, n)
        boots.append(float(np.nanmean(diffs[ii])))
    ci_low, ci_high = np.nanpercentile(boots, [2.5, 97.5])
    # permutation by swapping paired labels
    count = 0
    total = max(100, n_perm)
    for _ in range(total):
        signs = rng.choice([-1, 1], size=n)
        pdelt = float(np.nanmean(diffs * signs))
        if abs(pdelt) >= abs(delta):
            count += 1
    p = (count + 1) / (total + 1)
    return {"metric": col, "A": a_seg, "B": b_seg, "n_A": len(a), "n_B": len(b), "n_matched": n, "delta": delta, "ci_low": float(ci_low), "ci_high": float(ci_high), "perm_p_two_sided": float(p), "status": "ok"}


def run_core_contrasts(features: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> "pd.DataFrame":
    if features is None or len(features) == 0:
        return pd.DataFrame()
    metrics = []
    # primary power metrics
    for roi in ["primary_content_core", "meaning_candidate", "frontoparietal_task", "visual_control", "artifact_sentinel", "jaw_temporal_sentinel", "all_channels"]:
        for band in ["lgamma_30_45", "g30_35", "g35_40", "g40_45", "theta_4_8", "alpha_8_12"]:
            c = f"pow_{band}_{roi}"
            if c in features.columns:
                metrics.append(c)
            pc = f"plv_{band}_{roi}"
            if pc in features.columns:
                metrics.append(pc)
    # contrasts
    pairs = [
        ("TARGET_1", "CONTROL_1"),
        ("TARGET_1", "CONTEXTUAL_OVERRIDE_1"),
        ("WASHOUT_2", "WASHOUT_1"),
        ("WASHOUT_2", "WASHOUT_3"),
        ("TARGET_1_FINAL_30S", "CONTROL_1_FINAL_30S"),
        ("TARGET_1_FINAL_30S", "CONTEXTUAL_OVERRIDE_1_FINAL_30S"),
        ("TARGET_1_FINAL_60S", "CONTROL_1_FINAL_60S"),
        ("TARGET_1_FINAL_60S", "CONTEXTUAL_OVERRIDE_1_FINAL_60S"),
    ]
    rows = []
    for col in metrics:
        for a, b in pairs:
            if a in set(features["segment"]) and b in set(features["segment"]):
                rows.append(artifact_matched_delta(features, col, a, b, cfg.n_surrogates, cfg.random_seed))
    df = pd.DataFrame(rows)
    df.to_csv(out / "tables" / "artifact_matched_condition_contrasts.csv", index=False)
    return df


def run_residualized_lgamma(features: "pd.DataFrame", resp: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> "pd.DataFrame":
    if features is None or len(features) == 0:
        return pd.DataFrame()
    # basic residualization inside EEG windows: predict primary lower gamma from hf proxy + artifact metrics.
    target_cols = [c for c in features.columns if c.startswith("pow_lgamma_30_45_") and any(x in c for x in ["primary_content_core", "meaning_candidate", "frontoparietal_task", "all_channels"])]
    covars = [c for c in ["median_p2p", "max_p2p", "pow_hf_proxy_45_55_artifact_sentinel", "pow_hf_proxy_45_55_all_channels"] if c in features.columns]
    if not target_cols or not covars:
        return pd.DataFrame()
    outfeat = features[["segment","window_start","window_end"] + target_cols + covars].copy()
    for tcol in target_cols:
        sub = outfeat[[tcol]+covars].dropna()
        if len(sub) < len(covars) + 5:
            outfeat[tcol + "_resid"] = np.nan
            continue
        X = sub[covars].to_numpy(float)
        y = sub[tcol].to_numpy(float)
        X = np.column_stack([np.ones(len(X)), X])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        allX = outfeat[covars].to_numpy(float)
        valid = np.all(np.isfinite(allX), axis=1)
        pred = np.full(len(outfeat), np.nan)
        pred[valid] = np.column_stack([np.ones(valid.sum()), allX[valid]]).dot(beta)
        outfeat[tcol + "_resid"] = outfeat[tcol] - pred
    outfeat.to_csv(out / "tables" / "eeg_low_gamma_residualized_window_features.csv", index=False)
    rows = []
    for col in [c for c in outfeat.columns if c.endswith("_resid")]:
        tmp = features[["segment","median_p2p","max_p2p"]].copy()
        tmp[col] = outfeat[col]
        for extra in ["pow_hf_proxy_45_55_artifact_sentinel", "pow_hf_proxy_45_55_all_channels"]:
            if extra in features:
                tmp[extra] = features[extra]
        for a, b in [("TARGET_1","CONTEXTUAL_OVERRIDE_1"),("TARGET_1","CONTROL_1"),("TARGET_1_FINAL_30S","CONTEXTUAL_OVERRIDE_1_FINAL_30S"),("WASHOUT_2","WASHOUT_1"),("WASHOUT_2","WASHOUT_3")]:
            if a in set(tmp["segment"]) and b in set(tmp["segment"]):
                rows.append(artifact_matched_delta(tmp, col, a, b, cfg.n_surrogates, cfg.random_seed))
    df = pd.DataFrame(rows)
    df.to_csv(out / "tables" / "eeg_low_gamma_residualized_contrasts.csv", index=False)
    return df


def run_gammascalpel(features: "pd.DataFrame", hrv: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> Tuple["pd.DataFrame", "pd.DataFrame"]:
    if features is None or len(features) == 0:
        return pd.DataFrame(), pd.DataFrame()
    df = features.copy()
    # Window-level z scores for relevant columns.
    score_cols = []
    for band in ["g30_35", "g35_40", "g40_45", "lgamma_30_45"]:
        for roi in ["frontoparietal_task", "meaning_candidate", "visual_control", "artifact_sentinel", "jaw_temporal_sentinel", "primary_content_core"]:
            for prefix in ["pow", "plv"]:
                c = f"{prefix}_{band}_{roi}"
                if c in df.columns:
                    zc = "z_" + c
                    df[zc] = zscore_series(df[c])
                    score_cols.append(zc)
    # Artifact penalty.
    df["artifact_score"] = artifact_score(df)
    df["z_artifact_score"] = zscore_series(df["artifact_score"])
    # Build exploratory scores by band.
    for band in ["g30_35", "g35_40", "g40_45", "lgamma_30_45"]:
        pow_task = f"z_pow_{band}_frontoparietal_task"
        plv_task = f"z_plv_{band}_frontoparietal_task"
        pow_mean = f"z_pow_{band}_meaning_candidate"
        plv_mean = f"z_plv_{band}_meaning_candidate"
        pow_visual = f"z_pow_{band}_visual_control"
        pieces_task = [c for c in [pow_task, plv_task] if c in df.columns]
        pieces_mean = [c for c in [pow_mean] if c in df.columns]
        if pieces_task:
            df[f"TaskGamma_{band}"] = df[pieces_task].mean(axis=1) - 0.25*df["z_artifact_score"]
        if pieces_mean:
            base = df[pieces_mean].mean(axis=1)
            if plv_mean in df.columns:
                base = base - df[plv_mean]
            if pow_visual in df.columns:
                base = base - 0.25*df[pow_visual]
            if f"TaskGamma_{band}" in df.columns:
                base = base - 0.50*df[f"TaskGamma_{band}"]
            df[f"MeaningGamma_{band}"] = base - 0.50*df["z_artifact_score"]
    score_cols2 = [c for c in df.columns if c.startswith("TaskGamma_") or c.startswith("MeaningGamma_")]
    df_scores = df[["segment","window_start","window_end","artifact_score"] + score_cols2].copy() if score_cols2 else pd.DataFrame()
    df_scores.to_csv(out / "tables" / "gammascalpel_window_scores.csv", index=False)
    rows = []
    for col in score_cols2:
        for a, b in [("TARGET_1","CONTEXTUAL_OVERRIDE_1"),("TARGET_1","CONTROL_1"),("TARGET_1_FINAL_30S","CONTEXTUAL_OVERRIDE_1_FINAL_30S"),("TARGET_1_FINAL_30S","CONTROL_1_FINAL_30S")]:
            if a in set(df["segment"]) and b in set(df["segment"]):
                rows.append(artifact_matched_delta(df[["segment","median_p2p","max_p2p",col]].copy(), col, a, b, cfg.n_surrogates, cfg.random_seed))
    contrasts = pd.DataFrame(rows)
    contrasts.to_csv(out / "tables" / "gammascalpel_score_contrasts.csv", index=False)
    return df_scores, contrasts


def run_pncc_theta(features: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> Tuple["pd.DataFrame", "pd.DataFrame"]:
    if features is None or len(features) == 0:
        return pd.DataFrame(), pd.DataFrame()
    # Prefer theta PLV, fallback to theta power if PLV missing.
    metric_candidates = [
        "plv_theta_4_8_primary_content_core",
        "plv_theta_4_8_meaning_candidate",
        "plv_theta_4_8_all_channels",
        "pow_theta_4_8_primary_content_core",
        "pow_theta_4_8_meaning_candidate",
    ]
    rows = []
    for metric in metric_candidates:
        if metric not in features.columns:
            continue
        for a, b in [("WASHOUT_2", "WASHOUT_1"), ("WASHOUT_2", "WASHOUT_3"), ("WASHOUT_2_0_30S", "WASHOUT_1_0_30S"), ("WASHOUT_2_30_90S", "WASHOUT_1_30_90S"), ("WASHOUT_2_90_120S", "WASHOUT_1_90_120S")]:
            if a in set(features["segment"]) and b in set(features["segment"]):
                r = artifact_matched_delta(features, metric, a, b, cfg.n_surrogates, cfg.random_seed)
                r["endpoint"] = "PNCC_theta"
                rows.append(r)
    pncc = pd.DataFrame(rows)
    pncc.to_csv(out / "tables" / "pncc_theta_artifact_matched_surrogate_contrasts.csv", index=False)

    # tau_coh theta from W2 split/rolling windows: excess above W1 mean, exponential decay.
    tau_rows = []
    base_metric = next((m for m in metric_candidates if m in features.columns), None)
    if base_metric:
        w1 = features[features["segment"] == "WASHOUT_1"][base_metric].dropna()
        baseline = float(w1.mean()) if len(w1) else np.nan
        w2 = features[features["segment"] == "WASHOUT_2"].copy()
        w2 = w2[np.isfinite(w2[base_metric])]
        if len(w2) >= 5 and np.isfinite(baseline):
            t0 = float(w2["window_mid"].min())
            x = w2["window_mid"].to_numpy(float) - t0
            y = w2[base_metric].to_numpy(float) - baseline
            # keep positive excess points only for fit, but record all.
            pos = np.isfinite(x) & np.isfinite(y) & (y > 0)
            tau = np.nan
            status = "insufficient_positive_excess"
            if pos.sum() >= 3:
                def expfun(t, a, tau_):
                    return a * np.exp(-t / tau_)
                try:
                    popt, _ = optimize.curve_fit(expfun, x[pos], y[pos], p0=[max(y[pos]), 60.0], bounds=([0, 1.0], [np.inf, 300.0]), maxfev=5000)
                    tau = float(popt[1])
                    status = "fit_ok" if tau < 299.0 else "censored_upper_bound"
                except Exception as e:
                    status = "fit_failed"
            tau_rows.append({"metric": base_metric, "baseline_washout1_mean": baseline, "w2_initial_excess": float(y[0]) if len(y) else np.nan, "tau_sec": tau, "status": status, "n_w2_windows": len(w2), "n_positive_excess_windows": int(pos.sum()) if len(w2) else 0})
    tau_df = pd.DataFrame(tau_rows)
    tau_df.to_csv(out / "tables" / "tau_coh_theta_summary.csv", index=False)
    return pncc, tau_df


def run_frequency_cascade(features: "pd.DataFrame", cfg: SuiteConfig, out: Path) -> Tuple["pd.DataFrame", "pd.DataFrame"]:
    if features is None or len(features) == 0:
        return pd.DataFrame(), pd.DataFrame()
    # Key segments based on stimulus style.
    if cfg.stimulus_style == "delayed_reveal":
        key_segments = ["TARGET_1_FINAL_30S", "TARGET_1_FINAL_60S", "WASHOUT_2_0_30S", "WASHOUT_2_30_90S", "WASHOUT_2_90_120S", "WASHOUT_3_0_30S", "WASHOUT_3_30_90S"]
    elif cfg.stimulus_style == "steady_load_with_climax":
        key_segments = ["TARGET_1", "TARGET_1_FINAL_60S", "WASHOUT_2_0_30S", "WASHOUT_2_30_90S", "WASHOUT_2_90_120S", "WASHOUT_3_30_90S"]
    else:
        key_segments = ["TARGET_1", "WASHOUT_2_0_30S", "WASHOUT_2_30_90S", "WASHOUT_2_90_120S", "WASHOUT_3_30_90S"]
    metrics = {
        "gamma_power": "pow_lgamma_30_45_primary_content_core" if "pow_lgamma_30_45_primary_content_core" in features.columns else "pow_lgamma_30_45_all_channels",
        "theta_bridge": "plv_theta_4_8_primary_content_core" if "plv_theta_4_8_primary_content_core" in features.columns else "pow_theta_4_8_primary_content_core",
        "alpha_recovery": "pow_alpha_8_12_primary_content_core" if "pow_alpha_8_12_primary_content_core" in features.columns else "pow_alpha_8_12_all_channels",
        "z_lock": "plv_lgamma_30_45_frontoparietal_task" if "plv_lgamma_30_45_frontoparietal_task" in features.columns else "plv_lgamma_30_45_all_channels",
    }
    rows = []
    for seg in key_segments:
        sub = features[features["segment"] == seg]
        if len(sub) == 0:
            continue
        row = {"segment": seg}
        row["segment_order"] = len(rows)
        for name, col in metrics.items():
            row[name] = float(sub[col].mean()) if col in sub.columns else np.nan
            row[name + "_metric"] = col
        rows.append(row)
    kdf = pd.DataFrame(rows)
    if len(kdf):
        for name in ["gamma_power", "theta_bridge", "alpha_recovery", "z_lock"]:
            kdf["z_" + name] = zscore_series(kdf[name])
    # order index: first maximum occurrence by stage.
    order_row = {"stimulus_style": cfg.stimulus_style, "classic_FCOI_supported": False, "modified_delayed_reveal_supported": False}
    if len(kdf):
        peaks = {}
        for name in ["gamma_power", "theta_bridge", "alpha_recovery", "z_lock"]:
            if "z_"+name in kdf.columns and kdf["z_"+name].notna().any():
                ix = kdf["z_"+name].idxmax()
                peaks[name + "_peak_segment"] = kdf.loc[ix, "segment"]
                peaks[name + "_peak_order"] = int(kdf.loc[ix, "segment_order"])
        order_row.update(peaks)
        if all(k in peaks for k in ["gamma_power_peak_order","theta_bridge_peak_order","alpha_recovery_peak_order","z_lock_peak_order"]):
            order_row["classic_FCOI_supported"] = bool(peaks["gamma_power_peak_order"] <= peaks["theta_bridge_peak_order"] <= peaks["alpha_recovery_peak_order"] <= peaks["z_lock_peak_order"])
            order_row["modified_delayed_reveal_supported"] = bool(peaks["gamma_power_peak_order"] <= peaks["alpha_recovery_peak_order"] <= peaks["z_lock_peak_order"])
    odf = pd.DataFrame([order_row])
    kdf.to_csv(out / "tables" / "post_meaning_cascade_key_segments.csv", index=False)
    odf.to_csv(out / "tables" / "post_meaning_cascade_order_index.csv", index=False)
    return kdf, odf




# ---------------------------
# Feature-table compatibility helpers
# ---------------------------

def standardize_feature_columns(features: "pd.DataFrame") -> "pd.DataFrame":
    """Normalize column names across earlier ad hoc analysis tables and v1.x suite tables."""
    if features is None or len(features) == 0:
        return features
    df = features.copy()
    rename = {}
    for a,b in [("start_lsl","window_start"),("end_lsl","window_end"),("mid_lsl","window_mid"),("t0","window_start"),("t1","window_end"),("rel_t","window_mid"),("ptp_median","median_p2p"),("ptp_max","max_p2p")]:
        if a in df.columns and b not in df.columns:
            rename[a]=b
    df = df.rename(columns=rename)
    if "segment" not in df.columns and "phase" in df.columns:
        df["segment"] = df["phase"].astype(str)
    if "window_mid" not in df.columns and "window_start" in df.columns and "window_end" in df.columns:
        df["window_mid"] = (pd.to_numeric(df["window_start"], errors="coerce") + pd.to_numeric(df["window_end"], errors="coerce")) / 2.0
    if "median_p2p" not in df.columns:
        if "amp_rms_all" in df.columns:
            df["median_p2p"] = pd.to_numeric(df["amp_rms_all"], errors="coerce")
        elif "artifact_p2p_median" in df.columns:
            df["median_p2p"] = pd.to_numeric(df["artifact_p2p_median"], errors="coerce")
    if "max_p2p" not in df.columns:
        if "amp_peak_all" in df.columns:
            df["max_p2p"] = pd.to_numeric(df["amp_peak_all"], errors="coerce")
        elif "artifact_p2p_max" in df.columns:
            df["max_p2p"] = pd.to_numeric(df["artifact_p2p_max"], errors="coerce")
    # Posterior-temporal naming compatibility: older outputs used *_posterior_temporal_proxy.
    for c in list(df.columns):
        if "posterior_temporal_proxy" in c:
            c2 = c.replace("posterior_temporal_proxy", "posterior_temporal")
            if c2 not in df.columns:
                df[c2] = df[c]
        if c.startswith("meaninggamma_"):
            c2 = "MeaningGamma_" + c[len("meaninggamma_"):]
            if c2 not in df.columns: df[c2] = df[c]
        if c.startswith("taskgamma_"):
            c2 = "TaskGamma_" + c[len("taskgamma_"):]
            if c2 not in df.columns: df[c2] = df[c]
        if c.startswith("temporal_proxy_"):
            c2 = "TemporalSemanticProxy_" + c[len("temporal_proxy_"):]
            if c2 not in df.columns: df[c2] = df[c]
    return df

# ---------------------------
# Temporal semantic proxy + post-peak PNCC / gamma-to-theta handoff
# ---------------------------

def load_annotation_csv(path: str, out: Path, logger: RunLogger) -> "pd.DataFrame":
    if not path:
        return pd.DataFrame()
    p = Path(path).expanduser()
    if not p.exists():
        logger(f"Annotation CSV not found: {p}")
        return pd.DataFrame()
    ann = pd.read_csv(p)
    ann.columns = [str(c).strip() for c in ann.columns]
    for col in ["start_sec", "end_sec", "intensity_0_9", "confidence_0_3"]:
        if col in ann.columns:
            ann[col] = pd.to_numeric(ann[col], errors="coerce")
    ann.to_csv(out / "tables" / "stimulus_annotations_used.csv", index=False)
    try: shutil.copy2(p, out / "provenance" / p.name)
    except Exception: pass
    return ann


def add_relative_time(features: "pd.DataFrame") -> "pd.DataFrame":
    df = features.copy()
    if "segment" not in df.columns or "window_mid" not in df.columns:
        return df
    origins = df.groupby("segment")[("window_start" if "window_start" in df.columns else "window_mid")].min().to_dict()
    df["segment_origin"] = df["segment"].map(origins)
    df["rel_mid_sec"] = df["window_mid"] - df["segment_origin"]
    if "window_start" in df.columns: df["rel_start_sec"] = df["window_start"] - df["segment_origin"]
    if "window_end" in df.columns: df["rel_end_sec"] = df["window_end"] - df["segment_origin"]
    return df


def compute_temporal_semantic_proxy(features: "pd.DataFrame", out: Path) -> "pd.DataFrame":
    if features is None or len(features) == 0:
        return pd.DataFrame()
    df = features.copy()
    df["artifact_score"] = artifact_score(df)
    for band in ["g30_35", "g35_40", "g40_45", "lgamma_30_45"]:
        pt, vc, jaw, fp = f"pow_{band}_posterior_temporal", f"pow_{band}_visual_control", f"pow_{band}_jaw_temporal_sentinel", f"pow_{band}_frontoparietal_task"
        if pt in df.columns:
            score = zscore_series(df[pt])
            if vc in df.columns: score -= 0.35 * zscore_series(df[vc])
            if jaw in df.columns: score -= 0.50 * zscore_series(df[jaw])
            if fp in df.columns: score -= 0.35 * zscore_series(df[fp])
            score -= 0.25 * zscore_series(df["artifact_score"])
            df[f"TemporalSemanticProxy_{band}"] = score
    cols = [c for c in df.columns if c.startswith("TemporalSemanticProxy_")]
    keep = [c for c in ["segment", "window_start", "window_end", "window_mid", "rel_mid_sec", "artifact_score"] if c in df.columns] + cols
    (df[keep] if cols else pd.DataFrame()).to_csv(out / "tables" / "temporal_semantic_proxy_window_scores.csv", index=False)
    return df


def _smooth_vector(y: np.ndarray, k: int = 5) -> np.ndarray:
    if len(y) == 0: return y
    return pd.Series(y, dtype="float64").rolling(max(1, int(k)), center=True, min_periods=1).median().to_numpy(float)


def detect_peak_and_taper(features: "pd.DataFrame", cfg: SuiteConfig, out: Path) -> "pd.DataFrame":
    df = add_relative_time(features)
    if df is None or len(df) == 0 or "segment" not in df.columns:
        pd.DataFrame().to_csv(out / "tables" / "postpeak_peak_and_taper_detection.csv", index=False); return pd.DataFrame()
    target = df[df["segment"] == "TARGET_1"].copy()
    if len(target) == 0:
        pd.DataFrame().to_csv(out / "tables" / "postpeak_peak_and_taper_detection.csv", index=False); return pd.DataFrame()
    duration = float(target["rel_mid_sec"].max()) if "rel_mid_sec" in target.columns else float(len(target))
    traces = {
        "primary_gamma": "pow_lgamma_30_45_primary_content_core",
        "meaning_candidate_gamma": "pow_lgamma_30_45_meaning_candidate",
        "posterior_temporal_gamma": "pow_lgamma_30_45_posterior_temporal",
        "temporal_semantic_proxy": "TemporalSemanticProxy_lgamma_30_45",
        "task_gamma": "pow_lgamma_30_45_frontoparietal_task",
    }
    for c in df.columns:
        if c.startswith("MeaningGamma_lgamma"): traces["MeaningGamma_lgamma_30_45"] = c
        if c.startswith("TaskGamma_lgamma"): traces["TaskGamma_lgamma_30_45"] = c
    rows=[]
    for label,col in traces.items():
        if col not in target.columns: continue
        rel = target["rel_mid_sec"].to_numpy(float)
        scopes=[("whole_target", np.ones(len(target),bool)), ("first_half", rel <= duration/2), ("second_half", rel > duration/2)]
        for scope,mask in scopes:
            sub=target[mask].copy(); sub=sub[np.isfinite(sub[col])]
            if len(sub)<5: continue
            x=sub["rel_mid_sec"].to_numpy(float); y=_smooth_vector(sub[col].to_numpy(float),5)
            if not np.isfinite(y).any(): continue
            imax=int(np.nanargmax(y)); peak_t=float(x[imax]); peak=float(y[imax])
            base=float(np.nanmedian(y[:max(1,min(imax,10))])) if imax>1 else float(np.nanmedian(y))
            threshold=base+0.5*(peak-base); taper=np.nan; taper_val=np.nan
            for j in range(imax+1,len(y)):
                if np.isfinite(y[j]) and y[j] <= threshold:
                    taper=float(x[j]); taper_val=float(y[j]); break
            status="taper_found" if np.isfinite(taper) else "no_half_taper_found"
            if not np.isfinite(taper):
                taper=float(min(x[-1], peak_t+20)); taper_val=float(np.interp(taper,x,y)) if len(x)>1 else peak
            rows.append({"anchor_id":f"{label}_{scope}","predictor_label":label,"predictor_col":col,"scope":scope,"peak_rel_sec":peak_t,"taper_rel_sec":taper,"peak_value_smooth":peak,"baseline_value_smooth":base,"half_taper_threshold":threshold,"taper_value_smooth":taper_val,"status":status,"n_windows":len(sub)})
    peaks=pd.DataFrame(rows); peaks.to_csv(out/"tables"/"postpeak_peak_and_taper_detection.csv", index=False); return peaks


def _mean_in_rel_window(df: "pd.DataFrame", segment: str, col: str, start: float, end: float) -> float:
    if col not in df.columns: return np.nan
    sub=df[(df["segment"]==segment)&(df["rel_mid_sec"]>=start)&(df["rel_mid_sec"]<end)]
    return float(sub[col].mean()) if len(sub) else np.nan


def run_postpeak_pncc_theta(features: "pd.DataFrame", peaks: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> "pd.DataFrame":
    df=add_relative_time(features)
    if "artifact_score" not in df.columns: df["artifact_score"]=artifact_score(df)
    theta=[c for c in ["plv_theta_4_8_primary_content_core","plv_theta_4_8_meaning_candidate","plv_theta_4_8_posterior_temporal","pow_theta_4_8_primary_content_core","pow_theta_4_8_meaning_candidate","pow_theta_4_8_posterior_temporal"] if c in df.columns]
    rows=[]
    if peaks is None or len(peaks)==0:
        pd.DataFrame().to_csv(out/"tables"/"postpeak_pncc_theta_contrasts.csv", index=False); return pd.DataFrame()
    for _,p in peaks.iterrows():
        anchor=float(p.get("taper_rel_sec", np.nan))
        if not np.isfinite(anchor): continue
        for metric in theta:
            for w0,w1 in [(0,10),(10,30),(30,60)]:
                pre0,pre1=max(0,anchor-30),max(0,anchor-5)
                tp=_mean_in_rel_window(df,"TARGET_1",metric,pre0,pre1); tq=_mean_in_rel_window(df,"TARGET_1",metric,anchor+w0,anchor+w1)
                cp=_mean_in_rel_window(df,"CONTROL_1",metric,pre0,pre1); cq=_mean_in_rel_window(df,"CONTROL_1",metric,anchor+w0,anchor+w1)
                op=_mean_in_rel_window(df,"CONTEXTUAL_OVERRIDE_1",metric,pre0,pre1); oq=_mean_in_rel_window(df,"CONTEXTUAL_OVERRIDE_1",metric,anchor+w0,anchor+w1)
                ap=_mean_in_rel_window(df,"TARGET_1","artifact_score",pre0,pre1); aq=_mean_in_rel_window(df,"TARGET_1","artifact_score",anchor+w0,anchor+w1)
                td=tq-tp if np.isfinite(tq) and np.isfinite(tp) else np.nan
                cd=cq-cp if np.isfinite(cq) and np.isfinite(cp) else np.nan
                od=oq-op if np.isfinite(oq) and np.isfinite(op) else np.nan
                rows.append({"endpoint":"PostPeakPNCC_theta","anchor_id":p.get("anchor_id"),"predictor_label":p.get("predictor_label"),"scope":p.get("scope"),"anchor_taper_rel_sec":anchor,"theta_metric":metric,"post_window":f"{w0}-{w1}s_after_taper","target_delta":td,"control_delta":cd,"override_delta":od,"target_minus_control_delta":td-cd if np.isfinite(td) and np.isfinite(cd) else np.nan,"target_minus_override_delta":td-od if np.isfinite(td) and np.isfinite(od) else np.nan,"artifact_delta_target":aq-ap if np.isfinite(aq) and np.isfinite(ap) else np.nan})
    res=pd.DataFrame(rows); res.to_csv(out/"tables"/"postpeak_pncc_theta_contrasts.csv",index=False)
    if len(res): res[(res["theta_metric"].astype(str).str.contains("plv_theta_4_8_primary")) & (res["post_window"]=="10-30s_after_taper")].to_csv(out/"tables"/"focused_postpeak_pncc_theta_results.csv",index=False)
    logger("PostPeakPNCC_theta module complete."); return res


def run_annotation_locked_theta_carryover(features: "pd.DataFrame", annotations: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> "pd.DataFrame":
    df=add_relative_time(features)
    if "artifact_score" not in df.columns: df["artifact_score"]=artifact_score(df)
    if annotations is None or len(annotations)==0:
        pd.DataFrame().to_csv(out/"tables"/"annotation_locked_theta_carryover_contrasts.csv",index=False); return pd.DataFrame()
    metrics=[c for c in ["plv_theta_4_8_primary_content_core","plv_theta_4_8_meaning_candidate","pow_theta_4_8_primary_content_core"] if c in df.columns]
    eligible={"semantic_reveal","climax","post_reveal_reflection","sustained_meaning_load","meaning_taper","threat_startle"}
    rows=[]
    for _,ann in annotations.iterrows():
        etype=str(ann.get("event_type","")).strip()
        if etype not in eligible: continue
        phase=str(ann.get("phase","TARGET_VIDEO")).strip().upper(); seg="WASHOUT_2" if phase.startswith("WASHOUT_2") else "TARGET_1"
        anchor=float(ann.get("end_sec",np.nan))
        if not np.isfinite(anchor): continue
        for metric in metrics:
            for w0,w1 in [(0,10),(10,30),(30,60)]:
                pre0,pre1=max(0,anchor-30),max(0,anchor-5)
                tp=_mean_in_rel_window(df,seg,metric,pre0,pre1); tq=_mean_in_rel_window(df,seg,metric,anchor+w0,anchor+w1)
                td=tq-tp if np.isfinite(tq) and np.isfinite(tp) else np.nan
                cd=od=np.nan
                if seg=="TARGET_1":
                    cp=_mean_in_rel_window(df,"CONTROL_1",metric,pre0,pre1); cq=_mean_in_rel_window(df,"CONTROL_1",metric,anchor+w0,anchor+w1)
                    op=_mean_in_rel_window(df,"CONTEXTUAL_OVERRIDE_1",metric,pre0,pre1); oq=_mean_in_rel_window(df,"CONTEXTUAL_OVERRIDE_1",metric,anchor+w0,anchor+w1)
                    cd=cq-cp if np.isfinite(cq) and np.isfinite(cp) else np.nan; od=oq-op if np.isfinite(oq) and np.isfinite(op) else np.nan
                rows.append({"endpoint":"AnnotationLockedThetaCarryover","event_id":ann.get("event_id",""),"event_type":etype,"phase":phase,"anchor_segment":seg,"anchor_end_sec":anchor,"intensity_0_9":ann.get("intensity_0_9",np.nan),"confidence_0_3":ann.get("confidence_0_3",np.nan),"theta_metric":metric,"post_window":f"{w0}-{w1}s_after_annotation_end","target_delta":td,"target_minus_control_delta":td-cd if np.isfinite(td) and np.isfinite(cd) else np.nan,"target_minus_override_delta":td-od if np.isfinite(td) and np.isfinite(od) else np.nan})
    res=pd.DataFrame(rows); res.to_csv(out/"tables"/"annotation_locked_theta_carryover_contrasts.csv",index=False); logger("Annotation-locked theta carryover module complete."); return res


def _lagged_corr(df: "pd.DataFrame", predictor: str, outcome: str, lag: float, segment: str="TARGET_1") -> Tuple[float,int,float]:
    sub=df[df["segment"]==segment].copy().sort_values("rel_mid_sec")
    if len(sub)<8 or predictor not in sub.columns or outcome not in sub.columns: return np.nan,0,np.nan
    t=sub["rel_mid_sec"].to_numpy(float); x=sub[predictor].to_numpy(float); y=sub[outcome].to_numpy(float); art=sub["artifact_score"].to_numpy(float) if "artifact_score" in sub.columns else np.zeros(len(sub))
    pairs=[]
    for i,ti in enumerate(t):
        tt=ti+lag; j=int(np.argmin(np.abs(t-tt)))
        if abs(t[j]-tt)<=max(2.0,lag*.25) and t[j]>ti+1e-6: pairs.append((x[i],y[j],art[i],art[j]))
    arr=np.asarray(pairs,float)
    if len(arr)<6: return np.nan,len(arr),np.nan
    arr=arr[np.all(np.isfinite(arr),axis=1)]
    if len(arr)<6 or np.nanstd(arr[:,0])==0 or np.nanstd(arr[:,1])==0: return np.nan,len(arr),np.nan
    r=float(np.corrcoef(arr[:,0],arr[:,1])[0,1])
    try:
        X1=np.column_stack([np.ones(len(arr)),arr[:,2]]); X2=np.column_stack([np.ones(len(arr)),arr[:,3]])
        rx=arr[:,0]-X1.dot(np.linalg.lstsq(X1,arr[:,0],rcond=None)[0]); ry=arr[:,1]-X2.dot(np.linalg.lstsq(X2,arr[:,1],rcond=None)[0])
        pr=float(np.corrcoef(rx,ry)[0,1]) if np.nanstd(rx)>0 and np.nanstd(ry)>0 else np.nan
    except Exception: pr=np.nan
    return r,len(arr),pr


def run_gamma_to_theta_handoff(features: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> Tuple["pd.DataFrame","pd.DataFrame"]:
    df=add_relative_time(features)
    if "artifact_score" not in df.columns: df["artifact_score"]=artifact_score(df)
    predictors=[c for c in ["pow_lgamma_30_45_primary_content_core","pow_lgamma_30_45_meaning_candidate","pow_lgamma_30_45_posterior_temporal","TemporalSemanticProxy_lgamma_30_45","MeaningGamma_lgamma_30_45"] if c in df.columns]
    outcomes=[c for c in ["plv_theta_4_8_primary_content_core","plv_theta_4_8_meaning_candidate","plv_theta_4_8_posterior_temporal","pow_theta_4_8_primary_content_core"] if c in df.columns]
    rows=[]
    for pred in predictors:
        for outc in outcomes:
            for lag in [2,5,8,10,12,15,20,22,25,30,40,50,60]:
                r,n,pr=_lagged_corr(df,pred,outc,float(lag),"TARGET_1"); rows.append({"endpoint":"G2ThetaHandoff","predictor":pred,"outcome":outc,"lag_sec":lag,"r":r,"n_pairs":n,"artifact_partial_r":pr})
    corr=pd.DataFrame(rows); corr.to_csv(out/"tables"/"gamma_to_theta_handoff_lag_correlations.csv",index=False)
    best=[]
    if len(corr):
        for (pred,outc),sub in corr.dropna(subset=["r"]).groupby(["predictor","outcome"]):
            if len(sub): best.append(corr.loc[sub["r"].abs().idxmax()].to_dict())
    best=pd.DataFrame(best); best.to_csv(out/"tables"/"gamma_to_theta_handoff_best_lags.csv",index=False); logger("Gamma-to-theta handoff module complete."); return corr,best




# ---------------------------
# Thresholded State-Update + State-Locked Handoff Alignment (v1.2)
# ---------------------------

def _state_locked_metric_columns(df: "pd.DataFrame") -> List[str]:
    preferred = [
        "pow_lgamma_30_45_primary_content_core",
        "pow_lgamma_30_45_meaning_candidate",
        "pow_lgamma_30_45_posterior_temporal",
        "TemporalSemanticProxy_lgamma_30_45",
        "MeaningGamma_lgamma_30_45",
        "plv_theta_4_8_primary_content_core",
        "plv_theta_4_8_meaning_candidate",
        "plv_theta_4_8_posterior_temporal",
        "pow_theta_4_8_primary_content_core",
        "pow_alpha_8_12_primary_content_core",
        "artifact_score",
    ]
    return [c for c in preferred if c in df.columns]


def _window_mean(df: "pd.DataFrame", seg: str, col: str, start: float, end: float) -> float:
    if col not in df.columns or "rel_mid_sec" not in df.columns or "segment" not in df.columns:
        return np.nan
    sub = df[(df["segment"] == seg) & (df["rel_mid_sec"] >= start) & (df["rel_mid_sec"] < end)]
    return float(sub[col].mean()) if len(sub) else np.nan


def run_thresholded_state_update(features: "pd.DataFrame", peaks: "pd.DataFrame", annotations: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> Tuple["pd.DataFrame", "pd.DataFrame"]:
    """Summarize candidate state-update sequences: high-frequency intake -> taper -> theta/API integration.

    This module is deliberately conservative. It does not claim plasticity, LTP, or structural change.
    It only reports whether predeclared candidate intake anchors are followed by theta-compatible windows.
    """
    df = add_relative_time(features)
    if df is None or len(df) == 0:
        empty = pd.DataFrame()
        empty.to_csv(out/"tables"/"thresholded_state_update_candidate_windows.csv", index=False)
        empty.to_csv(out/"tables"/"thresholded_state_update_summary.csv", index=False)
        return empty, empty
    if "artifact_score" not in df.columns:
        df["artifact_score"] = artifact_score(df)
    if peaks is None or len(peaks) == 0:
        peaks = detect_peak_and_taper(df, cfg, out)
    theta_metrics = [c for c in ["plv_theta_4_8_primary_content_core", "plv_theta_4_8_meaning_candidate", "pow_theta_4_8_primary_content_core"] if c in df.columns]
    rows = []
    for _, p in (peaks if peaks is not None else pd.DataFrame()).iterrows():
        anchor = float(p.get("taper_rel_sec", np.nan))
        if not np.isfinite(anchor):
            continue
        pre0, pre1 = max(0.0, anchor - 30.0), max(0.0, anchor - 5.0)
        for metric in theta_metrics:
            for w0, w1 in [(0, 10), (10, 30), (30, 60)]:
                td_pre = _window_mean(df, "TARGET_1", metric, pre0, pre1)
                td_post = _window_mean(df, "TARGET_1", metric, anchor + w0, anchor + w1)
                cd_pre = _window_mean(df, "CONTROL_1", metric, pre0, pre1)
                cd_post = _window_mean(df, "CONTROL_1", metric, anchor + w0, anchor + w1)
                od_pre = _window_mean(df, "CONTEXTUAL_OVERRIDE_1", metric, pre0, pre1)
                od_post = _window_mean(df, "CONTEXTUAL_OVERRIDE_1", metric, anchor + w0, anchor + w1)
                art_pre = _window_mean(df, "TARGET_1", "artifact_score", pre0, pre1)
                art_post = _window_mean(df, "TARGET_1", "artifact_score", anchor + w0, anchor + w1)
                td = td_post - td_pre if np.isfinite(td_post) and np.isfinite(td_pre) else np.nan
                cd = cd_post - cd_pre if np.isfinite(cd_post) and np.isfinite(cd_pre) else np.nan
                od = od_post - od_pre if np.isfinite(od_post) and np.isfinite(od_pre) else np.nan
                tmc = td - cd if np.isfinite(td) and np.isfinite(cd) else np.nan
                tmo = td - od if np.isfinite(td) and np.isfinite(od) else np.nan
                artd = art_post - art_pre if np.isfinite(art_post) and np.isfinite(art_pre) else np.nan
                grade = "not_evaluable"
                if np.isfinite(tmo):
                    if tmo > 0 and (not np.isfinite(artd) or artd <= 0):
                        grade = "candidate_state_update_supported_by_sign_artifact_not_rising"
                    elif tmo > 0:
                        grade = "candidate_state_update_supported_by_sign_artifact_cautioned"
                    else:
                        grade = "not_supported_by_target_override_sign"
                rows.append({
                    "endpoint": "ThresholdedStateUpdate_v1",
                    "anchor_id": p.get("anchor_id", ""),
                    "predictor_label": p.get("predictor_label", ""),
                    "predictor_col": p.get("predictor_col", ""),
                    "scope": p.get("scope", ""),
                    "anchor_taper_rel_sec": anchor,
                    "theta_metric": metric,
                    "post_window": f"{w0}-{w1}s_after_taper",
                    "target_delta": td,
                    "target_minus_control_delta": tmc,
                    "target_minus_override_delta": tmo,
                    "artifact_delta_target": artd,
                    "state_update_grade": grade,
                })
    cand = pd.DataFrame(rows)
    cand.to_csv(out/"tables"/"thresholded_state_update_candidate_windows.csv", index=False)
    summary_rows = []
    if len(cand):
        focus = cand[(cand["theta_metric"].astype(str).str.contains("plv_theta_4_8_primary", na=False)) & (cand["post_window"] == "10-30s_after_taper")]
        if len(focus):
            best = focus.sort_values("target_minus_override_delta", ascending=False).iloc[0]
            summary_rows.append({
                "endpoint": "ThresholdedStateUpdate_v1",
                "best_anchor_id": best.get("anchor_id"),
                "best_target_minus_override_delta": best.get("target_minus_override_delta"),
                "best_grade": best.get("state_update_grade"),
                "interpretation": "candidate state-update window; exploratory unless pre-frozen and replicated",
            })
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(out/"tables"/"thresholded_state_update_summary.csv", index=False)
    logger("Thresholded State-Update module complete.")
    return cand, summary


def _build_anchor_table(peaks: "pd.DataFrame", annotations: "pd.DataFrame") -> "pd.DataFrame":
    rows = []
    if peaks is not None and len(peaks):
        for _, p in peaks.iterrows():
            if np.isfinite(float(p.get("taper_rel_sec", np.nan))):
                rows.append({
                    "anchor_id": p.get("anchor_id", ""),
                    "anchor_source": "gamma_or_tsp_taper",
                    "anchor_rel_sec": float(p.get("taper_rel_sec")),
                    "predictor_label": p.get("predictor_label", ""),
                    "scope": p.get("scope", ""),
                    "status": p.get("status", ""),
                })
    if annotations is not None and len(annotations):
        for _, a in annotations.iterrows():
            try:
                anchor = float(a.get("end_sec", np.nan))
            except Exception:
                anchor = np.nan
            if np.isfinite(anchor):
                rows.append({
                    "anchor_id": a.get("event_id", ""),
                    "anchor_source": "annotation_end",
                    "anchor_rel_sec": anchor,
                    "predictor_label": a.get("event_type", ""),
                    "scope": a.get("phase", "TARGET_VIDEO"),
                    "status": "annotation_supplied",
                })
    return pd.DataFrame(rows)


def run_state_locked_handoff_alignment(features: "pd.DataFrame", peaks: "pd.DataFrame", annotations: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> Dict[str, "pd.DataFrame"]:
    """Export state-aligned epochs and a minimal state-vs-video/random model comparison."""
    df = add_relative_time(features)
    if df is None or len(df) == 0:
        empty = pd.DataFrame()
        empty.to_csv(out/"tables"/"state_locked_anchor_summary.csv", index=False)
        empty.to_csv(out/"tables"/"state_locked_epochs_long.csv", index=False)
        empty.to_csv(out/"tables"/"state_locked_model_comparison.csv", index=False)
        return {"anchors": empty, "epochs": empty, "comparison": empty}
    if "artifact_score" not in df.columns:
        df["artifact_score"] = artifact_score(df)
    if peaks is None or len(peaks) == 0:
        peaks = detect_peak_and_taper(df, cfg, out)
    anchors = _build_anchor_table(peaks, annotations)
    metrics = _state_locked_metric_columns(df)
    epoch_rows = []
    for _, a in anchors.iterrows():
        anchor = float(a.get("anchor_rel_sec", np.nan))
        if not np.isfinite(anchor):
            continue
        for seg in ["TARGET_1", "CONTROL_1", "CONTEXTUAL_OVERRIDE_1"]:
            sub = df[(df["segment"] == seg) & (df["rel_mid_sec"] >= anchor - 30) & (df["rel_mid_sec"] <= anchor + 60)].copy()
            for _, r in sub.iterrows():
                row = {
                    "anchor_id": a.get("anchor_id", ""),
                    "anchor_source": a.get("anchor_source", ""),
                    "predictor_label": a.get("predictor_label", ""),
                    "anchor_rel_sec": anchor,
                    "segment": seg,
                    "tau_sec": float(r.get("rel_mid_sec", np.nan)) - anchor,
                }
                for m in metrics:
                    row[m] = r.get(m, np.nan)
                epoch_rows.append(row)
    epochs = pd.DataFrame(epoch_rows)
    anchors.to_csv(out/"tables"/"state_locked_anchor_summary.csv", index=False)
    epochs.to_csv(out/"tables"/"state_locked_epochs_long.csv", index=False)
    # Model comparison: state anchor vs video-end vs random anchors for primary theta PLV if available.
    comp_rows = []
    theta = "plv_theta_4_8_primary_content_core" if "plv_theta_4_8_primary_content_core" in df.columns else None
    if theta and len(anchors):
        rng = np.random.default_rng(int(getattr(cfg, "random_seed", 20260724)))
        target = df[df["segment"] == "TARGET_1"]
        dur = float(target["rel_mid_sec"].max()) if len(target) and "rel_mid_sec" in target.columns else np.nan
        def delta_at(anchor):
            pre = _window_mean(df, "TARGET_1", theta, max(0, anchor-30), max(0, anchor-5))
            post = _window_mean(df, "TARGET_1", theta, anchor+10, anchor+30)
            return post-pre if np.isfinite(post) and np.isfinite(pre) else np.nan
        state_vals = [delta_at(float(a)) for a in anchors["anchor_rel_sec"] if np.isfinite(float(a))]
        state_best = np.nanmax(state_vals) if len(state_vals) and np.isfinite(state_vals).any() else np.nan
        video_end_anchor = max(0.0, dur - 0.001) if np.isfinite(dur) else np.nan
        video_val = delta_at(video_end_anchor) if np.isfinite(video_end_anchor) else np.nan
        rand_vals = []
        if np.isfinite(dur) and dur > 90:
            for _ in range(min(200, int(getattr(cfg, "n_surrogates", 500)))):
                rand_vals.append(delta_at(float(rng.uniform(45, max(46, dur-60)))))
        rand_mean = float(np.nanmean(rand_vals)) if len(rand_vals) else np.nan
        rand_std = float(np.nanstd(rand_vals)) if len(rand_vals) else np.nan
        z_vs_rand = (state_best-rand_mean)/rand_std if np.isfinite(state_best) and np.isfinite(rand_mean) and rand_std>0 else np.nan
        comp_rows.append({"model":"M3_state_locked","anchor":"gamma/TSP/annotation taper","theta_metric":theta,"best_state_delta":state_best,"video_end_delta":video_val,"random_anchor_mean":rand_mean,"random_anchor_std":rand_std,"z_vs_random":z_vs_rand,"interpretation":"state anchor favored" if np.isfinite(state_best) and np.isfinite(video_val) and state_best>video_val else "state anchor not clearly better than video end"})
    comp = pd.DataFrame(comp_rows)
    comp.to_csv(out/"tables"/"state_locked_model_comparison.csv", index=False)
    # DTW readiness note rather than unconstrained use by default.
    note = out/"tables"/"dtw_readiness_note.md"
    note.write_text("# DTW readiness note\n\nConstrained DTW is disabled by default. Use it only after repeated same-stimulus runs or multi-subject data exist, with pre-frozen anchors and the same warping constraints applied to Target, Control, Override, and pseudo-events. Report unwarped state-aligned epochs first.\n", encoding="utf-8")
    logger("State-Locked Handoff Alignment module complete.")
    return {"anchors": anchors, "epochs": epochs, "comparison": comp}



# ---------------------------
# Human Translation K_HT v0.2
# ---------------------------

def _first_numeric_col(df: "pd.DataFrame", candidates: Sequence[str]) -> Optional[str]:
    if df is None or len(df) == 0:
        return None
    cols = set(df.columns)
    for c in candidates:
        if c in cols:
            return c
    # Fuzzy fallback: exact candidates are preferred; these keep old ad hoc tables usable.
    lower_map = {str(c).lower(): c for c in df.columns}
    for c in candidates:
        lc = c.lower()
        if lc in lower_map:
            return lower_map[lc]
    return None


def _z_safe(x: "pd.Series") -> "pd.Series":
    arr = pd.to_numeric(x, errors="coerce").astype(float)
    mu = arr.mean(skipna=True)
    sd = arr.std(skipna=True)
    if not np.isfinite(sd) or sd == 0:
        return pd.Series(np.zeros(len(arr)), index=x.index, dtype=float)
    return (arr - mu) / sd


def _segment_col(df: "pd.DataFrame") -> Optional[str]:
    for c in ["segment", "phase", "condition", "analysis_segment", "branch", "arm", "block"]:
        if c in df.columns:
            return c
    return None


def _time_col(df: "pd.DataFrame") -> Optional[str]:
    for c in ["condition_offset_sec", "analysis_time", "time_sec", "window_mid", "mid_lsl", "rel_mid_sec", "rel_t", "t0", "window_start", "start_lsl", "time_lsl"]:
        if c in df.columns:
            return c
    return None


def _construct_tsp_proxy(df: "pd.DataFrame") -> Tuple["pd.Series", Dict[str, Any]]:
    """Construct a posterior-temporal / semantic proxy when no ready-made TSP column exists."""
    direct = _first_numeric_col(df, [
        "tsp_z", "tsp_raw_z", "tsp_raw",
        "TemporalSemanticProxy_lgamma_30_45", "TemporalSemanticProxy_low_gamma_30_45",
        "TSP_gamma", "temporal_proxy_lgamma_30_45", "temporal_proxy_low_gamma_30_45",
        "z_logbp_posterior_temporal_low_gamma_30_45_minus_task_visual_jaw",
    ])
    if direct:
        return _z_safe(df[direct]), {"source": direct, "constructed": False}
    pt = _first_numeric_col(df, [
        "pow_lgamma_30_45_posterior_temporal", "lgamma_30_45_posterior_temporal", "lgamma_30_45_posterior_temporal_proxy",
        "logbp_posterior_temporal_low_gamma_30_45", "z_logbp_posterior_temporal_low_gamma_30_45",
        "logbp_meaning_candidate_low_gamma_30_45", "z_logbp_meaning_candidate_low_gamma_30_45",
    ])
    fp = _first_numeric_col(df, [
        "pow_lgamma_30_45_frontoparietal_task", "lgamma_30_45_frontoparietal_task", "logbp_frontoparietal_task_low_gamma_30_45", "z_logbp_frontoparietal_task_low_gamma_30_45"
    ])
    vc = _first_numeric_col(df, [
        "pow_lgamma_30_45_visual_control", "lgamma_30_45_visual_control", "logbp_visual_control_low_gamma_30_45", "z_logbp_visual_control_low_gamma_30_45"
    ])
    jaw = _first_numeric_col(df, [
        "pow_lgamma_30_45_jaw_temporal_sentinel", "lgamma_30_45_jaw_temporal_sentinel", "logbp_jaw_temporal_sentinel_low_gamma_30_45", "z_logbp_jaw_temporal_sentinel_low_gamma_30_45"
    ])
    art = _first_numeric_col(df, ["artifact_score", "artifact_p2p_median", "median_p2p", "amp_rms_all", "z_logbp_artifact_sentinel_hf_proxy_45_55"])
    if not pt:
        return pd.Series(np.nan, index=df.index, dtype=float), {"source":"not_found", "constructed": False}
    y = _z_safe(df[pt])
    used = {"pt": pt}
    if fp: y = y - 0.35 * _z_safe(df[fp]); used["frontoparietal"] = fp
    if vc: y = y - 0.35 * _z_safe(df[vc]); used["visual"] = vc
    if jaw: y = y - 0.50 * _z_safe(df[jaw]); used["jaw"] = jaw
    if art: y = y - 0.25 * _z_safe(df[art]); used["artifact"] = art
    return y, {"source": json.dumps(used), "constructed": True}


def inventory_media_covariates(cfg: SuiteConfig, out: Path, logger: RunLogger) -> "pd.DataFrame":
    """Record whether time-resolved media covariates are present. This does not overclaim sensory subtraction."""
    rows = []
    for label, path in [("media_manifest_json", cfg.media_manifest_json), ("stimulus_fingerprint_folder", cfg.stimulus_fingerprint_folder), ("cue_schedule_json", cfg.cue_schedule_json)]:
        if not path:
            rows.append({"source_type": label, "path": "", "exists": False, "time_resolved_detected": False, "notes": "not supplied"})
            continue
        p = Path(path).expanduser()
        if p.is_dir():
            candidates = list(p.rglob("*.csv")) + list(p.rglob("*.json"))
            time_like = []
            for f in candidates[:200]:
                try:
                    if f.suffix.lower() == ".csv":
                        head = pd.read_csv(f, nrows=5)
                        cols = [str(c).lower() for c in head.columns]
                    else:
                        txt = f.read_text(encoding="utf-8", errors="ignore")[:2000].lower()
                        cols = [txt]
                    if any(k in " ".join(cols) for k in ["time", "sec", "frame", "luminance", "audio", "rms", "optical", "cut"]):
                        time_like.append(str(f))
                except Exception:
                    pass
            rows.append({"source_type": label, "path": str(p), "exists": p.exists(), "time_resolved_detected": bool(time_like), "n_candidate_files": len(candidates), "notes": "; ".join(time_like[:5]) if time_like else "no obvious media covariate table found"})
        else:
            rows.append({"source_type": label, "path": str(p), "exists": p.exists(), "time_resolved_detected": False, "n_candidate_files": 1 if p.exists() else 0, "notes": "file supplied; parsed by other suite modules if applicable"})
    df = pd.DataFrame(rows)
    df.to_csv(out/"tables"/"human_translation_kht_media_covariate_inventory.csv", index=False)
    return df


def _fit_ols(y: np.ndarray, X: np.ndarray) -> Tuple[np.ndarray, float, int]:
    mask = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    if mask.sum() < max(8, X.shape[1] + 3):
        return np.full(X.shape[1], np.nan), np.nan, int(mask.sum())
    beta, *_ = np.linalg.lstsq(X[mask], y[mask], rcond=None)
    pred = X[mask] @ beta
    mse = float(np.mean((y[mask]-pred)**2)) if mask.sum() else np.nan
    return beta, mse, int(mask.sum())


def _phasewise_reciprocal_fit(df: "pd.DataFrame", seg_col: str) -> "pd.DataFrame":
    rows = []
    controls = [c for c in ["visual_proxy_z", "task_proxy_z", "artifact_proxy_z", "theta_proxy_z"] if c in df.columns]
    for seg in ["BASELINE_1", "CONTROL_1", "TARGET_1", "CONTEXTUAL_OVERRIDE_1", "WASHOUT_2"]:
        sub = df[df[seg_col].astype(str) == seg].copy()
        if len(sub) < 8:
            continue
        sub = sub.sort_values("analysis_time")
        sub["E_lag1"] = sub["E_gamma_z"].shift(1)
        sub["Y_lag1"] = sub["Y_proxy_z"].shift(1)
        # E equation: E_t ~ Y_{t-1} + E_{t-1} + controls
        X1_cols = ["Y_lag1", "E_lag1"] + controls
        X1 = np.column_stack([np.ones(len(sub))] + [pd.to_numeric(sub[c], errors="coerce").to_numpy(float) for c in X1_cols])
        b1, mse1, n1 = _fit_ols(pd.to_numeric(sub["E_gamma_z"], errors="coerce").to_numpy(float), X1)
        # Y equation: Y_t ~ E_{t-1} + Y_{t-1} + controls
        X2_cols = ["E_lag1", "Y_lag1"] + controls
        X2 = np.column_stack([np.ones(len(sub))] + [pd.to_numeric(sub[c], errors="coerce").to_numpy(float) for c in X2_cols])
        b2, mse2, n2 = _fit_ols(pd.to_numeric(sub["Y_proxy_z"], errors="coerce").to_numpy(float), X2)
        eta = float(b1[1]) if len(b1) > 1 else np.nan       # Y -> E
        zeta = float(b2[1]) if len(b2) > 1 else np.nan      # E -> Y
        prod = eta * zeta if np.isfinite(eta) and np.isfinite(zeta) else np.nan
        k_signed = math.copysign(math.sqrt(abs(prod)), prod) if np.isfinite(prod) else np.nan
        k_pos = math.sqrt(prod) if np.isfinite(prod) and prod > 0 else 0.0 if np.isfinite(prod) else np.nan
        rows.append({
            "segment": seg, "n_windows": min(n1, n2),
            "eta_Y_to_E_std": eta, "zeta_E_to_Y_std": zeta,
            "K_HT_signed_sqrt_product": k_signed, "K_HT_positive_loop": k_pos,
            "loop_product_eta_zeta": prod,
            "mse_E_equation": mse1, "mse_Y_equation": mse2,
            "interpretation": "positive reciprocal loop" if np.isfinite(prod) and prod > 0 else "mixed-sign/no positive reciprocal loop"
        })
    return pd.DataFrame(rows)


def _cv_model_comparison(df: "pd.DataFrame", seg_col: str, rng_seed: int = 20260724) -> Tuple["pd.DataFrame", "pd.DataFrame"]:
    d = df[df[seg_col].astype(str).isin(["CONTROL_1", "TARGET_1", "CONTEXTUAL_OVERRIDE_1"])].copy()
    if len(d) < 30:
        return pd.DataFrame(), pd.DataFrame()
    d = d.sort_values([seg_col, "analysis_time"]).reset_index(drop=True)
    d["E_lag1"] = d.groupby(seg_col)["E_gamma_z"].shift(1)
    d["Y_lag1"] = d.groupby(seg_col)["Y_proxy_z"].shift(1)
    d["fold"] = np.arange(len(d)) % 5
    models = {
        "full_reciprocal": ["E_lag1", "Y_lag1", "visual_proxy_z", "task_proxy_z", "artifact_proxy_z"],
        "replay_only_E_AR": ["E_lag1", "visual_proxy_z", "task_proxy_z", "artifact_proxy_z"],
        "sensory_task_artifact": ["visual_proxy_z", "task_proxy_z", "artifact_proxy_z"],
        "generic_theta_artifact": ["E_lag1", "theta_proxy_z", "artifact_proxy_z"],
        "Y_proxy_AR_only": ["Y_lag1", "visual_proxy_z", "artifact_proxy_z"],
    }
    losses=[]
    for fold in sorted(d["fold"].dropna().unique()):
        train = d[d["fold"] != fold]
        test = d[d["fold"] == fold]
        for name, cols in models.items():
            cols2 = [c for c in cols if c in d.columns]
            Xtr = np.column_stack([np.ones(len(train))] + [pd.to_numeric(train[c], errors="coerce").to_numpy(float) for c in cols2])
            ytr = pd.to_numeric(train["E_gamma_z"], errors="coerce").to_numpy(float)
            beta, _, ntrain = _fit_ols(ytr, Xtr)
            Xte = np.column_stack([np.ones(len(test))] + [pd.to_numeric(test[c], errors="coerce").to_numpy(float) for c in cols2])
            yte = pd.to_numeric(test["E_gamma_z"], errors="coerce").to_numpy(float)
            mask = np.isfinite(yte) & np.all(np.isfinite(Xte), axis=1) & np.all(np.isfinite(beta))
            mse = float(np.mean((yte[mask] - Xte[mask]@beta)**2)) if mask.sum() else np.nan
            losses.append({"fold": int(fold), "model": name, "test_mse_E": mse, "n_train": ntrain, "n_test": int(mask.sum()), "predictors": ",".join(cols2)})
    loss = pd.DataFrame(losses)
    wins=[]
    if len(loss):
        for fold, sub in loss.dropna(subset=["test_mse_E"]).groupby("fold"):
            if len(sub):
                best = sub.sort_values("test_mse_E").iloc[0]
                wins.append({"fold": int(fold), "winning_model": best["model"], "winning_mse": best["test_mse_E"]})
    win_df = pd.DataFrame(wins)
    if len(win_df):
        summ = win_df["winning_model"].value_counts().rename_axis("model").reset_index(name="fold_wins")
        summ["win_rate"] = summ["fold_wins"] / max(1, len(win_df))
    else:
        summ = pd.DataFrame()
    return loss, summ


def run_human_translation_kht(features: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> Dict[str, "pd.DataFrame"]:
    """
    HumanTranslation_KHT_v0.2.

    This is a rough human translation module, not OSM proof. It estimates a standardized reciprocal-loop
    coupling between an EEG gamma/work proxy E_human(t) and a human translation proxy Y_HT(t). It treats
    media fingerprint/QC information as exogenous input inventory rather than a direct biological Y channel.
    """
    media_inv = inventory_media_covariates(cfg, out, logger)
    if features is None or len(features) == 0:
        empty = pd.DataFrame()
        empty.to_csv(out/"tables"/"human_translation_kht_feature_frame.csv", index=False)
        empty.to_csv(out/"tables"/"human_translation_kht_phasewise_summary.csv", index=False)
        empty.to_csv(out/"tables"/"human_translation_kht_cv_model_losses.csv", index=False)
        empty.to_csv(out/"tables"/"human_translation_kht_cv_win_summary.csv", index=False)
        safe_json_dump({"status":"not_evaluable", "reason":"no feature table", "boundary":"K_HT is not K_OSM and cannot prove Opto-Structural Memory."}, out/"tables"/"human_translation_kht_interpretation.json")
        return {"media_inventory": media_inv, "feature_frame": empty, "phasewise": empty, "cv_losses": empty, "cv_wins": empty}
    df = standardize_feature_columns(features).copy()
    seg_col = _segment_col(df)
    tcol = _time_col(df)
    if not seg_col or not tcol:
        logger("HumanTranslation_KHT not evaluable: no segment/phase and time columns.")
        return {"media_inventory": media_inv, "feature_frame": pd.DataFrame(), "phasewise": pd.DataFrame(), "cv_losses": pd.DataFrame(), "cv_wins": pd.DataFrame()}
    df["analysis_segment"] = df[seg_col].map(_normalize_branch_for_anchor)
    df["analysis_time"] = pd.to_numeric(df[tcol], errors="coerce")
    e_col = _first_numeric_col(df, [
        "gamma_z", "lgamma_posterior_temporal_z", "lgamma_global_z",
        "MeaningGamma_phys", "MeaningGamma_lgamma_30_45", "GammaPrimary", "pow_lgamma_30_45_primary_content_core",
        "lgamma_30_45_primary_content_core", "logbp_meaning_candidate_low_gamma_30_45", "logbp_posterior_temporal_low_gamma_30_45",
        "z_logbp_posterior_temporal_low_gamma_30_45", "pow_lgamma_30_45_all_channels", "lgamma_30_45_non_sentinel_all",
    ])
    visual_col = _first_numeric_col(df, ["pow_lgamma_30_45_visual_control", "lgamma_30_45_visual_control", "logbp_visual_control_low_gamma_30_45", "z_logbp_visual_control_low_gamma_30_45"])
    task_col = _first_numeric_col(df, ["TaskGamma", "TaskGamma_lgamma_30_45", "pow_lgamma_30_45_frontoparietal_task", "lgamma_30_45_frontoparietal_task", "logbp_frontoparietal_task_low_gamma_30_45", "z_logbp_frontoparietal_task_low_gamma_30_45"])
    artifact_col = _first_numeric_col(df, ["artifact_ratio_lgamma_z", "lgamma_artifact_sentinel_z", "ptp_artifact_median_uV", "artifact_score", "artifact_p2p_median", "median_p2p", "amp_rms_all", "z_logbp_artifact_sentinel_hf_proxy_45_55", "logbp_artifact_sentinel_hf_proxy_45_55"])
    theta_col = _first_numeric_col(df, ["theta_z", "theta_midline_z", "theta_global_z", "ThetaPLV_primary", "plv_theta_4_8_primary_content_core", "theta_4_8_primary_content_core", "logbp_meaning_candidate_theta_4_8", "pow_theta_4_8_primary_content_core"])
    y_proxy, y_info = _construct_tsp_proxy(df)
    if e_col:
        df["E_gamma_z"] = _z_safe(df[e_col])
    else:
        df["E_gamma_z"] = np.nan
    df["Y_proxy_z"] = y_proxy
    df["V_proxy_z"] = df.groupby("analysis_segment")["Y_proxy_z"].diff().fillna(0.0)
    df["visual_proxy_z"] = _z_safe(df[visual_col]) if visual_col else 0.0
    df["task_proxy_z"] = _z_safe(df[task_col]) if task_col else 0.0
    df["artifact_proxy_z"] = _z_safe(df[artifact_col]) if artifact_col else 0.0
    df["theta_proxy_z"] = _z_safe(df[theta_col]) if theta_col else 0.0
    # store columns used
    used = pd.DataFrame([{
        "E_human_column": e_col or "not_found", "Y_HT_proxy_source": y_info.get("source"), "Y_HT_proxy_constructed": y_info.get("constructed"),
        "visual_column": visual_col or "not_found", "task_column": task_col or "not_found", "artifact_column": artifact_col or "not_found", "theta_column": theta_col or "not_found",
        "boundary": "This module estimates K_HT, a human translation coupling proxy. It does not estimate K_OSM or prove Opto-Structural Memory."
    }])
    used.to_csv(out/"tables"/"human_translation_kht_columns_used.csv", index=False)
    keep = ["analysis_segment", "analysis_time", "E_gamma_z", "Y_proxy_z", "V_proxy_z", "visual_proxy_z", "task_proxy_z", "artifact_proxy_z", "theta_proxy_z"]
    df[keep].to_csv(out/"tables"/"human_translation_kht_feature_frame.csv", index=False)
    phasewise = _phasewise_reciprocal_fit(df, "analysis_segment")
    phasewise.to_csv(out/"tables"/"human_translation_kht_phasewise_summary.csv", index=False)
    # contrast summary
    def val(seg, col):
        s = phasewise[phasewise["segment"] == seg]
        return float(s[col].iloc[0]) if len(s) and col in s.columns else np.nan
    summary = {
        "status": "exploratory",
        "primary_endpoint": "K_HT_positive_loop",
        "target_K_HT": val("TARGET_1", "K_HT_positive_loop"),
        "control_K_HT": val("CONTROL_1", "K_HT_positive_loop"),
        "override_K_HT": val("CONTEXTUAL_OVERRIDE_1", "K_HT_positive_loop"),
        "target_minus_control_K_HT": val("TARGET_1", "K_HT_positive_loop") - val("CONTROL_1", "K_HT_positive_loop") if np.isfinite(val("TARGET_1", "K_HT_positive_loop")) and np.isfinite(val("CONTROL_1", "K_HT_positive_loop")) else np.nan,
        "target_minus_override_K_HT": val("TARGET_1", "K_HT_positive_loop") - val("CONTEXTUAL_OVERRIDE_1", "K_HT_positive_loop") if np.isfinite(val("TARGET_1", "K_HT_positive_loop")) and np.isfinite(val("CONTEXTUAL_OVERRIDE_1", "K_HT_positive_loop")) else np.nan,
        "pass_rule_v0_2": "pilot_positive only if Target K_HT > Control and Target K_HT > Override, full reciprocal model wins CV, and artifact/timing/media covariates are not dominant",
        "boundary": "K_HT is a rough human-translation endpoint. It is not K_OSM, Y_cell, Y_OSM, LTP, microtubular memory, or proof of an opto-structural mechanism."
    }
    cv_loss, cv_win = _cv_model_comparison(df, "analysis_segment", int(getattr(cfg, "random_seed", 20260724)))
    cv_loss.to_csv(out/"tables"/"human_translation_kht_cv_model_losses.csv", index=False)
    cv_win.to_csv(out/"tables"/"human_translation_kht_cv_win_summary.csv", index=False)
    full_win = float(cv_win.loc[cv_win["model"]=="full_reciprocal", "win_rate"].iloc[0]) if len(cv_win) and "full_reciprocal" in set(cv_win["model"]) else 0.0
    summary["full_reciprocal_cv_win_rate"] = full_win
    summary["rough_interpretation"] = "candidate_positive" if (np.isfinite(summary["target_minus_control_K_HT"]) and np.isfinite(summary["target_minus_override_K_HT"]) and summary["target_minus_control_K_HT"]>0 and summary["target_minus_override_K_HT"]>0 and full_win>=0.5) else "not_a_clean_K_HT_pass"
    safe_json_dump(summary, out/"tables"/"human_translation_kht_interpretation.json")
    logger("HumanTranslation_KHT_v0.2 module complete.")
    return {"media_inventory": media_inv, "feature_frame": df[keep], "phasewise": phasewise, "cv_losses": cv_loss, "cv_wins": cv_win, "interpretation": pd.DataFrame([summary])}



# ----------------------- CandidateLocal_KHT_v0.2 -----------------------

def _candidate_col(df: "pd.DataFrame", names: Sequence[str]) -> Optional[str]:
    lower = {c.lower(): c for c in df.columns}
    for n in names:
        if n.lower() in lower:
            return lower[n.lower()]
    for n in names:
        for c in df.columns:
            if n.lower() in c.lower():
                return c
    return None


def _safe_float(x: Any, default: float = np.nan) -> float:
    try:
        v = float(x)
        return v if np.isfinite(v) else default
    except Exception:
        return default


def _ols_coeff(y: "np.ndarray", cols: List["np.ndarray"]) -> Tuple["np.ndarray", float, int]:
    X = np.column_stack([np.ones(len(y))] + cols)
    mask = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    if mask.sum() < max(6, X.shape[1] + 2):
        return np.full(X.shape[1], np.nan), np.nan, int(mask.sum())
    try:
        beta, *_ = np.linalg.lstsq(X[mask], y[mask], rcond=None)
        resid = y[mask] - X[mask] @ beta
        return beta, float(np.mean(resid ** 2)), int(mask.sum())
    except Exception:
        return np.full(X.shape[1], np.nan), np.nan, int(mask.sum())


def _normalize_branch_for_anchor(x: Any) -> str:
    v = str(x or "").upper()
    if "TARGET" in v:
        return "TARGET_1"
    if "OVERRIDE" in v or "CONTEXTUAL" in v:
        return "CONTEXTUAL_OVERRIDE_1"
    if "CONTROL" in v or "SCRAMB" in v:
        return "CONTROL_1"
    return v or "UNKNOWN"


def _load_predeclared_anchor_file(path: str, logger: RunLogger) -> "pd.DataFrame":
    if not path or not Path(path).exists():
        return pd.DataFrame()
    p = Path(path)
    try:
        if p.suffix.lower() == ".csv":
            return pd.read_csv(p)
        obj = json.loads(p.read_text(encoding="utf-8"))
        rows = []
        if isinstance(obj, dict):
            if isinstance(obj.get("anchors"), list):
                rows = obj["anchors"]
            elif isinstance(obj.get("anchor_events"), list):
                rows = obj["anchor_events"]
            else:
                rows = [obj]
        elif isinstance(obj, list):
            rows = obj
        return pd.DataFrame(rows)
    except Exception as exc:
        logger(f"WARNING: could not load predeclared anchor file {path}: {exc}")
        return pd.DataFrame()


def _anchor_rows_from_df(df: "pd.DataFrame", source_name: str, default_claim: str = "exploratory") -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if df is None or len(df) == 0:
        return rows
    id_col = _candidate_col(df, ["anchor_id", "event_id", "label", "name", "candidate_id"])
    seg_col = _candidate_col(df, ["condition", "phase", "segment", "analysis_segment", "branch"])
    time_col = _candidate_col(df, ["rendered_time_sec", "time_sec", "peak_sec", "peak_time", "peak_offset_sec", "anchor_time_sec", "analysis_time", "start_sec"])
    claim_col = _candidate_col(df, ["claim_level", "anchor_source", "source"])
    desc_col = _candidate_col(df, ["description", "scene_description", "note", "notes", "interpretation"])
    if not time_col:
        return rows
    for i, r in df.iterrows():
        t = _safe_float(r.get(time_col))
        if not np.isfinite(t):
            continue
        raw_id = str(r.get(id_col, f"{source_name}_{i:03d}")) if id_col else f"{source_name}_{i:03d}"
        raw_seg = _normalize_branch_for_anchor(r.get(seg_col, "TARGET_1") if seg_col else "TARGET_1")
        raw_claim = str(r.get(claim_col, default_claim)) if claim_col else default_claim
        # explicit source prefix helps later interpretation.
        if source_name not in raw_claim:
            raw_claim = f"{source_name}:{raw_claim}"
        rows.append({
            "anchor_id": re.sub(r"[^A-Za-z0-9_.-]+", "_", raw_id).strip("_") or f"{source_name}_{i:03d}",
            "condition": raw_seg,
            "time_sec": t,
            "anchor_source": source_name,
            "claim_level": raw_claim,
            "description": str(r.get(desc_col, "")) if desc_col else "",
        })
    return rows


def _top_feature_anchors(df: "pd.DataFrame", n_per_segment: int = 5) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    d = df.copy()
    if "analysis_segment" not in d.columns or "analysis_time" not in d.columns:
        return rows
    d["candidate_composite"] = _z_safe(d.get("E_gamma_z", 0.0)) + _z_safe(d.get("Y_proxy_z", 0.0)) - 0.5 * _z_safe(d.get("artifact_proxy_z", 0.0))
    for seg, sub in d[d["analysis_segment"].isin(["CONTROL_1", "TARGET_1", "CONTEXTUAL_OVERRIDE_1"])].groupby("analysis_segment"):
        sub = sub.dropna(subset=["analysis_time", "candidate_composite"]).sort_values("candidate_composite", ascending=False).head(n_per_segment)
        for j, r in sub.iterrows():
            rows.append({
                "anchor_id": f"PHYSIO_EXPLORATORY_{seg}_{int(round(float(r['analysis_time'])))}S",
                "condition": seg,
                "time_sec": float(r["analysis_time"]),
                "anchor_source": "physiology_exploratory_top_composite",
                "claim_level": "exploratory_only",
                "description": "Auto-selected top E/Y/artifact-guarded composite candidate. Cannot be confirmatory in the same run.",
            })
    return rows


def _prepare_candidate_kht_frame(features: "pd.DataFrame") -> "pd.DataFrame":
    df = standardize_feature_columns(features).copy()
    seg_col = _segment_col(df)
    tcol = _time_col(df)
    if not seg_col or not tcol:
        return pd.DataFrame()
    df["analysis_segment"] = df[seg_col].map(_normalize_branch_for_anchor)
    df["analysis_time"] = pd.to_numeric(df[tcol], errors="coerce")
    e_col = _first_numeric_col(df, [
        "gamma_z", "lgamma_posterior_temporal_z", "lgamma_global_z",
        "MeaningGamma_phys", "MeaningGamma_lgamma_30_45", "GammaPrimary", "pow_lgamma_30_45_primary_content_core",
        "lgamma_30_45_primary_content_core", "logbp_meaning_candidate_low_gamma_30_45", "logbp_posterior_temporal_low_gamma_30_45",
        "z_logbp_posterior_temporal_low_gamma_30_45", "pow_lgamma_30_45_all_channels", "lgamma_30_45_non_sentinel_all",
    ])
    artifact_col = _first_numeric_col(df, ["artifact_ratio_lgamma_z", "lgamma_artifact_sentinel_z", "ptp_artifact_median_uV", "artifact_score", "artifact_p2p_median", "median_p2p", "amp_rms_all", "z_logbp_artifact_sentinel_hf_proxy_45_55", "logbp_artifact_sentinel_hf_proxy_45_55"])
    theta_col = _first_numeric_col(df, ["theta_z", "theta_midline_z", "theta_global_z", "ThetaPLV_primary", "plv_theta_4_8_primary_content_core", "theta_4_8_primary_content_core", "logbp_meaning_candidate_theta_4_8", "pow_theta_4_8_primary_content_core"])
    y_proxy, _ = _construct_tsp_proxy(df)
    df["E_gamma_z"] = _z_safe(df[e_col]) if e_col else np.nan
    df["Y_proxy_z"] = y_proxy
    df["artifact_proxy_z"] = _z_safe(df[artifact_col]) if artifact_col else 0.0
    df["theta_proxy_z"] = _z_safe(df[theta_col]) if theta_col else np.nan
    return df[["analysis_segment", "analysis_time", "E_gamma_z", "Y_proxy_z", "artifact_proxy_z", "theta_proxy_z"]].dropna(subset=["analysis_time"])


def _local_kht_at_anchor(df: "pd.DataFrame", condition: str, t: float, local_pre: float = 10.0, local_post: float = 10.0) -> Dict[str, Any]:
    sub = df[(df["analysis_segment"].astype(str) == condition) & (df["analysis_time"].between(t - local_pre, t + local_post))].copy().sort_values("analysis_time")
    if len(sub) < 8:
        return {"n_local": int(len(sub)), "eta_Y_to_E": np.nan, "zeta_E_to_Y": np.nan, "K_local": np.nan, "K_signed": np.nan, "loop_product": np.nan, "mse_E": np.nan, "mse_Y": np.nan}
    sub["E_next"] = sub["E_gamma_z"].shift(-1)
    sub["Y_next"] = sub["Y_proxy_z"].shift(-1)
    sub["E_lag"] = sub["E_gamma_z"]
    sub["Y_lag"] = sub["Y_proxy_z"]
    art = pd.to_numeric(sub.get("artifact_proxy_z", 0.0), errors="coerce").to_numpy(float)
    bE, mseE, nE = _ols_coeff(pd.to_numeric(sub["E_next"], errors="coerce").to_numpy(float), [pd.to_numeric(sub["E_lag"], errors="coerce").to_numpy(float), pd.to_numeric(sub["Y_lag"], errors="coerce").to_numpy(float), art])
    bY, mseY, nY = _ols_coeff(pd.to_numeric(sub["Y_next"], errors="coerce").to_numpy(float), [pd.to_numeric(sub["Y_lag"], errors="coerce").to_numpy(float), pd.to_numeric(sub["E_lag"], errors="coerce").to_numpy(float), art])
    eta = float(bE[2]) if len(bE) > 2 else np.nan       # Y -> E, after E autoregression
    zeta = float(bY[2]) if len(bY) > 2 else np.nan      # E -> Y, after Y autoregression
    prod = eta * zeta if np.isfinite(eta) and np.isfinite(zeta) else np.nan
    k = math.sqrt(abs(prod)) if np.isfinite(prod) else np.nan
    ks = math.copysign(k, prod) if np.isfinite(k) and np.isfinite(prod) else np.nan
    return {"n_local": int(min(nE, nY)), "eta_Y_to_E": eta, "zeta_E_to_Y": zeta, "K_local": k, "K_signed": ks, "loop_product": prod, "mse_E": mseE, "mse_Y": mseY}


def _paired_washout_for_condition(condition: str) -> str:
    c = _normalize_branch_for_anchor(condition)
    if c == "CONTROL_1":
        return "WASHOUT_1"
    if c == "TARGET_1":
        return "WASHOUT_2"
    if c == "CONTEXTUAL_OVERRIDE_1":
        return "WASHOUT_3"
    return ""


def _theta_handoff_at_anchor(df: "pd.DataFrame", condition: str, t: float, followup_policy: str = "paired_washout_continuation") -> Dict[str, Any]:
    """Theta follow-up around a candidate event.

    v0.1 used strict within-phase windows only. v0.2 permits outcome windows to continue
    into the paired formal washout while keeping the local K-estimation window branch-local.
    This avoids discarding end-of-clip gamma/TSP peaks whose integration response occurs after
    the movie marker. The continuation is restricted to the paired washout only:

      CONTROL_1 -> WASHOUT_1
      TARGET_1 -> WASHOUT_2
      CONTEXTUAL_OVERRIDE_1 -> WASHOUT_3

    It never crosses into report screens, instruction screens, or another stimulus branch.
    """
    condition = _normalize_branch_for_anchor(condition)
    paired = _paired_washout_for_condition(condition)
    d_phase = df[df["analysis_segment"].astype(str) == condition].copy()
    d_pair = df[df["analysis_segment"].astype(str) == paired].copy() if paired else pd.DataFrame()
    phase_end = float(pd.to_numeric(d_phase["analysis_time"], errors="coerce").max()) if len(d_phase) else np.nan

    def mean_strict(a: float, b: float):
        s = pd.to_numeric(d_phase.loc[d_phase["analysis_time"].between(a, b), "theta_proxy_z"], errors="coerce").dropna()
        return (float(s.mean()) if len(s) else np.nan, int(len(s)), condition)

    def mean_continuation(a: float, b: float):
        if followup_policy != "paired_washout_continuation" or not np.isfinite(phase_end) or b <= phase_end:
            return mean_strict(a, b)
        vals = []
        segs = []
        n = 0
        # Part inside the originating branch.
        if a < phase_end:
            s = pd.to_numeric(d_phase.loc[d_phase["analysis_time"].between(a, phase_end), "theta_proxy_z"], errors="coerce").dropna()
            if len(s):
                vals.extend(s.tolist()); n += int(len(s)); segs.append(condition)
        # Overflow part mapped to the paired washout clock, using phase_end as the zero handoff boundary.
        if paired and len(d_pair):
            wa = max(0.0, a - phase_end)
            wb = max(0.0, b - phase_end)
            if wb > wa:
                s = pd.to_numeric(d_pair.loc[d_pair["analysis_time"].between(wa, wb), "theta_proxy_z"], errors="coerce").dropna()
                if len(s):
                    vals.extend(s.tolist()); n += int(len(s)); segs.append(paired)
        return (float(np.mean(vals)) if vals else np.nan, n, ",".join(segs))

    pre, npre, spre = mean_strict(t-15, t)
    post0, n0, s0 = mean_continuation(t, t+10)
    post10, n10, s10 = mean_continuation(t+10, t+30)
    crossed = bool(np.isfinite(phase_end) and (t + 30 > phase_end) and followup_policy == "paired_washout_continuation")
    return {
        "theta_followup_policy": followup_policy,
        "theta_paired_washout_phase": paired,
        "theta_post_0_30_crossed_phase_boundary": crossed,
        "theta_pre_m15_0": pre,
        "theta_post_0_10": post0,
        "theta_post_10_30": post10,
        "delta_theta_0_10_vs_pre": post0-pre if np.isfinite(post0) and np.isfinite(pre) else np.nan,
        "delta_theta_10_30_vs_pre": post10-pre if np.isfinite(post10) and np.isfinite(pre) else np.nan,
        "theta_n_pre": npre,
        "theta_n_post_0_10": n0,
        "theta_n_post_10_30": n10,
        "theta_segments_pre": spre,
        "theta_segments_post_0_10": s0,
        "theta_segments_post_10_30": s10,
    }


def run_candidate_local_kht(features: "pd.DataFrame", peaks: "pd.DataFrame", annotations: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> Dict[str, "pd.DataFrame"]:
    """CandidateLocal_KHT_v0.2.

    Event-level exploratory human-translation coupling module. It estimates local reciprocal E<->Y_HT
    coupling around predeclared/media/algorithmic/physiology-discovered anchors and tests whether theta
    carryover follows. This module deliberately inherits the Rung 0O rule: K alone is not enough and
    handoff alone is not enough.
    """
    tables = out / "tables"
    df = _prepare_candidate_kht_frame(features)
    if df.empty:
        empty = pd.DataFrame()
        empty.to_csv(tables/"candidate_local_kht_analysis.csv", index=False)
        empty.to_csv(tables/"candidate_local_kht_random_anchor_reference.csv", index=False)
        empty.to_csv(tables/"candidate_local_kht_anchor_manifest.csv", index=False)
        safe_json_dump({"status":"not_evaluable", "reason":"no usable feature table", "boundary":"CandidateLocal_KHT is exploratory and not K_OSM."}, tables/"candidate_local_kht_interpretation.json")
        return {"analysis": empty, "random_reference": empty, "anchors": empty}
    anchors: List[Dict[str, Any]] = []
    anchors += _anchor_rows_from_df(_load_predeclared_anchor_file(getattr(cfg, "predeclared_anchor_file", ""), logger), "predeclared_media_structural", "confirmatory_if_loaded_before_run")
    anchors += _anchor_rows_from_df(annotations, "annotation_file", "secondary_or_exploratory")
    anchors += _anchor_rows_from_df(peaks, "state_locked_or_postpeak", "physiology_exploratory")
    # Always include top feature candidates as an exploratory safety net.
    anchors += _top_feature_anchors(df, n_per_segment=5)
    # Deduplicate by condition/time/id.
    seen=set(); clean=[]
    for a in anchors:
        key=(a.get("condition"), round(_safe_float(a.get("time_sec")), 2), a.get("anchor_id"))
        if key in seen: continue
        seen.add(key); clean.append(a)
    anchor_df = pd.DataFrame(clean)
    if anchor_df.empty:
        anchor_df.to_csv(tables/"candidate_local_kht_anchor_manifest.csv", index=False)
        safe_json_dump({"status":"not_evaluable", "reason":"no anchor candidates found"}, tables/"candidate_local_kht_interpretation.json")
        return {"analysis": pd.DataFrame(), "random_reference": pd.DataFrame(), "anchors": anchor_df}
    rng = np.random.default_rng(int(getattr(cfg, "random_seed", 20260724)))
    rows=[]; ref_rows=[]
    n_ref = int(min(250, max(50, getattr(cfg, "n_surrogates", 500)//2)))
    for _, a in anchor_df.iterrows():
        cond = _normalize_branch_for_anchor(a.get("condition"))
        t = _safe_float(a.get("time_sec"))
        if cond not in {"CONTROL_1", "TARGET_1", "CONTEXTUAL_OVERRIDE_1"} or not np.isfinite(t):
            continue
        local = _local_kht_at_anchor(df, cond, t)
        theta = _theta_handoff_at_anchor(df, cond, t)
        segtimes = pd.to_numeric(df.loc[df["analysis_segment"] == cond, "analysis_time"], errors="coerce").dropna().to_numpy(float)
        segtimes = segtimes[(segtimes > 20) & (segtimes < max(segtimes, default=0)-30)] if len(segtimes) else segtimes
        ref_k=[]; ref_h0=[]; ref_h10=[]
        if len(segtimes) >= 20:
            choices = rng.choice(segtimes, size=min(n_ref, len(segtimes)), replace=False if len(segtimes) >= n_ref else True)
            for rt in choices:
                lk = _local_kht_at_anchor(df, cond, float(rt)).get("K_local", np.nan)
                th = _theta_handoff_at_anchor(df, cond, float(rt))
                ref_k.append(lk); ref_h0.append(th.get("delta_theta_0_10_vs_pre", np.nan)); ref_h10.append(th.get("delta_theta_10_30_vs_pre", np.nan))
                ref_rows.append({"anchor_id": a.get("anchor_id"), "condition": cond, "random_time_sec": float(rt), "K_local": lk, "delta_theta_0_10_vs_pre": th.get("delta_theta_0_10_vs_pre", np.nan), "delta_theta_10_30_vs_pre": th.get("delta_theta_10_30_vs_pre", np.nan)})
        def pct(x, arr):
            arr=np.asarray(arr, float); arr=arr[np.isfinite(arr)]
            if not np.isfinite(x) or arr.size==0: return np.nan
            return float((arr <= x).mean())
        k_pct = pct(local.get("K_local", np.nan), ref_k)
        h0_pct = pct(theta.get("delta_theta_0_10_vs_pre", np.nan), ref_h0)
        h10_pct = pct(theta.get("delta_theta_10_30_vs_pre", np.nan), ref_h10)
        claim = str(a.get("claim_level", ""))
        anchor_source = str(a.get("anchor_source", ""))
        is_predeclared = ("predeclared" in claim.lower()) or ("media_structural" in anchor_source.lower() and "physiology" not in anchor_source.lower())
        local_k_sig = bool(np.isfinite(k_pct) and k_pct >= 0.95)
        theta_sig = bool((np.isfinite(h0_pct) and h0_pct >= 0.95 and theta.get("delta_theta_0_10_vs_pre", np.nan) > 0) or (np.isfinite(h10_pct) and h10_pct >= 0.95 and theta.get("delta_theta_10_30_vs_pre", np.nan) > 0))
        final_lock = bool(is_predeclared and local_k_sig and theta_sig)
        rows.append({**dict(a), **local, **theta,
                     "K_local_percentile_vs_random_same_condition": k_pct,
                     "handoff_0_10_percentile_vs_random_same_condition": h0_pct,
                     "handoff_10_30_percentile_vs_random_same_condition": h10_pct,
                     "local_k_significant_p95": local_k_sig,
                     "theta_handoff_significant_p95": theta_sig,
                     "predeclared_or_media_structural": is_predeclared,
                     "candidate_local_kht_lock": final_lock,
                     "interpretation": "candidate lock" if final_lock else ("exploratory support" if local_k_sig and theta_sig else "not locked")})
    analysis = pd.DataFrame(rows).sort_values(["candidate_local_kht_lock", "local_k_significant_p95", "theta_handoff_significant_p95", "K_local"], ascending=[False, False, False, False]) if rows else pd.DataFrame()
    ref = pd.DataFrame(ref_rows)
    anchor_df.to_csv(tables/"candidate_local_kht_anchor_manifest.csv", index=False)
    analysis.to_csv(tables/"candidate_local_kht_analysis.csv", index=False)
    ref.to_csv(tables/"candidate_local_kht_random_anchor_reference.csv", index=False)
    if len(analysis):
        summary = {
            "status": "exploratory_or_confirmatory_by_anchor_level",
            "n_candidates": int(len(analysis)),
            "n_candidate_locks": int(analysis["candidate_local_kht_lock"].sum()) if "candidate_local_kht_lock" in analysis else 0,
            "best_candidate": analysis.iloc[0].to_dict(),
            "rule": "Final human-event lock requires predeclared/media-structural anchor + local K significance + theta handoff significance. K alone is not enough; handoff alone is not enough.",
            "boundary": "CandidateLocal_KHT estimates event-level human-translation coupling. It is not K_OSM, Y_cell, Y_OSM, or mechanism proof. Physiology-discovered anchors remain exploratory in the same run."
        }
    else:
        summary = {"status":"not_evaluable", "reason":"no evaluable candidates"}
    safe_json_dump(summary, tables/"candidate_local_kht_interpretation.json")
    logger(f"CandidateLocal_KHT module complete: {len(analysis)} candidates, {summary.get('n_candidate_locks', 0)} candidate locks.")
    return {"analysis": analysis, "random_reference": ref, "anchors": anchor_df}



# ----------------------- MRED_v0.1 -----------------------
# Meaning Recognition--Encoding Dissociation.


def _mred_load_optional_csv(path: str, logger: RunLogger, label: str) -> "pd.DataFrame":
    if not path:
        return pd.DataFrame()
    q = Path(str(path).strip().strip('"'))
    if not q.exists():
        logger(f"MRED {label} not found: {q}")
        return pd.DataFrame()
    try:
        return pd.read_csv(q)
    except Exception as exc:
        logger(f"WARNING: could not read MRED {label} CSV {q}: {exc}")
        return pd.DataFrame()


def _mred_match_value(aux: "pd.DataFrame", row: Dict[str, Any], candidates: Sequence[str], default: float = np.nan) -> float:
    if aux is None or len(aux) == 0:
        return default
    df = aux.copy()
    aid = str(row.get("anchor_id", ""))
    if aid and "anchor_id" in df.columns:
        sub = df[df["anchor_id"].astype(str) == aid]
        if len(sub):
            for c in candidates:
                if c in sub.columns:
                    return _safe_float(sub[c].iloc[0], default)
    scene = str(row.get("scene_label", row.get("label", "")))
    if scene and "scene_label" in df.columns:
        sub = df[df["scene_label"].astype(str).str.lower() == scene.lower()]
        if len(sub):
            for c in candidates:
                if c in sub.columns:
                    return _safe_float(sub[c].iloc[0], default)
    if len(df) == 1:
        for c in candidates:
            if c in df.columns:
                return _safe_float(df[c].iloc[0], default)
    return default


def _mred_window_mean(df: "pd.DataFrame", cond: str, t: float, col: Optional[str], pre: float = 2.0, post: float = 2.0) -> float:
    if not col or col not in df.columns or "analysis_segment" not in df.columns or "analysis_time" not in df.columns:
        return np.nan
    cond = _normalize_branch_for_anchor(cond)
    tt = pd.to_numeric(df["analysis_time"], errors="coerce")
    mask = (df["analysis_segment"] == cond) & (tt >= (t - pre)) & (tt <= (t + post))
    vals = pd.to_numeric(df.loc[mask, col], errors="coerce")
    return float(vals.mean()) if vals.notna().any() else np.nan


def _mred_prepare_feature_frame(features: "pd.DataFrame") -> Tuple["pd.DataFrame", Dict[str, str]]:
    df = standardize_feature_columns(features).copy() if features is not None and len(features) else pd.DataFrame()
    if df.empty:
        return df, {}
    seg_col = _segment_col(df)
    tcol = _time_col(df)
    if seg_col:
        df["analysis_segment"] = df[seg_col].map(_normalize_branch_for_anchor)
    if tcol:
        df["analysis_time"] = pd.to_numeric(df[tcol], errors="coerce")
    meaning_col = _first_numeric_col(df, ["MeaningGamma", "MeaningGamma_phys", "MeaningGamma_lgamma_30_45", "meaninggamma_score", "gamma_z", "lgamma_posterior_temporal_z", "lgamma_global_z", "pow_lgamma_30_45_primary_content_core"])
    tsp_col = _first_numeric_col(df, ["tsp_z", "TemporalSemanticProxy", "temporal_semantic_proxy_score", "Y_proxy_z"])
    if not tsp_col:
        try:
            y_proxy, _ = _construct_tsp_proxy(df)
            df["mred_tsp_constructed_z"] = y_proxy
            tsp_col = "mred_tsp_constructed_z"
        except Exception:
            tsp_col = None
    theta_col = _first_numeric_col(df, ["theta_z", "theta_midline_z", "theta_global_z", "theta_posterior_temporal_z", "ThetaPLV_primary", "plv_theta_4_8_primary_content_core"])
    artifact_col = _first_numeric_col(df, ["artifact_score", "artifact_ratio_lgamma_z", "lgamma_artifact_sentinel_z", "ptp_artifact_median_uV", "median_p2p", "z_logbp_artifact_sentinel_hf_proxy_45_55"])
    api_col = _first_numeric_col(df, ["api_a", "API_A", "autonomic_availability", "API_A_v1"])
    return df, {"meaning_gamma_col": meaning_col or "not_found", "tsp_col": tsp_col or "not_found", "theta_col": theta_col or "not_found", "artifact_col": artifact_col or "not_found", "api_a_col": api_col or "not_found"}


def _mred_classify(mr_high: bool, enc_high: bool) -> str:
    if mr_high and enc_high:
        return "MR_HIGH_ENC_HIGH_meaning_plus_new_encoding_candidate"
    if mr_high and not enc_high:
        return "MR_HIGH_ENC_LOW_meaning_recognition_or_old_memory_reactivation"
    if (not mr_high) and enc_high:
        return "MR_LOW_ENC_HIGH_nonsemantic_encoding_or_task_artifact_check"
    return "MR_LOW_ENC_LOW_null_or_weak_event"


def run_mred_layer(features: "pd.DataFrame", candidate_local: Any, annotations: "pd.DataFrame", cfg: SuiteConfig, out: Path, logger: RunLogger) -> Dict[str, "pd.DataFrame"]:
    """MeaningRecognition_EncodingDissociation_v0.1.

    Separates semantic-affective recognition / schema reactivation (MR) from theta-indexed new integration / encoding load (ENC).
    """
    tables = out / "tables"
    ensure_dir(tables)
    df, used_cols = _mred_prepare_feature_frame(features)
    fam = _mred_load_optional_csv(getattr(cfg, "mred_familiarity_csv", ""), logger, "familiarity covariates")
    scene_map = _mred_load_optional_csv(getattr(cfg, "mred_scene_map_csv", ""), logger, "scene map")
    cand = pd.DataFrame()
    if isinstance(candidate_local, dict) and isinstance(candidate_local.get("analysis"), pd.DataFrame):
        cand = candidate_local.get("analysis").copy()
    else:
        q = tables / "candidate_local_kht_analysis.csv"
        if q.exists():
            try:
                cand = pd.read_csv(q)
            except Exception:
                cand = pd.DataFrame()
    if cand.empty:
        anchors = []
        anchors += _anchor_rows_from_df(_load_predeclared_anchor_file(getattr(cfg, "predeclared_anchor_file", ""), logger), "predeclared_media_structural", "confirmatory_if_loaded_before_run")
        anchors += _anchor_rows_from_df(annotations, "annotation_file", "secondary_or_exploratory")
        cand = pd.DataFrame(anchors)
    if cand.empty:
        empty = pd.DataFrame()
        for name in ["mred_event_table.csv", "mred_quadrant_classification.csv", "mred_anchor_scene_map.csv", "mred_familiarity_covariates.csv", "mred_visual_overlay.csv"]:
            empty.to_csv(tables / name, index=False)
        safe_json_dump({"status":"not_evaluable", "reason":"no CandidateLocal_KHT, predeclared anchor, or annotation candidates available", "boundary":"MRED is a human-translation interpretive layer, not K_OSM, Y_cell, Y_OSM, or proof of memory encoding."}, tables / "mred_interpretation.json")
        return {"events": empty, "quadrants": empty, "scene_map": empty, "familiarity": fam}
    rows: List[Dict[str, Any]] = []
    for _, rr in cand.iterrows():
        r = dict(rr)
        cond = _normalize_branch_for_anchor(r.get("condition", r.get("analysis_segment", r.get("segment", ""))))
        t = _safe_float(r.get("time_sec", r.get("analysis_time", r.get("peak_sec", r.get("taper_sec", np.nan)))))
        aid = str(r.get("anchor_id", r.get("event_id", f"MRED_{cond}_{t:.1f}" if np.isfinite(t) else "MRED_event")))
        scene_label = str(r.get("scene_label", r.get("label", "")))
        if (not scene_label or scene_label == "nan") and len(scene_map) and "anchor_id" in scene_map.columns:
            sub = scene_map[scene_map["anchor_id"].astype(str) == aid]
            if len(sub) and "scene_label" in sub.columns:
                scene_label = str(sub["scene_label"].iloc[0])
        meaning_gamma = _safe_float(r.get("meaning_gamma_z", r.get("MeaningGamma", r.get("meaninggamma_score", np.nan))))
        if not np.isfinite(meaning_gamma) and np.isfinite(t) and len(df):
            c = used_cols.get("meaning_gamma_col")
            meaning_gamma = _mred_window_mean(df, cond, t, c if c != "not_found" else None)
        tsp = _safe_float(r.get("tsp_z", r.get("TSP", r.get("temporal_semantic_proxy_score", np.nan))))
        if not np.isfinite(tsp) and np.isfinite(t) and len(df):
            c = used_cols.get("tsp_col")
            tsp = _mred_window_mean(df, cond, t, c if c != "not_found" else None)
        k_local = _safe_float(r.get("K_local", r.get("K_HT_local", np.nan)))
        theta_0_10 = _safe_float(r.get("delta_theta_0_10_vs_pre", r.get("theta_handoff_0_10", np.nan)))
        theta_10_30 = _safe_float(r.get("delta_theta_10_30_vs_pre", r.get("theta_handoff_10_30", np.nan)))
        theta_best = np.nanmax([theta_0_10, theta_10_30]) if np.any(np.isfinite([theta_0_10, theta_10_30])) else np.nan
        artifact = _safe_float(r.get("artifact_score", r.get("artifact_proxy_z", np.nan)))
        if not np.isfinite(artifact) and np.isfinite(t) and len(df):
            c = used_cols.get("artifact_col")
            artifact = _mred_window_mean(df, cond, t, c if c != "not_found" else None)
        api_a = _safe_float(r.get("api_a", r.get("API_A", np.nan)))
        if not np.isfinite(api_a) and np.isfinite(t) and len(df):
            c = used_cols.get("api_a_col")
            api_a = _mred_window_mean(df, cond, t, c if c != "not_found" else None)
        row_for_match = {**r, "anchor_id": aid, "scene_label": scene_label}
        familiarity = _mred_match_value(fam, row_for_match, ["familiarity_score", "familiarity_0_9", "familiarity", "prior_exposure_0_9", "scene_remembered_0_9"], np.nan)
        prior_exposure = _mred_match_value(fam, row_for_match, ["prior_exposure_0_9", "prior_exposure", "seen_before_0_9"], np.nan)
        scene_remembered = _mred_match_value(fam, row_for_match, ["scene_remembered_0_9", "scene_remembered", "remembered_beat_0_9"], np.nan)
        beat_anticipated = _mred_match_value(fam, row_for_match, ["beat_anticipated_0_9", "beat_anticipated", "anticipated_0_9"], np.nan)
        if not np.isfinite(familiarity) and np.any(np.isfinite([prior_exposure, scene_remembered, beat_anticipated])):
            familiarity = float(np.nanmean([prior_exposure, scene_remembered, beat_anticipated]))
        novelty = _mred_match_value(fam, row_for_match, ["novelty_score", "novelty_0_9", "new_insight_0_9", "unexpectedness_0_9"], np.nan)
        new_insight = _mred_match_value(fam, row_for_match, ["new_insight_0_9", "new_insight"], np.nan)
        unexpectedness = _mred_match_value(fam, row_for_match, ["unexpectedness_0_9", "unexpectedness"], np.nan)
        if not np.isfinite(novelty) and np.any(np.isfinite([new_insight, unexpectedness, beat_anticipated])):
            novelty = float(np.nanmean([new_insight, unexpectedness, 9.0 - beat_anticipated if np.isfinite(beat_anticipated) else np.nan]))
        autobiographical = _mred_match_value(fam, row_for_match, ["autobiographical_resonance_0_9", "current_life_connection_0_9", "autobiographical_resonance"], np.nan)
        cringe = _mred_match_value(fam, row_for_match, ["cringe_score_0_9", "aversive_semantic_prediction_error_0_9", "cringe_score"], np.nan)
        rows.append({"anchor_id":aid, "condition":cond, "time_sec":t, "scene_label":scene_label, "anchor_source":r.get("anchor_source", r.get("source", "candidate_local_kht")), "claim_level":r.get("claim_level", "exploratory"), "meaning_gamma_z":meaning_gamma, "tsp_z":tsp, "K_local":k_local, "theta_handoff_0_10":theta_0_10, "theta_handoff_10_30":theta_10_30, "theta_handoff_best":theta_best, "artifact_score":artifact, "api_a":api_a, "familiarity_score":familiarity, "novelty_score":novelty, "autobiographical_resonance":autobiographical, "cringe_score":cringe, "candidate_local_kht_lock":bool(r.get("candidate_local_kht_lock", False)), "predeclared_or_media_structural":bool(r.get("predeclared_or_media_structural", False))})
    ev = pd.DataFrame(rows)
    for c in ["meaning_gamma_z", "tsp_z", "K_local", "theta_handoff_best", "artifact_score", "api_a", "familiarity_score", "novelty_score", "autobiographical_resonance", "cringe_score"]:
        ev[c] = pd.to_numeric(ev[c], errors="coerce") if c in ev.columns else np.nan
        ev[c + "_event_z"] = _z_safe(ev[c]) if ev[c].notna().any() else 0.0
    art_pos = ev["artifact_score_event_z"].clip(lower=0) if "artifact_score_event_z" in ev else 0.0
    ev["MR_score"] = 0.35*ev["meaning_gamma_z_event_z"] + 0.35*ev["tsp_z_event_z"] + 0.30*ev["K_local_event_z"] - 0.20*art_pos
    ev["ENC_score"] = 0.65*ev["theta_handoff_best_event_z"] + 0.15*ev["api_a_event_z"] + 0.20*ev["novelty_score_event_z"] - 0.20*ev["familiarity_score_event_z"] - 0.15*art_pos
    def pct_rank(x: "pd.Series") -> "pd.Series":
        return x.rank(pct=True, method="average") if len(x) else x
    ev["MR_percentile_global"] = pct_rank(ev["MR_score"])
    ev["ENC_percentile_global"] = pct_rank(ev["ENC_score"])
    ev["MR_percentile_by_condition"] = ev.groupby("condition")["MR_score"].transform(pct_rank)
    ev["ENC_percentile_by_condition"] = ev.groupby("condition")["ENC_score"].transform(pct_rank)
    ev["MR_high"] = ((ev["MR_percentile_global"] >= 0.75) | (ev["MR_percentile_by_condition"] >= 0.75)) & (ev["MR_score"] > 0)
    ev["ENC_high"] = ((ev["ENC_percentile_global"] >= 0.75) | (ev["ENC_percentile_by_condition"] >= 0.75)) & (ev["ENC_score"] > 0)
    ev["mred_quadrant"] = [_mred_classify(bool(m), bool(e)) for m, e in zip(ev["MR_high"], ev["ENC_high"])]
    ev["mred_interpretation"] = ev["mred_quadrant"].map({"MR_HIGH_ENC_HIGH_meaning_plus_new_encoding_candidate":"Meaning-recognition and theta-indexed integration are both high; candidate new-encoding/integration event if controls pass.", "MR_HIGH_ENC_LOW_meaning_recognition_or_old_memory_reactivation":"Meaning-recognition is high but theta-indexed integration is not; candidate familiar meaning, schema reactivation, or old-memory recognition.", "MR_LOW_ENC_HIGH_nonsemantic_encoding_or_task_artifact_check":"Theta-indexed integration is high without strong meaning-recognition; check task, novelty, respiration, artifact, or nonsemantic learning.", "MR_LOW_ENC_LOW_null_or_weak_event":"No strong recognition or integration pattern detected by this operational layer."})
    ev = ev.sort_values(["MR_high", "ENC_high", "MR_score", "ENC_score"], ascending=[False, False, False, False]).reset_index(drop=True)
    quadrants = ev.groupby(["condition", "mred_quadrant"], dropna=False).size().reset_index(name="n_events") if len(ev) else pd.DataFrame()
    scene_out = scene_map.copy() if len(scene_map) else ev[["anchor_id", "condition", "time_sec", "scene_label", "anchor_source", "claim_level"]].drop_duplicates()
    fam_out = fam.copy() if len(fam) else pd.DataFrame(columns=["anchor_id", "scene_label", "prior_exposure_0_9", "scene_remembered_0_9", "beat_anticipated_0_9", "new_insight_0_9", "unexpectedness_0_9", "current_life_connection_0_9", "meaningful_but_already_known_0_9", "autobiographical_resonance_0_9", "cringe_score_0_9"])
    ev.to_csv(tables / "mred_event_table.csv", index=False)
    quadrants.to_csv(tables / "mred_quadrant_classification.csv", index=False)
    scene_out.to_csv(tables / "mred_anchor_scene_map.csv", index=False)
    fam_out.to_csv(tables / "mred_familiarity_covariates.csv", index=False)
    overlay_rows=[]
    for _, r in ev.iterrows():
        try:
            t=float(r.get("time_sec"))
        except Exception:
            continue
        try:
            mr=f"{float(r.get('MR_score')):.2f}"; enc=f"{float(r.get('ENC_score')):.2f}"
        except Exception:
            mr=str(r.get('MR_score')); enc=str(r.get('ENC_score'))
        label = f"MRED {r.get('anchor_id')} MR={mr} ENC={enc} {r.get('mred_quadrant')}"
        overlay_rows.append({"start_sec": t, "end_sec": t+0.9, "label": label, "category": "mred", "source": "mred_event_table.csv"})
    pd.DataFrame(overlay_rows).to_csv(tables / "mred_visual_overlay.csv", index=False)
    summary = {"schema":"PRAYCG_MRED_v0_1_interpretation", "status":"exploratory_or_confirmatory_by_anchor_level", "n_events":int(len(ev)), "n_mr_high":int(ev["MR_high"].sum()) if len(ev) else 0, "n_enc_high":int(ev["ENC_high"].sum()) if len(ev) else 0, "n_mr_high_enc_low":int(((ev["MR_high"]) & (~ev["ENC_high"])).sum()) if len(ev) else 0, "n_mr_high_enc_high":int(((ev["MR_high"]) & (ev["ENC_high"])).sum()) if len(ev) else 0, "columns_used":used_cols, "rule":"MR estimates meaning-recognition/schema-reactivation load from MeaningGamma/TSP/local K. ENC estimates theta-indexed integration/new-encoding load from theta carryover plus optional novelty/familiarity covariates. MR and ENC are dissociable.", "claim_boundary":"MRED does not prove memory encoding, OSM, Y_cell, or K_OSM. Lack of theta handoff is not proof that no memory was encoded; it means the suite did not detect its operational theta-carryover marker.", "recommended_next_step":"Use predeclared media-structural anchors plus familiarity/novelty/self-report covariates for prospective testing."}
    if len(ev):
        summary["top_mr_event"] = ev.sort_values("MR_score", ascending=False).iloc[0].to_dict()
        summary["top_enc_event"] = ev.sort_values("ENC_score", ascending=False).iloc[0].to_dict()
    safe_json_dump(summary, tables / "mred_interpretation.json")
    logger(f"MRED_v0.1 module complete: {len(ev)} events; {summary['n_mr_high_enc_low']} high-MR/low-ENC recognition-reactivation candidates.")
    return {"events": ev, "quadrants": quadrants, "scene_map": scene_out, "familiarity": fam_out, "interpretation": pd.DataFrame([summary])}

def build_handoff_endpoint_table(postpeak:"pd.DataFrame", ann:"pd.DataFrame", lagbest:"pd.DataFrame", out:Path)->"pd.DataFrame":
    rows=[]
    def add(e,s,summary,table): rows.append({"endpoint":e,"status":s,"summary":summary,"evidence_table":table})
    if postpeak is not None and len(postpeak):
        foc=postpeak[(postpeak["theta_metric"].astype(str).str.contains("plv_theta_4_8_primary")) & (postpeak["post_window"].astype(str).str.contains("10-30"))]
        if len(foc):
            best=foc.sort_values("target_minus_override_delta",ascending=False).iloc[0]; val=best.get("target_minus_override_delta",np.nan)
            add("PostPeakPNCC_theta","exploratory_positive_by_sign" if np.isfinite(val) and val>0 else "not_supported_by_sign",f"Best primary-theta 10-30s post-taper Target-Override delta = {val:.3f} at {best.get('anchor_id')}","postpeak_pncc_theta_contrasts.csv")
        else: add("PostPeakPNCC_theta","not_evaluable","No primary theta PLV post-peak rows available.","postpeak_pncc_theta_contrasts.csv")
    else: add("PostPeakPNCC_theta","not_evaluable","Post-peak module produced no rows.","postpeak_pncc_theta_contrasts.csv")
    if ann is not None and len(ann):
        sub=ann[ann["theta_metric"].astype(str).str.contains("plv_theta_4_8_primary",na=False)]
        if len(sub):
            best=sub.sort_values("target_minus_override_delta",ascending=False).iloc[0]; val=best.get("target_minus_override_delta",np.nan)
            add("AnnotationLockedThetaCarryover","exploratory_positive_by_sign" if np.isfinite(val) and val>0 else "not_supported_by_sign",f"Best annotation-locked primary-theta Target-Override delta = {val:.3f} at event {best.get('event_id')}","annotation_locked_theta_carryover_contrasts.csv")
        else: add("AnnotationLockedThetaCarryover","not_evaluable","No annotation-locked primary theta rows available.","annotation_locked_theta_carryover_contrasts.csv")
    else: add("AnnotationLockedThetaCarryover","not_evaluable","No annotation CSV or no eligible annotation rows.","annotation_locked_theta_carryover_contrasts.csv")
    if lagbest is not None and len(lagbest):
        tsp=lagbest[lagbest["predictor"].astype(str).str.contains("TemporalSemanticProxy",na=False)]; source=tsp if len(tsp) else lagbest; row=source.sort_values("r", key=lambda s:s.abs(), ascending=False).iloc[0]
        add("G2ThetaHandoff","exploratory_lag_reported",f"Best lagged predictor/outcome: {row.get('predictor')} -> {row.get('outcome')} at {row.get('lag_sec')}s, r={row.get('r'):.3f}, artifact-partial r={row.get('artifact_partial_r'):.3f}.","gamma_to_theta_handoff_best_lags.csv")
    else: add("G2ThetaHandoff","not_evaluable","No lagged gamma-to-theta correlations available.","gamma_to_theta_handoff_best_lags.csv")
    df=pd.DataFrame(rows); df.to_csv(out/"tables"/"handoff_endpoint_status_table.csv",index=False); return df

def build_master_endpoint_table(contrasts: "pd.DataFrame", resid: "pd.DataFrame", gamma_contrasts: "pd.DataFrame", hrv: "pd.DataFrame", pncc: "pd.DataFrame", tau: "pd.DataFrame", cascade_order: "pd.DataFrame", out: Path) -> "pd.DataFrame":
    rows = []
    def add(endpoint, status, summary, evidence=""):
        rows.append({"endpoint": endpoint, "status": status, "summary": summary, "evidence_table": evidence})
    # Lower gamma T > O
    status = "not_evaluable"
    summary = "No primary lower-gamma contrast available."
    if contrasts is not None and len(contrasts):
        sub = contrasts[(contrasts["metric"].astype(str).str.contains("pow_lgamma_30_45_primary_content_core")) & (contrasts["A"] == "TARGET_1") & (contrasts["B"] == "CONTEXTUAL_OVERRIDE_1")]
        if len(sub):
            d = float(sub.iloc[0]["delta"])
            status = "supported_by_sign" if d > 0 else "not_supported_by_sign"
            summary = f"Target - Override primary-content lower-gamma delta = {d:.3f}."
    add("Mapped lower-gamma Target > Override", status, summary, "artifact_matched_condition_contrasts.csv")
    # Residualized
    status = "not_evaluable"; summary = "No residualized lower-gamma contrast available."
    if resid is not None and len(resid):
        sub = resid[(resid["metric"].astype(str).str.contains("primary_content_core")) & (resid["A"] == "TARGET_1") & (resid["B"] == "CONTEXTUAL_OVERRIDE_1")]
        if len(sub):
            d = float(sub.iloc[0]["delta"])
            status = "supported_by_sign" if d > 0 else "not_supported_by_sign"
            summary = f"Residualized Target - Override delta = {d:.3f}."
    add("Residualized lower-gamma Target > Override", status, summary, "eeg_low_gamma_residualized_contrasts.csv")
    # TaskGamma
    status = "not_evaluable"; summary = "No TaskGamma contrast available."
    if gamma_contrasts is not None and len(gamma_contrasts):
        sub = gamma_contrasts[(gamma_contrasts["metric"].astype(str).str.contains("TaskGamma_lgamma_30_45")) & (gamma_contrasts["A"] == "TARGET_1") & (gamma_contrasts["B"] == "CONTEXTUAL_OVERRIDE_1")]
        if len(sub):
            d = float(sub.iloc[0]["delta"])
            status = "override_task_lock_supported_by_sign" if d < 0 else "target_task_gamma_higher"
            summary = f"TaskGamma Target - Override = {d:.3f}; negative means Override > Target."
    add("GammaScalpel TaskGamma", status, summary, "gammascalpel_score_contrasts.csv")
    # API
    status = "not_evaluable"; summary = "No API_A summary available."
    if hrv is not None and len(hrv) and "API_A_v1" in hrv.columns:
        def api(seg):
            m = hrv[hrv["segment"] == seg]
            return float(m.iloc[0]["API_A_v1"]) if len(m) else np.nan
        t, c, o = api("TARGET_1"), api("CONTROL_1"), api("CONTEXTUAL_OVERRIDE_1")
        if np.isfinite(t):
            status = "supported_by_sign" if (not np.isfinite(c) or t > c) and (not np.isfinite(o) or t > o) else "mixed"
            summary = f"API_A Target={t:.3f}, Control={c:.3f}, Override={o:.3f}."
    add("Autonomic API_A Target advantage", status, summary, "hrv_api_segment_summary.csv")
    # PNCC
    status = "not_evaluable"; summary = "No PNCC theta table available."
    if pncc is not None and len(pncc):
        sub = pncc[(pncc["A"] == "WASHOUT_2") & (pncc["B"] == "WASHOUT_1")]
        if len(sub):
            d = float(sub.iloc[0]["delta"])
            ci1, ci2 = float(sub.iloc[0]["ci_low"]), float(sub.iloc[0]["ci_high"])
            status = "supported" if d > 0 and ci1 > 0 else ("weak_positive" if d > 0 else "not_supported")
            summary = f"PNCC_theta W2-W1 delta={d:.4f}, CI=[{ci1:.4f},{ci2:.4f}]."
    add("Formal PNCC_theta", status, summary, "pncc_theta_artifact_matched_surrogate_contrasts.csv")
    # tau
    status = "not_evaluable"; summary = "No tau_coh theta table available."
    if tau is not None and len(tau):
        status = str(tau.iloc[0].get("status", "unknown"))
        summary = f"tau_coh_theta={tau.iloc[0].get('tau_sec', np.nan)} sec; status={status}."
    add("tau_coh_theta", status, summary, "tau_coh_theta_summary.csv")
    # Cascade
    status = "not_evaluable"; summary = "No cascade order index available."
    if cascade_order is not None and len(cascade_order):
        classic = bool(cascade_order.iloc[0].get("classic_FCOI_supported", False))
        modified = bool(cascade_order.iloc[0].get("modified_delayed_reveal_supported", False))
        status = "classic_supported" if classic else ("modified_supported" if modified else "not_supported")
        summary = f"Classic FCOI={classic}; modified delayed-reveal order={modified}."
    add("Post-meaning frequency cascade", status, summary, "post_meaning_cascade_order_index.csv")
    df = pd.DataFrame(rows)
    df.to_csv(out / "tables" / "master_endpoint_status_table.csv", index=False)
    return df


# ---------------------------
# Figures and report
# ---------------------------

def make_figures(features: "pd.DataFrame", hrv: "pd.DataFrame", resp: "pd.DataFrame", ratings: "pd.DataFrame", endpoint: "pd.DataFrame", out: Path, logger: RunLogger) -> None:
    figdir = ensure_dir(out / "figures")
    try:
        if features is not None and len(features) and "pow_lgamma_30_45_primary_content_core" in features.columns:
            seg_order = ["CONTROL_1", "TARGET_1", "CONTEXTUAL_OVERRIDE_1", "WASHOUT_1", "WASHOUT_2", "WASHOUT_3"]
            rows = []
            for seg in seg_order:
                sub = features[features["segment"] == seg]
                if len(sub):
                    rows.append({"segment": seg, "low_gamma": sub["pow_lgamma_30_45_primary_content_core"].mean()})
            d = pd.DataFrame(rows)
            if len(d):
                plt.figure(figsize=(9, 4))
                plt.bar(d["segment"], d["low_gamma"])
                plt.xticks(rotation=30, ha="right")
                plt.ylabel("Mean log power, 30-45 Hz")
                plt.title("Primary-content lower-gamma by segment")
                plt.tight_layout()
                plt.savefig(figdir / "primary_content_low_gamma_by_segment.png", dpi=150)
                plt.close()
        if hrv is not None and len(hrv) and "API_A_v1" in hrv.columns:
            d = hrv[hrv["segment"].isin(["CONTROL_1", "TARGET_1", "CONTEXTUAL_OVERRIDE_1", "WASHOUT_1", "WASHOUT_2", "WASHOUT_3"])]
            if len(d):
                plt.figure(figsize=(9,4))
                plt.bar(d["segment"], d["API_A_v1"])
                plt.xticks(rotation=30, ha="right")
                plt.ylabel("API_A v1")
                plt.title("Autonomic Presence Index by segment")
                plt.tight_layout()
                plt.savefig(figdir / "api_a_by_segment.png", dpi=150)
                plt.close()
        if resp is not None and len(resp) and "dominant_breath_rate_bpm" in resp.columns:
            d = resp[resp["segment"].isin(["CONTROL_1", "TARGET_1", "CONTEXTUAL_OVERRIDE_1", "WASHOUT_1", "WASHOUT_2", "WASHOUT_3"])]
            if len(d):
                plt.figure(figsize=(9,4))
                plt.bar(d["segment"], d["dominant_breath_rate_bpm"])
                plt.xticks(rotation=30, ha="right")
                plt.ylabel("Dominant breathing rate, bpm")
                plt.title("Respiration by segment")
                plt.tight_layout()
                plt.savefig(figdir / "respiration_rate_by_segment.png", dpi=150)
                plt.close()
    except Exception as e:
        logger(f"Figure generation warning: {e}")


def table_to_md(df: "pd.DataFrame", max_rows: int = 12) -> str:
    """Small dependency-free Markdown table writer."""
    if df is None or len(df) == 0:
        return "_No rows available._\n"
    d = df.head(max_rows).copy()
    d = d.astype(object).where(pd.notna(d), "")
    cols = [str(c) for c in d.columns]
    lines = []
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(cols)) + " |")
    for _, row in d.iterrows():
        vals = []
        for c in d.columns:
            v = row[c]
            if isinstance(v, float):
                vals.append(f"{v:.4g}")
            else:
                txt = str(v).replace("\n", " ").replace("|", "/")
                if len(txt) > 120:
                    txt = txt[:117] + "..."
                vals.append(txt)
        lines.append("| " + " | ".join(vals) + " |")
    if len(df) > max_rows:
        lines.append(f"\n_Showing first {max_rows} of {len(df)} rows._")
    return "\n".join(lines) + "\n"


def build_report(cfg: SuiteConfig, out: Path, results: Dict[str, Any], logger: RunLogger) -> Path:
    report = []
    report.append(f"# {cfg.project_name} — Master Comprehensive PR-AYC-G Analysis Report v{VERSION}\n")
    report.append(f"Generated: {_dt.datetime.now().isoformat(timespec='seconds')}\n")
    report.append("## Interpretive boundary\n")
    report.append("This report is a post-processing summary. It does not prove meaning, consciousness, clinical efficacy, or a hidden molecular mechanism. It tests whether the recorded physiology, EEG, respiration, task, self-report, and artifact layers form a coherent pattern under the selected PR-AYC-G model.\n")
    report.append("## Configuration\n")
    report.append(f"- Stimulus style: `{cfg.stimulus_style}`\n")
    report.append(f"- Channel map preset: `{cfg.channel_map_preset}`; confidence: `{cfg.channel_map_confidence}`\n")
    report.append(f"- Marker source preference: `{cfg.preferred_marker_source}`\n")
    report.append(f"- EEG window/step: {cfg.eeg_window_sec:.2f}s / {cfg.eeg_step_sec:.2f}s\n")
    report.append("- Enabled modules:\n")
    for k, v in cfg.modules.items():
        if v:
            report.append(f"  - {k}\n")
    report.append("\n")

    if "stream_inventory" in results:
        report.append("## 1. Stream inventory and data integrity\n")
        report.append(table_to_md(results["stream_inventory"]))
    if "marker_status" in results:
        report.append("## 2. Marker and timing status\n")
        report.append(table_to_md(pd.DataFrame([results["marker_status"]])))
    if "channel_map" in results:
        report.append("## 3. Channel map\n")
        report.append(table_to_md(results["channel_map"], max_rows=20))
    if "cue_summary" in results:
        report.append("## 4. Cue schedule validation\n")
        report.append(table_to_md(pd.DataFrame([results["cue_summary"]])))
    if "override_scoring" in results:
        report.append("## 5. Contextual override task scoring\n")
        report.append(table_to_md(results["override_scoring"]))
    if "ratings_wide" in results:
        report.append("## 6. Self-report summary\n")
        report.append(table_to_md(results["ratings_wide"], max_rows=20))
    if "exclusions" in results:
        report.append("## 7. Report/input artifact censorship\n")
        report.append(table_to_md(results["exclusions"], max_rows=20))
    if "eeg_qc" in results:
        report.append("## 8. EEG channel QC\n")
        report.append(table_to_md(results["eeg_qc"], max_rows=20))
    if "contrasts" in results:
        report.append("## 9. Mapped EEG contrasts\n")
        report.append(table_to_md(results["contrasts"].head(25), max_rows=25))
    if "residualized" in results:
        report.append("## 10. Residualized lower-gamma contrasts\n")
        report.append(table_to_md(results["residualized"].head(20), max_rows=20))
    if "gammascalpel_contrasts" in results:
        report.append("## 11. GammaScalpel\n")
        report.append("GammaScalpel treats gamma as a work signal rather than a direct meaning signal. It attempts to separate task-lock, meaning-candidate, visual, and artifact-sensitive components using spatial, spectral, and rigidity features.\n")
        report.append(table_to_md(results["gammascalpel_contrasts"].head(20), max_rows=20))
    if "hrv" in results:
        report.append("## 12. Autonomic API_A\n")
        report.append(table_to_md(results["hrv"], max_rows=20))
    if "respiration" in results:
        report.append("## 13. Respiration\n")
        report.append(table_to_md(results["respiration"], max_rows=20))
    if "pncc" in results:
        report.append("## 14. Formal PNCC_theta\n")
        report.append(table_to_md(results["pncc"].head(20), max_rows=20))
    if "tau" in results:
        report.append("## 15. tau_coh_theta\n")
        report.append(table_to_md(results["tau"], max_rows=20))
    if "cascade_order" in results:
        report.append("## 16. Post-meaning frequency cascade\n")
        report.append(table_to_md(results.get("cascade_key", pd.DataFrame()), max_rows=20))
        report.append("\nOrder index:\n")
        report.append(table_to_md(results["cascade_order"], max_rows=5))
    if "endpoint" in results:
        report.append("## 17. Master endpoint status table\n")
        report.append(table_to_md(results["endpoint"], max_rows=30))
    if "human_translation_kht" in results:
        report.append("## 18. HumanTranslation_KHT_v0.2\n")
        report.append("This module estimates a rough human-translation coupling endpoint, K_HT. It is not K_OSM and it does not prove Opto-Structural Memory. Media/QC fingerprints are treated as exogenous input inventory, not as a biological Y variable.\n")
        kht = results.get("human_translation_kht", {})
        if isinstance(kht, dict):
            if "interpretation" in kht:
                report.append(table_to_md(kht["interpretation"], max_rows=5))
            if "phasewise" in kht:
                report.append(table_to_md(kht["phasewise"], max_rows=10))
            if "cv_wins" in kht:
                report.append("\nCross-validation winner summary:\n")
                report.append(table_to_md(kht["cv_wins"], max_rows=10))

    if "candidate_local_kht" in results:
        report.append("## 19. CandidateLocal_KHT_v0.1\n")
        report.append("This module estimates event-level local human-translation coupling around predeclared, annotation, state-locked, or physiology-discovered anchors. It follows the Rung 0O discipline: K alone is not enough, and theta handoff alone is not enough. For a candidate event to become more than exploratory, the anchor must be predeclared/media-structural and pass local K plus theta handoff checks. Physiology-discovered anchors remain hypothesis-generating in the same run.\n")
        clk = results.get("candidate_local_kht", {})
        if isinstance(clk, dict):
            if "analysis" in clk:
                report.append(table_to_md(clk["analysis"].head(12), max_rows=12))
            if "anchors" in clk:
                report.append("\nAnchor manifest preview:\n")
                report.append(table_to_md(clk["anchors"].head(12), max_rows=12))

    if "mred" in results:
        report.append("## 20. MRED_v0.1 - Meaning Recognition / Encoding Dissociation\n")
        report.append("This module separates meaning-recognition or schema-reactivation load from theta-indexed new-integration/encoding load. High MeaningGamma/TSP/local K without theta carryover is treated as possible recognition or old-memory reactivation, not as a failed meaning event. Lack of theta handoff is not proof that no memory was encoded; it means the suite did not detect its operational theta-carryover marker.\n")
        mred = results.get("mred", {})
        if isinstance(mred, dict):
            if "interpretation" in mred:
                report.append(table_to_md(mred["interpretation"], max_rows=3))
            if "quadrants" in mred:
                report.append("\nQuadrant counts:\n")
                report.append(table_to_md(mred["quadrants"], max_rows=20))
            if "events" in mred:
                report.append("\nTop MRED event rows:\n")
                report.append(table_to_md(mred["events"].head(12), max_rows=12))

    report.append("## 21. Recommended interpretation discipline\n")
    report.append("- A positive self-report does not replace physiology.\n")
    report.append("- A physiological pattern does not replace experience.\n")
    report.append("- Lower-gamma power alone is not meaning. Gamma is treated as biological work whose source must be modeled.\n")
    report.append("- Cue task correctness should be interpreted with cue visibility, analytic effort, override leakage, and task engagement.\n")
    report.append("- Respiration, report/input motion, EMG/EOG, stimulus timing, and visual/audio pacing remain common-drive alternatives.\n")

    rpath = out / "report" / "master_comprehensive_praycg_report.md"
    with open(rpath, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    if cfg.make_html:
        html = "<html><head><meta charset='utf-8'><title>PRAYCG Master Report</title><style>body{font-family:Arial, sans-serif; max-width:1100px; margin:40px auto; line-height:1.4} table{border-collapse:collapse;font-size:12px}td,th{border:1px solid #ccc;padding:4px 6px} code{background:#eee;padding:1px 3px}</style></head><body>" + "\n".join(report).replace("\n", "<br>\n") + "</body></html>"
        with open(out / "report" / "master_comprehensive_praycg_report.html", "w", encoding="utf-8") as f:
            f.write(html)
    logger(f"Report written: {rpath}")
    return rpath


# ---------------------------
# Main suite runner
# ---------------------------

def run_suite(cfg: SuiteConfig, progress_cb: Optional[Callable[[str], None]] = None) -> Path:
    if not SCI_AVAILABLE:
        raise RuntimeError("numpy/pandas/scipy/matplotlib are required. Install requirements_master_suite_v1_0.txt.")
    project = sanitize_name(cfg.project_name)
    root = Path(cfg.out_root).expanduser().resolve()
    out = root / f"{project}_MasterComprehensiveSuite_v{VERSION}_{now_stamp()}"
    if out.exists() and not cfg.overwrite:
        raise FileExistsError(f"Output folder exists: {out}")
    ensure_dir(out)
    for sub in ["tables", "figures", "report", "logs", "provenance", "config"]:
        ensure_dir(out / sub)
    logger = RunLogger(out / "logs" / "run_log.txt", progress_cb)
    safe_json_dump(asdict(cfg), out / "config" / "run_config.json")
    results: Dict[str, Any] = {}
    errors = []

    streams: List[dict] = []
    try:
        streams, _ = load_xdf_streams(cfg.xdf_path, logger) if cfg.xdf_path else ([], {})
        if cfg.modules.get("stream_inventory"):
            results["stream_inventory"] = create_stream_inventory(streams, out)
    except Exception as e:
        errors.append("XDF load / stream inventory failed:\n" + traceback.format_exc())
        logger(f"WARNING: XDF load/inventory failed: {e}")

    try:
        xdf_events = extract_markers_from_xdf(streams) if streams else pd.DataFrame(columns=["marker","lsl_time","phase","note","source"])
        log_events = load_event_log(cfg.event_log_path)
        events = select_event_source(xdf_events, log_events, cfg.preferred_marker_source, logger)
        events.to_csv(out / "tables" / "events_used.csv", index=False)
        marker_status = {
            "xdf_marker_count": len(xdf_events),
            "event_log_marker_count": len(log_events),
            "used_marker_count": len(events),
            "used_marker_source": events["source"].iloc[0] if len(events) else "none",
            "stasis_markers_in_xdf": bool(len(xdf_events) and xdf_events["source"].astype(str).str.contains("StasisMarkers", case=False).any()),
        }
        results["marker_status"] = marker_status
        segments = build_segments(events, out, cfg, logger)
    except Exception as e:
        errors.append("Marker parsing / segment construction failed:\n" + traceback.format_exc())
        logger(f"WARNING: markers/segments failed: {e}")
        events = pd.DataFrame(columns=["marker","lsl_time","phase","note","source"])
        segments = pd.DataFrame()

    try:
        eeg_s = choose_eeg_stream(streams) if streams else None
        nchan = stream_channel_count(eeg_s) if eeg_s is not None else 16
        cmap = load_channel_map(cfg, nchan, out, logger)
        results["channel_map"] = cmap
    except Exception as e:
        errors.append("Channel map failed:\n" + traceback.format_exc())
        logger(f"WARNING: channel map failed: {e}")
        cmap = built_in_channel_map("anonymous", 16)

    try:
        if cfg.modules.get("cue_schedule_validation"):
            cue_summary, cue_events = load_cue_schedule(cfg, out, events)
            results["cue_summary"] = cue_summary
        else:
            cue_summary, cue_events = {}, pd.DataFrame()
    except Exception as e:
        errors.append("Cue validation failed:\n" + traceback.format_exc())
        logger(f"WARNING: cue validation failed: {e}")
        cue_summary, cue_events = {}, pd.DataFrame()

    try:
        if cfg.modules.get("override_task_scoring"):
            results["override_scoring"] = score_override(events, cue_summary, out)
    except Exception as e:
        errors.append("Override scoring failed:\n" + traceback.format_exc())
        logger(f"WARNING: override scoring failed: {e}")

    try:
        if cfg.modules.get("self_report_summary"):
            long, wide = parse_ratings(events, out)
            results["ratings_long"] = long
            results["ratings_wide"] = wide
    except Exception as e:
        errors.append("Self-report parsing failed:\n" + traceback.format_exc())
        logger(f"WARNING: ratings failed: {e}")

    try:
        if cfg.modules.get("report_input_artifact_handling"):
            exclusions = build_exclusion_windows(events, cfg, out)
            results["exclusions"] = exclusions
        else:
            exclusions = pd.DataFrame()
    except Exception as e:
        errors.append("Artifact exclusion windows failed:\n" + traceback.format_exc())
        logger(f"WARNING: exclusion windows failed: {e}")
        exclusions = pd.DataFrame()

    # Physiology first because it is independent and useful for reports.
    try:
        if cfg.modules.get("autonomic_api"):
            hrv = summarize_hrv(streams, segments, out, logger)
            results["hrv"] = hrv
        else:
            hrv = pd.DataFrame()
    except Exception as e:
        errors.append("HRV/API failed:\n" + traceback.format_exc())
        logger(f"WARNING: HRV/API failed: {e}")
        hrv = pd.DataFrame()

    try:
        if cfg.modules.get("respiration_summary"):
            resp = summarize_respiration(streams, segments, out, logger)
            results["respiration"] = resp
        else:
            resp = pd.DataFrame()
    except Exception as e:
        errors.append("Respiration summary failed:\n" + traceback.format_exc())
        logger(f"WARNING: respiration failed: {e}")
        resp = pd.DataFrame()

    # EEG and all downstream EEG modules.
    try:
        if any(cfg.modules.get(k) for k in ["eeg_qc", "mapped_lower_gamma", "gammascalpel", "task_lock_plv", "pac_exploratory", "formal_pncc_theta", "post_meaning_cascade", "temporal_semantic_proxy", "postpeak_pncc_theta", "annotation_locked_theta_carryover", "gamma_to_theta_handoff", "temporal_semantic_proxy_to_theta_handoff", "thresholded_state_update", "state_locked_handoff_alignment", "human_translation_kht", "candidate_local_kht", "meaning_recognition_encoding_dissociation", "media_covariate_inventory", "constrained_dtw_exploratory"]):
            features, eeg_qc = extract_eeg_features(streams, segments, exclusions, cmap, cfg, out, logger)
            features = standardize_feature_columns(features)
            results["eeg_features"] = features
            if cfg.modules.get("eeg_qc"):
                results["eeg_qc"] = eeg_qc
        else:
            features, eeg_qc = pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        errors.append("EEG feature extraction failed:\n" + traceback.format_exc())
        logger(f"WARNING: EEG feature extraction failed: {e}")
        features, eeg_qc = pd.DataFrame(), pd.DataFrame()

    try:
        if (features is None or len(features) == 0) and cfg.feature_table_path and Path(cfg.feature_table_path).exists():
            features = standardize_feature_columns(pd.read_csv(cfg.feature_table_path))
            results["eeg_features"] = features
            logger(f"Loaded external feature table: {cfg.feature_table_path}")
    except Exception as e:
        errors.append("External feature table load failed:\n" + traceback.format_exc())
        logger(f"WARNING: external feature table load failed: {e}")

    try:
        if cfg.modules.get("mapped_lower_gamma") or cfg.modules.get("task_lock_plv"):
            contrasts = run_core_contrasts(features, cfg, out, logger)
            results["contrasts"] = contrasts
        else:
            contrasts = pd.DataFrame()
    except Exception as e:
        errors.append("Core EEG contrasts failed:\n" + traceback.format_exc())
        logger(f"WARNING: core contrasts failed: {e}")
        contrasts = pd.DataFrame()

    try:
        if cfg.modules.get("residualized_lower_gamma"):
            resid = run_residualized_lgamma(features, resp, cfg, out, logger)
            results["residualized"] = resid
        else:
            resid = pd.DataFrame()
    except Exception as e:
        errors.append("Residualized lower-gamma failed:\n" + traceback.format_exc())
        logger(f"WARNING: residualized lower-gamma failed: {e}")
        resid = pd.DataFrame()

    try:
        if cfg.modules.get("gammascalpel"):
            gs_scores, gs_contrasts = run_gammascalpel(features, hrv, cfg, out, logger)
            results["gammascalpel_scores"] = gs_scores
            results["gammascalpel_contrasts"] = gs_contrasts
            if len(features) and len(gs_scores):
                merge_keys = [k for k in ["segment", "window_start", "window_end"] if k in features.columns and k in gs_scores.columns]
                score_cols = [c for c in gs_scores.columns if c.startswith("TaskGamma_") or c.startswith("MeaningGamma_")]
                if merge_keys and score_cols:
                    features = standardize_feature_columns(features.merge(gs_scores[merge_keys + score_cols], on=merge_keys, how="left"))
                    results["eeg_features"] = features
        else:
            gs_contrasts = pd.DataFrame()
    except Exception as e:
        errors.append("GammaScalpel failed:\n" + traceback.format_exc())
        logger(f"WARNING: GammaScalpel failed: {e}")
        gs_contrasts = pd.DataFrame()

    try:
        if cfg.modules.get("formal_pncc_theta") or cfg.modules.get("tau_coh_theta") or cfg.modules.get("surrogate_theta_carryover"):
            pncc, tau = run_pncc_theta(features, cfg, out, logger)
            results["pncc"] = pncc
            results["tau"] = tau
        else:
            pncc, tau = pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        errors.append("PNCC/tau theta failed:\n" + traceback.format_exc())
        logger(f"WARNING: PNCC/tau failed: {e}")
        pncc, tau = pd.DataFrame(), pd.DataFrame()

    try:
        if cfg.modules.get("post_meaning_cascade"):
            cascade_key, cascade_order = run_frequency_cascade(features, cfg, out)
            results["cascade_key"] = cascade_key
            results["cascade_order"] = cascade_order
        else:
            cascade_key, cascade_order = pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        errors.append("Frequency cascade failed:\n" + traceback.format_exc())
        logger(f"WARNING: cascade failed: {e}")
        cascade_key, cascade_order = pd.DataFrame(), pd.DataFrame()

    try:
        if any(cfg.modules.get(k) for k in ["temporal_semantic_proxy", "postpeak_pncc_theta", "annotation_locked_theta_carryover", "gamma_to_theta_handoff", "temporal_semantic_proxy_to_theta_handoff", "thresholded_state_update", "state_locked_handoff_alignment", "human_translation_kht", "candidate_local_kht", "meaning_recognition_encoding_dissociation", "media_covariate_inventory", "constrained_dtw_exploratory"]):
            if len(features):
                features = add_relative_time(features)
                if cfg.modules.get("temporal_semantic_proxy") or cfg.modules.get("temporal_semantic_proxy_to_theta_handoff"):
                    features = compute_temporal_semantic_proxy(features, out)
                    results["eeg_features"] = features
                annotations = load_annotation_csv(cfg.annotation_csv, out, logger) if getattr(cfg, "annotation_csv", "") else pd.DataFrame()
                results["annotations"] = annotations
                peaks = detect_peak_and_taper(features, cfg, out) if any(cfg.modules.get(k) for k in ["postpeak_pncc_theta", "thresholded_state_update", "state_locked_handoff_alignment", "constrained_dtw_exploratory"]) else pd.DataFrame()
                results["postpeak_peaks"] = peaks
                postpeak = run_postpeak_pncc_theta(features, peaks, cfg, out, logger) if cfg.modules.get("postpeak_pncc_theta") else pd.DataFrame()
                results["postpeak_pncc"] = postpeak
                anncarry = run_annotation_locked_theta_carryover(features, annotations, cfg, out, logger) if cfg.modules.get("annotation_locked_theta_carryover") else pd.DataFrame()
                results["annotation_theta"] = anncarry
                lagcorr, lagbest = run_gamma_to_theta_handoff(features, cfg, out, logger) if (cfg.modules.get("gamma_to_theta_handoff") or cfg.modules.get("temporal_semantic_proxy_to_theta_handoff")) else (pd.DataFrame(), pd.DataFrame())
                results["g2theta_lagcorr"] = lagcorr
                results["g2theta_best"] = lagbest
                results["handoff_endpoint"] = build_handoff_endpoint_table(postpeak, anncarry, lagbest, out)
                if cfg.modules.get("thresholded_state_update"):
                    tsu_windows, tsu_summary = run_thresholded_state_update(features, peaks, annotations, cfg, out, logger)
                    results["thresholded_state_update_windows"] = tsu_windows
                    results["thresholded_state_update_summary"] = tsu_summary
                if cfg.modules.get("state_locked_handoff_alignment") or cfg.modules.get("constrained_dtw_exploratory"):
                    slha = run_state_locked_handoff_alignment(features, peaks, annotations, cfg, out, logger)
                    results["state_locked_handoff_alignment"] = slha
                if cfg.modules.get("candidate_local_kht"):
                    try:
                        clk = run_candidate_local_kht(features, peaks, annotations, cfg, out, logger)
                        results["candidate_local_kht"] = clk
                    except Exception:
                        logger("WARNING: CandidateLocal_KHT failed:\n" + traceback.format_exc())
                if cfg.modules.get("meaning_recognition_encoding_dissociation"):
                    try:
                        mred = run_mred_layer(features, results.get("candidate_local_kht", {}), annotations, cfg, out, logger)
                        results["mred"] = mred
                    except Exception:
                        logger("WARNING: MRED_v0.1 failed:\n" + traceback.format_exc())
                if cfg.modules.get("human_translation_kht") or cfg.modules.get("media_covariate_inventory"):
                    try:
                        kht = run_human_translation_kht(features, cfg, out, logger)
                        results["human_translation_kht"] = kht
                    except Exception:
                        logger("WARNING: HumanTranslation_KHT failed:\n" + traceback.format_exc())
            else:
                logger("Handoff/K_HT modules requested but EEG feature table is empty.")
                if cfg.modules.get("media_covariate_inventory"):
                    results["human_translation_kht"] = run_human_translation_kht(pd.DataFrame(), cfg, out, logger)
                if cfg.modules.get("candidate_local_kht"):
                    results["candidate_local_kht"] = run_candidate_local_kht(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), cfg, out, logger)
                if cfg.modules.get("meaning_recognition_encoding_dissociation"):
                    results["mred"] = run_mred_layer(pd.DataFrame(), results.get("candidate_local_kht", {}), pd.DataFrame(), cfg, out, logger)
    except Exception as e:
        errors.append("Post-peak / gamma-to-theta handoff modules failed:\n" + traceback.format_exc())
        logger(f"WARNING: handoff modules failed: {e}")

    try:
        if cfg.modules.get("master_endpoint_table"):
            endpoint = build_master_endpoint_table(contrasts, resid, gs_contrasts, hrv, pncc, tau, cascade_order, out)
            results["endpoint"] = endpoint
    except Exception as e:
        errors.append("Endpoint status table failed:\n" + traceback.format_exc())
        logger(f"WARNING: endpoint table failed: {e}")

    try:
        if cfg.modules.get("figures"):
            make_figures(features, hrv, resp, results.get("ratings_wide", pd.DataFrame()), results.get("endpoint", pd.DataFrame()), out, logger)
    except Exception as e:
        errors.append("Figure generation failed:\n" + traceback.format_exc())
        logger(f"WARNING: figure generation failed: {e}")

    if errors:
        with open(out / "logs" / "errors.txt", "w", encoding="utf-8") as f:
            f.write("\n\n".join(errors))
    safe_json_dump({"config": asdict(cfg), "output_folder": str(out), "errors_count": len(errors)}, out / "manifest.json")
    build_report(cfg, out, results, logger)
    logger(f"Suite complete. Output folder: {out}")
    return out


# ---------------------------
# GUI
# ---------------------------

class MasterSuiteGUI:
    def __init__(self):
        if not TK_AVAILABLE:
            raise RuntimeError("tkinter is not available. Use --no-gui mode.")
        self.root = tk.Tk()
        self.root.title("PRAYCG Master Comprehensive Suite v1.3")
        self.root.geometry("950x780")
        self.vars: Dict[str, Any] = {}
        self.module_vars: Dict[str, tk.BooleanVar] = {}
        self._build()

    def file_row(self, parent, label, key, filetypes=(('All files','*.*'),)):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=2)
        ttk.Label(frame, text=label, width=26).pack(side="left")
        var = tk.StringVar()
        self.vars[key] = var
        ttk.Entry(frame, textvariable=var).pack(side="left", fill="x", expand=True, padx=4)
        def browse():
            path = filedialog.askopenfilename(title=label, filetypes=filetypes)
            if path:
                var.set(path)
        ttk.Button(frame, text="Browse", command=browse).pack(side="left")

    def dir_row(self, parent, label, key):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=2)
        ttk.Label(frame, text=label, width=26).pack(side="left")
        var = tk.StringVar(value="outputs")
        self.vars[key] = var
        ttk.Entry(frame, textvariable=var).pack(side="left", fill="x", expand=True, padx=4)
        def browse():
            path = filedialog.askdirectory(title=label)
            if path:
                var.set(path)
        ttk.Button(frame, text="Browse", command=browse).pack(side="left")

    def text_row(self, parent, label, key, default=""):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=2)
        ttk.Label(frame, text=label, width=26).pack(side="left")
        var = tk.StringVar(value=default)
        self.vars[key] = var
        ttk.Entry(frame, textvariable=var).pack(side="left", fill="x", expand=True, padx=4)

    def combo_row(self, parent, label, key, values, default):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=2)
        ttk.Label(frame, text=label, width=26).pack(side="left")
        var = tk.StringVar(value=default)
        self.vars[key] = var
        cb = ttk.Combobox(frame, textvariable=var, values=values, state="readonly")
        cb.pack(side="left", fill="x", expand=True, padx=4)

    def _build(self):
        outer = ttk.Frame(self.root, padding=10)
        outer.pack(fill="both", expand=True)
        nb = ttk.Notebook(outer)
        nb.pack(fill="both", expand=True)

        tab_inputs = ttk.Frame(nb, padding=10)
        nb.add(tab_inputs, text="Inputs")
        self.text_row(tab_inputs, "Project / run name", "project_name", "PRAYCG_Run")
        self.file_row(tab_inputs, "XDF file", "xdf_path", filetypes=(('XDF files','*.xdf'),('All files','*.*')))
        self.file_row(tab_inputs, "Local event log JSON/CSV", "event_log_path", filetypes=(('Event logs','*.json *.csv'),('All files','*.*')))
        self.file_row(tab_inputs, "Channel map CSV", "channel_map_path", filetypes=(('CSV files','*.csv'),('All files','*.*')))
        self.file_row(tab_inputs, "Cue schedule JSON", "cue_schedule_json", filetypes=(('JSON files','*.json'),('All files','*.*')))
        self.file_row(tab_inputs, "Cue schedule CSV", "cue_schedule_csv", filetypes=(('CSV files','*.csv'),('All files','*.*')))
        self.file_row(tab_inputs, "MediaPrep manifest JSON", "media_manifest_json", filetypes=(('JSON files','*.json'),('All files','*.*')))
        self.file_row(tab_inputs, "Predeclared anchor JSON/CSV", "predeclared_anchor_file", filetypes=(('Anchor files','*.json *.csv'),('All files','*.*')))
        self.file_row(tab_inputs, "MRED familiarity CSV", "mred_familiarity_csv", filetypes=(('CSV files','*.csv'),('All files','*.*')))
        self.file_row(tab_inputs, "MRED scene map CSV", "mred_scene_map_csv", filetypes=(('CSV files','*.csv'),('All files','*.*')))
        self.file_row(tab_inputs, "Annotation CSV", "annotation_csv", filetypes=(('CSV files','*.csv'),('All files','*.*')))
        self.file_row(tab_inputs, "Feature table CSV", "feature_table_path", filetypes=(('CSV files','*.csv'),('All files','*.*')))
        self.dir_row(tab_inputs, "StimulusFingerprint folder", "stimulus_fingerprint_folder")
        self.dir_row(tab_inputs, "Output root", "out_root")

        tab_config = ttk.Frame(nb, padding=10)
        nb.add(tab_config, text="Config")
        self.combo_row(tab_config, "Stimulus style", "stimulus_style", STIMULUS_STYLES, "delayed_reveal")
        self.combo_row(tab_config, "Channel map preset", "channel_map_preset", ["PRAYCG16_FIXED_ORDER_v1", "OpenBCI_MarkIV_Default_16", "anonymous_16", "custom_csv"], "PRAYCG16_FIXED_ORDER_v1")
        self.combo_row(tab_config, "Channel map confidence", "channel_map_confidence", ["LOCKED", "PROBABLE", "RETROSPECTIVE", "UNKNOWN"], "LOCKED")
        self.combo_row(tab_config, "Marker source", "preferred_marker_source", ["auto", "xdf", "event_log"], "auto")
        self.text_row(tab_config, "EEG window sec", "eeg_window_sec", "2.0")
        self.text_row(tab_config, "EEG step sec", "eeg_step_sec", "1.0")
        self.text_row(tab_config, "Report prepad sec", "report_prepad_sec", "3.0")
        self.text_row(tab_config, "Report postpad sec", "report_postpad_sec", "5.0")
        self.text_row(tab_config, "Reveal windows sec", "reveal_windows_sec", "20,30,40,60,90")
        self.text_row(tab_config, "Washout splits sec", "washout_splits_sec", "0-30,30-90,90-120")
        self.text_row(tab_config, "Surrogates", "n_surrogates", "500")
        self.text_row(tab_config, "Random seed", "random_seed", "20260724")

        tab_modules = ttk.Frame(nb, padding=10)
        nb.add(tab_modules, text="Modules")
        row = 0
        col = 0
        grid = ttk.Frame(tab_modules)
        grid.pack(fill="both", expand=True)
        for k, default in DEFAULT_MODULES.items():
            var = tk.BooleanVar(value=default)
            self.module_vars[k] = var
            cb = ttk.Checkbutton(grid, text=k, variable=var)
            cb.grid(row=row, column=col, sticky="w", padx=6, pady=3)
            row += 1
            if row > 12:
                row = 0
                col += 1
        btns = ttk.Frame(tab_modules)
        btns.pack(fill="x", pady=10)
        ttk.Button(btns, text="Select all", command=lambda: [v.set(True) for v in self.module_vars.values()]).pack(side="left")
        ttk.Button(btns, text="Clear optional-heavy", command=self._clear_heavy).pack(side="left", padx=6)

        tab_run = ttk.Frame(nb, padding=10)
        nb.add(tab_run, text="Run")
        self.status = tk.Text(tab_run, height=24, wrap="word")
        self.status.pack(fill="both", expand=True)
        buttons = ttk.Frame(tab_run)
        buttons.pack(fill="x", pady=8)
        ttk.Button(buttons, text="Run Master Suite", command=self.run_clicked).pack(side="left")
        ttk.Button(buttons, text="Quit", command=self.root.destroy).pack(side="right")

    def _clear_heavy(self):
        for k in ["pac_exploratory", "figures"]:
            if k in self.module_vars:
                self.module_vars[k].set(False)

    def append_status(self, msg: str):
        self.status.insert("end", msg + "\n")
        self.status.see("end")
        self.root.update_idletasks()

    def get_config(self) -> SuiteConfig:
        def f(key, default=0.0):
            try: return float(self.vars[key].get())
            except Exception: return default
        def i(key, default=0):
            try: return int(float(self.vars[key].get()))
            except Exception: return default
        modules = {k: v.get() for k, v in self.module_vars.items()}
        return SuiteConfig(
            project_name=self.vars["project_name"].get(),
            xdf_path=self.vars["xdf_path"].get(),
            event_log_path=self.vars["event_log_path"].get(),
            channel_map_path=self.vars["channel_map_path"].get(),
            cue_schedule_json=self.vars["cue_schedule_json"].get(),
            cue_schedule_csv=self.vars["cue_schedule_csv"].get(),
            stimulus_fingerprint_folder=self.vars["stimulus_fingerprint_folder"].get(),
            annotation_csv=self.vars["annotation_csv"].get(),
            media_manifest_json=self.vars["media_manifest_json"].get(),
            predeclared_anchor_file=self.vars["predeclared_anchor_file"].get(),
            mred_familiarity_csv=self.vars["mred_familiarity_csv"].get(),
            mred_scene_map_csv=self.vars["mred_scene_map_csv"].get(),
            out_root=self.vars["out_root"].get(),
            stimulus_style=self.vars["stimulus_style"].get(),
            channel_map_preset=self.vars["channel_map_preset"].get(),
            channel_map_confidence=self.vars["channel_map_confidence"].get(),
            preferred_marker_source=self.vars["preferred_marker_source"].get(),
            eeg_window_sec=f("eeg_window_sec", 2.0),
            eeg_step_sec=f("eeg_step_sec", 1.0),
            report_prepad_sec=f("report_prepad_sec", 3.0),
            report_postpad_sec=f("report_postpad_sec", 5.0),
            reveal_windows_sec=self.vars["reveal_windows_sec"].get(),
            washout_splits_sec=self.vars["washout_splits_sec"].get(),
            n_surrogates=i("n_surrogates", 500),
            random_seed=i("random_seed", 20260724),
            modules=modules,
        )

    def run_clicked(self):
        cfg = self.get_config()
        self.append_status("Starting master suite...")
        try:
            out = run_suite(cfg, progress_cb=self.append_status)
            messagebox.showinfo("Complete", f"Master suite complete.\n\nOutput folder:\n{out}")
        except Exception as e:
            tb = traceback.format_exc()
            self.append_status(tb)
            messagebox.showerror("Master suite failed", str(e))

    def mainloop(self):
        self.root.mainloop()


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="PRAYCG Master Comprehensive Post-Processing Suite v1.4.3")
    p.add_argument("--no-gui", action="store_true", help="Run without GUI.")
    p.add_argument("--project-name", default="PRAYCG_Run")
    p.add_argument("--xdf", dest="xdf_path", default="")
    p.add_argument("--event-log", dest="event_log_path", default="")
    p.add_argument("--channel-map", dest="channel_map_path", default="")
    p.add_argument("--cue-schedule-json", default="")
    p.add_argument("--cue-schedule-csv", default="")
    p.add_argument("--stimulus-fingerprint-folder", default="")
    p.add_argument("--annotation-csv", default="")
    p.add_argument("--feature-table-path", default="")
    p.add_argument("--media-manifest-json", default="")
    p.add_argument("--predeclared-anchor-file", default="", help="Optional PRAYCG1.8B predeclared anchor JSON/CSV.")
    p.add_argument("--mred-familiarity-csv", default="", help="Optional MRED familiarity/novelty covariates CSV.")
    p.add_argument("--mred-scene-map-csv", default="", help="Optional MRED anchor scene map CSV.")
    p.add_argument("--out-root", default="outputs")
    p.add_argument("--stimulus-style", default="delayed_reveal", choices=STIMULUS_STYLES)
    p.add_argument("--channel-map-preset", default="PRAYCG16_FIXED_ORDER_v1", choices=["PRAYCG16_FIXED_ORDER_v1", "OpenBCI_MarkIV_Default_16", "anonymous_16", "custom_csv"])
    p.add_argument("--channel-map-confidence", default="LOCKED")
    p.add_argument("--marker-source", dest="preferred_marker_source", default="auto", choices=["auto", "xdf", "event_log"])
    p.add_argument("--eeg-window-sec", type=float, default=2.0)
    p.add_argument("--eeg-step-sec", type=float, default=1.0)
    p.add_argument("--report-prepad-sec", type=float, default=3.0)
    p.add_argument("--report-postpad-sec", type=float, default=5.0)
    p.add_argument("--reveal-windows-sec", default="20,30,40,60,90")
    p.add_argument("--washout-splits-sec", default="0-30,30-90,90-120")
    p.add_argument("--n-surrogates", type=int, default=500)
    p.add_argument("--random-seed", type=int, default=20260724)
    p.add_argument("--disable-module", action="append", default=[], help="Disable a module by name. Can be repeated.")
    p.add_argument("--enable-module", action="append", default=[], help="Enable a module by name. Can be repeated.")
    p.add_argument("--overwrite", action="store_true")
    return p.parse_args(argv)


def config_from_args(args: argparse.Namespace) -> SuiteConfig:
    modules = dict(DEFAULT_MODULES)
    for m in args.disable_module:
        if m in modules:
            modules[m] = False
    for m in args.enable_module:
        modules[m] = True
    return SuiteConfig(
        project_name=args.project_name,
        xdf_path=args.xdf_path,
        event_log_path=args.event_log_path,
        channel_map_path=args.channel_map_path,
        cue_schedule_json=args.cue_schedule_json,
        cue_schedule_csv=args.cue_schedule_csv,
        stimulus_fingerprint_folder=args.stimulus_fingerprint_folder,
        annotation_csv=args.annotation_csv,
        feature_table_path=args.feature_table_path,
        media_manifest_json=args.media_manifest_json,
        predeclared_anchor_file=args.predeclared_anchor_file,
        mred_familiarity_csv=args.mred_familiarity_csv,
        mred_scene_map_csv=args.mred_scene_map_csv,
        out_root=args.out_root,
        stimulus_style=args.stimulus_style,
        channel_map_preset=args.channel_map_preset,
        channel_map_confidence=args.channel_map_confidence,
        preferred_marker_source=args.preferred_marker_source,
        eeg_window_sec=args.eeg_window_sec,
        eeg_step_sec=args.eeg_step_sec,
        report_prepad_sec=args.report_prepad_sec,
        report_postpad_sec=args.report_postpad_sec,
        reveal_windows_sec=args.reveal_windows_sec,
        washout_splits_sec=args.washout_splits_sec,
        n_surrogates=args.n_surrogates,
        random_seed=args.random_seed,
        overwrite=args.overwrite,
        modules=modules,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    if args.no_gui or not TK_AVAILABLE:
        cfg = config_from_args(args)
        out = run_suite(cfg)
        print(f"\nComplete. Output folder: {out}")
        return 0
    gui = MasterSuiteGUI()
    gui.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
