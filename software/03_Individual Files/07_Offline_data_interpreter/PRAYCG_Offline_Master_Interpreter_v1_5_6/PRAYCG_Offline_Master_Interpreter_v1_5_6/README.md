# PRAYCG Offline Master Interpreter v1.5.6

This is a standalone, GitHub-uploadable subset of the PRAYCG Master Comprehensive Suite.

It reads a Master Comprehensive analysis output folder and writes a deterministic, rule-based text interpretation:

```text
reports/offline_interpretation/offline_interpretive_report.md
reports/offline_interpretation/offline_interpretive_report.txt
reports/offline_interpretation/offline_interpretive_report_summary.json
```

It is not an AI model and does not require internet access.

## What it can summarize

The interpreter searches for available tables in an analysis folder, including:

```text
A-MRED
MRED-Peak / MRED-Resolution
DGA / Decoder Gate Availability
NUPI
TTI
CII/NIP
CET/EET
MRED-ITP
OCM/RSM
Baseline1 vs Baseline2
ALS/timing QC
stream inventory
phase summaries
```

It explains what is present and what is missing. Missing modules are reported as unavailable rather than invented.

## GUI use

```bat
run_offline_interpreter_gui_windows.bat
```

Then select a Master Comprehensive analysis folder and press Generate.

## Command-line use

```bat
py -3.11 scripts\praycg_offline_interpretive_report_generator_v1_5_6.py ^
  --analysis-folder "C:\PRAYCG\analysis\MyRun_MasterComprehensive" ^
  --run-label "MyRun" ^
  --auto-run-mred-peak-resolution
```

## Boundary

This tool summarizes available PRAYCG module outputs. It does not prove consciousness, memory formation, OSM biology, hidden-Y mechanisms, clinical effects, or literal thermodynamic entropy. Self-report is treated as contextual evidence, not proof of internal state.
