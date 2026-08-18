@echo off
REM PRAYCG Unified Master Suite v1.4.3 - MRED example
cd /d %~dp0\..
python scripts\praycg_unified_master_analysis_visualizer_v1_4.py ^
  --mode analysis_only ^
  --project-name MyRun_MRED ^
  --xdf "C:\path\to\run.xdf" ^
  --event-log "C:\path\to\events.json" ^
  --cue-schedule-json "C:\path\to\cue_schedule.json" ^
  --predeclared-anchor-file "C:\path\to\predeclared_anchors.json" ^
  --mred-familiarity-csv "C:\path\to\mred_familiarity_covariates.csv" ^
  --mred-scene-map-csv "C:\path\to\mred_scene_map.csv" ^
  --out-root "C:\PRAYCG\analysis_outputs" ^
  --enable-module candidate_local_kht ^
  --enable-module meaning_recognition_encoding_dissociation ^
  --overwrite
pause
