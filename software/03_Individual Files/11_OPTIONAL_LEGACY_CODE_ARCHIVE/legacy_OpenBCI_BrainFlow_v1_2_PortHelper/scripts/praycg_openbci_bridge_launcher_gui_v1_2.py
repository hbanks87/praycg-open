#!/usr/bin/env python3
"""
PRAYCG OpenBCI BrainFlow Bridge Launcher GUI v1.2

Small Windows-friendly launcher for:
    OpenBCI Cyton/Daisy -> BrainFlow -> LSL obci_eeg1

It lists serial ports, lets you pick one, and starts the bridge in a separate Python process.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from serial.tools import list_ports
except Exception:
    list_ports = None

SCRIPT_DIR = Path(__file__).resolve().parent
BRIDGE = SCRIPT_DIR / "praycg_openbci_brainflow_to_lsl_v1_2.py"
WATCHDOG = SCRIPT_DIR / "praycg_lsl_eeg_watchdog_v1_2.py"


def get_ports():
    if list_ports is None:
        return []
    rows = []
    for p in list_ports.comports():
        text = " ".join(str(x or "") for x in [p.device, p.description, p.manufacturer, p.hwid])
        rows.append((str(p.device or ""), text))
    return rows


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PRAYCG OpenBCI BrainFlow → LSL Bridge v1.2")
        self.geometry("760x420")
        self.proc = None
        pad = {"padx": 8, "pady": 5}
        root = ttk.Frame(self); root.pack(fill="both", expand=True)
        cfg = ttk.LabelFrame(root, text="Bridge settings"); cfg.pack(fill="x", **pad)
        self.port_var = tk.StringVar()
        self.board_var = tk.StringVar(value="cyton-daisy")
        self.stream_var = tk.StringVar(value="obci_eeg1")
        self.timestamp_var = tk.StringVar(value="reconstructed")
        ttk.Label(cfg, text="COM port").grid(row=0, column=0, sticky="w", **pad)
        self.port_combo = ttk.Combobox(cfg, textvariable=self.port_var, width=36)
        self.port_combo.grid(row=0, column=1, sticky="ew", **pad)
        ttk.Button(cfg, text="Refresh ports", command=self.refresh_ports).grid(row=0, column=2, sticky="w", **pad)
        ttk.Label(cfg, text="Board").grid(row=1, column=0, sticky="w", **pad)
        ttk.Combobox(cfg, textvariable=self.board_var, values=["cyton-daisy", "cyton", "synthetic"], width=18, state="readonly").grid(row=1, column=1, sticky="w", **pad)
        ttk.Label(cfg, text="LSL stream").grid(row=2, column=0, sticky="w", **pad)
        ttk.Entry(cfg, textvariable=self.stream_var, width=22).grid(row=2, column=1, sticky="w", **pad)
        ttk.Label(cfg, text="Timestamp mode").grid(row=3, column=0, sticky="w", **pad)
        ttk.Combobox(cfg, textvariable=self.timestamp_var, values=["reconstructed", "lsl_chunk"], width=18, state="readonly").grid(row=3, column=1, sticky="w", **pad)
        cfg.columnconfigure(1, weight=1)
        btn = ttk.Frame(root); btn.pack(fill="x", **pad)
        ttk.Button(btn, text="Start Bridge", command=self.start_bridge).pack(side="left", padx=5)
        ttk.Button(btn, text="Start 120s Watchdog", command=self.start_watchdog).pack(side="left", padx=5)
        ttk.Button(btn, text="Stop Bridge", command=self.stop_bridge).pack(side="left", padx=5)
        ttk.Button(btn, text="Copy Command", command=self.copy_command).pack(side="left", padx=5)
        self.log = tk.Text(root, height=12, wrap="word")
        self.log.pack(fill="both", expand=True, padx=8, pady=8)
        self.refresh_ports()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def logline(self, s):
        self.log.insert("end", s + "\n")
        self.log.see("end")

    def refresh_ports(self):
        rows = get_ports()
        values = [f"{dev}  |  {desc}" for dev, desc in rows]
        self.port_combo["values"] = values
        if values and not self.port_var.get():
            self.port_var.set(values[0])
        self.logline(f"Detected {len(values)} serial port(s).")
        if not values:
            self.logline("No COM ports found. Plug in the OpenBCI dongle and press Refresh ports.")

    def selected_port(self):
        val = self.port_var.get().strip()
        if "|" in val:
            return val.split("|", 1)[0].strip()
        return val.split()[0].strip() if val else ""

    def command(self):
        cmd = [sys.executable, str(BRIDGE), "--board", self.board_var.get(), "--stream-name", self.stream_var.get(), "--timestamp-mode", self.timestamp_var.get(), "--confirmed-channel-map"]
        if self.board_var.get() != "synthetic":
            port = self.selected_port()
            if not port:
                raise ValueError("No COM port selected.")
            cmd += ["--serial-port", port]
        return cmd

    def start_bridge(self):
        if self.proc and self.proc.poll() is None:
            messagebox.showinfo("Bridge already running", "The bridge process is already running.")
            return
        try:
            cmd = self.command()
        except Exception as exc:
            messagebox.showerror("Missing setting", str(exc)); return
        self.logline("Starting bridge:")
        self.logline(" ".join(cmd))
        self.proc = subprocess.Popen(cmd)

    def start_watchdog(self):
        cmd = [sys.executable, str(WATCHDOG), "--stream-name", self.stream_var.get(), "--duration", "120", "--expected-rate", "125"]
        self.logline("Starting watchdog:")
        self.logline(" ".join(cmd))
        subprocess.Popen(cmd)

    def stop_bridge(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            self.logline("Terminate signal sent to bridge.")
        else:
            self.logline("No running bridge process to stop.")

    def copy_command(self):
        try:
            cmd = " ".join(self.command())
        except Exception as exc:
            messagebox.showerror("Missing setting", str(exc)); return
        self.clipboard_clear(); self.clipboard_append(cmd)
        self.logline("Copied command to clipboard.")

    def on_close(self):
        self.stop_bridge()
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
