# OSM / Opto-PING Rung 0O - Locked Reproduction of Null-Aware Specificity Gate v0.1

## Executive verdict

**Status: `PASS_LOCKED_NULL_AWARE_REPRODUCTION`**

Rung 0O froze the Rung 0N null-aware specificity specification and ran a fresh synthetic seed set without changing the locked generator-specific K thresholds, selected complexity penalty, model alternatives, final-lock rule, or pass/fail targets.

The result is a **locked synthetic reproduction pass** for the null-aware gate.

## What was frozen from Rung 0N

- Rung 0N locked specification SHA-256: `f11cc9662d5a666c10f29e11f70c88a04e377e6499e87ae0bb1f1632e884a6b8`
- Selected complexity penalty: `0.04`
- Models: full reciprocal, eta-only, zeta-only, null/no-coupling, replay-only, standard PING, sensory-drive-only, generic-hidden, colored-noise alternative
- Final lock rule: full reciprocal prediction win **and** generator-calibrated K significance
- K significance is not interpreted independently
- Generator-specific K thresholds from Rung 0N were reused; they were not recalibrated in Rung 0O.

## Fresh seed set

- Rung 0O reproduction seed: `20260805`
- Total trials: `410`
- Positive-control trials: `60`
- Null / empty-sky trials: `350`

## Main results

| Metric | Result |
|---|---:|
| Positive full + K lock rate | 0.950 |
| Positive K significant rate | 1.000 |
| Positive K within 15% | 1.000 |
| Positive K within 10% | 0.950 |
| Positive median K_hat_scaled | 0.991 |
| Positive median K absolute error | 0.030 |
| Null false full + K lock rate | 0.000 |
| Null raw K significant rate | 0.003 |
| Null interpreted K rate | 0.000 |
| Null full predictive win rate | 0.000 |
| Null non-full predictive win rate | 1.000 |

## Decision table

| criterion                                 |   value |   target | pass   |
|:------------------------------------------|--------:|---------:|:-------|
| positive_full_plus_K_lock_rate >= 0.80    |    0.95 |     0.8  | True   |
| positive_K_significant_rate >= 0.90       |    1    |     0.9  | True   |
| positive_K_within_15_rate >= 0.90         |    1    |     0.9  | True   |
| null_false_full_plus_K_lock_rate <= 0.05  |    0    |     0.05 | True   |
| null_interpreted_K_rate <= 0.05           |    0    |     0.05 | True   |
| null_non_full_predictive_win_rate >= 0.85 |    1    |     0.85 | True   |

## Cross-validation winners

- sensory_drive_only: 349 / 2460 folds (0.142)
- eta_only: 340 / 2460 folds (0.138)
- zeta_only: 324 / 2460 folds (0.132)
- full_reciprocal: 306 / 2460 folds (0.124)
- standard_ping: 299 / 2460 folds (0.122)
- null_no_coupling: 283 / 2460 folds (0.115)
- colored_noise_alt: 248 / 2460 folds (0.101)
- generic_hidden_oscillator: 175 / 2460 folds (0.071)
- replay_only_basis: 136 / 2460 folds (0.055)

## Generator-level summary

| generator                | generator_type   |   n_trials |   median_K_hat_scaled |   mean_K_hat_scaled |   K_significant_raw_rate |   full_predictive_win_rate |   interpreted_K_rate |   final_full_plus_K_lock_rate |   mean_full_fold_win_rate | dominant_model_mode   |   selected_threshold |
|:-------------------------|:-----------------|-----------:|----------------------:|--------------------:|-------------------------:|---------------------------:|---------------------:|------------------------------:|--------------------------:|:----------------------|---------------------:|
| colored_noise_null       | null             |         50 |             0.148652  |           0.143244  |                     0.02 |                       0    |                 0    |                          0    |                0.00333333 | null_no_coupling      |             0.342099 |
| generic_hidden_null      | null             |         50 |             0.107919  |           0.119868  |                     0    |                       0    |                 0    |                          0    |                0.0133333  | null_no_coupling      |             0.274014 |
| permuted_label_null      | null             |         50 |             0.0585868 |           0.0551901 |                     0    |                       0    |                 0    |                          0    |                0          | null_no_coupling      |             0.213644 |
| replay_only_null         | null             |         50 |             0.0600265 |           0.0577049 |                     0    |                       0    |                 0    |                          0    |                0          | null_no_coupling      |             0.213644 |
| sensory_drive_only_null  | null             |         50 |             0.0732653 |           0.0741264 |                     0    |                       0    |                 0    |                          0    |                0.01       | replay_only_basis     |             0.213644 |
| standard_ping_null       | null             |         50 |             0.0530278 |           0.0542706 |                     0    |                       0    |                 0    |                          0    |                0          | eta_only              |             0.213644 |
| time_reversed_null       | null             |         50 |             0.061081  |           0.0601548 |                     0    |                       0    |                 0    |                          0    |                0.00333333 | sensory_drive_only    |             0.213644 |
| full_reciprocal_positive | positive         |         60 |             0.991011  |           0.994928  |                     1    |                       0.95 |                 0.95 |                          0.95 |                0.825      | full_reciprocal       |           nan        |

## Interpretation

Rung 0N repaired the Rung 0M sensitivity/specificity problem by requiring a simultaneous two-gate lock: the full reciprocal model had to win prediction and K had to clear a generator-calibrated null threshold. Rung 0O asked whether that repaired gate reproduced under a fresh seed set without retuning.

It did. Positive-control sensitivity remained above the locked threshold, and empty-sky/null final false lock stayed at zero. The result supports the computational specificity of the synthetic gate. It does not establish any biological mechanism.

## Boundary

Locked synthetic reproduction of null-aware specificity gate only; no biological, human EEG, microtubular, biophotonic, or OSM mechanism claim.
