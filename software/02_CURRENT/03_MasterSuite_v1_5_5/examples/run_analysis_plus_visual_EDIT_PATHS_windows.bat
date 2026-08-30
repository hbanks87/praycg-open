@echo off
cd /d %~dp0\..
python scripts\praycg_unified_master_analysis_visualizer_v1_4.py ^
  --mode analysis_plus_visual ^
  --project-name EDIT_PROJECT_NAME ^
  --xdf "EDIT_PATH_TO_RUN.xdf" ^
  --event-log "EDIT_PATH_TO_EVENTS.json" ^
  --cue-schedule-json "EDIT_PATH_TO_CUE_SCHEDULE.json" ^
  --out-root "outputs" ^
  --visual-video "EDIT_PATH_TO_BRANCH_VIDEO.mp4" ^
  --visual-condition target ^
  --visual-events "EDIT_PATH_TO_CUE_SCHEDULE.json" ^
  --enable-module candidate_local_kht ^
  --overwrite
pause
