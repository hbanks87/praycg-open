#!/usr/bin/env python3
"""
PRAYCG Unified Launcher v1.5.5 - MRED Peak/Resolution + Offline Interpreter Hook

Compatibility wrapper that can be used after the normal Master Comprehensive Suite run.
It runs the new endpoint-compression module and/or the offline interpretation report from
an existing analysis output folder. It intentionally does not replace the full analysis engine.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

THIS = Path(__file__).resolve().parent


def run_py(script: str, args: list[str]) -> int:
    cmd = [sys.executable, str(THIS / script)] + args
    print('Running:', ' '.join(cmd))
    return subprocess.call(cmd)


def main() -> None:
    ap = argparse.ArgumentParser(description='PRAYCG v1.5.5 post-analysis launcher.')
    ap.add_argument('--analysis-folder', required=True, help='Existing Master Comprehensive output folder')
    ap.add_argument('--project-name', default='', help='Optional label')
    ap.add_argument('--run-mred-peak-resolution-modules', action='store_true')
    ap.add_argument('--write-offline-interpretation-report', action='store_true')
    ap.add_argument('--interpretation-out-dir', default='')
    ap.add_argument('--render-report-json', default='', help='Optional visualizer render_report.json')
    args = ap.parse_args()

    common = ['--analysis-folder', args.analysis_folder]
    if args.project_name:
        common += ['--project-name', args.project_name]

    if args.run_mred_peak_resolution_modules:
        rc = run_py('praycg_mred_peak_resolution_module_v1_5_5.py', common)
        if rc != 0:
            sys.exit(rc)

    if args.write_offline_interpretation_report:
        rep_args = common[:]
        if args.interpretation_out_dir:
            rep_args += ['--out-dir', args.interpretation_out_dir]
        if args.render_report_json:
            # Use the visualizer hook so render provenance is captured.
            rep_args += ['--render-report-json', args.render_report_json]
            rc = run_py('praycg_visualizer_interpretation_hook_v1_5_5.py', rep_args)
        else:
            rc = run_py('praycg_offline_interpretation_reporter_v1_5_5.py', rep_args)
        if rc != 0:
            sys.exit(rc)

    if not args.run_mred_peak_resolution_modules and not args.write_offline_interpretation_report:
        print('Nothing selected. Use --run-mred-peak-resolution-modules and/or --write-offline-interpretation-report.')


if __name__ == '__main__':
    main()
