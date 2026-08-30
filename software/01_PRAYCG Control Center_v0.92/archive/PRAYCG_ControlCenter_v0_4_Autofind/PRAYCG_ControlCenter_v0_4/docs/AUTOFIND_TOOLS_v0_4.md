# PRAYCG Control Center v0.4 Auto-Find Tools

v0.4 adds auto-find buttons for the common external tools that users struggled to configure manually:

- LabRecorder executable
- PsychoPy application / PsychoPy Coder launcher
- PsychoPy-bundled Python when discoverable
- PRAYCG2.0 runner script

## Where the buttons are

Open the Control Center and go to:

```text
Settings -> Auto-find common external tools v0.4
```

Buttons:

```text
Auto-find ALL
Find LabRecorder
Find PsychoPy
Find PRAYCG2.0 Runner
```

The Runner / PsychoPy tab also has:

```text
Auto-find PsychoPy / LabRecorder / Runner
```

## What it searches

The auto-finder searches bounded, common locations rather than sweeping the entire C: drive:

```text
PRAYCG_HOME
Stimulus root
Run root
Control Center package folder
Desktop
Downloads
Documents
Program Files
Program Files (x86)
LOCALAPPDATA
APPDATA
C:\PRAYCG
C:\LabRecorder
C:\PsychoPy
```

It also checks the system PATH for `LabRecorder`, `LabRecorder.exe`, `psychopy`, and `psychopy.exe`.

## Important limits

Auto-find is a convenience feature, not proof that a tool will launch correctly. Review the Settings tab after running it. If the runner only works from PsychoPy Coder on your system, keep the runner mode set to:

```text
Open PsychoPy Coder + runner file/folder
```

This is still the recommended public-safe launch mode.

## Logs

Every auto-find run writes a JSON report into:

```text
<PRAYCG_HOME>/logs/control_center/autofind/
```
