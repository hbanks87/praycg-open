@echo off
cd /d %~dp0\..
call .venv\Scripts\activate.bat
python scripts\praycg_list_lsl_streams_v1_4.py
pause
