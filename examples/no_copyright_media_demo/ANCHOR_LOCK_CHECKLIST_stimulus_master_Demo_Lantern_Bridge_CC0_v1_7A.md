# PRAYCG v1.7A Anchor Lock Checklist — stimulus_master_Demo_Lantern_Bridge_CC0

## Purpose
MediaPrep now generates a DRAFT predeclared-anchor schedule beside the cue schedule. The draft is not confirmatory until exact rendered video times are filled, finalized, and loaded into PRAYCG1.9C before acquisition.

## Files generated
- Draft JSON: `predeclared_anchors_stimulus_master_Demo_Lantern_Bridge_CC0_v1_7A_DRAFT.json`
- Draft CSV: `predeclared_anchors_stimulus_master_Demo_Lantern_Bridge_CC0_v1_7A_DRAFT.csv`

## Lock workflow
1. Open the final generated Target MP4, not the raw source video.
2. Step to each scene event and write the exact `rendered_time_sec` into the draft JSON or CSV.
3. Keep times in final rendered-video seconds. If the ALS fullscreen prefix is present, do not forget the prefix offset.
4. Run:

```bat
python scripts\praycg_anchor_lock_finalizer_v1_7A.py --draft "C:\Users\hoytb\Desktop\PRAYCGStimulus\lantern\stimulus_master_Demo_Lantern_Bridge_CC0_MediaPrep_v1_7A_20260819_210010\predeclared_anchors_stimulus_master_Demo_Lantern_Bridge_CC0_v1_7A_DRAFT.json"
```

5. Load the resulting `*_LOCKED.json` in the PRAYCG1.9C runner.
6. Confirm the runner logs `ANCHOR_SCHEDULE_LOADED`, `ANCHOR_DEF_*`, and scheduled branch anchor markers.

## Boundary
The anchor file freezes scene timing. It does not make a result positive. Physiology must still pass artifact, timing, condition-specificity, and null-window checks.
