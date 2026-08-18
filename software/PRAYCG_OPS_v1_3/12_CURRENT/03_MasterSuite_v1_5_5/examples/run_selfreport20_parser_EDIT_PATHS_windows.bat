@echo off
python scripts\praycg_selfreport20_parser_v1_4_9.py ^
  --event-log "C:\path\to\events.json" ^
  --sidecar-folder "C:\path\to\praycg_run_logs" ^
  --out-dir "C:\path\to\analysis\tables"
pause
