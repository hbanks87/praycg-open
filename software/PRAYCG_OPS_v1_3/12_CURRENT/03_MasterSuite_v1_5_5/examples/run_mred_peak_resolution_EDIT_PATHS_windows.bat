@echo off
REM Edit ANALYSIS_FOLDER below, then run.
set ANALYSIS_FOLDER=C:\PRAYCG\analysis_outputs\MyRun_MasterComprehensive
py -3.11 scripts\praycg_mred_peak_resolution_module_v1_5_5.py ^
  --analysis-folder "%ANALYSIS_FOLDER%" ^
  --run-label "MyRun" ^
  --overwrite
pause
