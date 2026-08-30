@echo off
cd /d %~dp0\..
py -3.11 -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements_brainflow_eeg_only_v1_0.txt
python scripts\praycg_check_install_eeg_only_v1_0.py
pause
