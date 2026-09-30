> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Post-hoc proxy analysis; no independently verified blink labels. Private events, masks and waveform figures are withheld.

# Supplementary boundary/DC audit: confirmed preparation artifact

Date: 2026-09-26 (local). Private, post-hoc engineering diagnostic for recording `RUN_1`, completed comparison `[PRIVATE_ID_REMOVED]`.

## This changes the priority

**A genuine preprocessing defect is confirmed.** PRAYCG resamples each block with zero extension before removing large per-channel constant offsets. The discontinuity against zero creates large endpoint transients that the subsequent bandpass does not fully confine to the discarded margins. The observed near-identical block-end transients cannot be treated as evidence of repeated human blinks.

This finding supersedes the initial source-only audit's provisional statement that no coding defect had been identified. It does not prove that all Zuna errors came from this defect or that corrected Zuna predictions will beat interpolation. The original recording is intact. The original scores still describe the executed computation but are materially confounded for evaluating the intended EEG reconstruction method.

## Evidence and exact reproducibility

1. The original 8.4 MB XDF was read without clock synchronization or timestamp de-jittering, using the run-bound outlet and existing reviewed timestamp mapping.
2. Each actual block was processed with the **unchanged installed worker**. Its retained arrays matched the saved model inputs exactly: maximum absolute difference **0.0 microvolts in every block**.
3. A diagnostic candidate subtracts each channel's own block mean **before** the unchanged resampling, bandpass and retained-only reference. Original samples are never changed on disk.
4. The difference between original and candidate prepared arrays equals the same worker's response to the blockwise constant offsets alone. Maximum residual across all blocks is below **6e-9 microvolts**. This is a linearity control, not a fitted correction to model predictions.
5. A separate synthetic signal test adds known channel-specific constant offsets to otherwise identical small oscillations. The current worker creates an **8,720 microvolt** maximum difference, including **8.68 microvolts** within the fixed 5-55-second interior. No blinks were simulated.
6. With channelwise centering before resampling, the same synthetic translation-invariance test has a maximum difference of **1.43e-10 microvolts**. Pure constant channels become exactly zero after centering, resampling and bandpass. Such flat data should remain ineligible for model inference; this diagnostic does not bypass flat-signal safeguards.

Source mechanism: resample then filter (supporting file not included in this public copy). No `padtype` is supplied to `resample_poly`; its zero-extended boundary behavior acts on the large raw offsets. The following zero-phase filter spreads the edge response in time.

## Size in this recording

Fp1's raw block means are approximately **-41,715 to -42,893 microvolts**. These are constant electrical offsets, not the amplitude of brain oscillations and not, by themselves, evidence of poor contact.

Across the eight blocks:

| Diagnostic | Observed range |
|---|---:|
| Prepared Fp1 peak magnitude in final five seconds, current worker | 6,720-7,581 microvolts |
| Same prepared region after diagnostic pre-resampling centering | 57-208 microvolts |
| Constant-offset-induced component at Fp1 inside original scored region | maximum 6.72-7.60 microvolts; RMS 0.790-0.895 microvolts |
| Constant-offset-induced component across all four held-out targets inside original scored region | maximum 9.38-11.25 microvolts; pooled channel/sample RMS 0.661-0.791 microvolts |
| Same held-out-target component after the additional comparison filter | maximum 33.36-40.32 microvolts; pooled channel/sample RMS 1.599-1.939 microvolts |

These are ranges of per-block statistics, not confidence intervals. The latter two rows explicitly concern the actual comparison targets **F3, F4, P3 and P4**, rather than only the frontal proxy. They measure a deterministic preparation sensitivity, not Zuna-versus-spline error or improvement. The extra filter does not necessarily reduce a finite-block edge transient; it can spread the response farther into the retained interior.

The current five-second guard removes the worst peaks but is **not sufficient to make this particular offset-related response negligible**. A small number of scored samples also share the 55-60-second model context containing the large edge artifact. Since Zuna is nonlinear and context-dependent, subtracting an estimated artifact from saved predictions would not produce the predictions of a corrected pipeline.

## Candidate correction and its limits

The smallest demonstrated correction is per-channel constant centering before resampling. It uses each retained channel only to transform that retained channel. Held-out channels can be centered independently for constructing evaluation targets, but their means must never contribute to retained-channel reference, normalization, model input or output scaling. The retained-only average reference remains unchanged in definition.

Do **not** restore the removed means after a highpass/bandpass intended to reject DC. No target-derived gain or time shift is involved. A full-block mean is suitable only for this offline preparation; it is not a causal online preprocessing rule.

This correction removes the demonstrated large-DC mechanism, not every possible filtering edge effect. A release-quality implementation should also assess endpoint extension and available continuous context, and select padding/guard policies using synthetic offset, ramp, oscillation and impulse tests rather than choosing whatever improves Zuna's score. Never cross verified acquisition gaps merely to acquire more context.

## Revised next step

1. Preserve the old reports and explicitly annotate this preparation limitation.
2. Use a separately versioned candidate preparation path for any subsequent implementation; keep the original recording and prior recipe immutable. This diagnostic audit has not changed the installed application.
3. Add regression tests for DC translation invariance, retained/hidden separation, known waveform preservation, output alignment, gap boundaries and guard adequacy. Repeat model-free diagnostics on all eight real blocks.
4. Revisit blink-like detection on the corrected prepared frontal signal. Endpoint-generated events must not be described as physiological blinks. Keep the initial proxy analysis as an audit trail rather than silently replacing it.
5. Only after these checks, freeze a small corrected-pipeline diagnostic comparison. Do not run an entire hour-long comparison merely because the preparation defect is established, and do not expect a favorable outcome in advance.

Normalization, longer contexts and input clipping should not be tuned simultaneously with the boundary correction. The corrected pipeline needs actual new model predictions; old checkpoints cannot be relabeled or algebraically corrected as equivalent.

## Files and provenance

- Reproducible diagnostic (supporting file not included in this public copy)
- [Machine-readable results](boundary_audit.json)
- [Original source audit, now annotated](integration_source_audit.md)

XDF SHA-256 was verified before and after, matching the reviewed recipe: `1937dad998f3cf265df32d3e235429a877b3f650f64c4ffde1b7e3d642b7c303`.

Installed worker SHA-256 was verified unchanged before and after: `80ca30c820144982f4d145b60bc16d090c354f43c5b05b03a87508f1d2ddab30`.

Only private diagnostic scripts/reports were created in the workspace. No app/source code, recipe, original recording or saved model predictions were changed. No model weights were loaded, no inference was run, and nothing was uploaded.
