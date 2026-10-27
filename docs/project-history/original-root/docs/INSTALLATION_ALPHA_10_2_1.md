# PRAYCG Control Center Alpha 10.2.1 — Installation and maintenance

This guide covers the packaged Windows installer for PRAYCG Control Center
Alpha 10.2.1. Begin with the [project README](../README.md), then use the
[end-to-end workflow guide](WORKFLOW_ALPHA_10_2_1.md) after installation.

PRAYCG is alpha research software. Installing it does not validate a protocol,
approve hardware for participant use or turn the system into a medical or
clinical device.

## Before installing

You need:

- a Windows computer capable of running the supplied `.bat` and PowerShell
  launchers;
- native Windows **Python 3.11** with Tcl/Tk support;
- internet access to Python package sources during installation or repair;
- a writable local folder with enough free space for the application and two
  optional isolated Python environments; and
- separate installations of PsychoPy and LabRecorder if you intend to run
  protocols and record XDF files.

The installer looks for Python 3.11 in this order:

1. the usual per-user Python 3.11 location under `%LOCALAPPDATA%`;
2. the Windows Python launcher, `py -3.11`; and
3. `python.exe` on `PATH`.

An interpreter with a different major or minor version is rejected. The
installer does not install Python itself.

PsychoPy, LabRecorder, device drivers and third-party publishers are not
included. They are not installed, upgraded or validated by `INSTALL.bat`.

## Verify and extract the download

If the release includes the adjacent
`PRAYCG_ControlCenter_v1_0_0_alpha_10_2_1.zip.sha256.txt` file, calculate the
ZIP hash in PowerShell:

```powershell
Get-FileHash .\PRAYCG_ControlCenter_v1_0_0_alpha_10_2_1.zip -Algorithm SHA256
```

Compare the displayed hash with the first field in the `.sha256.txt` file.
The comparison is case-insensitive. If they differ, do not use the archive.

Then:

1. Stop and save any active LabRecorder recording.
2. Stop PRAYCG-owned connectors from the Control Center and close all Control
   Center windows.
3. Extract the **entire ZIP** into a new writable local folder.
4. Do not run the program from inside the ZIP.
5. Do not extract over or merge with an older PRAYCG release.
6. Keep the `app` directory beside the five public files: `INSTALL.bat`,
   `START_PRAYCG.bat`, `README.md`, `CHANGELOG.md` and `LICENSE.md`.

Keeping each release in its own folder preserves the old program for audit or
rollback. Study data should remain outside the application folder.

## Standard installation

Double-click `INSTALL.bat`, or open a terminal in the extracted release folder
and run:

```text
INSTALL.bat
```

This is the same as `INSTALL.bat -Mode full`. It installs or checks all three
components:

| Component | Location | What the installer does |
| --- | --- | --- |
| Core | The discovered native Python 3.11 interpreter | Upgrades pip, setuptools and wheel; installs `app\requirements_PRAYCG_v1_0_0_alpha_10_2_1.txt`; checks imports and acquisition libraries without opening devices. |
| Live Monitor | `app\.live-monitor-env\` | Creates or repairs a dedicated environment from `app\tools\Live_Monitor_v1_0\requirements.txt`, checks its dependencies and performs an LSL clock-only native-library check. |
| Hardware Connectors | `app\.hardware-connectors-env\` | Creates or repairs a dedicated environment from `app\deployment\requirements_hardware_connectors.txt`, checks pinned BrainFlow/LSL libraries and reads Crown and Muse S Athena software descriptors without opening devices. |

Core does **not** receive its own PRAYCG virtual environment. Its installation
can change packages in the discovered Python 3.11 interpreter. Use a Python
installation you are comfortable dedicating to this software; do not point
the installer at PsychoPy's Python.

Live Monitor and Hardware Connectors are isolated from Core, from each other
and from PsychoPy. Do not manually combine their packages. In particular,
OpenMuse requires its own external Python 3.12-or-newer setup and must not be
installed into PRAYCG's Python 3.11 hardware environment.

At the end, read every component result. A full installation is complete only
when Core, Live Monitor and Hardware Connectors all report `PASS`. The
installer continues to report the other components after one component fails,
so partial success must not be mistaken for a complete installation.

## Installation and repair modes

Run these commands from the extracted release folder:

```text
INSTALL.bat -Mode full
INSTALL.bat -Mode minimal
INSTALL.bat -Mode monitor
INSTALL.bat -Mode hardware
```

| Mode | Scope |
| --- | --- |
| `full` | Core, Live Monitor and Hardware Connectors. This is the default. |
| `minimal` | Core only. It does not create or repair either isolated environment. |
| `monitor` | Live Monitor only. It does not modify Core or the hardware environment. |
| `hardware` | Hardware Connectors only. It does not modify Core or the monitor environment. |

Repeating a mode repairs or rechecks its requested component. It does not
delete study data.

Add `-CheckOnly` to check a requested component without installing packages,
upgrading installer tools, creating an environment or writing an environment
lock. Examples:

```text
INSTALL.bat -Mode full -CheckOnly
INSTALL.bat -Mode minimal -CheckOnly
INSTALL.bat -Mode monitor -CheckOnly
INSTALL.bat -Mode hardware -CheckOnly
```

Check-only mode still writes a small installation-result record. A missing
isolated environment is reported as a failure because check-only mode will not
create it.

`START_PRAYCG.bat -CheckOnly` checks Python 3.11 discovery only. It does not
replace `INSTALL.bat -CheckOnly` and does not verify the application's package
dependencies.

## Installation evidence

The installer writes component results outside the immutable release folder:

```text
%LOCALAPPDATA%\PRAYCG\installation_logs\
```

Core and Live Monitor environment inventories are written to:

```text
%LOCALAPPDATA%\PRAYCG\environment_locks\
```

The Hardware Connectors component uses pinned requirements and records
relevant runtime versions in session evidence, but Alpha 10.2.1 does not write
a complete hardware-environment inventory to that directory.

These checks establish software importability only. They do not open a device,
prove that samples are arriving, measure synchronization or approve equipment
for participant acquisition.

## First start

Double-click `START_PRAYCG.bat`, or run:

```text
START_PRAYCG.bat
```

On first start, PRAYCG creates its saved settings and its default data folders.
Open **Settings** and:

1. choose **Use Bundled Paths** so packaged tools point to this exact release;
2. select and verify the external PsychoPy application/interpreter paths;
3. select and verify the external LabRecorder executable; and
4. review the PRAYCG home, run, analysis, log and workspace locations before
   collecting data.

The default Windows data root is `C:\PRAYCG`, including `runs`, `analysis`,
`logs`, `study_workspaces`, `stimuli`, `protocol_assets`,
`protocol_design_drafts`, `config` and `research_exchange`. Those locations
are configurable in the application and are separate from the extracted
release folder.

Saved Control Center settings and the active-workspace pointer are under:

```text
%APPDATA%\PRAYCG_ControlCenter\
```

Locally installed protocol extensions are under:

```text
%LOCALAPPDATA%\PRAYCG\protocol_extensions\v1\
```

Do not run two Control Centers against the same workspace. Do not start a new
equipment session while an earlier runner or acquisition remains unresolved.

## External applications and publishers

PRAYCG coordinates external software but does not silently control all of it:

- **PsychoPy** runs supported visual/task protocol runners through the path
  selected in Settings.
- **LabRecorder** records XDF. The operator must select the required device
  outlets and PRAYCG marker stream, then start, stop and save the recording.
- **GazePoint Control** must already be running and the device calibrated there
  before the packaged GP3/GP3 HD connector uses the local API.
- **Pupil Core, Pupil Neon, OpenMuse and OpenViBE** remain external-publisher
  routes. Install and start the applicable publisher separately, then review
  and attach its exact live LSL outlet in PRAYCG.
- Device-specific USB, Bluetooth and vendor drivers remain external.

PRAYCG does not install, stop or upgrade an external publisher. Restarting a
publisher can change its LSL identity; re-review the new outlet in a fresh
equipment session rather than reusing a stale lock.

## Safe upgrade from an earlier release

1. Finish or explicitly finalize the active run. Save LabRecorder and stop all
   PRAYCG-owned connectors normally.
2. Close the old Control Center.
3. Back up the study folders, recordings, analysis outputs and reports under
   the configured PRAYCG data root.
4. Also preserve `%APPDATA%\PRAYCG_ControlCenter\` and
   `%LOCALAPPDATA%\PRAYCG\protocol_extensions\v1\` if you need settings and
   locally installed protocols for rollback.
5. Extract Alpha 10.2.1 into a new folder. Do not overwrite the old release.
6. Run `INSTALL.bat` in the new folder. Do not copy `.live-monitor-env` or
   `.hardware-connectors-env` from another location; Python virtual
   environments are not portable.
7. Start the new release, use **Use Bundled Paths**, and recheck PsychoPy,
   LabRecorder and any vendor-publisher paths.
8. Open the intended workspace and review its selected protocol, hardware
   profile, run identity and unresolved state before continuing.

The new Control Center rebases packaged tool paths to its own extraction while
preserving valid external-application choices. It does not rewrite completed
recordings into a new release. New code or input bindings can require a new QC
or analysis revision; preserve older receipts as history.

## Troubleshooting

### Python 3.11 was not found

Install native CPython 3.11 with Tcl/Tk support. Confirm one of these works in
a new terminal:

```text
py -3.11 -c "import sys, tkinter; print(sys.executable); print(sys.version)"
python -c "import sys, tkinter; print(sys.executable); print(sys.version)"
```

The printed version must begin with 3.11. The installer deliberately rejects
other Python versions. Do not try to use PsychoPy's bundled Python as the Core
installation target.

### A package download or installation failed

Keep the complete failing step and its installation-result JSON. Confirm the
computer can reach the configured Python package source, then rerun only the
affected mode. Proxy, certificate and institution-network policies are outside
the release and may require local administrator support.

Do not report a full install as successful merely because Core passed when an
optional component failed.

### Live Monitor is unavailable

Run:

```text
INSTALL.bat -Mode monitor
```

Its interpreter must be:

```text
app\.live-monitor-env\Scripts\python.exe
```

The Live Monitor is passive. It does not replace LabRecorder, own acquisition,
arm a session or prove that a stream is scientifically valid.

### A new managed hardware connector is unavailable

Run:

```text
INSTALL.bat -Mode hardware
```

Its interpreter must be:

```text
app\.hardware-connectors-env\Scripts\python.exe
```

Crown, Muse S Athena, Polar H10 ECG and GazePoint connector software remains
**experimental and bench-only pending physical validation**. A successful
install does not promote these routes to participant acquisition. Cerelog 16
remains withheld.

### An isolated environment appears damaged

First preserve the installation log and confirm that no Control Center,
monitor or connector process is running. A normal component repair is:

```text
INSTALL.bat -Mode monitor
INSTALL.bat -Mode hardware
```

If the environment's own Python executable is missing or unusable, rename only
the affected `.live-monitor-env` or `.hardware-connectors-env` directory to a
clearly labeled backup, then rerun its mode so the installer can create a new
one. Do not remove the whole application or any study directory as a repair
step.

### The application was moved after installation

Keep the release together, then reinstall both isolated components in their
new location:

```text
INSTALL.bat -Mode monitor
INSTALL.bat -Mode hardware
```

Start the application and use **Use Bundled Paths** again. Do not copy the old
virtual environments into the new folder.

### PsychoPy, LabRecorder or an external publisher is missing

Install or repair that application through its own supported distribution.
Then set its path in PRAYCG Settings or follow the exact external-publisher
route review. Running `INSTALL.bat` does not install those applications.

## Uninstall and manual-cleanup boundaries

Alpha 10.2.1 has no registry-based installer, Windows service or automatic
uninstaller. When no recording, runner, monitor or connector is active,
deleting the **specific extracted Alpha 10.2.1 release folder** removes the
application and its two release-local isolated environments.

That action does not remove:

- packages installed into the shared Core Python 3.11 interpreter;
- study data under `C:\PRAYCG` or another configured PRAYCG home;
- saved settings under `%APPDATA%\PRAYCG_ControlCenter`;
- installed protocol extensions, installation logs or environment records
  under `%LOCALAPPDATA%\PRAYCG`;
- optional offline-interpreter preferences under `%APPDATA%\PRAYCG`;
- protocol-builder exports under `%USERPROFILE%\Documents\PRAYCG_Custom_Protocols`;
  or
- PsychoPy, LabRecorder, vendor software or device drivers.

Do not issue a blanket `pip uninstall` against the Core interpreter: those
packages may be shared by unrelated software and the installer does not record
a safe pre-install rollback transaction. If the interpreter was dedicated to
PRAYCG, remove or rebuild that interpreter using Python's own maintenance tools
only after preserving any environments or projects that depend on it.

Treat every remaining data/configuration location as user data. Inspect and
back it up before manually removing anything. In particular, `C:\PRAYCG` can
contain raw XDF recordings, event evidence, hardware locks, analyses and
research bundles; uninstalling the application is not authorization to delete
those records.

## Installation boundaries specific to Alpha 10.2.1

- The release is not a complete offline Python distribution; dependencies are
  downloaded during installation.
- Software checks do not constitute a physical-device, timing, calibration or
  participant-safety test.
- Newly integrated Crown, Muse S Athena, Polar H10 ECG and GazePoint routes are
  limited to explicitly labeled experimental bench evaluation until physical
  evidence is completed.
- Pupil, OpenMuse and OpenViBE are external-publisher routes, not bundled
  third-party applications.
- Live Monitor is an observer/replay tool, not a recorder or closed-loop
  controller.
- Successful installation does not establish scientific validity,
  reproducibility on a second machine or suitability for clinical use.
