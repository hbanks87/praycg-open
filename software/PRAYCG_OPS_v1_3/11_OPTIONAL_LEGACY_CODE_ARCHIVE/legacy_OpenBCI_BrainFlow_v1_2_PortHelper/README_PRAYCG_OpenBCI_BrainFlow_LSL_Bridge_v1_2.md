# PRAYCG OpenBCI BrainFlow-to-LSL Bridge v1.2 — Port Helper Edition

This package replaces the CPU-heavy OpenBCI GUI during PR-AYC-G acquisition:

```text
OpenBCI Cyton/Daisy -> BrainFlow serial reader -> LSL obci_eeg1 -> LabRecorder
```

## Why v1.2 exists

On a new Windows laptop, running the bridge without a serial port, for example:

```bash
python praycg_openbci_brainflow_to_lsl_v1_1.py
```

can fail because OpenBCI Cyton/Cyton-Daisy needs an explicit COM port, such as `COM3`.

v1.2 adds:

- serial-port identifier script
- `--list-ports`
- `--auto-port`
- interactive COM-port prompt if no port is supplied
- lightweight launcher GUI
- watchdog and XDF timing-grade verifier

## Install

From this folder:

```bash
pip install -r requirements_openbci_brainflow_lsl_v1_2.txt
```

## Step 1: close OpenBCI GUI

Only one program can usually own the OpenBCI COM port. Close OpenBCI GUI before running BrainFlow.

## Step 2: identify the port

```bash
python scripts\praycg_identify_openbci_port_v1_2.py
```

Or use before/after plug-in mode:

```bash
python scripts\praycg_identify_openbci_port_v1_2.py --watch
```

## Step 3: start the bridge

Manual port:

```bash
python scripts\praycg_openbci_brainflow_to_lsl_v1_2.py --board cyton-daisy --serial-port COM3 --stream-name obci_eeg1 --timestamp-mode reconstructed --confirmed-channel-map
```

Auto-port:

```bash
python scripts\praycg_openbci_brainflow_to_lsl_v1_2.py --auto-port --confirmed-channel-map
```

Interactive prompt:

```bash
python scripts\praycg_openbci_brainflow_to_lsl_v1_2.py
```

## Step 4: run the watchdog

```bash
python scripts\praycg_lsl_eeg_watchdog_v1_2.py --stream-name obci_eeg1 --duration 120 --expected-rate 125
```

## Step 5: record a short XDF and verify timing

```bash
python scripts\praycg_verify_xdf_eeg_timing_grade_v1_2.py path\to\test.xdf
```

## Common errors

### `--serial-port is required`

The bridge does not know which COM port is the OpenBCI dongle. Run the port identifier, then pass `--serial-port COMx`, or use `--auto-port`.

### `Access is denied`

Another program has the COM port open. Close OpenBCI GUI, Arduino serial monitor, vendor serial tools, and rerun.

### No COM port appears

Try a different USB port, wait 3–5 seconds after plugging in, check Windows Device Manager, or install the USB serial driver.

### Bridge starts but no LabRecorder stream

Run the watchdog first. Confirm `obci_eeg1` is visible through LSL before launching PR-AYC-G.
