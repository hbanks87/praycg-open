@echo off
cd /d "%~dp0\.."
python scripts\praycg_confound_rsm_modules_v1_4_6.py ^
  --analysis-folder "C:\PRAYCG\outputs\MyRun_MasterComprehensiveSuite_v1_4_6" ^
  --event-log "C:\PRAYCG\run_logs\PRAYCG1_9_events.json" ^
  --cue-schedule-json "C:\PRAYCG\stimuli\cue_schedule.json" ^
  --ocm-cue-epoch-csv "C:\PRAYCG\outputs\MyRun\tables\combined_ocm_025_cue_epoch_table.csv"
pause
