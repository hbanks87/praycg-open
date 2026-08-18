@echo off
cd /d "%~dp0\.."
python scripts\praycg_lsl_eeg_watchdog_v1_2.py --stream-name obci_eeg1 --duration 120 --expected-rate 125
pause
