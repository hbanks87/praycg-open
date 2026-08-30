@echo off
cd /d %~dp0\..
call .venv\Scripts\activate.bat
REM EDIT COM3 BELOW TO YOUR OPENBCI DONGLE PORT
python scripts\praycg_openbci_brainflow_als_pt19_bridge_v1_4.py --board cyton-daisy --serial-port COM3 --enable-analog-aux --publish-als-stream --confirmed-channel-map
pause
