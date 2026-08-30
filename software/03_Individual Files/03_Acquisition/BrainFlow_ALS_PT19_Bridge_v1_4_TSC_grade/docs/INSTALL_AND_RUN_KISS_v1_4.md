# Install and Run KISS Guide — PRAYCG BrainFlow ALS v1.4

## 1. Do not open OpenBCI GUI

The OpenBCI GUI and BrainFlow both want the same COM port. Use one or the other, never both.

## 2. Recommended Windows install

```bat
cd C:\PRAYCG\BrainFlow_ALS_v1_4
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements_brainflow_als_pt19_v1_4.txt
python scripts\praycg_check_brainflow_install_v1_4.py
```

If Python 3.11 is unavailable, try:

```bat
py -3.12 -m venv .venv
```

## 3. Identify OpenBCI port

```bat
python scripts\praycg_identify_openbci_port_v1_4.py --watch
```

## 4. Start bridge

```bat
python scripts\praycg_openbci_brainflow_als_pt19_bridge_v1_4.py --board cyton-daisy --serial-port COM3 --enable-analog-aux --publish-als-stream --confirmed-channel-map
```

## 5. Confirm visible LSL streams

```bat
python scripts\praycg_list_lsl_streams_v1_4.py
```

## 6. Record in LabRecorder

Select these streams:

```text
obci_eeg1
OpenBCIAnalogAux
ALS_PT19_Timing
OpenBCIStatusMarkers
StasisMarkers
PolarHRV
VernierRespirationBelt
```

## 7. ALS pulse check

```bat
python scripts\praycg_als_pt19_light_watchdog_v1_4.py --duration 30 --expected-pulses 1
```

Play the Target video. Confirm a strong one-second rise and return to baseline.
