# Contact Run 1 - MRED-ITP / ACG / OCU Deep Analysis v1.0

## Executive verdict
The new information-thermodynamic proxy layer is useful but should remain exploratory. Contact shows some Target-aligned information-structure and ocular-release candidates, but the result is not a literal thermodynamic proof. Lempel-Ziv complexity is treated as a compressibility/diversity proxy, and Fp1 blink timing is treated as a rough ocular event-boundary proxy, not confirmed memory encoding.

## Boundary
Information-thermodynamic proxy layer only. LZC is not literal thermodynamic entropy; Fp1 blink timing is not proof of memory encoding. No OSM biology or human EEG mechanism claim.

## Data and streams
EEG stream `obci_eeg1`: 270000 samples, 16 channels, nominal 125.0 Hz.
Blink-proxy events detected from Fp1: 157 total.

## Phase-level complexity/blink summary
| phase                 |   duration_sec |   mean_lz_complexity_proxy |   blink_count |   blink_rate_per_min |
|:----------------------|---------------:|---------------------------:|--------------:|---------------------:|
| CONTROL_1             |        303.050 |                      0.911 |             7 |                1.386 |
| TARGET_1              |        300.505 |                      0.936 |             3 |                0.599 |
| CONTEXTUAL_OVERRIDE_1 |        300.440 |                      0.891 |             5 |                0.999 |
| BASELINE_1            |        120.003 |                      0.890 |            31 |               15.500 |
| WASHOUT_1             |        120.003 |                      0.921 |             3 |                1.500 |
| WASHOUT_2             |        120.004 |                      0.938 |             1 |                0.500 |
| WASHOUT_3             |        120.002 |                      0.910 |             7 |                3.500 |
| BASELINE_2_REFLECTION |        120.003 |                      0.916 |             2 |                1.000 |

## Target anchor-level candidates
| anchor_id                                                    | scene_label                                  |   delta_C_strike_peak_minus_pre |   delta_C_settle_post_minus_peak |   CSI_complexity_settlement_index |   blink_suppression_pre_minus_hold |   blink_release_release_minus_hold |   ORI_ocular_release_index |   MRED_ITP_convergence_score | ACG_candidate   | OCU_candidate   | MRED_ITP_candidate   | nearest_mred_quadrant   |
|:-------------------------------------------------------------|:---------------------------------------------|--------------------------------:|---------------------------------:|----------------------------------:|-----------------------------------:|-----------------------------------:|---------------------------:|-----------------------------:|:----------------|:----------------|:---------------------|:------------------------|
| CONTACT_A2B_AVATAR_FATHER_RECOGNITION_TSP_CLUSTER            | Father/avatar recognition TSP follow-through |                           0.016 |                           -0.028 |                             1.224 |                              0.000 |                              4.000 |                     -0.037 |                        0.694 | False           | False           | False                | MR_HIGH_ENC_LOW         |
| CONTACT_A1_PENSACOLA_REALIZATION                             | Pensacola realization                        |                          -0.003 |                           -0.002 |                            -0.597 |                              4.800 |                              0.000 |                      0.461 |                        0.080 | False           | False           | False                | MR_HIGH_ENC_LOW         |
| CONTACT_A4_SMALL_MOVES_TAPER_RELEASE_OR_LATE_PAYLOAD_RELEASE | Late payload / terminal release              |                           0.002 |                           -0.007 |                            -0.081 |                              0.000 |                              0.000 |                      0.000 |                        0.040 | False           | False           | False                | MR_HIGH_ENC_LOW         |
| CONTACT_A2_AVATAR_FATHER_RECOGNITION                         | Father/avatar recognition                    |                           0.009 |                           -0.021 |                             0.596 |                              0.000 |                              0.000 |                     -0.563 |                        0.016 | False           | False           | False                | MR_HIGH_ENC_HIGH        |
| CONTACT_A3_EXISTENTIAL_PAYLOAD_ONSET                         | Existential payload onset                    |                          -0.009 |                            0.011 |                            -1.375 |                              0.000 |                              0.000 |                      0.000 |                       -0.633 | False           | False           | False                | MR_HIGH_ENC_HIGH        |

## Condition specificity
| anchor_id                                                    | scene_label                                  |   Target_minus_Control_CSI_complexity_settlement_index |   Target_minus_Override_CSI_complexity_settlement_index |   Target_minus_Control_ORI_ocular_release_index |   Target_minus_Override_ORI_ocular_release_index |   Target_minus_Control_MRED_ITP_convergence_score |   Target_minus_Override_MRED_ITP_convergence_score |
|:-------------------------------------------------------------|:---------------------------------------------|-------------------------------------------------------:|--------------------------------------------------------:|------------------------------------------------:|-------------------------------------------------:|--------------------------------------------------:|---------------------------------------------------:|
| CONTACT_A1_PENSACOLA_REALIZATION                             | Pensacola realization                        |                                                  5.665 |                                                  -1.068 |                                           3.219 |                                            0.075 |                                             5.101 |                                             -0.505 |
| CONTACT_A2_AVATAR_FATHER_RECOGNITION                         | Father/avatar recognition                    |                                                  0.475 |                                                   1.058 |                                          -0.010 |                                            1.037 |                                             0.240 |                                              1.244 |
| CONTACT_A2B_AVATAR_FATHER_RECOGNITION_TSP_CLUSTER            | Father/avatar recognition TSP follow-through |                                                  1.334 |                                                   2.137 |                                           0.504 |                                            1.562 |                                             1.031 |                                              2.157 |
| CONTACT_A3_EXISTENTIAL_PAYLOAD_ONSET                         | Existential payload onset                    |                                                 -3.854 |                                                  -0.135 |                                          -1.169 |                                            0.000 |                                            -2.787 |                                             -0.070 |
| CONTACT_A4_SMALL_MOVES_TAPER_RELEASE_OR_LATE_PAYLOAD_RELEASE | Late payload / terminal release              |                                                  0.299 |                                                  -0.620 |                                           0.984 |                                            0.000 |                                             0.813 |                                             -0.322 |

## Interpretation
- ACG asks whether anchor windows show a complexity perturbation followed by settlement. It does not estimate thermodynamic entropy directly.
- OCU asks whether blinks are suppressed near the meaningful window and released afterward. It is a blink-timing proxy; without EOG/eye tracking it remains tentative.
- MRED-ITP convergence is strongest when complexity settlement and ocular release both align with MRED/KHT-topo target events and show Target > Control/Override specificity.
- The Contact father/avatar recognition cluster remains the most important target candidate from prior modules; this new layer adds supportive/diagnostic context rather than replacing MRED, NIP, or TTI.

## Strongest caution
The Fp1 channel is simultaneously a useful blink/ocular proxy and a possible EEG artifact source. Any blink-timed event must be treated as an ocular state marker, not as clean neural theta/gamma evidence in the same contaminated samples.