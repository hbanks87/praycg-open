# Offline Interpretation Reporter v1.5.5

## Purpose

The Offline Interpretation Reporter generates a deterministic text/Markdown/JSON explanation of a Master Comprehensive Suite output folder. It is designed for:

- offline review without internet access;
- GitHub users who need a first-pass explanation of their own run outputs;
- reproducible documentation of what the module outputs appear to say;
- reducing dependence on chat-based interpretation.

## Important boundary

This is not a language model embedded in Python. It cannot reason creatively, infer context, or fix bad data. It uses rule-coded summaries of CSV/JSON outputs. It flags missing outputs rather than inventing them.

Self-report is treated as context, not proof. Timing, artifact, ALS, and stimulus-fingerprint QC can downgrade otherwise positive module outputs.

## Outputs

- `offline_interpretation_report.md`
- `offline_interpretation_report.txt`
- `offline_interpretation_report.json`
- `offline_interpretation_report_input_table_map.json`

## Command

```bat
py -3.11 scripts\praycg_offline_interpretation_reporter_v1_5_5.py ^
  --analysis-folder "C:\PRAYCG\analysis_outputs\MyRun_MasterComprehensive" ^
  --project-name "MyRun"
```

## Visualizer hook

After rendering a synchronized MP4, you can write the text interpretation beside the report outputs:

```bat
py -3.11 scripts\praycg_visualizer_interpretation_hook_v1_5_5.py ^
  --analysis-folder "C:\PRAYCG\analysis_outputs\MyRun_MasterComprehensive" ^
  --render-report-json "C:\PRAYCG\analysis_outputs\MyRun_MasterComprehensive\visualizer_render_report.json"
```

## Report structure

The report includes:

1. Executive verdict.
2. Claim boundary.
3. Module registry and boxed pathway.
4. A-MRED primary endpoint.
5. MRED-Peak vs MRED-Resolution.
6. NIP/CII/IAQ.
7. TTI.
8. NUPI.
9. CET/CET-R.
10. EET.
11. MRED-ITP.
12. OCM/RSM/CVB/Squint.
13. Baseline2.
14. Self-report.
15. QC/timing/confounds.
16. Suggested next actions.
