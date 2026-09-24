# PRAYCG1.9 — Confound-Aware Runner

PRAYCG1.9 preserves the PRAYCG1.8B predeclared-anchor and final-reflection architecture, then adds formal confound capture for:

- cue legibility, small/blurry cue burden, and possible squint/visual strain;
- running-sum stalls, hard number combinations, approximate/guess compensation;
- perceived audio-video desynchrony;
- external acoustic intrusions such as train noise;
- speaker-volume or audio-comprehension difficulty.

## Core boundary

These reports are not proof of physiology or mechanism. They are covariates, veto flags, and interpretation aids for the Master Comprehensive Suite v1.4.6+.

## Run

```bat
python scripts\run_PRAYCG1_9_ConfoundAware.py
```

## New output files

The runner writes normal event logs plus:

```text
*_prerun_display_audio_calibration.json
*_CONTROL_1_AFTER_WASHOUT_1_confound_report.json
*_TARGET_1_AFTER_WASHOUT_2_confound_report.json
*_OVERRIDE_1_AFTER_WASHOUT_3_confound_report.json
*_final_master_subjective_report.json
```

## Recommended use

Use this runner when you want the Master Suite to distinguish a real weak/negative result from a presentation confound such as delayed audio, train noise, or unreadable cues.


## v1.9B Topo-OSM interpretive update

The default runner remains PRAYCG1.9 Confound-Aware. v1.9B adds documentation, templates, and claim boundaries for Topo-OSM network-state interpretation and the optional PRAYCG-SUB/LSO variant. Human EEG outputs must not be interpreted as microtubular, biophotonic, or molecular memory evidence.
