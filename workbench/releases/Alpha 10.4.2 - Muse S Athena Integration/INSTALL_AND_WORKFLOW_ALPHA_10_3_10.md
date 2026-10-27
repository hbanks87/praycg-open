# PRAYCG Alpha 10.3.10 — Installation and Analysis Forge workflow

This is a narrow compatibility and evidence-binding hotfix on 10.3.9. It does not change EEG quality thresholds or Zuna's reconstruction comparison. Existing recordings do not require another acquisition simply because the software is updated.

## Install separately

1. Finish recording, stop LabRecorder and managed streams normally, and close the old Workbench. Preserve your existing study folders, incomplete attempts, recordings and results.
2. Extract the complete ZIP into a **new writable folder**. Do not merge releases, run inside the ZIP or replace code in an armed session. Keep the six entry files beside `app/`.
3. With native Windows Python 3.11 and Tcl/Tk available, run **INSTALL.bat**. Core-only setup is `INSTALL.bat -Mode minimal`; normal setup also prepares isolated Live Monitor and Hardware Connectors environments.
4. Run **START_PRAYCG.bat**, confirm **Alpha 10.3.10**, choose **Use Bundled Paths**, and check external PsychoPy, LabRecorder and study paths. Do not leave current runner paths pointing into an older release.
5. Zuna is optional. **INSTALL_ZUNA.bat** installs its separate dependencies and model; `INSTALL_ZUNA.bat -CheckOnly` checks the new release's local installation without installing. A new extracted folder does not automatically contain the old folder's optional environment. Missing Zuna does not block ordinary Required QC.

The ZIP includes application assets and matching source/tests, not Python, PsychoPy, LabRecorder, model weights or installed environments. Existing workspaces remain separate; no study migration or historical reanalysis happens automatically. Do not edit saved hashes or reuse consumed launch authorizations.

## Continue an existing Zuna recording

1. Open the existing workspace/session and **Analysis Forge**. Confirm the exact XDF and recording. If necessary, select its containing folder and then the intended XDF; do not collect multiple studies in one generic input directory.
2. Run **Run Required QC** if the current release requests it. QC and run preparation save derived analysis evidence; they do not rewrite the original XDF. Review the inventory's bound run UUID, runner evidence folder and analysis window.
3. Forge now recognizes the original reviewed `zuna_validation_contract_v2_0.json` as well as supported legacy contracts. Leave acquisition sidecars in their original run-evidence folder. **Do not rename a v2 contract to v1, alter its hashes or replace it with another run's contract.** Missing, ambiguous or incompatible records remain visible errors.
4. If optical timing was enabled but the recorded contract contains an outdated ALS source identifier, use **Review ALS stream binding** in the optional Zuna area **after QC and before a new plan is locked or comparison prepared**. Inspect the actual recorded source, original declaration, channel and run. Provide your reviewer name and an honest reason. Cancel if you cannot identify the intended source.
5. Accepting that review writes a separate immutable post-hoc correction bound to the selected XDF and original contract/evidence. It neither edits the acquisition contract nor approves timing automatically. The correction is explicitly selected for new analysis; unrelated or stale corrections are not automatically adopted. Existing locked plans and prepared comparisons retain their prior identities; make a new reviewed analysis revision rather than changing them in place.
6. Use the optional Zuna panel's input review, preparation and run controls, or add Zuna to a new analysis plan. Confirm the current inputs and evidence classification before starting. Preparation-only checking is not a completed model comparison. Analysis can take substantially longer than the recording.
7. Review the report's execution state, comparison result, original QC cautions and any post-hoc optical binding disclosure separately. Open Results and include the relevant reports/provenance in a privacy-reviewed research bundle. Full waveform telemetry remains an explicit private-data option.

Restoring contract discovery does not guarantee that model preparation will pass. Native sample/timestamp, block coverage, reference, units and other suitability checks still run; a separate timing failure is not an EEG-amplitude-quality verdict. This release does not relax those checks or interpolate across gaps to obtain a pass.

An ALS correction only addresses which recorded stream the analysis should inspect. Missing sequences, poor signal, unsuitable clocks or mismatched observations can still prevent optical validation. Successful reconstruction analysis does not establish clean neural recovery, clinical utility or prospective validation. No optical correction changes the held-out EEG targets or turns generated channels into measured electrodes.

## Retained acquisition and workflow

New reviewed Zuna runs still collect channel/reference, geometry and optional ALS declarations before fullscreen. Review the **current attempt's exact source ID**, not a previous attempt's identifier. Explicit fullscreen confirmation and normal LabRecorder operation remain required. The scientific schedule and protocol identities are unchanged.

The [10.3.9 startup workflow](INSTALL_AND_WORKFLOW_ALPHA_10_3_9.md), [10.3.8 detailed workflow](INSTALL_AND_WORKFLOW_ALPHA_10_3_8.md), [correctness and method limits](CORRECTNESS_AND_METHODS_ALPHA_10_3_8.md) and [Zuna integration decisions](ZUNA_INTEGRATION_ALPHA_10_3_7.md) remain reference material; this guide is the current starting point. The consolidated `CHANGELOG.md` is the release history.

## Verification boundaries

The exact current checks and limitations are in `app/deployment/validation/BUILD_VALIDATION_v1_0_0_alpha_10_3_10.json`. Tests include synthetic/headless behavior and relocated-package checks, not a new human experiment, physical optical/display test, full model comparison, clean install or second-machine replication. Earlier SDK evidence, where retained for identical files, is labeled historical rather than newly executed.

For a read-only package check after Core installation, run from the extracted release folder:

```text
app\.core-env\Scripts\python.exe -B app\tools\Release_Validation_v0_1\praycg_public_release_check_v1_0.py --package app --output ..\praycg_10310_integrity.json
```

Keep the output outside the release. Add `--tests` to run the supplied regression suites. Verification checks bytes and software behavior, not scientific validity or upstream licensing clearance.
