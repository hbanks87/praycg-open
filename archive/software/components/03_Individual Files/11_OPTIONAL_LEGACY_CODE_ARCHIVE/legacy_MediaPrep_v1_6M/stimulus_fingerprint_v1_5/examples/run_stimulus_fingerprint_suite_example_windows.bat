@echo off
REM Example PRAYCG StimulusFingerprint Suite v1.5 headless run.
python scripts\praycg_stimulus_fingerprint_batch_ui_v1_5.py --no-gui ^
  --project-name CODA_Pilot1 ^
  --control stimulus_control_cued_scrambled.mp4 ^
  --target stimulus_target_cued_v1_6H.mp4 ^
  --override stimulus_override_cued_v1_6H.mp4 ^
  --cue-schedule-json cue_schedule_v1_6H.json ^
  --cue-schedule-csv cue_schedule_v1_6H.csv ^
  --out-root outputs ^
  --sample-fps 5 ^
  --resize-width 320
pause
