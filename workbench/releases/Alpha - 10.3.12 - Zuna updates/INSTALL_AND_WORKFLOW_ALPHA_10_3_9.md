# PRAYCG Alpha 10.3.9 — Installation and startup workflow

This is a focused hotfix on Alpha 10.3.8, not a change to EEG quality standards or Zuna's numerical comparison.

## Install separately

1. Finish recording, stop LabRecorder, stop managed streams through **Running Tools**, and close the old Workbench. Preserve study folders and incomplete attempts.
2. Extract the complete ZIP into a **new writable folder**. Do not merge releases, copy files into an armed session, or run inside the ZIP. Keep the six entry files beside `app/`.
3. With native Windows Python 3.11 available, run **INSTALL.bat**. Core-only setup is `INSTALL.bat -Mode minimal`; normal setup also prepares Live Monitor and Hardware Connectors. Dependencies are installed in separate local environments.
4. Run **START_PRAYCG.bat**. Confirm **Alpha 10.3.9**, choose **Use Bundled Paths**, and verify your external PsychoPy, LabRecorder and study paths. Do not retain runner paths into the previous release.
5. Zuna remains optional. **INSTALL_ZUNA.bat** installs its isolated dependencies/model; `INSTALL_ZUNA.bat -CheckOnly` performs a check without installing. Zuna is not needed to record the protocol, perform the ALS test or run ordinary Required QC.

The ZIP contains application source/assets and matching tests, not Python, PsychoPy, LabRecorder, model weights or a copied installed environment. Installing does not rerun old analyses or silently migrate locked settings. If a saved lock is bound to old runner code, make a fresh reviewed session/lock in the new release; never edit its hashes or reuse a consumed launch authorization.

## ALS barcode placement test

1. Select the intended hardware profile and equipment session.
2. Start the EEG/ALS bridge normally, or let **ALS Barcode Placement Test** offer to start it.
3. Run the test. A verified virtual-environment launcher/child pair is now treated as one current-session bridge and reused. No process is stopped merely to inspect ownership.
4. If genuinely different or insufficiently verified bridges remain, the test still blocks. When no recording/protocol is active, use **Running Tools** to stop the relevant bridge, wait for complete exit, then retry. Do not kill just one member of a launcher/child pair.
5. A successfully opened barcode window is not an ALS PASS. Inspect its saved measured response. Missing samples, a wrong-session outlet or a failed board connection remain separate errors.

## New Zuna validation run

For your sixteen-channel Cyton/Daisy plus ALS setup, choose **AI-Assisted EEG Reconstruction — Reviewed Montage + Optional Optical Timing**. Without the optional optical sequences, use **AI-Assisted EEG Reconstruction — Reviewed Montage (new runs)**. Both receive the setup-window fix; the original fixed-map protocol is not a substitute for reviewing actual wiring.

Follow the normal workspace → protocol → materials → hardware → equipment checks → confirm/arm workflow. On runner launch:

1. Review the channel-mapping dialog while **no fullscreen stimulus window exists**. Enter the reviewer, actual channel order, microvolt units, actual source sample rate, physical reference and digital-reference history. Defaults are proposals, not automatic approval.
2. Review and confirm the disclosed template geometry.
3. For the optical variant, review the independently recorded ALS source or explicitly leave the optical option disabled. Enabling it requires the exact stream name, source ID, channel, polarity and placement declaration.
4. Complete the runner's recording/preflight instructions. PRAYCG does not start or stop LabRecorder for you.
5. Fullscreen opens only after these reviews and the final authority check. Press **R** when the fullscreen confirmation instructions accurately describe the reviewed acquisition. The runner preserves the actual declarations in its contract before timed content.

Record all sixteen EEG channels. F3/F4/P3/P4 are withheld only during the offline comparison; do not unplug them. The scheduled content remains 600 seconds, with optional optical sequences/guards and setup instructions outside it.

Cancelling any review stops this attempt before timed calibration/evaluation. Setup markers or externally recorded samples may already exist, so the attempt remains explicitly incomplete rather than being erased or called empty. Keep its files. The runner finalizes and releases its authorization through the existing cancellation path.

## Analysis and verification

Use the normal Analysis Forge workflow after recording. Existing recordings do not need a new protocol run simply because this hotfix was installed. The [10.3.8 detailed workflow](INSTALL_AND_WORKFLOW_ALPHA_10_3_8.md), [correctness/method limits](CORRECTNESS_AND_METHODS_ALPHA_10_3_8.md) and [Zuna integration decisions](ZUNA_INTEGRATION_ALPHA_10_3_7.md) remain applicable except for the setup order described here.

For a read-only package check after Core installation, run from the extracted release folder:

```text
app\.core-env\Scripts\python.exe -B app\tools\Release_Validation_v0_1\praycg_public_release_check_v1_0.py --package app --output ..\praycg_1039_integrity.json
```

Use an output path outside the release. Add `--tests` to run the supplied regression suites. Consult `app/deployment/validation/BUILD_VALIDATION_v1_0_0_alpha_10_3_9.json` for this build's exact executed checks. Source/package checks and synthetic tests do not establish hardware safety, measured display timing, Zuna efficacy or a clean-machine installation.
