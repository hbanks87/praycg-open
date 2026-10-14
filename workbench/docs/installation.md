# Installation and first launch

## Public Alpha 11.2.2 update

Public Alpha 11.2.2 is the prepared replacement described in the [release guide](releases/alpha-11.2.2/README.md). Final publication is pending. Follow the new archive's own instructions and verification record; the Alpha 10.5.4 instructions below remain labeled historical published behavior until the new asset is verified.

Install an update into a **new release folder**, never over an old application or study-data folder. Retain existing settings, workspaces, recordings, external PsychoPy settings and Zuna environment/model paths. New release-local Core, Live Monitor and connector environments are independent of those study files. Do not reinstall Zuna merely to update the Workbench; first verify the existing configured environment and model paths. Back up important studies before any upgrade.

The standard path remains **INSTALL.bat → START.bat**. The Public package contains the independent PRAYCG AI Assistant and needs no private extension. Optional AI configuration is separate from local numerical analysis; do not paste credentials into public issue reports.

**INSTALL_STIMULUS_PACKAGE.bat** now offers the seven-film collection plus the original Lantern demo as two separate verified packages. It uses pinned release URLs, supports exact local ZIPs and checks destination/storage before installation. See [optional stimulus instructions](releases/alpha-11.2.2/STIMULUS_INSTALLATION.md). After installation, refresh installed masters in Prepare Materials and select the master for normal protocol-specific preparation and fingerprinting.

Saved studies and original measurements are not migrated into a new numerical meaning by this patch. Reanalysis and new explanations create new derivatives. A missing endpoint, absent physical sensor or unavailable provider remains visible without erasing available reports.

## Preserved Alpha 10.5.4 installation

**Current packaged release: Alpha 10.5.4.** Download the complete [PRAYCG Workbench Alpha 10.5.4 ZIP](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_A10.5.4/PRAYCG_Workbench_Alpha_10_5_4.zip) and follow the [current installation and workflow guide](releases/alpha-10.5.4/INSTALL_AND_WORKFLOW_ALPHA_10_5_4.md).

## Before you begin

- Extract the complete ZIP into a new writable folder, keeping `app/` beside the public launchers. Run the application from the extracted folder.
- Provide native Windows Python 3.11 with Tcl/Tk support. The installer requires this interpreter and does not install Python.
- Provide internet access for dependency downloads. PsychoPy, device drivers and external publishers still need their own installation or configuration.
- Keep study data in separate data folders and keep each release in its own folder. Preserve previous installations when upgrading.

## Install the components

Run `INSTALL.bat`, then `START.bat` or `START_PRAYCG.bat`. The normal installation includes all three components in separate release-local environments:

| Component | Alpha 10.5.4 environment |
| --- | --- |
| Core | `app/.core-env/` |
| Live Monitor | `app/.live-monitor-env/` |
| Hardware Connectors | `app/.hardware-connectors-env/` |

Core dependencies are installed in the dedicated environment, rather than the selected base Python installation. Retain installer output if a component fails.

Use `INSTALL.bat -Mode minimal` for Core only, `INSTALL.bat -Mode monitor` to repair Live Monitor, `INSTALL.bat -Mode hardware` to repair connectors, and `INSTALL.bat -CheckOnly` for read-only installation checks. Optional Zuna uses `INSTALL_ZUNA.bat` separately. An installation pass establishes software importability; physical devices and timing require their own evidence.

## First launch and upgrade

In Settings, select **Use Bundled Paths** to use this release's tools. Review the study-data locations, retain the intended external PsychoPy configuration, and select the bundled PRAYCG timing-patched LabRecorder. Its preserved recorder qualification has a synthetic scope; the Workbench release does not expand that scope into physical-device or cross-device timing validation.

Connect Athena through the normal Muse connection action. Use its red/yellow/green map to adjust contact. Recording readiness briefly checks actual incoming data; the thirty-second signal check is optional. Follow the [recording-with-cautions guide](releases/alpha-10.5.2/RECORDING_WITH_CAUTIONS_ALPHA_10_5_1.md) for findings that allow recording and issues that require correction.

Confirm and arm the setup, start LabRecorder before the protocol, then **Stop LabRecorder** when finished so the XDF closes before analysis. Select the separate Optical stream if later optical analysis is intended; save any required EOG/EMG references in the same XDF. Continue to the [workflow](workflow.md) and [hardware-support notes](hardware-support.md).

Open the completed recording in Analysis Forge for **Visual Analysis**, immediately after **Analyze**. Live Monitor places **Visual Analysis** beside **Time–Frequency**. Use **Visual sources** to select the exact EEG and optional RR inputs and declare electrode names, units and calibration. The dialog opens while recorded streams are loading, updates when they arrive and shows setup failures. Calibration starts at shared-recording time 0 by default; selecting the EEG stream's recorded start keeps that clock unchanged and still requires valid support. The [Visual Analysis guide](releases/alpha-10.5.4/VISUAL_ANALYSIS_ALPHA_10_5_4.md) distinguishes recorded prefix replay, passive live views and compatible completed-result attachments.

Alpha 10.5.4 restores the exact retained receipt required by Athena **Human connected** profile validation and checks runtime dependency closure. Missing or altered evidence still blocks admission. Current checks cover software regression, native visual integration, packaged admission and distribution hashes. A fresh full installation, optional Zuna installation/inference, physical acquisition and cross-device timing were not reexecuted as part of this release gate; retained earlier evidence keeps its original scope. See the [current implementation and validation boundaries](releases/alpha-10.5.4/UPDATE_TRACEABILITY_ALPHA_10_5_4.md).

The preserved [Alpha 10.2.1 installation guide](releases/alpha-10.2.1/INSTALLATION_ALPHA_10_2_1.md) documents that historical release, including its different Core installation behavior.

[Workbench](../README.md) · [Current installation guide](releases/alpha-10.5.4/INSTALL_AND_WORKFLOW_ALPHA_10_5_4.md) · [Release notes](releases/alpha-10.5.4/RELEASE_NOTES_v1_0_0_alpha_10_5_4.md)
