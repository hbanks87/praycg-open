@echo off
cd /d "%~dp0\.."
python scripts\praycg_openbci_brainflow_to_lsl_v1_2.py --confirmed-channel-map --stream-name obci_eeg1 --timestamp-mode reconstructed
pause
