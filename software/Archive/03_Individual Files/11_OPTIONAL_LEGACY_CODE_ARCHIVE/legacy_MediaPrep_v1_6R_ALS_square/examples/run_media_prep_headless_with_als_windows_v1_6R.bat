@echo off
cd /d "%~dp0\.."
python scripts\praycg_media_prep_gui_v1_6R.py ^
  --no-gui ^
  --master "C:\path\to\stimulus_master.mp4" ^
  --out-root "C:\path\to\outputs" ^
  --project-name "MyStimulus" ^
  --overwrite ^
  --sensor-timing-enabled ^
  --sensor-position lower_right ^
  --sensor-pulse-mode video_start
pause
