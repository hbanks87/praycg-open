# PRAYCG Workbench - Public - Alpha 11.9.2

A local-first research workbench for protocol preparation, synchronized acquisition, recorded analysis and reproducible research bundles. This patch improves Results refresh behavior and corrects Windows GUI-test capture and lifecycle issues. The independent PRAYCG AI Assistant remains available without AUL.

## New in this release

- Unchanged result dashboards retain their existing widgets, expanded child results and layout during refresh. Changed result content, evidence, context, callbacks or widget lifecycles invalidate the cached presentation.
- Windows GUI tests use Python-stream capture rather than replacing native file handles. Native output remains available to the enclosing test runner. The installed Tcl/Tk runtime is not patched or reinstalled.
- Synthetic operator-test fixtures cancel their own pending callbacks before teardown, avoiding orphan timer errors.
- Retains the previous media-route, physiology attribution, timestamp-rounding, catalog and protocol-validation corrections.

Read [BUILD_REPORT.md](BUILD_REPORT.md) for exact fresh test results and limits. A passing timing test is not a guarantee of every GUI latency on every machine. Start with [INSTALL_WORKFLOW.md](INSTALL_WORKFLOW.md); extract beside an existing installation, not on top of it. No settings, recordings, AUL histories or Zuna assets are bundled or migrated automatically. This ordinary ZIP is not a signed updater package.

## Retained from Alpha 11.9.0

- Current Athena catalog and source bindings, additional protocol profiles and clearer separation of recording compatibility from a protocol's declared endpoint. A four-channel stream cannot meet a mandatory physical 16-channel task; the Athena-specific alternative remains explicit.
- Per-measurement breathing-task support checks. A single RR interval cannot make an otherwise unsupported cardiac response available.
- Source-verified paired processing results can open native comparison views with original/processed selection and fixed original calibration. Unsupported state dimensions remain unavailable.
- Closed compact Cerelog captures can be reviewed and exported separately. The 3-EMG/2-EOG/ALS layout excludes disabled CH1/CH2 from physiology. This is not a new live connector or completed physical validation.

See [the integration guide](INTEGRATION_11_9.md) and the current [recommendation ledger](RELEASE_SCOPE_37.md).

## Retained guided workspace

1. A three-path Home screen: **Run a study**, **Inspect a recording**, or **Try an example**.
2. Persistent source context: recording, stream, participant metadata, channels, units, interval and processing selection; missing metadata stays unknown.
3. Frozen same-sample comparisons of the original recording, an explicitly selected recipe preview and an optional reviewed candidate.
4. Question-first routes into existing analysis tools, with prerequisites visible before execution.
5. Read-only review of existing numerical and preservation evidence, with source scope and no automatic winner.
6. Recorded-measurement, calculated-estimate and exploratory-construct labels in relevant plots, results, reports and AI evidence; unknown methods stay unclassified.
7. A portable, local, read-only Research Bundle browser-viewer export.

The example is conspicuously synthetic, generated only in a folder you choose, and uses no hardware or AI provider. The new guided and browser-viewer workflows add no dependencies.

## Start safely

Extract the complete release into a new writable folder. Run the outer **INSTALL.bat**, then **START.bat**. Native Windows Python 3.11 with Tcl/Tk is required. Do not merge application folders, reset settings or reinstall Zuna merely to apply this update.

Keep previous releases, external settings, study workspaces, recordings, historical results and existing Zuna runtime/model folders. Zuna reuse requires a matching pinned contract and successful verification; retain any older or shared folder still referenced by the new installation. The new workflows save separate derivatives, never replace original recordings, locked plans or existing reviewed results.

Existing analysis remains **Open recording… → Run recommended analyses → Run pending analyses** when offered **→ View latest report**. Required QC and endpoint prerequisites remain in force. A local numerical summary makes no provider request; **Generate AI explanation** remains a separate, explicitly authorized action.

## Public edition and updates

No private AUL implementation, prompts, persistence, evaluation fixtures or study histories are included or required for public installation, acquisition, analysis, supported protocol authoring or bundle reopening.

**Settings → Updates** supports explicit same-edition signed updates and signed local ZIP import. Keep the exact companion `.zip.update.json` sidecar. An ordinary ZIP or hash file is not a signed updater release.

Updates install beside the current application. Finish acquisition, stop/save LabRecorder and close active work before restarting; no active process is automatically killed. Local ZIP import can still need internet access or cached packages for existing runtime dependencies. See [installation instructions](INSTALL_WORKFLOW.md) for recovery and Zuna preservation.

## Evidence and limits

Measurement labels describe evidence type, not clinical validity, endpoint eligibility or acquisition quality. Smoother traces, lower line noise or a larger removed signal do not prove better physiological preservation. Missing sensors, units, participant identity, clock support or measurements remain explicit. No new cleaner or scientific endpoint is introduced, and no PiEEG code was copied.

Browser rendering is not verified by this release; export and source tests are not visual-rendering evidence. Physical acquisition, fresh-machine installation and real AI-provider behavior are outside the release test scope; AI testing is offline/simulated only. Cerelog physical validation and actual PRAYCG4 recordings remain research priorities.

Default AI/result-review bundles exclude full-resolution telemetry, but derived reports can still be sensitive. Frozen inspection files contain selected sample data and are private research derivatives. The browser export is a copy, not anonymization or publication permission. Review consent, identifiers, media rights and the file ledger before sharing.

PRAYCG is alpha research software, not a medical or diagnostic system. Upstream licenses and notices remain applicable. Earlier workflow details remain in [PROTOCOL_EVIDENCE_11_7.md](PROTOCOL_EVIDENCE_11_7.md), [WORKFLOW_COMPLETION_11_6.md](WORKFLOW_COMPLETION_11_6.md) and [SIGNAL_REVIEW_GUIDE.md](SIGNAL_REVIEW_GUIDE.md).

