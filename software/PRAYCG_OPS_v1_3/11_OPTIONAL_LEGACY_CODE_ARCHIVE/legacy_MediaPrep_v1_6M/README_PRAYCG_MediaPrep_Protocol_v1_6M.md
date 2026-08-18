# PRAYCG MediaPrep + Protocol Suite v1.6M

This package standardizes the PR-AYC-G media-preparation workflow and bundles it with the latest windowed PRAYCG acquisition runner.

## What this package creates

From one master `.mp4`, the MediaPrep GUI creates:

1. `stimulus_target_cued_<project>_v1_6M.mp4`
2. `stimulus_override_cued_<project>_v1_6M.mp4`
3. `stimulus_control_cued_phase_scrambled_<project>_v1_6M.mp4`
4. `cue_schedule_<project>_v1_6M.json`
5. `cue_schedule_<project>_v1_6M.csv`
6. `media_prep_manifest_v1_6M.json`
7. `PRAYCG_MediaPrep_v1_6M_report.md`

The Target and Contextual Override cued videos are intentionally identical. Only instructions should differ during the experiment.

## Why the cue-embedded Target and Override are identical

The contextual override is supposed to change participant stance, not the physical stimulus. The participant sees the same cue-embedded narrative twice:

- Target instruction: ignore the numbers and watch naturally.
- Contextual Override instruction: keep a running sum of the numbers.

This preserves the key comparison: same photons, different task stance.

## Why the Control is generated from the cue-embedded Target

The phase-scrambled control is generated from the cue-embedded Target. This makes the control inherit the cue timing and low-level cue energy while removing recognizable narrative, faces, words, and normal structure.

## Main script

```bash
python scripts/praycg_media_prep_gui_v1_6M.py
```

The GUI lets you select:

- master MP4
- output folder
- project name
- cue seed
- cue interval
- cue duration
- cue start delay
- cue number range
- cue position
- optional StimulusFingerprint QC

## Recommended standard settings

```text
Cue interval: 3.0 seconds
Cue duration: 0.85 seconds
Start delay: 3.0 seconds
Cue values: 1 to 10
Cue position: upper_right
Badge opacity: 0.78
Font scale factor: 0.95
```

v1.6M uses a contrast-protected badge: a semi-transparent dark box, pale border, and white number with black outline. This directly addresses the Snack Attack problem where white numbers could become difficult to read on bright backgrounds.

## Headless example

```bash
python scripts/praycg_media_prep_gui_v1_6M.py --no-gui \
  --project-name CODA_Pilot1 \
  --master stimulus_master.mp4 \
  --out-root outputs \
  --seed 20260724 \
  --cue-interval 3.0 \
  --cue-duration 0.85 \
  --start-delay 3.0 \
  --min-value 1 \
  --max-value 10 \
  --position upper_right \
  --run-fingerprint \
  --overwrite
```

## Bundled protocol scripts

The latest windowed acquisition runner is included in:

```text
protocol_PRAYCG1_6L/
```

Use PRAYCG1.6L for acquisition because it creates the StasisMarkers stream before LabRecorder starts while keeping the preflight screen windowed so you can activate LabRecorder.

## Bundled StimulusFingerprint suite

The StimulusFingerprint v1.5 suite is included in:

```text
stimulus_fingerprint_v1_5/
```

The MediaPrep GUI can optionally call it automatically after generating the media.

## Recommended workflow

1. Run `scripts/praycg_media_prep_gui_v1_6M.py`.
2. Select one master MP4.
3. Generate cued Target, cued Override, phase-scrambled Control, cue JSON, cue CSV, and manifest.
4. Review the generated report and optional StimulusFingerprint QC.
5. Start OpenBCI / Polar / Vernier streams.
6. Launch `protocol_PRAYCG1_6L/scripts/run_PRAYCG1_6L_LSL_First_Windowed.py`.
7. Confirm `StasisMarkers`, `obci_eeg1`, `PolarHRV`, and `VernierRespirationBelt` appear in LabRecorder.
8. Run the protocol.
9. Verify the final XDF contains all streams.

## Boundary

This package prepares and runs media. It does not certify meaning, empathy, consciousness, or neural endpoints. Use the Master Comprehensive PR-AYC-G Suite for data analysis.
