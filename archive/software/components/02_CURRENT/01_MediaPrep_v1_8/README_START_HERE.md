# Start Here — PRAYCG MediaPrep + StimulusFingerprint v1.8

Use this package to prepare PRAYCG stimulus videos and the stimulus-side regressors required by the Master Comprehensive Suite.

## KISS

```bat
py -3.11 scripts\run_PRAYCG_MediaPrep_v1_8.py
```

For fingerprint-only reruns:

```bat
py -3.11 scripts\praycg_stimulus_fingerprint_cet_eet_v1_8.py --help
```

For an existing MediaPrep folder:

```bat
py -3.11 scripts\praycg_batch_stimulus_fingerprint_v1_8.py --mediaprep-folder "C:\PRAYCG\stimuli\Contact\Contact_MediaPrep_v1_8_YYYYMMDD_HHMMSS"
```

## The important v1.8 patch

v1.8 fixes the Contact v1.7B failure mode by:

- replacing fragile `np.trapz` calls with `trapz_safe()`;
- continuing Target/Override processing if Control fails, or vice versa;
- writing `stimulusfingerprint_branch_status.csv` and `stimulusfingerprint_error_log.json`;
- preserving combined all-condition outputs when enough branches succeed.

## Boundary

This package prepares media and stimulus-side exogenous regressors in `u(t)`. It does not certify meaning, MRED, TTI, NIP, OSM, hidden-Y biology, or human EEG mechanism.
