> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Post-hoc proxy analysis; no independently verified blink labels. Private events, masks and waveform figures are withheld.

# Method-blind visual review of the fixed frontal-transient proxy

Reviewed `proxy_overview.png` and `proxy_examples.png` before viewing any detector-stratified Zuna/interpolation reconstruction scores. The examples contain prepared measured Fp1, measured Fz and the detector trace; no hidden-electrode or prediction traces were inspected for this review. The original aggregate comparison was already known, so this is method-blind visual inspection of new strata, not prospective study blinding.

## Observations

- Several large Fp1 transients have a corresponding smaller Fz deflection. This is compatible with a shared frontal disturbance, including possible ocular activity, but does not identify its physiological source.
- The selected examples include broad/biphasic events, recovery or secondary lobes following larger events, and smaller ambiguous transients. A detector peak cannot be equated one-for-one with a blink.
- Some marked intervals cover the recovery portion of a larger waveform rather than its largest deflection. A fixed narrow mask is consequently only an operational sensitivity interval; it is not a complete delineation of every contamination episode.
- The eight close-ups are the first chronological events, all from the first eyes-open block; the first two are outside the original scored interior. They provide an outcome-independent illustration, not a representative visual validation of all 66 scored detections or all conditions.
- Large terminal Fp1 deflections appear at approximately 58–60 seconds in every block, with strikingly similar shapes and amplitudes exceeding roughly one millivolt. The repetition at the same prepared-block boundary is suspicious for a systematic preparation, filtering or resampling boundary effect. Visual inspection alone cannot identify the exact cause.
- The terminal peaks are outside the original five-second scoring guards. This does not prove that filtering, model-context normalization or subsequent processing is unaffected. The input-stage provenance of these features warrants audit separately from the blink hypothesis.
- The global plotting scale is dominated by those terminal waveforms. It makes smaller interior activity difficult to inspect; the chronological close-ups are therefore more informative for judging what the detector actually labels. No thresholds or masks were revised based on these plots.

## Counts and coverage supplied with the fixed-mask result

The analysis reports 109 proxy peaks over the displayed blocks, of which 66 occur in the original scored interiors. Scored eyes-open counts are 9, 17, 18 and 14; eyes-closed counts are 4, 1, 1 and 2. These are detector-peak counts, not confirmed blink counts. The reported masks cover 43.67 seconds locally and touch 160.22 seconds of model contexts, out of approximately 400.22 scored seconds. These numerical totals were supplied with the frozen-mask output, not independently recalculated in this visual review.

The higher number of scored eyes-open detections is consistent with a condition-associated frontal-transient difference. It does not prove that blinking explains reconstruction differences, that all such transients are ocular, or that unflagged eyes-closed periods represent clean neural ground truth.

## Disposition

Keep the fixed detector and both original sensitivity masks unchanged. Report the limitations and all strata, and inspect the systematic boundary feature through the independent integration audit before drawing conclusions about Zuna's neural fidelity or artifact removal. No predictions, mask changes, model runs, source changes or recording edits were performed for this visual review.
