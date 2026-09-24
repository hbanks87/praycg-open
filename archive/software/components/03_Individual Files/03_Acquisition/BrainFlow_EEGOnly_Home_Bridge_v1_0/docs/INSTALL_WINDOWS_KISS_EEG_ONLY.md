# Install Windows - KISS EEG-Only Bridge

1. Install Python 3.11 or 3.12.
2. Unzip this folder to a short path, for example:

```text
C:\PRAYCG\PRAYCG_BrainFlow_EEGOnly_LSL_Bridge_v1_0
```

3. Open Command Prompt in that folder.

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements_brainflow_eeg_only_v1_0.txt
python scripts\praycg_check_install_eeg_only_v1_0.py
```

4. Find the COM port:

```bat
python scripts\praycg_identify_openbci_port_eeg_only_v1_0.py --watch
```

5. Start the bridge:

```bat
python scripts\praycg_openbci_brainflow_eeg_to_lsl_v1_0.py --board cyton-daisy --serial-port COM3 --confirmed-channel-map
```

6. Open LabRecorder and select `obci_eeg1`.

Do not run the OpenBCI GUI and this BrainFlow bridge at the same time.
