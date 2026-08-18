# PRAYCG Unified Master Suite v1.4.1 - Folder Picker and Auto Feature CSV Patch

## Problem fixed

The MasterSync Visualizer GUI previously used a file-picker for the `Analysis folder` field. This was confusing because the field is supposed to point to the root Master Comprehensive Suite output folder, not to an individual CSV file. Users also expected the theta/gamma scrolling panel to populate from the analysis folder alone, but the continuous graph requires a feature CSV.

## What changed

- `Analysis folder` now uses a true folder picker in the Visualizer GUI.
- If `Feature CSV` is blank, the Visualizer auto-detects a feature table from `<analysis folder>/tables/`.
- The auto-detection priority is:

```text
human_translation_kht_feature_frame.csv
her_time_resolved_feature_frame.csv
*_time_resolved_feature_frame.csv
*human_translation*kht*feature*.csv
*feature_frame*.csv
```

- If the old workflow accidentally places a CSV path in the `Analysis folder` field, the tool recovers by:
  - using that CSV as the Feature CSV if no Feature CSV was otherwise selected;
  - using the CSV parent or parent-of-`tables/` as the Analysis folder for overlays.
- The Unified Launcher now also auto-detects the best feature CSV for `analysis_plus_visual` mode.
- The Unified Launcher GUI now includes a `Feature CSV override` field under the Visual tab.

## Practical meaning

For reliable theta/gamma scrolling graphs, use either:

```text
Feature CSV selected directly
```

or:

```text
Analysis folder selected, with a feature table inside tables/
```

The analysis folder supplies overlays/events. The feature CSV supplies the continuous plotted traces.

## Boundary

This is a usability and file-routing patch only. It does not change PR-AYC-G endpoint interpretation, CandidateLocal_KHT rules, OSM boundaries, or biological claims.
