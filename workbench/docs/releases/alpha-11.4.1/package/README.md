# PRAYCG Workbench - Public - Alpha 11.4.1

## Public Alpha 11.4.1 optical-credit correction

This release repairs the structured optical relative-hemoglobin citation so new affected execution receipts retain automatic method and software credits. Numerical optical processing, profile requirements and historical results are unchanged. Read [the current attribution supplement](app/docs/ATTRIBUTION_ALPHA_11_4_1.md) and [BUILD_REPORT.md](BUILD_REPORT.md). Existing invalid historical credit records are not silently rewritten.

The workflow below retains the 11.4.0 feature scope. First-time users extract this complete release into a new folder; updater-enabled Public versions can use the matching signed update metadata.


## This release: signal support, inspectable comparisons and grounded reports

This release tightens event-window coverage, clock and gap checks; binds selected exclusions and reviewed candidates to their exact sources; and adds saved processing comparisons with playback and delayed SPAR recording replay. The replay is an experimental offline comparison, not a live acquisition filter. The synthetic preservation benchmark includes adverse results: SPAR can remove wanted slow activity. No cleaner is selected automatically.

Athena AI explanations can now reference exact recorded result IDs. Software preserves their values, source fingerprints, scope, method and limitations; the model supplies explanatory text. This does not verify that the explanation is correct. Drafts still require review and approval. Only a bounded subset fits each request, and omitted rows remain explicitly counted.

See [SIGNAL_INTEGRATION_11_4.md](SIGNAL_INTEGRATION_11_4.md) for the new workflow and [BUILD_REPORT.md](BUILD_REPORT.md) for verification. This release does not complete all 37 research recommendations, establish MATLAB equivalence or validate physiological signal preservation. Acquisition preflight and Athena exploratory access are unchanged.

## Retained Alpha 11.3.2 guided analysis, responsiveness and signed updates

This patch hardens the route from required QC through recommended and pending analyses to saved reports. Background work is kept away from the interface, stale responses are rejected, and interrupted or historical attempts remain distinguishable from the current workflow. A deliberately partial report identifies unfinished or unavailable analyses; it does not claim that every module ran. Local numerical summaries and authorized AI explanations remain separate.

Settings now includes **Updates** for explicit, signed, same-edition updates installed beside the current release. No update is downloaded or installed simply by opening the Workbench. The first installation of this updater-enabled version is still a manual extraction into a new folder. No remote signed release was published as part of this build, so remote updating becomes usable only when matching signed metadata is published. A signed ZIP and its companion sidecar can be imported locally.

Verification includes isolated updater tests with simulated installers and injected failures, real application-constructor checks, and verification of an existing Zuna runtime/model binding without downloading weights. It does not establish a successful fresh-machine installation. See [BUILD_REPORT.md](BUILD_REPORT.md) for the completed tests, latest-recording workflow evidence and remaining limits.

## Retained Alpha 11.3.1 responsiveness and report handoff

This hotfix targets repeated eligibility checks while searching, slow synchronous refresh work, and confusing report selection. Module searches use the loaded view, background refreshes reject stale results, and execution-time integrity checks remain in place. Report opening distinguishes the latest saved AI explanation from the local numerical summary. New explanation requests carry source-linked findings, not just eligibility labels; historical reports are not rewritten. Opening a saved draft does not mark it human-reviewed or scientifically validated. Generating a new AI explanation remains a separate, explicitly authorized request.

Read [BUILD_REPORT.md](BUILD_REPORT.md) for the completed verification scope. Existing recordings, historical results, settings and Zuna assets are not migrated or replaced by this package. Use a new release folder; do not merge it over an older installation. No acquisition-quality threshold or scientific estimator is relaxed by this responsiveness work.

## Retained Alpha 11.3.0 signal review and processing comparisons

The new tools extend Signal Quality & Cleaning Review: explicit sensor pairing, corrected legacy beat/gap handling, versioned exclusion retractions, physiology comparisons, offline SPAR/ICA/ASR/reference candidates, pass/component inspection, and saved downstream research comparisons. Original recordings and locked plans stay unchanged.

Start with [SIGNAL_REVIEW_GUIDE.md](SIGNAL_REVIEW_GUIDE.md). [RELEASE_SCOPE_37.md](RELEASE_SCOPE_37.md) lists the delivered scope and remaining work for all 37 recommendations. These are experimental comparison tools, not validated automatic cleaners. The synthetic SPAR benchmark includes unfavorable preservation results.

ASR, ICLabel and Pycrostates use the optional **INSTALL_SIGNAL_EXTRAS.bat** in a separate release-local environment. Core and Zuna are not modified. No optional environment, real recording or private study history is shipped. This build was not installed or published.

This Public edition includes the independent PRAYCG AI Assistant. No private AUL implementation, persistence, prompts, evaluation fixtures or study histories are included. No private extension is needed for public installation, acquisition, analysis, supported protocol authoring or bundle reopening.

A local-first research workbench connecting protocol preparation, synchronized acquisition, recorded analysis and reproducible research bundles. This patch hardens the path from a selected protocol and recording to useful figures and source-linked explanations.

## Retained workflow improvements

- Materials now checks matching release catalogs and reports actionable compatibility reasons.
- Visual Analysis uses the selected recording and verified saved outputs. A missing advanced state estimate does not hide an available TFR display.
- Explanations carry more numerical measurements, channel selections, time support, units and screening scope. Worker completion, endpoint availability and missing prerequisites remain separate.
- Explicit eye/activity context is retained as a post-hoc, unverified operator report. Unknown stays unknown; task names and signal patterns do not establish what happened.
- Optional versioned rating contracts declare categories, node/condition bindings and supported comparisons. Existing protocols remain unchanged; absent contracts do not authorize guessed scales or comparisons.
- The optional movie installer offers seven films plus original Lantern: eight masters in two separately verified packages. These are preparation inputs, not qualified protocol packages.

## Start here

Read [INSTALL_WORKFLOW.md](INSTALL_WORKFLOW.md). Run **INSTALL.bat**, then **START.bat** from this outer release folder. Do not launch an arbitrary historical script inside app. [CHANGELOG.md](CHANGELOG.md) summarizes the patch and [BUILD_REPORT.md](BUILD_REPORT.md) records its actual verification scope.

The ordinary analysis path is **Open recording… → Run recommended analyses → Run pending analyses (when offered) → View latest report**. Required QC runs first when needed. In **Advanced details…**, **Create / view local numerical summary** gives a factual report without a model; **Generate AI explanation** is a separate authorized request. A report can be deliberately partial, but must identify unrun or unavailable analyses. An explanation does not authorize recomputing statistics or changing acquisition.

## Settings updater

After the initial manual installation, open **Settings → Updates**. Use **Check for updates**, then **Download & prepare update**, or choose **Import signed update ZIP** with its adjacent `filename.zip.update.json`. Review the result before choosing **Update and restart**. Finish recording, stop/save LabRecorder and close running tools first; an update never kills an active recording or analysis.

Public update checks use the configured PRAYCG GitHub release repository and select a newer, verified signed alpha release. An ordinary unsigned ZIP is not an updater release. No matching remote signed release was published during this build. Local import does not remove the need for dependency downloads when packages are not already available.

**Create stable desktop shortcut** creates a separate launcher for this edition. **Restore previous version** is available only for a registered, compatible previous application; it does not roll back studies or assistant history. **Open update folder / logs** shows preparation evidence. **Cancel preparation safely** stops between safe steps and may wait for the current installer step.

Updates retain external settings, study folders and model assets. Exact-contract Zuna reuse is verified, not assumed: keep the older runtime folder while the new release references it. A changed Zuna contract needs a separate reviewed migration. The updater has isolated failure-injection coverage and a real existing-Zuna verification, but no fresh-machine installation guarantee. Detailed steps and limitations are in [INSTALL_WORKFLOW.md](INSTALL_WORKFLOW.md).

## Preserve your studies

Extract into a new folder. Keep existing settings, workspaces, recordings, analysis history, previous releases and Zuna environments/model assets intact. Do not merge over a running installation or reinstall Zuna merely to apply this patch. Building and extracting the archive do not install it over an existing setup.

Optional movies are available through **Prepare Materials → Optional movies: install / use a master…**, or **INSTALL_STIMULUS_PACKAGE.bat**. Review the source, destination and storage summary before confirming. Exact local ZIPs are supported. Then use the selected master through normal preparation, fingerprinting and review. Read the [stimulus guide](app/tools/Stimulus_Forge_Library_v1_0/OPTIONAL_STIMULUS_INSTALLATION.md).

## Limits and privacy

A supported EEG channel or pair cannot substitute for an unavailable full-montage endpoint. Raw optical trends do not supply hemoglobin estimates without a verified mapping. Sampled heart rate is not beat-to-beat HRV. Missing sensors, units, clocks or measurements remain explicit.

Default AI/result-review bundles exclude full-resolution telemetry. Derived summaries can still be sensitive. Full-telemetry exports require explicit selection and privacy/consent review; a hash does not grant publication rights.

PRAYCG is alpha research software, not a medical or diagnostic system. Software checks do not certify every function, physical timing, hardware safety, AI interpretation or scientific endpoint. Original upstream notices and licenses remain applicable.

