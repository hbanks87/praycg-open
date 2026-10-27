# PRAYCG Alpha 10.3.11 — Installation and Zuna timing workflow

This is a focused Zuna preparation repair on Alpha 10.3.10. It does not change EEG amplitude-quality thresholds or declare a recording scientifically clean. The new route asks whether supported acquisition evidence explains irregular host-receipt timestamps without evidence of missing or disordered samples.

## Install into a new folder

1. Finish recording, stop LabRecorder and managed streams normally, then close the old Workbench. Preserve existing workspaces, recordings, incomplete attempts and reports.
2. Extract the complete ZIP into a **new writable folder**. Do not merge releases, run inside the archive, copy code into an active acquisition, or remove old ownership records.
3. With native Windows Python 3.11 and Tcl/Tk available, run **INSTALL.bat**. Normal setup prepares isolated Core, Live Monitor and Hardware Connectors environments. `INSTALL.bat -Mode minimal` prepares Core only.
4. Run **START_PRAYCG.bat** and confirm **Alpha 10.3.11**. Choose **Use Bundled Paths** and check external PsychoPy, LabRecorder and study paths. Existing workspace data stays separate; the upgrade does not rerun analysis automatically.
5. Zuna remains optional and separately installed. Use **INSTALL_ZUNA.bat** for its dependencies/model or `INSTALL_ZUNA.bat -CheckOnly` for a non-installing check. A new extracted folder does not automatically contain another release's optional environment. Ordinary Required QC does not require Zuna.

Python, PsychoPy, LabRecorder, model weights and installed environments are not shipped in this archive. Preserve prior releases and use reviewed new session/analysis revisions when saved code bindings no longer match; do not edit historical hashes to force compatibility.

## Continue an existing Zuna run

1. Open the existing workspace/session and Analysis Forge. Confirm the exact XDF and its bound run UUID. Select the correct run folder/XDF only if the saved selection is wrong.
2. Run **Required QC** if requested for the new analysis context, then inspect the input inventory. The exact runner evidence should provide the original validation contract, observed blocks and run/window records. Reviewed v2 contracts remain supported; never rename them to v1.
3. The supported timing route also uses the same-run OpenBCI bridge manifest and chunk diagnostics. The matching bridge must be stopped and its evidence finished; an active or changing log cannot authorize this route. Keep those original files in their run-evidence location. Do not substitute another recording's diagnostics or interpret a missing optional sidecar as permission to bypass timing checks.
4. If the original optional ALS declaration names a previous attempt's source, use **Review ALS stream binding** after QC and before locking a new plan or preparing a comparison. Give a named, reasoned review of the actual recorded source. This remains a separate immutable post-hoc correction; it does not alter the acquisition contract or automatically validate optical timing.
5. Review inputs and create a **new comparison preparation**. The selected recording, timing evidence, source policy and other inputs are fingerprinted. Old attempts/results remain preserved; incompatible checkpoints are not silently reused under the changed timing policy.
6. Inspect preparation outcomes before starting inference. A supported timing route may identify host-receipt jitter using validated counter/chunk evidence. It does not hide actual discontinuities or turn an estimated time grid into observed hardware sample timestamps. Unsupported or conflicting evidence remains a stated limitation or block.
7. Only explicitly start the prepared comparison when you are ready for model processing. Preparation alone is not inference. After completion, review errors versus interpolation, all evaluation blocks, original QC cautions, timing provenance and any optical correction separately. Include the actual report/provenance in a privacy-reviewed bundle; private waveform telemetry remains an explicit opt-in.

## What the timing repair does and does not mean

Host-receipt times are recorded when data reaches the computer; operating-system and batch delivery can make their spacing irregular. Packet-counter and chunk evidence can support a declared analysis timing estimate for an eligible recording. That estimate does **not** directly measure each electrode sample's physical acquisition time, recover an unknown missing sample, or establish cross-device synchronization.

This new route is deliberately narrow: original reviewed Zuna v2 or optional-ALS v3 recordings with the supported Cyton/Daisy 125 Hz, packet-step-two, explicit-chunk BrainFlow host-receipt route and verifiable same-run chunk/counter evidence. Legacy or unknown routes retain their existing stricter handling. Selecting this software version alone does not make a recording eligible, and another device's nominal sample rate is not a substitute for the required bridge evidence.

For that route, the analysis verifies recorded chunk endpoints and sample counts against native XDF timestamps, checks counter transitions and ambiguity guards, and fits a sample-index time grid separately within supported contiguous regions. Anomalous chunks and adjoining boundaries remain unverified; no EEG samples are inserted, deleted or filled across a gap. The derivative applies only the recorded XDF clock-offset evidence. It uses neither EEG amplitudes nor held-out targets, condition labels, optical timing or reconstruction error to choose the timing correction. It is an offline, post-hoc preparation policy, not a causal real-time clock repair.

Reports preserve the timing-policy identity, evidence hashes, supported and unverified coverage, and native-versus-derived timing differences. A low residual is not a calibrated physical-timing uncertainty bound. Packet counters wrap and are not independently recorded as raw packet counters in the XDF; the supported inference is therefore an explicit approximation, not proof that hardware loss was impossible.

The original XDF samples/timestamps, recorded contract and QC remain unchanged. Existing evidence of genuine loss, duplicates, resets, invalid timestamps, mismatched identities or inadequate coverage is not silently reclassified as harmless jitter. Optical timing remains independently evaluated. No amplitude-quality threshold, model weight, electrode identity or hidden target selection is changed by this release.

Correct preparation does not demonstrate that Zuna improves on interpolation. Generated signals remain estimates, measured targets are not clean neural ground truth, and repeated windows within a recording are not independent replications. No clinical, live-AI or generalizable reconstruction claim follows from a software or preparation pass.

## Reference material and verification

The [10.3.10 guide](INSTALL_AND_WORKFLOW_ALPHA_10_3_10.md) explains contract discovery and reviewed ALS binding; its statement that the prior native timing rule is unchanged describes that older release. The [10.3.8 workflow](INSTALL_AND_WORKFLOW_ALPHA_10_3_8.md) and [Zuna integration guide](ZUNA_INTEGRATION_ALPHA_10_3_7.md) remain reference material. Use this guide as the current entry point and the single root `CHANGELOG.md` for release history.

Read `app/deployment/validation/BUILD_VALIDATION_v1_0_0_alpha_10_3_11.json` for exactly executed tests and their limitations. Software regression, synthetic acceptance and relocated-package checks do not certify physical hardware, display/ALS timing, a clean installation, new model performance or second-machine replication. Any retained earlier SDK evidence is explicitly labeled historical.

After Core installation, a read-only integrity check from the extracted release folder is:

```text
app\.core-env\Scripts\python.exe -B app\tools\Release_Validation_v0_1\praycg_public_release_check_v1_0.py --package app --output ..\praycg_10311_integrity.json
```

Keep the output outside the release. Add `--tests` to run supplied regression suites. No data is uploaded by these checks or by the optional local comparison.
