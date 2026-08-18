@echo off
REM This launcher opens the GUI. Select your media files and choose templates\Her_media_structural_anchors_v1_8B.json in the anchor field.
cd /d "%~dp0\.."
python scripts\run_PRAYCG1_8B_PredeclaredAnchors.py
pause
