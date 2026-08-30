@echo off
cd /d "%~dp0.."
py -3.11 scripts\praycg_stimulus_fingerprint_v1_8.py ^
  --video "C:\PRAYCG\stimuli\Contact\stimulus_target_cued.mp4" ^
  --condition target ^
  --project-name Contact ^
  --out-dir "C:\PRAYCG\stimuli\Contact\qc\single_video_fingerprint_v1_8" ^
  --sample-rate-hz 8
pause
