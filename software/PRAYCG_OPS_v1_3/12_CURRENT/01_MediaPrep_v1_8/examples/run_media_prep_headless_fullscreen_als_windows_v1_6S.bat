@echo off
REM Edit paths below, then double-click or run from Command Prompt.
python ..\scripts\praycg_media_prep_gui_v1_6S.py ^
  --no-gui ^
  --master "C:\path\to\stimulus_master.mp4" ^
  --out-root "C:\path\to\outputs" ^
  --project-name "MyStimulus" ^
  --overwrite ^
  --sensor-timing-enabled ^
  --sensor-pulse-mode fullscreen_start ^
  --sensor-video-start-duration 0.75 ^
  --sensor-fullscreen-black-guard 0.50
pause
