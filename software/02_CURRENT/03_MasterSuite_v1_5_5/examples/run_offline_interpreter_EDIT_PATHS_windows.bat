@echo off
REM Edit this path to your Master Comprehensive Suite output folder.
set ANALYSIS_FOLDER=C:\PRAYCG\analysis_outputs\MyRun_MasterComprehensive

py -3.11 scripts\praycg_offline_interpretation_reporter_v1_5_5.py ^
  --analysis-folder "%ANALYSIS_FOLDER%" ^
  --report-name "my_run_offline_interpretation"

pause
