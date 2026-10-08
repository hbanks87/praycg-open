# Alpha 10.5.2: implementation of the twelve requested improvements

| # | Improvement | Delivered behavior and verification |
|---|---|---|
| 1 | Gamma Scalpel 2.0 | One Forge action; report identifies EEG-only, EMG, EOG or combined reference mode. Numerical and governed-dispatch tests. |
| 2 | Reference discovery | Compatible recorded Cerelog/other reference streams checked for participant, source, labels, units and identity conflicts. Missing or ambiguous references remain unassessed. |
| 3 | Measured artifact assessment | Supported EMG replaces the EEG muscle-proxy screen; supported EOG adds measured eye screening. EEG gaps, clipping and amplitude checks remain. The legacy formula is retained as an explicit comparison. |
| 4 | Supported comparisons | Original and measured-reference-screened results, retained duration and equal-duration supported condition portions; unmatched conditions are unavailable. |
| 5 | Timing and reference quality | Native-rate reference features, continuity and quality checks. Independent-clock attribution requires documented timing support; software tests do not qualify physical Cerelog–Athena synchronization. |
| 6 | Actual Athena electrodes | Gamma is reported at measured TP9, AF7, AF8 and TP10. No unmeasured regional or meaning endpoint is inferred. Existing Master Suite implementation is preserved. |
| 7 | Reusable instrument profiles | Versioned exact-model/decoder/channel instrument profiles with evidence hashes. Bundled Athena raw profile recognizes the supported recorded connector format. |
| 8 | Recording-specific conversion | Verified instrument facts generate each recording's binding and baseline; synthetic inversion/profile tests pass. Actual Athena HbO/HbR stays unavailable because full mapping, geometry and intensity/firmware support are not established. |
| 9 | Optical review across protocols | Explore optical signals uses recorded optics independently of EEG QC, with whole-recording default and optional protocol scope. Existing Athena recording checked offline. |
| 10 | Adaptive optical spectra | Automatic 30 → 10 → 5-second windows, explicit spacing/range/support, gaps preserved, full and screened spectra use the same resolution. Raw trends remain when spectra are unsupported. This change applies to offline Forge review; live/replay retains its existing spectral policy. |
| 11 | Simple Forge workflow | Persistent recording, shared progress/cancel/retry, one Gamma action and one optical action. Source, scope and window choices live under Details and are frozen with the attempt. Prior public-bundle path migration corrected. |
| 12 | Tests and complete release | Meaningful numerical, metadata, timing, profile, GUI and governed-dispatch tests; existing regression groups, full installer check, saved-recording checks, public docs and complete distribution checksums. Final counts and limitations are in the shipped build receipt. |

Software implementation and offline file checks do not establish neural origin, physiological accuracy, clinical utility or physical cross-device timing. Gamma reference screening preserves the measured EEG rather than subtracting artifacts automatically. Raw optical percentage changes are recorded-value trends, not hemoglobin concentration.

Read the [Forge guide](ANALYSIS_FORGE_ALPHA_10_5_2.md), [Gamma guide](Gamma_Scalpel_v2_0/README.md), [optical guide](Optical_Signal_Review_v1_0/README.md), and [Athena source review](ATHENA_OPTICAL_SOURCE_REVIEW_ALPHA_10_5_2.md).
