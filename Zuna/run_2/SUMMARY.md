# Run 2 — completed offline comparison

Execution succeeded: all eight evaluation blocks and all 97 model contexts completed with eight CPU threads. Duration was approximately 31 minutes 31 seconds. The original acquisition designation is PARTICIPANT_ACQUISITION, not BENCH. Acquisition channel review was prospective; the evidence-bound timing preparation is a separate post-hoc processing step.

Mean per-electrode NMSE was **1.087064 for Zuna** versus **4.190243 for spherical-spline interpolation**, a 74.1% relative reduction for this endpoint in this recording. This percentage does not mean that percentage of EEG was cleaned, recovered, or made accurate.

| Method | Electrode | NMSE | RMSE (µV) | Pearson r |
|---|---|---:|---:|---:|
| spherical_spline | F3 | 0.977972 | 9.372328 | 0.503388 |
| spherical_spline | F4 | 6.554150 | 26.089897 | -0.511817 |
| spherical_spline | P3 | 0.752400 | 4.969115 | 0.855054 |
| spherical_spline | P4 | 8.476449 | 15.598475 | -0.398070 |
| zuna | F3 | 0.641519 | 7.590823 | 0.632013 |
| zuna | F4 | 1.437691 | 12.219317 | 0.122221 |
| zuna | P3 | 0.503341 | 4.064300 | 0.800680 |
| zuna | P4 | 1.765707 | 7.119255 | 0.445645 |

Zuna's F4 and P4 error remains greater than each target's variance (NMSE > 1); these channels require caution despite improvement over a weak spline baseline. Correlation and amplitude/error are different metrics. Results remain descriptive, not population inference.

The recorded ALS source did not match the original declaration, so optical timing remains UNVERIFIED. The counter-supported EEG timing derivative is not physical sensor/display calibration. Original QC warnings, template-geometry clipping, filtering, reference, and independent five-second model-context limitations remain in force. No block was removed because the model performed poorly.

- [Public module report data](comparison/zuna_eeg_reconstruction_v1_0.json)
- [All eight blocks](comparison/zuna_exploratory_block_metrics_v1_0.json)
- [Per-electrode CSV](comparison/zuna_comparison_metrics_v1_0.csv)
- [Model and preparation provenance](comparison/zuna_provenance_v1_0.json)
- [Completion checks](execution/execution_completion.json)
