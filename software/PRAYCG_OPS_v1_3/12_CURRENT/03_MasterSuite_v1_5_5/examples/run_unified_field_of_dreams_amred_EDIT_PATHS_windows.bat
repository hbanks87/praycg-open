@echo off
REM Edit all paths before running. Use *_LOCKED.json for strict A-MRED.
py -3.11 scripts\praycg_unified_master_analysis_visualizer_v1_4.py ^
  --mode analysis_only ^
  --project-name FieldOfDreams_CatchScene_Run1 ^
  --xdf "C:\path\to\run.xdf" ^
  --event-log "C:\path\to\PRAYCG2_0_events.json" ^
  --cue-schedule-json "C:\path\to\cue_schedule_FieldOfDreams.json" ^
  --predeclared-anchor-file "C:\path\to\predeclared_anchors_FieldOfDreams_CatchScene_LOCKED.json" ^
  --mred-familiarity-csv "C:\path\to\FieldOfDreams_CatchScene_MRED_familiarity_covariates.csv" ^
  --mred-scene-map-csv "C:\path\to\FieldOfDreams_CatchScene_MRED_scene_map.csv" ^
  --stimulus-fingerprint-folder "C:\path\to\MediaPrep_Output\qc" ^
  --out-root "C:\PRAYCG\analysis_outputs" ^
  --run-amred-modules ^
  --run-tti-modules ^
  --overwrite
pause
