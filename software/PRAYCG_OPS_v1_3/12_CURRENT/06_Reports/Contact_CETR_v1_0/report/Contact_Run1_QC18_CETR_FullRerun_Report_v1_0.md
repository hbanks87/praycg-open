# Contact Run 1 - QC v1.8 / Full CET-R Exploratory Rerun

Created UTC: 2026-08-17T03:43:10.750468+00:00

## Executive verdict

The Contact QC rerun succeeded. Unlike the earlier partial v1.7B pass, the uploaded v1.8 QC package contains Control, Target, and Override exogenous regressor files, and the branch status table reports PASS for all three branches with an empty error log.

Exploratory CET-R result: the full v1.8 stimulus-side regressors do **not** explain away the Contact Target-dominant NIP/CII pattern. The Target remains greater than both Control and Override across every conceptual Contact anchor after pooled full-exogenous residualization.

Boundary: this is exploratory exogenous-regressor residualization. It is not a confirmatory endpoint, not OSM biology, and not proof of hidden-Y. The Contact anchors remain conceptually predeclared but not runner-registered for the original Contact acquisition.

## QC package status

- StimulusFingerprint schema: `PRAYCG_StimulusFingerprint_CET_EET_v1_8`
- Version: `1.8`
- Overall status: `PASS`
- Cue count: `99`
- Anchor count in uploaded QC manifest: `0`
- Merge rate: `4.0` Hz
- Branch errors: `0`

### Branch metrics
| condition   | status   | sha256_12    |   duration_sec |   cut_count |   cut_rate_per_sec |   flash_event_count |   audio_rms_mean |   dbfs_mean |   cue_count |   min_cue_contrast |
|:------------|:---------|:-------------|---------------:|------------:|-------------------:|--------------------:|-----------------:|------------:|------------:|-------------------:|
| control     | PASS     | 35b99e132076 |       299.9666 |          23 |             0.0767 |                  68 |           0.0113 |    -42.5192 |          99 |             0.9998 |
| target      | PASS     | 14ea5e719dfe |       299.9666 |          33 |             0.1100 |                  26 |           0.0150 |    -40.5459 |          99 |             0.9998 |
| override    | PASS     | 14ea5e719dfe |       299.9666 |          33 |             0.1100 |                  26 |           0.0150 |    -40.5459 |          99 |             0.9998 |

## Model summary

Ridge models were used as exploratory residualization models. Train R2 is in-sample and can overstate explanatory power; blocked-CV R2 is included as a stricter diagnostic. Negative blocked-CV R2 means the exogenous model did not predict held-out time blocks better than a mean-only model.

| scope    | model          |   n_rows |   n_features |   train_r2 |   blocked_cv_r2 |
|:---------|:---------------|---------:|-------------:|-----------:|----------------:|
| pooled   | cue_only       |      904 |            4 |     0.0031 |         -0.2018 |
| pooled   | visual_only    |      904 |            7 |     0.0197 |         -0.2532 |
| pooled   | audio_only     |      904 |            2 |     0.0000 |         -0.2025 |
| pooled   | full_exogenous |      904 |           13 |     0.0237 |         -0.2608 |
| control  | cue_only       |      303 |            4 |     0.0138 |         -0.0624 |
| control  | visual_only    |      303 |            6 |     0.0256 |         -0.1006 |
| control  | audio_only     |      303 |            2 |     0.0044 |         -0.0619 |
| control  | full_exogenous |      303 |           12 |     0.0405 |         -0.1205 |
| target   | cue_only       |      301 |            4 |     0.0153 |         -0.1647 |
| target   | visual_only    |      301 |            7 |     0.0699 |         -0.1753 |
| target   | audio_only     |      301 |            2 |     0.0006 |         -0.1860 |
| target   | full_exogenous |      301 |           13 |     0.0874 |         -0.2352 |
| override | cue_only       |      300 |            4 |     0.0125 |         -0.1481 |
| override | visual_only    |      300 |            6 |     0.0992 |         -0.1790 |
| override | audio_only     |      300 |            2 |     0.0203 |         -0.1509 |
| override | full_exogenous |      300 |           12 |     0.1227 |         -0.2027 |

### Full-exogenous model interpretation

- `pooled` full-exogenous model: train R2=0.024; blocked-CV R2=-0.261.
- `control` full-exogenous model: train R2=0.041; blocked-CV R2=-0.120.
- `target` full-exogenous model: train R2=0.087; blocked-CV R2=-0.235.
- `override` full-exogenous model: train R2=0.123; blocked-CV R2=-0.203.

The cue-only, visual-only, audio-only, and full models explain only limited variance in NIP density, especially under blocked-CV. This supports the narrow conclusion that the available stimulus regressors are not sufficient to account for the Target NIP/CII pattern.

## Anchor-level residualized CII

The table below uses `pooled_full_exog_resid_density_mean`: NIP density after subtracting the pooled full-exogenous prediction and adding back the global mean for readability. It should be read as an exploratory residualized scene score, not as a new physiological endpoint.

| anchor_id                                                    | scene_label                                  |   target |   control |   override |   target_minus_control |   target_minus_override | target_greater_control   | target_greater_override   |
|:-------------------------------------------------------------|:---------------------------------------------|---------:|----------:|-----------:|-----------------------:|------------------------:|:-------------------------|:--------------------------|
| CONTACT_A1_PENSACOLA_REALIZATION                             | Pensacola realization                        |   0.4455 |    0.0770 |     0.1446 |                 0.3686 |                  0.3009 | True                     | True                      |
| CONTACT_A2_AVATAR_FATHER_RECOGNITION                         | Father/avatar recognition                    |   1.5724 |   -0.0246 |    -0.0772 |                 1.5970 |                  1.6495 | True                     | True                      |
| CONTACT_A2B_AVATAR_FATHER_RECOGNITION_TSP_CLUSTER            | Father/avatar recognition TSP follow-through |   1.1323 |   -0.0049 |    -0.0553 |                 1.1372 |                  1.1876 | True                     | True                      |
| CONTACT_A3_EXISTENTIAL_PAYLOAD_ONSET                         | Existential payload onset                    |   1.0022 |    0.0239 |     0.0108 |                 0.9784 |                  0.9914 | True                     | True                      |
| CONTACT_A4_SMALL_MOVES_TAPER_RELEASE_OR_LATE_PAYLOAD_RELEASE | Late payload / terminal release              |   0.8111 |    0.0316 |     0.0221 |                 0.7795 |                  0.7890 | True                     | True                      |

For comparison, the original unresidualized CII pattern is:

| anchor_id                                                    | scene_label                                  |   target |   control |   override |   target_minus_control |   target_minus_override | target_greater_control   | target_greater_override   |
|:-------------------------------------------------------------|:---------------------------------------------|---------:|----------:|-----------:|-----------------------:|------------------------:|:-------------------------|:--------------------------|
| CONTACT_A1_PENSACOLA_REALIZATION                             | Pensacola realization                        |   0.3794 |    0.0000 |     0.0785 |                 0.3794 |                  0.3009 | True                     | True                      |
| CONTACT_A2_AVATAR_FATHER_RECOGNITION                         | Father/avatar recognition                    |   1.6517 |    0.0019 |     0.0021 |                 1.6497 |                  1.6495 | True                     | True                      |
| CONTACT_A2B_AVATAR_FATHER_RECOGNITION_TSP_CLUSTER            | Father/avatar recognition TSP follow-through |   1.1910 |    0.0012 |     0.0034 |                 1.1898 |                  1.1876 | True                     | True                      |
| CONTACT_A3_EXISTENTIAL_PAYLOAD_ONSET                         | Existential payload onset                    |   0.9926 |    0.0052 |     0.0012 |                 0.9874 |                  0.9914 | True                     | True                      |
| CONTACT_A4_SMALL_MOVES_TAPER_RELEASE_OR_LATE_PAYLOAD_RELEASE | Late payload / terminal release              |   0.7899 |    0.0058 |     0.0008 |                 0.7841 |                  0.7890 | True                     | True                      |

## Key interpretation

1. The v1.8 QC fix worked: all three branches generated exogenous regressor frames.
2. The full media-level CET-R rerun is now substantially stronger than the earlier cue-only/proxy pass.
3. The father/avatar recognition windows remain the strongest Target-specific residualized Contact windows.
4. The late payload/terminal-release window also remains Target-dominant after residualization.
5. The Pensacola realization window remains Target-dominant, but it is weaker and more visually confounded than the father/avatar region.

## Limitations

- The uploaded QC manifest reports anchor_count=0, so anchor-specific stimulus-rhythm vectors were not generated from a locked anchor JSON in this QC pass.
- The original Contact run remains conceptually predeclared but not runner-registered.
- These are in-sample/proxy residualization models from one self-run. They are useful for falsification and confound inspection, not confirmatory causal proof.
- Better future CET-R should use the locked PRAYCG2.0 anchor JSON and preserve the full stimulus fingerprint path in the same run folder.

## Files generated

- `contact_qc18_branch_status_audit.csv`
- `contact_qc18_branch_metric_summary.csv`
- `contact_qc18_cet_model_summary.csv`
- `contact_qc18_cet_residualized_cii_anchor_integrals.csv`
- `contact_qc18_cet_anchor_delta_summary.csv`
- `contact_qc18_nip_with_cet_residuals.csv`
- `contact_qc18_key_stimulus_rhythm_summary.csv`
- `contact_qc18_cet_interpretation.json`

## Boundary

StimulusFingerprint/CET outputs belong to the exogenous input side of the model, u(t). They are used to test whether physiological/NIP/MRED/TTI effects are reducible to luminance, motion, audio envelope, cuts, cue rhythm, and start-pulse structure. They are not biological hidden-Y, not OSM, and not proof of meaning by themselves.