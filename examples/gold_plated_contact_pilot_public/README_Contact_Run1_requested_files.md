# Contact Run 1 requested anchor/MRED files v1.0

This folder provides the requested files for the Contact PRAYCG run:

1. `Contact_Run1_predeclared_anchors_CONCEPTUAL_NOT_RUNNER_REGISTERED_v1_0.json`
   - Conceptually predeclared Contact anchor family reconstructed into a PRAYCG anchor JSON.
   - Important: this is NOT a true runner-registered LOCKED anchor file for Contact Run 1. The Contact event log/run config recorded no loaded anchor file.
   - Use this as a review/future-freeze scaffold. Verify exact rendered MP4 timecodes before using in PRAYCG1.9C/2.0.

2. `Contact_Run1_MRED_familiarity_covariates_v1_0.csv`
   - MRED familiarity/novelty covariate table.
   - The PRAYCG1.9 Contact run did not directly collect all MRED familiarity fields, so values are blank and editable.

3. `Contact_Run1_MRED_scene_map_v1_0.csv`
   - Scene map CSV for Contact anchors.
   - Times are analysis-aligned estimates and require frame-accurate manual review on the final rendered Target MP4.

4. `Contact_Run1_annotation_windows_v1_0.csv`
   - Analysis annotation window table containing pre-windows, peak-search windows, theta windows, claim level, subjective note links, and nearest CandidateLocal K_HT-topo/MRED events.

5. `Contact_Run1_feature_table_contact_time_resolved_feature_frame_v1_0.csv`
   - Time-resolved feature frame produced by the Contact Master Suite analysis.

6. `Contact_Run1_candidate_local_kht_topo_mred_event_table_v1_0.csv`
   - Included as a convenience reference for MRED/K_HT-topo event interpretation.

## Status

Anchor classification: conceptually predeclared / not runner-registered.

Strict future use rule:
- Open the final rendered Target MP4.
- Verify each `rendered_time_sec_estimate` frame-by-frame.
- Change `locked_for_runner_use` only after exact rendered timecodes are verified.
- Run the MediaPrep v1.7A anchor finalizer to generate a true `*_LOCKED.json`.
- Load that LOCKED file in PRAYCG1.9C/2.0 before acquisition.

## Media context

- Video duration: 299.96663329996665 sec
- FPS: 29.97
- Content start offset from fullscreen ALS prefix: 1.234567901234568 sec
- Cue count: 99
- Expected override sum: 515
