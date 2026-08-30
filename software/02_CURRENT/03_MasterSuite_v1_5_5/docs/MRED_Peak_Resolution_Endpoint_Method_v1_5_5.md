# MRED-Peak vs MRED-Resolution Endpoint Compression v1.5.5

## Purpose

This module compresses the growing PR-AYC-G analysis workbench into two readable MRED endpoint families.

- **MRED-Peak:** acute, anchor-locked meaning recognition plus delayed integration.
- **MRED-Resolution:** delayed reflective/regulatory recovery after a meaningful anchor.

The module does not remove A-MRED, NIP, TTI, NUPI, EET, MRED-ITP, OCM, or any other analysis layer. It reads their outputs and produces a compact interpretation table.

## Scientific boundary

MRED-Peak and MRED-Resolution are endpoint-compression tools. They do not prove consciousness, memory formation, OSM biology, cellular hidden variables, or private experience.

## Inputs

The script reads whatever is available inside a Master Comprehensive Suite output folder, especially:

- `amred_anchor_endpoint_table.csv`
- `amred_primary_endpoint_summary.csv`
- `cii_anchor_integrals.csv`
- `nupi_anchor_polarity_table.csv`
- `nupi_run_summary.csv`
- `eet_endogenous_echo_tracking.csv`
- `mred_itp_anchor_summary.csv`
- `tti_anchor_deltas.csv`
- `tti_global_summary.csv`

Missing tables are not fabricated. The module downgrades the interpretation if supporting layers are absent.

## Outputs

- `mred_peak_resolution_anchor_table.csv`
- `mred_peak_resolution_run_summary.csv`
- `top_mred_peak_candidates.csv`
- `top_mred_resolution_candidates.csv`
- `mred_peak_resolution_visual_overlay.csv`
- `mred_peak_resolution_interpretation.json`

## Gate language

Peak gates:

- `STRICT_PEAK_PASS`
- `STRICT_PEAK_PASS_TIMING_CAUTION`
- `PEAK_CANDIDATE_NO_STRICT_LOCK`
- `RECOGNITION_ONLY_ENC_MISSING`
- `PEAK_NEGATIVE_OR_UNSUPPORTED`

Resolution gates:

- `RESOLUTION_CANDIDATE`
- `WEAK_RESOLUTION_SUPPORT`
- `RESOLUTION_NEGATIVE_OR_WEAK`
- `RESOLUTION_NOT_GRADABLE`

## Command

```bat
py -3.11 scripts\praycg_mred_peak_resolution_module_v1_5_5.py ^
  --analysis-folder "C:\PRAYCG\analysis_outputs\MyRun_MasterComprehensive" ^
  --project-name "MyRun"
```
