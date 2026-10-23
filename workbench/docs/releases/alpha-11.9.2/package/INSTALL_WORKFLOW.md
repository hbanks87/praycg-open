# PRAYCG Workbench - Public - Alpha 11.9.2 — installation and workflow

This reliability patch is delivered as a complete manual-install ZIP. Extract it beside your existing application; do not merge folders or delete your prior installation. It does not change the shared Zuna contract or require a new model download. See BUILD_REPORT.md for synthetic verification limits.

Existing reports keep their original method labels and release provenance. To obtain corrected physiology reports, run a new analysis derivative through the normal plan/version workflow. Do not edit old results or their fingerprints. Newly prepared SVNA and NATVIEW packages use the corrected generator route and still require normal review. Protocol-credit corrections do not grant scientific or participant approval.

Read [INTEGRATION_11_9.md](INTEGRATION_11_9.md) for Athena compatibility, supported paired-result views, cardiac support checks and offline compact Cerelog review. [GUIDED_WORKSPACE_11_8.md](GUIDED_WORKSPACE_11_8.md) describes the retained guided workflows. Original recordings and locked plans remain untouched. The synthetic example requires neither hardware nor an AI provider.

## Install beside your existing release

1. Finish acquisition and stop/save LabRecorder. Close the older Workbench before switching releases.
2. Preserve the old application, study folders, settings, recordings, analysis history and Zuna runtime/model assets. Extract the complete new release into its own writable directory, never over an application or recording folder.
3. Run the outer **INSTALL.bat**, then **START.bat**. Native Windows Python 3.11 with Tcl/Tk is required. Core, Live Monitor and Hardware Connectors use separate release-local environments. Do not launch an arbitrary historical script inside `app`.
4. Reopen your existing Study Workspace and verify recording, hardware, external application and Zuna paths. Do not reset settings or reinstall Zuna merely to apply this release.
5. Preserve historical plans, results and fingerprints. New execution or explanation creates new derivatives. If software drift is reported, use the normal new-plan or revision workflow; never edit a historical hash to force compatibility.

Earlier QC and locked-plan records retain their original release identities. New execution requires the matching recorded protocol evidence and current required QC. Viewing an earlier report does not require rewriting it.

Core retains its pinned NeuroKit2, mne-denoise and PyWavelets comparison dependencies. Optional ASR, ICLabel and Pycrostates tools use **INSTALL_SIGNAL_EXTRAS.bat** in a separate environment. **INSTALL_EVENT_DESCRIPTIONS.bat** optionally installs official HED validation in its own environment, separate from acquisition. Neither optional installer is required for the new guided inspection or browser export. Physical drivers, device publishers and PsychoPy still need their supported setup; importing a library does not validate equipment.

This Public edition includes the independent PRAYCG AI Assistant and needs no private AUL extension. Private AUL implementation, prompts, persistence and study histories are not included.

## Signed updates and recovery

1. Open **Settings → Updates**. Opening the tab does not download or install anything. Use **Check for updates** to request a newer verified release for the same edition.
2. The Public checker uses the configured PRAYCG GitHub release repository, including eligible alpha/prerelease entries. An unsigned legacy archive is not an updater release.
3. After reviewing the offered version, choose **Download & prepare update**, or place a signed ZIP beside its exact `.zip.update.json` companion and choose **Import signed update ZIP**. The included trust key verifies the signature. A ZIP hash alone is insufficient; wrong editions, unknown keys, altered files, incompatible state and unsafe archive paths are rejected.
4. Preparation installs beside the running release under the edition's update folder in `%LOCALAPPDATA%\PRAYCG\updates`. Existing runtime setup can require internet access or cached packages even when the ZIP is local. **Open update folder / logs** shows evidence. **Cancel preparation safely** waits for a safe boundary and does not kill an installer midway.
5. Stop/save LabRecorder, finish acquisition, analysis, provider requests and exports, and close running viewers/tools. Choose **Update and restart** only when ready. Active ownership or jobs block restart; no process is automatically killed. The helper rechecks the running release, snapshots configuration and waits for it to exit.
6. The prepared interface must report readiness before the stable launcher changes. Failure leaves the previous pointer intact. **Create stable desktop shortcut** adds an edition-specific launcher without deleting older shortcuts.
7. **Restore previous version** selects a registered compatible application; it does not rewind studies, recordings, reports or research decisions. Settings snapshots support reviewed recovery, not blind replacement of newer state.

A remote update is available only when matching signed metadata is published. This build does not publish a feed or install itself. Do not remove signature checks or change hashes to force an update.

Zuna reuse is conditional: the pinned requirements/model contract must match and verification must succeed. An ordinary update can reference the existing environment and model files without copying the large environment or downloading weights. Keep every referenced older or shared runtime/model folder. A changed contract requires explicit reviewed migration. For a manual installation, verify the new release's Zuna connection; extraction alone does not establish it. No Zuna reinstall or new model download is required by these additions.

## Choose a starting path

- **Run a study** opens existing protocol preparation and acquisition controls. It grants no new device or protocol authority.
- **Inspect a recording** selects a saved recording and opens a passive source view. Check the recording, stream, declared participant, channels and units before choosing an interval.
- **Try an example** asks for an output folder, then creates a conspicuously labeled synthetic recording there. It is never attached to the real study or hardware configuration and makes no AI request.

**Choose your question** routes to existing inspection, event/time–frequency, condition-analysis or saved-results workflows. Navigation does not execute an analysis. The persistent header distinguishes selected recordings from live/replay sources; unknown metadata stays unknown.

For exact-sample processing comparisons, use **Freeze interval**, explicitly choose a recipe and/or reviewed candidate receipt, then **Compare frozen samples**. All channels in the selected stream are frozen together; the channel picker changes the display only. Short or unsupported windows remain unavailable under existing method requirements. **Review comparison evidence…** reads selected existing evidence files without launching generators or tests. See the [guided guide](GUIDED_WORKSPACE_11_8.md) for support, scope and privacy limits.

## Prepare protocols and materials

Choose the actual hardware setup and protocol. Atlas separates **Recording** from **Intended result**. Exploratory Athena access does not supply missing electrodes or validate an endpoint. Task-critical equipment, identities, clocks, ownership and writable destinations remain prerequisites.

A reviewed AI return installs a supported declarative protocol, not arbitrary code, a new device route or a new estimator. Required assets must exist; a movie request does not generate media. Optional closed rating contracts must explicitly bind categories, nodes, conditions and supported comparisons. Unknown scales, aggregation, imputation or causal conclusions are not invented. New scoring of historical data remains post hoc.

Optional movies are available through **Prepare Materials → Optional movies: install / use a master…** or **INSTALL_STIMULUS_PACKAGE.bat**. Review source, destination and storage before confirming. The seven films—Coffee Run, Poached, Glass Half, You Imagined, Wing It!, Hero and Charge—and the separate original Lantern package provide eight masters. Starting Workbench alone downloads nothing. For local archives use the dialog or `INSTALL_STIMULUS_PACKAGE.bat --archive-directory "D:\Downloads\PRAYCG stimuli"`.

Exact verified installations are reused; changed content is not overwritten. Retry after failure to reuse completed packages. Unsafe or mismatched archives are rejected. **Use this master** still requires playback checks, protocol-specific preparation, fingerprinting and review. Installing a master is not protocol qualification or publication permission. Read the [stimulus guide](app/tools/Stimulus_Forge_Library_v1_0/OPTIONAL_STIMULUS_INSTALLATION.md).

## Record, analyze and explain

Connect the selected equipment and verify actual streams. Athena findings are retained without repeated quality acceptance. Confirm setup, mark ready and start LabRecorder before the protocol. Select every intended stream, including separate optical, cardiac, respiration, EOG/EMG and ALS streams where present. Stop/save LabRecorder before analysis so the XDF closes. Connected but unrecorded measurements cannot be recovered by an explanation.

1. In **PRAYCG AI Assistant → Analyze a recording**, choose **Open recording…** and check the exact recording/run identity.
2. **Recording conditions (optional)** records post-hoc operator context, not independently verified measurements. Leave unknown when unsure; describe variation instead of inferring conditions from a task name or signal.
3. Choose **Run recommended analyses**. Required QC runs first when needed. **Choose modules…** supports custom work. If shown **READY BUT NOT RUN**, use **Run pending analyses**; a saved plan is not an executed analysis. Do not restart while a job is active. Local numerical analysis does not contact a provider.
4. **Visual Analysis** opens recording-specific saved figures. Batch time–frequency work saves plots without automatically opening a window; use **Open latest time-frequency view**. Advanced state or calibrated endpoints retain their additional requirements.
5. Choose **View latest report**. **Advanced details… → Create / view local numerical summary**, **Individual module reports** and **Open selected report** expose saved evidence. Worker completion, endpoint availability, failed attempts and skipped dependencies are different facts. A deliberate partial report must state its omissions.
6. For ratings, bind the exact protocol manifest and canonical events. Inspect literal questions, categories, missing windows, response selection and declared comparisons.
7. **Generate AI explanation** is separate and requires configured provider access, allowance and explicit authorization, including confirmation for partial reports. It explains saved results, does not rerun numerical analysis or authorize acquisition changes. Opening an existing explanation makes no new request. Provider failure/cancellation leaves numerical results and earlier reports intact.

**Explain existing results** creates a new explanatory derivative without unlocking a historical plan or rewriting earlier narratives. Better wording does not validate an endpoint.

## Compare, export and share

Signal Quality & Cleaning Review retains original/current-preview/reviewed-candidate/difference views, exact annotation selection and saved comparisons. A current preview is not historical derivative replay. Delayed SPAR recording replay remains experimental offline processing of an explicitly selected interval up to 60 seconds, not a live acquisition filter. See [SIGNAL_INTEGRATION_11_4.md](SIGNAL_INTEGRATION_11_4.md). Closing a window does not kill physical background work; exit/update waits for it.

In Research Exchange, **Export browser viewer…** verifies an explicitly selected Research Bundle ZIP and saves a new local HTML file. Choose an existing output folder on a filesystem supporting hard links. No upload or browser launch occurs. The viewer is for bounded inert previews and simple CSV/TSV plots, not binary recording replay, numerical reruns or clinical interpretation. It does not anonymize the selected content.

Recorded/calculated/exploratory labels describe evidence type, not validity. Candidate smoothing, lower line noise or removed amplitude does not prove desired-signal preservation. Review scope, exclusions and limitations; no automatic cleaner is adopted.

Frozen inspection arrays are private full-resolution derivatives. Default AI/result-review bundles omit full-resolution telemetry, but summaries and browser copies can still disclose private information. Review consent, identifiers, raw selections, media rights and the ledger before sharing.

Browser visual interaction was not observed in this release's tests because a browser connection was unavailable. Native export and JavaScript checks do not establish browser rendering. Physical acquisition, fresh-machine installation and real AI-provider behavior were not tested for these additions; AI verification uses offline simulation only. Read [BUILD_REPORT.md](BUILD_REPORT.md) for completed checks. Software completion does not establish hardware safety, timing, AI correctness, clinical suitability or scientific validity.

