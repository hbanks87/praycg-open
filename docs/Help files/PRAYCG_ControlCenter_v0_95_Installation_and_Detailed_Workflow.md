# PRAYCG Control Center v0.95

## Installation and Detailed Workflow Guide

**Approved author:** Hoyt Banks  
**Contact:** hoytbanks@gmail.com  
**GitHub:** https://github.com/hbanks87/praycg-open  
**OSF:** https://osf.io/8n75v/overview?view_only=928f1fa1974b40e89252101d0ba356d3

## What this guide covers

This guide explains how to install PRAYCG Control Center v0.95, prepare a stimulus, start acquisition, access and lock the additional protocol modules, run a session, organize the recorded run, execute standard analysis, and access the separate exploratory tools.

The Control Center is an organizer and launcher. PsychoPy runs the experiment, LabRecorder records LSL streams, BrainFlow communicates with OpenBCI, MediaPrep creates stimulus derivatives, and the Master Comprehensive Suite performs analysis. A successful launch or software check does not certify data quality or validate a scientific endpoint.

## Current protocol choices

The normal **Runner / PsychoPy** protocol library contains three selectable modules:

| Protocol | Purpose | Required video inputs | Fixed branch order |
|---|---|---|---|
| PRAYCG3 v3.0 | Original three-prong protocol | PhaseScrambled Control, Target, Override | Control → Target → Contextual Override |
| PRAYCG4 v4.0 | Four-branch protocol with structural control | PhaseScrambled Control, ShotOrderScramble, Target, Override | Control → ShotOrder → Target → Contextual Override |
| Semantic Meaning Gradient v1.0 | Conditional semantic-gradient protocol | Semantic-Zero, High-Meaning Target, Arithmetic Override | Semantic-Zero → High-Meaning Target → Arithmetic Override |

All three retain Baseline 1, a washout and report after every branch, Baseline 2/final reflection, and the final report. The selected branch order is fixed by its versioned manifest.

Ten additional counterbalanced PRAYCG3/PRAYCG4 candidates are available through the **Prospective Study Console**. They are study-preparation templates, not drop-in replacements for the three validated library entries. See “Accessing prospective protocol variants” below.

## Part 1 — Before installation

## 1. Computer and external software

The public package is intended for a 64-bit Windows acquisition computer.

Install or make available:

1. **Python 3.11.** This is the preferred environment for the included installer and scripts.
2. **PsychoPy.** The recommended runner mode uses PsychoPy's bundled Python and opens the locked runner in PsychoPy Coder.
3. **LabRecorder.** This records the LSL streams into XDF.
4. **OpenBCI/USB drivers** appropriate for the board and dongle, if using OpenBCI acquisition.
5. Optional device support for Polar H10 and the Vernier respiration belt if those streams will be recorded.
6. FFmpeg/ffprobe is useful for stronger media validation, although MediaPrep also includes Python video dependencies.

PsychoPy, LabRecorder, OpenBCI drivers, and hardware are not bundled in the ZIP.

## 2. Hardware preparation

Before a real session, confirm the intended hardware path:

- OpenBCI EEG only; or
- OpenBCI EEG plus ALS/PT19; and optionally
- Polar H10 RR intervals; and/or
- Vernier respiration.

Only one application can own the OpenBCI serial port at a time. Close the OpenBCI GUI before starting a BrainFlow bridge.

If using the ALS/PT19 path, physically mount the sensor, confirm the correct AUX input, and plan to run both holder calibration and the screen-location pulse test on the actual display arrangement.

## Part 2 — Install Control Center v0.95

## 3. Extract the package

Use the current archive:

`PRAYCG_ControlCenter_v0_95_Public.zip`

1. Right-click the ZIP and choose **Extract All**.
2. Extract the complete folder to a normal writable location, preferably a short path such as:

   `C:\PRAYCG\PRAYCG_ControlCenter_v0_95_Public`

3. Do not launch anything from Windows ZIP Preview.
4. Do not separate the `control_center`, `tools`, `docs`, or configuration folders from the package root.

The published ZIP SHA-256 is:

`5B36631A0D0E35EED9AE1E00F2F053F0B3634D7FE4E9AB41599C40A2486A9C4C`

## 4. Install Python dependencies

From the extracted folder, double-click:

`INSTALL_PRAYCG_REQUIREMENTS_v0_95.bat`

The installer attempts to find Python 3.11 and installs the versioned dependency list, including NumPy, SciPy, pandas, matplotlib, OpenCV, MoviePy, pylsl, pyxdf, MNE, BrainFlow, device libraries, scene detection, and spreadsheet support.

Wait for the final success message. If installation fails:

1. Keep the visible error text.
2. Confirm that Python 3.11 is installed.
3. Confirm that the package was extracted and is not being run from inside the ZIP.
4. Run the installer again after correcting the reported package or permission problem.

## 5. Start the Control Center

Double-click:

`run_PRAYCG_ControlCenter_v0_95.bat`

The starter tries a local Python 3.11 installation, then the Windows `py` launcher, then `python` on PATH.

## 6. Configure paths on first launch

Open the **Settings** tab.

1. Click **Use Bundled Paths**. This rebases every included tool to the current extraction.
2. Click **Use Current Python** if the Python field is blank or points to an old installation.
3. Click **Auto-find ALL**.
4. Review the detected PsychoPy application, PsychoPy Coder/Python, and LabRecorder paths.
5. If needed, use **Find PsychoPy** or **Find LabRecorder**, or browse to the applications manually.
6. Confirm the main folders:

   - PRAYCG Home
   - Stimulus Root
   - Run Root
   - Analysis Root
   - Log Root
   - Protocol Module Library

7. Click **Save Settings**.

The normal bundled protocol-library path ends in:

`tools\ProtocolRunner_ModuleLibrary_v1_0`

If the protocol list is empty later, return to Settings, click **Use Bundled Paths**, save, then use **Rescan Library** on the Runner tab.

## 7. First-launch verification

Before preparing a study run:

1. Open **Dashboard** and click **Refresh Status**.
2. Confirm that Control Center reports v0.95 and that the configured roots are sensible.
3. Open **Runner / PsychoPy** and confirm that three protocol modules appear in the **Available protocol** list.
4. Open **Acquisition** and confirm the expected device buttons are visible.
5. Do not begin a real participant run until a short non-participant hardware and display dry run has succeeded.

## Part 3 — Prepare and register stimulus media

## 8. Add the master stimulus

Open **Stimulus Library**.

1. Click **Add Master Stimulus (.mp4)**.
2. Select the clean master MP4.
3. Enter a short, unique stimulus ID.
4. The Control Center copies it into the configured stimulus root under the selected ID.
5. Review the basic validation result and any duration, audio, or media warnings.
6. Select the new stimulus row so it becomes the active stimulus in the context bar.

Adding a file performs basic technical validation and hashing. It does not establish legal permission, scientific suitability, emotional safety, or stimulus equivalence.

## 9. Run MediaPrep

With the master stimulus selected:

1. Click **Launch MediaPrep** on the Stimulus Library tab or **2. Launch MediaPrep Suite** on Dashboard.
2. The Control Center passes the selected master MP4, the stimulus-specific MediaPrep output root, and the project name into MediaPrep.
3. Review the populated fields in MediaPrep.
4. Choose the intended preparation options and explicitly click Run inside MediaPrep.
5. Wait for successful completion rather than assuming the tool is finished because one intermediate video exists.
6. Inspect the generated Target, Override, PhaseScrambled Control, cue schedule, fingerprint/regressor files, manifests, and QC reports.

For the standard PRAYCG workflow:

- `target_video` should be the intact cue-embedded Target.
- `override_video` should satisfy the protocol's declared identity requirement relative to Target.
- `control_video` should be the intended PhaseScrambled control.
- the cue schedule should correspond to the actual rendered media.
- a locked anchor file is strongly preferred where anchor testing is planned.

## 10. Prepare the protocol-specific extra media

### PRAYCG3

Requires exactly one resolvable Control, Target, and Override video. ShotOrder and Semantic-Zero are not part of PRAYCG3.

### PRAYCG4

PRAYCG4 additionally requires a distinct ShotOrderScramble video.

1. On Dashboard click **2b. Generate Shot-Order Structural Control**, or on Stimulus Library click **Shot-Order Scramble Control**.
2. Generate ShotOrder from the cleaned master before cues are applied.
3. Apply the same cue schedule after shot reassembly so cue timing remains comparable.
4. Preserve the ShotOrder generation manifest.
5. Perform manual review of cut boundaries, audio treatment, frame count, duration, cue timing, and obvious rendering faults.

The Control Center looks for filenames containing `shot order` or `shotorder`. It only auto-prefills a file when exactly one candidate is found.

### Semantic Meaning Gradient

SMG requires a distinct Semantic-Zero video, Target, and Arithmetic Override.

1. Prepare and place the intended Semantic-Zero media inside the selected stimulus folder.
2. Use a clear filename containing `semantic_zero` or `semantic zero` so the Control Center can detect it.
3. Do not silently substitute PhaseScrambled media. Perceptual disorder can itself change salience, threat, puzzle demand, or spontaneous meaning-making.
4. Place the semantic-density coding JSON/CSV inside the stimulus folder if using that recommended sidecar.
5. Review the native SMG condition identities; canonical PRAYCG aliases are for compatibility and are not claims of construct equivalence.

## 11. Resolve ambiguous files

Auto-population follows a conservative rule:

- exactly one matching file: `FOUND` and eligible for prefill;
- no matching file: `MISSING`;
- multiple matching files: `AMBIGUOUS` and not automatically chosen.

If an input is ambiguous:

1. Remove or archive obsolete duplicates outside the active stimulus folder; or
2. Leave the context unresolved and select the intended file manually in the runner's **Media** tab.

Never rename a scientifically different file merely to make it auto-detect as the required condition.

## Part 4 — Access and launch the extra protocols

## 12. Open the protocol library

1. Select the intended prepared stimulus in **Stimulus Library**.
2. Open **Runner / PsychoPy**.
3. Locate **Protocol Module Library v1.0** at the top of the page.
4. Open the **Available protocol** dropdown.

The three entries should be:

- **PRAYCG3 — Original Three-Prong Protocol [PRAYCG3 v3.0]**
- **PRAYCG4 — ShotOrder Four-Branch Protocol [PRAYCG4 v4.0]**
- **Semantic Meaning Gradient — Three-State Protocol [SMG v1.0]**

PRAYCG3 is selected by default on a fresh configuration, but it is not launchable until locked.

## 13. Select and lock a protocol

1. Choose the desired entry from **Available protocol**.
2. Read the preview immediately below the controls.
3. Confirm:

   - protocol ID and version;
   - fixed branch order;
   - intended purpose;
   - scientific boundary;
   - manifest SHA-256;
   - runner SHA-256.

4. Click **Lock Selected Protocol**.
5. Confirm the displayed branch order in the confirmation message.
6. Verify that the lock status becomes green and says validation `PASS`.

Selecting is not the same as locking. The lock freezes the exact manifest, runner, identity, and branch order. Launch is disabled when no valid lock exists.

To change protocols later:

1. Finish or cancel the current preparation.
2. Click **Unlock**.
3. Select the new protocol.
4. Review its inputs and order.
5. Click **Lock Selected Protocol** again.

Do not change protocols during an active run.

## 14. Review auto-detected protocol inputs

The bottom of the Runner tab shows **Auto-detected Input Files for Selected Stimulus**.

Confirm that every media key required by the selected protocol says `FOUND`. Also review:

- cue schedule;
- locked versus draft/missing anchor;
- ShotOrder manifest for PRAYCG4;
- semantic-density sidecar for SMG.

Only unambiguous inputs declared by the selected module are passed into the runner. The runner independently validates them again.

## 15. Choose the runner-launch mode

Keep this selected unless a tested local procedure requires otherwise:

**Open locked protocol runner directly in PsychoPy Coder (recommended)**

Other modes are explicitly marked experimental or least recommended.

Click **Launch Locked Protocol Using Selected Mode**.

The Control Center opens the protocol-specific runner file in PsychoPy Coder. In PsychoPy Coder, click the normal green Run control to execute the script. The modular preflight GUI should then open.

If PsychoPy does not open:

1. Return to Settings.
2. Run **Auto-find ALL** or **Find PsychoPy**.
3. Confirm the PsychoPy Python/Coder path.
4. Save settings.
5. Rescan and relock if the lock is reported as stale.

## 16. Complete the runner preflight GUI

The runner GUI has four tabs: **Run**, **Media**, **EEG / Display**, and **Watchdog**.

### Run tab

Review or enter:

- Participant ID;
- Session ID;
- Run label;
- Baseline and washout durations;
- final reflection/Baseline 2 settings;
- pre-run display/audio calibration;
- per-branch confound reports;
- output/log directory.

Do not reuse participant/session/run identifiers accidentally.

### Media tab

Verify every protocol-specific media path. Also review:

- cue schedule JSON;
- locked anchor JSON/CSV;
- ShotOrder generation manifest for PRAYCG4;
- semantic-density sidecar for SMG;
- expected override sum if required.

Use **Auto-detect LOCKED anchor from cue folder** when applicable. A DRAFT or ESTIMATED anchor is not equivalent to a locked anchor with exact rendered times.

### EEG / Display tab

Review:

- fixed channel-map selection;
- whether the channel map was physically confirmed or photographed;
- screen index and fullscreen setting;
- movie safe-fit behavior;
- ALS placement/calibration profile;
- ALS barcode position, size, margin, and pulse timing.

Do not claim ROI-specific results from an unconfirmed channel map.

### Watchdog tab

Confirm the expected live EEG stream name and rate. The usual EEG stream is `obci_eeg1`. Start the BrainFlow stream before pressing Run in the runner GUI.

Click **Validate Inputs**. Correct every error. Then click **Run PRAYCG3**, **Run PRAYCG4**, or **Run SMG**, according to the locked protocol.

## Part 5 — Acquisition and live-session workflow

## 17. Start physiological streams

Open **Acquisition** in Control Center.

Start only the streams required by the session:

1. **Start Polar H10 RR → LSL**, if used.
2. **Start Vernier Respiration USB → LSL**, if used. USB is preferred before BLE unless the tested setup requires BLE.
3. Start one OpenBCI path:

   - **Start BrainFlow EEG Only**; or
   - **Start BrainFlow EEG + ALS**.

4. Choose and confirm the correct COM port when requested.
5. Click **Check Visible LSL Streams**.
6. Confirm the expected stream names, types, channel counts, and sample rates.

Do not start both BrainFlow bridges for the same board.

## 18. Run acquisition checks

Recommended non-destructive checks include:

### Signal Quality / Contact Index 0–100

Use this as a practical signal/contact heuristic. It is not true Cyton impedance and is not a medical measurement.

### ALS Holder Calibration Mode

Use this to establish the intended physical holder and display relationship and save a placement/profile record.

### ALS Screen Pulse Barcode Test

Run the long/short black-and-white pulse at the actual intended screen location. Confirm that the ALS/PT19 channel visibly responds.

### Optional 30-Second Acquisition Validation

Run this after EEG and ALS streams are active. It checks effective rate, timestamp behavior, missingness, flat/noisy/saturation-review indicators, and ALS pulse visibility. It records the display geometry, barcode rectangle, pulse schedule, and holder-profile hash when available.

This report is separate from runner arming. `PASS` means the declared quick engineering checks passed; it does not guarantee an artifact-free or scientifically valid session.

## 19. Open LabRecorder—but do not start recording yet

Click **Open LabRecorder** in Acquisition or Dashboard. Leave it open and ready.

Do not click LabRecorder Start before the runner creates the `StasisMarkers` outlet. Starting too early can cause the marker stream to be absent from the XDF.

## 20. Start the locked protocol runner

After completing the runner GUI and clicking its Run button:

1. The runner validates media, protocol hashes, anchor/channel-map information, output writability, and live EEG flow.
2. The runner creates the `StasisMarkers` LSL outlet.
3. A normal-sized **LSL preflight hold** window appears.
4. During this hold, switch to LabRecorder.
5. Click **Update** in LabRecorder.
6. Confirm that `StasisMarkers` is visible alongside EEG and every optional physiological stream.
7. Select the streams that must be recorded.
8. Set the XDF filename and destination under the intended run folder.
9. Click **Start** in LabRecorder.
10. Return to the runner's preflight window.
11. Right-click only after LabRecorder is actively recording `StasisMarkers`.

The runner then enters fullscreen mode and begins the protocol.

## 21. During the session

- Follow the participant-facing instructions exactly.
- Do not alter media, protocol, barcode, display, or channel settings during the run.
- Watch the Control Center process rows and bridge logs without covering or disturbing the participant display.
- Avoid opening the OpenBCI GUI while BrainFlow owns the COM port.
- If an emergency or unavoidable abort occurs, use the runner's supported exit path. The runner preserves an `INCOMPLETE` state and partial logs.
- Do not describe an aborted or incomplete run as complete simply because an XDF exists.

## 22. Finish the session

1. Allow Baseline 2/final reflection and the final report to finish.
2. Confirm the runner reaches its completed state.
3. Stop LabRecorder and verify that the XDF was written.
4. Stop the acquisition bridges normally.
5. Review their final PASS/WARN/FAIL QC outputs and stop reasons.
6. Preserve the run configuration, event JSON/CSV, lifecycle manifest, channel-map record, media/anchor hashes, self-reports, and XDF together.

Use the red per-tool **Close** button only after considering whether that tool is still writing data. **More → Force close** is for an unresponsive process and may leave outputs incomplete.

## Part 6 — Register and analyze a completed run

## 23. Select the run folder

Open **Analysis**.

1. Click **Select Run Folder**.
2. Choose the folder containing the completed run's XDF and sidecars.
3. Review the resolved run information.
4. If an item is ambiguous, use:

   - **Choose XDF**;
   - **Choose Event Log**;
   - **Choose Channel Map**.

5. Confirm that the selected run matches the intended stimulus and protocol.

The Control Center does not select the newest file merely because it is newest.

## 24. Run the canonical Master Suite analysis

Click **1. Open Master Suite**.

The Control Center supplies available XDF, event log, channel map, media, cues, anchors, fingerprints, output root, and context provenance. Review all populated fields, then explicitly click Run inside the Master Suite.

This first analysis produces the canonical v1.6.0 core output and `PRAYCG_AnalysisFrame_v1_6_0`. It establishes segmentation, QC, availability, and the foundation required by downstream modules.

If primary eligibility fails, review the reason. Exploratory files may still be produced, but the failed gate must not be ignored.

## 25. Refresh or select the canonical core output

After Master Suite finishes:

1. Return to Analysis.
2. Click **Refresh Resolution**.
3. Confirm that the Core path is `RESOLVED` and belongs to the active run.
4. If needed, use **Select Core Output** and choose the folder containing:

   `tables\praycg_analysis_frame_v1_6_0.csv`

## 26. Run the full chained analysis

Click **2. Run Full Chain** after the canonical core is resolved.

The distinction is:

- **Open Master Suite** creates the canonical core analysis frame and base QC/segmentation outputs.
- **Run Full Chain** starts the dependency-aware downstream analysis and records module applicability, failures, missing inputs, exploratory status, exact artifacts, and hashes.

The chain does not replace the core and should not be launched on an arbitrary raw-run folder.

## 27. Run targeted analysis tools

The standard Analysis panel also provides:

- **HOC-R** for supported high-order/ShotOrder contrasts;
- **Confound Expansion** for HOC-R, OSA, OHC, AAM, RespDualPath and related checks;
- **ALS Barcode** for timing-pattern review;
- **Visualizer** for synchronized timelines and diagnostic review;
- **Interpreter** for status-aware technical, research, and public-safe reporting.

Chain, HOC-R, and confound tools require a compatible canonical core. Visualizer and Interpreter should use the preferred compatible core or chain output shown by Active Research Context.

## 28. Interpret module statuses correctly

Do not collapse these states into “negative” or “positive” findings:

- `PASS`: the module completed under its declared computational conditions;
- `FAIL_PRIMARY_GATE`: the run failed a required primary eligibility condition;
- `NOT_GRADABLE_MISSING_INPUT`: a required measurement was absent;
- `NOT_APPLICABLE_PROTOCOL`: the module does not apply to this protocol/branch set;
- `EXPLORATORY_ONLY`: output is available but not a primary or validated endpoint;
- `SOFTWARE_ERROR`: the module failed technically.

A software PASS is not proof of the underlying scientific theory.

## Part 7 — Access exploratory analyses

The bottom of the Analysis tab contains **Exploratory Analysis — isolated from primary conclusions**.

## 29. CAI/SID v0.2

1. Select and resolve the run folder and compatible analysis folder.
2. Click **1. CAI Readiness Preflight**.
3. Review `PASS`, `CAUTION`, or `INELIGIBLE` and every stated reason.
4. If not ineligible, click **2. CAI/SID v0.2**.
5. Review branch summaries, contrasts, warnings, validation, and readiness reports.

CAI/SID is exploratory and does not affect Master Suite eligibility.

## 30. Continuous Autonomic / RespDualPath

With a run selected, click **Continuous Autonomic / RespDualPath**. Confirm the cardiac and respiration sources before running. Interpolated HR is for the declared grid; rolling HRV must remain derived from retained beat events.

## 31. Micro Handoff v0.1

With a run selected, click **Micro Handoff v0.1**.

The Control Center passes:

- selected run folder;
- exact XDF when resolved;
- preferred analysis folder;
- run-specific exploratory output folder.

In the Micro Handoff GUI, review the XDF, segment source, output path, readiness result, and claim boundary before running.

Micro Handoff is an exploratory temporal-gamma/theta coordination candidate. It is not a direct measure, probability, diagnosis, validated consciousness-density estimate, or consciousness RPM gauge.

## 32. Accessing prospective protocol variants

The counterbalanced variants are not in the normal Runner dropdown because they are separately versioned study-preparation candidates.

To inspect them:

1. Open **Analysis**.
2. In **Exploratory Analysis**, click **Prospective Study Console**.
3. Enter a template Participant ID such as `P001`.
4. Enter a template Stimulus ID such as `S001`.
5. Enter `PRAYCG3` or `PRAYCG4` in the Protocol field.
6. Click **Show assigned sequence**.
7. Review the assigned immutable sequence ID and branch order.
8. Click **Open assigned runner** only for review/development.

The console also includes:

- Regenerate protocol catalog;
- Template hash freeze;
- Synthetic blinded dry-run;
- Illustrative sample simulation;
- Promotion audit;
- Open OSF draft.

These tools do not make the template collection-ready. Before using a prospective variant with human data, replace every placeholder, freeze real media/anchors/configuration, run real-hardware acceptance and blinded feasibility, determine variance and sample-size inputs, obtain required ethics/consent approval, and register the final protocol on OSF.

## Part 8 — Troubleshooting

## 33. A button appears to do nothing

1. Look at **Dashboard → Running Tools**.
2. Open the tool's log.
3. Check whether it exited immediately.
4. In Settings, click **Use Bundled Paths** and **Use Current Python**.
5. Save settings and retry.

## 34. PsychoPy runner does not open

1. Run **Auto-find PsychoPy / LabRecorder** on the Runner tab.
2. Confirm PsychoPy Python/Coder in Settings.
3. Keep the recommended Coder mode selected.
4. Use **Open PsychoPy Coder Only** to verify PsychoPy independently.
5. Rescan and relock the protocol if the lock is invalid or stale.

## 35. Protocol missing from the dropdown

1. Open Settings.
2. Click **Use Bundled Paths**.
3. Confirm Protocol Module Library ends in `ProtocolRunner_ModuleLibrary_v1_0`.
4. Save.
5. Return to Runner / PsychoPy and click **Rescan Library**.
6. Read any library errors in the protocol preview.

## 36. Required protocol input is missing

- PRAYCG3: check Control, Target, Override, and cue schedule.
- PRAYCG4: also check ShotOrder video and preferably its generation manifest.
- SMG: check distinct Semantic-Zero, Target, Arithmetic Override, and preferably the semantic-density sidecar.

If multiple candidates exist, the Control Center leaves the field ambiguous. Select the intended file manually in the runner after verifying identity.

## 37. OpenBCI bridge exits immediately

1. Close OpenBCI GUI and any other serial-port owner.
2. Confirm board power and dongle connection.
3. Confirm the correct COM port.
4. Confirm BrainFlow and drivers were installed.
5. Open the bridge log from Running Tools.

## 38. LabRecorder does not show StasisMarkers

1. Do not proceed into fullscreen acquisition.
2. Confirm the runner is on its windowed LSL preflight hold.
3. Click Update in LabRecorder.
4. If the stream remains absent, stop the attempt, close the runner cleanly, inspect logs, and restart the sequence.

Do not right-click through the hold when the marker stream is missing.

## 39. Analysis buttons are disabled

Read the Analysis readiness preview. Common causes include:

- no selected run;
- ambiguous XDF/event log;
- no compatible canonical core;
- core provenance does not match the active run;
- no valid chain manifest;
- selected module is not applicable to the protocol.

Resolve the stated prerequisite instead of manually pointing the tool at a convenient but unrelated folder.

## 40. Safe operating and interpretation boundary

- Keep raw biosignals and identifiable self-reports private unless intentionally approved for release.
- Do not upload copyrighted stimulus media to the public GitHub repository.
- Preserve original raw XDFs and immutable hashes; perform analysis in separate output folders.
- Record every aborted, missing, or failed condition honestly.
- Do not reinterpret missing data as zero or a failed module as evidence against the hypothesis.
- Do not reinterpret an exploratory positive result as confirmation.
- Treat fixed-order legacy contrasts as descriptive because order, fatigue, habituation, and carryover remain possible.
- Use prospective counterbalancing, multiple participants/stimuli, declared exclusions/nulls, independent outcomes, and appropriate statistical models before stronger claims.

PRAYCG Control Center is exploratory research software. It is not a medical device, diagnostic system, safety-critical controller, or validated consciousness measurement system.
