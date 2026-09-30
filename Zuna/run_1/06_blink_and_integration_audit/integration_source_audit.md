> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Post-hoc proxy analysis; no independently verified blink labels. Private events, masks and waveform figures are withheld.

# Private Zuna integration source audit

Date: 2026-09-26 (local). Scope: installed PRAYCG Alpha 10.3.5 and pinned Zuna 1.1.6; no model inference, app changes, acquisition, uploads, or original-recording edits.

Recording: `RUN_1`. Completed guided comparison: `[PRIVATE_ID_REMOVED]`. This is a post-hoc, single-recording, historically BENCH comparison. Engineering correctness does not establish recovery of clean neural activity.

## Bottom line

**Update after numerical boundary investigation:** the initial source-only review below was insufficient to detect a preprocessing defect. A subsequent synthetic and exact-recording test confirmed that zero-extended resampling of large constant channel offsets creates severe block-edge artifacts, some of which remain inside the fixed evaluation mask. See [the superseding boundary audit](boundary_audit.md). Correcting and validating that preparation path now takes priority over context-length, clipping or normalization experiments. No model rerun has been performed.

The source review also identifies meaningful differences from the pinned upstream FIF pipeline, especially per-window scalar normalization, context length, and effective filtering. These differences make the completed result evidence about PRAYCG's particular reconstruction pipeline, not an exact reproduction of an upstream benchmark. They do not establish that the recording or electrode contact was inadequate.

All 14 source/dependency-description hashes recorded in the completed development plan match the currently installed app files. The installed pinned `config_infer_fif.yaml` and `eeg_data.py` also match the exact hashes recorded in the adapter contract. This source review is not an independent rehash of every model weight or an exhaustive software audit.

The companion numerical audit and blink-stratification report should be read with this document. The source reasoning below does not itself identify real blinks or demonstrate the model's output under a changed pipeline.

## Findings

### 1. Coordinate encoding is intentional and pinned, but loses some geometry

PRAYCG uses MNE head coordinates in metres, the same reviewed coordinate rows for the spline and model, then bins model coordinates using float32 subtraction/division/multiplication, integer truncation and clamping. The pinned FIF configuration selects 100 bins over -0.12 to +0.12 m. The prior engineering parity test covers coordinate encoding and token order, not full pipeline equivalence.

The actual template Cz z coordinate is 0.140199494 m and Pz is 0.126672924 m, exceeding the upper encoding bound by about 20.2 and 6.7 mm respectively. Their z bins are consequently both 99. The spline receives continuous coordinates; the model receives the quantized/clipped representation. That is a model-input representational limitation, disclosed and operator-reviewed, not evidence of a unit-conversion bug. Do not shrink or move the head coordinates until a favorable outcome appears. Actual digitized coordinates are not available for this run.

Sources: geometry and spline construction (supporting file not included in this public copy), adapter encoding (supporting file not included in this public copy), pinned upstream bounds (supporting file not included in this public copy), upstream bin function (supporting file not included in this public copy).

### 2. Scalar scaling has a plausible blink interaction; that is not a proven bug

For each five-second context, PRAYCG computes one mean and population standard deviation across all 12 retained electrodes and samples. It supplies `(x - mean)/(10 * std)` and reverses the transformation with those same retained-only values. Hidden target rows are appended as exact zeros after statistics are computed. With the retained-channel average reference, the mean is approximately zero by construction. The inverse operation is algebraically consistent; its numerical precision is covered by the companion engineering tests.

A large retained frontal transient can increase the common standard deviation, reducing the normalized amplitude of every other electrode in that context. The model's output is then multiplied by that common scale. This is a plausible mechanism linking frontal transients to reconstruction behavior; it is not proof that it caused the observed errors. Directly inspect retained-window scales and blink-like-event overlap rather than infer a mechanism from overall scores.

The pinned upstream FIF default instead calculates a mean and standard deviation per channel per segment, adds `1e-6` to each standard deviation in volts (equivalent to 1 microvolt), and divides by 10 before inference. PRAYCG has no matching additive 1-microvolt regularizer. The separate upstream raw preprocessing route uses global scalar normalization, so the statement that *all* upstream routes are per-channel would be inaccurate.

For genuinely absent electrodes, their own mean/standard deviation is unknown. Copying per-channel normalization and restoring target amplitude from the withheld recording would invalidate the missing-channel test. Any alternative must define target-free output scaling before evaluation, or explicitly change the question to normalized waveform shape rather than physical-amplitude reconstruction. A simple normalization swap is not yet a scientifically complete experiment.

Sources: PRAYCG normalization (supporting file not included in this public copy), inverse scaling (supporting file not included in this public copy), FIF normalization (supporting file not included in this public copy), separate raw global route (supporting file not included in this public copy).

### 3. Reference and target masking are intentionally target-free

Each channel is independently resampled/filtered. The digital reference is the mean of the 12 retained channels, subtracted from both retained inputs and held-out evaluation targets. The adapter receives no target waveform argument. The spline is also built from retained data plus zero target placeholders. These are coherent safeguards against target leakage.

The upstream low-level model recognizes dropped tokens from a zero token sum, so an explicit extra target-mask argument is not missing from PRAYCG's `sample()` call. Exact zeros in target tokens serve the intended model convention. The zero-sum heuristic could also recognize an accidentally zero-sum retained token; the companion actual-token check should establish whether that happened in this recording.

The pinned upstream FIF loader calculates reference and normalization before its bad/drop mask. Feeding original hidden channels to that route without modification could leak their information through reference or inverse scaling. Upstream functionality must not be mistaken for a leakage-free benchmark recipe for every masking scenario.

Sources: retained-only preparation (supporting file not included in this public copy), target-free inference call (supporting file not included in this public copy), upstream dropout convention (supporting file not included in this public copy).

### 4. Filtering is disclosed, but equal final filtering is not equivalent end-to-end filtering

Each evaluation block is independently resampled to 256 Hz and receives a fourth-order 0.5-40 Hz Butterworth SOS forward/backward filter. The model consumes those prepared retained inputs. A second identical filter is applied independently to the measured, spline and generated branches before comparison.

The measured and linear-interpolation branches consequently have two explicit passes. The generated branch is a nonlinear model of prefiltered inputs followed by an output pass. Equal output filtering does not establish identical effective transfer functions. The resulting score is valid for that disclosed operational definition, but cannot be called an unfiltered reconstruction score or generic denoising validation. The pinned upstream FIF defaults use a 0.5-Hz highpass, no lowpass, and FIR filtering; they are not identical to PRAYCG's bandpass route.

The NPZ preserves the precomparison target, spline and model arrays. Recompute the same masked metrics on these saved arrays to determine how much the extra reporting filter affects the conclusion, without new inference. That sensitivity result must not replace the original endpoint. Neither filter configuration is causal: future samples within a block can influence earlier output, so this offline execution is not evidence for live timing-safe use.

Sources: preparation filter (supporting file not included in this public copy), comparison filter (supporting file not included in this public copy), explicit disclosure and saved branches (supporting file not included in this public copy), FIF filter defaults (supporting file not included in this public copy).

### 5. Five-second contexts can create seams; upstream seam correction is not a ready fix

The completed comparison used 16 sampling steps, cfg 1, float32, fixed seed 20260924 and five-second contexts. Each of the eight observed blocks starts a fresh context sequence. No model context crosses a block boundary. There were 96 full 1280-sample contexts plus eight very short tails: one with 3 samples, three with 5 and four with 7. Each tail was reflected to 128 samples, generated, then truncated back to its original length. The final five seconds of each block are excluded from scoring, so the tail predictions themselves are not scored directly. The second blockwise zero-phase filter could nevertheless spread an edge effect inward; this can be assessed using the saved precomparison arrays.

The pinned FIF configuration defaults to ten-second contexts and truncates the final remainder down to complete 32-sample tokens instead of this reflected minimum-half-second padding. Both routes use independently processed contexts; the difference is not simply continuous versus discontinuous inference.

Upstream hybrid seam correction anchors *partially* missing segments to adjacent original measurements. It explicitly skips an entirely missing channel, which is our task. Turning it on is therefore not a demonstrated remedy for our five-second whole-channel context seams. Anchoring to held-out measured targets would be impermissible.

Sources: window construction (supporting file not included in this public copy), padding (supporting file not included in this public copy), FIF final-segment handling (supporting file not included in this public copy), upstream seam skip (supporting file not included in this public copy).

### 6. An additional input-clipping difference should be disclosed

The pinned FIF path divides normalized input by 10 then clamps it to [-1, 1]. PRAYCG's retained-scalar preparation does not clamp. This is an additional implementation difference not explicitly enumerated in the short contract list. It is not automatically a bug, particularly if no actual inputs exceed those bounds. Count out-of-range values using the exact saved-window normalization before considering an experiment. Adding clipping to a run whose inputs are already within bounds cannot explain an improvement.

Sources: FIF clipping (supporting file not included in this public copy), PRAYCG token scaling (supporting file not included in this public copy).

## Bounded follow-up, not a parameter search

**Superseded priority:** the confirmed boundary/DC artifact described in the supplementary audit must be resolved and numerically revalidated first. The alternatives below were written before that finding and are deferred, not recommended immediate model runs.

First complete all zero-inference diagnostics: blink-like stratification, window-scale/transient association, boundary-versus-interior errors, precomparison-versus-final-filter metrics, and actual token clipping/zero-sum checks. Preserve original scores and every diagnostic mask. Lower-blink intervals are not clean neural ground truth.

At most two short inference alternatives are presently source-justified, and neither should run automatically from this audit:

1. **Ten-second context sensitivity**, only if saved-output diagnostics implicate context boundaries. Hold weights, steps, coordinates, reference, filters and target-free normalization rule fixed. Use preselected intervals and retain the five-second result. Longer context also changes the normalization window and random trajectory; interpret it as a context-length pipeline test, not proof that seams alone caused any change.
2. **Pinned [-1,1] input-clipping sensitivity**, only if actual retained tokens exceed those bounds. Use exactly the same five-second contexts and seeds, disclose which inputs changed, and keep all results. If none exceed the limit, omit this alternative entirely.

A per-channel-normalization experiment is deferred until target-free amplitude restoration is specified. No coordinate rescaling, target-informed gains, target-informed time shifts, seed selection, or post-hoc winner-only reporting is justified.

If source and numerical checks pass but no worthwhile advantage appears, keep interpolation as the default and Zuna optional/experimental. An apparent reduction in blink fidelity alone cannot establish cleaning: it could also be loss of useful signal or unsupported generation.

## Provenance and limits

Inspected installed package: `[LOCAL_PATH_REMOVED]`.

Pinned upstream evidence hashes matched:

- `config_infer_fif.yaml`: `5b7cd9723dc25b09743670ed133ad99d709936e7348d33d6d9ce5d6b007ca4ee`.
- `eeg_data.py`: `170414f7375a47b83bdc4143a3cf2625ef25af1a0a4226263e1aea884398537f`.

Reviewed actual provenance: [completed model provenance](../04_guided_comparison/zuna_provenance_v1_0.json).

This audit makes no clinical, population, prospective-validation, full-upstream-parity, clean-ground-truth, or real-time-readiness claim. No model weights were loaded or model inference performed for this source audit.
