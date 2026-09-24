# Patch Notes — PRAYCG Unified Master Suite v1.4.6

## Added

- `praycg_confound_rsm_modules_v1_4_6.py`
- AVSyncConfound_v0.1
- ExternalAcousticIntrusion_v0.1
- RSM_v0.1 Running Sum Microstate Model
- CVB_v0.1 Cue Visibility / Legibility Burden
- SquintProxy_v0.1
- visual overlay support for `rsm_visual_overlay.csv` and `confound_visual_overlay.csv`
- unified launcher flag `--run-confound-rsm-modules`

## Why

Her Run 1 revealed that several non-neural presentation factors can affect PR-AYC-G interpretation:

- target/override audio-video desynchrony;
- external train noise masking stimulus audio during an important monologue;
- small/blurry upper-right number cues under high-DPI display settings;
- possible squint/visual strain;
- running-sum stalls and approximate-update pressure.

## Interpretation rule

Confounds do not automatically invalidate a run, but they lower claim strength for affected windows. The suite should mark these windows as covariates, veto candidates, or sensitivity-analysis regions.
