
# PRAYCG MediaPrep / StimulusFingerprint v1.8 Output Files

Inside the MediaPrep output folder:

```text
stimulus_target_cued_*.mp4
stimulus_override_cued_*.mp4
stimulus_control_cued_phase_scrambled_*.mp4
cue_schedule_*.json
cue_schedule_*.csv
predeclared_anchors_*_DRAFT.json
predeclared_anchors_*_DRAFT.csv
ANCHOR_LOCK_CHECKLIST_*.md
```

Inside `qc/` when StimulusFingerprint is enabled:

```text
stimulus_exogenous_regressor_frame_control.csv
stimulus_exogenous_regressor_frame_target.csv
stimulus_exogenous_regressor_frame_override.csv
stimulus_exogenous_regressor_frame_all_conditions.csv
cet_regressors_control.csv
cet_regressors_target.csv
cet_regressors_override.csv
cet_regressors_all_conditions.csv
stimulus_rhythm_summary_all_conditions.csv
stimulus_dominant_frequency_timeseries_all_conditions.csv
anchor_stimulus_rhythm_vectors_all_conditions.csv
stimulusfingerprint_branch_status.csv
stimulusfingerprint_error_log.json
stimulusfingerprint_cet_eet_manifest.json
stimulusfingerprint_cet_eet_report.md
```

`stimulus_exogenous_regressor_frame_all_conditions.csv` is the preferred Master Suite input for CET-R.
