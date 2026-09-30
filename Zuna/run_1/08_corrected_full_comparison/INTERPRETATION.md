> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Final corrected full Run 1 comparison. The two-sample eyes-closed/early/proxy-touched subgroup is insufficient for interpretation; historical numeric values are preserved with this warning.

# Corrected full Zuna comparison — plain-English interpretation

Completed September 26, 2026 (local time). Private, post-hoc development analysis of one real EEG recording with its historical BENCH designation preserved.

## Bottom line

The preparation correction worked, but **Zuna did not outperform spherical-spline interpolation overall**. It reconstructed the withheld measured electrodes better in every eyes-closed block and worse in every eyes-open block. That is a useful, specific finding—not proof that the recording was unusable, that Zuna cleans EEG, or that it is ready for live feedback.

Steps 2–5 are complete. The integration patch remains deferred: the installed Workbench and original recordings were not changed. The corrected candidate remains separate for later review.

## What ran

One full corrected comparison generated all 104 model contexts across all eight evaluation blocks in **66 minutes 38 seconds**, using two CPU threads at verified below-normal process priority. The original 102,456-sample scoring mask was retained (400.219 sample-equivalent seconds); no unfavorable blocks or blink-like periods were removed from the primary result. F3, F4, P3 and P4 were withheld from the model and reconstructed from the other 12 channels.

Independent verification passed: 59 frozen file/source bindings, all 104 checkpoints, all eight blocks, and 298,860 numerical values were checked. Recomputed values matched exactly. The four earlier short-test predictions also reproduced bit-for-bit. Their favorable result was real, but not representative of the full recording.

## Reconstruction results

Primary endpoint: pooled reconstruction error against the withheld measured signals. Lower RMSE is better; units are microvolts.

| Evaluated data | Interpolation RMSE | Zuna RMSE | Interpretation |
| --- | ---: | ---: | --- |
| Entire evaluated recording | 5.583 | 7.366 | Zuna error 31.9% higher |
| Eyes open | 5.850 | 9.376 | Interpolation favored |
| Eyes closed | 5.303 | 4.539 | Zuna favored |

The primary mean electrode-normalized error was **0.675 for interpolation versus 1.176 for Zuna** (74.2% higher for Zuna). This percentage differs from RMSE because it uses a different definition and electrode weighting. The mandatory companion endpoint, before the final comparison filter, also favored interpolation overall. All four eyes-closed blocks favored Zuna and all four eyes-open blocks favored interpolation under both endpoints.

## What this says about blinking

Worse reconstruction was associated with five-second model contexts touched by the historical frontal blink-like proxy. Untouched contexts favored Zuna, including within both eye conditions. This makes context sensitivity worth investigating.

However, **the disadvantage was not confined to the first 15–20 seconds after opening the eyes**: later eyes-open data still favored interpolation. Removing only the locally flagged moments also did not reverse the overall result. These flags are not independently verified blinks, and an unflagged context is not necessarily clean.

The benchmark asks whether Zuna reproduces measured electrodes, including any contamination they contain. A difference from an ocular transient could be suppression of contamination, loss of useful signal, or both. These results do not distinguish those possibilities and cannot establish successful cleaning.

## Frequency content is a separate caution

Zuna produced excess eyes-open spectral power and also overestimated eyes-closed alpha power. The mean closed-minus-open alpha-power difference across the four withheld electrodes was **9.886 µV² measured, 9.696 with interpolation, and 6.305 with Zuna**. Consequently, lower eyes-closed waveform error does not establish faithful preservation of every analytical feature. More alpha power is not automatically an improvement.

## The boundary correction genuinely helped

In the fixed tail-sensitivity diagnostic, the largest change reaching evaluated samples fell from **12.193 µV historically to 0.0159 µV** with corrected preparation. This strongly supports mitigation of the identified preparation/padding boundary mechanism. It does not prove all model-context seams are gone; remaining seams are documented in the full report.

The correction changed both prepared inputs and comparison targets. Absolute old-versus-new error changes must therefore not be described as isolated model improvement against an unchanged target. The main conclusions compare Zuna with interpolation within the corrected pipeline.

## Reporting caveat: one tiny descriptive subgroup

The immutable detailed report displays numerical scores for `eyes_closed / early_5_20 / proxy_context_touched`, which contains **only two samples (0.0078125 seconds)**. These arithmetic values are not scientifically interpretable and should be treated as **insufficient support / not estimable for interpretation**. The report should have displayed that warning. Its unusually large normalized errors must not be used as evidence.

This is a reporting limitation, not a new exclusion or a change to the frozen calculations. No primary, whole-condition, whole-block or whole-context aggregate conclusion above depends on interpreting that two-sample subgroup. This supplemental note preserves the original report rather than silently replacing its verified artifacts.

## Decision and remaining limits

Keep interpolation as the default for this missing-channel use case and Zuna optional/experimental. The eyes-closed result is a candidate benefit to confirm—not a general victory. If pursued later, freeze a narrow eyes-closed reconstruction question, meaningful error and spectral-preservation criteria, and a stopping rule before testing untouched sessions. Do not select favorable seeds or repeatedly alter this development recording until the overall outcome improves. Live adaptation remains a separate, unvalidated stage.

This is one recording, not four independent eyes-closed replications. BENCH is its historical software designation, not a claim that the EEG was synthetic or poor. The measured targets are not clean neural ground truth. Timing remains approximate without independent ALS-barcode confirmation; template electrode geometry includes disclosed coordinate clipping. Full-block centering and zero-phase filtering use future samples, so this pipeline is offline/noncausal. Preparation and final-filter history, reflected tails, and context seams can affect scores. No clinical validity, clean-signal restoration, or prospective validation is established.

## Preserved evidence

- Full report with all blocks, strata, spectra and waveform examples (supporting file not included in this public copy)
- Individual Zuna module report (supporting file not included in this public copy)
- [Independent verification](INDEPENDENT_FULL_VERIFICATION.md)
- [Frozen comparison plan](full_comparison_plan.json)
- [Execution completion record](execution_completion.json)

The completion record was written before independent review and therefore retains its historical `PENDING_INDEPENDENT_REPORT_REVIEW` field. The separate verification report records the subsequent successful review. No new model run was started to produce this interpretation.
