
# PRAYCG MediaPrep + StimulusFingerprint v1.8

This package combines:

- MediaPrep stimulus generation
- fullscreen ALS/photodiode start-pulse support
- anchor draft generation and anchor lock finalization
- StimulusFingerprint / CET / EET exogenous regressor generation
- v1.8 NumPy-safe integration and branch-isolated processing

## Main entry points

```text
scripts/run_PRAYCG_MediaPrep_v1_8.py
scripts/praycg_media_prep_gui_v1_8.py
scripts/praycg_stimulus_fingerprint_cet_eet_v1_8.py
scripts/praycg_anchor_lock_finalizer_v1_7A.py
```

## Why v1.8 exists

The v1.7B fingerprint builder could abort the entire run if one branch failed during numeric integration. v1.8 uses `trapz_safe()` and processes branches independently so Control, Target, and Override outputs are not lost because one branch fails.

## Boundary

MediaPrep prepares stimuli and exogenous regressors. It does not certify meaning, empathy, neural endpoints, task compliance, control-audio unintelligibility, OSM, or hidden biological mechanisms.
