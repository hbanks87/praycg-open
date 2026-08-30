# Offline Interpretive Report Generator v1.5.5

## Purpose

The offline interpreter reads a Master Comprehensive Suite output folder and writes a plain-language Markdown/TXT report explaining what the detected module outputs appear to say.

It is designed for GitHub/OSF users who may not understand every PRAYCG table and need a deterministic local helper without internet access.

## It is not an AI model

The interpreter is a rule-based text generator. It does not use ChatGPT, does not call the internet, and does not infer private experience beyond the fields present in CSV/JSON outputs.

## Main command

```bat
py -3.11 scripts\praycg_offline_interpretive_report_generator_v1_5_5.py ^
  --analysis-folder "C:\path\to\MasterComprehensiveOutput" ^
  --auto-run-mred-peak-resolution ^
  --run-label "MyRun"
```

## GUI command

```bat
py -3.11 scripts\praycg_offline_interpretive_report_gui_v1_5_5.py
```

## Outputs

```text
reports/offline_interpretation/offline_interpretive_report.md
reports/offline_interpretation/offline_interpretive_report.txt
reports/offline_interpretation/offline_interpretive_report_summary.json
```

## Interpretation hierarchy

The report separates modules into:

1. Data/QC gates.
2. Boxed primary endpoint path.
3. MRED-Peak versus MRED-Resolution.
4. Secondary summaries.
5. Exploratory/convergence modules.
6. Self-report and confound context.
7. Next-step guidance.

## Boundary

The report is an interpretation aid. It does not certify endpoint validity and should not be used as a substitute for visual inspection, artifact review, timing QC, and replication.
