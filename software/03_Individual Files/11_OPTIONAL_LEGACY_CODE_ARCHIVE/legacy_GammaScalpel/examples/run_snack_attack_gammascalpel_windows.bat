@echo off
python scripts\praycg_gammascalpel_v1_0.py ^
  "sub-P001_ses-S001_task-Default_run-001_eeg(11).xdf" ^
  --events-json "PRAYCG_v1_6J_hoyt_S003_snack_attack_4_20260725_080636_events.json" ^
  --cue-json "cue_schedule_v1_6H.json" ^
  --out "SnackAttackRun1_GammaScalpel_v1_0_Analysis"
pause
