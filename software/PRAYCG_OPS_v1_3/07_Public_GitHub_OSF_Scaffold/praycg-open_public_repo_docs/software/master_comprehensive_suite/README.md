# Master Comprehensive Analysis Suite

The Master Comprehensive Suite processes PR-AYC-G run data and produces feature tables, module tables, reports, and event overlays.

## Current recommended branch

```text
PRAYCG Unified Master Suite v1.4.1 - Folder Picker + Auto Feature CSV Patch
```

## Feature CSV

The suite may generate a feature table such as:

```text
tables/human_translation_kht_feature_frame.csv
tables/<run>_time_resolved_feature_frame.csv
```

This is the continuous time-resolved table used by the visualizer for theta/gamma/HR/HRV/API/respiration/ALS graphs.

## Major modules

- stream inventory and timing QC;
- ALS timing QC;
- EEG feature extraction;
- GammaScalpel;
- TemporalSemanticProxy;
- TSP-to-theta handoff;
- Gamma-to-theta handoff;
- PNCC theta family;
- API_A_v1;
- HumanTranslation_KHT;
- CandidateLocal_KHT;
- thresholded-state timing;
- report generation.

## CandidateLocal_KHT rule

```text
K alone is not enough.
Theta handoff alone is not enough.
Final human-event lock requires local coupling + theta carryover + condition specificity + artifact/timing pass.
```

## Boundary

`K_HT` is a human-translation proxy. It is not `K_OSM`.
