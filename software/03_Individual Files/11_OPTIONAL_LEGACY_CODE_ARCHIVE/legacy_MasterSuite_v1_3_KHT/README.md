# PRAYCG Master Comprehensive Suite v1.3.0

## HumanTranslation_KHT Update

This package is the v1.3.0 post-processing suite for PR-AYC-G. It extends v1.2.0 by adding:

- `HumanTranslation_KHT_v0.2`
- `media_covariate_inventory`
- feature-table compatibility patches for older window-feature tables using `phase/t0/t1/rel_t`
- stricter boundary language separating `K_HT` from `K_OSM`

## Boundary

`K_HT` is a rough human-translation coupling estimate between EEG-derived gamma/work features and a human-level proxy such as TemporalSemanticProxy. It is not `K_OSM`, not `Y_cell`, not `Y_OSM`, and not evidence of microtubular, cellular, or opto-structural memory by itself.

Media fingerprint/QC data are treated as exogenous input inventory: luminance, visual motion, audio envelope, cue events, and task demand help define the stimulus drive `u(t)`. They do not replace a biological `Y` channel.

## Main script

```bash
python scripts\praycg_master_comprehensive_suite_gui_v1_3.py
```

Headless example:

```bash
python scripts\praycg_master_comprehensive_suite_gui_v1_3.py ^
  --no-gui ^
  --project-name AboutTime_Run2_v13 ^
  --xdf path\to\run.xdf ^
  --event-log path\to\events.json ^
  --cue-schedule-json path\to\cue_schedule.json ^
  --media-manifest-json path\to\media_prep_manifest.json ^
  --stimulus-fingerprint-folder path\to\StimulusFingerprint ^
  --stimulus-style sustained_early_peak
```

Feature-table-only example:

```bash
python scripts\praycg_master_comprehensive_suite_gui_v1_3.py ^
  --no-gui ^
  --project-name ExistingFeatureTable_KHT ^
  --feature-table-path path\to\window_features.csv ^
  --stimulus-style sustained_early_peak
```

## New output tables

The new module writes:

```text
tables/human_translation_kht_media_covariate_inventory.csv
tables/human_translation_kht_columns_used.csv
tables/human_translation_kht_feature_frame.csv
tables/human_translation_kht_phasewise_summary.csv
tables/human_translation_kht_cv_model_losses.csv
tables/human_translation_kht_cv_win_summary.csv
tables/human_translation_kht_interpretation.json
```

## Rough pass rule

A run is not labeled as a clean human-translation K_HT pass unless:

```text
Target K_HT > Control K_HT
Target K_HT > Override K_HT
Full reciprocal model wins blocked CV over simpler alternatives
Artifact/timing/media covariates are not dominant
```

This is an exploratory rule for prioritizing follow-up, not proof of OSM.
