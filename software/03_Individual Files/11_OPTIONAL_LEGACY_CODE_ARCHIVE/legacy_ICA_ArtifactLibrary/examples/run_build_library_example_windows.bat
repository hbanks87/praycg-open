@echo off
REM Edit paths before use.
python scripts\praycg_build_ica_library.py artifact_control_run.xdf ^
  --out outputs\ica_artifact_library_hoyt ^
  --channel-map config\openbci_16_default_montage.csv ^
  --make-figures ^
  --overwrite
pause
