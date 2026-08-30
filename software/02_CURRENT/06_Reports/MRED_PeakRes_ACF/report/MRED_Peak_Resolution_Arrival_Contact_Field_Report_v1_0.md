# PRAYCG MRED-Peak and MRED-Resolution Analysis

Runs: Arrival Run 1, Contact Run 1, Field of Dreams Run 1.

## Executive verdict

- **Contact** is the cleanest current **MRED-Peak** case.
- **Field of Dreams** is the cleanest current **MRED-Resolution** case.
- **Arrival** remains recognition-dominant and theoretically useful, but does not pass strict peak or resolution endpoints with the available data.

## Run summary

| run     |   n_anchors |   strict_peak_passes |   peak_candidates_non_strict |   recognition_dominant_not_locked |   resolution_candidates |   afterstate_recovery_support_anchor_weak |   mean_peak_score |   max_peak_score | top_peak_anchor                      |   mean_resolution_score |   max_resolution_score | top_resolution_anchor                  |   RDI_resolutive_recovery | polarity_class                   |
|:--------|------------:|---------------------:|-----------------------------:|----------------------------------:|------------------------:|------------------------------------------:|------------------:|-----------------:|:-------------------------------------|------------------------:|-----------------------:|:---------------------------------------|--------------------------:|:---------------------------------|
| Arrival |           5 |                    0 |                            1 |                                 2 |                       0 |                                         0 |          0.519173 |         0.673475 | ARR_A3_READING_LETTERS_169P0         |                0.823965 |               0.87886  | ARR_A1_FUTURE_TRAGEDY_ACCEPTANCE_068P0 |                nan        | POLARITY_UNRESOLVED_NO_BASELINE2 |
| Contact |           5 |                    1 |                            3 |                                 1 |                       1 |                                         4 |          0.709249 |         0.89575  | CONTACT_A2_AVATAR_FATHER_RECOGNITION |                0.738501 |               0.789283 | CONTACT_A1_PENSACOLA_REALIZATION       |                  0.820079 | HIGH_LOAD_WITH_RECOVERY          |
| Field   |           7 |                    1 |                            0 |                                 1 |                       4 |                                         2 |          0.43982  |         0.684447 | FOD_BLIND_A6                         |                0.641757 |               0.745677 | FOD_BLIND_A6                           |                  0.711288 | RESOLUTIVE_RECOVERY              |

## Top MRED-Peak candidates

| run     | anchor_id                                                    |   time_sec |   MRED_peak_score | MRED_peak_gate                       |   target_MR |   target_ENC |   CII_margin_min | strict_peak_source      |
|:--------|:-------------------------------------------------------------|-----------:|------------------:|:-------------------------------------|------------:|-------------:|-----------------:|:------------------------|
| Contact | CONTACT_A2_AVATAR_FATHER_RECOGNITION                         |   161.007  |          0.89575  | STRICT_PEAK_PASS                     |    1.21576  |    1.98372   |        1.64954   | BIT_pass_praycg_strict  |
| Contact | CONTACT_A2B_AVATAR_FATHER_RECOGNITION_TSP_CLUSTER            |   166.007  |          0.768147 | PEAK_CANDIDATE_NO_STRICT_LOCK        |    1.22033  |    1.47787   |        1.18762   | none                    |
| Field   | FOD_BLIND_A6                                                 |   150      |          0.684447 | STRICT_PEAK_PASS_TIMING_CAUTION      |    1.19686  |    0.372768  |        0.148085  | field_amred_A_MRED_pass |
| Arrival | ARR_A3_READING_LETTERS_169P0                                 |   169      |          0.673475 | PEAK_CANDIDATE_NO_STRICT_LOCK        |    0.728509 |    0.565323  |        0.611151  | none                    |
| Contact | CONTACT_A3_EXISTENTIAL_PAYLOAD_ONSET                         |   263.007  |          0.65776  | PEAK_CANDIDATE_NO_STRICT_LOCK        |    1.00855  |    0.63207   |        0.595975  | none                    |
| Contact | CONTACT_A4_SMALL_MOVES_TAPER_RELEASE_OR_LATE_PAYLOAD_RELEASE |   271.007  |          0.657013 | PEAK_CANDIDATE_NO_STRICT_LOCK        |    1.01906  |    0.618226  |        0.593641  | none                    |
| Arrival | ARR_A2_STARDUST_CRINGE_120P0                                 |   120      |          0.589957 | RECOGNITION_DOMINANT_NOT_PEAK_LOCKED |    0.697655 |    0.222628  |        0.323431  | none                    |
| Contact | CONTACT_A1_PENSACOLA_REALIZATION                             |    28.0074 |          0.567576 | RECOGNITION_DOMINANT_NOT_PEAK_LOCKED |    1.07665  |    0.332     |        0.310976  | none                    |
| Arrival | ARR_A1_FUTURE_TRAGEDY_ACCEPTANCE_068P0                       |    68      |          0.524817 | RECOGNITION_DOMINANT_NOT_PEAK_LOCKED |    0.757794 |    0.0198573 |        0.338332  | none                    |
| Field   | FOD_BLIND_A4                                                 |   100      |          0.479228 | NO_PEAK_EVIDENCE                     |    0.371972 |    0.665803  |        0.0436977 | none                    |

## Top MRED-Resolution candidates

| run     | anchor_id                                                    |   time_sec |   MRED_resolution_score | MRED_resolution_gate                        |   RDI_resolutive_recovery |   afterstate_echo_max |   anchor_NUPI_proxy |   target_MR |
|:--------|:-------------------------------------------------------------|-----------:|------------------------:|:--------------------------------------------|--------------------------:|----------------------:|--------------------:|------------:|
| Arrival | ARR_A1_FUTURE_TRAGEDY_ACCEPTANCE_068P0                       |    68      |                0.87886  | NOT_GRADED_NO_BASELINE2_PROXY_ONLY          |                nan        |              0.9293   |          0.734692   |    0.757794 |
| Arrival | ARR_A4_CHILD_LIFE_MONTAGE_251P0                              |   251      |                0.84293  | NOT_GRADED_NO_BASELINE2_PROXY_ONLY          |                nan        |              0.878264 |          0.597864   |    0.339475 |
| Arrival | ARR_A2_STARDUST_CRINGE_120P0                                 |   120      |                0.811405 | NOT_GRADED_NO_BASELINE2_PROXY_ONLY          |                nan        |              0.870211 |          0.202113   |    0.697655 |
| Arrival | ARR_A5_HELD_BY_YOU_FINAL_310P0                               |   310      |                0.800456 | NOT_GRADED_NO_BASELINE2_PROXY_ONLY          |                nan        |              0.976142 |          0.211025   |   -0.363892 |
| Contact | CONTACT_A1_PENSACOLA_REALIZATION                             |    28.0074 |                0.789283 | RESOLUTION_COMPONENT_WITH_HIGH_LOAD_PROFILE |                  0.820079 |              0.957443 |          0.259235   |    1.07665  |
| Arrival | ARR_A3_READING_LETTERS_169P0                                 |   169      |                0.786173 | NOT_GRADED_NO_BASELINE2_PROXY_ONLY          |                nan        |              0.845908 |          0.0617968  |    0.728509 |
| Contact | CONTACT_A4_SMALL_MOVES_TAPER_RELEASE_OR_LATE_PAYLOAD_RELEASE |   271.007  |                0.762382 | AFTERSTATE_RECOVERY_SUPPORT_BUT_ANCHOR_WEAK |                  0.820079 |              0.830031 |          0.177872   |    1.01906  |
| Field   | FOD_BLIND_A6                                                 |   150      |                0.745677 | RESOLUTION_CANDIDATE                        |                  0.711288 |              0.924817 |          0.406002   |    1.19686  |
| Contact | CONTACT_A2B_AVATAR_FATHER_RECOGNITION_TSP_CLUSTER            |   166.007  |                0.726108 | AFTERSTATE_RECOVERY_SUPPORT_BUT_ANCHOR_WEAK |                  0.820079 |              0.785542 |         -0.00714275 |    1.22033  |
| Contact | CONTACT_A3_EXISTENTIAL_PAYLOAD_ONSET                         |   263.007  |                0.719558 | AFTERSTATE_RECOVERY_SUPPORT_BUT_ANCHOR_WEAK |                  0.820079 |              0.732975 |          0.0976026  |    1.00855  |

## Interpretation

**Arrival:** Target-dominant recognition/immersion screens appear at conceptual anchors, especially the reading-letters anchor, but no strict event lock is present. Resolution is not graded because the older run lacks a PRAYCG2.0 final-reflection Baseline2 layer.

**Contact:** the father/avatar region remains the strongest MRED-Peak result. It has strict BIT support, high Target MR, high Target ENC, and high Target-specific CII. Its after-state is positive, but the best label is high-load-with-recovery rather than pure resolution.

**Field of Dreams:** one runner-time A-MRED peak pass remains timing-cautioned. Its strongest result is MRED-Resolution: Target-favoring self-report, Baseline2/recovery context, and NUPI resolution profile.

## Boundary
MRED-Peak and MRED-Resolution are endpoint-compression profiles. They do not prove memory formation, consciousness, OSM biology, or literal thermodynamic entropy reduction. Strict confirmation requires frame-verified locked anchors, clean ALS timing, artifact/CET-R gates, and replication.