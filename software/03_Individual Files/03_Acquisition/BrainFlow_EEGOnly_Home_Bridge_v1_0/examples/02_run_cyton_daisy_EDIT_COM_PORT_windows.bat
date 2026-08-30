@echo off
cd /d %~dp0\..
call .venv\Scripts\activate
REM EDIT COM3 BELOW TO MATCH YOUR OPENBCI DONGLE PORT
python scripts\praycg_openbci_brainflow_eeg_to_lsl_v1_0.py ^
  --board cyton-daisy ^
  --serial-port COM3 ^
  --stream-name obci_eeg1 ^
  --confirmed-channel-map ^
  --stats-json logs\eegonly_stats.json
pause
