# PRAYCG Unified Master Suite v1.5.5 — MRED-Peak/Resolution + Offline Interpreter

This package preserves the full Master Comprehensive Suite workbench and adds two usability/compression layers:

1. **MRED-Peak vs MRED-Resolution endpoint compression**
2. **Offline Interpretation Reporter** for deterministic module-by-module text reports

No existing modules are removed.

## Boxed primary path

```text
Timing/QC
+ StimulusFingerprint/CET-R
+ artifact/confound gates
-> A-MRED
-> MRED-Peak / MRED-Resolution endpoint compression
```

## Secondary summaries

```text
NIP / BIT / CII / IAQ
TTI
NUPI
```

## Exploratory / convergence

```text
KHT-topo
NAST
EET
MRED-ITP / ACG / OCU
OCM025 / RSM / CVB / SquintProxy
LSO / Subtitle Override when applicable
```

## Run endpoint compression

```bat
py -3.11 scripts\praycg_mred_peak_resolution_module_v1_5_5.py ^
  --analysis-folder "C:\PRAYCG\analysis_outputs\MyRun_MasterComprehensive" ^
  --project-name "MyRun"
```

## Run offline interpretation report

```bat
py -3.11 scripts\praycg_offline_interpretation_reporter_v1_5_5.py ^
  --analysis-folder "C:\PRAYCG\analysis_outputs\MyRun_MasterComprehensive"
```

## Run both from the v1.5.5 wrapper

```bat
py -3.11 scripts\praycg_unified_master_analysis_visualizer_v1_5_5.py ^
  --analysis-folder "C:\PRAYCG\analysis_outputs\MyRun_MasterComprehensive" ^
  --run-mred-peak-resolution-modules ^
  --write-offline-interpretation-report ^
  --project-name "MyRun"
```

## Boundary

This package writes deterministic, rule-coded summaries of existing output tables. It is not an embedded AI assistant. It does not infer private mental states, certify meaning, prove memory formation, prove OSM biology, or replace expert review.
