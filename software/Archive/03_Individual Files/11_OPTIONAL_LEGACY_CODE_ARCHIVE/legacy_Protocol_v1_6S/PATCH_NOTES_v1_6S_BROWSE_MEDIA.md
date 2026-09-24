# PRAYCG1.6S Patch Notes — Browse Media Selection

## Summary

PRAYCG1.6S adds file-browse buttons to the initial acquisition GUI.

The operator now explicitly chooses:

```text
Control MP4
Target MP4
Contextual Override MP4
Cue schedule JSON
```

before `StasisMarkers` is created and before LabRecorder is started.

## Why this patch exists

Earlier versions could fail when the cue schedule filename or working directory did not match the default path. A run could continue with `CUE_SCHEDULE_NOT_LOADED`, which prevented cue-by-cue markers and objective override scoring. v1.6S turns the cue JSON into an explicit selected input and aborts if it cannot be loaded.

## Preserved from v1.6R

The v1.6R transition order remains intact:

```text
report/input
→ instruction/proceed screen
→ press SPACE
→ stillness countdown
→ next analyzable video block
```

The keypress now occurs before stillness, not immediately before the stimulus.

## New markers

```text
MEDIA_SELECTION_GUI_VERSION_1.6S
MEDIA_FILE_SELECTION_START
MEDIA_SELECTED_CONTROL_VIDEO
MEDIA_SELECTED_TARGET_VIDEO
MEDIA_SELECTED_CONTEXTUAL_OVERRIDE_VIDEO
MEDIA_SELECTED_CUE_SCHEDULE_JSON
MEDIA_SHA256_CONTROL_<first12>
MEDIA_SHA256_TARGET_<first12>
MEDIA_SHA256_OVERRIDE_<first12>
MEDIA_SHA256_CUEJSON_<first12>
TARGET_OVERRIDE_HASH_MATCH_TRUE/FALSE
MEDIA_FILE_SELECTION_END
ERROR_CUE_SCHEDULE_NOT_LOADED_ABORT
```

Full paths and complete SHA-256 hashes are stored in the local config JSON, not only in LSL marker names.

## New local output

```text
PRAYCG_v1_6S_<participant>_<session>_<run>_<timestamp>_run_config_media_selection.json
```

## Validation behavior

v1.6S validates:

```text
video files exist
cue schedule exists
cue schedule contains cue_events
expected_sum exists or is manually supplied
```

A missing/empty cue schedule is a hard abort.

## Compatibility

The Tkinter GUI is used for Browse buttons. If Tkinter is unavailable, the script falls back to a PsychoPy text-field dialog, but without browse buttons.
