@echo off
REM Run this after your visualizer MP4 render.
py -3.11 scripts\praycg_visualizer_interpretation_hook_v1_5_5.py ^
  --analysis-folder "C:\PRAYCG\analysis_outputs\MyRun_MasterComprehensive" ^
  --render-report-json "C:\PRAYCG\analysis_outputs\MyRun_MasterComprehensive\my_visualizer_render_report.json" ^
  --project-name "MyRun"
pause
