# Alpha 10.3.5 — installation and operator workflow

## Install separately

1. When no recording is active, close the previous Control Center. Back up study folders separately.
2. Extract the complete ZIP into a new writable local folder. Do not merge releases or run inside the archive. Keep the `app` folder beside the launchers.
3. Run `INSTALL.bat`, then `START_PRAYCG.bat`. The core setup does not install Zuna; existing vendor software, PsychoPy and LabRecorder requirements remain.
4. If using Zuna in this release, run `INSTALL_ZUNA.bat` explicitly. It installs pinned upstream packages/model into this release's separate environment; it may download several gigabytes. Do not copy an old environment between versions. A cached download may be reused only if its expected identity verifies.
5. Open the intended Study Workspace and check the selected run. No release installation rewrites an XDF or upgrades historical BENCH evidence.

## Record with warnings

Select and lock the protocol/materials and reviewed hardware profile, start the hardware streams, and run the required 30-second check. Read the individual findings. READY WITH WARNINGS means acquisition may proceed after a recorded operator decision; it is not a clean-signal certificate.

Confirm Session Setup, enter the operator and participant pseudonym, and record a reason for accepting warnings. The lock preserves the exact report hashes, policy and finding codes. Do not enable Bench Test Mode merely to acknowledge these warnings. Missing or wholly unusable required data, wrong identities/units and essential setup errors still need correction.

Bench mode remains available for deliberate non-participant tests; old BENCH recordings retain that historical designation. Experimental hardware profiles and exact connection identity contracts retain their existing restrictions.

Start LabRecorder yourself, ensuring the required streams and StasisMarkers are selected. Launch the locked runner. Stop LabRecorder after completion and finalize the run using the existing workflow. PRAYCG does not operate LabRecorder's record/stop buttons.

## Analyze an existing recording

1. Select its run folder in Analysis Forge, or confirm the automatically selected folder. Resolve exactly one XDF.
2. Prepare/finalize that recorded run if needed. The recorded protocol, not the currently selected next experiment, determines the analysis identity.
3. Run Required QC. A completed CAUTION report is usable diagnostic evidence, not a crashed job.
4. Add the desired modules. Automatic prerequisites remain part of the locked plan. A plan from another version/protocol may be preserved in history and require a fresh binding; do not edit its hashes.
5. Run the plan. Regenerate preprocessing under 10.3.5 rather than reusing an old derivative that joined missing time. New derivatives preserve original timestamps, segment boundaries and exclusions.
6. Open each persistent results card. Distinguish completed analysis, insufficient usable input, missing prerequisite and execution failure. Review retained seconds/trials and all exclusions before interpreting a number.

The five-second filtering guards are a declared engineering policy, not proof that artifacts have disappeared. Some analyses need longer uninterrupted periods or enough independent trials. No module is entitled to manufacture a result simply because recording succeeded.

## Zuna on an older recording

In the optional Zuna panel, use Review inputs and Prepare comparison. If the old contract has a different electrode map or a whole-window continuity limitation, preparation directs you to Review existing recording. This does not mean the signal is generally unusable.

The review locates the saved contract, session lock and block ledger. It suggests same-run historical clock diagnostics covering the evaluation blocks; if evidence is missing or ambiguous, choose the correct file explicitly. Confirm the actual physical electrode order, microvolt units, external reference and absence of a prior all-channel digital average reference. Inspect the exact template geometry and disclosed model-coordinate clipping before saving a new post-hoc recipe.

Your explicit recipe selection is retained for that recording. Preparation verifies all eight evaluation blocks and writes an eligibility receipt without model inference. It excludes calibration from this endpoint. If an evaluation block fails, the fixed eight-block comparison remains unavailable and reports exactly which block failed; it does not silently select a favorable subset.

Once preparation succeeds, choose Run prepared comparison. CPU threads are frozen into that attempt. Cancel safely to retain compatible checkpoints. Compare measured hidden targets against both Zuna and spherical-spline interpolation; lower error is better. The model may lose. Model-generated values are not clean neural ground truth or replacement hardware measurements.

Adopt completed result can preserve an earlier comparison without rerunning the model. Its original model/software provenance and post-hoc/BENCH classification remain visible.

## New Zuna recordings and ALS

The reviewed-montage protocol remains available. The separate optical-timing variant adds optional source-bound pre/post screen sequences and 10-second settling guards outside the ten-minute calibration/evaluation content. It adds about 29.5 seconds plus operator instructions. No barcode flashes occur inside scored resting blocks.

If using optical timing, select the exact ALS stream and recorded channel as requested by the runner. A missing optional ALS result is UNVERIFIED and does not block EEG analysis. Required primary hardware streams and shared-device connection identities remain separately governed. An optical PASS is not evidence of actual sound onset, eye closure, cross-device synchronization or continuous timing accuracy throughout the recording.

## Review and bundle

Per-module reports retain warnings, exclusions and method versions. Use the existing bundling layer for a privacy-reviewed results package. Raw telemetry and private waveform arrays require the explicit private/full-telemetry choices. Private reports can still contain identifiers; review them before sharing or AI upload. Nothing is uploaded automatically.

See `RECORDING_ANALYSIS_POLICY_ALPHA_10_3_5.md` and `RELEASE_NOTES_v1_0_0_alpha_10_3_5.md` for precise boundaries. Older installation guides are historical references.
