#!/usr/bin/env python3
"""
Optional visualizer sidecar wrapper.

This script is for workflows where you render a visualizer MP4 and want a separate
rule-based text interpretation report from the same Master Suite analysis folder.
It does not render video by itself; it calls the offline reporter after your visualizer
has produced or selected an analysis folder.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


def main() -> None:
    ap = argparse.ArgumentParser(description="Write a PRAYCG interpretation sidecar next to a visualizer MP4.")
    ap.add_argument("--analysis-folder", required=True)
    ap.add_argument("--visualizer-mp4", default=None, help="Optional MP4 path; report base name will follow this file.")
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()

    reporter = Path(__file__).with_name("praycg_offline_interpretation_reporter_v1_5_5.py")
    report_name = "praycg_offline_interpretation_report"
    if args.visualizer_mp4:
        report_name = Path(args.visualizer_mp4).stem + "_interpretation_sidecar"
        out_dir = Path(args.out_dir) if args.out_dir else Path(args.visualizer_mp4).resolve().parent
    else:
        out_dir = Path(args.out_dir) if args.out_dir else Path(args.analysis_folder).resolve() / "report"
    cmd = [sys.executable, str(reporter), "--analysis-folder", args.analysis_folder, "--out-dir", str(out_dir), "--report-name", report_name]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    print(proc.stdout)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(proc.returncode)
    print(json.dumps({"status": "OK", "sidecar_report_base": str(out_dir / report_name)}, indent=2))


if __name__ == "__main__":
    main()
