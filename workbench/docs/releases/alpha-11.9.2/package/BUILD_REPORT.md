# PRAYCG Workbench — Public Alpha 11.9.2 build verification

## Outcome

All four previously outstanding GUI checks now pass in repeated qualification. The Results refresh path no longer destroys and rebuilds an unchanged dashboard. This preserves mapped widgets, expanded child results and existing layout. Changes to results, evidence, source/session context, callbacks or widget lifecycles still trigger a rebuild.

The two Tcl/Tk setup errors were isolated to a Windows test-capture interaction: the richer unchanged operator suite failed in six of seven file-descriptor-capture attempts and passed all eight Python-stream-capture attempts. Minimal Tk-only controls passed both modes. This is not a claim of a universal Tcl defect. The release adds `pytest.ini` with `--capture=sys`; the installed Tcl/Tk runtime is not replaced or patched, and native output remains visible to the outer test runner.

Synthetic GUI fixtures now settle their own idle events and cancel their pending callbacks before teardown. The Forge heartbeat fixture also cancels its own pulse timer. No production acquisition or analysis timer was removed. Native layout test callback failures now terminate cleanly and report the assertion instead of lingering until timeout; the 200 ms allocation sample, heartbeat and configuration-event thresholds are unchanged.

## Fresh selected tests

This edition: **979 passed**, 1 skipped and 10 installer-wrapper checks refused by the isolated test guard. No remaining selected product assertion failures or native GUI errors.

Across both editions: **2,012 distinct selected cases passed**, 2 skipped and 20 guard-refused. Those blocked checks attempted shell-wrapper dispatch, not an actual installation; they remain unverified, not passes. The two skipped cases require permission to create Windows directory symbolic links, which this test account lacks. This is a focused GUI/workflow regression, not a fresh execution of the entire preceding audit.

- The selected suite includes unchanged/changed result rendering, real report/evidence menus, source/session switching, cancellation, assistant workflow, AUL integration, reporting lifecycle, physiology roundoff regressions and current protocol/catalog checks.
- The dedicated layout qualification passed 100 distinct cases across both editions, including 100-module synthetic-history no-op refreshes. Its native layout check passed 12 executions with empty native stderr, including ten repetitions beyond the two whole-file executions. These overlap the selected regression count and are not added again.
- The operator qualification passed five complete 11-case repetitions per edition: 110 executions, 22 distinct cases, empty native stderr. After the broader suite exposed an additional synthetic heartbeat cleanup defect, five complete 20-case Forge repetitions per edition passed without native stderr. Repeated executions are evidence of repeatability, not additional distinct cases.
- Fifteen synthetic data scenarios per edition passed QC, preprocessing, spectral analysis, bundle export/verification/import and fresh reanalysis. These are three illustrative EEG shapes across clean, 60 Hz contamination, flat-channel, gap and short-duration scenarios, not every hardware route executing every protocol.
- The protocol/hardware contract matrix passed 1,335 checks per edition, covering 1,188 declared compatibility pairs and 32 actual scripted task dispatches. The current acceptance test walked all 79 workflow entries. Contracts and scripted rehearsal are not physical acquisition.
- Eight-stream synthetic Athena XDF readback and invalid-input refusal passed per edition.

## Interpretation of the GUI evidence

The old layout test also passed six baseline repetitions during this investigation. The confirmed deterministic defect was unnecessary widget destruction and loss of expanded state on an unchanged refresh. That defect now has a before/after regression. Passing native timing replays does not prove that this was the sole cause of every historical timing miss, guarantee absolute latency, or establish performance with every recording size.

All original failures, controlled capture comparisons, warning-bearing intermediate attempts and complete reruns remain in the local QA record. The final selected evidence uses whole-file reruns after cleanup, not cherry-picked successful nodes. Assertions were not skipped or relaxed to close the four GUI checks.

## Preservation and delivery

The installed Workbench was not replaced. **31,581 inventoried entries remained unchanged**, including settings, recordings, AUL history and the external Zuna setup. Settings/history/bindings use SHA-256 plus metadata; large recordings and Zuna collections use size and modification time, not exhaustive content hashes. Original release ZIPs remain unchanged. No participant recordings, private histories, provider credentials or model weights are included in these releases.

Public/private package boundaries, file checksums and fresh extracted contents are required by the archive gate. The private AUL implementation, permission boundaries and external persistence contract remain unchanged. Statistical algorithms, protocol tasks, marker namespaces and hardware declarations are unchanged by this GUI patch.

No device acquisition, real provider request, Zuna inference, model download, fresh-machine installation or publication was performed. Browser rendering and all physical protocol/hardware combinations remain outside this test scope. This ordinary ZIP and checksum are manual release artifacts, not a signed updater package. Extract beside the existing installation; do not merge application folders. See [INSTALL_WORKFLOW.md](INSTALL_WORKFLOW.md).
