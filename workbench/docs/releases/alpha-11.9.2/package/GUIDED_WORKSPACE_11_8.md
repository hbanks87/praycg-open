# Guided workspace — PRAYCG Workbench Public Alpha 11.8.0

This release improves entry, source visibility and inspection around existing analysis services. It does not add an automatic cleaner, redefine a scientific endpoint, change acquisition thresholds or give an AI model control of a participant protocol. No PiEEG code was copied. The new guided and browser-viewer features add no dependencies.

Use [INSTALL_WORKFLOW.md](INSTALL_WORKFLOW.md) for installation, runtime preservation and existing study workflows. The seven delivered features are described below. [BUILD_REPORT.md](BUILD_REPORT.md) is the authority for the checks actually completed; this guide is not a claim of universal validation.

## 1. Start with a purpose

Home offers **Run a study**, **Inspect a recording** and **Try an example**. They lead to existing study preparation, saved-recording inspection or an isolated simulation. Advanced tools remain accessible.

**Try an example** asks where to write new files, creates a labeled **SIMULATED** source with generated channels and an intentional timestamp gap, and opens inspection. It uses no hardware or AI provider and does not replace the active study, recording, settings or acquisition configuration. Its participant label denotes simulation, not a person. Synthetic results are not evidence about real acquisition or physiological preservation.

## 2. Keep the source visible

The persistent context header shows the selected source and available recording/stream, participant, channel, unit, interval and processing metadata. Unknown participant identity is not inferred from filenames, channel names or task titles. A saved recording is distinct from current equipment and from a live/replay viewer. Cached details are tied to the selected source and are not silently reused for a different recording.

Use **Inspect saved source…** to read source metadata and samples in the background. Reading a source does not establish quality or run the current analysis plan.

## 3. Freeze and compare identical samples

1. Open a saved recording or compatible saved review. Check the source, stream, recorded channel labels and units.
2. Choose a display channel and enter an interval in **Seconds from recording start**. Choose a destination for separate inspection files, then **Freeze interval**.
3. All channels of that stream are frozen together, preserving multichannel recipe context. The channel chooser changes only the display; changing the stream or interval requires another freeze.
4. Leave **None — original only**, or explicitly select an existing current-recipe preview. Optionally **Select receipt…** for an existing reviewed candidate.
5. Choose **Compare frozen samples**. Inspect **Same-sample traces** and **Evidence and limitations**; no recipe or candidate is adopted automatically.

The immutable snapshot records source identity, selected stream/channel indices and units, explicit participant metadata, interval, source sample indices, timestamps, declared segments, exclusions and processing lineage. It saves sample/timestamp hashes and an internal identity digest; later loading checks arrays and metadata together. A changed source or invalid snapshot is rejected. Hashes detect inconsistent data; they are not a digital signature or proof of scientific validity.

The freeze limit is 600 seconds and two million channel-values. Strictly increasing finite timestamps are required; invalid clock ordering is not repaired. Gaps, unsupported samples and selected exclusions remain explicit. Raw sample values are not overwritten by exclusion or processing.

A reviewed candidate must be bound to the same source, stream, annotation state, channels, units and exact selected timestamps. Unaligned candidates are rejected, not silently interpolated. Available branches are compared on the same intersection of supported samples. An absent candidate remains absent; the original recording is never relabeled as a cleaned candidate.

Current previews use the existing Signal Review recipes and support rules. They are not a replay of a historical locked derivative. A short window may be useful for original-waveform inspection but insufficient for filtering: current defaults retain their minimum continuous-support and edge-guard requirements. No requirement is relaxed to make a plot appear. Raw-only inspection preserves declared native units; EEG processing retains its existing channel/unit prerequisites.

The display uses shared amplitude scaling and gap-aware, bounded drawing. Display thinning is not analysis input. Original/current/candidate/difference views are inspection aids; a smaller, smoother or less noisy-looking candidate does not establish better physiological fidelity. Original minus candidate is a calculated difference, not proof that every removed value was artifact.

Closing or cancelling inspection does not kill an in-progress numerical worker. It can finish writing a separate derivative, but a cancelled or stale result is not automatically selected. Original recordings, plans and previous outputs remain unchanged.

## 4. Choose a research question

**Choose your question** exposes these routes:

- **What is in this recording?** — source inspection.
- **What did processing change?** — frozen comparison.
- **What changed around an event?** — existing event and time–frequency tools.
- **How do conditions compare?** — existing plan/module configuration.
- **What did the analyses find?** — saved results and processing history.

Each route states its prerequisites. Navigation alone does not start an analysis. Event conclusions still need identified timing; condition comparisons need suitable labels and design. Fixed order, repeated samples, confounds, missing support and post-hoc choices do not disappear because a workflow is easier to reach.

## 5. Review numerical and preservation evidence together

A frozen comparison reports matched numerical changes, support, source identities, processing provenance and any available authenticated candidate-method evidence. Artifact-reduction fields and desired-signal distortion/preservation fields remain separate. A reported field is not automatically established artifact proof or preserved physiology; read its stated scope and limitations.

**Review comparison evidence…** reads explicitly selected existing JSON evidence files. It records file hashes, declared schema/type/status and source scope. It never launches numerical generators or benchmarks implicitly. Source-matched, mismatched, synthetic/control, unknown-scope and unsupported records remain distinguishable. A recording-file hash match alone does not prove matching streams, channels or intervals.

Saved evidence retains its original scope; it is not silently recomputed for the frozen interval. Malformed, unsupported or unavailable evidence stays explicit. A successful software status is not scientific validation. The unified view does not rank cleaners or invent a winner. Any benchmark conclusion must be read under that benchmark's own declared target, controls and limitations.

## 6. Label what a result means

| Status | Meaning |
| --- | --- |
| Recorded measurement | Observed values from an identified recording in declared sensor units; acquisition quality still matters. |
| Calculated estimate | A numerical result calculated from identified data with a stated method and support. |
| Exploratory construct | An interpretation, model reconstruction, simulation or research construct; not a directly measured mental state. |
| Unclassified | No reviewed mapping is registered. Do not assume measurement status or established validity. |

These structured labels include provenance, limitations and an explicit statement that classification is not validation. Exact reviewed module identifiers are mapped; unknown identifiers remain unclassified. Zuna reconstruction is not an observed sensor measurement, even when a calculated descriptor is subsequently computed from it. CAI/SID and related exploratory proxy constructs are not promoted to established primary endpoints.

The labels are carried into relevant plots, result views, saved summaries and AI evidence metadata. They do not alter numerical values, historical results, availability or endpoint qualification. A completed worker, available estimate, human-approved report and scientifically supported conclusion remain different states. Existing report bytes are not rewritten merely to attach a new label.

## 7. Export a local browser inspection copy

In Research Exchange choose **Export browser viewer…**, select a Research Bundle 1.0 ZIP, review the privacy warning and choose a new HTML destination. The exporter verifies the archive and ledger before building an inert local inspection page. It refuses to overwrite an existing destination. Use an existing output folder on a filesystem supporting hard links.

The page is designed to open in a modern browser without Workbench, Python, a server or installed dependencies. It contains bounded complete text previews and a file ledger; omitted members remain listed with reasons. HTML/XML reports are displayed as literal source text, not executed. CSV/TSV plotting uses explicitly chosen columns, retains source order and breaks lines at missing/nonfinite values. Row index is not time, units are not invented, and there is no resampling, filtering, synchronization or binary XDF/NPZ decoding.

The browser checks embedded preview hashes, not the entire original ZIP. The embedded manifest and hashes are not a signature; compare the ZIP digest with a separately trusted receipt when authenticity matters. Export does not upload, publish, redact identifiers or authorize sharing. Private paths already present in report text can remain visible.

Browser rendering could not be observed because the available browser route was blocked by URL policy. Exporter/source tests do not establish visual rendering or operation in every browser. See the [viewer reference](app/tools/Research_Bundle_Viewer_v1_0/README.md) for exact size, format and integrity limits.

## Preserve the research boundary

- These workflows save new local derivatives only. They do not mutate raw sources, historical plans, prior results, hardware configuration or protocol authority.
- Frozen arrays contain selected full-resolution samples and are private research derivatives. A report, evidence JSON or browser page can still disclose identities and sensitive findings. Review consent, rights and the actual contents before sharing.
- Local inspection, simulation and existing-result review make no provider request. **Generate AI explanation** remains separately configured and explicitly authorized. Real provider behavior was not tested for these additions; AI tests use offline simulation only.
- Physical acquisition and fresh-machine installation were not tested for these additions. Cerelog physical validation, dual-system timing and actual PRAYCG4 recordings remain separate research work.
- No automatic quality winner, MATLAB equivalence, physiological preservation, clinical suitability or general validity is established by a successful test or cleaner-looking trace.

The Public edition remains independent of private AUL code or histories. Its existing PRAYCG AI Assistant remains available under its separate request and review controls.
