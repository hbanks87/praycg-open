# Installation and first launch

**Current packaged release: Alpha 10.2.1.** Use the preserved [Alpha 10.2.1 installation and maintenance guide](releases/alpha-10.2.1/INSTALLATION_ALPHA_10_2_1.md) for the complete procedure, repair modes, upgrade instructions and uninstall boundaries.

## Before you begin

- Download the [versioned application ZIP](../releases/alpha-10.2.1/PRAYCG_ControlCenter_v1_0_0_alpha_10_2_1.zip) and extract it completely into a new writable folder.
- Provide native Windows Python 3.11 with Tcl/Tk support. The installer does not install Python.
- Expect internet access to be needed for Python dependencies. PsychoPy, LabRecorder, device drivers and external publishers are separate installations.
- Keep study data outside the extracted application folder and keep each release in its own folder.

## Installation decisions

| Component | Alpha 10.2.1 behavior |
| --- | --- |
| Core | Installs into the selected native Python 3.11 interpreter; the installer does not isolate it in a dedicated environment |
| Live Monitor | Uses its own release-local Python environment |
| Hardware Connectors | Uses a separate release-local environment with pinned connector requirements |

The default `INSTALL.bat` mode checks or installs all three components. The full guide explains `minimal`, `monitor`, `hardware` and `-CheckOnly`, including where installation evidence is written. Installation checks establish software importability; they do not test a physical device or its timing.

## After installation

Launch `START_PRAYCG.bat` from the extracted release. In Settings, select **Use Bundled Paths**, verify PsychoPy and LabRecorder, and review the configured study-data locations. Then continue to the [workflow index](workflow.md) and [hardware-support notes](hardware-support.md).

The full guide remains the release-specific reference. This page is an entry point and does not replace its detailed instructions.

[Workbench](../README.md) · [Full installation guide](releases/alpha-10.2.1/INSTALLATION_ALPHA_10_2_1.md)
