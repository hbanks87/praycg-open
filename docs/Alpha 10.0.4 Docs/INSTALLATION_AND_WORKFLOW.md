# PRAYCG Control Center Alpha 10.0.4

## Installation and practical workflow guide

This guide follows the controls shipped in version `1.0.0-alpha.10.0.4`. It covers installing the application, conducting or rehearsing a study, analyzing a recording, sharing a reviewed package, and using an external AI collaborator without confusing a proposal with approved software.

PRAYCG is local-first research software. A completed calculation is not proof that an experiment, interpretation, or device is scientifically valid. Preserve warnings, missing measurements, failed runs, and unexpected findings. Do not edit locks, fingerprints, or old results to make a check pass.

## 1. Install or upgrade safely

1. Finish any active acquisition. Stop and save LabRecorder, close the protocol runner normally, and then close the older Control Center. Do not upgrade while a recording is active.
2. Back up your Study Workspaces, recordings, stimulus materials, and analysis reports separately from the application. Keep the previous release until you have checked the new one.
3. Extract the entire public ZIP into a new writable local folder. Do not launch inside the ZIP, merge releases, or overwrite an older installation. In the public download, keep the `app` folder beside `INSTALL.bat` and `START_PRAYCG.bat`. The developer source tree has a different, flatter layout; ordinary users should use the public download.
4. Install native Windows Python 3.11 with Tcl/Tk support. The launcher checks the usual per-user installation, the Windows Python launcher, and PATH, accepting Python 3.11 rather than an arbitrary installed version.
5. Double-click `INSTALL.bat`. Its default is a full installation: Core plus the isolated Live Monitor environment. Internet access is normally needed for dependency installation.
6. Read the component results before closing the installer. Core passing while Live Monitor fails is partial success, not a complete installation. Preserve the failing step and error message.
7. Double-click `START_PRAYCG.bat`.
8. Open **Settings**. Use **Use Bundled Paths** for this release's packaged tools. Set or verify the external PsychoPy and LabRecorder paths. **Auto-find PsychoPy / LabRecorder** is also available in **Run Session**; review anything it finds.

The download does not include Python, dependency wheels, PsychoPy, LabRecorder, or every device driver/bridge. A catalog entry is not an installed device integration.

Core installs into the selected Python 3.11 interpreter; the installer does not create a separate Core environment. It can therefore update packages in that interpreter. Live Monitor uses `app/.live-monitor-env/` and its own dependencies. Do not point it at PsychoPy's interpreter or manually merge those environments.

For an optional installation mode, open a terminal in the extracted folder and use one of these commands:

```text
INSTALL.bat -Mode minimal
INSTALL.bat -Mode monitor
INSTALL.bat -CheckOnly
```

`minimal` requests Core only. `monitor` installs or repairs Live Monitor only. `CheckOnly` checks the requested components without installing packages or creating an environment; a missing component can correctly fail. Modes can be combined with `-CheckOnly`.

Installation records are under `%LOCALAPPDATA%/PRAYCG/installation_logs/`; captured component environments are under `%LOCALAPPDATA%/PRAYCG/environment_locks/`. These checks do not connect hardware or establish synchronization. If you move the application, reinstall/check the monitor environment in its new location: a virtual environment is not a reliably portable folder.

## 2. Understand the workspace and tabs

The main tabs are **Home**, **Operator Confidence**, **Choose Protocol**, **Prepare Materials**, **Connect & Check Equipment**, **Live Monitor (optional)**, **Run Session**, **Analysis Forge**, **Research Exchange**, and **Settings**.

On **Home**, the **Guided Session Workflow** provides **New**, **Open**, **New Session**, **Show Workspace in Explorer**, and **Close Workspace**. Use **New** for a new Study Workspace; use **Open** for an existing one. A workspace connects protocol choices, preparation, acquisition evidence, run identities, analysis decisions, and reports.

**New Session** is not the same as **Start New Equipment Session**. The former creates a workspace session; the latter creates an acquisition run identity and evidence folder. Neither makes previously inspected outcomes unknown or turns post-hoc decisions into prospective ones. Keep only one Control Center operating a given workspace.

**Show Workspace in Explorer** opens Windows Explorer for inspection. It is not the analysis-folder selection dialog. Later, use **Analysis Forge → Select Run Folder** to actually choose a dataset.

The Home **Running Tools** area shows individually launched processes, their status, runtime, logs, and controls. Use the relevant row when troubleshooting; do not stop unrelated programs just because their names resemble a PRAYCG tool.

**Operator Confidence → Open Operator Confidence Hub** provides rehearsals, diagnostics, readiness/recovery evidence, and hardware-development checks. **Open Tool Guide** explains those tools. Synthetic rehearsal and adapter conformance do not approve participant acquisition or grant ARM authority.

## 3. Choose the protocol and prepare materials

1. Open **Choose Protocol** and select an actual protocol in the **Protocol Atlas** tree.
2. Read **Selected Protocol**, including its purpose, authors/sources, measures, limitations, timeline, and required inputs.
3. Select **Use This Protocol**. This freezes a protocol selection; it does not select hardware or authorize acquisition.
4. Open **Prepare Materials**. Supply the required files by their stated purpose. A stimulus package, source video, event file, channel map, and image directory are not interchangeable.
5. Use the preparation tool required by that protocol. Review its output package and fingerprints before continuing. Some generated-task protocols do not require an external stimulus package; follow the displayed requirement rather than adding an unrelated file.
6. Select **Continue to Connect & Check Equipment →** when preparation is complete.

Use **Change Protocol** if you deliberately need another protocol while no acquisition is active. A changed protocol or material can invalidate downstream readiness evidence; this is not permission to reuse an old session lock.

Public names describe tasks or measurements without proving their proposed explanation. Original source authors and the PRAYCG adaptation byline have different roles. Citations are useful provenance, not permission to redistribute another person's media or code, endorsement, or scientific approval.

## 4. Select and lock equipment

**Connect & Check Equipment** contains five steps:

- **1. Hardware Selection**: choose the devices you intend to use. **Open Hardware Forge** opens the hardware workbench. Inspect validation details and the selected-device tray, then use **Create Hardware Profile →**.
- **2. Hardware Profile**: inspect the draft and use **Review, Approve, and Lock Draft**. For an existing profile, use **Load Existing Reviewed Profile**, verify its contents, and **Lock Active Profile for Connect & Launch**.
- **3. Connect & Launch**: press **Start New Equipment Session**. The displayed new run ID and evidence folder identify this acquisition. Use the launch controls generated from the locked profile.
- **4. Live Checks**: use **Refresh Visible LSL Streams** and inspect the expected versus visible streams. **Open Live Stream Monitor** shows current delivery and signal information. Run the applicable EEG and ALS checks.
- **5. Monitor, Record & Arm**: review configuration, run the required equipment check, confirm the session, and mark it ready.

One bridge button may publish several streams. Only one program may own an OpenBCI serial port at a time. A previously launched or unrelated outlet cannot simply stand in for the current run's required stream identity. If no reviewed launcher exists, the interface should report that limitation rather than guess a command.

For an ALS-capable profile, use **ALS Barcode Placement Test** and inspect the result. **ALS Holder Calibration** is a separate tool. For EEG, **EEG Signal Quality / Contact 0–100** provides diagnostics; it is not a direct impedance measurement or a guarantee of usable neuroscience data.

In step 5, run **Run Required 30-Second Equipment Check**. It samples the streams specified by the profile. Read the findings rather than treating any warning as an automatic go-ahead. Missing or ambiguous outlets, delivery problems, signal-quality failures, and unmeasured optical timing are different issues. **Open Latest Reports** exposes the evidence.

The reviewed profile defines channel count, sample rate, units, identities, and roles. Do not apply an OpenBCI channel map to another device because it has a similar channel count. Profiles without ALS do not acquire optical onset evidence; “not measured” is not PASS. Device catalog and synthetic-test coverage do not establish successful live use of every consumer device.

## 5. Participant acquisition versus bench testing

For a participant session, leave **Bench Test Mode (no participant)** off and satisfy the applicable live readiness requirements. Observe the session-mode banner. The software's checks do not replace your participant safeguards or scientific judgment.

For a software/equipment demonstration with no participant, deliberately enable **Bench Test Mode (no participant)** in step 5. It removes live-hardware readiness qualifiers so a software workflow can be exercised without connected equipment. It still requires a valid selected protocol, materials, reviewed hardware definition, file identities, and session lock.

Bench output remains labeled non-participant data. Bench does not invent missing streams, turn a failed measurement into PASS, or generate an XDF without a recording source. An ALS display-only check may report `BENCH_DISPLAY_ONLY`; that is not a physical light measurement. A no-ALS profile does not gain ALS by checking bench mode. The bench switch resets on application restart, so check the banner again.

A short demonstration is a separate choice. Enabling bench mode does not automatically shorten a protocol, and selecting a shortened preset does not automatically enable bench mode.

## 6. Configure, confirm, record, and launch

1. In **5. Monitor, Record & Arm**, inspect the protocol-dependent pre-start configuration. Set supported values before confirming. Native PRAYCG3, PRAYCG4, and SMG expose their supported baseline/washout and EEG-watchdog settings. Other protocols expose their own supported controls; a fixed schedule does not necessarily have an editable duration.
2. If the protocol offers **Short Demonstration**, review its changed timings and recorded reason. Use **Restore Protocol Defaults** when appropriate. Duration estimates may exclude responses, loading, or operator pauses.
3. Complete the equipment check for participant acquisition, or verify your explicit bench-mode choice for a no-participant rehearsal.
4. Press **Confirm Session Setup**. Review failures instead of bypassing them. **Open Confirmed Session Setup** opens the frozen record.
5. Press **Mark Ready to Run**. This is the current ARM control. **Disarm** and **Refresh Readiness** are available beside it.
6. Use **Open LabRecorder**. In LabRecorder itself, select the intended streams and recording destination, and start recording before the task events you need to capture. Launching LabRecorder is not the same as starting or saving a recording.
7. Open **Run Session**. Review **Locked Session Inputs** and **Resolved Inputs and Timeline Readiness**; **Refresh Locked Input Readiness** rechecks them.
8. Select **PsychoPy Python interpreter — canonical acquisition path**, then **Launch Locked Protocol Runner**. This is a launch-mode selection, not a request to run the file manually in another terminal. Coder options are explicitly for debugging/noncanonical use.
9. Follow the runner's displayed participant/operator instructions. Preserve its logs and events.
10. When the task ends, stop and save LabRecorder promptly. Check that the XDF has finished being written before preparing it for analysis.

Changing supported configuration after confirmation requires reconfirmation. Do not edit configuration or substitute assets while the runner/recording is active. A permitted pre-run custom variant is not automatically post hoc, but neither is it automatically preregistered.

If you forget to stop LabRecorder, preserve the raw recording. Governed preparation can use the protocol-window evidence without pretending the extra minutes belonged to the task. Do not manually trim away inconvenient samples or overwrite the original XDF.

## 7. Recover from cancellation or interruption

An acquisition run ID is not reused for a fresh task. After a terminal run, use **Start New Equipment Session**—which may display **Start Another Equipment Session**—then reconfirm and arm the next acquisition.

If PRAYCG says the runner is still active or an ACQUIRE-stage run is unresolved:

1. Inspect the matching row and log in **Home → Running Tools**. Check whether the actual runner or recorder is still operating.
2. Stop the real runner normally when appropriate. Save the recording before recovery; do not start another bridge against a still-owned device.
3. In **Analysis Forge**, open **Show / hide input overrides and recovery tools** and use **Finalize Interrupted Run** when the recorded state requires it.
4. Read the resulting disposition. An incomplete run remains incomplete; finalization is not a declaration that all planned data exist.
5. Start a fresh equipment session for a genuinely new run.

The application has checks for verified terminal/inactive sessions, pre-start cancellations without acquisition artifacts, and reused Windows process IDs. Those checks do not justify deleting ownership files or killing an unrelated process. If ownership remains uncertain, preserve the log and ask for diagnosis rather than forcing the gate.

## 8. Live observation and XDF replay

Open **Live Monitor (optional)**. Verify **Monitor Python** points to the isolated monitor environment; **Choose Python** allows explicit selection. For live inspection, choose **Find Live Streams**, select the intended streams, and **Monitor Selected**. **Simulated Signal** is an explicitly synthetic demonstration. **Close Viewer** stops the viewer, not your source bridge or LabRecorder.

The monitor is passive. It does not arm acquisition, claim bridge ownership, record raw data, publish replacement outlets, or implement closed-loop feedback. Signal traces and spectra are provisional diagnostics.

For replay:

1. Select the intended saved run, then **Replay Loaded Run**, or use **Choose XDF** for an explicit recording.
2. Wait for loading. Replay starts paused and is labeled offline.
3. Use **Play**, **Pause**, **Stop**, **−10 sec**, **+10 sec**, the position control, and **Speed:**. Stop rewinds; **Close Viewer** closes the viewing process.
4. Read elapsed/total time. Scroll the stream panels and optionally enable **Show signal diagnostics**.
5. Compare recorded streams with the saved hardware profile. Present, supported EEG, auxiliary analog/ALS, Polar RR, respiration, and marker streams can be shown. Missing or ambiguous hardware matches are disclosed.

Replay uses the recorded timeline, not today's equipment selections. Gaps remain gaps; an absent device cannot be reconstructed. Replay controls do not modify the XDF or set the analysis window.

## 9. Analyze a recording: required QC first

1. Open the correct workspace and **Analysis Forge**. Inspect **Run folder:** rather than assuming that the newest filename is correct. Completed-run association uses recorded identity; it may still need an operator override if files are missing or ambiguous.
2. To override, press **Select Run Folder**. The dialog is **Select the folder containing the recorded XDF**. Choose the run's data folder, not a general Downloads directory or mixed collection of sessions.
3. Use **Review Input Inventory** to inspect the exact evidence. Expand **Show / hide input overrides and recovery tools** if needed: **Choose XDF**, **Choose Events**, and **Choose Channel Map** bind explicit files. Keep them from the same run. **BIDS Export** and **Finalize Interrupted Run** are also there.
4. Press **Run Required QC**. This prepares the inputs and saves run-integrity, event-timing, and applicable EEG/line-noise evidence. You do not need to find an old separate “Prepare Run for Analysis” button in the simplified workflow.
5. Read **Saved QC reports and failure details** and the status message. The module registry unlocks after authenticated saved QC for these exact inputs, not merely because QC was pressed once on another dataset.

If two XDFs are present, deliberately select the correct one and verify its associated evidence. Do not delete data merely to remove ambiguity. A separate workspace may be needed if an analysis history mixes different recordings; **New Session** alone does not erase that history.

Known 60 Hz contamination should be documented, not confused with a software crash. It also does not justify ignoring missing events, gaps, insufficient duration, or an invalid estimator. In this release, the continuous preprocessing derivative can return `NOT_ESTIMABLE` for discontinuous EEG instead of filtering across missing acquisition time. Choosing a continuous window or another validated method is a documented new analytical decision, not a reason to erase gaps.

## 10. Choose methods, run the plan, and read reports

After QC, **2. Choose modules — prerequisites are included automatically** becomes available.

1. Use **Find:** and the **Actionable**, **Selected / locked**, **Unavailable**, or **All** filter.
2. Expand a category and select an actual module row. A blue category heading is not an analysis module.
3. Read **Availability**, **Automatic prerequisites**, and the detailed explanation. A planned prerequisite can be run first automatically; truly missing recorded inputs or unsupported mathematics remain a different limitation.
4. Press **Add to locked plan** for each desired compatible module. Each addition saves an immutable plan revision. There is no separate required “Build & Lock Plan” tab in this workflow.
5. Resolve any required EEG recipe using **Review EEG Recipe** or **Create / Revise Recipe**. Compatible modules can derive one when supported inputs make the choices unambiguous.
6. Press **Run / Resume Plan**. Use **Pause After Current** to stop progression after the current calculation; it does not kill that calculation. **Cancel Running Analysis** and **Retry Failed / Cancelled** are separate actions.
7. Scroll to **Persistent Analysis Results — one row per locked-plan module**. Select the intended **Analysis session:** and use **Refresh Results** or **Open Master Index**.

Each row's **Open** menu provides **Plain-English findings**, **View individual report**, **View standardized dashboard summary**, **Native reports**, **Figures**, **Tables / data**, **View execution receipt / provenance**, **Open module output folder**, and **Warnings and limitations**, where available. Suite child results have their own report entries. **Open Session Analysis Folder** opens the selected results location.

Read the native report alongside the plain-English account. The latter is an offline, deterministic explanation of recorded outputs—not a cloud AI interpretation or an additional statistical test. Refreshing results rebuilds the display; it does not rerun numerical analysis.

“Complete” concerns execution/output checks. “Complete with limitations” retains usable output with constraints. `NOT_ESTIMABLE` means the endpoint lacks sufficient support; it is not zero, a null result, or proof against a hypothesis. “Failed” requires execution/log diagnosis. Shortened data may support descriptive spectra while lacking the epochs, baseline coverage, or valid denominators needed for another module. Several windows from one person do not become several independent participants.

## 11. Revise an EEG recipe manually

**Create / Revise Recipe** opens **Create and Lock EEG Analysis Recipe**. The dialog configures existing packaged methods: exact condition-to-marker mappings; epoch start/end; baseline; time-frequency values; optional ERP windows; motor-imagery conditions/epoch; and RSA conditions/window.

Conditions use `name | MARKER_1, MARKER_2`. ERP rows use `name | condition | channel | start | end | polarity`. Use the actual recorded marker spelling and appropriate channel labels. Optional blank motor/RSA settings remain disabled. This is not the place to install an algorithm or choose arbitrary preprocessing code.

Use **Validate Draft**, inspect any error, then **Lock Recipe**. Locking creates a new immutable file under `recipe_revisions`, named `analysis_recipe_<fingerprint-prefix>.json`, and records the old recipe as its parent. Earlier plans and outputs remain historical. Requested modules are re-added through current eligibility checks; inspect the resulting new plan rather than assuming every re-add succeeded.

Existing hidden settings are retained, including an event-condition subset and RSA model matrix. An RSA matrix is tied to ordered conditions: simply reversing the names must not silently relabel it. Labels with pipes, commas, newlines/control characters, or outer whitespace cannot be edited losslessly in this form. ERP windows require a nonempty display name. Unsupported existing recipes are refused without modifying their files; obtain a separately reviewed revision rather than hand-editing a locked artifact.

## 12. Ask an AI to help with an EEG recipe

This path changes permitted parameters of existing methods. It does not install a new module or ask PRAYCG to execute an AI response.

1. Open **Create / Revise Recipe** for the intended dataset. Ensure the current form represents the parent you want to change.
2. Press **Export AI Recipe Request…**. The dialog is **Export a new local AI recipe request — no upload**, with suggested filename `PRAYCG_EEG_Recipe_AI_Request.zip`. Choose a new destination; existing files are not overwritten.
3. Keep this original request ZIP. It contains exactly `README.md`, `REQUEST.json`, `RETURN_SCHEMA.json`, and `RETURN_EXAMPLE.json`.
4. Inspect the contents before manually sharing with your chosen AI provider. No raw EEG is included and nothing is uploaded automatically, but event labels and recipe choices can still be sensitive.
5. Ask the AI to follow `RETURN_SCHEMA.json`, preserve the request/base/protocol identities, explain assumptions and limitations, and return one UTF-8 JSON proposal using the example's shape. Do not ask it to guess missing markers, scientific justification, or channel evidence.
6. Save the returned JSON locally. Back in the same recipe form, press **Review AI Recipe Proposal…**.
7. First select the original exported request ZIP; then select the returned proposal JSON. Do not choose a Python file, protocol candidate, or study-results ZIP.
8. In **AI recipe proposal — review changes**, read the summary, limitations, and exact parameter differences. Nothing is locked or activated. Choose **Keep current recipe** to cancel, or **Load reviewed proposal into form** to proceed.
9. Inspect the populated fields and press **Validate Draft**. Then separately press **Lock Recipe**. If you edit fields after validation, validate again before locking.
10. Return to the Forge, review the new recipe/plan binding, add any desired compatible modules, and **Run / Resume Plan** for the new analysis revision. Old results are not silently recalculated or replaced.

The returned schema is `PRAYCG_EEGRecipeAIProposal_v0_1`. Unknown/executable fields, duplicate JSON keys, nonfinite numbers, invalid shapes, oversized content, changed identities, and unsuitable parameters are rejected. Proposal JSON is limited to 256 KiB; the request ZIP is bounded to 1 MiB. Where observed marker labels were exported, proposed marker assignments must match that inventory. An absent inventory is not evidence that an invented marker exists.

If the form changed after export, create a fresh request; do not alter its fingerprints to force a match. Loading verifies that the reviewed parameters survive the actual form parser, restoring the previous form if they do not. RSA order/model changes need an explicit compatible proposal. New preprocessing filters, executable algorithms, dependency installers, and module-registry changes are outside this return contract. Changes after outcomes are known remain exploratory/post hoc.

## 13. Design a protocol with an AI collaborator

This is a different path from recipe revision. Its supported endpoint is a reviewed, staged design candidate—not a newly runnable Atlas entry.

1. In **Choose Protocol**, press **Create New Protocol with AI Docs…**. The separate window is **PRAYCG Protocol AI Docs Builder v0.1**.
2. Work through **1. Concept and hypotheses**, **2. Design and stimuli**, **3. Measures and safeguards**, and **4. Review and create**. Explain the task, falsifiable predictions, comparison conditions, materials, timing, hardware roles, measures, confounds, analysis, safeguards, sources, and unresolved choices. State uncertainty instead of inventing an answer.
3. If adapting an existing study, explicitly select **Use study context…** and review its identity/privacy preview. Choose the intended purpose. Explaining results or requesting post-hoc analysis is not an instruction to replace the acquired protocol.
4. Use **Save draft revision** to preserve your work; **Load saved draft** reopens a draft. Revisions retain lineage. Choose a new output folder/name when generating another package; existing design folders are not overwritten.
5. Press **Create Protocol AI Docs**. The completion dialog identifies the editable folder and `UPLOAD_PROTOCOL_AI_DOCS.zip`, and offers to open the folder.
6. Review the outgoing documents before manually uploading. They include your input, design brief, handoff, `protocol_draft_manifest.json`, `AI_RETURN_INSTRUCTIONS.md`, schemas, `protocol_review_capabilities_v1_0.json`, and `protocol_candidate_FORMAT_EXAMPLE.json`. The format example is not an implementation of your design.
7. Ask the AI for `protocol_candidate.json`, `DESIGN_REVIEW.md`, and `CHANGE_SUMMARY.md` following the included instructions. For a new Atlas design, use schema `PRAYCG_ProtocolAtlasModule_v2_0` and the draft-review schema. Keep `approval.status` as `DRAFT`; do not fabricate reviewer names, approval dates, sources, or permissions.
8. Save the returned files locally. In **Choose Protocol**, select **Review AI Protocol Return…** to open **Protocol Candidate Review — no installation or execution**.
9. Under **Protocol module**, use **Browse** to select the returned candidate JSON—not the outgoing ZIP, design manifest, Markdown, or Python. Select a separate **Review output folder**.
10. Press **Check Returned Candidate**. Read errors, cautions, engine bindings, and the timeline. Correct errors in a new candidate revision. **Save Timeline Preview (not execution)** saves a review artifact; it does not present stimuli.
11. After human design review, press **Human Review + Stage Candidate** and enter the actual reviewer's name. Use **Open Build Folder** to inspect the staged evidence.

The new folder contains `source_protocol_candidate.json`, `validation_report.json`, `timeline_preview.json`, and `candidate_review_manifest.json`. Its status is `HUMAN_REVIEWED_CANDIDATE_NOT_RUNTIME_APPROVED`. Stop here: it will not automatically become selectable in the runnable Atlas.

The reviewer accepts supported Atlas or native `PRAYCG_ProtocolModule_v1_0` JSON candidates up to 4 MiB. Native runtime configuration is limited to the supported PRAYCG3/PRAYCG4/SMG contracts; prefer Atlas syntax for a new design. Unsupported task behavior, new stimulus engines, closed-loop control, or new analysis algorithms require a design-only engine-development proposal and separately reviewed implementation/tests. Do not copy AI files into packaged libraries or change approval fields to bypass admission.

Keep the outgoing `document_set_sha256` and draft identity with the return. The requested change summary reports that lineage, but the current candidate importer does not automatically verify linkage to the outgoing design package. Large/generated schedules can be shown declaratively rather than fully expanded. Neither a valid schema nor a timeline preview proves playback, timing, scientific validity, participant safety, or runtime admission.

## 14. Bundle results or a private study

Choose the package for your purpose; similarly named AI controls accept different artifacts.

For derived outputs, use the Forge's **Shareable derived-results bundle — excludes raw data**. Review outcomes, use **Mark Outcome Review Complete** when appropriate, then **Build Local Results Bundle**. **Review Latest Local Bundle**, **Verify Bundle Portability**, and **Open Latest Bundle** inspect the result. Raw XDF/EEG-class files are excluded. “Shareable” is not automatic privacy or publication approval.

The retained **Private full-study / AI-ready package — local export only** panel offers **Private full-study archive** or **AI-ready study package**, with **Explain existing results**, **Replay original analysis**, or **Additional post-hoc analysis**. Optionally choose **Optional Theory / Porting Pack…**; it supplies background, not governing authority. Use **Preview and Create Package…**, review contents/missingness, and choose a new ZIP. If the immediate confirmation prevents examining the preview fully, decline first, inspect the preview, then repeat when ready. **Verify Package…** checks the saved archive.

Available XDFs, events, channel maps, anchors, familiarity/context records, hardware evidence, plans, recipes, software snapshots, and outputs can be inventoried. “Full” cannot recover information never recorded. Inspect the actual ledger; do not assume every category is present or exact historical dependencies are preserved.

For a study-analysis return, **Review AI Return…** asks for the returned ZIP and the original exported study ZIP. Its root `RETURN_MANIFEST.json` must use `PRAYCG_ExternalAnalysisReturn_v0_1`, matching dataset/input identities, with a hashed file ledger restricted to `outputs/`, `reports/`, and `proposals/`. Verified artifacts can be staged in a new `external_analysis_revisions` folder as untrusted external/post-hoc work. Returned code is not executed and accepted results/plans are not overwritten. This is neither the single-JSON protocol reviewer nor the recipe reviewer, and it is not automatic promotion into the locked-plan result dashboard.

## 15. Research Exchange and the local DATA catalog

For Research Bundle 1.0 exchange, open **Research Exchange → 1. Export study**. Choose **Private replay study**, **AI-ready review**, or **Results review only**. The default tier is `PRIVATE_LOCAL`.

Designated private context and raw telemetry start unchecked. Explicitly select both if raw inputs are needed; raw inclusion also requires private context. Review-only exports generally cannot replay analyses requiring omitted data. All formats, including results-only, may retain sensitive values in byte-preserved reports/code.

Use **Preview selected study…**, inspect inventory, size, missing/excluded items, and hashes, then **Create local ZIP…** in the preview. Changed inputs require another preview. Publication-candidate tiers require recorded privacy, consent/sharing-authority, and content/software-rights review references; recording those declarations is not certification. Nothing is uploaded.

For another bundle, **Verify bundle…** checks it read-only. In **2. Import & reanalyze**, select **Import research bundle…** and **Review imported contents**. Import preserves independent originals and receipts; it does not execute archived scripts or install dependencies. Choose the source plan explicitly. If needed, explicitly allow clearly labeled current-build reanalysis, then **Prepare reanalysis**, inspect the plan/differences, and **Run prepared reanalysis**. Required QC comes first. **Cancel reanalysis** requests a controlled stop; **Review comparison report** shows actual coverage and differences, not assumed equivalence. **Export completed reanalysis…** creates a new linked package.

In **3. Local DATA catalog**, use **Register existing bundle…**, **Search / refresh**, **Verify selected**, **Import selected**, **Details / relationships**, **View verified report…**, and **Link studies…**. This catalog is local, not an online publication service. Report previews recheck evidence and display bounded inert text. A relationship records lineage, not successful replication. File integrity, executed replay, second-machine verification, and scientific validity are separate claims.

## 16. When something does not work

Preserve the exact message, selected workspace/run, component log, and relevant receipt. Do not modify originals to clear an error.

- Installation: identify which component failed; retry the appropriate mode rather than mixing Python environments.
- Confirmation/arming: check protocol/material identity, reviewed hardware profile, current session, configuration, and participant-versus-bench banner.
- Blank module list: check required QC status and the catalog filter. Select a module row, not its category.
- Recipe return rejected: keep the original request; check stale parent/form, schema, markers, bounds, unsupported labels, and missing ERP names. Export a fresh request after intentional edits.
- Protocol candidate not visible in Atlas: staging is not installation; reviewed developer integration is still required.
- Missing report: inspect the correct analysis session and execution receipt; refreshing does not rerun a failed calculation.
- Bundle failure: preserve preview/source identity; a valid hash cannot replace missing data or prove a provider can process XDF.

Before sharing any package, independently review identifiers, consent/sharing authority, stimulus/software rights, recipient/provider handling, and size limits. No PRAYCG export uploads automatically. Keep your own original study, outgoing request/package, returned proposal, and subsequent revision. PRAYCG is alpha research software, not a clinical diagnostic system.
