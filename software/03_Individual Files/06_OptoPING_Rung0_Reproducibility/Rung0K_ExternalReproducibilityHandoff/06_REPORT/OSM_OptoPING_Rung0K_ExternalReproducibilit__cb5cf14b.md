# OSM / Opto-PING Rung 0K - External Reproducibility Handoff Report v0.1

## Executive verdict

Rung 0K is a **handoff pass**, not a true external-reproduction pass.

The frozen Rung 0J package was extracted into a fresh clean-room directory and rerun without modifying the locked model equations, parameter grids, perturbation order, seed policy, alternative models, pass/fail criteria, or reporting template. The internal clean-room replay reproduced the locked metrics.

A true external reproduction still requires another machine or independent reproducer to run this same package unchanged.

## Locked spec

Locked spec SHA-256:

```text
d93f6146e4e77ffeffbdd5c133250fd6d474317d8af6c34c3354dd6b28756282
```

## Clean-room replay results

| Criterion | Result | Status |
|---|---:|---|
| n trials | 60 | PASS |
| K within 15% | 1.000 | PASS |
| K within 10% | 1.000 | PASS |
| Median K error | 0.028175 | PASS |
| Directional eta/zeta <=20% | 1.000 | PASS |
| Full reciprocal CV fold wins | 0.872222 | PASS |

CV fold winners:

```json
{
  "full_reciprocal": 314,
  "replay_only_basis": 20,
  "zeta_only": 14,
  "eta_only": 9,
  "generic_hidden_oscillator": 3
}
```

## Why this is the right next gate

Rung 0J already changed the test from adaptive tuning to a locked seed-run. Rung 0K packages that locked result so another person can rerun it without touching the design. This is the correct next move because more tuning would weaken the meaning of the previous lock-in.

## What is frozen

- Model equations
- Parameter grids
- Perturbation order
- K-lock criteria
- Failure thresholds
- Random-seed policy
- Alternative models
- Reporting template

## What is not claimed

This is synthetic identifiability work. It does not prove OSM, microtubular memory, LTP, dendritic spine growth, quantum memory, or any human EEG mechanism. It only tests whether a locked synthetic model can reproduce its primary composite-coupling result.

## External reproduction status categories

| Status | Meaning |
|---|---|
| HANDOFF_READY | Locked files and instructions are packaged. |
| INTERNAL_CLEANROOM_PASS | Same locked package reran in a fresh directory. |
| EXTERNAL_PASS | Independent person/machine reran package unchanged and passed. |
| EXTERNAL_FAIL | Independent rerun failed without modifying the locked package. |

Current status:

```text
HANDOFF_READY + INTERNAL_CLEANROOM_PASS
```

## Next action

Send the ZIP to an external reproducer. They should run only the script in `02_REPRODUCTION_SCRIPT/`, then return:

- `reproduced_outputs/rung0j_pass_summary.json`
- `reproduced_outputs/rung0j_trial_results.csv`
- `reproduced_outputs/rung0j_cv_model_losses.csv`
- Python version and OS
- any deviation notes
