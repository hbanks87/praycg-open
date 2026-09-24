
# PRAYCG MediaPrep + StimulusFingerprint v1.8 KISS Workflow

1. Run MediaPrep v1.8.
2. Enable StimulusFingerprint/CET/EET after media generation.
3. Confirm output videos:
   - Target
   - Contextual Override
   - phase-scrambled Control
   - cue schedule JSON/CSV
   - draft anchor JSON/CSV
4. Review the final rendered Target MP4.
5. Fill exact `rendered_time_sec` values in the draft anchor file.
6. Run the anchor finalizer to create `*_LOCKED.json`.
7. Load the locked anchor file in PRAYCG2.0 before acquisition.
8. After acquisition, give the Master Comprehensive Suite both:
   - the run XDF / event log
   - `qc/stimulus_exogenous_regressor_frame_all_conditions.csv`

The v1.8 fingerprint pass writes a branch-status CSV. Treat any `PARTIAL_FAIL` run as incomplete for confirmatory CET-R.
