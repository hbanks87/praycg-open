# OSM / Opto-PING Rung 0O - Locked Reproduction of Null-Aware Specificity Gate v0.1

Rung 0O freezes the Rung 0N null-aware specificity design and runs a fresh synthetic seed set without changing the model alternatives, selected penalty, K thresholds, pass/fail criteria, or final-lock rule.

## Status

`PASS_LOCKED_NULL_AWARE_REPRODUCTION`

## Source lock

- Source Rung 0N locked spec SHA-256: `f11cc9662d5a666c10f29e11f70c88a04e377e6499e87ae0bb1f1632e884a6b8`
- Rung 0O reproduction seed: `20260805`
- Selected penalty: `0.04`
- Threshold rule: locked generator-specific K thresholds from Rung 0N; no recalibration.

## Re-run

```bash
pip install -r requirements_rung0o_v0_1.txt
python scripts/run_rung0o_locked_reproduction_v0_1.py --out-dir reproduced_rung0o_outputs
```

## Boundary

This is synthetic sensitivity/specificity reproduction only. It is not biological evidence and does not prove or disprove OSM, microtubular memory, biophotonic flickering, human EEG mechanism, or PR-AYC-G empirical results.
