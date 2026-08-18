# PRAYCG StimulusFingerprint Suite v1.5

This package standardizes PR-AYC-G media QC in one execution.

It opens a small user-interface window where you select:

- phase-scrambled Control MP4
- intact Target MP4
- Contextual Override MP4
- optional cue schedule JSON
- optional cue schedule CSV
- output folder

Then it automatically runs:

1. StimulusFingerprint v1.0 on all three videos.
2. Cue-visibility QC on Target and Contextual Override when a cue schedule JSON is supplied.
3. Pairwise physical-delivery comparisons:
   - Target vs Control
   - Target vs Contextual Override
   - Control vs Contextual Override
4. A master report and summary tables.

## Boundary

This tool measures digital stimulus-delivery proxies: pixel luminance, visual change, cut-rate proxy, digital audio dBFS, audio envelope rhythm, and cue visibility. It does **not** measure literal photons, true dB SPL, empathy, meaning, consciousness, or narrative quality.

## How to run with the UI

From this folder:

```bash
python scripts/praycg_stimulus_fingerprint_batch_ui_v1_5.py
```

Fill in the fields and click **Run Full Fingerprint Suite**.

## Headless command-line run

```bash
python scripts/praycg_stimulus_fingerprint_batch_ui_v1_5.py --no-gui ^
  --project-name CODA_Pilot1 ^
  --control stimulus_control_cued_scrambled.mp4 ^
  --target stimulus_target_cued_v1_6H.mp4 ^
  --override stimulus_override_cued_v1_6H.mp4 ^
  --cue-schedule-json cue_schedule_v1_6H.json ^
  --cue-schedule-csv cue_schedule_v1_6H.csv ^
  --out-root outputs ^
  --sample-fps 5 ^
  --resize-width 320
```

## Output structure

```text
<project>_StimulusFingerprint_v1_5_<timestamp>/
  00_master/
    PRAYCG_StimulusFingerprint_v1_5_master_report.md
    stimulus_suite_master_summary.json
    stimulus_suite_metric_matrix.csv
    stimulus_suite_pairwise_comparisons.csv
    stimulus_suite_manifest.json
  01_fingerprints/
    control/
    target/
    contextual_override/
  02_comparisons/
    target_vs_control/
    target_vs_contextual_override/
    control_vs_contextual_override/
  03_provenance/
    cue_schedule_v1_6H.json
    cue_schedule_v1_6H.csv
```

## Recommended usage

For cue-embedded suites, the strongest PR-AYC-G design is:

- Control = phase-scrambled version of the same cue-embedded source.
- Target = intact cue-embedded target, numbers ignored.
- Contextual Override = the same intact cue-embedded target, numbers summed.

The Target and Contextual Override files should be identical or nearly identical at the media-file level. The intended difference is instruction and cognitive stance.
