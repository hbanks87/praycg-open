# MRED_v0.1 - Meaning Recognition / Encoding Dissociation

## Purpose

MRED_v0.1 formalizes a new PR-AYC-G analysis layer: a meaningful scene can be recognized, retrieved, or reactivated without necessarily producing a detectable theta-indexed new encoding / integration handoff.

The module separates two event-level quantities:

```text
MR  = Meaning Recognition / schema-reactivation load
ENC = New Encoding / integration load
```

This distinction was motivated by Arrival Run 1: multiple scene-interpretable gamma/TSP/local-K candidates appeared meaningful, but several did not show strong post-taper theta carryover. That pattern should not be forced into a binary “meaning vs no meaning” interpretation.

## Core formula

For event or anchor `j`:

```text
MR_j = 0.35*z(MeaningGamma_j)
     + 0.35*z(TSP_j)
     + 0.30*z(K_local_j)
     - 0.20*z_positive(artifact_j)
```

Meaning Recognition is high when the event shows semantic-affective work signals such as MeaningGamma, TemporalSemanticProxy, and local K_HT-style coupling.

```text
ENC_j = 0.65*z(theta_handoff_best_j)
      + 0.15*z(API_A_j)
      + 0.20*z(novelty_j)
      - 0.20*z(familiarity_j)
      - 0.15*z_positive(artifact_j)
```

ENC is high when a post-event theta carryover/integration signal appears, optionally supported by novelty and autonomic availability. Familiarity reduces the new-encoding interpretation because a familiar meaningful scene may reactivate an existing schema without requiring a new update.

If familiarity/novelty covariates are not supplied, the module does **not** invent them. Missing covariates contribute zero after event-level standardization.

## Quadrants

| MR | ENC | Label | Interpretation |
|---|---|---|---|
| High | High | `MR_HIGH_ENC_HIGH` | Meaning recognition plus possible new integration / encoding candidate. |
| High | Low | `MR_HIGH_ENC_LOW` | Meaning recognition, old-memory reactivation, or schema retrieval without detected theta-indexed integration. |
| Low | High | `MR_LOW_ENC_HIGH` | Non-semantic encoding, task effect, novelty, respiration/artifact, or control flag. |
| Low | Low | `MR_LOW_ENC_LOW` | Null or weak event. |

`MR_high` and `ENC_high` require both relative elevation and a positive score. A high percentile alone is not enough when the score is negative.

## Inputs

Preferred event source:

```text
tables/candidate_local_kht_analysis.csv
```

Optional user-supplied covariates:

```text
--mred-familiarity-csv <file.csv>
--mred-scene-map-csv <file.csv>
```

Optional anchor sources:

```text
--predeclared-anchor-file <anchors.json|anchors.csv>
--annotation-csv <annotations.csv>
```

## Output files

```text
tables/mred_event_table.csv
tables/mred_quadrant_classification.csv
tables/mred_anchor_scene_map.csv
tables/mred_familiarity_covariates.csv
tables/mred_visual_overlay.csv
tables/mred_interpretation.json
```

The visualizer ingests `mred_visual_overlay.csv` automatically when an analysis folder is supplied.

## Interpretation boundary

MRED_v0.1 is a human-translation interpretive layer. It does **not** prove memory encoding, Opto-Structural Memory, `Y_cell`, `Y_OSM`, or `K_OSM`.

A missing theta handoff does **not** prove that no memory was encoded. It only means the current suite did not detect its operational theta-carryover marker.

## Recommended prospective use

For future runs, define media-structural anchors before analysis and collect familiarity/novelty ratings:

```text
Have you seen this clip before?
How familiar was the scene? 0-9
Did you remember the emotional beat before it happened? 0-9
Did the scene feel newly meaningful today? 0-9
Did it reactivate an older memory or feeling? 0-9
Did it connect to your current life? 0-9
Did it create a new insight? 0-9
Did it feel meaningful but already known? 0-9
```
