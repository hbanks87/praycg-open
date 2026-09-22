# PRAYCG Control Center Alpha 10.2.1 — Detailed Workflow

This guide follows the controls and labels in Alpha 10.2.1. It covers a study from local workspace creation through acquisition, analysis, review, replay and research exchange.

PRAYCG is alpha research software. A successful software check does not establish scientific validity, participant safety, calibration, cortical origin, causality or clinical utility. Preserve failures, warnings and missing estimates as evidence; do not relabel them as passes.

## Workflow at a glance

```text
Study Workspace
  → Choose Protocol
  → Prepare Materials
  → Hardware Selection
  → Hardware Profile
  → Equipment Session
  → Connect & Launch
  → Live Checks and pre-start configuration
  → Confirm Session Setup
  → Mark Ready to Run
  → Launch Locked Protocol Runner
  → Record all required streams plus StasisMarkers in LabRecorder
  → Stop and save LabRecorder
  → Run Required QC
  → Add modules to the locked plan
  → Run / Resume Plan
  → Review per-module results and plain-English findings
  → Build a local results, private study or Research Exchange bundle
```

## 1. Before starting a study

1. Start the application with `START_PRAYCG.bat` from the extracted release folder.
2. Open **Settings** and select **Use Bundled Paths** if the packaged tool paths are not already selected.
3. Use **Auto-find ALL**, **Find LabRecorder** or **Find PsychoPy** as needed, then inspect the resolved paths. PsychoPy and LabRecorder are external applications; the PRAYCG installer does not install them.
4. Leave **PsychoPy Python interpreter — canonical acquisition path** selected in **Run Session** for governed acquisition. The other runner modes are labeled debugging, experimental or noncanonical for a reason.
5. Close older Control Centers that use the same workspace. Do not run two Control Centers against one workspace.

The default study-data root on Windows is `C:\PRAYCG`. Application settings and the pointer to the active workspace are separate, under the user's application-data folder. Extracting a new release does not move or rewrite earlier studies.

### Three identities that should not be confused

- A **Study Workspace** is the persistent study record containing all its sessions, inputs, decisions, results and exports.
- **Home → New Session** starts another logical session inside that workspace. It preserves earlier evidence and clears only the new session's acquisition-, analysis-, review- and export-bound state.
- **Connect & Check Equipment → Start New Equipment Session** creates a fresh acquisition/run UUID and evidence directory for one attempted recording.

Neither New Session nor a new equipment UUID makes an analysis prospective after its outcomes have already been examined.

## 2. Create or open the Study Workspace

On **Home**, use the **Guided Session Workflow** panel.

1. Select **New** and enter a study display name, or select **Open** and choose that study's `study_workspace.json`.
2. Confirm that the **Current Study** strip and the Home summary show the intended study and session.
3. Use **Show Workspace in Explorer** when you need to inspect its files. Use **Close Workspace** only to detach it from the application; this does not delete the workspace.

The workflow buttons on Home are status shortcuts, not independent copies of the tools. They lead to the same **Choose Protocol**, **Prepare Materials**, **Connect & Check Equipment**, **Run Session** and **Analysis Forge** tabs.

Use **New Session** only when beginning a genuinely new session. It is blocked while required QC or governed analysis is running. Starting a new session preserves earlier plans, reports and knowledge that outcomes were viewed.

## 3. Choose and lock a protocol

1. Open **Choose Protocol**.
2. Search by current name, former name or protocol ID if helpful.
3. Select an individual protocol row under **Protocol Atlas** or **Installed Protocols**. Selecting a category is not sufficient.
4. Read the **Selected Protocol** panel, including the task, intended population, required inputs, authors, sources, limitations and scientific status.
5. Select **Use This Protocol**.
6. Confirm that the panel now identifies the confirmed protocol, then select **Continue to Prepare Materials →**.

Use **Change Protocol** before acquisition if the wrong protocol was selected. A later protocol change invalidates downstream session-bound evidence; it does not rewrite an old lock or recording.

Protocol-library inclusion means the declared runner and inputs passed the package's software admission checks. It does not validate a hypothesis or grant participant-acquisition authority.

## 4. Prepare and bind protocol materials

The **Prepare Materials** tab is filtered by the confirmed protocol.

1. In **Required Protocol Files**, use each row's **Choose File** or **Choose Folder** control. Bind the file to the purpose named in that row; similar-looking files are not interchangeable.
2. If the protocol uses a prepared pack or master stimulus, select an individual row in **Compatible Prepared Materials** and choose **Use Selected Compatible Asset**. For a bundled example, the button may read **Install and Use Working Copy**.
3. Use only the preparation buttons displayed under **Optional Preparation Tools** for this protocol. A generated-task protocol may explicitly require no external media.
4. Inspect the status of every required row, then select **Continue to Connect & Check Equipment →**.

**Refresh Compatible Assets** rescans the current state. **Add Master PRAYCG Stimulus (.mp4)** and **Revalidate & Tag Existing Masters** are specialist intake tools, not substitutes for the protocol's declared requirements.

Bundled sample material remains `DEMO_ONLY` unless separate evidence says otherwise. Installing a writable copy does not promote its scientific status. Once **Confirm Session Setup** is created, changing a bound input makes that session lock stale; confirm a new setup rather than editing the evidence.

## 5. Build or load a hardware profile

Open **Connect & Check Equipment**. Its five sub-tabs are intended to be used in order:

1. **Hardware Selection**
2. **Hardware Profile**
3. **Connect & Launch**
4. **Live Checks**
5. **Monitor, Record & Arm**

### 5.1 Select the intended use first

**Profile intended use** defaults to `HUMAN_CONNECTED`. Keep that setting only for routes whose existing review and physical evidence are appropriate for the planned use.

The newly integrated Crown, Muse S Athena, Polar H10 ECG, GazePoint and reviewed external-publisher routes are `EXPERIMENTAL_EVALUATION`. To use one:

1. Change **Profile intended use** to `EXPERIMENTAL_EVALUATION`.
2. Accept the **Bench Test Mode (no participant)** warning.
3. Enter an honest bench-test reason.

Changing intended use clears the validated selection tray and any current UI launch lock. Do it before building the profile. A profile containing an experimental route makes the whole session bench-only and not participant-data eligible. Software availability and physical validation are separate states.

### 5.2 Add hardware from the library

1. Expand the needed role in **Hardware Library**. Roles include EEG, ECG/heart timing, respiration, ALS, gaze/pupil, motion, optical and status/markers as applicable.
2. Select the exact device or route row, not its category.
3. Read **Selected Hardware and Validation**.
4. Select **Validate and Add Selected Device**.
5. Confirm that it appears in **Validated Hardware Selections — one row per device**.
6. Repeat for the required equipment. Use **Remove Selected Role from Tray** or **Clear Validated Tray** to correct the draft before creating a profile.

This validates the packaged definition and admission state. It does not open the device, inspect electrodes, prove signal delivery or grant acquisition authority.

### 5.3 External-publisher routes

Pupil Core, Pupil Neon, OpenMuse and OpenViBE are not launched or installed by PRAYCG.

1. Install and start the external publisher yourself.
2. Select the exact product route in **Hardware Library**, then select **Validate and Add Selected Device**.
3. In **Review external publisher for hardware profile**, select **Publisher requirements and limitations…** and confirm the required publisher settings.
4. Select **Refresh streams**, choose the exact outlet, and inspect its UID, source ID, channel order, labels, units, rate and format.
5. Select **Review and add to hardware tray** and complete the product-specific facts honestly. Do not invent unavailable firmware, calibration or timing facts.

The resulting module freezes that observed outlet and product review. If the publisher restarts and its outlet UID or descriptor changes, build and review a new profile and use a new equipment session; a same-name replacement cannot silently satisfy the old lock.

**Use existing LSL stream…** is also available for an additional observed outlet. A generic attachment does not replace missing required profile hardware or satisfy its physical checks. Pending generic attachments are frozen only at **Confirm Session Setup**.

### 5.4 Create, review and lock the profile

1. Select **Create Hardware Profile →** or **Create / Refresh Draft from Validated Tray**.
2. On **Hardware Profile**, inspect the draft and select **Review, Approve, and Lock Draft**.
3. Enter the actual reviewer's name. This attests to review of the definitions, not connected-device testing or electrical safety.
4. Confirm that the profile appears under **Active reviewed and UI-locked profile**.

The review action also locks the resulting profile for the **Connect & Launch** controls. When loading a previously reviewed profile, use **Load Existing Reviewed Profile**, then **Lock Active Profile for Connect & Launch**. A UI lock creates exact launch actions but does not ARM a session.

### 5.5 Alpha 10.2.1 route boundaries

| Route | How it is started | Important boundary |
| --- | --- | --- |
| Neurosity Crown / BrainFlow OSC | Locked PRAYCG connector action | Requires the full 32-character Crown device ID and OSC Raw Mode. It is the BrainFlow OSC signal, not the Neurosity SDK `rawUnfiltered` route. No ALS is supplied. |
| Muse S Athena / BrainFlow p1041 | Locked PRAYCG connector action | Requires the Bluetooth address. EEG, motion, raw optical and diagnostics are separate. Raw optical data are not validated fNIRS. No ALS is supplied. |
| Polar H10 ECG waveform | Locked PRAYCG connector action | Requires the exact device ID/address. This is a 130 Hz ECG route, separate from the irregular RR route. Two simultaneous BLE clients may not work. |
| GazePoint GP3 or GP3 HD | Locked PRAYCG connector action | Start GazePoint Control and calibrate there first. Select the exact GP3 or GP3 HD profile. |
| Pupil Core, Pupil Neon, OpenMuse, OpenViBE | External publisher plus exact outlet review | PRAYCG does not download, start or stop the publisher. Product, version, channel and timing facts remain explicit. |
| Cerelog 16 | Withheld/catalog entry | It cannot become runnable merely by selecting it; its exact physical acquisition contract remains unresolved. |

See `app/docs/HARDWARE_ROUTES_ALPHA_10_2_1.md` in the installed release for product-specific limits and upstream sources.

## 6. Create the equipment session and start streams

1. Open **3. Connect & Launch**.
2. Select **Start New Equipment Session**. This creates the run UUID and a dedicated evidence folder. If a previous authorized runner is still active or unresolved at `ACQUIRE`, the action is correctly blocked.
3. Use each exact action shown under **Streams in the locked hardware profile**.

For a managed Crown, Athena, H10 ECG or GazePoint route:

1. Its locked action opens **Multimodal connectors — Alpha 10.2.1**.
2. Enter the exact device identifier or GazePoint Control host.
3. Select **Start connector**.
4. Read the status and verify sample delivery under **Live Checks**. Process startup alone is not evidence that samples are flowing.
5. Leave the connector running through LabRecorder capture. Closing the panel leaves it running.

Opening **Manage running connectors…** by itself is a management view. **Start connector** is enabled only after entering through the exact action generated by a reviewed and locked profile.

For a locked external-publisher route, select its **Attach … / reviewed observed outlet** action, select the same reviewed live outlet and choose **Attach selected outlet**. PRAYCG rechecks that identity again before confirmation, ARM and direct runner launch. PRAYCG never takes ownership of that external publisher.

Never launch another bridge for the same serial port or device simply because it has a familiar stream name. Only the identities bound to this equipment session can satisfy readiness.

## 7. Inspect streams and run equipment checks

In **4. Live Checks**:

1. Select **Refresh Visible LSL Streams** and compare the visible outlets with **Expected and visible LSL streams**.
2. Use **Open Live Stream Monitor** for passive inspection if useful.
3. For EEG profiles, use **EEG Signal Quality / Contact 0–100** as a diagnostic. It is not a direct impedance measurement.
4. For a profile that actually includes ALS, use **ALS Barcode Placement Test** and, when needed, **ALS Holder Calibration**.

Do not run or simulate an ALS test for a profile with no ALS role. Crown and Muse S Athena do not gain ALS simply because another profile supports it.

In **5. Monitor, Record & Arm**:

1. Review the protocol-dependent pre-start configuration before locking the session.
2. Select **Run Required 30-Second Equipment Check** for participant acquisition. This samples every stream in the locked profile and saves readiness evidence.
3. Optional diagnostics are **Observe Stream Stability for 30 Seconds** and **Contract-Bound Drift / Sync Observation**. They do not repair data, confirm the session or ARM it.
4. Use **Open Latest Reports** to inspect the saved evidence.

### Bench Test Mode

**Bench Test Mode (no participant)** bypasses live hardware, missing-stream, timing, signal-quality, ALS-placement and demo-only scientific-use qualifiers for confirmation and ARM. It does not bypass:

- the selected protocol and required materials;
- the reviewed hardware definition and profile identity;
- file-integrity checks;
- the runtime session lock; or
- exact external-outlet rechecks when such an outlet is being used.

Bench outputs are permanently labeled `BENCH_TEST` and not participant eligible. Bench mode resets off when the application restarts. It may still be useful to run the checks diagnostically; their failures remain recorded even though they do not block a bench lock.

## 8. Freeze the pre-start configuration, confirm and ARM

The pre-start configuration panel follows the selected protocol module.

- Use **Restore Protocol Defaults** to return to that protocol's declared configuration.
- Use **Short Demonstration** only where the protocol explicitly offers it. For native PRAYCG3, PRAYCG4 and SMG, it declares 10-second baseline/washout/final-baseline settings and may disable the EEG watchdog. It does not automatically enable Bench Test Mode.
- Enter a **Reason for custom settings** whenever the selected values differ from protocol defaults.
- Some Atlas schedules are intentionally fixed. A value that the runner does not consume is not exposed as an editable scientific control.

Set the values before confirmation. A supported pre-run variant is not automatically post hoc, but it is not automatically preregistered either. Changing it after confirmation makes the lock stale.

Then:

1. Select **Confirm Session Setup**.
2. Enter the session operator. For participant acquisition, enter a non-identifying participant code, never a name. Bench sessions receive a reserved `BENCH-…` identity automatically.
3. If a participant setup is `CAUTION` or uses a noncanonical configuration, read the warning and record a specific decision reason if proceeding is justified. Accepting a caution does not convert it to PASS.
4. Confirm the success message and, if desired, select **Open Confirmed Session Setup** to inspect the immutable JSON.
5. Select **Mark Ready to Run**.

The readiness line should show the current lock and ARM state. A change to the protocol, materials, hardware profile, session mode or protected configuration disarms/stales the session. Create a new lock; do not edit hash or ownership files.

## 9. Launch the runner and record with LabRecorder

1. Open **Run Session** and inspect **Locked Session Inputs — what must pass before arming**.
2. Keep **PsychoPy Python interpreter — canonical acquisition path** selected.
3. Select **Launch Locked Protocol Runner**.

The canonical runner can be launched only once for an acquisition UUID. If another run is needed, create another equipment session, confirm it and ARM it.

### Correct LabRecorder order

For the packaged runners, do not begin recording before the runner creates its marker outlet.

1. Launch the locked runner first.
2. Wait for its windowed LSL preflight hold. At that point `StasisMarkers` is online.
3. Open or switch to LabRecorder. Click **Update**.
4. Select `StasisMarkers` and every required hardware/profile outlet. Include any reviewed external attachments. Do not assume that a checked name from an earlier session is the current exact outlet.
5. Choose the intended LabRecorder output location and select **Start**.
6. Return to the runner and follow its on-screen instruction to leave the preflight hold. Native PRAYCG3/4/SMG uses a right-click after recording is underway; Protocol Atlas runners use the Space bar.
7. Complete the task without changing the frozen inputs or configuration.
8. When PRAYCG reports **Protocol complete — stop LabRecorder now**, stop and save LabRecorder promptly.

Recording a few extra minutes does not erase the run; the raw XDF retains those samples and governed analysis uses event/window evidence. It is nevertheless better to stop promptly. Never trim or overwrite the raw XDF to make a run look cleaner.

After recording, use **Manage running connectors… → Stop selected** for PRAYCG-owned experimental connectors and wait for them to finish. Close an external publisher yourself only after confirming that no other recording uses it.

## 10. Analyze the completed recording

Open **Analysis Forge**. The normal flow is:

```text
Run Required QC → Add to locked plan → Run / Resume Plan → Review → Bundle
```

### 10.1 Select and prepare the run

After a successful runner exit, PRAYCG tries to associate the recording by run UUID. Stop/save LabRecorder before expecting the final XDF to appear.

1. Confirm the displayed **Run folder**.
2. If it is wrong or unresolved, select **Select Run Folder** and choose the folder containing the intended XDF. This control selects a folder, not an individual file.
3. Select **Review Input Inventory** to inspect resolved XDF, events, channel map and provenance.
4. If there are multiple or ambiguous candidates, select **Show / hide input overrides and recovery tools**, then use **Choose XDF**, **Choose Events** or **Choose Channel Map**. Use only evidence from the same acquisition.
5. Select **Run Required QC**.

Required QC prepares the run and saves run-integrity, event-timing and applicable EEG/line-noise evidence. A dirty signal is reported as dirty; it is not a software crash. Missing support stays missing. **Cancel Required QC** requests cancellation and retains evidence already completed.

The module registry appears only after saved QC for these exact inputs is authenticated. Use **Saved QC reports and failure details** when it does not unlock.

### 10.2 Create the cumulative locked plan

1. Under **2. Choose modules — prerequisites are included automatically**, select an individual module row, not a category.
2. Read its availability, interpretation, prerequisites and limitations.
3. Select **Add to locked plan**.
4. Repeat for every desired standard or exploratory module.

There is no separate final Lock button in the consolidated Forge. Every Add saves a new immutable, cumulative plan revision. Dependencies are inserted and ordered automatically; the user should not have to add preprocessing, NAST/NAS or another prerequisite manually merely to make a downstream module visible.

When a compatible EEG recipe is deterministically derivable, the Forge creates it automatically. Use **Review EEG Recipe** to inspect it. Use **Create / Revise Recipe** when the protocol or desired event-locked analysis requires a choice that cannot be inferred safely.

Add planned analyses before examining their outcomes when possible. A later addition is allowed but is labeled exploratory/post hoc; the earlier decision and result history remain preserved.

### 10.3 Run and monitor the plan

1. Select **Run / Resume Plan**.
2. Use **Pause After Current** to stop automatic progression after the active module. It does not terminate the calculation currently running.
3. Use **Cancel Running Analysis** for a controlled cancellation.
4. Use **Retry Failed / Cancelled** only for software failures or cancelled attempts. A scientifically `NOT_ESTIMABLE` result is not silently retried as if it were a crash.

The scheduler runs prerequisites first and continues independent branches after a branch-specific failure when safe. It does not turn contamination, insufficient duration or missing measurements into a valid estimate.

## 11. Review results and automatic interpretation

The **Persistent Analysis Results — one row per locked-plan module** area remains attached to the workspace session.

1. Select the desired **Analysis session**. Current and historical sessions are kept distinct.
2. Select **Refresh Results** to rebuild the display. Refreshing does not rerun numerical analysis.
3. Use **Open Master Index** for the session-level overview.
4. On each module card, open **Open ▾** and inspect:
   - **Plain-English findings**;
   - **View individual report**;
   - **View standardized dashboard summary**;
   - **Native reports**;
   - **Figures**;
   - **Tables / data**;
   - **View execution receipt / provenance**;
   - **Open module output folder**; and
   - **Warnings and limitations**.
5. For a suite, use **Show / hide … suite results** to reach each child module's independent reports.

The plain-English findings are an automatic, offline, deterministic interpretation of the module's recorded outputs. They do not contact an AI, rerun the statistics or replace the native scientific report. Use them as a guide to the actual estimates, caveats and missingness.

Status meanings:

- `COMPLETE`: the expected worker and output checks completed; this is not scientific validation.
- `COMPLETE_WITH_LIMITATIONS`: usable outputs exist with retained limitations.
- `NOT_ESTIMABLE`: the dataset does not support that endpoint. It is not zero and not a statistical null.
- `FAILED`: a software or processing failure requires log review.
- `BLOCKED` or `WAITING`: an input, dependency or execution condition remains unresolved.

## 12. Build local and private study packages

### Derived-results bundle

Under **Shareable derived-results bundle — excludes raw data**:

1. Select **Mark Outcome Review Complete** when that human review has actually occurred.
2. Select **Build Local Results Bundle**.
3. Use **Review Latest Local Bundle**, **Verify Bundle Portability** and **Open Latest Bundle**.

This bundle excludes raw EEG/XDF-class data. Structural verification does not prove second-machine execution or publication readiness.

### Private full-study or AI-ready package

Under **Private full-study / AI-ready package — local export only**:

1. Choose **Private full-study archive** or **AI-ready study package**.
2. Choose the purpose: **Explain existing results**, **Replay original analysis** or **Additional post-hoc analysis**.
3. Optionally select **Optional Theory / Porting Pack…** as background. It cannot override the frozen protocol, methods or observations.
4. Select **Preview and Create Package…** and inspect included, missing and private material before confirming a new ZIP.
5. Use **Verify Package…** to check the archive's identity and ledger.
6. Use **Review AI Return…** only with the original exported study ZIP. Returned material is reviewed and staged into a new external-analysis revision; no returned code is executed and no accepted result is overwritten.

These packages can contain raw biosignals, responses, device IDs, hostnames, paths and other identifying metadata. They are not automatically de-identified, encrypted, uploaded or approved for sharing. Review consent, authority, privacy, media rights and the receiving service's terms yourself.

## 13. Use Research Exchange / PRAYCG DATA

The **Research Exchange** tab is local and has three pages.

### 13.1 Export study

1. Select **Private replay study**, **AI-ready review** or **Results review only**.
2. Select the privacy-review tier: `PRIVATE_LOCAL`, `COLLABORATOR_REVIEW` or `PUBLICATION_CANDIDATE`.
3. If genuinely required, explicitly enable **Include designated private context, identifiers and original-path records** and **Include recorded inputs/raw telemetry (also requires private context)**. Both begin off.
4. For a publication candidate, complete the privacy, consent/sharing-authority and content/software-rights review fields with evidence references.
5. Select **Preview selected study…**, inspect the exact inventory, then create the local ZIP.
6. Use **Verify bundle…** for a read-only verification.

A review classification is not publication authority or legal certification. A raw-data replay generally needs both private-context and telemetry selections, but those selections also increase disclosure risk.

### 13.2 Import and reanalyze

1. Select **Import research bundle…**. Verification occurs before extraction to a new local import folder.
2. Use **Review imported contents**.
3. Select the intended archived source plan.
4. If the archived software/environment differs and current code is acceptable for the stated comparison, explicitly enable **Allow clearly labeled current-build reanalysis when original code/environment differs**.
5. Select **Prepare reanalysis**, inspect the frozen mapping and comparison policy, then select **Run prepared reanalysis**.
6. Use **Cancel reanalysis** only for a controlled stop.
7. Select **Review comparison report** after completion.
8. Use **Export completed reanalysis…** to create a separately reviewed child bundle linked to its source.

Imported originals remain inert. PRAYCG does not execute archived or AI-supplied code, install archived dependencies, overwrite the source study or grant acquisition authority.

### 13.3 Local DATA catalog

Use **Register existing bundle…**, **Search / refresh**, **Verify selected**, **Import selected**, **Details / relationships**, **View verified report…** and **Link studies…**. The catalog stays on this computer. A reanalysis or replication relationship records lineage; it does not establish successful replication.

Technical details are in `app/tools/Research_Exchange_v1_0/BUNDLE_FORMAT.md` and `app/tools/Research_Exchange_v1_0/REANALYSIS.md` in the installed release.

## 14. Create a protocol with AI assistance

### 14.1 Create the request package

1. In **Choose Protocol**, select **Create New Protocol with AI Docs…**.
2. Complete the builder tabs: **1. Concept and hypotheses**, **2. Design and stimuli**, **3. Measures and safeguards**, and **4. Review and create**.
3. Use **Save draft revision** when preserving an intermediate version is useful. **Use study context…** is optional and can contain private paths or identifiers; review it before sharing.
4. Select the appropriate **Purpose** and then **Create Protocol AI Docs**.
5. Review the generated folder and `UPLOAD_PROTOCOL_AI_DOCS.zip` locally before uploading it to an AI collaborator.

The request is a non-executable design handoff. It does not create a runner, install a protocol, approve hardware or validate the science.

### 14.2 Request the return

Ask the AI collaborator to follow the included return instructions and capability/schema files, preserve unresolved limitations, cite real sources and return the required `protocol_extension.json` plus its review/change summary. Keep the original request ZIP unchanged because its hashes establish return lineage.

An AI cannot make unsupported runners, hardware commands or analysis algorithms installable merely by naming them. Redesign unsupported components or treat them as a separate development project.

### 14.3 Review and install the return

1. In **Choose Protocol**, select **My Protocols / AI Return…**.
2. On **1. Import and review**, choose **Returned / local protocol JSON** and the matching **Original AI request ZIP**. The request ZIP may be omitted only for a genuinely local template.
3. Select **Review and rehearse safely**.
4. Read the request/return comparison, limitations, admission checks and bounded fake-I/O rehearsal.
5. If rejected, select **Create repair request…** and return that package to the AI along with the original request and current return.
6. When review actually passes, select **I reviewed the design, limitations and software rehearsal…**, then **Install to My Protocols** and enter the real local reviewer.
7. Return to **Choose Protocol**, refresh if needed, select the installed version under **Installed Protocols**, and use **Use This Protocol**.

Installation does not collect data or ARM anything. Media are selected later in **Prepare Materials**. Existing workspace locks continue to identify their original installed version even if **Installed versions → Activate selected version / roll back** changes future discovery.

See `app/docs/AI_AUTHORING_WORKFLOW_REVIEW.md` in the installed release for supported extension boundaries.

## 15. Create or revise an EEG recipe with AI assistance

The EEG recipe configures supported settings for existing analysis workers. It does not install a new algorithm.

1. In **Analysis Forge**, select **Create / Revise Recipe**.
2. Enter or review the supported conditions, event markers, epoch/filter/baseline settings, time-frequency values, optional ERP windows, motor settings and RSA choices.
3. Select **Validate Draft**.
4. Select **Lock Recipe** to create the immutable local revision.

For AI help:

1. Select **Export AI Recipe Request…** and review the ZIP before sharing it.
2. Ask the AI to return the documented recipe-proposal JSON, not executable code.
3. Select **Review AI Recipe Proposal…** and inspect the differences against the exact parent recipe.
4. Choose **Load reviewed proposal into form** or **Keep current recipe**.
5. After loading a proposal, select **Validate Draft** again and then **Lock Recipe**. Importing a proposal does not lock it, change a plan or run analysis.

Unsupported old recipe fields and RSA condition-order conflicts require explicit resolution. Do not discard them silently to make a proposal fit the editor.

## 16. Replay a recorded XDF

The **Live Monitor (optional)** tab is passive. It does not record, ARM, acquire bridge ownership or feed replayed samples back into LSL.

1. Select **Replay Loaded Run** for the run already associated with the workspace, or **Choose XDF** for an explicit file.
2. Wait for loading. Replay begins paused and is labeled offline.
3. Use **Play**, **Pause**, **Stop**, **−10 sec**, **+10 sec**, the position slider and **Speed**.
4. Read the elapsed/total clock and scroll the recorded stream panels.
5. Inspect hardware-profile mismatch, missing-stream, extra-stream and ambiguous-metadata warnings.

**Stop** rewinds and pauses the replay; **Close Viewer** stops only the observer. Replay uses the recording's timestamps and saved hardware evidence, not today's equipment selection. Missing samples or unrecorded devices are never reconstructed, and replay does not alter the XDF or analysis window. See `app/tools/Live_Monitor_v1_0/README.md` in the installed release for the technical limits.

## 17. Recovery and common blockers

### A runner was cancelled or failed before acquisition

When no acquisition artifacts were created and the evidence is unambiguous, PRAYCG records a pre-start cancellation/failure and releases its exact ownership automatically. Start a new equipment session before retrying. Preserve the failure log.

### A prior run remains unresolved at `ACQUIRE`

1. Confirm that its runner is no longer active.
2. Open **Analysis Forge**.
3. Select **Show / hide input overrides and recovery tools**.
4. Select **Finalize Interrupted Run** and provide the requested operator review.

Finalization is refused when ownership or evidence cannot be resolved safely. Do not delete the runtime lock, owner or lease files and do not terminate an unrelated process merely because Windows reused a process number.

### A connector says the device is owned

Use **Manage running connectors…**, choose the exact process and select **Stop selected**. Wait for a graceful stop. For externally owned publishers, close the actual publisher only after confirming no other recording uses it. One physical serial/BLE/API endpoint may not support multiple owners.

### The Forge sees two XDF files

Choose the folder containing the intended run, inspect **Review Input Inventory**, then use **Choose XDF** under the recovery controls to bind the correct file. Do not combine the XDF from one run with events or channel maps from another.

### Required QC reports dirty EEG or 60 Hz contamination

Treat that as a data-quality result, not a software failure. The Forge should still expose dataset-compatible descriptive/exploratory modules when the required inputs exist. Downstream reports must retain the contamination warning; no workflow control can manufacture clean data.

### A result is `NOT_ESTIMABLE`

Open **Warnings and limitations**, the individual report and receipt. Common causes include insufficient duration, absent event coverage, a missing modality or an unsupported denominator. `NOT_ESTIMABLE` should not be changed to zero, null or PASS.

### A plan or lock is stale

Create a new immutable revision bound to the correct inputs. Historical locks, plans and reports should remain preserved. Do not hand-edit paths, hashes or status fields.

## 18. End-of-session checklist

Before closing the application:

1. Confirm the protocol runner has reached a terminal state.
2. Stop and save LabRecorder.
3. Stop PRAYCG-owned connector processes and close external publishers only when safe.
4. Finish or cancel active required QC, governed analysis or Research Exchange work.
5. Confirm that the run folder, workspace and reports open correctly.
6. Preserve the raw recording and evidence. Create a new session for the next acquisition rather than reusing the old UUID.

For installation, dependency repair and startup troubleshooting, use the release's current installation guide. For product-specific experimental route constraints, use `app/docs/HARDWARE_ROUTES_ALPHA_10_2_1.md` in the installed release.
