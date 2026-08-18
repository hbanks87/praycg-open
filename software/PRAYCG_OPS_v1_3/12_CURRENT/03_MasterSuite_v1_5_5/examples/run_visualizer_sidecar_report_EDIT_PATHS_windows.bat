@echo off
set ANALYSIS_FOLDER=C:\PRAYCG\analysis_outputs\MyRun_MasterComprehensive
set VISUALIZER_MP4=C:\PRAYCG\visuals\my_visualizer_output.mp4

py -3.11 scripts\praycg_visualizer_report_sidecar_v1_5_5.py ^
  --analysis-folder "%ANALYSIS_FOLDER%" ^
  --visualizer-mp4 "%VISUALIZER_MP4%"

pause
