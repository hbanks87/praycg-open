#!/usr/bin/env python3
"""
PRAYCG StimulusFingerprint Suite v1.5

Batch UI/orchestrator for PR-AYC-G stimulus QC.

Purpose:
- Let the operator select Control, Target, and Contextual Override MP4 files in one UI.
- Optionally select PR-AYC-G number-cue schedule JSON/CSV files.
- Run the full StimulusFingerprint v1.0 analysis on all three MP4s.
- Run pairwise physical-delivery comparisons.
- Write a master suite report, master tables, and manifest in one standardized folder.

Boundary:
This tool analyzes digital stimulus-delivery proxies: pixel luminance, visual change,
digital audio amplitude, timing, cue visibility, and physical-match metrics. It does not
measure literal photons at the retina, true dB SPL at the ear, or narrative meaning itself.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
FINGERPRINT_SCRIPT = SCRIPT_DIR / "praycg_stimulus_fingerprint_v1_0.py"
COMPARE_SCRIPT = SCRIPT_DIR / "praycg_compare_stimulus_fingerprints_v1_0.py"


@dataclass
class SuiteConfig:
    project_name: str
    control_mp4: Path
    target_mp4: Path
    override_mp4: Path
    cue_schedule_json: Optional[Path]
    cue_schedule_csv: Optional[Path]
    out_root: Path
    sample_fps: float = 5.0
    resize_width: int = 320
    make_plots: bool = True
    apply_cue_schedule_to_control: bool = False


def sanitize_name(name: str) -> str:
    clean = "".join(ch if ch.isalnum() or ch in ("-", "_", ".") else "_" for ch in name.strip())
    clean = clean.strip("._")
    return clean or "PRAYCG_StimulusSuite"


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
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


def run_subprocess(cmd: List[str], log) -> None:
    log("$ " + " ".join(f'\"{c}\"' if " " in str(c) else str(c) for c in cmd))
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.stdout is not None
    for line in proc.stdout:
        log(line.rstrip())
    code = proc.wait()
    if code != 0:
        raise RuntimeError(f"Command failed with exit code {code}: {' '.join(cmd)}")


def validate_config(cfg: SuiteConfig) -> None:
    if not FINGERPRINT_SCRIPT.exists():
        raise FileNotFoundError(f"Missing fingerprint script: {FINGERPRINT_SCRIPT}")
    if not COMPARE_SCRIPT.exists():
        raise FileNotFoundError(f"Missing comparison script: {COMPARE_SCRIPT}")
    for label, p in [
        ("control_mp4", cfg.control_mp4),
        ("target_mp4", cfg.target_mp4),
        ("override_mp4", cfg.override_mp4),
    ]:
        if not p.exists():
            raise FileNotFoundError(f"{label} not found: {p}")
        if p.suffix.lower() not in (".mp4", ".mov", ".m4v"):
            raise ValueError(f"{label} does not look like a video file: {p}")
    if cfg.cue_schedule_json and not cfg.cue_schedule_json.exists():
        raise FileNotFoundError(f"cue_schedule_json not found: {cfg.cue_schedule_json}")
    if cfg.cue_schedule_csv and not cfg.cue_schedule_csv.exists():
        raise FileNotFoundError(f"cue_schedule_csv not found: {cfg.cue_schedule_csv}")
    if cfg.sample_fps <= 0:
        raise ValueError("sample_fps must be positive")
    if cfg.resize_width < 80:
        raise ValueError("resize_width should be at least 80 pixels")


def fingerprint_one(label: str, mp4: Path, out_dir: Path, cfg: SuiteConfig, log) -> Path:
    out = out_dir / f"01_fingerprints/{label}"
    out.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(FINGERPRINT_SCRIPT),
        str(mp4),
        "--out",
        str(out),
        "--sample-fps",
        str(cfg.sample_fps),
        "--resize-width",
        str(cfg.resize_width),
    ]
    use_cue = cfg.cue_schedule_json and (label in ("target", "contextual_override") or cfg.apply_cue_schedule_to_control)
    if use_cue:
        cmd.extend(["--cue-schedule-json", str(cfg.cue_schedule_json)])
    if cfg.make_plots:
        cmd.append("--make-plots")
    run_subprocess(cmd, log)
    return out


def compare_pair(name: str, folder_a: Path, folder_b: Path, out_dir: Path, log) -> Path:
    out = out_dir / f"02_comparisons/{name}"
    out.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(COMPARE_SCRIPT),
        str(folder_a),
        str(folder_b),
        "--out",
        str(out),
    ]
    run_subprocess(cmd, log)
    return out


def flatten_condition_summary(label: str, folder: Path) -> Dict[str, Any]:
    summary_path = folder / "stimulus_fingerprint_summary.json"
    obj = read_json(summary_path)
    visual = obj.get("visual", {}) or {}
    audio = obj.get("audio", {}) or {}
    summ = obj.get("summary", {}) or {}
    cue = obj.get("cue_visibility", {}) or {}
    return {
        "condition": label,
        "input_file": obj.get("input_file"),
        "input_sha256": obj.get("input_sha256"),
        "duration_sec": visual.get("duration_sec"),
        "fps": visual.get("fps"),
        "width": visual.get("width"),
        "height": visual.get("height"),
        "mean_luminance_0_255": visual.get("mean_luminance_0_255"),
        "visual_change_mean_0_255": visual.get("visual_change_mean_0_255"),
        "cut_count_estimated": visual.get("cut_count_estimated"),
        "cut_rate_per_sec": visual.get("cut_rate_per_sec"),
        "flash_risk_0_1": visual.get("flash_risk_0_1"),
        "has_audio": audio.get("has_audio"),
        "dbfs_mean": audio.get("dbfs_mean"),
        "dbfs_peak": audio.get("dbfs_peak"),
        "silence_fraction": audio.get("silence_fraction"),
        "audio_envelope_rhythm_concentration_0_1": audio.get("envelope_rhythm_concentration_0_1"),
        "sensory_energy_proxy_0_100": summ.get("sensory_energy_proxy_0_100"),
        "visual_energy_proxy_0_1": summ.get("visual_energy_proxy_0_1"),
        "audio_energy_proxy_0_1": summ.get("audio_energy_proxy_0_1"),
        "exogenous_entrainment_risk_0_1": summ.get("exogenous_entrainment_risk_0_1"),
        "entrainment_risk_class": summ.get("entrainment_risk_class"),
        "overload_risk_0_1": summ.get("overload_risk_0_1"),
        "cue_visibility_available": cue.get("cue_visibility_available"),
        "cue_count": cue.get("cue_count"),
        "expected_sum": cue.get("expected_sum"),
        "visibility_weighted_sum": cue.get("visibility_weighted_sum"),
        "mean_visibility_score_0_1": cue.get("mean_visibility_score_0_1"),
        "low_visibility_count": cue.get("low_visibility_count"),
        "low_visibility_fraction": cue.get("low_visibility_fraction"),
    }


def flatten_comparison_summary(name: str, folder: Path) -> Dict[str, Any]:
    obj = read_json(folder / "stimulus_physical_match_summary.json")
    return {
        "comparison": name,
        "identical_file_hash": obj.get("identical_file_hash"),
        "physical_match_score_0_100": obj.get("physical_match_score_0_100"),
        "duration_similarity_0_1": obj.get("duration_similarity_0_1"),
        "fps_match_0_1": obj.get("fps_match_0_1"),
        "resolution_match_0_1": obj.get("resolution_match_0_1"),
        "luminance_timeline_correlation": obj.get("luminance_timeline_correlation"),
        "visual_change_timeline_correlation": obj.get("visual_change_timeline_correlation"),
        "audio_dbfs_timeline_correlation": obj.get("audio_dbfs_timeline_correlation"),
        "sha256_a": obj.get("sha256_a"),
        "sha256_b": obj.get("sha256_b"),
    }


def as_float(x: Any, default: float = float("nan")) -> float:
    try:
        return float(x)
    except Exception:
        return default


def classify_match(score: Any) -> str:
    s = as_float(score, -1)
    if s >= 90:
        return "excellent physical match"
    if s >= 80:
        return "good physical match"
    if s >= 70:
        return "usable/pilot physical match; interpret cautiously"
    if s >= 0:
        return "weak physical match; major caution"
    return "not available"


def make_master_report(out_dir: Path, cfg: SuiteConfig, condition_rows: List[Dict[str, Any]], comparison_rows: List[Dict[str, Any]], cue_meta: Dict[str, Any]) -> None:
    report_dir = out_dir / "00_master"
    report_dir.mkdir(parents=True, exist_ok=True)

    def fmt(x: Any, nd: int = 3) -> str:
        try:
            if x is None or x == "":
                return "NA"
            xf = float(x)
            if not (xf == xf):
                return "NA"
            return f"{xf:.{nd}f}"
        except Exception:
            return str(x)

    # Useful comparisons by name.
    comp_map = {r["comparison"]: r for r in comparison_rows}
    target_override = comp_map.get("target_vs_contextual_override", {})
    target_control = comp_map.get("target_vs_control", {})

    target_override_hash = target_override.get("identical_file_hash")
    target_override_match = target_override.get("physical_match_score_0_100")
    target_control_match = target_control.get("physical_match_score_0_100")

    # Cue visibility warnings.
    cue_rows = [r for r in condition_rows if r.get("cue_visibility_available")]
    worst_low_frac = max([as_float(r.get("low_visibility_fraction"), 0.0) for r in cue_rows] or [0.0])
    cue_warning = "none"
    if worst_low_frac >= 0.10:
        cue_warning = "high low-visibility cue fraction; regenerate overlays with stronger contrast"
    elif worst_low_frac >= 0.05:
        cue_warning = "moderate low-visibility cue fraction; inspect cue_visibility_qc.csv"
    elif cue_rows:
        cue_warning = "cue visibility mostly acceptable by current proxy"

    lines: List[str] = []
    lines += [
        "# PRAYCG StimulusFingerprint Suite v1.5 Master Report",
        "",
        f"Project: **{cfg.project_name}**",
        f"Created: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Boundary",
        "This suite reports digital sensory-delivery proxies and physical-match metrics. It does not measure literal photons at the retina, true dB SPL at the ear, narrative meaning, empathy, or consciousness. The output helps decide whether a stimulus suite is physically and operationally clean enough for PR-AYC-G acquisition.",
        "",
        "## Inputs",
        f"- Control MP4: `{cfg.control_mp4}`",
        f"- Target MP4: `{cfg.target_mp4}`",
        f"- Contextual Override MP4: `{cfg.override_mp4}`",
        f"- Cue schedule JSON: `{cfg.cue_schedule_json}`" if cfg.cue_schedule_json else "- Cue schedule JSON: `none`",
        f"- Cue schedule CSV: `{cfg.cue_schedule_csv}`" if cfg.cue_schedule_csv else "- Cue schedule CSV: `none`",
        f"- Sample FPS: {cfg.sample_fps}",
        f"- Resize width: {cfg.resize_width}",
        "",
        "## Executive QC verdict",
        f"- Target vs Contextual Override identical file hash: **{target_override_hash}**",
        f"- Target vs Contextual Override physical match: **{fmt(target_override_match, 2)}/100** ({classify_match(target_override_match)})",
        f"- Target vs Control physical match: **{fmt(target_control_match, 2)}/100** ({classify_match(target_control_match)})",
        f"- Cue visibility warning: **{cue_warning}**",
        "",
        "Interpretation: Target-vs-Override should ideally be identical or near-identical at the media-file level, because the intended difference is instruction/stance rather than photons. Target-vs-Control may be less perfect if the control is phase-scrambled, but duration, FPS, resolution, audio envelope, luminance dynamics, and visual-change structure should be as close as the method allows.",
        "",
        "## Condition fingerprint table",
        "",
        "| Condition | Duration s | FPS | Resolution | Sensory energy | Entrainment risk | Mean luminance | Visual change | Mean dBFS | Cue visibility | Low-vis cues |",
        "|---|---:|---:|---|---:|---|---:|---:|---:|---:|---:|",
    ]
    for r in condition_rows:
        res = f"{r.get('width')}x{r.get('height')}"
        lines.append(
            f"| {r.get('condition')} | {fmt(r.get('duration_sec'), 2)} | {fmt(r.get('fps'), 2)} | {res} | "
            f"{fmt(r.get('sensory_energy_proxy_0_100'), 2)} | {r.get('entrainment_risk_class')} | "
            f"{fmt(r.get('mean_luminance_0_255'), 2)} | {fmt(r.get('visual_change_mean_0_255'), 2)} | "
            f"{fmt(r.get('dbfs_mean'), 2)} | {fmt(r.get('mean_visibility_score_0_1'), 3)} | {r.get('low_visibility_count')} |"
        )

    lines += [
        "",
        "## Pairwise physical-match comparisons",
        "",
        "| Comparison | Identical hash | Physical match | Duration | FPS | Resolution | Luminance corr | Visual-change corr | Audio dBFS corr |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in comparison_rows:
        lines.append(
            f"| {r.get('comparison')} | {r.get('identical_file_hash')} | {fmt(r.get('physical_match_score_0_100'), 2)} | "
            f"{fmt(r.get('duration_similarity_0_1'), 3)} | {fmt(r.get('fps_match_0_1'), 3)} | "
            f"{fmt(r.get('resolution_match_0_1'), 3)} | {fmt(r.get('luminance_timeline_correlation'), 3)} | "
            f"{fmt(r.get('visual_change_timeline_correlation'), 3)} | {fmt(r.get('audio_dbfs_timeline_correlation'), 3)} |"
        )

    lines += [
        "",
        "## Cue schedule metadata",
    ]
    if cue_meta:
        cd = cue_meta.get("cue_design", {}) or {}
        lines += [
            f"- Schema: `{cue_meta.get('schema')}`",
            f"- Cue count: {cue_meta.get('cue_count')}",
            f"- Expected sum: {cue_meta.get('expected_sum')}",
            f"- Cue interval seconds: {cd.get('interval_sec')}",
            f"- Cue display duration seconds: {cd.get('display_duration_sec')}",
            f"- Cue position: {cd.get('position')}",
            f"- Recommended use: {cd.get('recommended_use')}",
        ]
    else:
        lines.append("- No cue schedule JSON supplied.")

    lines += [
        "",
        "## Standardized interpretation rules",
        "1. If Target and Override are not media-identical or near-identical, do not call the contrast purely psychological. The video files themselves differ.",
        "2. If cue visibility is degraded, contextual-override sum error is not pure noncompliance. It may reflect perceptual dropout.",
        "3. If the phase-scrambled Control is much brighter, more visually active, or has very different audio energy than Target, Target-vs-Control interpretation is weakened.",
        "4. If exogenous entrainment risk is high, future EEG analyses must model stimulus timing, visual change, audio envelope, respiration, and artifacts carefully.",
        "5. This suite categorizes the vehicle. It does not certify the meaning payload.",
        "",
        "## Output folders",
        "- `01_fingerprints/control/`",
        "- `01_fingerprints/target/`",
        "- `01_fingerprints/contextual_override/`",
        "- `02_comparisons/target_vs_control/`",
        "- `02_comparisons/target_vs_contextual_override/`",
        "- `02_comparisons/control_vs_contextual_override/`",
        "- `00_master/`",
    ]
    (report_dir / "PRAYCG_StimulusFingerprint_v1_5_master_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_suite(cfg: SuiteConfig, log=print) -> Path:
    validate_config(cfg)
    project = sanitize_name(cfg.project_name)
    out_dir = cfg.out_root.resolve() / f"{project}_StimulusFingerprint_v1_5_{now_stamp()}"
    out_dir.mkdir(parents=True, exist_ok=True)
    log(f"Output folder: {out_dir}")

    # Copy schedule files for provenance, but do not copy MP4 media by default.
    provenance_dir = out_dir / "03_provenance"
    provenance_dir.mkdir(parents=True, exist_ok=True)
    cue_meta: Dict[str, Any] = {}
    if cfg.cue_schedule_json:
        shutil.copy2(cfg.cue_schedule_json, provenance_dir / cfg.cue_schedule_json.name)
        try:
            cue_meta = read_json(cfg.cue_schedule_json)
        except Exception:
            cue_meta = {"error": "cue schedule JSON could not be parsed"}
    if cfg.cue_schedule_csv:
        shutil.copy2(cfg.cue_schedule_csv, provenance_dir / cfg.cue_schedule_csv.name)

    manifest = {
        "schema": "PRAYCG_stimulus_fingerprint_suite_v1_5",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "project_name": cfg.project_name,
        "control_mp4": str(cfg.control_mp4),
        "target_mp4": str(cfg.target_mp4),
        "contextual_override_mp4": str(cfg.override_mp4),
        "cue_schedule_json": str(cfg.cue_schedule_json) if cfg.cue_schedule_json else None,
        "cue_schedule_csv": str(cfg.cue_schedule_csv) if cfg.cue_schedule_csv else None,
        "sample_fps": cfg.sample_fps,
        "resize_width": cfg.resize_width,
        "make_plots": cfg.make_plots,
        "apply_cue_schedule_to_control": cfg.apply_cue_schedule_to_control,
    }
    write_json(out_dir / "00_master/stimulus_suite_manifest.json", manifest)

    folders: Dict[str, Path] = {}
    for label, mp4 in [
        ("control", cfg.control_mp4),
        ("target", cfg.target_mp4),
        ("contextual_override", cfg.override_mp4),
    ]:
        log(f"\n=== Fingerprinting {label}: {mp4.name} ===")
        folders[label] = fingerprint_one(label, mp4, out_dir, cfg, log)

    comp_folders: Dict[str, Path] = {}
    comparisons = [
        ("target_vs_control", folders["target"], folders["control"]),
        ("target_vs_contextual_override", folders["target"], folders["contextual_override"]),
        ("control_vs_contextual_override", folders["control"], folders["contextual_override"]),
    ]
    for name, a, b in comparisons:
        log(f"\n=== Comparing {name} ===")
        comp_folders[name] = compare_pair(name, a, b, out_dir, log)

    condition_rows = [flatten_condition_summary(label, folder) for label, folder in folders.items()]
    comparison_rows = [flatten_comparison_summary(name, folder) for name, folder in comp_folders.items()]

    master = out_dir / "00_master"
    master.mkdir(parents=True, exist_ok=True)
    write_csv(master / "stimulus_suite_metric_matrix.csv", condition_rows)
    write_csv(master / "stimulus_suite_pairwise_comparisons.csv", comparison_rows)

    master_summary = {
        "schema": "PRAYCG_stimulus_fingerprint_suite_summary_v1_5",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "project_name": cfg.project_name,
        "output_folder": str(out_dir),
        "conditions": condition_rows,
        "comparisons": comparison_rows,
        "cue_schedule_meta": {
            "schema": cue_meta.get("schema"),
            "cue_count": cue_meta.get("cue_count"),
            "expected_sum": cue_meta.get("expected_sum"),
            "cue_design": cue_meta.get("cue_design"),
            "output_cued_sha256": cue_meta.get("output_cued_sha256"),
            "output_override_sha256": cue_meta.get("output_override_sha256"),
        } if cue_meta else {},
    }
    write_json(master / "stimulus_suite_master_summary.json", master_summary)
    make_master_report(out_dir, cfg, condition_rows, comparison_rows, cue_meta)

    log("\nDONE. Master report:")
    log(str(master / "PRAYCG_StimulusFingerprint_v1_5_master_report.md"))
    return out_dir


# ----------------------------- GUI -----------------------------

def launch_gui() -> None:
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        from tkinter import ttk
    except Exception as e:
        raise RuntimeError("Tkinter is unavailable. Run with --no-gui and command-line paths instead.") from e

    root = tk.Tk()
    root.title("PRAYCG StimulusFingerprint Suite v1.5")
    root.geometry("980x720")

    vars: Dict[str, Any] = {
        "project_name": tk.StringVar(value="PRAYCG_StimulusSuite"),
        "control_mp4": tk.StringVar(),
        "target_mp4": tk.StringVar(),
        "override_mp4": tk.StringVar(),
        "cue_schedule_json": tk.StringVar(),
        "cue_schedule_csv": tk.StringVar(),
        "out_root": tk.StringVar(value=str(Path.home() / "Desktop")),
        "sample_fps": tk.StringVar(value="5.0"),
        "resize_width": tk.StringVar(value="320"),
        "make_plots": tk.BooleanVar(value=True),
        "apply_cue_to_control": tk.BooleanVar(value=False),
    }

    q: "queue.Queue[str]" = queue.Queue()
    running = {"value": False}

    def pick_file(varname: str, filetypes: List[Tuple[str, str]]) -> None:
        path = filedialog.askopenfilename(title=f"Select {varname}", filetypes=filetypes)
        if path:
            vars[varname].set(path)

    def pick_folder(varname: str) -> None:
        path = filedialog.askdirectory(title=f"Select {varname}")
        if path:
            vars[varname].set(path)

    main = ttk.Frame(root, padding=12)
    main.pack(fill="both", expand=True)
    title = ttk.Label(main, text="PRAYCG StimulusFingerprint Suite v1.5", font=("Segoe UI", 16, "bold"))
    title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
    sub = ttk.Label(main, text="Select Control, Target, Override, cue schedule, and output folder. One click runs the full media QC suite.")
    sub.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 12))

    rows = [
        ("Project / stimulus suite name", "project_name", None, None),
        ("Control MP4", "control_mp4", "file", [("Video files", "*.mp4 *.mov *.m4v"), ("All files", "*.*")]),
        ("Target MP4", "target_mp4", "file", [("Video files", "*.mp4 *.mov *.m4v"), ("All files", "*.*")]),
        ("Contextual Override MP4", "override_mp4", "file", [("Video files", "*.mp4 *.mov *.m4v"), ("All files", "*.*")]),
        ("Cue schedule JSON (optional)", "cue_schedule_json", "file", [("JSON files", "*.json"), ("All files", "*.*")]),
        ("Cue schedule CSV (optional/provenance)", "cue_schedule_csv", "file", [("CSV files", "*.csv"), ("All files", "*.*")]),
        ("Output root folder", "out_root", "folder", None),
        ("Video sample FPS", "sample_fps", None, None),
        ("Resize width", "resize_width", None, None),
    ]
    for i, (label, varname, kind, filetypes) in enumerate(rows, start=2):
        ttk.Label(main, text=label).grid(row=i, column=0, sticky="w", padx=(0, 8), pady=4)
        ent = ttk.Entry(main, textvariable=vars[varname], width=86)
        ent.grid(row=i, column=1, sticky="ew", pady=4)
        if kind == "file":
            ttk.Button(main, text="Browse", command=lambda v=varname, ft=filetypes: pick_file(v, ft)).grid(row=i, column=2, padx=(8, 0), pady=4)
        elif kind == "folder":
            ttk.Button(main, text="Browse", command=lambda v=varname: pick_folder(v)).grid(row=i, column=2, padx=(8, 0), pady=4)
    main.columnconfigure(1, weight=1)

    opts = ttk.Frame(main)
    opts.grid(row=11, column=0, columnspan=3, sticky="w", pady=(8, 8))
    ttk.Checkbutton(opts, text="Make plots", variable=vars["make_plots"]).pack(side="left", padx=(0, 18))
    ttk.Checkbutton(opts, text="Apply cue-visibility QC to Control too", variable=vars["apply_cue_to_control"]).pack(side="left")

    log_text = tk.Text(main, height=20, wrap="word")
    log_text.grid(row=13, column=0, columnspan=3, sticky="nsew", pady=(8, 8))
    main.rowconfigure(13, weight=1)

    def log_to_ui(msg: str) -> None:
        q.put(msg)

    def poll_queue() -> None:
        try:
            while True:
                msg = q.get_nowait()
                log_text.insert("end", msg + "\n")
                log_text.see("end")
        except queue.Empty:
            pass
        root.after(100, poll_queue)

    def build_config_from_ui() -> SuiteConfig:
        cue_json = vars["cue_schedule_json"].get().strip()
        cue_csv = vars["cue_schedule_csv"].get().strip()
        return SuiteConfig(
            project_name=vars["project_name"].get().strip() or "PRAYCG_StimulusSuite",
            control_mp4=Path(vars["control_mp4"].get().strip()),
            target_mp4=Path(vars["target_mp4"].get().strip()),
            override_mp4=Path(vars["override_mp4"].get().strip()),
            cue_schedule_json=Path(cue_json) if cue_json else None,
            cue_schedule_csv=Path(cue_csv) if cue_csv else None,
            out_root=Path(vars["out_root"].get().strip() or "."),
            sample_fps=float(vars["sample_fps"].get()),
            resize_width=int(float(vars["resize_width"].get())),
            make_plots=bool(vars["make_plots"].get()),
            apply_cue_schedule_to_control=bool(vars["apply_cue_to_control"].get()),
        )

    def run_clicked() -> None:
        if running["value"]:
            messagebox.showinfo("Already running", "The fingerprint suite is already running.")
            return
        try:
            cfg = build_config_from_ui()
            validate_config(cfg)
        except Exception as e:
            messagebox.showerror("Configuration error", str(e))
            return

        running["value"] = True
        run_button.config(state="disabled")
        log_text.insert("end", "Starting PRAYCG StimulusFingerprint Suite v1.5...\n")
        log_text.see("end")

        def worker() -> None:
            try:
                out = run_suite(cfg, log=log_to_ui)
                log_to_ui(f"SUITE COMPLETE: {out}")
                try:
                    if sys.platform.startswith("win"):
                        os.startfile(str(out))  # type: ignore[attr-defined]
                except Exception:
                    pass
            except Exception as e:
                log_to_ui("ERROR: " + str(e))
                log_to_ui(traceback.format_exc())
            finally:
                def finish() -> None:
                    running["value"] = False
                    run_button.config(state="normal")
                root.after(0, finish)

        threading.Thread(target=worker, daemon=True).start()

    buttons = ttk.Frame(main)
    buttons.grid(row=12, column=0, columnspan=3, sticky="w", pady=(8, 0))
    run_button = ttk.Button(buttons, text="Run Full Fingerprint Suite", command=run_clicked)
    run_button.pack(side="left")
    ttk.Button(buttons, text="Quit", command=root.destroy).pack(side="left", padx=10)

    poll_queue()
    root.mainloop()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="PRAYCG StimulusFingerprint Suite v1.5 UI/batch runner.")
    p.add_argument("--no-gui", action="store_true", help="Run headless from command-line arguments.")
    p.add_argument("--project-name", default="PRAYCG_StimulusSuite")
    p.add_argument("--control", help="Control MP4 file.")
    p.add_argument("--target", help="Target MP4 file.")
    p.add_argument("--override", help="Contextual Override MP4 file.")
    p.add_argument("--cue-schedule-json", default=None, help="Optional cue schedule JSON.")
    p.add_argument("--cue-schedule-csv", default=None, help="Optional cue schedule CSV for provenance.")
    p.add_argument("--out-root", default=str(Path.cwd()), help="Output root folder.")
    p.add_argument("--sample-fps", type=float, default=5.0)
    p.add_argument("--resize-width", type=int, default=320)
    p.add_argument("--no-plots", action="store_true", help="Disable plots.")
    p.add_argument("--apply-cue-schedule-to-control", action="store_true", help="Also run cue visibility QC on the Control MP4.")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.no_gui:
        missing = [name for name in ("control", "target", "override") if getattr(args, name) is None]
        if missing:
            raise SystemExit(f"Missing required args for --no-gui: {missing}")
        cfg = SuiteConfig(
            project_name=args.project_name,
            control_mp4=Path(args.control),
            target_mp4=Path(args.target),
            override_mp4=Path(args.override),
            cue_schedule_json=Path(args.cue_schedule_json) if args.cue_schedule_json else None,
            cue_schedule_csv=Path(args.cue_schedule_csv) if args.cue_schedule_csv else None,
            out_root=Path(args.out_root),
            sample_fps=args.sample_fps,
            resize_width=args.resize_width,
            make_plots=not args.no_plots,
            apply_cue_schedule_to_control=args.apply_cue_schedule_to_control,
        )
        out = run_suite(cfg)
        print(f"\nDONE: {out}")
    else:
        launch_gui()


if __name__ == "__main__":
    main()
