@echo off
set MEDIAPREP_FOLDER=C:\PRAYCGStimulus\Contact\Contact_final_scene_MediaPrep_v1_8_YYYYMMDD_HHMMSS
cd /d "%~dp0.."
py -3.11 scripts\praycg_batch_stimulus_fingerprint_v1_8.py ^
  --mediaprep-folder "%MEDIAPREP_FOLDER%" ^
  --project-name Contact ^
  --out-dir "%MEDIAPREP_FOLDER%\qc\stimulus_fingerprint_v1_8"
pause
