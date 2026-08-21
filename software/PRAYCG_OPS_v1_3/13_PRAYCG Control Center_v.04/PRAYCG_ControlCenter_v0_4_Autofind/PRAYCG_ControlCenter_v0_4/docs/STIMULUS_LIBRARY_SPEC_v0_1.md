# Stimulus Library Specification v0.4

## Root folder

```text
C:\PRAYCG\stimuli\<stimulus_id>\
```

## Folder map

```text
<stimulus_id>\
  master\
    stimulus_master.mp4
    master_media_validation_report.json
    master_sha256.txt

  mediaprep\
    <timestamped_mediaprep_folder>\
      stimulus_target_cued_*.mp4
      stimulus_override_cued_*.mp4
      stimulus_control_cued_phase_scrambled_*.mp4
      cue_schedule_*.json
      cue_schedule_*.csv
      qc\

  anchors\
    *_DRAFT.json
    *_LOCKED.json
    *_annotation_windows.csv
    *_MRED_scene_map.csv
    *_MRED_familiarity_covariates.csv
```

## Add Master Stimulus

The Control Center copies the selected MP4 to:

```text
master/stimulus_master.mp4
```

and creates:

```text
master_media_validation_report.json
master_sha256.txt
```

## Validation checks

Basic validation includes:

- file exists;
- extension is `.mp4`;
- SHA-256 hash computed;
- duration if FFmpeg/OpenCV available;
- width/height/fps if FFmpeg/OpenCV available;
- audio stream if FFmpeg available;
- warnings for no audio, too short, too long, or limited validation.

## Boundary

This library validates file handling. It does not validate narrative quality, participant effect, or empirical endpoint status.
