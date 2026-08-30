# PRAYCG Control Center v0.4

A single public-facing desktop launcher for the PRAYCG ecosystem.

This is an **orchestrator**, not a replacement for the existing tools. It launches MediaPrep, acquisition streamers, PsychoPy/PRAYCG2.0, LabRecorder, the Master Comprehensive Suite, the Visualizer, and the Offline Interpreter as separate processes.

## Why this exists

PRAYCG has become powerful but spread across many scripts. Public users need one front door.

The Control Center provides:

- a main workflow dashboard;
- a Stimulus Library and MP4 validator;
- acquisition launch buttons for Polar, Vernier, BrainFlow EEG-only, and BrainFlow EEG+ALS;
- LSL stream checking;
- Signal Quality / Contact Index 0.4.0;
- ALS screen pulse barcode test;
- PsychoPy-safe runner launching;
- analysis and visualizer launch buttons;
- settings for all tool paths.

## Important runner note

The PRAYCG2.0 runner may need to be launched from **PsychoPy Coder** on some machines. This Control Center does not pretend to fix that. Instead, it makes that workflow explicit:

1. Set the PsychoPy Coder path in Settings.
2. Set the PRAYCG2.0 runner script path.
3. Use the Runner / PsychoPy tab.
4. Select **Open PsychoPy Coder + runner file/folder**, the default recommended mode.
5. Run the PRAYCG2.0 file from inside PsychoPy Coder.

Experimental direct-launch modes are included, but the safe mode is the default.

## Quick start on Windows

```bat
cd C:\path\to\PRAYCG_ControlCenter_v0.4
py -3.11 -m pip install -r requirements_optional.txt
run_PRAYCG_ControlCenter_v0.4.bat
```

On first launch, the Control Center writes a user config file to:

```text
%APPDATA%\PRAYCG_ControlCenter\config.json
```

Use the Settings tab to point to your current PRAYCG tools.

## Recommended root folder

```text
C:\PRAYCG\
  config\
  stimuli\
  runs\
  analysis\
  logs\
```

## Recommended workflow

1. Add master stimulus.
2. Run MediaPrep v1.8.
3. Run StimulusFingerprint QC.
4. Frame-lock anchors.
5. Start acquisition streams.
6. Check LSL streams.
7. Open LabRecorder.
8. Launch PRAYCG2.0 from PsychoPy Coder.
9. Run Master Comprehensive Suite.
10. Render Visualizer.
11. Generate Offline Interpretive Report.

## Included streamers

The package includes the user-provided Polar H10 and Vernier Respiration Belt LSL scripts under:

```text
tools/acquisition/
```

## Boundary

This software does not certify endpoints. It helps you organize and launch the pipeline.

The Signal Quality / Contact Index is not true impedance. It is a 0.4.0 live data quality proxy.

## v0.4 update: Auto-find buttons

v0.4 adds auto-find buttons for LabRecorder, PsychoPy, PsychoPy Coder/application, PsychoPy-bundled Python when discoverable, and the PRAYCG2.0 runner script. Use the Settings tab or the Runner / PsychoPy tab to run the auto-finder, then review the discovered paths before launching.

