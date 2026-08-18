# MediaPrep

MediaPrep prepares the PR-AYC-G stimulus suite.

## Current recommended branch

```text
PRAYCG MediaPrep v1.6S - ALS fullscreen start pulse
```

## Core outputs

```text
stimulus_target_cued_<project>.mp4
stimulus_override_cued_<project>.mp4
stimulus_control_cued_phase_scrambled_<project>.mp4
cue_schedule_<project>.json
cue_schedule_<project>.csv
media_prep_manifest.json
QC checklists
```

## Critical method rules

1. Target and Contextual Override must be generated from the same cue-embedded video.
2. Only participant instructions should differ between Target and Override.
3. Control should be phase-scrambled from the cue-embedded Target.
4. Control audio must be manually QC-checked.
5. Any source-stamp cleanup must occur before branch generation.
6. No copyrighted stimulus media should be committed to GitHub.

## ALS v1.6S fullscreen start pulse

The recommended ALS timing pulse is:

```text
black settle screen before video
-> full-screen white pulse at start of MP4
-> black guard
-> actual stimulus content
```

The ALS pulse validates physical display timing. It is not a biological measurement.

## Public release note

Put scripts here. Do not put commercial movie clips here.
