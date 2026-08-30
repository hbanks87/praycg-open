@echo off
cd /d "%~dp0\.."
python scripts\praycg_identify_openbci_port_v1_2.py --watch
pause
