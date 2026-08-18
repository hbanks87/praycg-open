@echo off
cd /d "%~dp0\.."
python scripts\praycg_confound_rsm_modules_v1_4_6.py ^
  --analysis-folder "C:\PRAYCG\outputs\PRAYCG_Her_Run1_Comprehensive_Analysis_v1_0" ^
  --event-log "C:\PRAYCG\run_logs\PRAYCG_v1_6U_hoyt_banks_S0010_Her_run_1_20260806_060456_events.json" ^
  --cue-schedule-json "C:\PRAYCG\stimuli\Her\cue_schedule_Her_cued_sensor_v1_6R.json" ^
  --ocm-cue-epoch-csv "C:\PRAYCG\outputs\Her\tables\her_ocm025_cue_epoch_table.csv" ^
  --manual-confound-json "templates\Her_Run1_manual_confound_addendum_example.json"
pause
