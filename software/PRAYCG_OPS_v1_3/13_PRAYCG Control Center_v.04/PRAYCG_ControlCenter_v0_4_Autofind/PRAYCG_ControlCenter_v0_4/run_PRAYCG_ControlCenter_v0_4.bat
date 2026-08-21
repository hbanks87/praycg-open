@echo off
setlocal
cd /d "%~dp0"
py -3.11 scripts\praycg_control_center_v0_4.py
if errorlevel 1 (
  echo.
  echo PRAYCG Control Center exited with an error.
  pause
)
