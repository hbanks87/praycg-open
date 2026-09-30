> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Four fixed five-second contexts, not an independent recording or a full endpoint. See subsequent priority-status correction in prestart history.

# Independent review of the bounded boundary-fix comparison

## Decision

The proposed four-context experiment is reasonable as a **post-hoc engineering diagnostic**, subject to the checks below. It is not a repeat of the original full-recording endpoint, not prospective validation, and cannot establish a general reconstruction or cleaning benefit. No model inference was performed by this reviewer.

The confirmed DC-offset/polyphase-padding boundary mechanism provides an independent engineering reason to test one candidate. Choosing that candidate is not contingent on favorable Zuna errors. Per-channel centering plus line padding are two changes packaged as one declared boundary-treatment candidate; the experiment cannot identify their individual contributions. Do not describe it as an isolated single-operation causal experiment.

## Selection must be frozen before candidate predictions

1. Use exactly the existing recorded retained-electrode proxy masks and their already-fixed definition. Call them **blink-like proxy strata**, not known blink/no-blink labels. The proxy was developed on this recording and may itself reflect preprocessing, so it is not independent validation evidence.
2. Define `touched` unambiguously before selection: at least one proxy-flagged sample within the original five-second model context. `Untouched` means zero proxy-flagged samples, not clean neural signal.
3. Require exactly 1,280 original samples in each selected context, and require **every selected sample** to pass the original evaluation mask. Do not include tiny final reflected contexts or partly evaluated transition contexts.
4. Within each `(eyes-open, eyes-closed) × (touched, untouched)` stratum, select the earliest qualifying original context. Record zero-based global window index, original segment index, sample bounds, timestamps, condition, proxy count, original seed and input hashes. Run selected contexts in chronological order.
5. If a stratum is absent, report it as absent; do not adjust the detector, timing eligibility or selection rule to fill it. If a selected inference fails, retain that failure and stop under the declared policy rather than replacing the context.

## Seed preservation

The installed adapter sets `window_seed = (seed + local_index) % 2**31` and explicitly calls `torch.manual_seed(window_seed)` immediately before each `model.sample` call. Therefore, a separate one-context call can preserve the historical sampling seed by passing the **recorded original window seed** as its base seed and having exactly one local window.

Verify, rather than assume, that the new provenance records the same seed, 16 sampling steps, CFG 1.0, float32, two CPU threads, one interop thread, model revision, weight hash and geometry. Input shape must be 12 × 1,280 with four generated target channels, without new padding. No checkpoint from the original pipeline may be reused as a corrected candidate prediction. Fixed seeds reduce one source of variation; they do not guarantee cross-platform bitwise reproducibility or favorable results.

## Processing and comparison

- Apply the candidate whole-block numerical preparation consistently before cropping the chosen context. Per-channel means must be computed independently, and only retained channels may contribute to the model input reference or normalization. Target-channel statistics must never reach model inputs.
- This uses future samples within the block and zero-phase filtering. It is explicitly an offline diagnostic and provides no causal/live-processing validation.
- The historical comparison must use historical saved precomparison measured targets, saved raw generated output and saved precomparison spline output for the identical sample indices.
- The candidate comparison must use corrected precomparison targets, actual newly generated candidate output and corrected spline output at those same indices.
- **Do not run a new zero-phase comparison filter on the cropped five-second outputs.** That would introduce another crop-boundary treatment absent from the whole-block preparation. The declared diagnostic instead evaluates raw model output against already band-limited targets and baseline. This is a different estimand from the original twice-filtered comparison and must remain visibly separate.
- Historical and candidate targets differ because preparation changed. Compare Zuna against spline within each pipeline. Absolute historical-to-candidate error changes combine target-processing and prediction changes; they cannot alone be described as a clean gain in the model's accuracy. Report the target change magnitude alongside the paired pipeline results.
- Never label saved historical predictions scored against corrected targets as newly executed corrected-model predictions. That is not the proposed comparison.

## Metrics and interpretation

Report per-context and per-channel RMSE, MAE, NMSE with its explicit target variance, and correlation where estimable. If pooling across four contexts, state exactly whether RMSE is pooled over samples/channels or averaged across channel scores; retain the individual results so one transient cannot be hidden in the aggregate.

Calculate descriptive alpha power separately within each five-second context using fixed Welch settings. Do not concatenate disjoint contexts for spectral estimation. Twenty selected seconds cannot reliably characterize full eyes-open/eyes-closed physiology, estimate independent replications, or validate a participant-level effect. Do not calculate inferential p-values from channels/windows as though they were independent participants.

The artifact should preserve both favorable and unfavorable results, all failures, original QC/BENCH/post-hoc designations, and the fact that measured hidden electrodes are not clean neural ground truth. Original scores, artifacts and masks remain untouched.

## Bounded execution

One declared candidate, at most four contexts, fixed weights and settings, and no tuning afterward. Record an overall ten-minute execution budget including preparation and model loads; stop cooperatively at a safe boundary or terminate the isolated process under the declared timeout if required. Preserve partial results and failure details. Do not automatically escalate threads, add contexts, sweep seeds, tune gains, or start a full comparison when this short diagnostic ends.

## What a successful short run could establish

It could show that the engineering correction is executable and how the two pipelines behave on a small, predetermined sample. The strongest established result may remain the model-free finding that boundary treatment removes an artificial response to constant channel offsets. Any apparent reconstruction benefit still needs a frozen full evaluation and independent recordings. A negative short result should be retained, not followed by parameter searching.
