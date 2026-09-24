# Offline Interpretation Report Generator v1.5.5

## Purpose

The offline interpretation reporter reads a Master Comprehensive Suite output folder and writes a human-readable report in Markdown and plain text.

It is intended for:

```text
offline data review
GitHub/OSF users who do not have a local expert available
quick explanation of which modules passed, failed, or were unavailable
teaching new users how to read PR-AYC-G output folders
```

## What it is

A deterministic rule-based reporter.

It summarizes tables that already exist. It does not run new EEG preprocessing, does not make new statistical discoveries, and does not use an AI model.

## What it is not

```text
not a peer reviewer
not a clinical interpretation engine
not a consciousness detector
not a memory-formation proof
not an OSM mechanism detector
not a replacement for reading the actual tables
```

## Main command

```bat
py -3.11 scripts\praycg_offline_interpretation_reporter_v1_5_5.py ^
  --analysis-folder "C:\path\to\MasterComprehensiveOutput" ^
  --report-name "my_run_interpretation"
```

## GUI command

```bat
py -3.11 scripts\praycg_offline_interpretation_gui_v1_5_5.py
```

## Visualizer sidecar command

```bat
py -3.11 scripts\praycg_visualizer_report_sidecar_v1_5_5.py ^
  --analysis-folder "C:\path\to\MasterComprehensiveOutput" ^
  --visualizer-mp4 "C:\path\to\visualizer_output.mp4"
```

## Outputs

```text
report/praycg_offline_interpretation_report.md
report/praycg_offline_interpretation_report.txt
report/praycg_offline_interpretation_report.json
```

## Design principle

The report uses the current module hierarchy:

```text
PRIMARY PATH:
  Timing/QC + StimulusFingerprint/CET-R + artifact/confound gates -> A-MRED

SECONDARY:
  NIP/BIT/CII/IAQ, TTI, NUPI, MRED-Peak/Resolution

EXPLORATORY / CONVERGENCE:
  KHT-topo, NAST, EET, MRED-ITP/ACG/OCU, OCM025/RSM/CVB/SquintProxy, LSO when applicable
```

The reporter should make the output easier to understand without elevating exploratory modules into proof.
