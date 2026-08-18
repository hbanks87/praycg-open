# PRAYCG Unified Master Suite v1.4.3

This package combines the Master Comprehensive PR-AYC-G Analysis Suite and the MasterSync visual review tool.

## What is new in v1.4.3

- Adds `MRED_v0.1` / `meaning_recognition_encoding_dissociation` to the Master Comprehensive Analysis Suite.
- MRED separates Meaning Recognition / schema-reactivation load from theta-indexed new Encoding / integration load.
- Keeps CandidateLocal_KHT_v0.2 cross-boundary paired-washout follow-up logic.
- Updates MasterSync Visualizer to v1.2.2 with automatic MRED overlay ingestion.
- Keeps the v1.4.1 Analysis-folder picker and automatic Feature CSV detection.
- Adds optional MRED scene-map and familiarity/novelty covariate CSV inputs.
- Adds a unified launcher that can run either:
  - analysis only, or
  - analysis plus synchronized visual MP4 generation.

## Core boundary

This is an analysis and visualization package. It does not certify meaning, task compliance, OSM, hidden-Y biology, human EEG mechanism, or cellular mechanism. CandidateLocal_KHT estimates an event-level human-translation coupling proxy. MRED is an interpretive layer that distinguishes recognition/reactivation from possible new integration. Neither is K_OSM.

## Fast install on Windows

```bat
cd C:\PRAYCG\PRAYCG_Unified_MasterSuite_v1_4_3_MRED
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements_praycg_unified_v1_4.txt
```

Python 3.11 or 3.12 is recommended.

## Run GUI

```bat
python scripts\praycg_unified_master_analysis_visualizer_v1_4.py --gui
```

## Run analysis only

```bat
python scripts\praycg_unified_master_analysis_visualizer_v1_4.py ^
  --mode analysis_only ^
  --project-name MyRun ^
  --xdf "C:\path\to\run.xdf" ^
  --event-log "C:\path\to\events.json" ^
  --cue-schedule-json "C:\path\to\cue_schedule.json" ^
  --out-root "C:\path\to\analysis_outputs" ^
  --enable-module candidate_local_kht ^
  --enable-module meaning_recognition_encoding_dissociation ^
  --overwrite
```

## Run analysis plus visual review

```bat
python scripts\praycg_unified_master_analysis_visualizer_v1_4.py ^
  --mode analysis_plus_visual ^
  --project-name MyRun ^
  --xdf "C:\path\to\run.xdf" ^
  --event-log "C:\path\to\events.json" ^
  --cue-schedule-json "C:\path\to\cue_schedule.json" ^
  --out-root "C:\path\to\analysis_outputs" ^
  --visual-video "C:\path\to\stimulus_target_cued.mp4" ^
  --visual-condition target ^
  --visual-events "C:\path\to\cue_schedule.json" ^
  --overwrite
```

## Key outputs

After analysis, look in:

```text
<out-root>/<project>_MasterComprehensiveSuite_v1.4.3_<timestamp>/tables/
```

New CandidateLocal_KHT outputs:

```text
candidate_local_kht_analysis.csv
candidate_local_kht_anchor_manifest.csv
candidate_local_kht_random_anchor_reference.csv
candidate_local_kht_interpretation.json
candidate_local_kht_visual_overlay.csv
```

The visualizer can automatically pick up the CandidateLocal_KHT tables if you pass:

```text
--analysis-out <Master Comprehensive output folder>
```



## v1.4.2 GUI patch: Analysis folder vs Feature CSV

The MasterSync Visualizer now treats these fields separately:

```text
Analysis folder:
  The root Master Comprehensive Suite output folder. Use Browse Folder.

Feature CSV:
  The continuous time-series feature table used to draw theta/gamma, HR/HRV, API-A, respiration, and ALS.
```

If the Feature CSV field is blank and an Analysis folder is supplied, the visualizer auto-detects the best feature table in this order:

```text
tables/human_translation_kht_feature_frame.csv
tables/her_time_resolved_feature_frame.csv
tables/*_time_resolved_feature_frame.csv
tables/*feature_frame*.csv
```

If an older file-picker workflow accidentally places a CSV into the Analysis folder field, v1.4.2 recovers by using that CSV as the Feature CSV and the parent analysis folder for overlays.

For Her-style existing analysis packages, the correct setup is usually:

```text
Analysis folder = PRAYCG_Her_Run1_Comprehensive_Analysis_v1_0
Feature CSV     = PRAYCG_Her_Run1_Comprehensive_Analysis_v1_0\tables\her_time_resolved_feature_frame.csv
```

But the Feature CSV may now be left blank if the Analysis folder contains the file.


## v1.4.2 Cross-Boundary CandidateLocal_KHT Patch

CandidateLocal_KHT now supports paired-washout continuation for theta follow-up windows. See `docs/PATCH_NOTES_v1_4_2_CROSS_BOUNDARY_KHT.md`.


MRED_v0.1 outputs:

```text
mred_event_table.csv
mred_quadrant_classification.csv
mred_anchor_scene_map.csv
mred_familiarity_covariates.csv
mred_visual_overlay.csv
mred_interpretation.json
```

Optional MRED inputs:

```bat
--mred-familiarity-csv "C:\path\to\mred_familiarity_covariates.csv" ^
--mred-scene-map-csv "C:\path\to\mred_scene_map.csv"
```

MRED quadrants:

```text
MR_HIGH_ENC_HIGH: meaning recognition + possible new encoding candidate
MR_HIGH_ENC_LOW: meaning recognition / old-memory reactivation candidate
MR_LOW_ENC_HIGH: non-semantic encoding / task / artifact check
MR_LOW_ENC_LOW: null or weak event
```

Boundary: MRED does not prove memory encoding. Missing theta handoff does not prove no memory was encoded; it means this suite did not detect its operational theta-carryover marker.
