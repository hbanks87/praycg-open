# Alpha 10.3.0 — Installation and validation workflow

This guide covers the new optional Zuna path. It supplements—not replaces—the [complete operator workflow](WORKFLOW_ALPHA_10_2_1.md), [general installation guide](INSTALLATION_ALPHA_10_2_1.md) and [hardware-route guide](HARDWARE_ROUTES_ALPHA_10_2_1.md).

The scope is one optional model installation, one Forge module, one ten-minute protocol and one automatic comparison report. Alpha 10.2.3's existing acquisition, analysis, assisted-authoring and hardware features remain available. Existing studies and older reports are not silently rewritten.

## 1. Install beside your current release

1. Finish or stop active recordings, finalize unresolved acquisition as appropriate, and close the older Control Center.
2. Back up your workspace, recordings and analysis outputs. Keep data separate from software folders.
3. Extract the whole Alpha 10.3.0 ZIP into a new writable local folder. Keep the five top-level files with the `app` folder. Do not merge releases.
4. Use native Windows Python 3.11 with Tcl/Tk support. Run `INSTALL.bat`, then `START_PRAYCG.bat`.
5. In Settings, choose **Use Bundled Paths** for this release. Verify the separate PsychoPy and LabRecorder locations. Open the intended workspace and inspect the selected study/session before doing anything with hardware.

The default full installation remains Core + Live Monitor + Hardware Connectors. Zuna is not part of that default. Missing Zuna does not prevent existing modules or this protocol's acquisition from running.

### Optional Zuna installation

From a terminal opened in the extracted release folder, run:

```text
INSTALL.bat -Mode zuna
```

The explicit command installs the pinned Zuna 1.1.6 wheel, its Python runtime packages and the pinned ZUNA1.1 model. Model weights alone are 1,528,504,816 bytes (approximately 1.53 GB); dependencies and working files require additional space. The installer requires at least 8 GB free disk space. Download time depends on your connection. Installation verifies file hashes rather than silently choosing the latest model.

The optional environment is `app/.zuna-env`; model files, installation receipt and retained package notices are under `app/.zuna-models/<pinned revision>`. This is separate from Core, Live Monitor and hardware environments. Do not manually replace a weight file, update Zuna inside the environment or change its lock to clear a verification failure.

Read [the upstream rights/provenance boundary](ZUNA_METHODS_ALPHA_10_3_0.md#upstream-identity-and-rights) before installing. Upstream software and weights are downloaded from their publishers; they are not bundled in PRAYCG's release ZIP.

For a non-installing local check:

```text
INSTALL.bat -Mode zuna -CheckOnly
```

A successful installation check establishes files/imports/identity, not reconstruction accuracy. A missing or changed model stops its module with an explanation. It does not trigger a download during analysis or silently substitute the conventional baseline.

CPU is the supported default; inference uses two compute threads. Run one model analysis at a time and avoid concurrent acquisition on the same laptop. Keep normal ventilation available. No ten-minute analysis-time promise is made, and no GPU performance or compatibility is claimed.

Bounded same-machine smoke measurements were approximately 43–61 seconds for five seconds of EEG using two CPU threads. A simple full-run projection is roughly 1.5–2 hours for 600 seconds, plus startup and output work; this is an estimate, not a completed full-length performance test or a promise for your computer. The managed worker reports progress and can be cancelled; retain the run and use a new analysis attempt when restarting.

The shared Atlas runner changed in this release. A previously installed user-authored protocol can therefore appear quarantined until its compatibility is explicitly reviewed and accepted through the existing extension workflow. Do not edit its engine hashes, automatically unquarantine it, or overwrite the user-protocol store. Historical protocol versions and run evidence remain preserved.

## 2. Prepare the first validation recording

Choose **AI-Assisted EEG Reconstruction and Signal Preservation** in the Protocol Atlas. Its stable identifier is `ATLAS_AI_EEG_RECONSTRUCTION_VALIDATION`, version 1.0. It generates its own instructions, fixation and tone cues; it needs no downloaded stimulus media.

This first benchmark requires one 16-channel EEG stream and StasisMarkers. It does not require ALS, Vernier, Polar, a second board or live AI. Other sensors can remain recorded when properly configured, but they are not model inputs and do not make missing EEG eligible.

Use the following actual electrode-to-channel wiring, not merely a renamed list:

| Recorded channel | Electrode | Recorded channel | Electrode |
| --- | --- | --- | --- |
| 1 | Fp1 | 9 | F7 |
| 2 | Fp2 | 10 | F8 |
| 3 | C3 | 11 | F3 |
| 4 | C4 | 12 | F4 |
| 5 | P7 | 13 | T7 |
| 6 | P8 | 14 | T8 |
| 7 | O1 | 15 | P3 |
| 8 | O2 | 16 | P4 |

The data must be in microvolts, using an external physical acquisition reference. **Do not use an EEG stream that has already been digitally average-referenced across all sixteen electrodes.** That would mix the held-out target signals into model inputs and invalidate the comparison. The Forge worker creates its own retained-channel-only reference from the raw recording.

Check your physical wiring, publisher settings, reference connection and units. Do not guess from stream labels. If your cap uses a different map or a different reference arrangement, do not confirm this preset; a reviewed new profile is needed. The worker uses standard-1020 template coordinates, not individually digitized electrode locations.

Record all sixteen electrodes. F3, F4, P3 and P4 are withheld by analysis only; do not disconnect them or remove them from LabRecorder. They are the measured comparison targets.

## 3. Record the ten-minute task

1. Follow the normal workspace, protocol, hardware-profile and equipment-check workflow.
2. Review the protocol-dependent configuration, confirm the session, lock the hardware and arm. Use bench mode only for an explicitly labeled non-participant rehearsal; it does not turn absent EEG into analyzable data.
3. Launch the locked runner. At the LabRecorder hold, update its stream list and select the intended EEG and **StasisMarkers** outlets. Start recording, then continue the runner.
4. The first screen lists the exact map, units and reference. Press **R** only after personally checking all three. **Escape** cancels. This explicit confirmation is preserved as evidence; the program does not claim to measure the wiring itself.
5. Listen to both practice tones at a comfortable volume. **High tone: eyes open. Low tone: eyes closed.** Confirm each cue only when it is audible. Escape if the sound does not work.
6. Remain seated, awake and comfortably still. The timed content is:

   - 120 seconds eyes-open calibration;
   - eight 60-second blocks, four eyes open and four eyes closed, in the session's frozen complementary order.
7. A tone starts every interval. Adjacent blocks can have the same eye state; keep that state when the same tone repeats. Open your eyes at the final high tone, finish the completion screen, then stop LabRecorder promptly.

The 600 seconds refers to scheduled content. Instructions, operator decisions, display-refresh overhead and completion are additional. Tone-play requests are marked in the software clock; acoustic delay and eye-state compliance are not measured.

Escape stops the runner and leaves an incomplete run. Completed observed intervals remain preserved, but an interrupted block is not invented or assigned its planned end time. Finalize the interrupted acquisition through the normal workflow.

## 4. Prepare the run and run Analysis Forge

1. Confirm that the intended run folder and XDF are selected. Preserve the original XDF, event logs and session evidence.
2. Use **Prepare Run for Analysis** and inspect the selected protocol analysis window. Do not include arbitrary recorder overrun as protocol time.
3. Open Analysis Forge and run **Run Required QC**. Review run integrity, event timing, EEG signal quality and line noise.
4. Find **Zuna EEG Reconstruction — Experimental** in the module registry and add it to the plan. Its stable module ID is `zuna_eeg_reconstruction_v1_0`.
5. Lock the plan and run or resume it. Required QC dependencies run first where needed. Do not add the ordinary all-channel common-average preprocessing derivative as a substitute for the model's dedicated preparation.
6. Inspect the persistent results entry and open its comparison report. Keep the technical receipt and provenance alongside the readable report.

The model module reads the raw selected EEG branch, verifies the reviewed mapping contract and checks that QC belongs to the selected XDF. It compares Zuna and spherical splines on identical held-out targets. The report retains the original quality cautions; it does not relabel contaminated data as clean.

A short bench recording without EEG cannot supply sixteen measured targets. Missing evidence must remain missing. A failure or not-estimable result includes a reason; no successful model run is claimed merely because a report file exists.

## 5. Read the comparison

- **RMSE, in microvolts:** typical error size on the processed measured target. Lower is better.
- **NMSE:** mean squared error divided by measured target variance. Lower is better. Zero would be a perfect numerical match; a constant target makes the denominator undefined, so the result is null rather than zero.
- **Correlation:** similarity of waveform shape. High correlation can coexist with incorrect amplitude or offset.
- **Zuna minus spline NMSE:** a negative value favors Zuna on this comparison; a positive value favors the conventional method.
- **Eye-state spectral comparison:** descriptive measured-versus-reconstructed differences, only where usable observed block boundaries support them.

With all eight observed test blocks available, the prospective scoring mask excludes calibration and five seconds at each block boundary. Without the complete ledger, useful whole-window reconstruction errors may still be reported as exploratory, while the prospective endpoint stays explicitly **NOT_ESTIMABLE**. Do not present the fallback as completion of the planned validation.

The conventional method is allowed to win. One recording's thousands of samples are not thousands of independent participants. Shared artifacts can make predictions agree with contaminated EEG; lower error is not proof of neural truth. See the [full method definition](ZUNA_METHODS_ALPHA_10_3_0.md).

## 6. Bundle and retain the result

The module automatically writes its HTML/JSON report, metrics table, provenance and generated-mask description into its Forge output folder. Include that analysis folder through the existing Research Bundle workflow; the comparison report and provenance travel with it.

The separate reconstruction array archive holds prepared retained measurements, withheld measured targets, both methods' predictions, masks and timestamp/sample mapping. Include waveform arrays only through the explicit **private full-telemetry** option. Public-oriented or derived-results packages must not silently acquire those arrays. Neither model weights nor the model environment belong in a study bundle.

Review every sharing decision. Even summary outputs and metadata can carry private study information. A private AI-review package is not automatically de-identified, encrypted or authorized for upload. PRAYCG does not contact an AI provider or publish the bundle.

## Troubleshooting

| Message or symptom | What to check |
| --- | --- |
| Optional Zuna environment/model unavailable | Run the explicit installation or local check command above. Existing Forge modules should remain usable. |
| Model or source fingerprint mismatch | Preserve the error and reinstall the pinned optional component. Do not edit hashes. |
| Mapping/reference contract missing | Select the correct validation run folder and its saved evidence. Do not manufacture a retrospective operator declaration. |
| Channel count, units or mapping conflict | Check the actual recorded stream and confirmed cap wiring. This first release is not a universal-montage benchmark. |
| QC belongs to a different XDF | Reselect the intended run, prepare it and rerun Required QC for that recording. |
| Gaps, nonfinite samples or reversed timestamps | Inspect Required QC. The benchmark does not silently fill acquisition gaps. Other descriptive QC remains useful. |
| No eye-state comparison | Inspect the observed-block ledger and run completeness. Planned times do not replace missing actual boundary markers. |
| Slow analysis | Ten minutes is the recording duration, not a speed guarantee. CPU inference is bounded to two threads; avoid parallel model jobs. |
| Earlier comparison already exists | Preserve it. Use the Forge's new attempt/output path for a rerun instead of overwriting historical results. |

For general session recovery, recipe editing, AI returns, replay and bundle import, use the [complete operator workflow](WORKFLOW_ALPHA_10_2_1.md). Keep the raw recording and logs when seeking help.
