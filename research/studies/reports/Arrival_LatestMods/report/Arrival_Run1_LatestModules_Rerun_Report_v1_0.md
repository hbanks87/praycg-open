# Arrival Run 1 - Latest Master Suite Exploratory Rerun

**Status:** exploratory rerun from available processed Arrival tables. No new raw-XDF extraction was performed in this pass.

## Executive verdict

Arrival remains a strong *hypothesis-generating* PR-AYC-G run for recognition-versus-encoding dissociation. The latest modules do not convert it into a clean endpoint pass. The clearest retained pattern is: Target shows a NAST-style transition into narrative absorption and multiple conceptual anchors show Target-dominant immersion/recognition proxies, but CandidateLocal KHT-topo/BIT strict event-lock remains negative.

## Data basis and limitations

- Feature rows analyzed: 1378 across phases {'BASELINE_1': 115, 'CONTEXTUAL_OVERRIDE_1': 308, 'CONTROL_1': 308, 'TARGET_1': 308, 'WASHOUT_1': 114, 'WASHOUT_2': 114, 'WASHOUT_3': 111}.

- Available inputs: canonical processed feature frame, EEG-window feature table, prior CandidateLocal KHT cross-boundary table, prior NAST/OCM tables, cue schedule, self-report summary.

- Not available here: full v1.8 Arrival StimulusFingerprint regressors, raw EOG/eye tracking, and a runner-registered anchor file.

## Module registry

| module                           | status    | primary_table                                         | interpretation                                                                           | limitation                                                                    |
|:---------------------------------|:----------|:------------------------------------------------------|:-----------------------------------------------------------------------------------------|:------------------------------------------------------------------------------|
| TopoOSM_NetworkState             | completed | arrival_topo_osm_phase_state_vectors.csv              | Phase-state topology summarized across baselines/washouts/branches.                      | ROI metadata is channel-map-cautioned for Arrival.                            |
| CandidateLocal_KHT-topo / MRED   | completed | arrival_candidate_local_kht_topo_mred_event_table.csv | Cross-boundary CandidateLocal KHT reviewed; no strict event lock.                        | Uses prior processed feature tables; not raw-XDF re-extraction in this rerun. |
| MRED_v0.1                        | completed | arrival_nip_mred_component_timeseries.csv             | Recognition/encoding proxies computed continuously and by anchors.                       | Feature-derived proxy; no population inference.                               |
| NAST_v0.1                        | completed | arrival_nast_phase_transition_table.csv               | Arrival Target shows NAST-style WASHOUT1->TARGET transition from existing module.        | Uses prior NAST window feature table.                                         |
| OCM025 / RSM / CVB / SquintProxy | completed | arrival_ocm025_rsm_cvb_squint_cue_table.csv           | Override cue-update/working-memory burden reviewed; no clean OCM pass.                   | Uses prior OCM table; SquintProxy remains artifact proxy only.                |
| TTI_v0.1                         | completed | arrival_tti_global_summary.csv                        | Reception/extraction Target-vs-Override contrast computed.                               | Exploratory single-run construct, not moral/clinical score.                   |
| NIP/BIT/CII/IAQ_v0.1             | completed | arrival_cii_anchor_integrals.csv                      | Narrative immersion proxies computed over conceptual Arrival anchor windows.             | Anchors are conceptual/future-freeze, not runner-registered.                  |
| CET/EET_v0.1                     | partial   | arrival_cet_cue_residualization_model_summary.csv     | Cue-only cinematic entrainment residualization and state-vector echo analysis completed. | No v1.8 Arrival full media regressors available; full CET-R not possible.     |
| MRED-ITP / ACG / OCU_v0.1        | partial   | arrival_mred_itp_anchor_summary.csv                   | Feature-state complexity and blink-sentinel proxy analysis completed.                    | No raw XDF LZ / true EOG/eye tracker in this rerun; proxy only.               |

## Phase-state / Topo-OSM summary

| phase                 |   n_windows |   meaning_gamma_z |   tsp_z |   theta_primary_z |   task_gamma_z |   MR_score |   ENC_score |   NIP_density |
|:----------------------|------------:|------------------:|--------:|------------------:|---------------:|-----------:|------------:|--------------:|
| BASELINE_1            |         115 |            -0.471 |   0.152 |             0.124 |          0.601 |     -0.325 |      -0.082 |         0.004 |
| CONTEXTUAL_OVERRIDE_1 |         308 |            -0.889 |  -0.717 |             0.464 |          0.813 |     -0.738 |       0.142 |         0.004 |
| CONTROL_1             |         308 |             0.087 |  -0.169 |             0.050 |         -0.144 |     -0.129 |      -0.083 |         0.045 |
| TARGET_1              |         308 |             0.913 |   0.878 |             0.435 |         -0.699 |      0.461 |       0.146 |         0.272 |
| WASHOUT_1             |         114 |             0.076 |  -0.850 |            -0.115 |         -0.314 |     -0.365 |      -0.129 |         0.014 |
| WASHOUT_2             |         114 |             0.859 |   0.893 |             0.056 |         -0.556 |      0.523 |      -0.032 |         0.225 |
| WASHOUT_3             |         111 |            -0.771 |  -0.026 |             0.242 |          0.988 |     -0.468 |       0.031 |         0.005 |

## NAST - narrative absorption state transition

| transition                       |   delta_alpha_proxy_z |   delta_meaning_gamma_z |   delta_tsp_z |   delta_task_gamma_z |   delta_theta_primary_z | interpretation                                 |
|:---------------------------------|----------------------:|------------------------:|--------------:|---------------------:|------------------------:|:-----------------------------------------------|
| BASELINE_1->CONTROL_1            |                -0.108 |                   1.010 |         0.542 |               -0.884 |                   0.008 | alpha suppression + meaning/TSP rise candidate |
| WASHOUT_1->TARGET_1              |                -0.102 |                   0.600 |         1.434 |               -0.022 |                   0.020 | alpha suppression + meaning/TSP rise candidate |
| WASHOUT_2->CONTEXTUAL_OVERRIDE_1 |                 0.080 |                  -2.263 |        -0.874 |                2.542 |                   1.518 | no alpha-suppression transition                |


Interpretation: the retained NAST result is WASHOUT_1->TARGET with alpha suppression plus MeaningGamma/TSP rise. Override looks more like task-state reorientation, with TaskGamma/theta rising and MeaningGamma/TSP falling relative to WASHOUT_2.

## CandidateLocal KHT-topo / MRED event gate

- Strict cross-boundary CandidateLocal KHT event locks: 0 / 48 target-candidate rows.

| search_window   | predictor_name     |   peak_sec |   anchor_sec |   K_local |   K_local_percentile_by_phase |   delta_theta_0_10_vs_pre |   delta_theta_10_30_vs_pre | candidate_local_kht_event_lock_cross_boundary   | interpretation_cross_boundary   |
|:----------------|:-------------------|-----------:|-------------:|----------:|------------------------------:|--------------------------:|---------------------------:|:------------------------------------------------|:--------------------------------|
| second_half     | primary_gamma_z    |    310.000 |      310.000 |     2.273 |                       100.000 |                    -1.354 |                     -0.831 | False                                           | local_K_without_theta_handoff   |
| second_half     | primary_gamma_z    |    310.000 |      310.000 |     2.273 |                       100.000 |                    -0.762 |                     -0.739 | False                                           | local_K_without_theta_handoff   |
| second_half     | primary_gamma_z    |    310.000 |      310.000 |     2.273 |                       100.000 |                    -0.550 |                     -0.558 | False                                           | local_K_without_theta_handoff   |
| second_half     | primary_gamma_z    |    310.000 |      310.000 |     2.273 |                       100.000 |                    -0.575 |                     -0.436 | False                                           | local_K_without_theta_handoff   |
| whole_target    | meaninggamma_score |     68.000 |       91.000 |     0.649 |                        94.545 |                    -0.536 |                     -1.110 | False                                           | not_locked                      |
| whole_target    | meaninggamma_score |     68.000 |       91.000 |     0.649 |                        94.545 |                    -0.327 |                     -0.785 | False                                           | not_locked                      |
| whole_target    | meaninggamma_score |     68.000 |       91.000 |     0.649 |                        94.545 |                     0.257 |                      0.271 | False                                           | not_locked                      |
| whole_target    | meaninggamma_score |     68.000 |       91.000 |     0.649 |                        94.545 |                     0.242 |                      0.028 | False                                           | not_locked                      |


Interpretation: the late clip-edge primary-gamma event still appears as high local K but lacks theta handoff; earlier events show recognition/meaning structure but do not pass the combined K+theta+specificity lock.

## NIP/BIT/CII/IAQ - narrative immersion proxy

- Strict BIT passes: 0 / 5 conceptual anchors.

| anchor_id                              |   target_CII |   control_CII |   override_CII |   target_minus_control_CII |   target_minus_override_CII |   IAQ_target_vs_override | target_specific_CII   |
|:---------------------------------------|-------------:|--------------:|---------------:|---------------------------:|----------------------------:|-------------------------:|:----------------------|
| ARR_A1_FUTURE_TRAGEDY_ACCEPTANCE_068P0 |        0.346 |         0.007 |          0.000 |                      0.338 |                       0.346 |                    0.997 | True                  |
| ARR_A2_STARDUST_CRINGE_120P0           |        0.332 |         0.009 |          0.000 |                      0.323 |                       0.332 |                    0.997 | True                  |
| ARR_A3_READING_LETTERS_169P0           |        0.615 |         0.004 |          0.000 |                      0.611 |                       0.615 |                    0.998 | True                  |
| ARR_A4_CHILD_LIFE_MONTAGE_251P0        |        0.204 |         0.001 |          0.000 |                      0.203 |                       0.204 |                    0.995 | True                  |
| ARR_A5_HELD_BY_YOU_FINAL_310P0         |        0.022 |         0.000 |          0.000 |                      0.022 |                       0.022 |                    0.956 | True                  |


Interpretation: CII is target-dominant for some anchors but not a strict immersion/event-lock endpoint because CandidateLocal KHT/BIT remains negative and the anchors were not runner-registered.

## TTI - reception/extraction tradeoff

| run          |   TTI |   target_MR |   override_MR |   target_ENC |   override_ENC |   target_task_gamma |   override_task_gamma |   target_artifact |   override_artifact | interpretation                                                                                             |
|:-------------|------:|------------:|--------------:|-------------:|---------------:|--------------------:|----------------------:|------------------:|--------------------:|:-----------------------------------------------------------------------------------------------------------|
| Arrival_Run1 | 0.533 |       0.461 |        -0.738 |        0.146 |          0.142 |              -0.699 |                 0.813 |             1.206 |              -0.066 | positive means Target retained more reception/integration while Override carried more extraction/task load |


| anchor_id                              |   TTI_anchor |   target_MR |   override_MR |   target_ENC |   override_ENC |   target_task_gamma |   override_task_gamma |   IAQ_target_vs_override |
|:---------------------------------------|-------------:|------------:|--------------:|-------------:|---------------:|--------------------:|----------------------:|-------------------------:|
| ARR_A1_FUTURE_TRAGEDY_ACCEPTANCE_068P0 |        0.565 |       0.758 |        -0.567 |        0.020 |          0.222 |              -1.037 |                 0.378 |                    0.997 |
| ARR_A2_STARDUST_CRINGE_120P0           |        0.755 |       0.698 |        -0.768 |        0.223 |         -0.190 |              -1.057 |                 0.360 |                    0.997 |
| ARR_A3_READING_LETTERS_169P0           |        0.834 |       0.729 |        -0.664 |        0.565 |         -0.173 |              -0.939 |                 0.464 |                    0.998 |
| ARR_A4_CHILD_LIFE_MONTAGE_251P0        |        0.418 |       0.339 |        -0.782 |       -0.039 |          0.180 |              -1.406 |                 0.687 |                    0.995 |
| ARR_A5_HELD_BY_YOU_FINAL_310P0         |        0.127 |      -0.364 |        -0.919 |        0.165 |          0.216 |               1.028 |                 1.344 |                    0.956 |


Interpretation: TTI is mixed in Arrival. Override does show task-state behavior at the phase-transition level, but at specific anchors the target/override relationship is heterogeneous.

## OCM025/RSM/CVB/SquintProxy

- Override cues analyzed: 104. Cue-update events: 19.

| x                       | y                   |   spearman_rho |   p_value |   n |
|:------------------------|:--------------------|---------------:|----------:|----:|
| arithmetic_compute_load | compute_stall_score |          0.244 |     0.014 | 104 |
| arithmetic_compute_load | latent_guess_risk   |          0.558 |     0.000 | 104 |
| carry_required          | compute_stall_score |          0.056 |     0.579 | 104 |
| carry_required          | latent_guess_risk   |          0.234 |     0.018 | 104 |
| high_carry_load         | latent_guess_risk   |          0.255 |     0.010 | 104 |
| hard9_pattern           | compute_stall_score |          0.093 |     0.350 | 104 |
| hard9_pattern           | latent_guess_risk   |          0.137 |     0.169 | 104 |
| cue_visibility_burden   | latent_guess_risk   |          0.659 |     0.000 | 104 |

Top latent guess/compute burden candidates:

|   cue_index |   value |   running_sum |   prior_units_digit |   carry_required |   hard9_pattern |   digit_recognition_DR |   working_memory_update_WMU |   maintenance_MAINT |   compute_stall_score |   cue_visibility_burden |   latent_guess_risk |
|------------:|--------:|--------------:|--------------------:|-----------------:|----------------:|-----------------------:|----------------------------:|--------------------:|----------------------:|------------------------:|--------------------:|
|      55.000 |   9.000 |       306.000 |               7.000 |            1.000 |           1.000 |                 -0.342 |                       2.458 |               1.778 |                 3.434 |                   0.946 |               0.943 |
|      88.000 |   2.000 |       460.000 |               8.000 |            1.000 |           0.000 |                  0.929 |                       3.303 |               3.231 |                 4.895 |                   0.751 |               0.942 |
|      60.000 |  10.000 |       337.000 |               7.000 |            1.000 |           0.000 |                 -0.235 |                       1.921 |               2.428 |                 3.153 |                   0.891 |               0.925 |
|      48.000 |   9.000 |       265.000 |               6.000 |            1.000 |           0.000 |                 -0.464 |                       1.658 |               1.718 |                 2.554 |                   1.076 |               0.891 |
|      39.000 |  10.000 |       219.000 |               9.000 |            1.000 |           0.000 |                  0.228 |                       2.394 |               0.953 |                 2.779 |                   0.267 |               0.874 |
|      32.000 |   8.000 |       177.000 |               9.000 |            1.000 |           0.000 |                 -1.606 |                       0.836 |               1.066 |                 1.295 |                   1.581 |               0.859 |
|      98.000 |   2.000 |       509.000 |               7.000 |            0.000 |           0.000 |                 -0.863 |                       0.845 |               2.293 |                 1.957 |                   1.429 |               0.858 |
|      83.000 |   1.000 |       437.000 |               6.000 |            0.000 |           0.000 |                 -0.236 |                       1.332 |               2.116 |                 2.271 |                   0.989 |               0.833 |


Interpretation: Arrival does not show a clean Override-wide working-memory update signature; RSM remains a diagnostic layer rather than a positive task-pass layer here.

## CET/EET - cue-only entrainment and state echo

| phase                 |   train_r2 |   blocked_cv_r2 |   n | limitation                                                                           |
|:----------------------|-----------:|----------------:|----:|:-------------------------------------------------------------------------------------|
| CONTROL_1             |      0.005 |          -0.063 | 308 | cue-only CET; no full visual/audio/cut-rate regressors for Arrival in this workspace |
| TARGET_1              |      0.007 |          -0.050 | 308 | cue-only CET; no full visual/audio/cut-rate regressors for Arrival in this workspace |
| CONTEXTUAL_OVERRIDE_1 |      0.012 |          -0.005 | 308 | cue-only CET; no full visual/audio/cut-rate regressors for Arrival in this workspace |
| POOLED                |      0.002 |          -0.062 | 924 | cue-only CET; no full visual/audio/cut-rate regressors for Arrival in this workspace |

Cue-residualized CII by anchor:

| anchor_id                              | label                                                   |   start_sec |   end_sec |   control_cue_resid_CII |   target_cue_resid_CII |   override_cue_resid_CII |   target_minus_control_cue_resid_CII |   target_minus_override_cue_resid_CII | target_specific_after_cue_residualization   |
|:---------------------------------------|:--------------------------------------------------------|------------:|----------:|------------------------:|-----------------------:|-------------------------:|-------------------------------------:|--------------------------------------:|:--------------------------------------------|
| ARR_A1_FUTURE_TRAGEDY_ACCEPTANCE_068P0 | Future/tragedy acceptance line                          |      58.000 |    78.000 |                   0.008 |                  0.346 |                    0.000 |                                0.338 |                                 0.346 | True                                        |
| ARR_A2_STARDUST_CRINGE_120P0           | "Star dust" cringe / aversive semantic prediction error |     112.000 |   128.000 |                   0.008 |                  0.331 |                   -0.001 |                                0.323 |                                 0.332 | True                                        |
| ARR_A3_READING_LETTERS_169P0           | Mother teaches daughter letters                         |     156.000 |   176.000 |                   0.009 |                  0.621 |                    0.006 |                                0.611 |                                 0.615 | True                                        |
| ARR_A4_CHILD_LIFE_MONTAGE_251P0        | Child-life montage under tragic foreknowledge           |     240.000 |   265.000 |                   0.002 |                  0.204 |                    0.000 |                                0.203 |                                 0.204 | True                                        |
| ARR_A5_HELD_BY_YOU_FINAL_310P0         | Final embrace / held-by-you line                        |     300.000 |   313.000 |                   0.006 |                  0.028 |                    0.006 |                                0.022 |                                 0.022 | True                                        |

Top EET state-vector echo similarities:

| anchor_id                              | comparison_window   |   cosine_similarity |   euclidean_distance | claim_level                               |
|:---------------------------------------|:--------------------|--------------------:|---------------------:|:------------------------------------------|
| ARR_A5_HELD_BY_YOU_FINAL_310P0         | WASHOUT_3_first30   |               0.976 |                0.768 | state-vector echo proxy; not replay proof |
| ARR_A5_HELD_BY_YOU_FINAL_310P0         | BASELINE_1_all      |               0.940 |                0.859 | state-vector echo proxy; not replay proof |
| ARR_A1_FUTURE_TRAGEDY_ACCEPTANCE_068P0 | WASHOUT_2_all       |               0.929 |                1.171 | state-vector echo proxy; not replay proof |
| ARR_A5_HELD_BY_YOU_FINAL_310P0         | WASHOUT_3_all       |               0.893 |                0.972 | state-vector echo proxy; not replay proof |
| ARR_A4_CHILD_LIFE_MONTAGE_251P0        | WASHOUT_2_first30   |               0.878 |                2.056 | state-vector echo proxy; not replay proof |
| ARR_A2_STARDUST_CRINGE_120P0           | WASHOUT_2_all       |               0.870 |                1.456 | state-vector echo proxy; not replay proof |
| ARR_A3_READING_LETTERS_169P0           | WASHOUT_2_all       |               0.846 |                1.595 | state-vector echo proxy; not replay proof |
| ARR_A1_FUTURE_TRAGEDY_ACCEPTANCE_068P0 | WASHOUT_2_first30   |               0.842 |                1.466 | state-vector echo proxy; not replay proof |
| ARR_A4_CHILD_LIFE_MONTAGE_251P0        | WASHOUT_2_all       |               0.815 |                2.646 | state-vector echo proxy; not replay proof |
| ARR_A2_STARDUST_CRINGE_120P0           | WASHOUT_2_first30   |               0.778 |                1.772 | state-vector echo proxy; not replay proof |


Interpretation: cue-only CET does not represent full media-level CET-R. EET is a state-vector resemblance analysis, not proof of replay. Arrival lacks Baseline 2, so EET is limited to washouts and baseline/control/override comparisons.

## MRED-ITP - complexity and ocular proxy layer

| anchor_id                              |   C_strike |   C_settle |   complexity_settlement_index |   blink_suppression_proxy |   blink_release_proxy | ACG_feature_proxy_flag   | OCU_proxy_flag   | MRED_ITP_strict_pass   | claim_level                                            |
|:---------------------------------------|-----------:|-----------:|------------------------------:|--------------------------:|----------------------:|:-------------------------|:-----------------|:-----------------------|:-------------------------------------------------------|
| ARR_A1_FUTURE_TRAGEDY_ACCEPTANCE_068P0 |     -1.476 |     -1.075 |                        -0.401 |                         0 |                     0 | False                    | False            | False                  | feature-level proxy only; no raw LZ/true EOG available |
| ARR_A2_STARDUST_CRINGE_120P0           |     -0.948 |      0.248 |                        -1.197 |                         4 |                     0 | False                    | False            | False                  | feature-level proxy only; no raw LZ/true EOG available |
| ARR_A3_READING_LETTERS_169P0           |     -0.797 |      1.343 |                        -2.140 |                         1 |                     0 | False                    | False            | False                  | feature-level proxy only; no raw LZ/true EOG available |
| ARR_A4_CHILD_LIFE_MONTAGE_251P0        |      0.576 |     -0.178 |                         0.755 |                         2 |                     0 | True                     | False            | False                  | feature-level proxy only; no raw LZ/true EOG available |
| ARR_A5_HELD_BY_YOU_FINAL_310P0         |      0.854 |    nan     |                         0.854 |                        -1 |                    -2 | False                    | False            | False                  | feature-level proxy only; no raw LZ/true EOG available |


Interpretation: this pass used a feature-state complexity proxy and a blink-sentinel proxy. It is not raw EEG Lempel-Ziv complexity and not EOG-confirmed blink analysis. It should be treated as exploratory convergence/falsification only.

## Overall conclusion

The latest suite additions strengthen the interpretation that Arrival is not a clean KHT-topo endpoint but is valuable for model refinement. The run supports the MRED idea that semantic-affective recognition can occur without reliable theta-indexed integration, especially for familiar material. It also supports the need for runner-registered anchors, full stimulus-fingerprint regressors, and cleaner post-run familiarity/novelty covariates in future Arrival-like runs.

## Boundary

This analysis is exploratory. It does not prove OSM biology, microtubules, biophotons, consciousness, or literal thermodynamic entropy reduction. It estimates macroscopic proxy trajectories from existing processed PR-AYC-G tables.
