> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Historical uncorrected preparation; not the final corrected Run 1 endpoint.

# Zuna comparison: private interpretation

Recording: `RUN_1`  
PRAYCG Alpha 10.3.1 | Reviewed 2026-09-26  
Designation: **POSTHOC_EXPLORATORY · single recording · BENCH_TEST · CAUTION**  
Scientific authority: NONE. Original participant-data eligibility remains false.

## Bottom line

The computation completed correctly, but this Zuna configuration did **not** improve the primary reconstruction outcome over spherical-spline interpolation. The simpler baseline predicted the withheld measured signals better overall. This is a useful negative result for this specific implementation and recording—not evidence that Zuna always performs worse, or that either method recovered clean brain activity.

Mean per-electrode normalized mean squared error (NMSE; lower is better) was **0.659 for interpolation versus 1.212 for Zuna**. Zuna's mean NMSE was approximately **84% higher**. This percentage describes normalized squared error, not a percentage loss of accuracy or an increase in RMSE.

## What was compared

Twelve measured EEG channels supplied the inputs. Four measured channels—F3, F4, P3 and P4—were withheld as prediction targets. All eight fixed evaluation blocks were included; calibration and five seconds at each block edge were excluded from scoring. Approximately 480.18 seconds were modeled and 400.22 seconds scored. Hidden targets were not used in input referencing or normalization.

| Withheld electrode | Interpolation NMSE | Zuna NMSE | Interpolation RMSE (µV) | Zuna RMSE (µV) |
| --- | ---: | ---: | ---: | ---: |
| F3 | 0.309 | 0.960 | 4.80 | 8.46 |
| F4 | 0.845 | 1.001 | 7.28 | 7.93 |
| P3 | 0.726 | 1.482 | 4.96 | 7.09 |
| P4 | 0.755 | 1.404 | 5.55 | 7.57 |

Zuna had lower block-average NMSE in three of eight blocks, all eyes-closed; interpolation was better in every eyes-open block. These are correlated observations within one recording, not independent replications. Not every metric worsened: F4 mean absolute error improved, despite its worse RMSE.

As a secondary descriptive result, closed-minus-open alpha power averaged 9.89 µV² in the measured targets, 9.69 with interpolation and 4.93 with Zuna. Zuna preserved the direction but reduced its magnitude. The last eyes-open block also had elevated generated alpha. Neither observation establishes clean neural activity, participant compliance or state-decoding validity.

## Verification and limitations

- Successful completion at 20:25:58 UTC (15:25:58 CDT), in about 72 minutes 46 seconds. All 104 checkpoints and all eight evaluation blocks were verified. Outputs are actual MODEL_GENERATED predictions, not placeholders.
- Independent read-only checks matched the original input/source bindings, pinned model, report and derivative hashes. Preprocessing, checkpoint output slices and reported NMSE were independently reproduced. The original two-thread run completed without mixing benchmark checkpoints.
- The montage and right-ear SRB/left-ear BIAS wiring were confirmed by the operator after recording. They differ from the original prospective montage assumption; the original prospective endpoint therefore remains NOT_ESTIMABLE_POSTHOC.
- Withheld measured signals can contain artifacts: they are **not clean neural ground truth**. Full-record QC cautions, including timestamp gaps, remain preserved. Timing uses an approximate diagnostic host/device clock mapping, not physical timing calibration.
- Independent five-second model contexts can introduce seams. Filtering was explicitly disclosed: prepared measured/interpolation branches effectively received two linear filtering passes, while generated Zuna output received the comparison pass after inference from prepared inputs. This can affect the comparison and is not an exact reproduction of the model paper.
- Template geometry was used, not digitized electrode positions. Cz exceeded the model's spatial grid and was clipped during coordinate encoding. This deserves review, but is not a demonstrated explanation for the unfavorable result.

No clinical validity, clean-signal restoration or prospective validation is established. Do not promote the generated channels to measured data, discard unfavorable blocks, or tune this recording into a claimed independent success.

## Recommended next step

Preserve this complete result. Review spatial-coordinate handling, model-context seams and filtering as separately labeled diagnostics before freezing a fresh validation configuration. Any revised analysis of this recording must remain explicitly post-hoc; a prospective replication requires a new recording.

## Local evidence

- Module HTML report (supporting file not included in this public copy)
- [Machine-readable report](zuna_eeg_reconstruction_v1_0.json)
- [Per-channel metrics](zuna_comparison_metrics_v1_0.csv)
- [Per-block metrics](zuna_exploratory_block_metrics_v1_0.json)
- [Provenance](zuna_provenance_v1_0.json)

This note is a new private interpretation; original recordings, frozen code, recipe and generated results were not modified.
