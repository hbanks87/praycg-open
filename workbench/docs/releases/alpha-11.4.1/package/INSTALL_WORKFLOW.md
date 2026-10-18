# PRAYCG Workbench - Public - Alpha 11.4.1 — Installation and workflow

## Public Alpha 11.4.1 optical-credit correction

This release repairs the structured optical relative-hemoglobin citation so new affected execution receipts retain automatic method and software credits. Numerical optical processing, profile requirements and historical results are unchanged. Read [the current attribution supplement](app/docs/ATTRIBUTION_ALPHA_11_4_1.md) and [BUILD_REPORT.md](BUILD_REPORT.md). Existing invalid historical credit records are not silently rewritten.

The workflow below retains the 11.4.0 feature scope. First-time users extract this complete release into a new folder; updater-enabled Public versions can use the matching signed update metadata.


## New in this release

Batch time-frequency analysis now saves its plots without opening a window automatically. Use **Open latest time-frequency view** in Visual Analysis to inspect them. This opens the saved result; it does not rerun analysis or contact an AI provider.

Install into a new folder, or import this edition's signed ZIP with its adjacent `.zip.update.json` through **Settings → Updates**. Keep your older installation and shared Zuna assets until the new installation has been checked. This build does not itself install, migrate settings or publish a remote update.

For processing comparisons, open your recording in **Analysis Forge → Signal Quality & Cleaning Review**. Explicitly select any annotation version; do not assume the newest file was adopted. Use **Open saved reviewed comparison** for a verified candidate, or **Run delayed SPAR recording replay** for an experimental interval of up to 60 seconds. The comparison window supplies play/pause, rewind, seeking and elapsed time. Read [SIGNAL_INTEGRATION_11_4.md](SIGNAL_INTEGRATION_11_4.md) first: cleaning may remove wanted activity, and shared cursor movement does not recalculate CAI/SID/TFR endpoints. Closing a review window does not terminate a background calculation; updates and application exit wait for physical work to finish.

The existing AI explanation workflow now binds supported Athena result explanations to exact saved evidence. Review the **Result sources and qualifications** section along with the prose before accepting a draft. Source binding does not verify the model's interpretation. No new provider request is made merely by opening a report.

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

## Upgrade without disturbing your existing setup

1. Finish acquisition and stop/save LabRecorder. Close the older Workbench before switching releases.
2. Preserve the old application and all study folders. Extract the complete new ZIP into its own writable directory, not over an old application or recording folder.
3. Run **INSTALL.bat**, then **START.bat**. Native Windows Python 3.11 with Tcl/Tk is required. Core, Live Monitor and Hardware Connectors use separate release-local environments.
4. Reopen your existing Study Workspace and check recording, hardware, external application and Zuna paths. Preserve existing settings and Zuna environment/model assets. Do not reset settings or reinstall Zuna merely for this patch.
5. Preserve old plans, results and fingerprints. New executions/explanations create new derivatives. Do not edit hashes to force compatibility.

This release changes the analysis-registry fingerprint. Earlier QC and locked-plan records remain historical evidence, not newly authenticated checks for this release. To execute a new analysis, select the matching recorded protocol evidence and run required QC with the current release; use its normal new-plan or revision workflow if software drift is reported. Viewing saved reports does not require rewriting old results. Do not modify historical hashes to bypass this distinction.

Normal Core setup includes the pinned NeuroKit2, mne-denoise and PyWavelets comparison dependencies. Optional ASR, ICLabel and Pycrostates tools use **INSTALL_SIGNAL_EXTRAS.bat** and its separate environment; they are not required to apply this responsiveness hotfix. Physical drivers, device publishers and PsychoPy still need their supported configuration; an importable library is not device validation.

## Updating from an updater-enabled release

1. Open **Settings → Updates**. Nothing downloads or installs merely because this tab opens. Use **Check for updates** to look for a newer signed release for the same edition.
2. The Public checker uses the configured PRAYCG GitHub release repository, including eligible alpha/prerelease entries, rather than assuming GitHub's latest stable release is appropriate. Unsigned legacy archives are not accepted as updater releases.
3. Choose **Download & prepare update** after checking the offered version. Alternatively, put a signed release ZIP beside its exact companion sidecar, such as `release.zip` and `release.zip.update.json`, then choose **Import signed update ZIP**. The included public trust key verifies the signature; a hash alone is insufficient. Wrong editions, unknown keys, altered files, incompatible state and unsafe archive paths are rejected.
4. Preparation makes a complete side-by-side installation in the edition's update folder under `%LOCALAPPDATA%\PRAYCG\updates`. It does not overwrite the running application. Core and previously installed optional runtimes are set up separately; this can need internet access or cached packages even when the release ZIP is local. Use **Open update folder / logs** to inspect progress or a failure. **Cancel preparation safely** waits for a safe boundary and does not kill an installer process midway.
5. Finish and save recording, stop LabRecorder, stop analysis and close running viewers/tools. Click **Update and restart** only when ready. Confirm external recording is stopped. Acquisition/runner ownership, current jobs and remaining provider/export work block restart. No process is automatically killed. The helper rechecks the actual running release, snapshots configuration and waits for the old application to exit.
6. The prepared version must report that its interface is running before the stable launcher changes. A failed launch leaves the previous pointer intact and records the failure. **Create stable desktop shortcut** adds an edition-specific launcher without removing old shortcuts. Keep the old application until the new version and optional integrations have been checked.
7. **Restore previous version** switches to a registered, compatible prior application. It does not rewind recordings, reports, assistant history or research decisions. Settings snapshots are retained for reviewed recovery, not blindly restored over newer studies.

No remote signed release was published during this build. Until signed metadata is published, a check may correctly report that no verified update is available. The signed ZIP-plus-sidecar route can be used independently of a remote feed. Do not substitute an unsigned archive, change hashes or remove a signature check to force an update.

Zuna is a special preservation case. An updater-prepared installation can reference the existing runtime and model files only when the pinned requirements/model contract matches and verification succeeds. It does not copy the large environment or download weights for an ordinary patch. Keep the referenced older runtime folder. A changed contract requires an explicit reviewed migration. For the first manual installation of this release, preserve the old installation and verify the new release's Zuna connection before using it; extracting a ZIP alone does not establish that connection.

Updater testing includes simulated complete-edition installers, failure injection, actual application-constructor checks and verification of the existing Zuna binding without installs, downloads or inference. A new-machine installation and a published remote update were not performed for this build. See [BUILD_REPORT.md](BUILD_REPORT.md) for the exact verification scope.

## Protocols and materials

Choose the active hardware setup and protocol. The Atlas separates **Recording** from **Intended result**. Exploratory Athena recording does not supply absent electrodes or validate an endpoint. Missing task-critical equipment, ambiguous identities, unusable clocks, active ownership and unwritable destinations remain operational issues.

A reviewed AI return installs a supported declarative protocol, not arbitrary code, a new device route or an invented numerical estimator. Required assets must exist. Importing a definition requesting forward, reversed or ambient movies does not generate those movies.

Future protocol versions can include the optional closed rating contract: explicit category labels, node/condition bindings and declared descriptive comparisons. Keys must match the actual nodes. No aggregation, imputation or causal inference is guessed. Existing definitions are unchanged. Newly specified scoring applied to historical data stays post hoc.

## Optional movies: seven films and original Lantern

Open **Prepare Materials → Optional movies: install / use a master…**, or run **INSTALL_STIMULUS_PACKAGE.bat**. Select both packages, seven films only or Lantern only. Review destination, source and storage, then confirm. Starting the Workbench alone downloads nothing.

The seven films are Coffee Run, Poached, Glass Half, You Imagined, Wing It!, Hero and Charge. Original Lantern is a separate package, making eight master choices. Both packages preserve edition hashes, credits and license records. The original Lantern master is unchanged; historical cues, anchors and prepared variants remain examples, not current protocol qualification.

For offline installation, select a folder containing the exact companion ZIPs, or run:

```bat
INSTALL_STIMULUS_PACKAGE.bat --archive-directory "D:\Downloads\PRAYCG stimuli"
```

Exact verified installations are reused. Changed content is never overwritten. If a later package fails, rerun to reuse earlier verified packages and retry; incomplete downloads restart. Unsafe paths, linked entries, executables, nested archives, unexpected files and mismatched hashes are rejected.

After installation, refresh installed masters and select **Use this master**. Complete local playback checks, protocol-specific variants, fingerprinting and review. Installing media does not lock a study or grant collection/publication authority. See the [detailed stimulus guide](app/tools/Stimulus_Forge_Library_v1_0/OPTIONAL_STIMULUS_INSTALLATION.md).

## Record

Connect the selected equipment and verify actual streams. Athena signal findings are retained automatically without repeated quality acceptance. Confirm setup, mark ready and start LabRecorder before the protocol. Select every intended stream, including separate Optical, cardiac, respiration, EOG/EMG or ALS streams where present. Stop LabRecorder so the XDF closes before analysis. Connected but unrecorded measurements cannot be recovered by an explanation.

## Analyze, visualize and explain

1. In **PRAYCG AI Assistant → Analyze a recording**, choose **Open recording…** and the exact saved XDF. Check the displayed recording and run identity.
2. **Recording conditions (optional)** records actual eye/activity context. Leave unknown when unsure or when conditions changed; describe variation in the optional note. This is an explicitly post-hoc operator report, not measured or independently verified evidence. Revisions preserve prior files and their source chain.
3. Choose **Run recommended analyses**. Required QC runs and is saved first when needed, followed by the supported recommendation workflow. **Choose modules…** supports custom work. If the status says **READY BUT NOT RUN**, use **Run pending analyses** to execute the prepared work; a saved plan is not an executed analysis. Do not repeatedly restart the workflow while a job is active. Local numerical analysis makes no provider request.
4. Open **Visual Analysis** for recording-specific saved TFR, measured-sensor displays, traces or optical trends. Advanced calibrated/state views retain extra requirements. Unavailable cardiac/state measures do not make EEG figures unavailable. Loading/errors are shown beside the relevant action.
5. Choose **View latest report** and inspect the saved results. In **Advanced details…**, **Create / view local numerical summary** produces or opens the factual summary without an AI request. **Individual module reports** and **Open selected report** expose underlying results. Completed workers, supported endpoints, unavailable estimates, failed attempts and skipped dependencies are different facts. When work is pending, run it first for a fuller summary, or deliberately keep a partial report with those omissions stated.
6. For supported ratings, select the native rating analysis and bind the exact recorded protocol manifest and canonical events. Read literal questions, categories, missing/incomplete windows, response-selection rule and source-linked comparisons. EEG quality is not a substitute for rating evidence.
7. Optionally choose **Generate AI explanation** with a configured provider and allowance. Review and authorize the request; an explicit confirmation is required for a partial report. The request explains saved measurements and context, not raw recording samples, and does not rerun analysis. **Open latest AI explanation** opens an accepted saved explanation, not a new request. Provider failure or cancellation leaves numerical results and earlier reports intact; an incomplete/unaccepted provider reply is not promised as a usable report.

**Explain existing results** creates a new explanatory derivative without rerunning numerical analysis or unlocking a historical plan. Old narratives and original measurements remain unchanged. More readable reporting does not retroactively validate an endpoint.

## Review and share

Live/replay views are passive. **Save snapshot locally** preserves a derived review window without an AI request; it does not replace LabRecorder. A historical snapshot or delayed explanation is not current live status.

Signal Quality & Cleaning Review retains source-aligned original, explicit current-transform preview, candidate and removed-signal views. A preview is not replay of a historical locked derivative. No candidate or explanation automatically replaces a recipe or XDF. Reduced line noise alone does not prove neural preservation.

Review consent, identifiers, raw telemetry, media rights and the file ledger before sharing. Default AI/result-review exports exclude full-resolution telemetry; explicit private export still needs privacy review. Read **BUILD_REPORT.md** for the release's actual tests and remaining limits. No hardware, clinical, timing or scientific validation follows merely from software completion.

