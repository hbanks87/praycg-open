# Master Suite v1.4.9 - PRAYCG2.0 Self-Report Parser

This patch adds a parser for the consolidated PRAYCG2.0 report structure:

- branch core reports
- Override task reports
- gated confound detail reports
- pre-run display/audio calibration
- final master report

The parser produces table outputs that can be joined with MRED, NAST, TTI, OCM/RSM, and confound modules.

Run:

```bat
python scripts\praycg_selfreport20_parser_v1_4_9.py ^
  --event-log "C:\path	o\events.json" ^
  --sidecar-folder "C:\path	o\praycg_run_logs" ^
  --out-dir "C:\path	onalysis	ables"
```
