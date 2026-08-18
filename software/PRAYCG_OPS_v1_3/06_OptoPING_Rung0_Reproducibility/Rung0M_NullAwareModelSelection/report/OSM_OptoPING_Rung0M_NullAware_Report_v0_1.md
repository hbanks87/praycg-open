# OSM / Opto-PING Rung 0M - Null-Aware Model Selection and K-Significance Calibration v0.1

**Overall status:** `PARTIAL_OR_FAILED_NULL_AWARE_SPECIFICITY`

Rung 0M requires two simultaneous gates: the full reciprocal model must win held-out prediction and K must be significant against trial-wise shuffled/time-reversed/null controls. Full-model prediction alone is not sufficient.

Spec SHA-256: `6e9be8fc28625ad63c851af513eb39195d321bef0865ccbe18311b0208e47659`

Total trials: 120 (20 positive, 100 null).

## Main result

{
  "full_and_K_lock_rate": 0.6,
  "K_significant_rate": 1.0,
  "K_within_15_rate": 1.0,
  "K_within_10_rate": 0.95,
  "full_model_cv_win_rate_mean": 0.5999999999999999,
  "median_K_hat_scaled": 1.0067475843453353
}

{
  "overall_false_full_and_K_lock_rate": 0.0,
  "overall_K_significant_rate": 0.35,
  "overall_full_model_cv_win_rate_mean": 0.06166666666666667,
  "overall_non_full_cv_win_rate_mean": 0.9383333333333332,
  "overall_median_K_hat_scaled": 0.06428735330498983,
  "overall_median_K_null_p": 0.5
}

## Generator summary

| generator                        |   n_trials |   K_true_scaled |   median_K_hat_scaled |   mean_K_hat_scaled |   K_within_15_positive_rate |   K_within_10_positive_rate |   K_significant_rate |   full_cv_win_rate_mean |   full_prediction_win_rate |   full_and_K_lock_rate |   non_full_cv_win_rate_mean |   median_K_null_p |
|:---------------------------------|-----------:|----------------:|----------------------:|--------------------:|----------------------------:|----------------------------:|---------------------:|------------------------:|---------------------------:|-----------------------:|----------------------------:|------------------:|
| colored_noise_null               |         20 |               0 |             0.788793  |           0.766869  |                           0 |                        0    |                 1    |               0.0583333 |                        0   |                    0   |                    0.941667 |              0.1  |
| full_reciprocal_positive_control |         20 |               1 |             1.00675   |           1.0117    |                           1 |                        0.95 |                 1    |               0.6       |                        0.6 |                    0.6 |                    0.4      |              0.1  |
| generic_hidden_oscillator_null   |         20 |               0 |             0.0543484 |           0.0549876 |                           0 |                        0    |                 0.1  |               0         |                        0   |                    0   |                    1        |              0.75 |
| replay_only_null                 |         20 |               0 |             0.0371716 |           0.0425212 |                           0 |                        0    |                 0.05 |               0.0416667 |                        0   |                    0   |                    0.958333 |              0.6  |
| sensory_drive_only_null          |         20 |               0 |             0.0732384 |           0.0788321 |                           0 |                        0    |                 0.35 |               0         |                        0   |                    0   |                    1        |              0.2  |
| standard_ping_null               |         20 |               0 |             0.0452772 |           0.0586128 |                           0 |                        0    |                 0.25 |               0.208333  |                        0.1 |                    0   |                    0.791667 |              0.6  |

## Decision table

| generator                        | criterion                  |   observed | threshold   | pass   |
|:---------------------------------|:---------------------------|-----------:|:------------|:-------|
| full_reciprocal_positive_control | full_and_K_lock_rate       |  0.6       | >= 0.8      | False  |
| full_reciprocal_positive_control | K_significant_rate         |  1         | >= 0.85     | True   |
| full_reciprocal_positive_control | full_cv_win_rate_mean      |  0.6       | >= 0.7      | False  |
| full_reciprocal_positive_control | K_within_15_positive_rate  |  1         | >= 0.8      | True   |
| standard_ping_null               | false_full_and_K_lock_rate |  0         | <= 0.05     | True   |
| standard_ping_null               | K_significant_rate         |  0.25      | <= 0.1      | False  |
| standard_ping_null               | full_cv_win_rate_mean      |  0.208333  | <= 0.35     | True   |
| replay_only_null                 | false_full_and_K_lock_rate |  0         | <= 0.05     | True   |
| replay_only_null                 | K_significant_rate         |  0.05      | <= 0.1      | True   |
| replay_only_null                 | full_cv_win_rate_mean      |  0.0416667 | <= 0.2      | True   |
| sensory_drive_only_null          | false_full_and_K_lock_rate |  0         | <= 0.05     | True   |
| sensory_drive_only_null          | K_significant_rate         |  0.35      | <= 0.1      | False  |
| sensory_drive_only_null          | full_cv_win_rate_mean      |  0         | <= 0.2      | True   |
| generic_hidden_oscillator_null   | false_full_and_K_lock_rate |  0         | <= 0.05     | True   |
| generic_hidden_oscillator_null   | K_significant_rate         |  0.1       | <= 0.1      | True   |
| generic_hidden_oscillator_null   | full_cv_win_rate_mean      |  0         | <= 0.25     | True   |
| colored_noise_null               | false_full_and_K_lock_rate |  0         | <= 0.05     | True   |
| colored_noise_null               | K_significant_rate         |  1         | <= 0.1      | False  |
| colored_noise_null               | full_cv_win_rate_mean      |  0.0583333 | <= 0.25     | True   |

## Boundary

Synthetic sensitivity/specificity calibration only; no biological, PR-AYC-G, human EEG, microtubular memory, biophotonic, or OSM mechanism claim.
