@echo off
cd /d %~dp0\..
call .venv\Scripts\activate
python scripts\praycg_eeg_lsl_watchdog_v1_0.py --stream-name obci_eeg1 --duration 120
pause
