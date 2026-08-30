# Contact Run 1 - MRED-ITP / ACG / OCU Deep Analysis v1.1

## Executive verdict
The new MRED-ITP layer is useful as an exploratory information-structure and ocular-release audit, but it does not provide a literal thermodynamic proof. In Contact Run 1, the father/avatar cluster remains the most important MRED/KHT-topo event from the earlier modules. The new ACG/OCU layer adds mixed support: the A2b father/avatar TSP follow-through window showed the strongest Target complexity-settlement index, while Fp1 blink release was sparse in Target overall. No strict combined MRED-ITP candidate passed both ACG and OCU gates.

## Boundary
Lempel-Ziv-style complexity is a compressibility/diversity proxy, not literal thermodynamic entropy. Fp1 blink timing is an ocular event-boundary proxy, not proof of memory encoding. Without EOG or eye tracking, OCU remains tentative. No OSM biology, hidden-Y biology, microtubules, or human EEG mechanism is inferred.

## Alignment note
The analysis used the corrected Contact stream inventory (`sample_index_from_ALS_pulses`) to map raw EEG sample indices into protocol time. This matters because raw XDF stream timestamps and StasisMarker timestamps can be offset unless the physically validated ALS/sample-index alignment is used.

## Phase summary
| phase                 |   mean complexity proxy |   blinks |   blink/min |
|:----------------------|------------------------:|---------:|------------:|
| CONTROL_1             |                   0.911 |        7 |       1.386 |
| TARGET_1              |                   0.936 |        3 |       0.599 |
| CONTEXTUAL_OVERRIDE_1 |                   0.891 |        5 |       0.999 |
| BASELINE_1            |                   0.890 |       31 |      15.500 |
| WASHOUT_1             |                   0.921 |        3 |       1.500 |
| WASHOUT_2             |                   0.938 |        1 |       0.500 |
| WASHOUT_3             |                   0.910 |        7 |       3.500 |
| BASELINE_2_REFLECTION |                   0.916 |        2 |       1.000 |

## Target anchor summary
| anchor           |   C strike |   C settle |    CSI |   blink suppression |   blink release |    ORI | MRED quadrant    | MRED lock   |
|:-----------------|-----------:|-----------:|-------:|--------------------:|----------------:|-------:|:-----------------|:------------|
| A1 Pensacola     |     -0.003 |     -0.002 | -0.597 |               4.800 |           0.000 |  0.461 | MR_HIGH_ENC_LOW  | False       |
| A2 Father/avatar |      0.009 |     -0.021 |  0.596 |               0.000 |           0.000 | -0.563 | MR_HIGH_ENC_HIGH | True        |
| A2b Father TSP   |      0.016 |     -0.028 |  1.224 |               0.000 |           4.000 | -0.037 | MR_HIGH_ENC_LOW  | True        |
| A3 Existential   |     -0.009 |      0.011 | -1.375 |               0.000 |           0.000 |  0.000 | MR_HIGH_ENC_HIGH | False       |
| A4 Late release  |      0.002 |     -0.007 | -0.081 |               0.000 |           0.000 |  0.000 | MR_HIGH_ENC_LOW  | False       |

## Target vs Override specificity
| anchor           |   Target-Override CSI |   Target-Override ORI |   Target-Override ITP |
|:-----------------|----------------------:|----------------------:|----------------------:|
| A1 Pensacola     |                -1.068 |                 0.075 |                -0.505 |
| A2 Father/avatar |                 1.058 |                 1.037 |                 1.244 |
| A2b Father TSP   |                 2.137 |                 1.562 |                 2.157 |
| A3 Existential   |                -0.135 |                 0.000 |                -0.070 |
| A4 Late release  |                -0.620 |                 0.000 |                -0.322 |

## Interpretation
- ACG: the father/avatar TSP follow-through window had the strongest Target CSI. The father/avatar recognition anchor itself had MRED lock but did not pass strict ACG/OCU gates.
- OCU: Target blink rate was low overall, which is consistent with sustained visual/narrative attention, but release events were sparse. This makes OCU supportive at most, not confirmatory.
- Baseline 1 had many Fp1 blink-proxy events relative to later phases; this may reflect settling, ocular strain, or early artifact rather than narrative state.
- The late payload/release anchor showed modest complexity settlement but no blink-release support.
- The correct use of this layer is convergence/falsification: it can strengthen MRED/NIP/TTI when it aligns, but it should veto or caution claims when complexity or ocular timing is artifact-driven.

## Files
Primary tables: `lz_complexity_timeseries.csv`, `acg_event_table.csv`, `blink_event_table.csv`, `ocu_event_table.csv`, `mred_itp_anchor_summary.csv`, `mred_itp_condition_specificity.csv`, `mred_itp_visual_overlay.csv`, and `mred_itp_interpretation.json`.