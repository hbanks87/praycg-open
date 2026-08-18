# Patch Notes - PRAYCG Unified Master Suite v1.4.3

## Added

### MRED_v0.1 - Meaning Recognition / Encoding Dissociation

This release adds a new Master Comprehensive Suite module:

```text
meaning_recognition_encoding_dissociation
```

The new module separates:

```text
MR  = meaning recognition / schema-reactivation load
ENC = theta-indexed new encoding / integration load
```

The module was added because Arrival backtesting suggested that some scene-interpretable MeaningGamma/TSP/local-K candidates may represent familiar meaning recognition without a strong theta handoff.

## New outputs

```text
tables/mred_event_table.csv
tables/mred_quadrant_classification.csv
tables/mred_anchor_scene_map.csv
tables/mred_familiarity_covariates.csv
tables/mred_visual_overlay.csv
tables/mred_interpretation.json
```

## Visualizer update

The MasterSync Visualizer now auto-ingests MRED overlays from:

```text
<analysis_folder>/tables/mred_visual_overlay.csv
<analysis_folder>/tables/mred_event_table.csv
```

and displays them using the `mred` event category.

## CLI additions

```text
--mred-familiarity-csv <file.csv>
--mred-scene-map-csv <file.csv>
```

These are optional. If not supplied, familiarity/novelty variables are not invented.

## Boundary

MRED does not prove memory encoding, OSM, hidden-Y biology, cellular photonics, or human EEG mechanism. It is an exploratory human-translation layer unless anchors and covariates are prospectively locked.
