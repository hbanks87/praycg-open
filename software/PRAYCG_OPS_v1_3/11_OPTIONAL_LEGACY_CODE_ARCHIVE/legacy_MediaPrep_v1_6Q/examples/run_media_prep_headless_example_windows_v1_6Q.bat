@echo off
cd /d "%~dp0\.."
python scripts\praycg_media_prep_gui_v1_6Q.py --no-gui ^
  --project-name example_project ^
  --master "C:\PRAYCG\source\stimulus_master.mp4" ^
  --out-root "C:\PRAYCG\media_prepared" ^
  --seed 20260724 ^
  --cue-interval 3.0 ^
  --cue-duration 0.85 ^
  --start-delay 3.0 ^
  --min-value 1 ^
  --max-value 10 ^
  --position upper_right ^
  --control-audio-mode speech_shaped_noise_envelope ^
  --overwrite
pause
