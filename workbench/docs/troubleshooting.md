# Troubleshooting

**Maintained guide · Public Alpha 11.9.2 · reviewed 2026-10-25.** These checks follow the shipped [installation/workflow reference](releases/alpha-11.9.2/package/INSTALL_WORKFLOW.md), [guided workspace](releases/alpha-11.9.2/package/GUIDED_WORKSPACE_11_8.md) and [integration guide](releases/alpha-11.9.2/package/INTEGRATION_11_9.md). Keep the original files and error evidence while investigating.

## Installation and updates

| Symptom | Check or next action |
| --- | --- |
| Download has no application launchers | Download the named **PRAYCG_Workbench_Public_Alpha_11_9_2.zip** release asset. GitHub source archives are repository snapshots. |
| Installation or first launch fails | Confirm native Windows Python 3.11 with Tcl/Tk, extract into a new writable folder and run the outer `INSTALL.bat`, then `START.bat`. Retain the failing component's installer output. Core, Live Monitor and Hardware Connectors have separate environments; follow the [installation guide](installation.md). |
| Signed ZIP import is rejected | Use the matching Public ZIP and its exact `.zip.update.json` companion from the release. Edition, signature, archive and state checks must pass. Do not change hashes or bypass signature checks. |
| Update preparation fails or appears incomplete | In **Settings → Updates**, choose **Open update folder / logs**. Prepared updates live under the edition's folder in `%LOCALAPPDATA%\PRAYCG\updates`. Dependencies can require internet access or cached packages even with a local ZIP. Preserve the existing installation and inspect the recorded failure. |
| Update/restart is blocked | Finish acquisition, analyses, provider requests and exports; stop/save LabRecorder and close running viewers/tools. Active ownership and jobs block restart. **Cancel preparation safely** waits for a safe boundary. |
| Zuna paths no longer resolve after an update | Keep any older/shared runtime and model folders still referenced. Verify the new release's connection against the pinned contract. Do not reinstall or download models merely because the application changed; extraction alone does not verify the binding. |

The [release build report](releases/alpha-11.9.2/package/BUILD_REPORT.md) distinguishes completed checks from the 10 guard-refused installer-wrapper checks and records that fresh-machine installation was not tested. Treat those limits as limits, not successful installer evidence.

## Recording and analysis

| Symptom | Check or next action |
| --- | --- |
| A required sensor is absent from the saved recording | Confirm whether its actual outlet was selected in LabRecorder. A connected but unrecorded sensor cannot be recovered later. Review [hardware and recording support](hardware-support.md) before the next acquisition. |
| A publisher was restarted or its metadata changed | For an external-publisher profile with a changed outlet UID or descriptor, build and review a new profile and use a new Equipment Session. A same-name replacement cannot satisfy the old lock; see [hardware guidance](hardware-support.md). |
| Plan says **READY BUT NOT RUN** | Choose **Run pending analyses**. A saved plan has not necessarily executed. |
| Current results are empty but an older report exists | Check recording/run identity and select the prior results explicitly. Historical results do not populate a new run automatically. |
| Endpoint says **NOT_ESTIMABLE** or unavailable | Read its reason: required channels, units, timing, duration, finite samples, gaps, adjacency or baseline may be insufficient. Do not substitute zero or relax support merely to obtain a value. |
| Time-frequency work finished but no plot appeared | Use **Open latest time-frequency view**. Batch work saves plots without automatically opening a window. |
| Paired processing viewer rejects a result | Check registration, source receipt, array hashes and timing provenance. A legacy result without adequate recording-clock metadata may need a new comparison derivative. Do not guess its origin or modify fingerprints. |
| Frozen raw traces display but a processing branch is unavailable | A short interval can support waveform inspection while failing filtering's continuous-support or edge requirements. Read support/exclusion evidence; candidates must match the exact source and timestamps. |
| AI explanation fails or is unavailable | Review the saved numerical and module reports directly. Provider configuration and authorization are separate from local numerical analysis; preserve the provider error for diagnosis. |

See [analysis and interpretation](analysis.md) for the exact analysis, report, figure and comparison actions.

## Materials and browser export

For missing optional films, use the verified stimulus installer and its [installation instructions](releases/alpha-11.2.2/STIMULUS_INSTALLATION.md). Seven films and the original Lantern are separately verified packages; the full eleven-film companion is not included in the public release. Installation or preparation does not replace operator review of the material and protocol.

If browser export cannot write its destination, choose a **new** HTML filename in an existing folder on a filesystem supporting hard links. The exporter refuses to overwrite existing files and verifies the bundle/ledger before export. Some members are intentionally omitted from bounded previews and remain listed with reasons. The page does not decode XDF/NPZ or rerun analysis. See the [browser-export contract](releases/alpha-11.9.2/package/GUIDED_WORKSPACE_11_8.md#7-export-a-local-browser-inspection-copy).

## Report a reproducible problem

Include the exact release, action, source mode (synthetic, saved recording or live), relevant hardware/profile, error text and a minimal non-sensitive reproduction. The isolated **Try an example** route can help distinguish application behavior from a particular private recording. Inspect logs and reports for identifiers, credentials and private paths before sharing; keep raw participant recordings private unless their sharing is authorized. Follow the repository's [contribution guidance](../../CONTRIBUTING.md).

[Workbench home](../README.md) · [Installation](installation.md) · [Study workflow](workflow.md) · [Analysis](analysis.md)
