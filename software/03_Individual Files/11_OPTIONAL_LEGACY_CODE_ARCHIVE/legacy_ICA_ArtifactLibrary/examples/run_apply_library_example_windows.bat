@echo off
REM Edit paths before use.
python scripts\praycg_apply_ica_library.py praycg_run.xdf ^
  --library outputs\ica_artifact_library_hoyt ^
  --out outputs\praycg_run_ica_reference ^
  --channel-map config\openbci_16_default_montage.csv ^
  --make-figures
pause
