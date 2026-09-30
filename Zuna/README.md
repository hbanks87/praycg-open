# PRAYCG Zuna — two-recording public analysis archive

This is a **report-and-summary-data publication copy**, prepared for human review before public GitHub upload. It contains the completed analyses, negative findings, engineering audits, and unsuccessful-attempt history located for two Zuna EEG recordings. It does not contain raw EEG, waveform derivatives, checkpoints, model files, or installed software. Nothing was uploaded automatically.

Open **index.html** locally for the overview, or browse this README and the linked Markdown documents directly on GitHub.

## Results at a glance

Lower normalized mean squared error (NMSE) is better. These are comparisons against withheld **measured** EEG, not unknown clean neural signals.

| Analysis stage | Spline mean NMSE | Zuna mean NMSE | Lower error |
|---|---:|---:|---|
| Run 1 — initial comparison | 0.658757 | 1.211829 | Spline |
| Run 1 — guided comparison | 0.658757 | 1.224085 | Spline |
| Run 1 — corrected full comparison | 0.675071 | 1.175655 | Spline |
| Run 2 — full comparison | 4.190243 | 1.087064 | Zuna |

The stages in this table are **not four recordings**. The first three reuse Run 1. A separate corrected short diagnostic used four five-second contexts from Run 1; its favorable result did not predict the full-recording outcome.

- **Run 1, corrected full:** interpolation was favored overall. Zuna was better in the four eyes-closed blocks and worse in the four eyes-open blocks. Its historical BENCH label is retained; that label does not mean the recording was synthetic. The blink-proxy, breathing-association and preparation-boundary audits are included.
- **Run 2:** Zuna was favored against spline interpolation on the mean NMSE endpoint and across each held-out electrode overall. This is a relative advantage against this particular baseline, not demonstrated cleaning or general validity. Zuna's F4 and P4 NMSE values remain above 1; the four-electrode mean is also above 1. An NMSE of 1 corresponds to predicting the evaluation target's own mean as a hindsight reference, not a deployable hidden-target estimator.
- **Do not infer a trend from two recordings.** The stages differ in acquisition, evidence review, timing preparation, and processing history. This is not a controlled version comparison, independent-participant validation, or a preregistered efficacy claim.

## Start here

- [Complete analysis index](ANALYSIS_INDEX.md)
- [Run 1 final interpretation](run_1/08_corrected_full_comparison/INTERPRETATION.md)
- [Run 1 full detailed report](run_1/08_corrected_full_comparison/report/FULL_COMPARISON_REPORT.md)
- [Run 2 readable summary and electrode results](run_2/SUMMARY.md)
- [Methods and limitations](METHODS_AND_LIMITATIONS.md)
- [Privacy review and deliberate exclusions](PUBLICATION_PRIVACY_REVIEW.md)
- [Citations and rights](CITATIONS_AND_RIGHTS.md)
- [Data dictionary and verification](DATA_DICTIONARY.md)

## Publication boundaries

This archive is not anonymous simply because direct local identifiers were removed. It still discloses physiological research findings, and association with a public account can identify the participant. Review it before publishing and confirm authority to disclose every participant's information. No claim of institutional approval or consent from any other participant is made here.

Public JSON files are wrapped, transformed derivatives—not original signed records, valid import recipes, or an executable Research Bundle. Original private artifacts are unchanged. Original-document hashes and exported-file hashes are distinguished in `manifest.json`; `SHA256SUMS.txt` verifies the public files. Raw-data numerical replay is not possible from this report-only archive.

No new model inference, selective rerun, code patch, upload, or alteration of original results was performed to create this bundle.
