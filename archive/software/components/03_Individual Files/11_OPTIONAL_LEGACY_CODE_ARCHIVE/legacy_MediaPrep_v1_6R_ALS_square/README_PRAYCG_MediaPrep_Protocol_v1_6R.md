# PRAYCG MediaPrep Suite v1.6R — ALS-PT19 Timing-Pulse Patch

This package prepares one master `.mp4` for PR-AYC-G and adds an optional physical display-timing square for an ALS-PT19, photodiode, or photoresistor-style analog light sensor.

## What it generates

From one master MP4, the suite creates:

1. Optional cleaned master video with documented source-stamp / watermark mask.
2. Number-cue-embedded Target video.
3. Bit-identical number-cue-embedded Contextual Override video.
4. Phase-scrambled Control generated from the cue-embedded Target.
5. Optional ALS-PT19 timing square rendered into Target, Override, and Control.
6. Cue schedule JSON/CSV with expected running sum.
7. Media-prep manifest, report, and QC checklists.

## Recommended KISS settings

Use the timing square in default mode first:

```text
sensor_timing_enabled = true
sensor_position = lower_right
sensor_pulse_mode = video_start
sensor_video_start_duration = 1.0 sec
sensor_cue_pulse_duration = 0.25 sec, ignored unless cue_start/both is selected
sensor_size_px = 0, auto
sensor_size_frac = 0.035
sensor_margin_px = 16
```

The default `video_start` mode renders one white pulse at the start of each video and keeps the square black otherwise. This validates actual physical video onset without adding a regular 3-second flicker train.

Use `cue_start` or `both` only for dedicated hardware-validation runs, because a pulse every cue can become a periodic visual perturbation if any light leaks around the sensor shroud.

## Hardware use

Place the ALS-PT19 directly over the lower-right timing square and surround it with black electrical tape or another opaque shroud. The participant should not see the square. The square is a hardware timing channel, not a subject-facing cue.

Suggested Cyton analog AUX wiring:

```text
ALS-PT19 +      -> Cyton DVDD / 3V3
ALS-PT19 -      -> Cyton GND
ALS-PT19 OUT    -> Cyton D12 / A6
```

Powering the sensor from 3.3 V keeps its output within the Cyton-safe voltage range.

## Run GUI

```bash
python scripts\praycg_media_prep_gui_v1_6R.py
```

or double-click:

```text
examples\run_media_prep_gui_windows_v1_6R.bat
```

## Run headless example

```bash
python scripts\praycg_media_prep_gui_v1_6R.py ^
  --no-gui ^
  --master "C:\path\to\stimulus_master.mp4" ^
  --out-root "C:\path\to\outputs" ^
  --project-name "MyStimulus" ^
  --overwrite ^
  --sensor-timing-enabled ^
  --sensor-position lower_right ^
  --sensor-pulse-mode video_start
```

## Output files to use in PRAYCG acquisition

Use the generated:

```text
stimulus_control_cued_phase_scrambled_<project>_v1_6R.mp4
stimulus_target_cued_<project>_v1_6R.mp4
stimulus_override_cued_<project>_v1_6R.mp4
cue_schedule_<project>_v1_6R.json
```

The Target and Override videos should remain hash-identical. The Control is generated from the number-cue-embedded Target and then receives the same sensor timing square as the other branches.

## Boundary

The timing square validates physical display timing. It belongs to the external input vector `u(t)`. It is not biological photonic data and not a hidden-Y measurement.
