@echo off
cd /d "%~dp0.."
py -3.11 scripts\praycg_batch_stimulus_fingerprint_v1_8.py ^
  --mediaprep-folder "C:\PRAYCG\stimuli\Contact\Contact_MediaPrep_v1_8_YYYYMMDD_HHMMSS" ^
  --project-name Contact ^
  --out-dir "C:\PRAYCG\stimuli\Contact\Contact_MediaPrep_v1_8_YYYYMMDD_HHMMSS\qc\stimulus_fingerprint_v1_8" ^
  --video-sample-hz 8 ^
  --merge-hz 4 ^
  --resize-width 320
pause
