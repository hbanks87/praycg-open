# Contact Run 1 - NIP / BIT / CII / IAQ / CET-EET Deep Analysis v1.0

## Boundary

This analysis operationalizes a macroscopic PR-AYC-G narrative immersion proxy. It does not measure dopamine, oxytocin, microtubules, biophotons, OSM biology, consciousness, or hidden cellular Y. CET/EET outputs are exploratory and depend on available media/proxy regressors.

## Executive summary

- Mean NIP density: Target 0.551, Control 0.028, Override 0.016.

- Strict BIT passes: 1. The strict pass occurred at Target ~161 s for the MeaningGamma father/avatar recognition event.

- CII/IAQ: Target exceeded both Control and Override for 5 / 5 conceptual Contact anchors.

- CET cue tracking was weak at the 1 Hz feature-table resolution; the strongest available target visual proxy correlations were moderate and came from the uploaded visualizer MP4, not the raw stimulus media.

- CET-R residualization explained little of the NIP variance, and the Target anchor CII pattern remained positive after available exogenous regressors were modeled.

- EET shows state-vector resemblance between target anchor geometry and washout/Baseline 2, but this is not proof of replay or memory.


## NIP/BIT/CII/IAQ results

| anchor_id                                                    | scene_label                                  |   CII_Target |   CII_Control |   CII_Override |   Target_minus_Control_CII |   Target_minus_Override_CII |   IAQ_Target_vs_Override | Target_greater_Control   | Target_greater_Override   |
|:-------------------------------------------------------------|:---------------------------------------------|-------------:|--------------:|---------------:|---------------------------:|----------------------------:|-------------------------:|:-------------------------|:--------------------------|
| CONTACT_A1_PENSACOLA_REALIZATION                             | Pensacola realization                        |     0.379446 |    0          |    0.0684702   |                   0.379446 |                    0.310976 |                 0.81955  | True                     | True                      |
| CONTACT_A2B_AVATAR_FATHER_RECOGNITION_TSP_CLUSTER            | Father/avatar recognition TSP follow-through |     1.19103  |    0.0010894  |    0.0034025   |                   1.18994  |                    1.18762  |                 0.997142 | True                     | True                      |
| CONTACT_A2_AVATAR_FATHER_RECOGNITION                         | Father/avatar recognition                    |     1.65165  |    0.00183342 |    0.00211477  |                   1.64982  |                    1.64954  |                 0.998719 | True                     | True                      |
| CONTACT_A3_EXISTENTIAL_PAYLOAD_ONSET                         | Existential payload onset                    |     0.633088 |    0.0154369  |    0.0371133   |                   0.617651 |                    0.595975 |                 0.941376 | True                     | True                      |
| CONTACT_A4_SMALL_MOVES_TAPER_RELEASE_OR_LATE_PAYLOAD_RELEASE | Late payload / terminal release              |     0.611488 |    0.0178471  |    0.000840012 |                   0.593641 |                    0.610648 |                 0.998625 | True                     | True                      |


## BIT strict events

| condition   |   condition_offset_sec | anchor_metric      |   K_HT_topo_local |   theta_delta_10_30 | mred_quadrant    | BIT_pass_praycg_strict   |
|:------------|-----------------------:|:-------------------|------------------:|--------------------:|:-----------------|:-------------------------|
| TARGET_1    |                161.007 | meaninggamma_score |           4.37505 |             2.17106 | MR_HIGH_ENC_HIGH | True                     |


## CET cue-tracking summary

| condition             | stimulus_regressor   | signal               |   max_abs_corr |   lag_sec_signal_after_regressor |   signal_dominant_freq_hz |   signal_dominant_power |   cue_frequency_hz |
|:----------------------|:---------------------|:---------------------|---------------:|---------------------------------:|--------------------------:|------------------------:|-------------------:|
| CONTROL_1             | cue_on_3s            | meaninggamma_score   |     -0.0695401 |                                2 |                 0.046875  |              0.444267   |           0.333333 |
| CONTROL_1             | cue_on_3s            | tsp_z                |     -0.0789785 |                                2 |                 0.046875  |              0.313818   |           0.333333 |
| CONTROL_1             | cue_on_3s            | taskgamma_score      |     -0.0445574 |                               10 |                 0.078125  |             10.5872     |           0.333333 |
| CONTROL_1             | cue_on_3s            | theta_integration_z  |     -0.0563083 |                               -8 |                 0.0546875 |             87.4253     |           0.333333 |
| CONTROL_1             | cue_on_3s            | gamma_visual_30_45_z |     -0.0547634 |                               10 |                 0.09375   |             11.2292     |           0.333333 |
| CONTROL_1             | cue_on_3s            | gamma_front_35_40_z  |     -0.0506658 |                               10 |                 0.078125  |             14.2359     |           0.333333 |
| CONTROL_1             | cue_on_3s            | nas_score            |      0.0532945 |                               -8 |                 0.09375   |              7.30447    |           0.333333 |
| CONTROL_1             | cue_on_3s            | NIP_density          |      0.0403955 |                                0 |                 0.0234375 |              0.0427463  |           0.333333 |
| TARGET_1              | cue_on_3s            | meaninggamma_score   |     -0.0311666 |                                8 |                 0.0234375 |              3.96411    |           0.333333 |
| TARGET_1              | cue_on_3s            | tsp_z                |     -0.0218982 |                                3 |                 0.0234375 |              3.35891    |           0.333333 |
| TARGET_1              | cue_on_3s            | taskgamma_score      |     -0.0616333 |                               -1 |                 0.0390625 |             12.723      |           0.333333 |
| TARGET_1              | cue_on_3s            | theta_integration_z  |      0.0316296 |                               10 |                 0.109375  |            130.193      |           0.333333 |
| TARGET_1              | cue_on_3s            | gamma_visual_30_45_z |     -0.0614053 |                               -1 |                 0.0625    |             23.7721     |           0.333333 |
| TARGET_1              | cue_on_3s            | gamma_front_35_40_z  |     -0.062788  |                               -1 |                 0.0390625 |             16.8114     |           0.333333 |
| TARGET_1              | cue_on_3s            | nas_score            |      0.049858  |                               -1 |                 0.109375  |             15.4956     |           0.333333 |
| TARGET_1              | cue_on_3s            | NIP_density          |     -0.0147779 |                              -10 |                 0.0234375 |              9.62065    |           0.333333 |
| CONTEXTUAL_OVERRIDE_1 | cue_on_3s            | meaninggamma_score   |     -0.0299108 |                                0 |                 0.03125   |              0.886796   |           0.333333 |
| CONTEXTUAL_OVERRIDE_1 | cue_on_3s            | tsp_z                |     -0.0314061 |                                3 |                 0.03125   |              0.858491   |           0.333333 |
| CONTEXTUAL_OVERRIDE_1 | cue_on_3s            | taskgamma_score      |     -0.0768704 |                                0 |                 0.0390625 |              5.04299    |           0.333333 |
| CONTEXTUAL_OVERRIDE_1 | cue_on_3s            | theta_integration_z  |     -0.0387839 |                                9 |                 0.046875  |             12.0698     |           0.333333 |
| CONTEXTUAL_OVERRIDE_1 | cue_on_3s            | gamma_visual_30_45_z |     -0.0697491 |                                1 |                 0.0390625 |              2.24285    |           0.333333 |
| CONTEXTUAL_OVERRIDE_1 | cue_on_3s            | gamma_front_35_40_z  |     -0.0761628 |                                0 |                 0.0234375 |              6.30721    |           0.333333 |
| CONTEXTUAL_OVERRIDE_1 | cue_on_3s            | nas_score            |      0.0344334 |                                0 |                 0.046875  |              1.5733     |           0.333333 |
| CONTEXTUAL_OVERRIDE_1 | cue_on_3s            | NIP_density          |     -0.0491472 |                               -8 |                 0.0234375 |              0.00659967 |           0.333333 |


## CET residualization summary

| condition             | dependent   | regressors                                                          |   n_rows |   r2_exogenous_tracking | beta_json                                                                                                                           |
|:----------------------|:------------|:--------------------------------------------------------------------|---------:|------------------------:|:------------------------------------------------------------------------------------------------------------------------------------|
| CONTROL_1             | NIP_density | cue_on+cue_phase_sin+cue_phase_cos                                  |      303 |              0.00182288 | [0.01838046758395039, 0.03040384209303229, -0.011090929435736016, -0.004453993675176115]                                            |
| TARGET_1              | NIP_density | cue_on+cue_phase_sin+cue_phase_cos+video_luminance_z+video_change_z |      301 |              0.0582325  | [0.43954211152359435, 0.4298195450794535, -0.27420614792658315, -0.005395256905657875, -0.17410326070576057, -0.010972614828596215] |
| CONTEXTUAL_OVERRIDE_1 | NIP_density | cue_on+cue_phase_sin+cue_phase_cos                                  |      300 |              0.00300116 | [0.010243096668948262, 0.01673198795409463, -0.010179717864258333, 0.003912311801023089]                                            |


## EET top echo similarities

| anchor_id                                                    | reference_window   |   cosine_similarity |   euclidean_distance |
|:-------------------------------------------------------------|:-------------------|--------------------:|---------------------:|
| CONTACT_A1_PENSACOLA_REALIZATION                             | WASHOUT_2_first60  |            0.957443 |              1.24533 |
| CONTACT_A1_PENSACOLA_REALIZATION                             | WASHOUT_2_first45  |            0.92968  |              1.22841 |
| CONTACT_A1_PENSACOLA_REALIZATION                             | WASHOUT_2_first30  |            0.923481 |              1.13742 |
| CONTACT_A4_SMALL_MOVES_TAPER_RELEASE_OR_LATE_PAYLOAD_RELEASE | BASELINE_2_all     |            0.830495 |              2.1346  |
| CONTACT_A4_SMALL_MOVES_TAPER_RELEASE_OR_LATE_PAYLOAD_RELEASE | WASHOUT_2_first60  |            0.830031 |              2.61286 |
| CONTACT_A4_SMALL_MOVES_TAPER_RELEASE_OR_LATE_PAYLOAD_RELEASE | WASHOUT_2_first30  |            0.824711 |              2.40475 |
| CONTACT_A2B_AVATAR_FATHER_RECOGNITION_TSP_CLUSTER            | BASELINE_2_all     |            0.817698 |              2.64434 |
| CONTACT_A4_SMALL_MOVES_TAPER_RELEASE_OR_LATE_PAYLOAD_RELEASE | WASHOUT_2_first45  |            0.791257 |              2.61686 |
| CONTACT_A2B_AVATAR_FATHER_RECOGNITION_TSP_CLUSTER            | WASHOUT_2_first30  |            0.785542 |              3.1622  |
| CONTACT_A1_PENSACOLA_REALIZATION                             | BASELINE_2_all     |            0.754639 |              2.17608 |