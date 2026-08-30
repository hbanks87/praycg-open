# PRAYCG Unified Master Suite v1.5.3 — A-MRED + Field of Dreams Patch

This package preserves all prior modules and adds the A-MRED primary endpoint compression plus Field of Dreams “Have a Catch?” anchor scaffolds.

## Recommended boxed pathway

```text
Timing/QC + MediaPrep/StimulusFingerprint/CET-R
  → artifact/confound gate
  → A-MRED primary endpoint
  → NIP/TTI secondary summaries
  → exploratory convergence modules as needed
```

See `docs/A_MRED_PrimaryEndpoint_Method_v1_5_3.md`, `docs/MODULE_TIER_MAP_v1_5_3.md`, and `docs/FIELD_OF_DREAMS_CATCH_SCENE_ANCHOR_GUIDE_v1_0.md`.

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

## v1.4.4 update - NAST and OCM

This package adds two additional modules:

- `NAST_v0.1`: Narrative Absorption State Transition. This is a DMN-proxy / absorption-transition analysis; it does not directly measure the fMRI-defined Default Mode Network.
- `OCM_v0.1`: Override Cue Microstate Analysis. This tests whether the upper-right number-cue task produces cue-locked digit-recognition and working-memory update microstates.

The main module implementation is:

```text
scripts/praycg_nast_ocm_modules_v1_4_4.py
```

The MasterSync Visualizer has been updated to auto-ingest NAST/OCM visual-overlay CSVs from an analysis folder.

## v1.4.6 OCM025 patch

This copy includes `scripts/praycg_ocm_quartersecond_reextract_v1_4_5.py`, a standalone raw-XDF OCM_v0.2 module for 0.25-second cue-locked re-extraction. See `docs/OCM_v0_2_RawXDF_QuarterSecond.md`.


## v1.4.6 Confound-aware additions

Adds formal post-run modules for PRAYCG1.9 confound reports, RSM_v0.1 Running Sum Microstate Model, CVB_v0.1 Cue Visibility/Legibility Burden, SquintProxy_v0.1, AVSyncConfound_v0.1, and ExternalAcousticIntrusion_v0.1. Use `--run-confound-rsm-modules` in the unified launcher after running the Master Suite.


## v1.4.7 Topo-OSM / LSO update

This package adds human-scale network-state interpretation (`K_HT-topo`) and optional Lexical/Subtitle Override analysis. It does not infer microtubules, biophotons, cellular OSM, or molecular memory from scalp EEG.

## v1.4.8 TTI module

This package adds `TTI_v0.1`, the Thermodynamic Theft Index / Reception-Extraction Tradeoff module. It estimates whether natural Target viewing preserved more receptive meaning/integration while Contextual Override diverted finite work capacity into task extraction.

Run directly:

```bat
python scripts\praycg_tti_reception_extraction_module_v1_4_8.py --analysis-folder "C:\path\to\analysis_folder"
```

Run through unified launcher:

```bat
python scripts\praycg_unified_master_analysis_visualizer_v1_4.py --mode analysis_only --project-name MyRun --xdf run.xdf --event-log events.json --cue-schedule-json cue_schedule.json --out-root outputs --run-tti-modules --overwrite
```

TTI remains exploratory and bounded. It is not a moral score, clinical metric, consciousness proof, or OSM biology claim.


## v1.5.1 additions

Adds `scripts/praycg_nip_cet_eet_modules_v1_5_1.py` for NIP/BIT/CII/IAQ and CET/EET analysis, plus `scripts/praycg_master_sync_visualizer_v1_3_1.py` with overlay recognition for NIP/CET/EET outputs.


## v1.5.2 MRED-ITP update

Adds the Information-Thermodynamic Proxy layer: ACG (Algorithmic Complexity Gate), CSI (Complexity Settlement Index), OCU (Ocular-Cognitive Unloading proxy), and ORI (Ocular Release Index). The module can use raw XDF through the bundled minimal XDF reader and can fall back to feature-level proxies when raw EEG/EOG are unavailable. These are proxy modules only and do not prove literal thermodynamic entropy reduction, memory encoding, OSM biology, hidden-Y biology, microtubules, or biophotons.

Main script: `scripts/praycg_mred_itp_modules_v1_5_2.py`.

## v1.5.4 NUPI addition

This package adds `NUPI_v0.1 - Narrative Update Polarity Index`, a secondary/exploratory module that estimates whether a narrative event/run is better described as accommodative load, resolutive recovery, high-load-with-recovery, or unresolved recognition. A-MRED remains the boxed primary recommended endpoint.

Run directly:

```bat
py -3.11 scripts\praycg_nupi_module_v1_5_4.py ^
  --analysis-folder "C:\path\to\MasterComprehensiveOutput\tables" ^
  --profile field ^
  --run-name FieldOfDreams_Run1
```

Run via unified launcher:

```bat
py -3.11 scripts\praycg_unified_master_analysis_visualizer_v1_4.py ^
  --mode analysis_only ^
  --project-name MyRun ^
  --xdf "C:\path\to\run.xdf" ^
  --event-log "C:\path\to\events.json" ^
  --cue-schedule-json "C:\path\to\cue_schedule.json" ^
  --out-root "C:\PRAYCG\outputs" ^
  --run-nupi-modules ^
  --nupi-profile field
```

---

# v1.5.5 Addendum — MRED-Peak / MRED-Resolution + Offline Interpreter

This package adds a rule-based endpoint-compression layer and an offline plain-language interpreter.

## New scripts

```text
scripts/praycg_mred_peak_resolution_module_v1_5_5.py
scripts/praycg_offline_interpretive_report_generator_v1_5_5.py
scripts/praycg_offline_interpretive_report_gui_v1_5_5.py
```

## MRED-Peak / MRED-Resolution

MRED-Peak asks whether a predeclared anchor produced an acute Target-specific recognition/integration event.

MRED-Resolution asks whether an anchor produced delayed reflective/regulatory recovery rather than a sharp event peak.

Run:

```bat
py -3.11 scripts\praycg_mred_peak_resolution_module_v1_5_5.py ^
  --analysis-folder "C:\path\to\MasterComprehensiveOutput"
```

## Offline interpretive report

The interpreter reads detected tables and writes local Markdown/TXT/JSON explanation files:

```bat
py -3.11 scripts\praycg_offline_interpretive_report_generator_v1_5_5.py ^
  --analysis-folder "C:\path\to\MasterComprehensiveOutput" ^
  --auto-run-mred-peak-resolution
```

GUI:

```bat
py -3.11 scripts\praycg_offline_interpretive_report_gui_v1_5_5.py
```

## Boundary

The offline interpreter is deterministic and rule-based. It does not use an AI model and does not certify endpoint validity. It is meant to help local/offline users understand module outputs before deeper review.
