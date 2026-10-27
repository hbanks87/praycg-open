# Alpha 10.3.14 installation and Muse S Athena workflow

This release adds a separate four-channel Muse S Athena Zuna study. Do not use the original Zuna protocol 1.0 as a workaround for a four-channel headset: the older protocols and their analysis contracts are not interchangeable with this study. Software checks do not establish physical compatibility or a useful model benefit.

## Install beside the previous release

1. Stop acquisition and close the old Control Center when safe. Keep study folders and earlier releases.
2. Extract the entire Alpha 10.3.14 ZIP into a new writable local folder. Do not merge releases or run inside the ZIP. Keep the six top-level files and `app` folder together.
3. Use native Windows Python 3.11 with Tcl/Tk support. Run **INSTALL.bat**, then **START_PRAYCG.bat**. Select **Use Bundled Paths** and verify separate PsychoPy and LabRecorder locations.
4. Zuna remains optional. Run **INSTALL_ZUNA.bat** to prepare this release's isolated model environment. The installer can reuse the verified shared model cache at `C:\PRAYCG\shared\Zuna`; it does not reuse an old release's Python environment or silently migrate study data. See [shared model options](INSTALL_AND_WORKFLOW_ALPHA_10_3_12.md).
5. `INSTALL_ZUNA.bat -CheckOnly` inspects the optional installation without installing anything. Core QC does not require Zuna. The archive does not include model weights, PsychoPy, LabRecorder or vendor applications.

The managed Athena route requires the pinned **BrainFlow 5.23.0** Hardware Connectors environment. Normal full installation includes it; if using a minimal installation or an older connector environment, run `INSTALL.bat -Mode hardware` for this release. Do not silently substitute an older Muse implementation or a global Python environment.

No installation, hardware acquisition, user recording, external upload or full Zuna model inference was performed as part of this software build. The build-validation record states the actual automated tests and skips.

## Choose the Muse study

Select **Muse S Athena EEG Reconstruction Validation** in the Protocol Atlas. It has a separate protocol identifier, `ATLAS_ZUNA_MUSE_S_ATHENA_VALIDATION`, version 1.0. No external stimulus package is needed: the runner generates the rest instructions and cues.

The supported route is the managed BrainFlow **muse_s_athena** profile with **p1041** configuration. The analyzed native EEG channels are **TP9, AF7, AF8 and TP10**, at **256 Hz** in microvolts. The operator reviews the declared physical **FPz reference**, actual stream and channel order before timed content. Template electrode coordinates are approximate, not a digitized individual head model.

This route does not use an auxiliary electrode, fNIRS or ALS. Do not select the sixteen-channel PRAYCG cap map, invent missing electrodes, rename an unrelated LSL outlet to appear compatible, or add an optical sensor merely to satisfy another protocol. The existing hardware-profile eligibility rules remain in force. Athena is admitted as **EXPERIMENTAL_EVALUATION**, not hardware-validated or **HUMAN_CONNECTED_APPROVED**; this new protocol does not promote its hardware evidence.

## Record the task

1. Create and lock the appropriate Muse hardware profile, start its managed stream, and complete the usual equipment checks. Preserve warnings and their reasons.
2. Confirm the session setup and arm through the normal workflow. Review the native-channel declaration before fullscreen presentation. Cancel if the observed stream, channels, units or reference do not match.
3. Start LabRecorder and select the **Muse EEG stream and StasisMarkers**. For the first validation attempt, record one EEG outlet rather than also selecting an OpenBCI EEG outlet: the generic QC handoff still uses a governed single-EEG selection. Additional diagnostic streams do not become extra EEG electrodes. PRAYCG does not operate LabRecorder recording controls for you.
4. Follow the generated eyes-open/eyes-closed instructions. Timed content is two minutes of eyes-open settling/acclimation (not model training) followed by eight one-minute blocks, totaling ten minutes. Setup, tone checks and completion instructions are additional.
5. Stop LabRecorder promptly after completion. Finalize the run and select its unchanged XDF. Preserve the run folder with the task contract, observed-block evidence and locked hardware profile.

There is no optical-timing verification in this Muse study. Software markers and timestamps must not be reported as photon timing, and Muse results must not inherit an OpenBCI/ALS timing declaration.

## Analyze the recorded Muse study

Prepare the run in Analysis Forge and run **Required QC** first. Then select **Zuna Muse S Athena Reconstruction — Experimental** and follow the normal analysis-plan workflow. Do not run the sixteen-channel Zuna worker on the Muse recording or edit old contracts to pass its checks.

Recording-wide effective rate is descriptive and does not by itself exclude this module from the plan. The worker still verifies the exact nominal 256 Hz native stream and each scored piece's rate, continuity and coverage. A planning pass does not certify those later checks.

The Muse analysis uses four fixed leave-one-channel-out comparisons. In each comparison, Zuna receives three measured channels and predicts the fourth. Each native channel is withheld once; all four results remain visible. A three-electrode spherical-spline estimate and a fixed-zero prediction provide comparison baselines. Held-out measured values do not supply model normalization or reference information.

Read absolute error in microvolts, normalized error, individual target/block results and coverage. A three-electrode interpolation baseline has sparse spatial support, so beating it alone does not establish accurate reconstruction. The zero comparator is intentionally simple; beating zero alone is also insufficient. Undefined metrics remain unavailable, not silently favorable.

This is an exploratory sparse-sensor feasibility study, not clean-signal recovery, a new dense measured montage, a clinical test, a live decoder or evidence of general benefit. Channels and windows from one recording are not independent participants. Keep all results, including unfavorable targets and interrupted attempts. Choose any future numerical success criteria and replication plan before reviewing those new results.

## Preserve and bundle the evidence

Keep original measured data separate from generated predictions. The module's reports and method/model provenance remain analysis artifacts; generated channels do not count as additional hardware electrodes. Use the existing research-bundle review to include the relevant run, protocol, analysis and reports. Private full telemetry requires explicit selection and privacy review. PRAYCG does not upload the bundle.

Muse report JSON and provenance JSON can contain private local paths and therefore require the bundle's private-data option. Readable HTML, metrics CSV and block summaries can be included in a public-oriented bundle only after human privacy review. The private preparation file and waveform arrays additionally require full-telemetry opt-in; selecting an analysis does not silently publish those files.

Reports can take longer to compute than the ten-minute recording. The four sparse folds add work; this release makes no full-run speed claim. Synthetic test predictors establish software behavior, not actual Zuna performance.

## Keep the sixteen-channel study separate

The legacy, reviewed-montage and optional-optical protocols remain available. Their recorded identities are not rewritten. The [frozen sixteen-channel plan](ZUNA_NEXT_VALIDATION_PLAN_ALPHA_10_3_13.md), its JSON and original receipt are preserved byte-for-byte, but they bind the exact Alpha 10.3.13 runtime. Shared code changes in 10.3.14 mean this newer runtime is not that exact freeze.

For the already-frozen sixteen-channel study, use its exact Alpha 10.3.13 release or prospectively review and record a new version before collecting data. The machine-readable `config/zuna_next_validation_plan_context_v1_0.json` explicitly records this distinction. No replacement freeze was silently created, and the old plan does not enroll Muse runs.

## Credits and limitations

Hoyt Banks is credited for the PRAYCG study design and integration, not the upstream model or acquisition libraries. Zuna/Zyphra, BrainFlow, MNE and other dependencies keep their own authorship, licensing and notices. See [the upstream Zuna project](https://github.com/Zyphra/zuna), [BrainFlow board documentation](https://brainflow.readthedocs.io/en/stable/SupportedBoards.html), and the distribution's master citations and license notices. Citation is not endorsement or comprehensive license clearance.

No new physical Muse, Bluetooth transport, headset reference, electrode contact, display or participant validation is claimed. If the headset exposes a different contract, preserve the logs and stop that route rather than changing labels to force compatibility.
