@echo off
cd /d %~dp0\..
py -3.11 -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements_brainflow_als_pt19_v1_4.txt
python scripts\praycg_check_brainflow_install_v1_4.py
pause
