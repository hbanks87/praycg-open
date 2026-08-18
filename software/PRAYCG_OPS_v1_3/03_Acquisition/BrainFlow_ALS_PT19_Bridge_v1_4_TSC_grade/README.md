# PRAYCG OpenBCI BrainFlow ALS-PT19 Bridge v1.4

This package replaces the OpenBCI GUI networking layer when the GUI will only export one LSL stream at a time.

It creates simultaneous LSL streams from one BrainFlow session:

```text
obci_eeg1              EEG, 16 channels for Cyton+Daisy
OpenBCIAnalogAux       raw analog AUX, 3 channels: A5/D11, A6/D12, A7/D13
ALS_PT19_Timing        single extracted light sensor channel, default A6/D12
OpenBCIStatusMarkers   status / heartbeat markers
```

Do not run OpenBCI GUI at the same time. BrainFlow needs exclusive control of the OpenBCI COM port.

## KISS wiring

```text
ALS-PT19 +      -> Cyton DVDD / 3V3
ALS-PT19 -      -> Cyton GND
ALS-PT19 OUT    -> Cyton D12 / A6
```

Default ALS channel in the script:

```text
--als-aux-channel 1
```

because the analog channels are:

```text
0 = A5 / D11
1 = A6 / D12  <- ALS-PT19 default
2 = A7 / D13
```

## Windows installation, reliable path

Use a normal Python install rather than the Microsoft Store Python. Python 3.11 or 3.12 is recommended for the least package friction.

Unzip this folder somewhere simple:

```text
C:\PRAYCG\BrainFlow_ALS_v1_4\
```

Open **Command Prompt** in that folder.

Create a virtual environment:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements_brainflow_als_pt19_v1_4.txt
python scripts\praycg_check_brainflow_install_v1_4.py
```

If `py -3.11` is not found, install Python 3.11 or 3.12 from python.org and check **Add Python to PATH**.

## Find the COM port

Close OpenBCI GUI first.

```bat
python scripts\praycg_identify_openbci_port_v1_4.py --watch
```

Unplug the dongle, press Enter, plug the dongle back into the USB port you intend to use, wait a few seconds, and press Enter. Use the COM port that appears.

You can also simply list ports:

```bat
python scripts\praycg_openbci_brainflow_als_pt19_bridge_v1_4.py --list-ports
```

## Start the EEG + ALS bridge

Replace `COM3` with your actual COM port:

```bat
python scripts\praycg_openbci_brainflow_als_pt19_bridge_v1_4.py ^
  --board cyton-daisy ^
  --serial-port COM3 ^
  --enable-analog-aux ^
  --publish-als-stream ^
  --confirmed-channel-map
```

The script sends `/2` to the Cyton to enter analog board mode. On exit it tries to send `/0` to restore default mode.

## Confirm LSL streams

In a second Command Prompt with the same venv activated:

```bat
python scripts\praycg_list_lsl_streams_v1_4.py
```

Expected streams:

```text
obci_eeg1
OpenBCIAnalogAux
ALS_PT19_Timing
OpenBCIStatusMarkers
```

## ALS bench test

Start LabRecorder and select at least:

```text
obci_eeg1
OpenBCIAnalogAux
ALS_PT19_Timing
OpenBCIStatusMarkers
StasisMarkers
PolarHRV
VernierRespirationBelt
```

Then run the ALS watchdog in a second terminal:

```bat
python scripts\praycg_als_pt19_light_watchdog_v1_4.py --duration 30 --expected-pulses 1
```

Play the first 10 seconds of the Target video while it records. The ALS pulse should rise for about one second and return to baseline.

## If the bridge fails to open the port

Almost always this means something else owns the serial port.

Close:

```text
OpenBCI GUI
Arduino serial monitor
old BrainFlow terminal windows
PuTTY / serial tools
```

Then unplug/replug the dongle and rerun the port identifier.

## If ALS stream is flat

Check in this order:

```text
1. ALS OUT really goes to D12/A6.
2. ALS + is on DVDD/3V3, not 5V.
3. ALS - is on GND.
4. The timing square is actually visible under the sensor.
5. The sensor is covered/shrouded from room light.
6. --enable-analog-aux was included.
7. --als-aux-channel is 1 for D12/A6.
```

## Interpretation boundary

The ALS stream is not a brain signal. It validates physical monitor timing. It belongs to the external input vector `u(t)`, not to any biological hidden variable `Y(t)`.
