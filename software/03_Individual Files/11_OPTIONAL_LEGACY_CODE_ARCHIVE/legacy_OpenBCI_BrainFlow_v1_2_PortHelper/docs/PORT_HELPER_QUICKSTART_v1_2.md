# Port Helper Quickstart v1.2

1. Plug the OpenBCI dongle into the USB port you plan to use.
2. Turn on the Cyton/Daisy board.
3. Close OpenBCI GUI.
4. Run:

```bash
python scripts\praycg_identify_openbci_port_v1_2.py --watch
```

5. Use the COM port that appears after plugging in the dongle.
6. Start the bridge:

```bash
python scripts\praycg_openbci_brainflow_to_lsl_v1_2.py --board cyton-daisy --serial-port COM3 --stream-name obci_eeg1 --timestamp-mode reconstructed --confirmed-channel-map
```

7. In a second terminal, run:

```bash
python scripts\praycg_lsl_eeg_watchdog_v1_2.py --stream-name obci_eeg1 --duration 120 --expected-rate 125
```

A good result should report a PASS, around 15,000 samples over 120 seconds, and an effective rate near 125 Hz.
