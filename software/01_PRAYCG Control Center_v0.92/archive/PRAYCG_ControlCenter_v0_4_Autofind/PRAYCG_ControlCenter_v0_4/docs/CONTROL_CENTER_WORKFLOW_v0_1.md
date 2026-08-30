# PRAYCG Control Center Workflow v0.4

## 1. Set paths

Open the Settings tab and set:

- PRAYCG Home
- Python executable
- MediaPrep GUI
- PRAYCG2.0 runner script
- PsychoPy Coder or PsychoPy app
- LabRecorder executable
- Master Suite GUI
- Visualizer GUI
- Offline Interpreter GUI
- BrainFlow EEG-only script
- BrainFlow EEG+ALS script

The bundled Polar and Vernier scripts are already referenced by default.

## 2. Add a master stimulus

Use **Stimulus Library → Add Master Stimulus**.

The tool copies the selected MP4 into:

```text
C:\PRAYCG\stimuli\<stimulus_id>\master\stimulus_master.mp4
```

and writes:

```text
master_media_validation_report.json
master_sha256.txt
```

The validator checks MP4 existence, extension, SHA-256, duration, video properties, and audio presence when FFmpeg/ffprobe or OpenCV are available.

## 3. Run MediaPrep

Click **Launch MediaPrep**. MediaPrep remains a separate GUI.

Recommended output location:

```text
C:\PRAYCG\stimuli\<stimulus_id>\mediaprep\<timestamped_folder>\
```

The Control Center scans for:

```text
stimulus_target_cued_*.mp4
stimulus_override_cued_*.mp4
stimulus_control_cued_phase_scrambled_*.mp4
cue_schedule_*.json
cue_schedule_*.csv
*_LOCKED.json
stimulus_exogenous_regressor_frame_all_conditions.csv
cet_regressors_all_conditions.csv
```

## 4. Start streams

Use the Acquisition tab.

Recommended order:

1. Start Polar H10 RR stream.
2. Start Vernier Respiration Belt stream.
3. Start BrainFlow EEG+ALS.
4. Run LSL Stream Checker.
5. Run Signal Quality / Contact Index.
6. Run ALS Screen Pulse Barcode Test.
7. Open LabRecorder.

## 5. Launch PRAYCG2.0

Use Runner / PsychoPy tab.

Default launch mode:

```text
Open PsychoPy Coder + runner file/folder
```

This is intentional because the runner may not work correctly when launched outside PsychoPy on some systems.

## 6. Run analysis

Use Analysis tab after acquisition.

Select the run folder and scan for:

```text
*.xdf
*_events.json
*_events.csv
*_run_config_media_selection.json
*_channel_map*.csv
*_core_report.json
*_confound_report.json
*_override_task_report.json
*_final_master_report.json
```

Then launch:

```text
Master Comprehensive Suite
Visualizer
Offline Interpreter
```
