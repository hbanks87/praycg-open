@echo off
REM Edit paths before running.
python scripts\praycg_nip_cet_eet_modules_v1_5_1.py ^
  --feature-csv "C:\path\to\Contact_Run1_feature_table_contact_time_resolved_feature_frame_v1_0.csv" ^
  --event-csv "C:\path\to\Contact_Run1_candidate_local_kht_topo_mred_event_table_v1_0.csv" ^
  --annotation-csv "C:\path\to\Contact_Run1_annotation_windows_v1_0.csv" ^
  --cue-schedule-json "C:\path\to\cue_schedule_Contact_final_scene_v1_6S.json" ^
  --out-dir "C:\PRAYCG\outputs\Contact_NIP_CET_EET_v1_5_1"
