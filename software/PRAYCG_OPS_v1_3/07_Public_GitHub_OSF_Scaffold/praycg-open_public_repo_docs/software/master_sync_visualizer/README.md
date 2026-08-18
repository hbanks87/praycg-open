# MasterSync Visualizer

The MasterSync Visualizer renders synchronized review videos containing the stimulus on top and rolling physiology panels below.

## Current recommended branch

```text
PRAYCG Unified Master Suite v1.4.1 visualizer
```

## Inputs

```text
XDF file, optional
stimulus MP4
condition selector: control / target / override / full session
analysis folder
feature CSV
event overlays
output MP4 path
```

## Analysis folder vs Feature CSV

```text
Analysis folder:
  root Master Comprehensive Suite output folder containing tables/ with event overlays.

Feature CSV:
  continuous feature table used to draw scrolling traces.
```

If Feature CSV is blank, the patched visualizer searches `<analysis folder>/tables/` for:

```text
human_translation_kht_feature_frame.csv
*_time_resolved_feature_frame.csv
*feature_frame*.csv
```

## Output sidecars

```text
<output>_features_used.csv
<output>_events_used.csv
<output>_render_report.json
```

## Boundary

This is a visualization/audit tool. It does not certify meaning, OSM, hidden-Y biology, task compliance, or endpoint validity.
