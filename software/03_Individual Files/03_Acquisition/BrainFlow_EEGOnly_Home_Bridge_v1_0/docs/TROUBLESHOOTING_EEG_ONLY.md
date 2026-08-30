# Troubleshooting - EEG-Only BrainFlow Bridge

## Error: `--serial-port is required`

Run the port finder:

```bat
python scripts\praycg_identify_openbci_port_eeg_only_v1_0.py --watch
```

Then pass the resulting COM port:

```bat
python scripts\praycg_openbci_brainflow_eeg_to_lsl_v1_0.py --board cyton-daisy --serial-port COM3
```

## Error: COM port busy

Close:

```text
OpenBCI GUI
older BrainFlow terminals
other Python bridge scripts
Arduino serial monitor
```

Only one program can own the OpenBCI serial port.

## LabRecorder does not show `obci_eeg1`

1. Confirm the bridge terminal says `LSL_EEG_OUTLET_ONLINE`.
2. Run:

```bat
python scripts\praycg_list_lsl_streams_v1_0.py
```

3. Restart LabRecorder after the stream is already running.

## Stream appears but data are poor

This script only transports the data. Check:

```text
battery
USB dongle location
OpenBCI board power
electrode contact
ground/reference clips
channel map
radio packet quality
motion/jaw/eye artifact
```

## Need photodiode / ALS timing

Use the ALS-enabled bridge instead. This EEG-only public-home bridge intentionally does not publish physical display timing.
