# Alpha 10.4.0 installation and Muse Athena workflow

Alpha 10.4.0 builds on the completed 10.3.14 release. It adds compatibility requirements for all 91 packaged protocol definitions, 20 separately identified Athena adaptations, a first-connection check, descriptive four-channel analysis, and corrections to event selection and response timing. The original 71 protocol definitions retain their identities and declared scientific questions.

## Install in a new folder

1. Finish any active acquisition and close the previous Control Center. Keep earlier releases and study folders.
2. Extract the complete 10.4.0 ZIP into a new writable local folder. Keep `app/` beside `INSTALL.bat`, `INSTALL_ZUNA.bat`, `START_PRAYCG.bat`, `README.md`, `CHANGELOG.md`, and `LICENSE.md`. Do not merge releases or run inside the ZIP.
3. Use native Windows Python 3.11 with Tcl/Tk. Run **INSTALL.bat**, then **START_PRAYCG.bat**. Use **Use Bundled Paths** and verify the separate PsychoPy and LabRecorder paths.
4. The normal installation prepares separate Core, Live Monitor, and Hardware Connectors environments. The Athena route uses the pinned BrainFlow 5.23.0 connector environment. `INSTALL.bat -Mode hardware` prepares that component when needed; `INSTALL.bat -Mode monitor` prepares Live Monitor.
5. Zuna is optional. **INSTALL_ZUNA.bat** prepares this release's isolated environment and can reuse the verified shared model cache. **INSTALL_ZUNA.bat -CheckOnly** checks it without installing. See the [shared-cache guide](INSTALL_AND_WORKFLOW_ALPHA_10_3_12.md). Ordinary recording, QC, and the new descriptive module do not require Zuna.

Python, PsychoPy, LabRecorder, model weights, and vendor applications are not shipped inside the workbench archive. The workbench does not require the proprietary Muse application for the managed acquisition route. A clean-machine installation and actual headset acquisition have not been performed for this build; consult the build-validation record for the executed software checks.

## First connection and recording check

In Hardware, open **Muse Athena setup check…**. Charge and unplug the headset, power it on, and close other applications that may own its Bluetooth connection. Use the setup window's Bluetooth discovery to identify the exact headset. Start the reviewed managed **Muse S Athena / BrainFlow p1041** connector through the existing Hardware workflow, then discover and select its EEG outlet in the setup window.

The window binds evidence to the selected outlet and equipment session. Confirm that the chosen outlet belongs to the headset you intend to check. Start the setup markers, select the EEG and **PRAYCG_AthenaSetupMarkers** streams in LabRecorder, and start recording there. Run the bounded live observation, view that same outlet in Live Monitor, then stop and finalize LabRecorder. Reopen the saved XDF in the setup window and save the equipment-check report.

The checker evaluates declared channel identity, native rate and units, continuity, sample coverage, markers, and reopening of the recorded file. Live Monitor visibility is explicitly an operator observation. A result distinguishes observed, failed, not-run, and synthetic evidence. Changing the selected source invalidates earlier source-specific checks. The saved report records the equipment/run/source identity and the recording hash.

The managed Athena profile remains **experimental and bench-only**. The setup report does not automatically grant participant acquisition or certify contact quality, wireless latency, stimulus arrival, or scientific validity. No physical check was substituted with a software fixture. A separate review of actual equipment evidence is needed before changing the existing acquisition restriction.

## Select a protocol

The Protocol Atlas now shows an **Athena fit** column and separate task, measurement, and analysis statuses in the selected-protocol details. The preview assumes Athena EEG plus task markers. Session setup evaluates the actual selected hardware; extra signals must come from their real reviewed sources. The compatibility result is retained in the session's analysis-capability record.

Start with:

- **MIPDB-Derived Eyes-Closed Rest — PRAYCG Adaptation** for a descriptive baseline.
- **Meditation — Breath Counting vs Active Thinking — PRAYCG Adaptation** for the existing descriptive comparison.
- The new **IndividualRest — Athena EEG-only baseline** edition for its revised EEG-only resting question. The original calibration still requires its autonomic signals.
- **Muse S Athena EEG Reconstruction Validation** when testing the optional Zuna reconstruction workflow.
- Any of the 13 behavioral protocols with optional EEG. Their behavioral results remain distinct from EEG estimability.

PRAYCG3, PRAYCG4, and Semantic Meaning Gradient have separate Athena editions ending in `_ATHENA_V1`. The ten prospective sequences also have separate Athena editions, preserving each original order and independent reports. Choose the edition before preparing or assigning the study. Existing assignments and historical runs are not silently migrated.

Six ERP task adaptations have separate exploratory Athena editions. These permit the declared task and recorded-site exploration while leaving the original regional ERP endpoints unavailable. The original ERP, motor-imagery, SSVEP, inner-speech, autonomic, and dyadic definitions retain their actual electrode and sensor requirements. A new title or generated channel does not supply missing measurements.

## Record and monitor

The managed EEG outlet contains **TP9, AF7, AF8, TP10**, nominally **256 Hz**, in **microvolts**. The native physical reference is manufacturer-described FPz. AUX, optical, and motion outlets remain separate; they are not extra measured EEG electrodes or automatic cardiac, respiratory, or hemoglobin measurements.

Complete the existing profile/session setup and locking workflow. The native runner's LabRecorder screen names the selected EEG outlet, even if its optional watchdog is disabled. Task recordings require their normal **StasisMarkers** stream; the setup-marker outlet is only for the equipment check. Review channel labels in Live Monitor and record the intended EEG outlet without adding an unrelated second EEG source to a single-source analysis.

For the new prospective Athena editions, software markers remain available without requiring an ALS overlay. They make no physical optical-arrival claim. Original prospective sequences still require their declared runner barcode events, and the frozen runner policy is checked before launch.

Finalize the run, stop/finalize LabRecorder, and preserve the original XDF and run folder. Old recordings are not rereferenced, repaired, or relabeled by upgrading the application.

## Analyze four measured channels

Prepare the saved run and complete Required QC in Analysis Forge. Add **Muse Athena — Four-channel descriptive EEG**, review and lock the plan, then run it. This module reads the raw XDF with the native reference retained. It does not consume the generic common-average-reference derivative.

The versioned operational recipe uses independent continuous-piece 1–40 Hz filtering, four-second nonoverlapping windows, explicit edge guards, and deterministic amplitude, step, flatness, and neighboring-artifact exclusions. The minimum usable duration is 40 seconds with at least 50% usable coverage for a reported interval. These are disclosed engineering thresholds, not validated physiological artifact criteria. The report includes the exact policy and hash, rejected windows, measured-site theta/alpha/beta power, and data limitations. Native/prospective phase names remain explicit; phase-scrambled data are not silently mapped to the original control phase.

Unusable EEG yields **NOT_ESTIMABLE** and reasons, rather than a zero-valued physiological outcome. Behavioral and event records remain untouched. Results describe the four recorded sensors; they do not establish regional scalp effects, anatomical connectivity, clinical status, mental states, or causal mechanisms.

For reconstruction, select **Zuna Muse S Athena Reconstruction — Experimental** with **Muse S Athena EEG Reconstruction Validation**. Its separate native-input, three-input/one-hidden-target reference rules are unchanged. Generated estimates remain distinct from measured EEG. The three older reconstruction protocols require 16 measured EEG channels and are not Muse alternatives. See the [10.3.14 Muse reconstruction guide](INSTALL_AND_WORKFLOW_ALPHA_10_3_14.md) for the retained study design and comparisons.

## Event selection and multiperson studies

Motor decoding now uses explicit task-mode/effector context and retained per-class trial requirements; execution and imagery must not be pooled to reach a count threshold. N2pc selection can use target side, but Athena still lacks the original posterior sites. SVNA correction updates both ranking and response timestamps.

Full dyadic hyperscanning requires separately identified EEG, cardiac, and respiratory sources for participants A and B, with device/source ownership checked. The two-EEG requirement is not applied to caregiver/child behavioral protocols. An event-log structural check is labeled separately from a physiological estimator, and a missing analysis remains unavailable.

## Release evidence and limits

The source build record and packaged checksums identify the tested files. Automated tests use synthetic inputs and controlled device/XDF seams; no real headset recording, manual on-device validation, fresh full installation, or Zuna model inference is claimed. The retained sixteen-channel frozen plan still belongs to its exact Alpha 10.3.13 runtime.

See [the 12-item implementation record](ATHENA_UPDATE_TRACEABILITY_ALPHA_10_4_0.md) and [protocol compatibility details](ATHENA_PROTOCOL_COMPATIBILITY_ALPHA_10_4_0.md).
