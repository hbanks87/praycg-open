# OSM / Opto-PING Rung 0N - K-Null Calibration Repair and Sensitivity-Specificity Balance v0.1

This package contains a synthetic specificity/sensitivity calibration gate for the Opto-PING Rung 0 ladder.

Rung 0N repairs the Rung 0M failure mode by using higher-resolution null distributions, generator-specific K thresholds, and a final-lock rule requiring both full reciprocal prediction and K significance. It is synthetic only and makes no biological or human EEG mechanism claim.

## Main report

- `report/OSM_OptoPING_Rung0N_KNullCalibration_Report_v0_1.pdf`
- `report/OSM_OptoPING_Rung0N_KNullCalibration_Report_v0_1.md`

## Reproducibility

Run:

```bash
python scripts/run_rung0n_k_null_calibration_repair_v0_1.py --out-dir reproduced_rung0n
```

The locked spec SHA-256 for this v0.1 gate is in:

```text
locked_protocol/LOCKED_SPEC_SHA256.txt
```

## Boundary

Synthetic sensitivity/specificity calibration only. This does not prove or disprove OSM, microtubular memory, biophotonic flickering, human EEG mechanism, or PR-AYC-G empirical results.
