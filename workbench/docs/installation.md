# Installation and first launch

**Current packaged release: Alpha 10.5.2.** Download the complete [PRAYCG Workbench Alpha 10.5.2 ZIP](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_A10.5.2/PRAYCG_Workbench_Alpha_10_5_2.zip) and follow the [current installation and workflow guide](releases/alpha-10.5.2/INSTALL_AND_WORKFLOW_ALPHA_10_5_2.md).

## Before you begin

- Extract the complete ZIP into a new writable folder, keeping `app/` beside the public launchers. Run the application from the extracted folder.
- Provide native Windows Python 3.11 with Tcl/Tk support. The installer requires this interpreter and does not install Python.
- Provide internet access for dependency downloads. PsychoPy, device drivers and external publishers still need their own installation or configuration.
- Keep study data in separate data folders and keep each release in its own folder. Preserve previous installations when upgrading.

## Install the components

Run `INSTALL.bat`, then `START_PRAYCG.bat`. The normal installation includes all three components in separate release-local environments:

| Component | Alpha 10.5.2 environment |
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

The preserved [Alpha 10.2.1 installation guide](releases/alpha-10.2.1/INSTALLATION_ALPHA_10_2_1.md) documents that historical release, including its different Core installation behavior.

[Workbench](../README.md) · [Current installation guide](releases/alpha-10.5.2/INSTALL_AND_WORKFLOW_ALPHA_10_5_2.md) · [Release notes](releases/alpha-10.5.2/RELEASE_NOTES_v1_0_0_alpha_10_5_2.md)
