# PRAYCG Workbench - Public - Alpha 11.2.2 — Installation and workflow

This Public edition includes the independent PRAYCG AI Assistant. No private AUL implementation, persistence, prompts, evaluation fixtures or study histories are included. No private extension is needed for public installation, acquisition, analysis, supported protocol authoring or bundle reopening.

## Upgrade without disturbing your existing setup

1. Finish acquisition and stop/save LabRecorder. Close the older Workbench before switching releases.
2. Preserve the old application and all study folders. Extract the complete new ZIP into its own writable directory, not over an old application or recording folder.
3. Run **INSTALL.bat**, then **START.bat**. Native Windows Python 3.11 with Tcl/Tk is required. Core, Live Monitor and Hardware Connectors use separate release-local environments.
4. Reopen your existing Study Workspace and check recording, hardware, external application and Zuna paths. Preserve existing settings and Zuna environment/model assets. Do not reset settings or reinstall Zuna merely for this patch.
5. Preserve old plans, results and fingerprints. New executions/explanations create new derivatives. Do not edit hashes to force compatibility.

Normal Core setup includes the pinned NeuroKit2, mne-denoise and PyWavelets comparison dependencies. There is no separate signal-review installer. Physical drivers, device publishers and PsychoPy still need their supported configuration; an importable library is not device validation.

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

1. **Open recording** and choose the exact saved XDF. Check the displayed recording and run identity.
2. **Recording conditions (optional)** records actual eye/activity context. Leave unknown when unsure or when conditions changed; describe variation in the optional note. This is an explicitly post-hoc operator report, not measured or independently verified evidence. Revisions preserve prior files and their source chain.
3. **Run recommended analyses**. Required QC runs when needed. **Choose modules** supports custom work. Local numerical analysis makes no provider request.
4. Open **Visual Analysis** for recording-specific saved TFR, measured-sensor displays, traces or optical trends. Advanced calibrated/state views retain extra requirements. Unavailable cardiac/state measures do not make EEG figures unavailable. Loading/errors are shown beside the relevant action.
5. **View results**. Read individual reports and the local summary. Completed workers, supported endpoints, unavailable estimates, failed attempts and skipped dependencies are different facts.
6. For supported ratings, select the native rating analysis and bind the exact recorded protocol manifest and canonical events. Read literal questions, categories, missing/incomplete windows, response-selection rule and source-linked comparisons. EEG quality is not a substitute for rating evidence.
7. Optionally request an AI explanation with your configured provider and allowance. It explains saved measurements and context; provider failure leaves numerical results and earlier reports intact.

**Explain existing results** creates a new explanatory derivative without rerunning numerical analysis or unlocking a historical plan. Old narratives and original measurements remain unchanged. More readable reporting does not retroactively validate an endpoint.

## Review and share

Live/replay views are passive. **Save snapshot locally** preserves a derived review window without an AI request; it does not replace LabRecorder. A historical snapshot or delayed explanation is not current live status.

Signal Quality & Cleaning Review retains source-aligned original, explicit current-transform preview, candidate and removed-signal views. A preview is not replay of a historical locked derivative. No candidate or explanation automatically replaces a recipe or XDF. Reduced line noise alone does not prove neural preservation.

Review consent, identifiers, raw telemetry, media rights and the file ledger before sharing. Default AI/result-review exports exclude full-resolution telemetry; explicit private export still needs privacy review. Read **BUILD_REPORT.md** for the release's actual tests and remaining limits. No hardware, clinical, timing or scientific validation follows merely from software completion.

