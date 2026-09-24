# Standalone usage

The offline interpreter expects a Master Comprehensive Suite analysis output folder. It recursively searches for known CSV and JSON result tables.

## GUI

```bat
run_offline_interpreter_gui_windows.bat
```

## Command line

```bat
py -3.11 scripts\praycg_offline_interpretive_report_generator_v1_5_6.py ^
  --analysis-folder "C:\PRAYCG\analysis\MyRun_MasterComprehensive" ^
  --run-label "MyRun" ^
  --auto-run-mred-peak-resolution
```

The output will be written under:

```text
<analysis-folder>\reports\offline_interpretation\
```
