@echo off
cd /d %~dp0\..
python scripts\praycg_unified_master_analysis_visualizer_v1_4.py ^
  --mode analysis_only ^
  --project-name EDIT_PROJECT_NAME ^
  --xdf "EDIT_PATH_TO_RUN.xdf" ^
  --event-log "EDIT_PATH_TO_EVENTS.json" ^
  --cue-schedule-json "EDIT_PATH_TO_CUE_SCHEDULE.json" ^
  --out-root "outputs" ^
  --enable-module candidate_local_kht ^
  --overwrite
pause
