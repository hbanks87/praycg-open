# PRAYCG Master Comprehensive Suite v1.4.6
## Confound-Aware Presentation + RSM/CVB/Squint Modules

## Purpose

Version 1.4.6 adds formal analysis support for issues that can change PR-AYC-G interpretation without invalidating a run automatically:

- perceived audio-video desynchrony;
- external acoustic intrusion such as train noise;
- cue legibility, small cue, blur, and display-scaling burden;
- possible squint / forehead visual-strain proxy;
- running-sum compute stalls and approximation pressure during Contextual Override.

These modules are covariate and veto layers. They do not prove meaning, OSM, hidden-Y biology, squinting, or a private cognitive strategy.

## New modules

### AVSyncConfound_v0.1

Uses PRAYCG1.9 branch confound reports, and future measured A/V sync files when available, to flag branches where lip-sync or audio-video delay may have disturbed narrative reception.

### ExternalAcousticIntrusion_v0.1

Uses PRAYCG1.9 external noise reports to flag branch windows where environmental sound may have masked or disrupted the stimulus audio. Example: distant train noise masking laptop speakers during a monologue.

### RSM_v0.1 — Running Sum Microstate Model

For each cue value `v_i`, the module reconstructs the true running sum:

```text
S_i = S_{i-1} + v_i
```

It then derives objective arithmetic-load features:

```text
prior_units_digit_i = S_{i-1} mod 10
carry_required_i = 1[prior_units_digit_i + v_i >= 10]
high_carry_load_i = max(0, prior_units_digit_i + v_i - 9)
hard9_personal_pattern_i = 1[v_i = 9 and prior_units_digit_i in {7,8,9}]
```

### CVB_v0.1 — Cue Visibility / Legibility Burden

This module separates easy cue recognition from visually costly cue processing. It is meant to capture cue size, blur, contrast, display scaling, and edge-position burden.

### SquintProxy_v0.1

Uses Fp1/frontal high-frequency and peak-to-peak sentinel features when available. This is a visual-strain/artifact covariate, not confirmed squint detection. EOG or eye tracking is required for confirmation.

## Core outputs

```text
branch_confound_reports.csv
prerun_display_audio_calibration_table.csv
confound_registry.csv
rsm_cvb_squint_cue_table.csv
rsm_visual_overlay.csv
confound_visual_overlay.csv
confound_rsm_interpretation.json
```

## Recommended command

```bat
python scripts\praycg_confound_rsm_modules_v1_4_6.py ^
  --analysis-folder "C:\path\to\MasterComprehensiveOutput" ^
  --event-log "C:\path\to\PRAYCG1_9_events.json" ^
  --cue-schedule-json "C:\path\to\cue_schedule.json" ^
  --ocm-cue-epoch-csv "C:\path\to\ocm_025_cue_epoch_table.csv"
```

Or through the unified launcher:

```bat
python scripts\praycg_unified_master_analysis_visualizer_v1_4.py ^
  --mode analysis_only ^
  --project-name MyRun ^
  --xdf "C:\path\to\run.xdf" ^
  --event-log "C:\path\to\events.json" ^
  --cue-schedule-json "C:\path\to\cue_schedule.json" ^
  --out-root "C:\PRAYCG\outputs" ^
  --run-confound-rsm-modules ^
  --overwrite
```

## Boundary

A confound report changes interpretation strength. It is not a proof of failure and not a proof of mechanism. If a target scene has train-noise masking, audio-video delay, or cue-legibility burden, that scene should be marked as confound-cautioned and analyzed with sensitivity windows or excluded from confirmatory claims.

## Manual retrospective addenda

For runs collected before PRAYCG1.9, presentation problems may not appear in the event log. Version 1.4.6 supports a manual retrospective addendum:

```bat
python scripts\praycg_confound_rsm_modules_v1_4_6.py ^
  --analysis-folder "C:\path\to\analysis" ^
  --event-log "C:\path\to\events.json" ^
  --cue-schedule-json "C:\path\to\cue_schedule.json" ^
  --manual-confound-json "C:\path\to\manual_confound_addendum.json"
```

Manual retrospective reports are explicitly lower claim strength than markers collected during the run. They should be used to label windows as confound-cautioned, not to create confirmatory anchors after the fact.
