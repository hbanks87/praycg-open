#!/usr/bin/env python3
"""Batch PRAYCG StimulusFingerprint/CET/EET v1.8 for target/control/override.

This wrapper finds the three branch videos in a MediaPrep output folder and calls
praycg_stimulus_fingerprint_cet_eet_v1_8.py once with all available branches.
It is the preferred post-processing route for an existing MediaPrep folder.
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path


def first_match(folder: Path, patterns):
    for pat in patterns:
        xs = sorted(folder.glob(pat))
        if xs:
            return xs[0]
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Batch PRAYCG StimulusFingerprint/CET/EET v1.8 for target/control/override")
    ap.add_argument("--mediaprep-folder", required=True)
    ap.add_argument("--project-name", default=None)
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--video-sample-hz", type=float, default=8.0)
    ap.add_argument("--merge-hz", type=float, default=4.0)
    ap.add_argument("--resize-width", type=int, default=320)
    ap.add_argument("--anchor-json", default="")
    ap.add_argument("--fail-on-partial", action="store_true")
    args = ap.parse_args(argv)

    folder = Path(args.mediaprep_folder)
    if not folder.exists():
        raise FileNotFoundError(folder)
    project = args.project_name or folder.name
    out_dir = Path(args.out_dir) if args.out_dir else folder / "qc" / "stimulus_fingerprint_v1_8"
    out_dir.mkdir(parents=True, exist_ok=True)

    cue = first_match(folder, ["cue_schedule*.json", "*cue*schedule*.json"])
    anchor = Path(args.anchor_json) if args.anchor_json else first_match(folder, ["*LOCKED*.json", "predeclared_anchors*_LOCKED.json", "predeclared_anchors*.json"])
    branch_map = {
        "control": first_match(folder, ["stimulus_control_cued_phase_scrambled*.mp4", "*control*phase_scrambled*.mp4", "*control*.mp4"]),
        "target": first_match(folder, ["stimulus_target_cued*.mp4", "*target*cued*.mp4"]),
        "override": first_match(folder, ["stimulus_override_cued*.mp4", "*override*cued*.mp4"]),
    }

    script = Path(__file__).with_name("praycg_stimulus_fingerprint_cet_eet_v1_8.py")
    cmd = [sys.executable, str(script), "--project-name", project, "--out-root", str(out_dir), "--flat-output", "--overwrite", "--video-sample-hz", str(args.video_sample_hz), "--merge-hz", str(args.merge_hz), "--resize-width", str(args.resize_width)]
    for cond, video in branch_map.items():
        if video:
            cmd += [f"--{cond}", str(video)]
    if cue:
        cmd += ["--cue-schedule-json", str(cue)]
    if anchor:
        cmd += ["--anchor-json", str(anchor)]
    if args.fail_on_partial:
        cmd += ["--fail-on-partial"]

    (out_dir / "stimulusfingerprint_batch_command.txt").write_text(" ".join(map(str, cmd)), encoding="utf-8")
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    (out_dir / "stimulusfingerprint_batch_stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (out_dir / "stimulusfingerprint_batch_stderr.txt").write_text(proc.stderr or "", encoding="utf-8")

    manifest = {
        "schema": "PRAYCG_batch_stimulus_fingerprint_v1_8",
        "mediaprep_folder": str(folder),
        "project": project,
        "cue_schedule_json": str(cue) if cue else None,
        "anchor_json": str(anchor) if anchor else None,
        "outputs_dir": str(out_dir),
        "branch_paths": {k: str(v) if v else None for k, v in branch_map.items()},
        "returncode": proc.returncode,
        "status": "PASS" if proc.returncode == 0 else "NONZERO_RETURN",
        "boundary": "External stimulus regressors only; no physiological endpoint certification."
    }
    (out_dir / f"stimulus_fingerprint_batch_manifest_{project}_v1_8.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
