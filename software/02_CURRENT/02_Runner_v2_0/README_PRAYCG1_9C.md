# PRAYCG1.9C — Anchor-Registered Confound-Aware Runner

PRAYCG1.9C makes the predeclared anchor workflow visible and hard to miss.

## Main script

```bat
python scripts\run_PRAYCG1_9C_AnchorRegistered.py
```

## What changed from 1.9B

- The media tab now labels the anchor field as **Predeclared anchor JSON/CSV — LOCKED file**.
- Adds an **Auto-detect LOCKED anchor from cue folder** button.
- If no locked anchor is loaded, validation states that the run is anchor-unregistered.
- If a DRAFT anchor file is selected, the runner will not crash; incomplete anchors are skipped and logged.
- Run config now includes the anchor file path and anchor SHA-256 when present.
- StasisMarkers now include `MEDIA_SELECTED_PREDECLARED_ANCHOR_FILE`, `MEDIA_SHA256_ANCHOR_*`, `ANCHOR_SCHEDULE_LOADED`, `ANCHOR_DEF_*`, and scheduled branch anchor markers when valid anchors are loaded.

## Correct workflow

```text
1. Run MediaPrep v1.7A.
2. Open final Target MP4 and fill exact rendered_time_sec in the DRAFT anchor file.
3. Run the v1.7A anchor finalizer to create *_LOCKED.json.
4. Start PRAYCG1.9C.
5. Select media and cue schedule.
6. Click Auto-detect LOCKED anchor from cue folder, or browse to the LOCKED file.
7. Validate.
8. Record.
```

## Claim boundary

Conceptually planned anchors are useful. Runner-registered anchors require a valid LOCKED JSON/CSV loaded before acquisition so the run files contain anchor provenance and markers.
