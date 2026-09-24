#!/usr/bin/env python3
"""
PRAYCG Unified Master Analysis + Visualizer v1.4.3
==================================================

One operational entry point for:
  1. Master Comprehensive Analysis only, or
  2. Master Comprehensive Analysis plus MasterSync Visualizer rendering.

This script is an orchestrator. It does not certify PR-AYC-G results, meaning,
OSM, hidden-Y biology, or human EEG mechanism. It runs the analysis and passes
its output folder to the visualizer for optional review MP4 generation.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import traceback
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False

VERSION = "1.4.3"
ROOT = Path(__file__).resolve().parent
MASTER_SCRIPT = ROOT / "praycg_master_comprehensive_suite_gui_v1_4.py"
VIS_SCRIPT = ROOT / "praycg_master_sync_visualizer_v1_2.py"


def run_cmd(cmd: List[str]) -> subprocess.CompletedProcess:
    print("\n>>> " + " ".join([str(c) for c in cmd]))
    return subprocess.run(cmd, text=True, capture_output=True)


def find_latest_analysis_folder(out_root: Path, project_name: str) -> Optional[Path]:
    if not out_root.exists():
        return None
    prefix = project_name.replace(" ", "_")
    candidates = [p for p in out_root.iterdir() if p.is_dir() and p.name.startswith(prefix)]
    if not candidates:
        # fallback: any MasterComprehensiveSuite folder
        candidates = [p for p in out_root.iterdir() if p.is_dir() and "MasterComprehensiveSuite" in p.name]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def build_master_cmd(args: argparse.Namespace) -> List[str]:
    cmd = [sys.executable, str(MASTER_SCRIPT), "--no-gui", "--project-name", args.project_name]
    def add(flag: str, value: str):
        if value:
            cmd.extend([flag, value])
    add("--xdf", args.xdf)
    add("--event-log", args.event_log)
    add("--channel-map", args.channel_map)
    add("--cue-schedule-json", args.cue_schedule_json)
    add("--cue-schedule-csv", args.cue_schedule_csv)
    add("--stimulus-fingerprint-folder", args.stimulus_fingerprint_folder)
    add("--annotation-csv", args.annotation_csv)
    add("--feature-table-path", args.feature_table_path)
    add("--media-manifest-json", args.media_manifest_json)
    add("--predeclared-anchor-file", args.predeclared_anchor_file)
    add("--mred-familiarity-csv", getattr(args, "mred_familiarity_csv", ""))
    add("--mred-scene-map-csv", getattr(args, "mred_scene_map_csv", ""))
    add("--out-root", args.out_root)
    add("--stimulus-style", args.stimulus_style)
    add("--channel-map-preset", args.channel_map_preset)
    add("--channel-map-confidence", args.channel_map_confidence)
    cmd.extend(["--n-surrogates", str(args.n_surrogates), "--random-seed", str(args.random_seed)])
    if args.overwrite:
        cmd.append("--overwrite")
    for m in args.disable_module or []:
        cmd.extend(["--disable-module", m])
    for m in args.enable_module or []:
        cmd.extend(["--enable-module", m])
    # CandidateLocal_KHT is enabled by default in v1.4, but keep this explicit in the run manifest.
    if "candidate_local_kht" not in (args.disable_module or []):
        cmd.extend(["--enable-module", "candidate_local_kht"])
    if "meaning_recognition_encoding_dissociation" not in (args.disable_module or []):
        cmd.extend(["--enable-module", "meaning_recognition_encoding_dissociation"])
    return cmd




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

def find_best_feature_csv(analysis_folder: Path) -> str:
    """Find best continuous feature CSV inside a Master Suite analysis folder."""
    search_roots = []
    if (analysis_folder / "tables").exists():
        search_roots.append(analysis_folder / "tables")
    search_roots.append(analysis_folder)
    for folder in search_roots:
        for name in FEATURE_CSV_PRIORITY_NAMES:
            cand = folder / name
            if cand.exists() and cand.is_file():
                return str(cand)
    for folder in search_roots:
        for pat in FEATURE_CSV_GLOB_PATTERNS:
            matches = sorted([m for m in folder.glob(pat) if m.is_file()])
            if matches:
                return str(matches[0])
    return ""

def build_visual_cmd(args: argparse.Namespace, analysis_folder: Path) -> List[str]:
    out_mp4 = Path(args.visual_out) if args.visual_out else Path(args.out_root) / f"{args.project_name}_MasterSync_{args.visual_condition}.mp4"
    cmd = [sys.executable, str(VIS_SCRIPT), "--out", str(out_mp4), "--analysis-out", str(analysis_folder)]
    def add(flag: str, value: str):
        if value:
            cmd.extend([flag, value])
    add("--xdf", args.xdf)
    feature_csv = args.visual_feature_csv or find_best_feature_csv(analysis_folder)
    add("--features", feature_csv)
    add("--video", args.visual_video)
    add("--events", args.visual_events)
    add("--condition", args.visual_condition)
    cmd.extend(["--fps", str(args.visual_fps), "--width", str(args.visual_width), "--video-height", str(args.visual_video_height), "--graph-height", str(args.visual_graph_height), "--rolling-window", str(args.visual_rolling_window), "--als-aux-channel", str(args.als_aux_channel)])
    return cmd


def run_pipeline(args: argparse.Namespace) -> Dict[str, Any]:
    out_root = Path(args.out_root).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    master_cmd = build_master_cmd(args)
    master_proc = run_cmd(master_cmd)
    print(master_proc.stdout)
    if master_proc.returncode != 0:
        print(master_proc.stderr, file=sys.stderr)
        raise RuntimeError(f"Master Comprehensive Suite failed with code {master_proc.returncode}")
    analysis_folder = find_latest_analysis_folder(out_root, args.project_name)
    if not analysis_folder:
        raise RuntimeError("Could not locate Master Comprehensive output folder after analysis.")
    result: Dict[str, Any] = {
        "schema": "PRAYCG_Unified_Master_Analysis_Visualizer_v1_4_1_run_result",
        "version": VERSION,
        "mode": args.mode,
        "analysis_folder": str(analysis_folder),
        "master_command": master_cmd,
        "master_stdout_tail": master_proc.stdout.splitlines()[-20:],
        "boundary": "Tools only: does not certify meaning, OSM, hidden-Y biology, or human EEG mechanism.",
    }
    if args.mode in {"analysis_plus_visual", "both"}:
        if not args.visual_video:
            raise RuntimeError("--visual-video is required for analysis_plus_visual mode.")
        vis_cmd = build_visual_cmd(args, analysis_folder)
        vis_proc = run_cmd(vis_cmd)
        print(vis_proc.stdout)
        if vis_proc.returncode != 0:
            print(vis_proc.stderr, file=sys.stderr)
            raise RuntimeError(f"MasterSync Visualizer failed with code {vis_proc.returncode}")
        result.update({
            "visual_command": vis_cmd,
            "visual_stdout_tail": vis_proc.stdout.splitlines()[-20:],
        })
    result_path = out_root / f"{args.project_name}_unified_run_result_v1_4_1.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("\nUnified run result:", result_path)
    return result


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="PRAYCG Unified Master Analysis + Visualizer v1.4.3")
    p.add_argument("--gui", action="store_true", help="Launch GUI.")
    p.add_argument("--mode", default="analysis_only", choices=["analysis_only", "analysis_plus_visual", "both"])
    p.add_argument("--project-name", default="PRAYCG_Run")
    p.add_argument("--xdf", default="")
    p.add_argument("--event-log", default="")
    p.add_argument("--channel-map", default="")
    p.add_argument("--cue-schedule-json", default="")
    p.add_argument("--cue-schedule-csv", default="")
    p.add_argument("--stimulus-fingerprint-folder", default="")
    p.add_argument("--annotation-csv", default="")
    p.add_argument("--feature-table-path", default="")
    p.add_argument("--media-manifest-json", default="")
    p.add_argument("--predeclared-anchor-file", default="")
    p.add_argument("--mred-familiarity-csv", default="", help="Optional MRED familiarity/novelty covariates CSV.")
    p.add_argument("--mred-scene-map-csv", default="", help="Optional MRED scene map CSV.")
    p.add_argument("--out-root", default="outputs")
    p.add_argument("--stimulus-style", default="delayed_reveal", choices=["delayed_reveal", "steady_load_with_climax", "sustained_early_peak", "dark_valence_threat_reveal", "sustained_steady", "weak_or_ambiguous", "custom"])
    p.add_argument("--channel-map-preset", default="PRAYCG16_FIXED_ORDER_v1")
    p.add_argument("--channel-map-confidence", default="LOCKED")
    p.add_argument("--n-surrogates", type=int, default=500)
    p.add_argument("--random-seed", type=int, default=20260724)
    p.add_argument("--enable-module", action="append", default=[])
    p.add_argument("--disable-module", action="append", default=[])
    p.add_argument("--overwrite", action="store_true")
    # Visual settings
    p.add_argument("--visual-video", default="", help="Branch MP4 for visual render.")
    p.add_argument("--visual-condition", default="target", choices=["control", "target", "override", "full", "auto"])
    p.add_argument("--visual-events", default="", help="Additional event CSV/JSON files for overlays.")
    p.add_argument("--visual-feature-csv", default="", help="Override feature CSV for visualizer. Defaults to analysis output KHT feature frame.")
    p.add_argument("--visual-out", default="")
    p.add_argument("--visual-fps", type=float, default=24.0)
    p.add_argument("--visual-width", type=int, default=1280)
    p.add_argument("--visual-video-height", type=int, default=540)
    p.add_argument("--visual-graph-height", type=int, default=620)
    p.add_argument("--visual-rolling-window", type=float, default=30.0)
    p.add_argument("--als-aux-channel", type=int, default=1)
    return p


def launch_gui() -> int:
    if not TK_AVAILABLE:
        raise RuntimeError("Tkinter not available. Use CLI mode.")
    parser = build_arg_parser()
    class App(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("PRAYCG Unified Master Suite v1.4.3")
            self.geometry("880x820")
            self.vars = {k: tk.StringVar(value=v) for k, v in {
                "mode": "analysis_only", "project_name": "PRAYCG_Run", "xdf": "", "event_log": "", "channel_map": "",
                "cue_schedule_json": "", "annotation_csv": "", "feature_table_path": "", "media_manifest_json": "",
                "predeclared_anchor_file": "", "mred_familiarity_csv": "", "mred_scene_map_csv": "", "out_root": str(Path.cwd() / "outputs"), "stimulus_style": "delayed_reveal",
                "visual_video": "", "visual_condition": "target", "visual_events": "", "visual_feature_csv": "", "visual_out": "",
            }.items()}
            self.build()
        def row_file(self, parent, label, key, folder=False, save=False, filetypes=None):
            fr = ttk.Frame(parent); fr.pack(fill="x", pady=3)
            ttk.Label(fr, text=label, width=24).pack(side="left")
            ttk.Entry(fr, textvariable=self.vars[key]).pack(side="left", fill="x", expand=True)
            def browse():
                if folder:
                    pth = filedialog.askdirectory(title=f"Select {label}")
                elif save:
                    pth = filedialog.asksaveasfilename(title=f"Select {label}", defaultextension=".mp4", filetypes=filetypes or [("MP4", "*.mp4"), ("All", "*.*")])
                else:
                    pth = filedialog.askopenfilename(title=f"Select {label}", filetypes=filetypes or [("All", "*.*")])
                if pth: self.vars[key].set(pth)
            ttk.Button(fr, text=("Browse Folder" if folder else "Browse"), command=browse).pack(side="left", padx=3)
        def build(self):
            nb = ttk.Notebook(self); nb.pack(fill="both", expand=True, padx=10, pady=10)
            run = ttk.Frame(nb, padding=10); nb.add(run, text="Run")
            ttk.Label(run, text="PRAYCG Unified Master Suite v1.4.3", font=("Arial", 16, "bold")).pack(anchor="w")
            fr = ttk.Frame(run); fr.pack(fill="x", pady=8)
            ttk.Label(fr, text="Mode", width=24).pack(side="left")
            ttk.Radiobutton(fr, text="Analysis only", value="analysis_only", variable=self.vars["mode"]).pack(side="left")
            ttk.Radiobutton(fr, text="Analysis + visual", value="analysis_plus_visual", variable=self.vars["mode"]).pack(side="left")
            for lab,key,folder in [("Project name","project_name",False),("XDF","xdf",False),("Event log JSON/CSV","event_log",False),("Channel map","channel_map",False),("Cue schedule JSON","cue_schedule_json",False),("Annotation / scene anchors CSV","annotation_csv",False),("Feature table CSV","feature_table_path",False),("Media manifest JSON","media_manifest_json",False),("Predeclared anchor JSON/CSV","predeclared_anchor_file",False),("MRED familiarity CSV","mred_familiarity_csv",False),("MRED scene map CSV","mred_scene_map_csv",False),("Output root","out_root",True)]:
                self.row_file(run, lab, key, folder=folder)
            vis = ttk.Frame(nb, padding=10); nb.add(vis, text="Visual")
            self.row_file(vis, "Branch video MP4", "visual_video", filetypes=[("MP4", "*.mp4"), ("All", "*.*")])
            self.row_file(vis, "Extra event overlays", "visual_events", filetypes=[("CSV/JSON", "*.csv *.json"), ("All", "*.*")])
            self.row_file(vis, "Feature CSV override", "visual_feature_csv", filetypes=[("CSV", "*.csv"), ("All", "*.*")])
            ttk.Label(vis, text="Feature CSV override can be left blank. In analysis+visual mode, v1.4.3 auto-detects human_translation_kht_feature_frame.csv or *_time_resolved_feature_frame.csv from the analysis folder.", wraplength=800).pack(anchor="w", pady=(0,6))
            self.row_file(vis, "Output MP4", "visual_out", save=True, filetypes=[("MP4", "*.mp4"), ("All", "*.*")])
            fr2 = ttk.Frame(vis); fr2.pack(fill="x", pady=6)
            ttk.Label(fr2, text="Condition", width=24).pack(side="left")
            for val, txt in [("control","Control"),("target","Target"),("override","Override"),("full","Full")]:
                ttk.Radiobutton(fr2, text=txt, value=val, variable=self.vars["visual_condition"]).pack(side="left")
            action = ttk.Frame(self, padding=10); action.pack(fill="x")
            ttk.Button(action, text="Run", command=self.run).pack(side="left")
            self.log = tk.Text(self, height=14); self.log.pack(fill="both", expand=True, padx=10, pady=(0,10))
        def ns(self):
            argv = ["--mode", self.vars["mode"].get(), "--project-name", self.vars["project_name"].get(), "--out-root", self.vars["out_root"].get()]
            mapping = {
                "xdf":"--xdf", "event_log":"--event-log", "channel_map":"--channel-map", "cue_schedule_json":"--cue-schedule-json",
                "annotation_csv":"--annotation-csv", "feature_table_path":"--feature-table-path", "media_manifest_json":"--media-manifest-json",
                "predeclared_anchor_file":"--predeclared-anchor-file", "mred_familiarity_csv":"--mred-familiarity-csv", "mred_scene_map_csv":"--mred-scene-map-csv", "visual_video":"--visual-video", "visual_condition":"--visual-condition",
                "visual_events":"--visual-events", "visual_feature_csv":"--visual-feature-csv", "visual_out":"--visual-out"
            }
            for key, flag in mapping.items():
                val = self.vars[key].get().strip()
                if val:
                    argv += [flag, val]
            argv += ["--enable-module", "candidate_local_kht", "--overwrite"]
            return parser.parse_args(argv)
        def run(self):
            try:
                self.log.insert("end", "Starting unified run...\n"); self.update_idletasks()
                res = run_pipeline(self.ns())
                self.log.insert("end", json.dumps(res, indent=2) + "\n")
                messagebox.showinfo("Done", "Unified run complete.")
            except Exception as exc:
                tb=traceback.format_exc(); self.log.insert("end", tb + "\n"); messagebox.showerror("Error", str(exc))
    app = App(); app.mainloop(); return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    if args.gui:
        return launch_gui()
    try:
        result = run_pipeline(args)
        print(json.dumps(result, indent=2))
        return 0
    except Exception as exc:
        print("ERROR:", exc, file=sys.stderr)
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
