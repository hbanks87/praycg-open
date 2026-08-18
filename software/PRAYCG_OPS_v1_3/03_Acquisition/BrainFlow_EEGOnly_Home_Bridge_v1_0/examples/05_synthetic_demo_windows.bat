@echo off
cd /d %~dp0\..
call .venv\Scripts\activate
python scripts\praycg_openbci_brainflow_eeg_to_lsl_v1_0.py --board synthetic --stream-name obci_eeg1 --duration 30
pause
