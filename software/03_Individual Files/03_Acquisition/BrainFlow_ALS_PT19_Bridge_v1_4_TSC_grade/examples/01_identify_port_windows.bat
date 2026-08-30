@echo off
cd /d %~dp0\..
call .venv\Scripts\activate.bat
python scripts\praycg_identify_openbci_port_v1_4.py --watch
pause
