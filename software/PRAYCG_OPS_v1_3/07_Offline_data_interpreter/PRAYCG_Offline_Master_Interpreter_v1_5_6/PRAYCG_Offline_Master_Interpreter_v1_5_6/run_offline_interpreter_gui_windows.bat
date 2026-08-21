@echo off
setlocal
cd /d "%~dp0"
py -3.11 -m pip install -r requirements.txt
py -3.11 scripts\praycg_offline_interpretive_report_gui_v1_5_6.py
pause
