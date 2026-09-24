# KISS Workflow — MediaPrep v1.7A

## One sentence

MediaPrep v1.7A creates the videos, cue schedule, full-screen ALS start pulse, QC files, and a DRAFT anchor schedule in one output folder.

## Basic use

```bat
python scripts\praycg_media_prep_gui_v1_7A.py
```

Recommended settings:

```text
ALS pulse mode: fullscreen_start
Generate DRAFT predeclared anchor schedule: checked
Anchor preset: generic/contact/eternal_sunshine/contact_eternal_sunshine
```

## After generation

Open the output folder and manually QC:

```text
1. Target video plays correctly.
2. Override video is hash-identical to Target.
3. Control is phase-scrambled from the cue-embedded Target.
4. Control audio is unintelligible by human listening.
5. Full-screen white start pulse is visible to ALS on Target, Control, and Override.
6. DRAFT anchor JSON/CSV exists.
```

Then lock anchors with:

```bat
python scripts\praycg_anchor_lock_finalizer_v1_7A.py --draft "<DRAFT anchor JSON>"
```

Use the `*_LOCKED.json` in the PRAYCG runner.
