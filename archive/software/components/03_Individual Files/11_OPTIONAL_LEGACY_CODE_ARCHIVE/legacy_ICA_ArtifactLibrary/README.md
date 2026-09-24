# PR-AYC-G ICA Artifact Library Tools

This package creates a subject-specific artifact reference library for PR-AYC-G EEG runs.

The purpose is not to prove a physiological claim. The purpose is to make artifacts less mysterious.
You intentionally record blinks, jaw tension, neck movement, shoulder movement, swallowing, breathing artifacts, clean stillness, and silent task states while dropping precise LSL markers. Then you fit ICA to that control run and build a reference library of event-locked artifact component candidates.

## Files

```text
scripts/praycg_ica_control_run.py
  PsychoPy + LSL control-run script. Run this while OpenBCI and LabRecorder are recording.

scripts/praycg_build_ica_library.py
  Builds the ICA library from artifact-control XDF files.

scripts/praycg_apply_ica_library.py
  Fits ICA to a PR-AYC-G run and scores its components against the artifact library. Report-only by default.

scripts/praycg_ica_common.py
  Shared loading, QC, marker parsing, ICA feature extraction, and template utilities.

config/artifact_event_plan.csv
  The artifact protocol schedule. Edit repetitions/durations here.

config/openbci_16_default_montage.csv
  Default 16-channel montage map. Edit this to match your actual OpenBCI wiring before serious use.

config/ica_label_rules.json
  Heuristic interpretation guide and prohibited claims.
```

## Installation

Use a normal Python/MNE environment for analysis scripts:

```bash
pip install -r requirements_ica.txt
```

For `praycg_ica_control_run.py`, run inside PsychoPy Standalone/Coder or install PsychoPy in your Python environment. If running inside PsychoPy Standalone, install `pylsl` in PsychoPy's internal Python environment first.

## Run order

### 1. Record the artifact library XDF

Start OpenBCI EEG LSL stream. Open LabRecorder. Then run:

```bash
python scripts/praycg_ica_control_run.py
```

LabRecorder should record:

```text
obci_eeg1
ICAArtifactMarkers
optional: PolarHRV
optional: VernierRespirationBelt
optional: PolarECG
```

### 2. Build the ICA library

```bash
python scripts/praycg_build_ica_library.py artifact_control_run.xdf \
  --out outputs/ica_artifact_library_hoyt \
  --channel-map config/openbci_16_default_montage.csv \
  --make-figures \
  --overwrite
```

### 3. Reference the library against a PR-AYC-G run

```bash
python scripts/praycg_apply_ica_library.py praycg_run.xdf \
  --library outputs/ica_artifact_library_hoyt \
  --out outputs/praycg_run_ica_reference \
  --channel-map config/openbci_16_default_montage.csv \
  --make-figures
```

Default behavior is report-only. It writes candidate artifact components but does not remove them.

To auto-clean only after you trust the library and threshold:

```bash
python scripts/praycg_apply_ica_library.py praycg_run.xdf \
  --library outputs/ica_artifact_library_hoyt \
  --out outputs/praycg_run_ica_reference \
  --channel-map config/openbci_16_default_montage.csv \
  --auto-clean
```

## Critical boundary

ICA is not a truth machine. It is a spatial-statistical decomposition. With 16-channel OpenBCI data, it can help identify strong blink, jaw, neck, shoulder, and contact components, but it cannot guarantee that remaining 30-45 Hz activity is cortical.

Use this library for:

```text
artifact inspection
component ranking
artifact-matched windowing
manual exclusion support
future preregistration
```

Do not use it to claim:

```text
artifact-proof low-gamma payload
proof of meaning
proof of consciousness
proof of an optical or molecular mechanism
```

