# PRAYCG1.8B — Predeclared Anchor / Chronometric Humility Runner

PRAYCG1.8B amends PRAYCG1.8 by adding an optional predeclared anchor JSON/CSV file. The anchor file is selected in the preflight GUI and recorded in the local event log and StasisMarkers stream.

## Why this exists

Absorbed subjects are not reliable clocks. PRAYCG1.8B therefore moves the confirmatory timing layer away from retrospective subject time estimates and toward:

1. media-structural anchors,
2. algorithmically predeclared anchors,
3. post-run scene descriptions that do not require exact timestamps, and
4. physiology-discovered anchors that remain exploratory until repeated under a frozen rule.

## Core rule

Freeze the scene, freeze the algorithm, and let the subject describe meaning without pretending to be a stopwatch.

## How to run

```bat
python scripts\run_PRAYCG1_8B_PredeclaredAnchors.py
```

or:

```bat
python scripts\run_praycg_v1_8B.py
```

The GUI now includes an optional field:

```text
Predeclared anchor JSON/CSV
```

Leave it blank for no predeclared anchors. Select a JSON/CSV to emit anchor definitions and scheduled anchor markers during Control, Target, and Contextual Override.

## Her template

The package includes:

```text
templates\Her_media_structural_anchors_v1_8B.json
```

This freezes the user-reviewed Her scene at approximately 113.9 seconds, when the letter reading ends and the characters reach the roof. For the already completed Her Run 1, this is post-hoc/future-freeze. For a future Her repeat, it becomes predeclared only if loaded before acquisition or before physiology analysis.

## Marker families

Setup markers:

```text
ANCHOR_SCHEDULE_LOADED
ANCHOR_SCHEDULE_N_<N>
ANCHOR_CHRONOMETRIC_HUMILITY_RULE
ANCHOR_DEF_<ANCHOR_ID>
```

During branch videos:

```text
ANCHOR_<PHASE>_<ANCHOR_ID>_PRE_START
ANCHOR_<PHASE>_<ANCHOR_ID>_PRE_END
ANCHOR_<PHASE>_<ANCHOR_ID>_POINT
ANCHOR_<PHASE>_<ANCHOR_ID>_PEAK_SEARCH_START
ANCHOR_<PHASE>_<ANCHOR_ID>_PEAK_SEARCH_END
ANCHOR_<PHASE>_<ANCHOR_ID>_THETA_CARRYOVER_START
ANCHOR_<PHASE>_<ANCHOR_ID>_THETA_CARRYOVER_END
```

## Anchor schema

JSON anchor files contain:

```json
{
  "schema": "PRAYCG_predeclared_anchor_schedule_v1_8B",
  "content_start_offset_sec": 0.0,
  "anchors": [
    {
      "anchor_id": "EXAMPLE_A1",
      "source": "media_structural",
      "claim_level": "confirmatory_if_loaded_before_run",
      "condition_scope": "all_branches",
      "rendered_time_sec": 113.9,
      "description": "Exact scene event.",
      "pre_window_sec": [-15, 0],
      "expected_peak_search_window_sec": [0, 10],
      "theta_carryover_window_sec": [10, 30]
    }
  ]
}
```

If `rendered_time_sec` is absent, the runner can use `content_time_sec + content_start_offset_sec`. This matters for media prepared with fullscreen ALS prefixes.

## Boundary

PRAYCG1.8B does not prove meaning, K_HT, OSM, hidden-Y biology, or human EEG mechanism. It only improves the timing discipline of the protocol by replacing retrospective subject-clock windows with predeclared anchors.
