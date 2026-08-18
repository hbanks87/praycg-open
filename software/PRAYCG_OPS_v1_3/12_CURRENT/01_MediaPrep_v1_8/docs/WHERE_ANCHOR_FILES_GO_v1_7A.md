# Where v1.7A Anchor Files Are Generated

MediaPrep v1.7A writes anchor-prep files into the same MediaPrep output folder that contains the generated stimulus videos and cue schedule.

Typical output folder:

```text
<chosen_output_root>/<project>_MediaPrep_v1_7A_<timestamp>/
```

Typical files:

```text
stimulus_master_cleaned_<project>_v1_7A.mp4
stimulus_target_cued_<project>_v1_7A.mp4
stimulus_override_cued_<project>_v1_7A.mp4
stimulus_control_cued_phase_scrambled_<project>_v1_7A.mp4
cue_schedule_<project>_v1_7A.json
cue_schedule_<project>_v1_7A.csv
predeclared_anchors_<project>_v1_7A_DRAFT.json
predeclared_anchors_<project>_v1_7A_DRAFT.csv
ANCHOR_LOCK_CHECKLIST_<project>_v1_7A.md
```

The DRAFT anchor files are not confirmatory. They are scaffolds.

## Lock workflow

1. Open the final generated Target MP4, not the raw source video.
2. Fill `rendered_time_sec` for each anchor using final rendered-video time.
3. Run the finalizer:

```bat
python scripts\praycg_anchor_lock_finalizer_v1_7A.py ^
  --draft "C:\path\to\predeclared_anchors_<project>_v1_7A_DRAFT.json"
```

4. The finalizer writes:

```text
predeclared_anchors_<project>_v1_7A_LOCKED.json
predeclared_anchors_<project>_v1_7A_LOCKED.csv
predeclared_anchors_<project>_v1_7A_LOCKED_manifest.json
```

5. Load the `*_LOCKED.json` in PRAYCG1.9C / PRAYCG2.0 before acquisition.

## Claim boundary

A LOCKED anchor file freezes timing hypotheses. It does not make the physiology positive. A result still needs artifact/timing pass, Target > Control, Target > Override, local K_HT-topo/MRED/TTI criteria, and confound review.
