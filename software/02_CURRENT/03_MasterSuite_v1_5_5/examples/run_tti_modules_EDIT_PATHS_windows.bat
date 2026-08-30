@echo off
REM PRAYCG TTI v1.4.8 example. Edit paths before running.
python scripts\praycg_tti_reception_extraction_module_v1_4_8.py ^
  --analysis-folder "C:\PRAYCG\outputs\Contact_Run1_MasterSuite" ^
  --feature-csv "C:\PRAYCG\outputs\Contact_Run1_MasterSuite\tables\contact_time_resolved_feature_frame.csv" ^
  --event-table "C:\PRAYCG\outputs\Contact_Run1_MasterSuite\tables\candidate_local_kht_topo_mred_event_table.csv"
pause
