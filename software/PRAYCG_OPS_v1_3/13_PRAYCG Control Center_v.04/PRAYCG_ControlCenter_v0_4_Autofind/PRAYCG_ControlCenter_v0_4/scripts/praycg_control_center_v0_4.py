#!/usr/bin/env python3
"""
PRAYCG Control Center v0.4

A public-facing orchestration GUI for PRAYCG tools.
It launches existing tools as separate processes, manages stimulus/run folders,
checks LSL streams, and provides acquisition helper panels.

This is intentionally an orchestrator, not a monolithic replacement for MediaPrep,
PsychoPy, LabRecorder, BrainFlow, or the Master Comprehensive Suite.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import shlex
import subprocess
import sys
import threading
import time
import traceback
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

APP_NAME = "PRAYCG Control Center"
APP_VERSION = "0.4.0"


def slugify(text: str, default: str = "item") -> str:
    text = str(text or "").strip().lower()
    text = re.sub(r"[^a-z0-9._-]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("._-")
    return text or default


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def open_path(path: Path) -> None:
    path = Path(path)
    if not path.exists():
        messagebox.showwarning("Path not found", f"Path does not exist:\n{path}")
        return
    if sys.platform.startswith("win"):
        os.startfile(str(path))  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
    else:
        subprocess.Popen(["xdg-open", str(path)])


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def user_config_dir() -> Path:
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or str(Path.home())
        return Path(base) / "PRAYCG_ControlCenter"
    return Path.home() / ".praycg_control_center"


def default_config() -> Dict[str, Any]:
    root = package_root()
    home = Path("C:/PRAYCG") if sys.platform.startswith("win") else Path.home() / "PRAYCG"
    py = sys.executable
    return {
        "schema": "PRAYCG_ControlCenter_Config_v0_4",
        "version": APP_VERSION,
        "praycg_home": str(home),
        "python_executable": py,
        "stimulus_root": str(home / "stimuli"),
        "run_root": str(home / "runs"),
        "analysis_root": str(home / "analysis"),
        "log_root": str(home / "logs"),
        "lsl": {
            "expected_streams": ["obci_eeg1", "OpenBCIStatusMarkers", "PolarHRV", "VernierRespirationBelt", "praycg_stasismarkers"],
            "eeg_stream_name": "obci_eeg1",
            "eeg_expected_rate_hz": 125.0,
            "als_channel_index_1based": -1
        },
        "tools": {
            "mediaprep_gui": "",
            "protocol_runner_praycg2": "",
            "psychopy_app": "",
            "psychopy_coder": "",
            "psychopy_python": "",
            "labrecorder": "",
            "master_suite_gui": "",
            "visualizer_gui": "",
            "offline_interpreter_gui": "",
            "brainflow_eeg_only": "",
            "brainflow_eeg_als": "",
            "polar_h10": str(root / "tools" / "acquisition" / "polar_to_lsl.py"),
            "vernier_resp": str(root / "tools" / "acquisition" / "vernier_respiration_belt_to_lsl.py"),
            "lsl_stream_checker": str(root / "scripts" / "praycg_lsl_stream_checker_v0_1.py"),
            "signal_quality_index": str(root / "scripts" / "praycg_signal_quality_index_v0_1.py"),
            "als_pulse_test": str(root / "scripts" / "praycg_als_screen_pulse_test_v0_1.py")
        },
        "runner_launch_mode": "open_psychopy_coder_then_open_runner_file",
        "stimulus_registry": str(home / "config" / "stimulus_registry.json"),
        "run_registry": str(home / "config" / "run_registry.json")
    }


def merge_defaults(cfg: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
    out = defaults.copy()
    for k, v in cfg.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            d = out[k].copy(); d.update(v); out[k] = d
        else:
            out[k] = v
    return out


@dataclass
class RunningProcess:
    label: str
    process: subprocess.Popen
    log_path: Path
    started: float
    cmd: List[str]


class ScrollText(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = tk.Text(self, wrap="word", height=12)
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        self.text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def write(self, msg: str) -> None:
        self.text.insert("end", msg)
        self.text.see("end")
        self.text.update_idletasks()

    def clear(self) -> None:
        self.text.delete("1.0", "end")


class PRAYCGControlCenter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1180x820")
        self.minsize(1000, 700)
        self.pkg = package_root()
        self.config_path = user_config_dir() / "config.json"
        self.cfg = self.load_config()
        self.processes: Dict[str, RunningProcess] = {}
        self.selected_stimulus_id: Optional[str] = None
        self.selected_run_folder: Optional[Path] = None
        self.create_dirs()
        self.build_ui()
        self.refresh_dashboard()
        self.after(1500, self.periodic_update)

    def load_config(self) -> Dict[str, Any]:
        defaults = default_config()
        if self.config_path.exists():
            try:
                cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
                return merge_defaults(cfg, defaults)
            except Exception:
                traceback.print_exc()
        user_config_dir().mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(defaults, indent=2), encoding="utf-8")
        return defaults

    def save_config(self) -> None:
        user_config_dir().mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(self.cfg, indent=2), encoding="utf-8")
        self.log(f"Saved config: {self.config_path}\n")

    def create_dirs(self) -> None:
        for key in ["praycg_home", "stimulus_root", "run_root", "analysis_root", "log_root"]:
            Path(self.cfg[key]).mkdir(parents=True, exist_ok=True)
        Path(self.cfg["stimulus_registry"]).parent.mkdir(parents=True, exist_ok=True)
        if not Path(self.cfg["stimulus_registry"]).exists():
            Path(self.cfg["stimulus_registry"]).write_text(json.dumps({"schema":"PRAYCG_StimulusRegistry_v0_1", "stimuli": []}, indent=2), encoding="utf-8")
        if not Path(self.cfg["run_registry"]).exists():
            Path(self.cfg["run_registry"]).write_text(json.dumps({"schema":"PRAYCG_RunRegistry_v0_1", "runs": []}, indent=2), encoding="utf-8")

    def build_ui(self) -> None:
        top = ttk.Frame(self)
        top.pack(side="top", fill="x", padx=8, pady=6)
        ttk.Label(top, text="PRAYCG Control Center", font=("Segoe UI", 18, "bold")).pack(side="left")
        ttk.Label(top, text="  Orchestrator / launcher / folder manager — not a replacement for PsychoPy or LabRecorder", foreground="#555").pack(side="left")
        ttk.Button(top, text="Open PRAYCG Home", command=lambda: open_path(Path(self.cfg["praycg_home"]))).pack(side="right", padx=4)
        ttk.Button(top, text="Save Settings", command=self.save_settings_from_ui).pack(side="right", padx=4)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=8, pady=4)
        self.dashboard_tab = ttk.Frame(self.nb); self.nb.add(self.dashboard_tab, text="Dashboard")
        self.stim_tab = ttk.Frame(self.nb); self.nb.add(self.stim_tab, text="Stimulus Library")
        self.acq_tab = ttk.Frame(self.nb); self.nb.add(self.acq_tab, text="Acquisition")
        self.runner_tab = ttk.Frame(self.nb); self.nb.add(self.runner_tab, text="Runner / PsychoPy")
        self.analysis_tab = ttk.Frame(self.nb); self.nb.add(self.analysis_tab, text="Analysis")
        self.settings_tab = ttk.Frame(self.nb); self.nb.add(self.settings_tab, text="Settings")

        self.build_dashboard_tab()
        self.build_stimulus_tab()
        self.build_acquisition_tab()
        self.build_runner_tab()
        self.build_analysis_tab()
        self.build_settings_tab()

        bottom = ttk.LabelFrame(self, text="Control Center Log")
        bottom.pack(fill="both", expand=False, padx=8, pady=4)
        self.logbox = ScrollText(bottom)
        self.logbox.pack(fill="both", expand=True)
        self.log(f"{APP_NAME} v{APP_VERSION} started. Config: {self.config_path}\n")

    def log(self, msg: str) -> None:
        if hasattr(self, "logbox"):
            self.logbox.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        else:
            print(msg, end="")

    def build_dashboard_tab(self) -> None:
        f = self.dashboard_tab
        left = ttk.Frame(f); left.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        right = ttk.Frame(f); right.pack(side="right", fill="both", expand=True, padx=8, pady=8)
        ttk.Label(left, text="Workflow", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        buttons = [
            ("1. Add / Validate Master Stimulus", lambda: self.nb.select(self.stim_tab)),
            ("2. Launch MediaPrep Suite", self.launch_mediaprep),
            ("3. Open Acquisition Panel", lambda: self.nb.select(self.acq_tab)),
            ("4. Open LabRecorder", self.launch_labrecorder),
            ("5. Open PsychoPy Runner", lambda: self.nb.select(self.runner_tab)),
            ("6. Run Master Comprehensive Suite", lambda: self.nb.select(self.analysis_tab)),
            ("7. Run Visualizer", self.launch_visualizer),
            ("8. Run Offline Interpreter", self.launch_offline_interpreter),
        ]
        for txt, cmd in buttons:
            ttk.Button(left, text=txt, command=cmd).pack(fill="x", pady=4)

        ttk.Label(right, text="Current Status", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        self.status_text = tk.Text(right, height=20, wrap="word")
        self.status_text.pack(fill="both", expand=True)
        ttk.Button(right, text="Refresh Status", command=self.refresh_dashboard).pack(fill="x", pady=4)

        procs = ttk.LabelFrame(f, text="Running Tools")
        procs.pack(side="bottom", fill="x", padx=8, pady=8)
        self.proc_tree = ttk.Treeview(procs, columns=("pid","status","runtime","log"), show="headings", height=5)
        for col, width in [("pid",80),("status",100),("runtime",100),("log",700)]:
            self.proc_tree.heading(col, text=col); self.proc_tree.column(col, width=width)
        self.proc_tree.pack(side="left", fill="x", expand=True)
        pbtns = ttk.Frame(procs); pbtns.pack(side="right", padx=4)
        ttk.Button(pbtns, text="Stop Selected", command=self.stop_selected_process).pack(fill="x", pady=2)
        ttk.Button(pbtns, text="Open Selected Log", command=self.open_selected_process_log).pack(fill="x", pady=2)

    def build_stimulus_tab(self) -> None:
        f = self.stim_tab
        top = ttk.Frame(f); top.pack(fill="x", padx=8, pady=8)
        ttk.Button(top, text="Add Master Stimulus (.mp4)", command=self.add_master_stimulus).pack(side="left", padx=4)
        ttk.Button(top, text="Refresh Stimulus Registry", command=self.refresh_stimulus_registry).pack(side="left", padx=4)
        ttk.Button(top, text="Open Stimulus Root", command=lambda: open_path(Path(self.cfg["stimulus_root"]))).pack(side="left", padx=4)
        ttk.Button(top, text="Launch MediaPrep", command=self.launch_mediaprep).pack(side="left", padx=4)

        mid = ttk.Panedwindow(f, orient="horizontal"); mid.pack(fill="both", expand=True, padx=8, pady=4)
        lframe = ttk.LabelFrame(mid, text="Stimuli")
        rframe = ttk.LabelFrame(mid, text="Detected Files for Selected Stimulus")
        mid.add(lframe, weight=1); mid.add(rframe, weight=2)
        self.stim_tree = ttk.Treeview(lframe, columns=("id","duration","created","path"), show="headings")
        for col, width in [("id",180),("duration",90),("created",150),("path",360)]:
            self.stim_tree.heading(col, text=col); self.stim_tree.column(col, width=width)
        self.stim_tree.pack(fill="both", expand=True)
        self.stim_tree.bind("<<TreeviewSelect>>", self.on_stim_select)
        self.stim_detail = tk.Text(rframe, wrap="word")
        self.stim_detail.pack(fill="both", expand=True)
        self.refresh_stimulus_registry()

    def build_acquisition_tab(self) -> None:
        f = self.acq_tab
        left = ttk.LabelFrame(f, text="Start / Stop Streams")
        left.pack(side="left", fill="y", padx=8, pady=8)
        ttk.Button(left, text="Start Polar H10 RR -> LSL", command=self.launch_polar).pack(fill="x", pady=3)
        ttk.Button(left, text="Start Vernier Respiration USB -> LSL", command=lambda: self.launch_vernier("usb")).pack(fill="x", pady=3)
        ttk.Button(left, text="Start Vernier Respiration BLE -> LSL", command=lambda: self.launch_vernier("ble")).pack(fill="x", pady=3)
        ttk.Separator(left).pack(fill="x", pady=6)
        ttk.Button(left, text="Start BrainFlow EEG Only", command=self.launch_brainflow_eeg_only).pack(fill="x", pady=3)
        ttk.Button(left, text="Start BrainFlow EEG + ALS", command=self.launch_brainflow_eeg_als).pack(fill="x", pady=3)
        ttk.Separator(left).pack(fill="x", pady=6)
        ttk.Button(left, text="Check Visible LSL Streams", command=self.check_lsl_streams).pack(fill="x", pady=3)
        ttk.Button(left, text="Signal Quality / Contact Index 0-100", command=self.run_signal_quality).pack(fill="x", pady=3)
        ttk.Button(left, text="ALS Screen Pulse Barcode Test", command=self.run_als_test).pack(fill="x", pady=3)
        ttk.Button(left, text="Open LabRecorder", command=self.launch_labrecorder).pack(fill="x", pady=3)

        right = ttk.LabelFrame(f, text="LSL Stream Monitor")
        right.pack(side="right", fill="both", expand=True, padx=8, pady=8)
        self.lsl_tree = ttk.Treeview(right, columns=("name","type","ch","srate","source"), show="headings", height=14)
        for col, width in [("name",220),("type",120),("ch",60),("srate",100),("source",400)]:
            self.lsl_tree.heading(col, text=col); self.lsl_tree.column(col, width=width)
        self.lsl_tree.pack(fill="both", expand=True)
        ttk.Button(right, text="Refresh LSL Stream List", command=self.populate_lsl_tree).pack(fill="x", pady=4)
        note = tk.Text(right, height=7, wrap="word")
        note.pack(fill="x")
        note.insert("end", "Notes:\n- Polar script streams RR intervals as LSL stream 'PolarHRV'.\n- Vernier script streams raw force as 'VernierRespirationBelt'. USB is recommended first.\n- Signal Quality Index is a contact-quality proxy, not true Cyton impedance.\n- ALS test uses a black/white barcode. The strongest future setup is a physical sensor mount over a runner-level screen pulse region.\n")
        note.config(state="disabled")

    def build_runner_tab(self) -> None:
        f = self.runner_tab
        top = ttk.LabelFrame(f, text="PsychoPy-safe Runner Launch")
        top.pack(fill="x", padx=8, pady=8)
        ttk.Label(top, text="Because the PRAYCG2.0 runner currently works most reliably when started from PsychoPy Coder, this tab defaults to opening PsychoPy Coder and the runner file/folder rather than forcing direct Python execution.", wraplength=1000).pack(anchor="w", pady=4)
        self.runner_mode_var = tk.StringVar(value=self.cfg.get("runner_launch_mode", "open_psychopy_coder_then_open_runner_file"))
        modes = [
            ("Open PsychoPy Coder + runner file/folder (recommended)", "open_psychopy_coder_then_open_runner_file"),
            ("Launch runner with PsychoPy application and file argument (experimental)", "psychopy_app_file_arg"),
            ("Launch runner with PsychoPy Python interpreter (experimental)", "psychopy_python"),
            ("Launch runner with regular Python (least recommended for your current setup)", "regular_python"),
        ]
        for text, val in modes:
            ttk.Radiobutton(top, text=text, value=val, variable=self.runner_mode_var).pack(anchor="w")
        ttk.Button(top, text="Launch PRAYCG2.0 Runner Using Selected Mode", command=self.launch_praycg_runner).pack(fill="x", pady=6)
        ttk.Button(top, text="Open Runner Script Location", command=self.open_runner_location).pack(fill="x", pady=2)
        ttk.Button(top, text="Open PsychoPy Coder Only", command=self.launch_psychopy_coder_only).pack(fill="x", pady=2)
        ttk.Button(top, text="Auto-find PsychoPy / LabRecorder / Runner", command=self.autofind_common_tools).pack(fill="x", pady=6)

        media = ttk.LabelFrame(f, text="Auto-detected PRAYCG2.0 Input Files for Selected Stimulus")
        media.pack(fill="both", expand=True, padx=8, pady=8)
        self.runner_detect_text = tk.Text(media, wrap="word")
        self.runner_detect_text.pack(fill="both", expand=True)
        ttk.Button(media, text="Refresh Detected Stimulus Files", command=self.refresh_runner_detect_text).pack(fill="x", pady=4)

    def build_analysis_tab(self) -> None:
        f = self.analysis_tab
        top = ttk.Frame(f); top.pack(fill="x", padx=8, pady=8)
        ttk.Button(top, text="Select Run Folder", command=self.select_run_folder).pack(side="left", padx=4)
        ttk.Button(top, text="Scan Run Folder", command=self.scan_selected_run_folder).pack(side="left", padx=4)
        ttk.Button(top, text="Launch Master Suite", command=self.launch_master_suite).pack(side="left", padx=4)
        ttk.Button(top, text="Launch Visualizer", command=self.launch_visualizer).pack(side="left", padx=4)
        ttk.Button(top, text="Launch Offline Interpreter", command=self.launch_offline_interpreter).pack(side="left", padx=4)
        ttk.Button(top, text="Open Analysis Root", command=lambda: open_path(Path(self.cfg["analysis_root"]))).pack(side="left", padx=4)
        self.analysis_text = tk.Text(f, wrap="word")
        self.analysis_text.pack(fill="both", expand=True, padx=8, pady=4)

    def build_settings_tab(self) -> None:
        f = self.settings_tab
        canvas = tk.Canvas(f)
        scroll = ttk.Scrollbar(f, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        self.setting_vars: Dict[str, tk.StringVar] = {}

        def add_path_row(label: str, key_path: Tuple[str, Optional[str]], folder=False):
            row = ttk.Frame(inner); row.pack(fill="x", padx=8, pady=3)
            ttk.Label(row, text=label, width=32).pack(side="left")
            key, subkey = key_path
            val = self.cfg.get(key, {}).get(subkey, "") if subkey else self.cfg.get(key, "")
            var = tk.StringVar(value=str(val))
            name = key if subkey is None else f"{key}.{subkey}"
            self.setting_vars[name] = var
            ttk.Entry(row, textvariable=var).pack(side="left", fill="x", expand=True, padx=4)
            def browse():
                if folder:
                    p = filedialog.askdirectory(title=f"Select {label}")
                else:
                    p = filedialog.askopenfilename(title=f"Select {label}")
                if p: var.set(p)
            ttk.Button(row, text="Browse", command=browse).pack(side="left")

        ttk.Label(inner, text="Core Folders", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=8, pady=6)
        add_path_row("PRAYCG Home", ("praycg_home", None), folder=True)
        add_path_row("Stimulus Root", ("stimulus_root", None), folder=True)
        add_path_row("Run Root", ("run_root", None), folder=True)
        add_path_row("Analysis Root", ("analysis_root", None), folder=True)
        add_path_row("Log Root", ("log_root", None), folder=True)
        ttk.Label(inner, text="Tool Paths", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=8, pady=8)
        auto_frame = ttk.LabelFrame(inner, text="Auto-find common external tools v0.4")
        auto_frame.pack(fill="x", padx=8, pady=6)
        ttk.Label(auto_frame, text="Searches common Windows locations, PRAYCG_HOME, Desktop, Downloads, Program Files, and PATH. Review results before launching.", wraplength=900).pack(anchor="w", padx=6, pady=4)
        btnrow = ttk.Frame(auto_frame); btnrow.pack(fill="x", padx=6, pady=4)
        ttk.Button(btnrow, text="Auto-find ALL", command=self.autofind_common_tools).pack(side="left", padx=3)
        ttk.Button(btnrow, text="Find LabRecorder", command=self.autofind_labrecorder).pack(side="left", padx=3)
        ttk.Button(btnrow, text="Find PsychoPy", command=self.autofind_psychopy).pack(side="left", padx=3)
        ttk.Button(btnrow, text="Find PRAYCG2.0 Runner", command=self.autofind_runner).pack(side="left", padx=3)
        tool_labels = [
            ("Python executable", ("python_executable", None)),
            ("MediaPrep GUI", ("tools", "mediaprep_gui")),
            ("PRAYCG2.0 Runner Script", ("tools", "protocol_runner_praycg2")),
            ("PsychoPy App", ("tools", "psychopy_app")),
            ("PsychoPy Coder", ("tools", "psychopy_coder")),
            ("PsychoPy Python", ("tools", "psychopy_python")),
            ("LabRecorder exe", ("tools", "labrecorder")),
            ("Master Suite GUI", ("tools", "master_suite_gui")),
            ("Visualizer GUI", ("tools", "visualizer_gui")),
            ("Offline Interpreter GUI", ("tools", "offline_interpreter_gui")),
            ("BrainFlow EEG Only", ("tools", "brainflow_eeg_only")),
            ("BrainFlow EEG + ALS", ("tools", "brainflow_eeg_als")),
            ("Polar H10 script", ("tools", "polar_h10")),
            ("Vernier Resp script", ("tools", "vernier_resp")),
        ]
        for label, kp in tool_labels:
            add_path_row(label, kp, folder=False)
        ttk.Button(inner, text="Save Settings", command=self.save_settings_from_ui).pack(fill="x", padx=8, pady=10)
        ttk.Button(inner, text="Open Config JSON", command=lambda: open_path(self.config_path)).pack(fill="x", padx=8, pady=4)

    # Settings and process handling
    def save_settings_from_ui(self) -> None:
        if not hasattr(self, "setting_vars"):
            return self.save_config()
        for name, var in self.setting_vars.items():
            if "." in name:
                key, sub = name.split(".", 1)
                self.cfg.setdefault(key, {})[sub] = var.get().strip()
            else:
                self.cfg[name] = var.get().strip()
        self.cfg["runner_launch_mode"] = self.runner_mode_var.get() if hasattr(self, "runner_mode_var") else self.cfg.get("runner_launch_mode")
        self.create_dirs()
        self.save_config()
        self.refresh_dashboard()
        self.refresh_stimulus_registry()

    def launch_process(self, label: str, cmd: List[str], cwd: Optional[Path] = None) -> None:
        cmd = [str(x) for x in cmd if str(x) != ""]
        if not cmd:
            messagebox.showerror("Cannot launch", "Empty command.")
            return
        log_dir = Path(self.cfg["log_root"]) / "control_center"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / f"{now_stamp()}_{slugify(label)}.log"
        self.log(f"Launching {label}: {' '.join(cmd)}\n  log: {log_path}\n")
        try:
            f = open(log_path, "w", encoding="utf-8", errors="replace")
            f.write(f"{label}\n{' '.join(cmd)}\nStarted {datetime.now().isoformat()}\n\n")
            f.flush()
            p = subprocess.Popen(cmd, cwd=str(cwd) if cwd else None, stdout=f, stderr=subprocess.STDOUT)
            self.processes[label] = RunningProcess(label=label, process=p, log_path=log_path, started=time.time(), cmd=cmd)
            self.update_process_tree()
        except Exception as exc:
            messagebox.showerror("Launch failed", f"Could not launch {label}:\n{exc}")
            self.log(f"FAILED {label}: {exc}\n")

    def launch_python_tool(self, label: str, script_key: str, args: Optional[List[str]]=None) -> None:
        script = Path(self.cfg["tools"].get(script_key, ""))
        if not script.exists():
            messagebox.showerror("Script not found", f"Set the path for {script_key} in Settings.\n\nCurrent path:\n{script}")
            return
        py = self.cfg.get("python_executable") or sys.executable
        py_cmd = shlex.split(str(py))
        self.launch_process(label, py_cmd + [str(script)] + (args or []), cwd=script.parent)

    def update_process_tree(self) -> None:
        if not hasattr(self, "proc_tree"): return
        self.proc_tree.delete(*self.proc_tree.get_children())
        dead = []
        for label, rp in self.processes.items():
            rc = rp.process.poll()
            status = "running" if rc is None else f"exited {rc}"
            runtime = time.strftime("%H:%M:%S", time.gmtime(time.time() - rp.started))
            self.proc_tree.insert("", "end", iid=label, values=(rp.process.pid, status, runtime, str(rp.log_path)))
            if rc is not None:
                dead.append(label)
        # keep exited rows visible; do not remove automatically

    def periodic_update(self) -> None:
        self.update_process_tree()
        self.after(1500, self.periodic_update)

    def stop_selected_process(self) -> None:
        sel = self.proc_tree.selection()
        if not sel: return
        label = sel[0]
        rp = self.processes.get(label)
        if not rp: return
        if rp.process.poll() is None:
            rp.process.terminate()
            self.log(f"Terminated {label}\n")
        self.update_process_tree()

    def open_selected_process_log(self) -> None:
        sel = self.proc_tree.selection()
        if not sel: return
        rp = self.processes.get(sel[0])
        if rp: open_path(rp.log_path)

    # Dashboard/status
    def refresh_dashboard(self) -> None:
        if not hasattr(self, "status_text"): return
        self.status_text.config(state="normal")
        self.status_text.delete("1.0", "end")
        lines = []
        lines.append(f"Version: {APP_VERSION}")
        lines.append(f"PRAYCG_HOME: {self.cfg['praycg_home']}")
        lines.append(f"Stimulus root: {self.cfg['stimulus_root']}")
        lines.append(f"Run root: {self.cfg['run_root']}")
        lines.append(f"Analysis root: {self.cfg['analysis_root']}")
        lines.append("")
        lines.append("Current recommended workflow:")
        lines.append("1. Add master stimulus and validate MP4.")
        lines.append("2. Launch MediaPrep v1.8 and generate Target / Override / Control / cue schedule / QC.")
        lines.append("3. Frame-lock anchors and load LOCKED JSON in PRAYCG2.0.")
        lines.append("4. Start Polar / Vernier / BrainFlow streams.")
        lines.append("5. Open LabRecorder and verify streams.")
        lines.append("6. Launch PRAYCG2.0 from PsychoPy Coder if direct launch fails.")
        lines.append("7. Run Master Suite, Visualizer, and Offline Interpreter.")
        lines.append("")
        lines.append("Important boundary: this Control Center launches and organizes tools; it does not certify endpoints.")
        self.status_text.insert("end", "\n".join(lines))
        self.status_text.config(state="disabled")

    # Stimulus library
    def read_registry(self) -> Dict[str, Any]:
        p = Path(self.cfg["stimulus_registry"])
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {"schema":"PRAYCG_StimulusRegistry_v0_1", "stimuli": []}

    def write_registry(self, reg: Dict[str, Any]) -> None:
        Path(self.cfg["stimulus_registry"]).write_text(json.dumps(reg, indent=2), encoding="utf-8")

    def refresh_stimulus_registry(self) -> None:
        if not hasattr(self, "stim_tree"): return
        self.stim_tree.delete(*self.stim_tree.get_children())
        reg = self.read_registry()
        for s in reg.get("stimuli", []):
            self.stim_tree.insert("", "end", iid=s.get("stimulus_id"), values=(s.get("stimulus_id"), s.get("duration_sec", ""), s.get("created_local", ""), s.get("folder", "")))

    def add_master_stimulus(self) -> None:
        path_str = filedialog.askopenfilename(title="Select master stimulus MP4", filetypes=[("MP4", "*.mp4"), ("All files", "*.*")])
        if not path_str: return
        src = Path(path_str)
        stim_id = simpledialog.askstring("Stimulus ID", "Enter a short stimulus ID (letters/numbers/underscore):", initialvalue=slugify(src.stem))
        if not stim_id: return
        stim_id = slugify(stim_id)
        stim_dir = Path(self.cfg["stimulus_root"]) / stim_id
        master_dir = stim_dir / "master"
        master_dir.mkdir(parents=True, exist_ok=True)
        dst = master_dir / "stimulus_master.mp4"
        if dst.exists() and not messagebox.askyesno("Overwrite?", f"{dst} already exists. Overwrite?"):
            return
        self.log(f"Copying master stimulus to {dst}\n")
        shutil.copy2(src, dst)
        report = self.validate_mp4(dst)
        report["original_source_path"] = str(src)
        report["stimulus_id"] = stim_id
        report["copied_to"] = str(dst)
        report["created_local"] = datetime.now().isoformat(timespec="seconds")
        report["sha256"] = sha256_file(dst)
        (master_dir / "master_sha256.txt").write_text(report["sha256"] + "\n", encoding="utf-8")
        (master_dir / "master_media_validation_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        reg = self.read_registry()
        reg["stimuli"] = [s for s in reg.get("stimuli", []) if s.get("stimulus_id") != stim_id]
        reg["stimuli"].append({
            "stimulus_id": stim_id,
            "folder": str(stim_dir),
            "master_mp4": str(dst),
            "duration_sec": report.get("duration_sec"),
            "created_local": report["created_local"],
            "sha256": report["sha256"],
            "validation_status": report.get("status", "UNKNOWN"),
        })
        self.write_registry(reg)
        self.refresh_stimulus_registry()
        self.selected_stimulus_id = stim_id
        self.display_stimulus_detail(stim_id)
        messagebox.showinfo("Stimulus added", f"Added {stim_id}\n\nValidation status: {report.get('status')}")

    def validate_mp4(self, path: Path) -> Dict[str, Any]:
        rep: Dict[str, Any] = {"schema":"PRAYCG_MasterStimulus_Validation_v0_1", "file": str(path), "status":"PILOT_UNVALIDATED"}
        rep["size_bytes"] = path.stat().st_size
        rep["extension_ok"] = path.suffix.lower() == ".mp4"
        warnings = []
        # Try ffprobe first
        ffprobe = shutil.which("ffprobe")
        if ffprobe:
            try:
                cmd = [ffprobe, "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(path)]
                out = subprocess.check_output(cmd, text=True, errors="replace")
                info = json.loads(out)
                rep["ffprobe"] = info
                fmt = info.get("format", {})
                rep["duration_sec"] = float(fmt.get("duration")) if fmt.get("duration") else None
                video_streams = [s for s in info.get("streams", []) if s.get("codec_type") == "video"]
                audio_streams = [s for s in info.get("streams", []) if s.get("codec_type") == "audio"]
                rep["has_video"] = bool(video_streams); rep["has_audio"] = bool(audio_streams)
                if video_streams:
                    vs = video_streams[0]
                    rep["width"] = vs.get("width"); rep["height"] = vs.get("height")
                    rep["avg_frame_rate"] = vs.get("avg_frame_rate")
                if not audio_streams: warnings.append("No audio stream detected.")
            except Exception as exc:
                rep["ffprobe_error"] = str(exc)
        else:
            warnings.append("ffprobe not found; validation limited. Install FFmpeg for stronger checks.")
        # Try OpenCV if useful
        try:
            import cv2  # type: ignore
            cap = cv2.VideoCapture(str(path))
            if cap.isOpened():
                fps = cap.get(cv2.CAP_PROP_FPS)
                frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                w = cap.get(cv2.CAP_PROP_FRAME_WIDTH); h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                rep.setdefault("fps", fps); rep.setdefault("frame_count", frames)
                rep.setdefault("width", w); rep.setdefault("height", h)
                if not rep.get("duration_sec") and fps and frames:
                    rep["duration_sec"] = float(frames / fps)
                cap.release()
            else:
                warnings.append("OpenCV could not open MP4.")
        except Exception as exc:
            rep["opencv_error"] = str(exc)
        dur = rep.get("duration_sec")
        if dur is not None:
            if dur < 120: warnings.append("Duration < 2 min; acceptable for tests, weak for standard PRAYCG.")
            if dur > 360: warnings.append("Duration > 6 min; may be long for standard PRAYCG.")
        rep["warnings"] = warnings
        rep["status"] = "PASS_WITH_WARNINGS" if warnings else "PASS_BASIC_VALIDATION"
        return rep

    def on_stim_select(self, event=None) -> None:
        sel = self.stim_tree.selection()
        if not sel: return
        stim_id = sel[0]
        self.selected_stimulus_id = stim_id
        self.display_stimulus_detail(stim_id)

    def selected_stimulus_folder(self) -> Optional[Path]:
        if not self.selected_stimulus_id:
            return None
        return Path(self.cfg["stimulus_root"]) / self.selected_stimulus_id

    def display_stimulus_detail(self, stim_id: str) -> None:
        if not hasattr(self, "stim_detail"): return
        folder = Path(self.cfg["stimulus_root"]) / stim_id
        detections = self.detect_stimulus_files(folder)
        self.stim_detail.delete("1.0", "end")
        self.stim_detail.insert("end", json.dumps(detections, indent=2))
        self.refresh_runner_detect_text()

    def detect_stimulus_files(self, folder: Path) -> Dict[str, Any]:
        patterns = {
            "master_mp4": ["master/stimulus_master.mp4", "**/stimulus_master.mp4"],
            "target_video": ["**/stimulus_target_cued*.mp4"],
            "override_video": ["**/stimulus_override_cued*.mp4"],
            "control_video": ["**/stimulus_control*cued*phase*scrambled*.mp4", "**/stimulus_control*.mp4"],
            "cue_schedule_json": ["**/cue_schedule*.json"],
            "cue_schedule_csv": ["**/cue_schedule*.csv"],
            "locked_anchor_json": ["**/*LOCKED*.json"],
            "draft_anchor_json": ["**/*DRAFT*.json", "**/*ESTIMATED*.json"],
            "stimulus_fingerprint_all": ["**/stimulus_exogenous_regressor_frame_all_conditions.csv"],
            "cet_regressors_all": ["**/cet_regressors_all_conditions.csv"],
            "mediaprep_manifest": ["**/*manifest*.json", "**/*MediaPrep*report*.json"],
        }
        out = {"folder": str(folder), "exists": folder.exists(), "files": {}}
        for key, pats in patterns.items():
            matches: List[str] = []
            for pat in pats:
                matches += [str(p) for p in folder.glob(pat) if p.is_file()]
            # de-duplicate, shortest newest-ish: preserve sorted
            matches = sorted(set(matches), key=lambda x: (len(x), x))
            out["files"][key] = matches[:10]
        # convenience recommended files
        rec = {}
        for key in ["target_video", "override_video", "control_video", "cue_schedule_json", "locked_anchor_json", "draft_anchor_json", "stimulus_fingerprint_all"]:
            vals = out["files"].get(key, [])
            rec[key] = vals[-1] if vals else None
        out["recommended"] = rec
        status = []
        for key in ["target_video","override_video","control_video","cue_schedule_json"]:
            status.append(f"{key}: {'FOUND' if rec.get(key) else 'MISSING'}")
        status.append(f"anchor: {'LOCKED' if rec.get('locked_anchor_json') else 'DRAFT/ESTIMATED' if rec.get('draft_anchor_json') else 'MISSING'}")
        status.append(f"stimulus_fingerprint: {'FOUND' if rec.get('stimulus_fingerprint_all') else 'MISSING'}")
        out["status_lines"] = status
        return out

    def refresh_runner_detect_text(self) -> None:
        if not hasattr(self, "runner_detect_text"): return
        self.runner_detect_text.delete("1.0", "end")
        folder = self.selected_stimulus_folder()
        if not folder:
            self.runner_detect_text.insert("end", "No stimulus selected. Select one in Stimulus Library.\n")
            return
        det = self.detect_stimulus_files(folder)
        self.runner_detect_text.insert("end", "\n".join(det["status_lines"]) + "\n\n")
        self.runner_detect_text.insert("end", json.dumps(det["recommended"], indent=2))
        self.runner_detect_text.insert("end", "\n\nRecommended: PRAYCG2.0 should load Control, Target, Override, cue schedule JSON, and preferably a frame-verified LOCKED anchor JSON.\n")

    # Launchers
    def launch_mediaprep(self) -> None:
        path = self.cfg["tools"].get("mediaprep_gui", "")
        if not path:
            messagebox.showwarning("Path missing", "Set MediaPrep GUI path in Settings.")
            return
        self.launch_python_or_exe("MediaPrep Suite", path)

    def launch_master_suite(self) -> None:
        path = self.cfg["tools"].get("master_suite_gui", "")
        if not path:
            messagebox.showwarning("Path missing", "Set Master Suite GUI path in Settings.")
            return
        self.launch_python_or_exe("Master Comprehensive Suite", path)

    def launch_visualizer(self) -> None:
        path = self.cfg["tools"].get("visualizer_gui", "")
        if not path:
            messagebox.showwarning("Path missing", "Set Visualizer GUI/script path in Settings.")
            return
        self.launch_python_or_exe("Master Sync Visualizer", path)

    def launch_offline_interpreter(self) -> None:
        path = self.cfg["tools"].get("offline_interpreter_gui", "")
        if not path:
            messagebox.showwarning("Path missing", "Set Offline Interpreter GUI path in Settings.")
            return
        self.launch_python_or_exe("Offline Interpreter", path)

    def launch_python_or_exe(self, label: str, path: str, args: Optional[List[str]]=None) -> None:
        p = Path(path)
        if not p.exists():
            messagebox.showerror("Path not found", f"Path not found for {label}:\n{p}")
            return
        if p.suffix.lower() == ".py":
            py = self.cfg.get("python_executable") or sys.executable
            py_cmd = shlex.split(str(py))
            self.launch_process(label, py_cmd + [str(p)] + (args or []), cwd=p.parent)
        else:
            self.launch_process(label, [str(p)] + (args or []), cwd=p.parent)

    def launch_polar(self) -> None:
        self.launch_python_tool("Polar H10 RR -> LSL", "polar_h10")

    def launch_vernier(self, connection: str) -> None:
        self.launch_python_tool(f"Vernier Respiration {connection.upper()} -> LSL", "vernier_resp", ["--connection", connection])

    def launch_brainflow_eeg_only(self) -> None:
        path = self.cfg["tools"].get("brainflow_eeg_only", "")
        if not path:
            messagebox.showwarning("Path missing", "Set BrainFlow EEG-only script path in Settings.")
            return
        self.launch_python_or_exe("BrainFlow EEG Only", path)

    def launch_brainflow_eeg_als(self) -> None:
        path = self.cfg["tools"].get("brainflow_eeg_als", "")
        if not path:
            messagebox.showwarning("Path missing", "Set BrainFlow EEG+ALS script path in Settings.")
            return
        self.launch_python_or_exe("BrainFlow EEG + ALS", path)

    def launch_labrecorder(self) -> None:
        path = self.cfg["tools"].get("labrecorder", "")
        if not path:
            messagebox.showwarning("Path missing", "Set LabRecorder executable path in Settings.")
            return
        self.launch_python_or_exe("LabRecorder", path)

    def check_lsl_streams(self) -> None:
        args = ["--duration", "5", "--out-dir", str(Path(self.cfg["log_root"]) / "lsl_stream_checks")]
        expected = self.cfg.get("lsl", {}).get("expected_streams", [])
        if expected:
            args += ["--required"] + expected
        self.launch_python_tool("LSL Stream Checker", "lsl_stream_checker", args)
        self.after(1000, self.populate_lsl_tree)

    def run_signal_quality(self) -> None:
        lsl = self.cfg.get("lsl", {})
        args = [
            "--stream-name", lsl.get("eeg_stream_name", "obci_eeg1"),
            "--duration", "20",
            "--expected-rate", str(lsl.get("eeg_expected_rate_hz", 125.0)),
            "--out-dir", str(Path(self.cfg["log_root"]) / "signal_quality")
        ]
        self.launch_python_tool("Signal Quality / Contact Index", "signal_quality_index", args)

    def run_als_test(self) -> None:
        lsl = self.cfg.get("lsl", {})
        args = [
            "--stream-name", lsl.get("eeg_stream_name", "obci_eeg1"),
            "--channel-index", str(lsl.get("als_channel_index_1based", -1)),
            "--out-dir", str(Path(self.cfg["log_root"]) / "als_pulse_tests"),
            "--fullscreen",
            "--pulse-position", "fullscreen"
        ]
        self.launch_python_tool("ALS Screen Pulse Barcode Test", "als_pulse_test", args)

    def populate_lsl_tree(self) -> None:
        if not hasattr(self, "lsl_tree"): return
        self.lsl_tree.delete(*self.lsl_tree.get_children())
        try:
            from pylsl import resolve_streams
            streams = resolve_streams(wait_time=1.0)
            for idx, s in enumerate(streams):
                self.lsl_tree.insert("", "end", iid=str(idx), values=(s.name(), s.type(), s.channel_count(), s.nominal_srate(), s.source_id()))
            self.log(f"LSL monitor found {len(streams)} stream(s).\n")
        except Exception as exc:
            self.log(f"LSL monitor unavailable/error: {exc}\n")
            messagebox.showwarning("LSL monitor", f"Could not resolve LSL streams. Install pylsl or check network.\n\n{exc}")

    # Runner launch modes
    def launch_praycg_runner(self) -> None:
        mode = self.runner_mode_var.get()
        self.cfg["runner_launch_mode"] = mode
        runner = self.cfg["tools"].get("protocol_runner_praycg2", "")
        if not runner:
            messagebox.showwarning("Runner path missing", "Set PRAYCG2.0 runner script path in Settings.")
            return
        rp = Path(runner)
        if mode == "open_psychopy_coder_then_open_runner_file":
            self.launch_psychopy_coder_only(show_warning=False)
            try:
                open_path(rp.parent if rp.parent.exists() else rp)
            except Exception:
                pass
            self.log("Opened PsychoPy Coder mode. In Coder, open/run the PRAYCG2.0 runner script if it did not auto-open.\n")
            messagebox.showinfo("PsychoPy-safe runner workflow", f"PsychoPy Coder should open.\n\nRunner file/folder:\n{rp}\n\nThis is the recommended mode because your runner has worked reliably from PsychoPy Coder.")
        elif mode == "psychopy_app_file_arg":
            app = self.cfg["tools"].get("psychopy_app", "")
            if not app:
                messagebox.showwarning("PsychoPy app missing", "Set PsychoPy app path in Settings.")
                return
            self.launch_process("PRAYCG2.0 Runner via PsychoPy app", [app, str(rp)], cwd=rp.parent)
        elif mode == "psychopy_python":
            py = self.cfg["tools"].get("psychopy_python", "")
            if not py:
                messagebox.showwarning("PsychoPy Python missing", "Set PsychoPy Python interpreter path in Settings.")
                return
            self.launch_process("PRAYCG2.0 Runner via PsychoPy Python", [py, str(rp)], cwd=rp.parent)
        else:
            py = self.cfg.get("python_executable") or sys.executable
            py_cmd = shlex.split(str(py))
            self.launch_process("PRAYCG2.0 Runner via regular Python", py_cmd + [str(rp)], cwd=rp.parent)

    def launch_psychopy_coder_only(self, show_warning=True) -> None:
        coder = self.cfg["tools"].get("psychopy_coder", "") or self.cfg["tools"].get("psychopy_app", "")
        if not coder:
            if show_warning:
                messagebox.showwarning("PsychoPy path missing", "Set PsychoPy Coder or PsychoPy app path in Settings.")
            return
        self.launch_python_or_exe("PsychoPy Coder", coder)

    def open_runner_location(self) -> None:
        runner = self.cfg["tools"].get("protocol_runner_praycg2", "")
        if not runner:
            messagebox.showwarning("Runner path missing", "Set PRAYCG2.0 runner path in Settings.")
            return
        p = Path(runner)
        open_path(p.parent if p.parent.exists() else p)



    # Auto-find helpers v0.4
    def _autofind_roots(self) -> List[Path]:
        roots: List[Path] = []
        def add(x):
            if not x: return
            try:
                p = Path(x).expanduser()
                if p.exists() and p.is_dir() and p not in roots:
                    roots.append(p)
            except Exception:
                pass
        add(self.cfg.get("praycg_home"))
        add(self.cfg.get("stimulus_root"))
        add(self.cfg.get("run_root"))
        add(self.pkg)
        add(Path.home() / "Desktop")
        add(Path.home() / "Downloads")
        add(Path.home() / "Documents")
        for env in ["PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA", "APPDATA"]:
            add(os.environ.get(env))
        for x in ["C:/PRAYCG", "C:/Program Files/PsychoPy", "C:/Program Files/LabRecorder", "C:/LabRecorder", "C:/PsychoPy"]:
            add(x)
        return roots

    def _bounded_find(self, patterns: List[str], roots: Optional[List[Path]]=None, max_depth: int=7, max_hits: int=40, time_budget_sec: float=9.0) -> List[Path]:
        """Fast bounded recursive finder for public Windows users. Avoids full C:\ sweeps."""
        start = time.time()
        roots = roots or self._autofind_roots()
        hits: List[Path] = []
        seen = set()
        lower_patterns = [p.lower() for p in patterns]
        for root in roots:
            if time.time() - start > time_budget_sec or len(hits) >= max_hits:
                break
            try:
                root = root.resolve()
            except Exception:
                continue
            if not root.exists():
                continue
            stack = [(root, 0)]
            while stack and time.time() - start <= time_budget_sec and len(hits) < max_hits:
                cur, depth = stack.pop()
                try:
                    entries = list(cur.iterdir())
                except Exception:
                    continue
                for e in entries:
                    if len(hits) >= max_hits or time.time() - start > time_budget_sec:
                        break
                    name = e.name.lower()
                    if e.is_file():
                        for pat in lower_patterns:
                            if self._wild_match(name, pat) or self._wild_match(str(e).lower(), pat):
                                try:
                                    r = e.resolve()
                                except Exception:
                                    r = e
                                if str(r).lower() not in seen:
                                    hits.append(r); seen.add(str(r).lower())
                                break
                    elif e.is_dir() and depth < max_depth:
                        # Skip noisy folders.
                        if name in {".git", "__pycache__", "node_modules", "windows", "winsxs", "appdata"} and depth > 0:
                            continue
                        stack.append((e, depth + 1))
        return hits

    def _wild_match(self, text: str, pattern: str) -> bool:
        # small wildcard matcher for names/paths; pattern is lowercase.
        if "*" not in pattern:
            return pattern in text
        rx = re.escape(pattern).replace(r"\*", ".*")
        return re.search(rx, text) is not None

    def _score_candidate(self, path: Path, kind: str) -> int:
        txt = str(path).lower()
        score = 0
        if kind == "runner":
            for token, pts in [("praycg2_0", 50), ("2_0", 30), ("consolidated", 30), ("selfreport", 25), ("runner", 10), ("scripts", 5), ("current", 10)]:
                if token in txt: score += pts
            if path.name == "run_PRAYCG2_0_ConsolidatedSelfReport.py": score += 80
        elif kind == "labrecorder":
            if path.name.lower() == "labrecorder.exe": score += 80
            if "program files" in txt: score += 10
        elif kind == "psychopy":
            if path.name.lower() in {"psychopy.exe", "psychopyapp.exe"}: score += 80
            if "program files" in txt: score += 10
        elif kind == "psychopy_python":
            if path.name.lower() in {"python.exe", "pythonw.exe"}: score += 30
            if "psychopy" in txt: score += 50
        # prefer shorter paths after scoring.
        score -= min(len(txt) // 80, 5)
        return score

    def _choose_best(self, candidates: List[Path], kind: str) -> Optional[Path]:
        if not candidates:
            return None
        return sorted(candidates, key=lambda p: (self._score_candidate(p, kind), -len(str(p))), reverse=True)[0]

    def _set_tool_path(self, key: str, path: Optional[Path]) -> None:
        if not path:
            return
        self.cfg.setdefault("tools", {})[key] = str(path)
        if hasattr(self, "setting_vars"):
            var = self.setting_vars.get(f"tools.{key}")
            if var is not None:
                var.set(str(path))

    def _set_core_path(self, key: str, path: Optional[Path]) -> None:
        if not path:
            return
        self.cfg[key] = str(path)
        if hasattr(self, "setting_vars"):
            var = self.setting_vars.get(key)
            if var is not None:
                var.set(str(path))

    def autofind_labrecorder(self, save: bool=True) -> Dict[str, Any]:
        report: Dict[str, Any] = {"tool": "labrecorder", "found": False, "candidates": []}
        which = shutil.which("LabRecorder") or shutil.which("LabRecorder.exe")
        cands = [Path(which)] if which else []
        cands += self._bounded_find(["labrecorder.exe", "*LabRecorder*.exe"], max_depth=6, time_budget_sec=7.0)
        best = self._choose_best(cands, "labrecorder")
        report["candidates"] = [str(p) for p in cands[:20]]
        if best:
            report.update({"found": True, "selected": str(best)})
            self._set_tool_path("labrecorder", best)
            self.log(f"Auto-find LabRecorder: {best}\n")
        else:
            self.log("Auto-find LabRecorder: not found. Set manually in Settings.\n")
        if save: self.save_config()
        return report

    def autofind_psychopy(self, save: bool=True) -> Dict[str, Any]:
        report: Dict[str, Any] = {"tool": "psychopy", "found": False, "candidates": []}
        cands: List[Path] = []
        for name in ["psychopy", "psychopy.exe"]:
            w = shutil.which(name)
            if w: cands.append(Path(w))
        cands += self._bounded_find(["psychopy.exe", "*PsychoPy*.exe"], max_depth=7, time_budget_sec=9.0)
        best = self._choose_best(cands, "psychopy")
        report["candidates"] = [str(p) for p in cands[:20]]
        if best:
            report.update({"found": True, "selected_app": str(best), "selected_coder": str(best)})
            self._set_tool_path("psychopy_app", best)
            self._set_tool_path("psychopy_coder", best)
            # Look for PsychoPy-bundled Python near the app.
            py_cands = []
            for parent in [best.parent, best.parent.parent if best.parent.parent else best.parent]:
                for nm in ["python.exe", "pythonw.exe"]:
                    p = parent / nm
                    if p.exists(): py_cands.append(p)
                for sub in ["python", "Python", "resources", "Scripts"]:
                    d = parent / sub
                    if d.exists():
                        py_cands += [p for p in d.rglob("python*.exe") if p.is_file()][:10]
            py_best = self._choose_best(py_cands, "psychopy_python")
            if py_best:
                self._set_tool_path("psychopy_python", py_best)
                report["selected_python"] = str(py_best)
            self.log(f"Auto-find PsychoPy: {best}\n")
        else:
            self.log("Auto-find PsychoPy: not found. Set manually in Settings.\n")
        if save: self.save_config()
        return report

    def autofind_runner(self, save: bool=True) -> Dict[str, Any]:
        report: Dict[str, Any] = {"tool": "praycg_runner", "found": False, "candidates": []}
        # Favor PRAYCG home/current-tools locations and the user Desktop.
        roots = self._autofind_roots()
        cands = self._bounded_find([
            "run_praycg2_0_consolidatedselfreport.py",
            "*praycg2*consolidated*selfreport*.py",
            "*praycg*2_0*runner*.py",
            "*run*praycg*2*.py"
        ], roots=roots, max_depth=10, max_hits=80, time_budget_sec=12.0)
        best = self._choose_best(cands, "runner")
        report["candidates"] = [str(p) for p in cands[:30]]
        if best:
            report.update({"found": True, "selected": str(best)})
            self._set_tool_path("protocol_runner_praycg2", best)
            self.log(f"Auto-find PRAYCG2.0 runner: {best}\n")
        else:
            self.log("Auto-find PRAYCG2.0 runner: not found. Set manually in Settings.\n")
        if save: self.save_config()
        return report

    def autofind_common_tools(self) -> None:
        report = {
            "schema": "PRAYCG_ControlCenter_AutoFind_Report_v0_4",
            "created_local": datetime.now().isoformat(timespec="seconds"),
            "labrecorder": self.autofind_labrecorder(save=False),
            "psychopy": self.autofind_psychopy(save=False),
            "runner": self.autofind_runner(save=False),
        }
        # Save after all updates so the Settings GUI gets all values.
        self.save_config()
        out_dir = Path(self.cfg["log_root"]) / "control_center" / "autofind"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"autofind_report_{now_stamp()}.json"
        out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        self.log(f"Auto-find report written: {out_path}\n")
        if hasattr(self, "runner_detect_text"):
            self.refresh_runner_detect_text()
        messagebox.showinfo("Auto-find complete", "Auto-find finished. Review Settings paths before launching tools.\n\nReport:\n" + str(out_path))

    # Analysis tab
    def select_run_folder(self) -> None:
        d = filedialog.askdirectory(title="Select PRAYCG run folder")
        if d:
            self.selected_run_folder = Path(d)
            self.scan_selected_run_folder()

    def scan_selected_run_folder(self) -> None:
        self.analysis_text.delete("1.0", "end")
        folder = self.selected_run_folder
        if not folder:
            self.analysis_text.insert("end", "No run folder selected.\n")
            return
        patterns = {
            "xdf": "**/*.xdf",
            "events_json": "**/*events.json",
            "events_csv": "**/*events.csv",
            "run_config_media_selection": "**/*run_config_media_selection.json",
            "channel_map": "**/*channel_map*.csv",
            "core_reports": "**/*core_report.json",
            "confound_reports": "**/*confound_report.json",
            "override_task_reports": "**/*override_task_report.json",
            "final_master_report": "**/*final_master_report.json",
            "predeclared_anchors_csv": "**/*predeclared_anchors*.csv",
        }
        out = {k: [str(p) for p in folder.glob(pat) if p.is_file()] for k, pat in patterns.items()}
        self.analysis_text.insert("end", json.dumps(out, indent=2))


def main() -> int:
    app = PRAYCGControlCenter()
    app.mainloop()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
