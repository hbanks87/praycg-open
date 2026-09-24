# OSM / Opto-PING Rung 0N Report v0.1

## Rung 0N - K-Null Calibration Repair and Sensitivity-Specificity Balance

**Status:** `PASS_NULL_CALIBRATION_REPAIRED`

Rung 0N was run to repair the sensitivity/specificity tradeoff exposed by Rung 0M. Rung 0M correctly stopped false final locks, but it reduced positive-control sensitivity. Rung 0N keeps the conservative null-aware rule but recalibrates the K threshold layer and model penalty layer.

## Locked / frozen elements in this gate

- Rung 0N spec SHA-256: `f11cc9662d5a666c10f29e11f70c88a04e377e6499e87ae0bb1f1632e884a6b8`
- Selected full-model penalty: `0.04`
- Total synthetic trials: `410`
- Positive-control trials: `60`
- Null / empty-sky trials: `350`

## What Rung 0N added

1. Higher-resolution null distributions: 5,000 calibration samples per null generator.
2. Generator-specific K thresholds.
3. K significance interpreted only when the full reciprocal model also wins prediction.
4. Penalty tuning to recover positive-control sensitivity.
5. Strong colored-noise and generic-hidden alternatives retained.

## Core decision rule

```text
FinalFullPlusKLock = FullPredictiveWin AND KSignificant
```

In other words, K by itself is not enough. Full-model prediction by itself is not enough. The pipeline requires both.

The K threshold rule was:

```text
selected_threshold = max(generator_q99, pooled_q975)
```

This makes each null generator carry its own high-resolution calibration while still protecting against under-thresholding weak null families.

## Main numerical result

Positive-control generator:

- Positive full+K lock rate: `0.967`
- Positive full predictive win rate: `0.967`
- Positive K significant rate: `1.000`
- Positive K within 15% rate: `1.000`
- Positive K within 10% rate: `0.950`
- Positive median K_hat_scaled: `1.014`

Empty-sky / null generators:

- Null false full+K lock rate: `0.000`
- Null raw K significant rate: `0.011`
- Null interpreted K rate: `0.000`
- Null full predictive win rate: `0.000`
- Null non-full predictive win rate: `1.000`
- Null median K_hat_scaled: `0.070`

## Interpretation

Rung 0N produced a cleaner sensitivity/specificity balance than Rung 0M. The positive-control generator still locked in 96.7% of trials, while the empty-sky false final-lock rate was 0.0%. Null generators still sometimes produced raw K-like values above threshold, but those values were not interpreted because the full reciprocal model did not win prediction.

This is the important methodological correction: **raw K is not sovereign**. K must travel with held-out predictive dominance.

## What this means

Rung 0N is a synthetic calibration pass. It strengthens the claim that the Opto-PING synthetic pipeline can be made both sensitive to loop-present synthetic data and quiet under structured null generators. It does not prove OSM, human EEG mechanism, PR-AYC-G K_HT, microtubular memory, biophotonic flickering, or Y_OSM.

## Next gate

The next gate should be:

```text
Rung 0O - Locked Null-Aware Replication Gate
```

Rung 0O should freeze the Rung 0N choices, then rerun on fresh seeds without penalty retuning or threshold adjustment.
