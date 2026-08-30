@echo off
REM Edit these paths before running.
py -3.11 scripts\praycg_amred_endpoint_module_v1_5_3.py ^
  --analysis-folder "C:\PRAYCG\analysis_outputs\FieldOfDreams_Run1_MasterComprehensive" ^
  --anchor-file "C:\PRAYCG\stimuli\FieldOfDreams\predeclared_anchors_FieldOfDreams_CatchScene_LOCKED.json"
pause
