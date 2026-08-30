@echo off
setlocal
REM Edit ANALYSIS_FOLDER and optional RUN_LABEL, then run this file.
set ANALYSIS_FOLDER=C:\PRAYCG\analysis\YourRun_MasterComprehensive
set RUN_LABEL=YourRun
cd /d "%~dp0"
py -3.11 -m pip install -r requirements.txt
py -3.11 scripts\praycg_offline_interpretive_report_generator_v1_5_6.py ^
  --analysis-folder "%ANALYSIS_FOLDER%" ^
  --run-label "%RUN_LABEL%" ^
  --auto-run-mred-peak-resolution
pause
