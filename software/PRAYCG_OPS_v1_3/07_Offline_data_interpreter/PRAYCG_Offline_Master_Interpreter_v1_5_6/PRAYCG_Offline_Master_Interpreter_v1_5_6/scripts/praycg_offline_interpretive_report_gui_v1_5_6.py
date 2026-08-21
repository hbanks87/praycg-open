#!/usr/bin/env python3
"""Small Tkinter GUI wrapper for the PRAYCG Offline Master Interpreter v1.5.6."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

SCRIPT = Path(__file__).with_name("praycg_offline_interpretive_report_generator_v1_5_6.py")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PRAYCG Offline Master Interpreter v1.5.6")
        self.geometry("860x540")
        self.analysis = tk.StringVar()
        self.outdir = tk.StringVar()
        self.runlabel = tk.StringVar()
        self.auto_mred = tk.BooleanVar(value=True)
        self._build()

    def _row(self, parent, label, var, folder=True):
        fr = ttk.Frame(parent); fr.pack(fill="x", pady=5)
        ttk.Label(fr, text=label, width=24).pack(side="left")
        ttk.Entry(fr, textvariable=var).pack(side="left", fill="x", expand=True)
        def browse():
            p = filedialog.askdirectory(title=f"Select {label}") if folder else filedialog.askopenfilename(title=f"Select {label}")
            if p: var.set(p)
        ttk.Button(fr, text="Browse", command=browse).pack(side="left", padx=4)

    def _build(self):
        pad = ttk.Frame(self, padding=12); pad.pack(fill="both", expand=True)
        ttk.Label(pad, text="PRAYCG Offline Master Interpreter v1.5.6", font=("Arial", 15, "bold")).pack(anchor="w")
        ttk.Label(pad, text="Reads a Master Comprehensive output folder and writes a rule-based Markdown/TXT explanation. No internet or AI model required.", wraplength=780).pack(anchor="w", pady=(4, 10))
        self._row(pad, "Analysis folder", self.analysis)
        self._row(pad, "Output folder", self.outdir)
        fr = ttk.Frame(pad); fr.pack(fill="x", pady=5)
        ttk.Label(fr, text="Run label", width=24).pack(side="left")
        ttk.Entry(fr, textvariable=self.runlabel).pack(side="left", fill="x", expand=True)
        ttk.Checkbutton(pad, text="Auto-generate MRED-Peak / MRED-Resolution tables first if missing", variable=self.auto_mred).pack(anchor="w", pady=7)
        ttk.Button(pad, text="Generate offline interpretive report", command=self.run).pack(anchor="w", pady=8)
        self.log = tk.Text(pad, height=14); self.log.pack(fill="both", expand=True)

    def run(self):
        if not self.analysis.get():
            messagebox.showwarning("Missing folder", "Select an analysis folder first.")
            return
        cmd = [sys.executable, str(SCRIPT), "--analysis-folder", self.analysis.get()]
        if self.outdir.get(): cmd += ["--out-dir", self.outdir.get()]
        if self.runlabel.get(): cmd += ["--run-label", self.runlabel.get()]
        if self.auto_mred.get(): cmd += ["--auto-run-mred-peak-resolution"]
        self.log.insert("end", "Running:\n" + " ".join(cmd) + "\n\n"); self.update_idletasks()
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=600)
            self.log.insert("end", res.stdout + "\n")
            if res.stderr: self.log.insert("end", "STDERR:\n" + res.stderr + "\n")
            if res.returncode == 0: messagebox.showinfo("Done", "Offline interpretive report generated.")
            else: messagebox.showerror("Failed", f"Generator exited with code {res.returncode}")
        except Exception as exc:
            self.log.insert("end", f"ERROR: {exc}\n"); messagebox.showerror("Error", str(exc))

if __name__ == "__main__":
    App().mainloop()
