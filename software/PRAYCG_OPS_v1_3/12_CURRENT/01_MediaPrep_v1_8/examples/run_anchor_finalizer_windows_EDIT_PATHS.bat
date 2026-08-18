@echo off
cd /d "%~dp0.."
py -3.11 scripts\praycg_anchor_lock_finalizer_v1_7A.py ^
  --draft "C:\PRAYCG\stimuli\Contact\predeclared_anchors_Contact_v1_8_DRAFT.json"
pause
