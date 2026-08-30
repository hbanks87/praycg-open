#!/usr/bin/env python3
"""Tiny Tkinter GUI for PRAYCG Offline Interpretation Reporter v1.5.5."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

SCRIPT = Path(__file__).with_name("praycg_offline_interpretation_reporter_v1_5_5.py")


def main() -> None:
    root = tk.Tk()
    root.title("PRAYCG Offline Interpretation Reporter v1.5.5")
    root.geometry("720x280")

    analysis_var = tk.StringVar()
    out_var = tk.StringVar()
    report_name_var = tk.StringVar(value="praycg_offline_interpretation_report")

    def browse_analysis():
        p = filedialog.askdirectory(title="Select Master Comprehensive Suite output folder")
        if p:
            analysis_var.set(p)
            if not out_var.get():
                out_var.set(str(Path(p) / "report"))

    def browse_out():
        p = filedialog.askdirectory(title="Select report output folder")
        if p:
            out_var.set(p)

    def run_report():
        if not analysis_var.get():
            messagebox.showerror("Missing folder", "Select an analysis folder first.")
            return
        cmd = [sys.executable, str(SCRIPT), "--analysis-folder", analysis_var.get(), "--report-name", report_name_var.get()]
        if out_var.get():
            cmd.extend(["--out-dir", out_var.get()])
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if proc.returncode != 0:
                messagebox.showerror("Reporter failed", proc.stderr[-4000:] or proc.stdout[-4000:])
            else:
                messagebox.showinfo("Report created", proc.stdout[-2000:] or "Report created.")
        except Exception as e:
            messagebox.showerror("Reporter failed", str(e))

    pad = {"padx": 8, "pady": 6}
    tk.Label(root, text="Analysis folder:").grid(row=0, column=0, sticky="w", **pad)
    tk.Entry(root, textvariable=analysis_var, width=78).grid(row=0, column=1, **pad)
    tk.Button(root, text="Browse", command=browse_analysis).grid(row=0, column=2, **pad)

    tk.Label(root, text="Output folder:").grid(row=1, column=0, sticky="w", **pad)
    tk.Entry(root, textvariable=out_var, width=78).grid(row=1, column=1, **pad)
    tk.Button(root, text="Browse", command=browse_out).grid(row=1, column=2, **pad)

    tk.Label(root, text="Report name:").grid(row=2, column=0, sticky="w", **pad)
    tk.Entry(root, textvariable=report_name_var, width=78).grid(row=2, column=1, **pad)

    tk.Label(root, text="This is a deterministic text-summary tool. It does not certify endpoints or infer consciousness.", fg="gray25").grid(row=3, column=0, columnspan=3, sticky="w", **pad)
    tk.Button(root, text="Generate Offline Interpretation Report", command=run_report, bg="#1f4e79", fg="white", font=("Arial", 11, "bold")).grid(row=4, column=0, columnspan=3, pady=18)

    root.mainloop()


if __name__ == "__main__":
    main()
