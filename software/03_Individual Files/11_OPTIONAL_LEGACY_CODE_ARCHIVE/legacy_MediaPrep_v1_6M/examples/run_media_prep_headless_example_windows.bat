@echo off
REM Example headless run. Edit paths before use.
cd /d "%~dp0\.."
python scripts\praycg_media_prep_gui_v1_6M.py --no-gui ^
  --project-name CODA_Pilot1 ^
  --master "C:\Users\hoytb\Desktop\PRAYCG_Sandbox\stimulus_master.mp4" ^
  --out-root "C:\Users\hoytb\Desktop\PRAYCG_Sandbox\prepared_media" ^
  --seed 20260724 ^
  --cue-interval 3.0 ^
  --cue-duration 0.85 ^
  --start-delay 3.0 ^
  --min-value 1 ^
  --max-value 10 ^
  --position upper_right ^
  --run-fingerprint ^
  --overwrite
pause
