# PRAYCG MediaPrep Suite v1.6S — ALS-PT19 Fullscreen Start-Pulse Patch

This package prepares one master `.mp4` for PR-AYC-G and adds a stronger physical display-timing marker for an ALS-PT19, photodiode, or photoresistor-style analog light sensor.

v1.6S changes the default ALS mode from a small lower-corner square to a **full-screen white start pulse** followed by a short **black guard** before the original content begins. This is more robust because the sensor no longer has to be placed over a precise 38 × 38 pixel square.

## What it generates

From one master MP4, the suite creates:

1. Optional cleaned master video with documented source-stamp / watermark mask.
2. Number-cue-embedded Target video.
3. Bit-identical number-cue-embedded Contextual Override video.
4. Phase-scrambled Control generated from the cue-embedded Target.
5. ALS-PT19 physical timing marker in Target, Override, and Control.
6. Shifted cue schedule JSON/CSV with expected running sum.
7. Media-prep manifest, report, and QC checklists.

## Recommended KISS settings

Use the new default fullscreen start-pulse mode:

```text
sensor_timing_enabled = true
sensor_pulse_mode = fullscreen_start
sensor_video_start_duration = 0.75 sec
sensor_fullscreen_black_guard = 0.50 sec
```

This creates the following pattern inside every final branch video:

```text
0.00 - 0.75 s: full-screen white pulse
0.75 - 1.25 s: full-screen black guard
1.25 s onward: original cue-embedded content
```

The exact content start offset is written to the manifest as:

```text
content_start_offset_sec
analysis_exclusion_prefix_sec
```

The cue schedule is shifted automatically so the protocol runner's cue markers match the final rendered video time.

## Legacy corner-square mode

The previous v1.6R mode is still available:

```text
sensor_pulse_mode = video_start
sensor_position = lower_right
sensor_size_frac = 0.035
```

Use this only if you want the smaller hidden square behavior. The new `fullscreen_start` mode is recommended for reliability.

## Hardware use

Place the ALS-PT19 anywhere securely over the active display area where it can see the full-screen white flash. You no longer need to hit a precise lower-right square. A black tape shroud is still recommended to reduce room-light contamination.

Suggested Cyton analog AUX wiring:

```text
ALS-PT19 +      -> Cyton DVDD / 3V3
ALS-PT19 -      -> Cyton GND
ALS-PT19 OUT    -> Cyton D12 / A6
```

Powering the sensor from 3.3 V keeps its output within the Cyton-safe voltage range.

## Run GUI

```bash
python scripts\praycg_media_prep_gui_v1_6S.py
```

or double-click:

```text
examples\run_media_prep_gui_windows_v1_6S.bat
```

## Run headless example

```bash
python scripts\praycg_media_prep_gui_v1_6S.py ^
  --no-gui ^
  --master "C:\path\to\stimulus_master.mp4" ^
  --out-root "C:\path\to\outputs" ^
  --project-name "MyStimulus" ^
  --overwrite ^
  --sensor-timing-enabled ^
  --sensor-pulse-mode fullscreen_start ^
  --sensor-video-start-duration 0.75 ^
  --sensor-fullscreen-black-guard 0.50
```

## Output files to use in PRAYCG acquisition

Use the generated:

```text
stimulus_control_cued_phase_scrambled_<project>_v1_6S.mp4
stimulus_target_cued_<project>_v1_6S.mp4
stimulus_override_cued_<project>_v1_6S.mp4
cue_schedule_<project>_v1_6S.json
```

The Target and Override videos should remain hash-identical. The Control is generated from the number-cue-embedded Target and then receives the same full-screen ALS prefix as the other branches.

## Analysis rule

Exclude the prefix interval from physiological interpretation:

```text
0 <= t < analysis_exclusion_prefix_sec
```

The prefix is a physical timing marker, not part of the narrative stimulus.

## Boundary

The ALS marker validates physical display timing. It belongs to the external input vector `u(t)`. It is not biological photonic data and not a hidden-Y measurement.
