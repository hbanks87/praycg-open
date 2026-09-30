> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Four fixed five-second contexts, not an independent recording or a full endpoint. See subsequent priority-status correction in prestart history.

# Boundary-safe Zuna preparation: correction and short comparison

Private development result · 26 September 2026 · historical BENCH recording.

## Outcome

The boundary-safe correction is implemented and regression-tested in an **isolated candidate**, and all four planned model contexts completed. The original recording, installed Workbench, original recipe and prior reports are unchanged. This is not a packaged release or full validation run.

On the fixed 20-second sample, corrected-pipeline pooled RMSE was **5.735 µV interpolation versus 5.059 µV Zuna**. Zuna's error was 11.8% lower; Zuna had lower RMSE in 4 of four contexts. These four contexts were selected from measured-input categories, not model performance.

**Engineering success and reconstruction benefit are different outcomes.** Passing the preparation tests does not establish that Zuna improves EEG, removes blinks or is ready for live use. All results below are post-hoc, short, single-recording diagnostics.

## What changed

Each channel's constant full-block mean is removed before resampling. The resampler now explicitly extends the endpoint linearly instead of assuming zero outside the interval. The arithmetic layout is canonicalized so a C/F memory-layout difference cannot change retained-channel statistics. The 256 Hz grid, 0.5–40 Hz filter, retained-only reference, four hidden electrodes, original timestamps/masks and model settings remain unchanged.

The candidate records the versioned policy `PRAYCG_ZUNA_OFFLINE_BLOCK_CENTER_LINE_RESAMPLE_V1_0`, source hashes and removed offsets. Targets are independently centered; their values/statistics never enter retained inputs or reference. Full-block means and zero-phase filtering remain offline/noncausal operations.

The old and new preparations reproduced identical timestamps, source-grid lengths and all 102,456 originally evaluated samples across eight blocks. Fp1 maximum absolute amplitude in each last-five-second interval changed from approximately **6720–7581 µV to 12.1–119.2 µV**. This demonstrates removal of the giant offset-related processing waves, not proof that all remaining EEG is clean.

## Regression evidence

**All 198 tests passed: 38 new boundary-preparation tests and 160 existing Zuna tests, with no skipped tests.** They ran in the installed Zuna numerical environment. The largest tested constant-offset difference was 1.74 × 10⁻⁹ µV; the largest tested 10/20 Hz interior gain deviation was 0.166%.

The model run was gated on `regression_gate.json`, which binds the tested worker hash. Tests cover constant-offset invariance across sample rates, gain/phase at declared pass-band frequencies, exact retained-input independence from hidden values and memory layout, nonfinite/overflow/flat-input rejection, true-gap and reversed-clock rejection, interval independence, unchanged timestamp mapping and explicit new provenance. Exact dependency versions and tolerances are in the linked evidence; no test result is a clinical or physiological validation claim.

A first regression attempt exposed a roughly 10⁻¹² µV storage-order rounding difference. It was corrected without weakening exact independence assertions. The pre-fix preparation was retained under `pre_layout_fix_preparation`; it was not used for model inference.

## Fixed short comparison

Selection: the first chronological complete five-second context for each eye-condition/proxy category, with every sample passing the original scoring mask. The proxy is the detector frozen during the prior audit and is not a verified blink label. No alternative window was substituted.

Both eyes-open contexts came from the first eyes-open block; both eyes-closed contexts came from the first eyes-closed block. This is four windows from two blocks, not four independently replicated conditions. "Proxy-untouched" means the fixed detector did not flag that context, not that the context is artifact-free.

Model: pinned ZUNA1.1 weights, 16 steps, cfg 1, float32 CPU, two threads, below-normal process priority. Every single-context call used that historical context's recorded seed. New execution took **2.92 minutes**. Exactly four new contexts (20 seconds) were inferred, with no automatic retries or full-recording rerun.

| Context | Start within its block, s | Spline RMSE, µV | Zuna RMSE, µV | Spline NMSE | Zuna NMSE |
|---|---:|---:|---:|---:|---:|
| eyes open / proxy-untouched | 5.002 | 4.922 | 4.326 | 1.464 | 1.071 |
| eyes open / proxy-touched | 10.000 | 6.331 | 5.397 | 0.907 | 0.561 |
| eyes closed / proxy-untouched | 5.006 | 5.981 | 5.340 | 1.515 | 1.239 |
| eyes closed / proxy-touched | 35.004 | 5.610 | 5.099 | 0.178 | 0.161 |
| **Pooled 20 seconds** | — | **5.735** | **5.059** | **0.525** | **0.428** |

Lower is better. Pooled RMSE weights all samples and channels equally. Mean-channel NMSE averages per-electrode MSE divided by that electrode's target variance. The pooled row uses each electrode's variance across all four contexts, not the average of the four context-specific NMSEs. The windows and electrodes are not independent replications; no significance test is reported.

*Figure omitted from this public report-only copy.*

### How this differs from the old report

These short-window scores use the **precomparison arrays**: measured targets and interpolation were prepared as whole blocks, while generated outputs were not passed through a newly cropped five-second filter. No disconnected samples were stitched for spectral estimates. This avoids introducing fresh cropped-filter artifacts but is not the old full-recording final-filter endpoint.

For the same selected intervals under the old preparation and the same precomparison scoring, pooled RMSE was 5.740 µV interpolation versus 5.073 µV Zuna. **The prepared targets also change with the corrected pipeline**, so absolute old/new error changes are not a clean, isolated measure of improved model accuracy. Compare Zuna with interpolation within each pipeline. The full old result has not been replaced or promoted.

**These intervals already favored Zuna before the correction.** The short result therefore does not establish that this fix turns the earlier unfavorable full-recording comparison into a favorable one. Across the corrected sample, Zuna improved pooled error but did not improve every electrode; P3 pooled RMSE was slightly higher (4.717 versus 4.707 µV). The blink explanation remains a hypothesis, not a conclusion of this four-window check.

Per-channel errors, target-change magnitudes, short-context band powers, model provenance and failure-free completion evidence are preserved in the JSON report. Band powers from these few seconds are descriptive only.

## Scope and next decision

The demonstrated DC-boundary defect is corrected in the candidate. It does not follow that all filter edges, five-second model seams, ocular artifacts or model limitations are solved. The local candidate is ready for integration into a separately versioned Workbench patch; the installed 10.3.5 app has not been silently replaced.

The next scientific decision should use the complete per-context result, not select whichever condition favors Zuna. If a full corrected comparison is commissioned, freeze its scoring/filter policy first and preserve the original reports. Fresh-session confirmation, sparse-montage testing, denoising studies and live adaptation remain separate tasks; no new recording was needed for this step.

## Files

- [Full machine-readable comparison](short_comparison_result.json).
- [Frozen selection and model settings](short_comparison_plan.json).
- [Regression gate](regression_gate.json) and boundary regression source (supporting file not included in this public copy).
- [Readable regression report](BOUNDARY_REGRESSION_REPORT.md).
- [Independent result verification](INDEPENDENT_RESULT_VERIFICATION.md).
- [Corrected preparation receipt](corrected_preparation_receipt.json).
- Source patch (supporting file not included in this public copy), [change note](BOUNDARY_PREPARATION_CHANGE.md), [design review](design_review.md).
- [Execution status](execution_status.json).

The candidate lives in `candidate_app`; it contains a copied 10.3.5 tree with two changed worker files, not a newly versioned distribution. Do not mistake old release manifests in that copy for a new release certification. The patch and tests are the reviewable change set.

Private EEG-derived material: do not upload or publish without separate privacy review. The input and installed-source hashes were rechecked after inference. Hidden measured electrodes are not clean neural ground truth. Model estimates are not new measurements. The historical BENCH designation remains unchanged: block timing uses an approximate software clock without independent ALS-barcode verification, template coordinates retain the disclosed clipping, and offline filtering and model-context seams can affect results. No clinical validity, clean-signal restoration or prospective validation is established.
