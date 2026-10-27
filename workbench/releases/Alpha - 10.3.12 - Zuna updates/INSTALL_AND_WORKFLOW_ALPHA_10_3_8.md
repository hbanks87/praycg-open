# PRAYCG Alpha 10.3.8 — Installation and workflow

## Install beside the previous release

1. Finish any recording, stop LabRecorder and close the previous Workbench. Back up study folders separately.
2. Extract the entire ZIP into a **new** writable folder. Do not merge releases or replace your study folder. Keep the six entry files and `app` together.
3. Use native Windows Python 3.11 with Tk support. Run `INSTALL.bat`. Setup downloads Core, Live Monitor and Hardware Connector dependencies into separate local environments; it no longer changes global Python packages. A failed component is reported separately.
4. Core-only setup: `INSTALL.bat -Mode minimal`. Checks only: `INSTALL.bat -CheckOnly`. A Core environment must exist before normal startup; an older global installation does not satisfy that requirement.
5. Run `START_PRAYCG.bat`. In Settings, use bundled tool paths and verify your separate PsychoPy and LabRecorder paths. Do not point tools back at an older release.
6. Zuna remains optional: `INSTALL_ZUNA.bat` downloads its separately isolated dependencies/model. No model, EEG recording or installed Python environment is shipped in this archive.

The direct Core constraints record observed release-test package versions, not a complete hash-locked wheel/transitive dependency inventory. Installer control-flow tests do not establish successful installation on a clean second machine. Preserve any installation error report.

## Record and analyze

Use the existing sequence: workspace → protocol → media preparation and fingerprints → hardware profile → equipment check → confirm/arm → LabRecorder and runner → prepare run → Required QC → analysis plan → Results.

The 30-second equipment check now evaluates coverage across the requested interval and receipt of recent samples near the end. A briefly active or stalled stream must not pass as a complete check. Explicit Bench Test Mode remains separate from participant eligibility and does not manufacture physical signal evidence.

Stop OpenBCI bridges from Running Tools and allow time for graceful device release and final diagnostics. Force close remains a separate fallback; it cannot guarantee release diagnostics. Old bridges without the new stop mechanism may still require guarded recovery.

The native runner records software-flip event timing and completed uninterrupted playback alignment for fingerprints. These are software timing observations, not measured photon latency or validated cross-device synchronization. Keep ALS checks and their limitations visible. Paused, missing, incomplete or mismatched playback must not silently become a valid continuous alignment.

For existing runs, select the exact run folder and prepare it normally. Run new analyses as **new attempts**; do not replace old reports or alter their hashes. This release does not retroactively recalculate an old run simply by opening it. Older runs lacking bound fingerprint timing receive a clear unavailable adjusted result while other descriptive analyses remain available.

If an older locked plan reports changed software bindings, create a new plan revision using the current release. Retain the old plan and its attempts; do not edit lock hashes to make an earlier plan appear to have used corrected code.

## Read the results

Analysis Forge Results retains each module's reports and the six-question explanation: question, findings, meaning, supported comparisons, limitations and next step. Study Explanation consolidates executed results without treating shared-data measures as independent replications. Missing estimates are not zero, failed calculations are not null findings, and a positive difference is not proof of a theory.

Stimulus adjustment requires verified final media, fingerprint tables and condition-specific time alignment. Reports retain original and adjusted values, model identity, included/excluded windows and estimation limitations. An adjusted residual is not a measure of meaning or evidence of a neural mechanism. Micro Handoff remains descriptive with **sensitivity not validated**; inspect its unfavorable synthetic audit rather than interpreting a process exit as scientific success.

Explain existing results remains a separate report derivative, not a numerical rerun. AI returns require the original evidence packet, validated placeholders and explicit human review. Numeric-text screening cannot verify all prose or scientific claims. AI/report failure must not erase a completed numerical result.

## Export and bundle

BIDS export uses the first stored EEG sample as origin for explicit LSL events. Ambiguous time columns, unknown units and unsupported regularization are reported instead of guessed. Copied raw XDF can retain identifying information. Changing subject labels is **not de-identification**. Export completion and independent readback do not certify whole-dataset BIDS compliance; use the appropriate external validator and privacy review before distribution.

Reviewing a results bundle first checks its existing ledger and original content binding. Modified bundles are rejected instead of receiving a fresh apparently original checksum. Corrected content belongs in a new derived bundle. Earlier review receipts are retained.

## Reproduce software checks without changing the release

In a terminal at the extracted release folder, after Core setup:

```text
app\.core-env\Scripts\python.exe -B app\tools\Release_Validation_v0_1\praycg_public_release_check_v1_0.py --package app --output ..\praycg_1038_integrity.json
```

Add `--tests` to run the supplied automated regression suites. The report path must be **outside** the extracted release. The Workbench's public release-check action uses the same non-mutating entry point. It never installs dependencies, opens equipment, rewrites release manifests or validates participant safety. Matching tests and generated-fixture instructions are in `app`; synthetic data are created in temporary folders, not confused with human recordings.

See `app/deployment/validation/BUILD_VALIDATION_v1_0_0_alpha_10_3_8.json` for the precise checks executed for this build. Historical validation records are historical evidence only. No clean-machine installation, physical Cerelog/EEG/ALS test, new Zuna inference, general neural validity or live adaptive-AI safety is implied.

The retained [10.3.7 guide](INSTALL_AND_WORKFLOW_ALPHA_10_3_7.md) documents the detailed optional Zuna workflow. The [correctness/method guide](CORRECTNESS_AND_METHODS_ALPHA_10_3_8.md) explains this release's interpretation limits.
