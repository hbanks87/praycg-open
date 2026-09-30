> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Post-hoc proxy analysis; no independently verified blink labels. Private events, masks and waveform figures are withheld.

# Blink-aware Zuna sensitivity review: methodology

Status: methodological recommendation for a post-hoc development analysis, not a validated blink detector or a claim that these checks have run. Prepared without examining new detector-stratified outcome scores. The original aggregate reconstruction results were already known.

## Purpose and interpretation

Assess whether the saved reconstruction errors concentrate around frontal transient activity, reopening transitions, or model-context boundaries. This can identify a plausible confound; it cannot demonstrate clean neural reconstruction or prove that an event was a blink. Retain the original full-data comparison unchanged.

## Fixed transient proxy

- Use measured, retained Fp1 only. Do not use predicted signals or withheld F3/F4/P3/P4 to select samples. Fz may provide visual corroboration but must not silently determine which events are retained.
- Filter each original continuous observed block separately at 0.5–8 Hz with the proposed second-order SOS, forward/backward implementation. Document the exact software implementation and input derivative. Filtering is only for event detection, not a replacement for comparison signals. Never concatenate discontinuous blocks for filtering.
- Estimate one median and one robust scale from Fp1 samples in all eight original scored block interiors, using scale = 1.4826 times median absolute deviation. Record the scale in microvolts. These are descriptive units, not Gaussian significance thresholds.
- Center the detector trace with that median. Detect peaks of absolute deviation with height at least 4 times the robust scale, fixed prominence at least 2 times the scale, and minimum spacing 0.35 seconds. The prominence addition is a proposed fixed shoulder-rejection rule, not an empirically optimized choice.
- Record half-prominence widths and prominence for every detected event. Do not tune duration limits after seeing reconstruction errors. A broad width distribution or repeated rhythmic peaks may indicate drift or neural oscillations rather than blinks.
- Apply the proposed fixed interval from 0.25 seconds before to 0.50 seconds after each peak, merge overlaps, and clip only to the original scored intervals. Keep the original five-second block guards.
- If the robust scale is zero/nonfinite, the channel is missing, or usable coverage is inadequate, report the proxy as unavailable rather than manufacturing a mask. Zero detected events means this proxy found none; it does not establish absence of blinks.

Eyes-closed alpha activity, slow drift, movement, reference contamination, channel placement and filter ringing can influence this detector. A global scale can be affected by the mixture of eyes-open/closed conditions. Preserve this limitation; do not change thresholds to obtain the expected condition pattern.

## Two distinct, predeclared masks

1. Sample-level transient mask: the merged fixed intervals above, compared with its complement inside the original score mask.
2. Context-touched mask: every original five-second model context whose real input samples overlap a transient interval. Map using the actual saved context boundaries, not an assumed time grid. Report this separately from the sample mask.

The second check matters because a transient may affect normalization and inference for an entire context. Forward/backward filtering and later reconstruction filtering can also spread influence beyond a narrow event interval. Even samples outside all flagged contexts are not certified artifact-free.

## Reporting and scoring safeguards

- Apply identical masks to measured targets, interpolation and Zuna. Preserve synchronization and do not align predictions against the answers.
- Report event counts, event times, duration/coverage, counts per block, and first-20-second versus later event rates before interpreting error contrasts.
- Retain the original mean-per-channel NMSE endpoint. For each sensitivity stratum also report RMSE/MSE, target variance, sample count and channel/block contributions. Pooled RMSE and mean-per-channel NMSE are different summaries.
- Compare the two methods within the same stratum. Lower NMSE across different strata is not by itself better reconstruction: the target-variance denominator also changes.
- Treat blocks and electrodes as dependent observations from one recording, not independent participants. Do not attach population-level significance claims.
- Report full-data, transient-associated and lower-transient results side by side, including all unfavorable outcomes. Use 'lower-transient' or 'unflagged,' never 'clean ground truth.'
- For spectral sensitivity analyses, do not stitch separated unmasked samples into a continuous signal. Use an explicitly documented contiguous-window strategy shared by all branches; if coverage is insufficient, report the spectral estimate as unavailable.

## Scientific limits and next decision

Interpolation can agree with contaminated measured targets by reproducing the contamination. Zuna disagreement can represent attenuation, distortion or inaccurate prediction; this sensitivity analysis alone cannot distinguish those explanations. A controlled added-artifact experiment on copied data would test a different, limited cleaning claim, and its uncorrupted copy would still not be guaranteed artifact-free neural ground truth.

Keep the analysis bounded. First inspect saved outputs and complete the independent integration audit. Only objectively justified changes should enter a small declared comparison budget. Any method or exclusion policy chosen using this recording requires untouched-session confirmation. No new recording, long inference run, source modification, upload or hardware action is performed by this methodology note.

## Independent verification after the sensitivity results became available

The following review is a later, explicitly outcome-aware verification; it is not part of the preceding method-blind visual inspection.

- Read the full `blink_audit.py`. The proxy stage selects events using retained Fp1 and original block/evaluation boundaries, not predictions or hidden-channel errors. Both comparison methods receive identical masks. The analysis reproduces the original mean-per-channel NMSE endpoint before reporting the new strata.
- Independently verified the current NPZ, source report, provenance, script, plan and mask hashes against their frozen records. All matched. Reconstructed both masks from the saved event intervals using an independent interval-overlap calculation; both matched exactly. Original model contexts partition all real input samples once without overlap or gaps.
- Independently recomputed pooled RMSE from summed squared errors: all samples, spline 5.734388 versus Zuna 7.752855 microvolts; untouched contexts, 5.554913 versus 5.111288; touched contexts, 5.993186 versus 10.536100; outside the narrower local mask, 5.596334 versus 6.893295. These reproduce the saved results.
- Untouched-context coverage is 240 seconds, including 180 seconds eyes closed and only 60 seconds eyes open. Individual eyes-open coverage is 25, 5, 10 and 20 seconds. Zuna has lower pooled RMSE in three of four eyes-open blocks and three of four eyes-closed blocks within this subset, not all blocks.
- The approximately 8% lower pooled RMSE in untouched contexts is a modest descriptive association worth investigating. The original all-data comparison and the narrower local-mask complement still favor interpolation. Neither the subset nor its lower error establishes blink removal, clean neural recovery, general superiority or a validated deployment rule.
- Reviewed the seam diagnostic separately: its original 88 points include scoring-entry and near-exit boundaries. A read-only recalculation retaining only seams with a fully scored quarter-second on each side leaves 72 interior joins. Median pre-comparison absolute jumps are 0.733927 microvolts measured, 0.688694 spline and 2.677164 Zuna; Zuna's post-comparison median is 1.288722. Thus the greater Zuna discontinuity is not explained solely by the scoring-entry/exit points. No original masks or saved analysis outputs were changed by this diagnostic check.

Reporting should show full-data and both sensitivity masks together, keep unequal condition coverage visible, and avoid choosing a retrospective hybrid that uses whichever method happens to win in each window. Any context-dependent routing policy requires a separately frozen evaluation on untouched data.
