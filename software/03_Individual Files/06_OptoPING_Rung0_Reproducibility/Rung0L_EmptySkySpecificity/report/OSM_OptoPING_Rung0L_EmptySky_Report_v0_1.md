# OSM / Opto-PING Rung 0L - Standard-PING Null and Empty-Sky Specificity Gate v0.1

## Executive verdict

**Overall status:** `PARTIAL_OR_FAILED_SPECIFICITY`

Rung 0L is the explicit empty-sky test. It asks whether the Opto-PING reciprocal model hallucinates a hidden loop when the generator contains no reciprocal Y-loop.

## Locked specification

- Rung 0L spec SHA-256: `07b72130147812bd9f4cbf206bc224ff2af05874ab9ad1f554ed80310a64e8ae`
- Total trials: 360 (60 positive-control; 300 null / empty-sky)
- Trials per generator: 60
- Conditions per trial: 6
- Models compared: full_reciprocal, eta_only, zeta_only, null_no_coupling, replay_only_basis, standard_ping, generic_hidden_oscillator, sensory_drive_only

## Main result

### Positive-control loop-present generator

- Full reciprocal CV win rate mean: 0.731
- K within 15% rate: 1.000
- K within 10% rate: 0.933
- Median K_hat_scaled: 1.053

### Empty-sky loop-absent generators

- Null full-model CV win rate mean: 0.458
- Null false K-lock rate: 0.023
- Null non-full model CV win rate mean: 0.542
- Null median K_hat_scaled: 0.054

## Generator summary

| generator                        |   n_trials |   K_true_scaled |   median_K_hat_scaled |   mean_K_hat_scaled |   K_within_15_positive_rate |   K_within_10_positive_rate |   false_K_lock_rate |   full_cv_win_rate_mean |   full_cv_dominance_rate |   non_full_cv_win_rate_mean |   non_full_dominance_rate |
|:---------------------------------|-----------:|----------------:|----------------------:|--------------------:|----------------------------:|----------------------------:|--------------------:|------------------------:|-------------------------:|----------------------------:|--------------------------:|
| colored_noise_null               |         60 |               0 |             0.175029  |           0.17237   |                           0 |                    0        |            0.116667 |               0.822222  |                 0.95     |                    0.177778 |                  0        |
| full_reciprocal_positive_control |         60 |               1 |             1.05314   |           1.0493    |                           1 |                    0.933333 |            0        |               0.730556  |                 0.816667 |                    0.269444 |                  0        |
| generic_hidden_oscillator_null   |         60 |               0 |             0.0287964 |           0.0343289 |                           0 |                    0        |            0        |               0.872222  |                 0.983333 |                    0.127778 |                  0        |
| replay_only_null                 |         60 |               0 |             0.0526691 |           0.0616424 |                           0 |                    0        |            0        |               0.0833333 |                 0        |                    0.916667 |                  0.916667 |
| sensory_drive_only_null          |         60 |               0 |             0.0617484 |           0.0637138 |                           0 |                    0        |            0        |               0.111111  |                 0        |                    0.888889 |                  0.9      |
| standard_ping_null               |         60 |               0 |             0.0453807 |           0.0600197 |                           0 |                    0        |            0        |               0.4       |                 0.2      |                    0.6      |                  0.25     |

## Interpretation

Rung 0L complements Rung 0J/K. Rung 0J/K demonstrated positive synthetic recovery when the reciprocal loop was present. Rung 0L tests specificity: under Standard-PING, replay-only, sensory-drive-only, generic-hidden, and colored-noise generators, the full reciprocal model should lose and K should not lock.

## Boundary

Synthetic specificity only; no biological, PR-AYC-G, human EEG, or OSM mechanism claim.
