@echo off
cd /d "%~dp0.."
py -3.11 scripts\praycg_stimulus_fingerprint_cet_eet_v1_8.py ^
  --project-name Contact ^
  --control "C:\PRAYCG\stimuli\Contact\stimulus_control_cued_phase_scrambled.mp4" ^
  --target "C:\PRAYCG\stimuli\Contact\stimulus_target_cued.mp4" ^
  --override "C:\PRAYCG\stimuli\Contact\stimulus_override_cued.mp4" ^
  --cue-schedule-json "C:\PRAYCG\stimuli\Contact\cue_schedule.json" ^
  --out-root "C:\PRAYCG\stimuli\Contact\qc" ^
  --flat-output ^
  --overwrite
pause
