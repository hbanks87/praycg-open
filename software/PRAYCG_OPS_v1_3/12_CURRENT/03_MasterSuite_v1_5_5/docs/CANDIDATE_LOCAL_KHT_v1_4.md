# CandidateLocal_KHT_v0.1

CandidateLocal_KHT is an event-level exploratory module added to the Master Comprehensive Suite in v1.4.0.

## Purpose

The module asks whether a local candidate event shows both:

1. local reciprocal coupling between gamma/work signal E(t) and a human-translation proxy Y_HT(t), and
2. a theta carryover/handoff after the candidate event.

It follows the Rung 0O rule:

```text
K alone is not enough.
Theta handoff alone is not enough.
Final event lock requires both.
```

## Endpoint

For each candidate event, the module estimates:

```text
E_next ~ E_t + Y_HT_t + artifact_t
Y_HT_next ~ Y_HT_t + E_t + artifact_t
```

Then:

```text
eta  = Y_HT -> E coefficient
zeta = E -> Y_HT coefficient
K_local = sqrt(abs(eta * zeta))
```

The sign of the eta*zeta product is retained separately.

## Anchor levels

- Predeclared/media-structural anchors may become confirmatory if loaded before acquisition or before physiology analysis.
- Annotation-file anchors are secondary unless explicitly predeclared.
- Physiology-discovered anchors are exploratory in the same run.

## Outputs

```text
candidate_local_kht_analysis.csv
candidate_local_kht_anchor_manifest.csv
candidate_local_kht_random_anchor_reference.csv
candidate_local_kht_interpretation.json
candidate_local_kht_visual_overlay.csv
```

## Boundary

CandidateLocal_KHT estimates event-level human-translation coupling. It does not prove OSM, hidden-Y biology, cellular photonics, microtubular memory, or a human EEG mechanism.
