# PRAYCG BrainFlow EEG-Only LSL Bridge v1.0

A simple public-home acquisition bridge for PR-AYC-G users who want OpenBCI EEG streaming through BrainFlow without ALS-PT19 / photodiode timing setup.

## What it streams

```text
obci_eeg1
  EEG stream from OpenBCI Cyton or Cyton+Daisy

OpenBCIStatusMarkers
  bridge status / heartbeat markers
```

## What it deliberately does not stream

```text
ALS_PT19_Timing
OpenBCIAnalogAux
photodiode / light-sensor timing
Cyton analog AUX mode
```

This is the KISS home version. It is useful for getting people started, teaching the protocol, and collecting lower-burden pilot data. It is not the full metrological version of PR-AYC-G.

## Install on Windows

Use Python 3.11 or 3.12.

```bat
cd C:\PRAYCG\PRAYCG_BrainFlow_EEGOnly_LSL_Bridge_v1_0
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements_brainflow_eeg_only_v1_0.txt
python scripts\praycg_check_install_eeg_only_v1_0.py
```

If `py -3.11` is not available, use:

```bat
py -3.12 -m venv .venv
```

## Find the OpenBCI COM port

Close the OpenBCI GUI first. Only one program can own the OpenBCI serial port at a time.

```bat
python scripts\praycg_identify_openbci_port_eeg_only_v1_0.py --watch
```

## Run with Cyton+Daisy

Replace `COM3` with your actual port.

```bat
python scripts\praycg_openbci_brainflow_eeg_to_lsl_v1_0.py ^
  --board cyton-daisy ^
  --serial-port COM3 ^
  --stream-name obci_eeg1 ^
  --confirmed-channel-map ^
  --stats-json logs\eegonly_stats.json
```

## Run with plain Cyton

```bat
python scripts\praycg_openbci_brainflow_eeg_to_lsl_v1_0.py ^
  --board cyton ^
  --serial-port COM3 ^
  --stream-name obci_eeg1
```

## Test with synthetic board

```bat
python scripts\praycg_openbci_brainflow_eeg_to_lsl_v1_0.py ^
  --board synthetic ^
  --stream-name obci_eeg1 ^
  --duration 30
```

## Confirm LSL streams

In another terminal:

```bat
python scripts\praycg_list_lsl_streams_v1_0.py
```

Expected:

```text
obci_eeg1
OpenBCIStatusMarkers
```

## Watchdog test

```bat
python scripts\praycg_eeg_lsl_watchdog_v1_0.py --stream-name obci_eeg1 --duration 120
```

## LabRecorder

Select at least:

```text
obci_eeg1
OpenBCIStatusMarkers
StasisMarkers
PolarHRV, if used
VernierRespirationBelt, if used
```

## Boundary

This EEG-only bridge is a lower-burden acquisition route. It does not physically validate screen onset. The ALS-enabled bridge remains the recommended path for timing-critical TSC-grade runs.
