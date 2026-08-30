# PRAYCG1.8 Final Reflection Baseline Runner

## What this is

PRAYCG1.8 is a protocol-runner update built from the v1.6U compact runner. It preserves the existing PR-AYC-G sequence, browse-file media selection, LSL hardening, StasisMarkers, optional EEG watchdog, cue markers, objective override sum scoring, and the settle-after-proceed flow.

It adds two changes:

1. **Final Reflection Baseline + Final Master Subjective Report**
2. **Safe-fit movie display sizing for high-DPI laptop displays**

## New end-of-run sequence

After `WASHOUT_3` and `OVERRIDE_1_AFTER_WASHOUT_3` ratings, v1.8 can run:

```text
FINAL REFLECTION INSTRUCTION SCREEN
  Subject reflects on Control, Target, and Override in relation to one another.

SPACEBAR TO PROCEED

BASELINE_2_REFLECTION_PRE_START_STILLNESS
  5-10 second stillness countdown.

BASELINE_2_REFLECTION
  Default 120 seconds.
  This is a reflection baseline, not a neutral resting baseline.

FINAL_MASTER_REPORT
  Final ratings for Control, Target, and Override.
  Typed frozen notes for Control, Target, and Override.
```

The typed note prompts ask what specific portions of each branch felt meaningful, if any.

## Important interpretation boundary

`BASELINE_2_REFLECTION` is not the same as `BASELINE_1`. It is a delayed reflective comparison state. Treat it as a post-protocol integration / washout-retest window, not as a clean neutral baseline.

The final typed notes are frozen subjective annotations. They are evidence streams. They do not prove physiology, consciousness, hidden-Y, or OSM.

## Display safe-fit

Some high-DPI laptops or Windows scaling settings can make the baked-in upper-right number cues feel too close to the physical screen edge. v1.8 adds presentation-layer sizing:

```text
movie_display_mode = safe_fit
movie_safe_fit_fraction = 0.92
```

This draws the full movie slightly inside the screen boundary, preserving aspect ratio and leaving a black margin. It does not alter the MP4 or cue schedule.

Recommended settings for the 2560x1600 / 150% scale laptop issue:

```text
Windows scale: 150%
movie_display_mode: safe_fit
movie_safe_fit_fraction: 0.90 to 0.94
```

If the cue is still too small or too far right, regenerate the stimulus in MediaPrep with a larger cue font or larger cue inset. The protocol runner can shrink/reposition the entire rendered movie, but it cannot move a cue that is already baked into the MP4.

## Run

From the `scripts` folder:

```bat
python run_PRAYCG1_8_FinalReflectionBaseline.py
```

or double-click:

```text
examples\run_PRAYCG1_8_windows.bat
```

## Output files

The runner writes the standard event CSV/JSON plus:

```text
<run>_final_master_subjective_report.json
```

The final report also appears inside the marker log through:

```text
FINAL_MASTER_REPORT_START
FINAL_MASTER_REPORT_CONTROL_START / END
FINAL_MASTER_REPORT_TARGET_START / END
FINAL_MASTER_REPORT_OVERRIDE_START / END
FINAL_FROZEN_NOTE_CONTROL_START / END
FINAL_FROZEN_NOTE_TARGET_START / END
FINAL_FROZEN_NOTE_OVERRIDE_START / END
FINAL_MASTER_REPORT_SAVED
FINAL_MASTER_REPORT_END
```

## Required upstream setup

Use the current operational stack:

```text
BrainFlow/OpenBCI EEG stream
StasisMarkers
PolarHRV or ECG/R-R if used
VernierRespirationBelt if used
ALS_PT19_Timing if used
LabRecorder/XDF
```

If you use MediaPrep v1.6S fullscreen ALS prefix, use the v1.6S cue schedule with the v1.6S videos. Do not reuse old cue schedules after changing the video prefix or cue timing.
