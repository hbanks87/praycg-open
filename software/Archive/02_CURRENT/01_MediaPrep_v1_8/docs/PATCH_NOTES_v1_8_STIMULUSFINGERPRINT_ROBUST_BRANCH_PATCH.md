
# PRAYCG MediaPrep / StimulusFingerprint v1.8 Patch Notes

## Purpose

v1.8 patches the v1.7B StimulusFingerprint / CET / EET regressor builder after a Contact exploratory rerun showed that the fingerprint pass could abort after the Control branch when the local NumPy environment did not expose `np.trapz`.

## Main fixes

1. **NumPy-safe trapezoidal integration**
   - Adds `trapz_safe()`.
   - Uses `np.trapezoid` when available, falls back to `np.trapz` when available, and finally to a manual trapezoid implementation.

2. **Per-branch failure isolation**
   - Control, Target, and Override are processed independently.
   - One branch failure no longer prevents the remaining branches from being fingerprinted.
   - `--fail-on-partial` is available when a strict nonzero exit code is desired.

3. **Explicit branch status outputs**
   - `stimulusfingerprint_branch_status.csv`
   - `stimulusfingerprint_error_log.json`
   - Manifest status: `PASS`, `PARTIAL_FAIL`, or `FAIL`.

4. **Combined outputs only from successful branches**
   - `stimulus_exogenous_regressor_frame_all_conditions.csv`
   - `cet_regressors_all_conditions.csv`
   - `stimulus_rhythm_summary_all_conditions.csv`
   - `stimulus_dominant_frequency_timeseries_all_conditions.csv`
   - `anchor_stimulus_rhythm_vectors_all_conditions.csv`

## Boundary

These files are stimulus-side regressors for external input `u(t)`. They support CET/CET-R/EET and confound modeling. They do not certify meaning, MRED, TTI, NIP, OSM, hidden-Y biology, or human EEG mechanism.
