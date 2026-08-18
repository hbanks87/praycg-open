# PR-AYC-G GammaScalpel v1.0

GammaScalpel is an exploratory PR-AYC-G analysis module for splitting the broad 30-45 Hz lower-gamma bucket into spatial, spectral, and rigidity features.

It asks a narrower question than earlier lower-gamma analysis:

> Is the observed gamma-band work more compatible with task-lock, meaning-candidate processing, visual entrainment, or artifact?

It does **not** claim that any gamma feature is a direct marker of meaning, consciousness, empathy, or opto-structural memory.

## Main script

```bash
python scripts/praycg_gammascalpel_v1_0.py run.xdf \
  --events-json run_events.json \
  --cue-json cue_schedule_v1_6H.json \
  --out outputs/gammascalpel_run01
```

The script includes a minimal float32 XDF reader, so it does not require `pyxdf`.

## Required inputs

- XDF file with OpenBCI EEG and optional Vernier/Polar streams.
- Local PR-AYC-G event JSON with LSL timestamps.
- Optional number-cue schedule JSON.

## Fixed PRAYCG16 channel map

The default map is:

```text
1 Fz, 2 Cz, 3 Pz, 4 F3, 5 F4, 6 C3, 7 C4, 8 P3,
9 P4, 10 T5, 11 T6, 12 O1, 13 O2, 14 T3, 15 T4, 16 Fp1
```

## Outputs

- `gammascalpel_window_features.csv`
- `gammascalpel_segment_summary.csv`
- `gammascalpel_condition_contrasts.csv`
- `gammascalpel_segment_level_pac.csv`
- `gammascalpel_segment_level_pac_contrasts.csv`
- `gammascalpel_key_segment_scores.csv`
- `cue_visibility_qc_status.csv`
- figures

## Interpretation boundary

GammaScalpel produces candidate feature patterns. It does not adjudicate internal experience by itself. Self-report, task behavior, HRV/API, respiration, artifact scores, and cue visibility must be interpreted together.
