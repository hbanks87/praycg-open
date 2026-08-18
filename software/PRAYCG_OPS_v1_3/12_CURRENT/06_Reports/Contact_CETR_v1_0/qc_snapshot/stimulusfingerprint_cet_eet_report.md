# PRAYCG StimulusFingerprint/CET/EET v1.8 Report

Project: `Cetfixed_Contact`
Created UTC: `2026-08-17T03:33:46.439302+00:00`
Status: `PASS`

## Outputs

- `stimulus_exogenous_regressor_frame_all_conditions.csv` — merged visual/audio/cue/ALS regressors.
- `cet_regressors_all_conditions.csv` — compact design matrix for CET/CET-R.
- `stimulus_rhythm_summary_all_conditions.csv` — FFT/Welch dominant-frequency summary.
- `stimulus_dominant_frequency_timeseries_all_conditions.csv` — STFT-like rolling dominant-frequency map.
- `anchor_stimulus_rhythm_vectors_all_conditions.csv` — anchor-window vectors for EET, when anchor JSON is supplied.

## Boundary

These outputs belong to the stimulus/input side of the model: `u(t)`. They are not biological hidden-Y, not OSM, not proof of meaning, and not an EEG endpoint.

Overall status: `PASS`
Branch errors: `0`