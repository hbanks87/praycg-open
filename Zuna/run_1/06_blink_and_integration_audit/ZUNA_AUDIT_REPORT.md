> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Post-hoc proxy analysis; no independently verified blink labels. Private events, masks and waveform figures are withheld.

# Zuna blink-aware evaluation and integration audit

Private development report — 26 September 2026, America/Chicago.

**Bottom line:** Your blink hypothesis identifies a useful part of the pattern, but this audit also found a reproducible preprocessing defect. Large constant offsets in the recorded EEG become artificial block-edge waves during resampling. The immediate priority is boundary-safe preparation and its regression tests, not another full Zuna run or a request for better cap quality.

The original recording, installed application, frozen recipe, model predictions, evaluation mask and reports were not changed. No new model inference, hardware access or upload was performed. New private diagnostic scripts, masks, figures and reports are confined to this audit folder.

## 1. What was examined

Recording UUID: `RUN_1`.

The completed Alpha 10.3.5 comparison used 12 measured inputs to reconstruct withheld F3, F4, P3 and P4. It processed eight blocks, with 400.21875 seconds evaluated after the original transition guards. The saved predictions and all original evaluated samples were reused. The original mean-per-electrode NMSE reproduced to numerical precision: **0.658757 interpolation versus 1.224085 Zuna**.

This remains a **post-hoc, single-recording, historical BENCH evaluation**. Nothing here promotes the recording to a prospectively validated experiment or claims clean neural ground truth. The old numerical results remain a record of the old pipeline; the newly found preparation defect limits their interpretation as a fair verdict on Zuna itself.

## 2. Blink-like events and your timing hypothesis

A detector was frozen before examining the new reconstruction strata. It used only retained measured Fp1: blockwise 0.5–8 Hz filtering, a threshold of four robust scale units, prominence of two units, at least 0.35 seconds between peaks, and a fixed mask from 0.25 seconds before to 0.50 seconds after each peak. Fz was viewed as corroborating information, not used to select favorable events. Hidden channels and predictions were not used to build the mask.

The threshold was 25.79 microvolts after filtering. Visual inspection showed a mixture of large frontal transients, recovery lobes and smaller ambiguous events. Therefore these are **proxy peaks, not confirmed blinks or a validated blink count**.

- Eyes-open scored periods contained **58 proxy peaks**, versus **8** during equally long eyes-closed periods.
- During eyes-open seconds 5–20, the rate was **23 proxy peaks/minute**. During seconds 20–55, it was **15/minute**.
- Substantial later activity remained. Only two eyes-open blocks immediately followed eyes-closed blocks; eyes-open block 4 followed another eyes-open block.

This pattern is consistent with more early eyes-open frontal transients, but timing and scalp EEG alone do not prove blink causation. The original first five seconds were already excluded.

*Figure omitted from this public report-only copy.*

The first eight chronological events were plotted without hidden-channel or prediction traces. No events were manually removed after seeing model performance. The full overview also reveals the repeated terminal preprocessing artifact discussed below.

## 3. Whole model contexts matter

The model normalizes every five-second context using a common scale from retained channels. A transient can therefore affect a whole model context, not only the short interval containing its peak. Both event-local and whole-context masks were evaluated. Both methods always received exactly the same scoring mask.

| Evaluated subset | Seconds | Interpolation RMSE, µV | Zuna RMSE, µV | Interpolation NMSE | Zuna NMSE |
|---|---:|---:|---:|---:|---:|
| Original complete evaluation | 400.22 | 5.734 | 7.753 | 0.659 | 1.224 |
| Outside short proxy-event masks | 356.55 | 5.596 | 6.893 | 0.982 | 1.550 |
| Contexts touched by a proxy mask | 160.22 | 5.993 | 10.536 | 0.493 | 1.560 |
| Contexts untouched by proxy masks | 240.00 | 5.555 | 5.111 | 0.942 | 0.815 |

Lower error is better. RMSE is pooled across samples and four targets; NMSE is calculated separately per target electrode and then averaged. They are different summaries. Each stratum has a different target variance; NMSE values across strata are not a direct measure of contamination severity.

In untouched contexts, Zuna had **about 8% lower pooled RMSE**. However, this subset contained 180 seconds eyes closed and only 60 seconds eyes open—just 30% of the eyes-open evaluation. One eyes-open block contributed only five seconds. Zuna was better in six of eight blocks within this subset, not every block.

Within the 60 seconds of untouched eyes-open contexts, RMSE was 5.985 µV for interpolation and 5.670 µV for Zuna. Excluding only the short transient intervals did **not** reverse the overall baseline-favored outcome.

This is an interesting descriptive sign of context sensitivity, not a validated benefit, proof of blink removal or justification for a retrospectively selected “use Zuna where it wins” strategy. Untouched contexts are not guaranteed artifact-free, and the preparation defect also affects these analyses.

*Figure omitted from this public report-only copy.*

## 4. Confirmed preprocessing defect: offset-to-edge conversion

The prepared frontal signal showed an almost identical large terminal waveform in every block. A direct check against the original XDF reproduced all saved prepared inputs **bit-for-bit**, confirming that this was the actual pipeline, not a plotting error.

The worker resamples each block using zero boundary padding before applying its high-pass/band-pass filter. Recorded channels have substantial steady offsets; raw Fp1 block means were about −41,700 to −42,900 µV. Abruptly treating a nonzero endpoint as zero creates an artificial boundary transition. Subsequent filtering turns that transition into ringing.

In a private diagnostic calculation, subtracting only each channel's constant block mean **before** the otherwise unchanged resampling and filtering reduced prepared Fp1 last-five-second peaks from approximately **6,720–7,581 µV to 57–208 µV**. The difference was reproduced by processing the constant offsets alone, with residual error below 0.000000006 µV. This separates the offset-processing effect from actual blink or other time-varying activity.

The original five-second guards do not remove all of its influence. Across the four held-out targets, the isolated offset component inside the original scored mask had RMS **0.661–0.791 µV** before the final comparison filter. After that extra filter it had RMS **1.599–1.939 µV**, with localized absolute maxima **33.36–40.32 µV**, depending on block. These are differences attributable to the isolated constant-offset processing, not estimates of biological artifact or total model error.

Synthetic controls confirmed the mechanism without human EEG: adding channel-specific constants to otherwise identical oscillations changed the old prepared output, including its scored interior. A private candidate—per-channel mean subtraction before resampling—restored constant-offset invariance within approximately **1.43 × 10⁻¹⁰ µV**, and a pure-constant input produced zero after the candidate route.

**The candidate is a tested private diagnostic, not an installed fix.** It removes an arbitrary constant before a high-pass operation; it does not establish that all remaining signal is neural, fix every boundary effect, or show that Zuna's predictions improve. A production patch needs explicit boundary handling, reference/leakage checks and regression coverage before a new comparison.

This numerical finding supersedes the earlier provisional source-only observation that no coding issue had been identified.

## 5. Other engineering findings

- **Leakage safeguards passed the tested cases.** Finite replacement of hidden measurements in synthetic eight-block data left retained inputs, reference, timestamps, masks, all 96 full-context token arrays and normalization statistics unchanged. This tests preparation independence, not newly rerun model outputs.
- **Scaling and units passed.** The production inverse expression recovered synthetic signals within 0.00000744 µV. Actual spline microvolt/volt conversions passed. Seven grouped checks, including nine existing unit tests, passed; these do not override the separately discovered boundary defect.
- **Coordinate encoding matched pinned upstream behavior** for 4,401 tested vectors. Cz/Pz clipping remains explicitly disclosed; coordinates should not be rescaled to improve the score.
- **Context seams are measurable.** At 72 fully scored interior joins, the median absolute step before comparison filtering was 0.734 µV measured, 0.689 µV interpolation and 2.677 µV Zuna. After comparison filtering the Zuna median was 1.289 µV. This survives removal of scoring-entry/exit seams, but does not prove seams cause all reconstruction error.
- **The final filter changes the outcome magnitude, not its full-data direction.** Before that filter, full-data RMSE was 5.752 µV interpolation versus 9.979 µV Zuna; afterward it was 5.734 versus 7.753. The pre-filter branches have different effective bandwidths, so this is an operational sensitivity check, not a cleaner alternative endpoint.
- **Input clipping differs from pinned upstream.** The upstream FIF route clamps normalized inputs to [−1,1]; PRAYCG does not. In the actual saved inputs, 0.0459% of retained values exceeded this range. No retained tokens were accidentally flagged as missing by the model's exact zero-sum convention. Reassess clipping only after boundary-safe preparation; the percentage is not a rejection threshold.
- The eight tiny padded tail contexts contained only 3–7 real samples each and had no directly scored output. However, several scored samples per block lie just beyond nominal second 55, inside the preceding 55–60-second model context. Whole-context eligibility and subsequent filtering need explicit treatment.

The pinned upstream FIF path uses different normalization/reference defaults. Copying those defaults with hidden measured channels still present could leak their reference contribution or amplitude statistics. A target-free benchmark must not import them blindly.

## 6. Decision and next bounded work

**Do not spend another hour on the unchanged pipeline.** The engineering defect is a stronger immediate reason to pause new model comparisons than trying to choose a more favorable scoring subset.

1. Implement and regression-test boundary-safe preparation in a separately versioned patch. Preserve the old recording and reports. Freeze how offsets, padding, filtering, true acquisition gaps and incomplete contexts are handled.
2. Rebuild only the prepared diagnostic data first. Require constant-offset invariance, stable interior pass-band behavior, input-only referencing, unchanged clock evidence, no cross-gap processing and explicit edge/context coverage.
3. Recompute the fixed blink proxy on the corrected preparation as a separately labeled sensitivity analysis; retain today's masks and results. Do not tune detection from reconstruction scores.
4. Then authorize one short, fixed comparison using both eye conditions and both proxy-activity levels. Keep original weights/seed policy and report every result. A longer-context alternative is justified only as a declared pipeline sensitivity; normalization and random trajectories also change with context length. Input clipping is conditional on remaining excursions.
5. Only if that passes engineering checks should a new full comparison run. Sparse-input, controlled-added-artifact, fresh-session and decoder studies remain distinct later stages. Current results do not establish denoising or live readiness.

Interpolation remains the default while this is resolved. The modest untouched-context signal is worth preserving, not promoting to a confirmed advantage. No additional recording or higher cap-contact score is required for the immediate correction work.

## 7. Reproducibility, files and privacy

The frozen mask plan, independent review and all outcomes are included, not only favorable subsets:

- [Frozen proxy plan](proxy_plan.json), detected proxy events (supporting file not included in this public copy), mask arrays (supporting file not included in this public copy).
- [Complete sensitivity results](blink_sensitivity_results.json) and [compact tables](metrics_table.md).
- [Methodology and independent numerical verification](methodology_review.md), [method-blind visual review](visual_proxy_review.md).
- [Engineering checks](engineering_checks.md), [saved-input checks](additional_saved_input_checks.md).
- [Source audit](integration_source_audit.md), [boundary defect audit](boundary_audit.md), [boundary numerical evidence](boundary_audit.json).
- [Final-filter sensitivity](filter_sensitivity.json), [strictly interior seam check](interior_seam_check.json).
- Full retained-only proxy overview (supporting file not included in this public copy).

Scripts are private analysis tools, not application changes. Artifact hashes are recorded in `audit_manifest.json`. Figures and arrays contain private EEG-derived information and should not be uploaded or published without a separate privacy review.

Original XDF SHA-256: `1937dad998f3cf265df32d3e235429a877b3f650f64c4ffde1b7e3d642b7c303`.

Original prediction-array SHA-256: `44be66d1e9f5b2b7395d74c7fd1f5ce546afaca20942dc8f3bd7f33ea0c8190d`.

### Scientific limits

There is one recording and no independent participant replication. The eye-state labels follow software observations; actual compliance and physical onset were not independently measured. Timing uses the previously disclosed log-based approximation. Blink proxies do not separate all ocular, movement and neural components. Filtering can spread transients beyond masks. The model estimates missing signals; withheld measurements are not clean neural ground truth. No clinical, prospective-validation, clean-signal-restoration, thought-decoding or population-level claim is supported.
