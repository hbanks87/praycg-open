@echo off
REM PRAYCG MRED-ITP v1.5.2 - Contact example
python scripts\praycg_mred_itp_modules_v1_5_2.py ^
  --out-dir "C:\PRAYCG\outputs\Contact_MRED_ITP" ^
  --xdf "C:\path\to\sub-P001_ses-S001_task-Default_run-001_eeg.xdf" ^
  --event-log "C:\path\to\PRAYCG_v1_9_hoyt_S001_Contact_20260815_070408_events.json" ^
  --feature-csv "C:\path\to\Contact_Run1_feature_table_contact_time_resolved_feature_frame_v1_0.csv" ^
  --annotation-csv "C:\path\to\Contact_Run1_annotation_windows_v1_0.csv" ^
  --mred-event-csv "C:\path\to\Contact_Run1_candidate_local_kht_topo_mred_event_table_v1_0.csv" ^
  --stream-inventory-csv "C:\path\to\stream_inventory_corrected.csv"
