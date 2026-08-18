@echo off
cd /d %~dp0\..
call .venv\Scripts\activate
python scripts\praycg_identify_openbci_port_eeg_only_v1_0.py --watch
pause
