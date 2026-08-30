# OSM / Opto-PING Rung 0N - K-Null Calibration Repair and Sensitivity-Specificity Balance v0.1

## Executive verdict

**Status: PASS_NULL_CALIBRATION_REPAIRED**

Rung 0N repaired the specific weakness exposed by Rung 0M: K could still look significant under some null generators if interpreted by itself. The repaired rule is stricter and cleaner:

```text
Final lock = full reciprocal prediction win AND generator-calibrated K significance.
K significance is not interpreted when the full reciprocal model does not win prediction.
```

Under this rule, the synthetic gate passed:

| Metric | Result |
|---|---:|
| Total trials | 410 |
| Positive-control trials | 60 |
| Null / empty-sky trials | 350 |
| Selected complexity penalty | 0.040 |
| Positive full+K lock rate | 0.967 |
| Positive K significant rate | 1.000 |
| Positive K within 15% | 1.000 |
| Positive K within 10% | 0.950 |
| Null false full+K lock rate | 0.000 |
| Null raw K significant rate | 0.011 |
| Null interpreted K rate | 0.000 |
| Null non-full predictive win rate | 1.000 |

Locked Rung 0N spec SHA-256:

```text
f11cc9662d5a666c10f29e11f70c88a04e377e6499e87ae0bb1f1632e884a6b8
```

## What Rung 0N changed

Rung 0N implements the requested corrections:

1. Higher-resolution null distributions: 5,000 calibration samples per null generator.
2. Generator-specific K thresholds: each null generator receives a threshold equal to `max(generator_q99, pooled_q975)`.
3. K significance is interpreted only when full reciprocal prediction also wins.
4. Penalty tuning restores positive-control sensitivity while retaining a real complexity penalty.
5. Strong colored-noise and generic-hidden alternatives remain in the comparison set.

## Why this gate matters

Rung 0J showed that the pipeline can recover the reciprocal-loop endpoint when the loop is present in synthetic data. Rung 0L and 0M showed the harder problem: the model must also stay quiet under empty-sky generators. Rung 0N is the first null-aware gate in which:

```text
Positive sensitivity remained high.
Final false lock under null generators fell to zero.
Raw K significance was not allowed to become a standalone claim.
```

## Generator-level summary

| generator                | generator_type   |   n_trials |   median_K_hat_scaled |   mean_K_hat_scaled |   K_significant_raw_rate |   full_predictive_win_rate |   interpreted_K_rate |   final_full_plus_K_lock_rate |   mean_full_fold_win_rate | dominant_model_mode   |
|:-------------------------|:-----------------|-----------:|----------------------:|--------------------:|-------------------------:|---------------------------:|---------------------:|------------------------------:|--------------------------:|:----------------------|
| colored_noise_null       | nan              |         50 |             0.14236   |           0.152348  |                     0.02 |                   0        |             0        |                      0        |                      0    | sensory_drive_only    |
| generic_hidden_null      | nan              |         50 |             0.139604  |           0.143525  |                     0.06 |                   0        |             0        |                      0        |                      0.01 | null_no_coupling      |
| permuted_label_null      | nan              |         50 |             0.0548651 |           0.0578583 |                     0    |                   0        |             0        |                      0        |                      0    | sensory_drive_only    |
| replay_only_null         | nan              |         50 |             0.0562752 |           0.0520982 |                     0    |                   0        |             0        |                      0        |                      0    | null_no_coupling      |
| sensory_drive_only_null  | nan              |         50 |             0.0793415 |           0.0756865 |                     0    |                   0        |             0        |                      0        |                      0    | colored_noise_alt     |
| standard_ping_null       | nan              |         50 |             0.0588777 |           0.058715  |                     0    |                   0        |             0        |                      0        |                      0.01 | sensory_drive_only    |
| time_reversed_null       | nan              |         50 |             0.051463  |           0.0541156 |                     0    |                   0        |             0        |                      0        |                      0    | standard_ping         |
| full_reciprocal_positive | positive         |         60 |             1.01381   |           1.00919   |                     1    |                   0.966667 |             0.966667 |                      0.966667 |                      0.85 | full_reciprocal       |

## K-null calibration thresholds

| generator               |   n_calibration |   median_K_null |   q99_K_null |   selected_threshold | threshold_rule                  |
|:------------------------|----------------:|----------------:|-------------:|---------------------:|:--------------------------------|
| colored_noise_null      |            5000 |       0.134323  |     0.342099 |             0.342099 | max(generator_q99, pooled_q975) |
| generic_hidden_null     |            5000 |       0.122733  |     0.274014 |             0.274014 | max(generator_q99, pooled_q975) |
| permuted_label_null     |            5000 |       0.0609545 |     0.131031 |             0.213644 | max(generator_q99, pooled_q975) |
| replay_only_null        |            5000 |       0.049886  |     0.105653 |             0.213644 | max(generator_q99, pooled_q975) |
| sensory_drive_only_null |            5000 |       0.0699739 |     0.151619 |             0.213644 | max(generator_q99, pooled_q975) |
| standard_ping_null      |            5000 |       0.0550619 |     0.123583 |             0.213644 | max(generator_q99, pooled_q975) |
| time_reversed_null      |            5000 |       0.0549877 |     0.110636 |             0.213644 | max(generator_q99, pooled_q975) |

## Penalty tuning

|   penalty |   positive_full_plus_K_lock_rate |   positive_full_predictive_win_rate |   positive_K_significant_rate |   positive_K_within_15_rate |   positive_K_within_10_rate |   null_false_full_plus_K_lock_rate |   null_full_predictive_win_rate |   null_raw_K_significant_rate |     score |
|----------:|---------------------------------:|------------------------------------:|------------------------------:|----------------------------:|----------------------------:|-----------------------------------:|--------------------------------:|------------------------------:|----------:|
|      0    |                        1         |                           1         |                             1 |                           1 |                        0.95 |                                  0 |                               0 |                     0.0114286 |  1        |
|      0.02 |                        1         |                           1         |                             1 |                           1 |                        0.95 |                                  0 |                               0 |                     0.0114286 |  1        |
|      0.04 |                        0.966667  |                           0.966667  |                             1 |                           1 |                        0.95 |                                  0 |                               0 |                     0.0114286 |  0.966667 |
|      0.06 |                        0.9       |                           0.9       |                             1 |                           1 |                        0.95 |                                  0 |                               0 |                     0.0114286 |  0.9      |
|      0.08 |                        0.7       |                           0.7       |                             1 |                           1 |                        0.95 |                                  0 |                               0 |                     0.0114286 |  0.625    |
|      0.1  |                        0.466667  |                           0.466667  |                             1 |                           1 |                        0.95 |                                  0 |                               0 |                     0.0114286 |  0.275    |
|      0.12 |                        0.3       |                           0.3       |                             1 |                           1 |                        0.95 |                                  0 |                               0 |                     0.0114286 |  0.025    |
|      0.14 |                        0.15      |                           0.15      |                             1 |                           1 |                        0.95 |                                  0 |                               0 |                     0.0114286 | -0.2      |
|      0.16 |                        0.0333333 |                           0.0333333 |                             1 |                           1 |                        0.95 |                                  0 |                               0 |                     0.0114286 | -0.375    |
|      0.18 |                        0.0166667 |                           0.0166667 |                             1 |                           1 |                        0.95 |                                  0 |                               0 |                     0.0114286 | -0.4      |
|      0.2  |                        0.0166667 |                           0.0166667 |                             1 |                           1 |                        0.95 |                                  0 |                               0 |                     0.0114286 | -0.4      |

## Lock decision table

| criterion                                 |    value |   target | pass   |
|:------------------------------------------|---------:|---------:|:-------|
| positive_full_plus_K_lock_rate >= 0.80    | 0.966667 |     0.8  | True   |
| positive_K_significant_rate >= 0.90       | 1        |     0.9  | True   |
| positive_K_within_15_rate >= 0.90         | 1        |     0.9  | True   |
| null_false_full_plus_K_lock_rate <= 0.05  | 0        |     0.05 | True   |
| null_interpreted_K_rate <= 0.05           | 0        |     0.05 | True   |
| null_non_full_predictive_win_rate >= 0.85 | 1        |     0.85 | True   |

## Model-comparison fold winners

| model                     |   wins |   total_folds |   win_rate |
|:--------------------------|-------:|--------------:|-----------:|
| sensory_drive_only        |    360 |          2460 |  0.146341  |
| zeta_only                 |    327 |          2460 |  0.132927  |
| standard_ping             |    318 |          2460 |  0.129268  |
| full_reciprocal           |    312 |          2460 |  0.126829  |
| eta_only                  |    311 |          2460 |  0.126423  |
| colored_noise_alt         |    264 |          2460 |  0.107317  |
| null_no_coupling          |    257 |          2460 |  0.104472  |
| generic_hidden_oscillator |    172 |          2460 |  0.0699187 |
| replay_only_basis         |    139 |          2460 |  0.0565041 |

## Interpretation

The best interpretation is:

```text
Rung 0N repaired the empty-sky false-lock problem at the final decision layer.
The full reciprocal model cannot claim lock unless it both predicts held-out folds and crosses a null-calibrated K threshold.
```

The important epistemic improvement is that **full-model prediction alone is not enough**, and **K significance alone is not enough**. The claim requires their conjunction.

## Boundary

This remains synthetic sensitivity/specificity calibration only. It does not prove or disprove OSM, microtubular memory, biophotonic flickering, human EEG mechanism, or PR-AYC-G empirical results.

## Next gate

The next gate should be:

```text
Rung 0O - Locked Reproduction of Null-Aware Specificity Gate
```

Freeze the Rung 0N specification, rerun a fresh seed set without changing thresholds, penalties, alternatives, or report template, and then ask an independent verifier to run the unchanged package.
