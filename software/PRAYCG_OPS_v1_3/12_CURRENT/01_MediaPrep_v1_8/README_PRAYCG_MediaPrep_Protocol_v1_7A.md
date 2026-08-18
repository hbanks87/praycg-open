# PRAYCG MediaPrep v1.7A — AnchorPrep + ALS Fullscreen Start-Pulse

This package extends the v1.6S MediaPrep tool by generating **DRAFT predeclared anchor schedules** beside the cue schedule.

## Why this exists

The runner can only marker-register anchors if it receives a concrete anchor JSON/CSV before acquisition. Previously, anchors could exist in planning notes but not appear in the run files. v1.7A fixes the workflow:

```text
MediaPrep generates final rendered videos
→ MediaPrep writes DRAFT anchor JSON/CSV beside cue_schedule
→ human reviews final Target MP4 and fills exact rendered_time_sec
→ anchor finalizer writes *_LOCKED.json
→ PRAYCG1.9C runner loads *_LOCKED.json and emits ANCHOR markers into StasisMarkers/XDF
```

## Main script

```bat
python scripts\praycg_media_prep_gui_v1_7A.py
```

## Anchor files generated

Inside each MediaPrep output folder:

```text
predeclared_anchors_<project>_v1_7A_DRAFT.json
predeclared_anchors_<project>_v1_7A_DRAFT.csv
ANCHOR_LOCK_CHECKLIST_<project>_v1_7A.md
```

These DRAFT files are not confirmatory. Fill exact final rendered-video times, then run:

```bat
python scripts\praycg_anchor_lock_finalizer_v1_7A.py --draft "C:\path\to\predeclared_anchors_<project>_v1_7A_DRAFT.json"
```

This writes:

```text
predeclared_anchors_<project>_v1_7A_LOCKED.json
predeclared_anchors_<project>_v1_7A_LOCKED.csv
```

Load the LOCKED file in PRAYCG1.9C.

## Presets

```text
generic
contact
eternal_sunshine
contact_eternal_sunshine
```

The preset only creates editable scene-anchor rows. It does not know the exact timecode. Exact timecodes must be measured on the final generated MP4.

## Boundary

The anchor file freezes timing hypotheses. It does not certify meaning, neural endpoints, empathy, task compliance, or OSM. The physiology still must pass artifact, timing, condition-specificity, null-window, and report-consistency checks.

## Additional docs

```text
docs/KISS_WORKFLOW_v1_7A.md
docs/WHERE_ANCHOR_FILES_GO_v1_7A.md
docs/CONTACT_ETERNAL_SUNSHINE_ANCHOR_PRESETS_v1_7A.md
```

## Verification notes

The two main Python files were syntax-checked:

```text
scripts/praycg_media_prep_gui_v1_7A.py
scripts/praycg_anchor_lock_finalizer_v1_7A.py
```
