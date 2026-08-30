#!/usr/bin/env python3
"""Compatibility wrapper for PRAYCG StimulusFingerprint v1.8.

For new work, call praycg_stimulus_fingerprint_cet_eet_v1_8.py directly.
This wrapper preserves the older single-video interface and maps it to the v1.8
CET/EET regressor builder.
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
import praycg_stimulus_fingerprint_cet_eet_v1_8 as engine


def main(argv=None):
    ap = argparse.ArgumentParser(description="PRAYCG StimulusFingerprint v1.8 compatibility wrapper")
    ap.add_argument("--video", required=True)
    ap.add_argument("--out-dir", default="stimulus_fingerprint_v1_8")
    ap.add_argument("--project-name", default="PRAYCG_Stimulus")
    ap.add_argument("--condition", default="stimulus")
    ap.add_argument("--sample-rate-hz", type=float, default=8.0)
    ap.add_argument("--cue-schedule-json", default="")
    ap.add_argument("--anchor-json", default="")
    args = ap.parse_args(argv)
    mapped = [
        "--video", args.video,
        "--condition", args.condition,
        "--project-name", args.project_name,
        "--out-root", args.out_dir,
        "--flat-output",
        "--overwrite",
        "--video-sample-hz", str(args.sample_rate_hz),
        "--merge-hz", "4",
    ]
    if args.cue_schedule_json:
        mapped += ["--cue-schedule-json", args.cue_schedule_json]
    if args.anchor_json:
        mapped += ["--anchor-json", args.anchor_json]
    return engine.main_with_args(mapped) if hasattr(engine, "main_with_args") else _run_engine(mapped)


def _run_engine(mapped):
    old = sys.argv
    try:
        sys.argv = [str(Path(__file__).with_name("praycg_stimulus_fingerprint_cet_eet_v1_8.py"))] + mapped
        return engine.main()
    finally:
        sys.argv = old


if __name__ == "__main__":
    raise SystemExit(main())
