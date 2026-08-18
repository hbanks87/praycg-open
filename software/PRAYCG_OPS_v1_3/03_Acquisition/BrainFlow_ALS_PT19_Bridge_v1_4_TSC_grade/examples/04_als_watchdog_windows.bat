@echo off
cd /d %~dp0\..
call .venv\Scripts\activate.bat
python scripts\praycg_als_pt19_light_watchdog_v1_4.py --duration 30 --expected-pulses 1
pause
