# Zuna integration and compatibility decisions — Alpha 10.3.7

## Decision

Integrate the verified boundary-preparation correction. Retain the audited PRAYCG adapter choices rather than introducing an untested preprocessing variant or silently claiming reproduction of the entire upstream pipeline.

The pinned model, weight revision, channel selection, float32 inference, 16 sampling steps, cfg 1.0, retained-input-only normalization and explicit geometry review are unchanged. The immutable adapter contract `tools/Zuna_EEG_Reconstruction_v1_0/zuna_adapter_contract_v1_1.json` describes these existing choices. Its coordinate encoding follows reviewed upstream inference configuration, not proof of every training coordinate. Template coordinates are not individualized electrode digitization; disclosed clipping still requires the existing review.

## Corrected preparation

Policy identifier: `PRAYCG_ZUNA_OFFLINE_BLOCK_CENTER_LINE_RESAMPLE_V1_0`.

Before polyphase resampling to 256 Hz, subtract each electrode's own mean within its independent continuous preparation segment and use line-padded boundaries. Canonical contiguous float64 preparation prevents array-layout-dependent reductions. Each electrode is prepared independently before the retained-only reference is formed: hidden target values must not influence model inputs, normalization, geometry, selection or seeds.

The declared 0.5–40 Hz filtering remains explicit. No segment crosses a known preparation boundary or repairs missing samples. Independent model contexts and reflected final padding remain disclosed; this correction does not eliminate all model seams. Full-segment centering and zero-phase filtering use future data and therefore cannot be reused as an already-validated live pipeline.

Preparation receipts identify the method and source/input bindings. Resume compatibility includes preparation identity, not merely a recording filename. Original contracts and reviewed recipes are not edited to manufacture compatibility. Guided preparation prepared with older dependencies must be repeated explicitly under current software before a new execution; old completed results remain readable as historical evidence.

## Comparison meanings

Three branches are distinct:

1. **Measured:** withheld recorded electrodes after declared preparation; not clean neural ground truth.
2. **Spherical spline:** conventional interpolation of those withheld locations from retained electrodes.
3. **Zuna:** model-generated estimates at those locations; not new physical measurements.

The primary endpoint applies the same final comparison filter to each branch. Their total filter histories are not identical: measured/interpolated signals already underwent preparation filtering, while raw model output did not. The companion endpoint before this final filter is therefore always reported; users must not select whichever endpoint favors the model.

Reports describe overall, eyes-open and eyes-closed groups, all evaluation blocks and electrodes. RMSE is expressed in microvolts; normalized error divides each channel's mean squared error by its measured variance before averaging across all four declared electrodes. In the new diagnostic summaries, one undefined electrode makes that mean not estimable; supported individual errors remain visible. These measures have different weightings. A zero-variance or unsupported denominator is undefined, not zero. Historical compatibility fields retain their stated earlier aggregation conventions rather than being silently rewritten.

Spectra use complete contiguous windows within retained runs, never stitched fragments across gaps or excluded times. Coverage, window support, band-power differences and eyes-closed-minus-eyes-open alpha contrast are descriptive. Missing conditions, too-short groups and unsupported spectra produce explicit not-estimable states. A minimum support rule is an engineering safeguard, not a guarantee of statistical adequacy.

All conditions remain visible regardless of which method wins. No new blink detector, private historical masks, favorable-seed selection, hidden-target correction or outcome-selected exclusion is shipped. Lower error against a contaminated target cannot establish clean-neural recovery; disagreeing with a blink cannot establish successful denoising either.

## Privacy, scientific status and limits

Summary metrics and provenance accompany the module report and established bundle workflow. Private waveform arrays/traces remain separate full-telemetry artifacts. Public-oriented output still needs human privacy review; metrics are not automatically anonymous. The release archive contains no participant recording, private comparison report, model checkpoint, model weights or local Python environment.

Historical BENCH, post-hoc, timing approximation and QC cautions remain unchanged. Repeated windows, channels and blocks are not independent participants. No significance, clinical validity, prospective validation or general Zuna advantage is inferred by this integration.

The source of the method's implementation is PRAYCG's versioned worker/adapter/reporting code; upstream model attribution and notices remain in the existing [methods guide](ZUNA_METHODS_ALPHA_10_3_0.md) and [master attribution](../CITATIONS_AND_ATTRIBUTION.md). This document does not resolve historical upstream licensing ambiguities.
