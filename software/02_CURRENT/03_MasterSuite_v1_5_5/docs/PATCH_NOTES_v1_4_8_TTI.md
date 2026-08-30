# PRAYCG Unified Master Suite v1.4.8 - TTI Patch Notes

## Added

- `praycg_tti_reception_extraction_module_v1_4_8.py`
- `TTI_v0.1_Reception_Extraction_Tradeoff.md`
- Visualizer overlay support for:
  - `tti_visual_overlay.csv`
  - `thermodynamic_theft_visual_overlay.csv`
- Unified launcher flag:
  - `--run-tti-modules`

## Purpose

This patch formalizes the Reception-Extraction Tradeoff and Thermodynamic Theft Index (TTI): a bounded, exploratory module for comparing natural Target reception against Contextual Override extraction.

## Boundary

TTI is not a moral score, clinical score, or proof of consciousness or OSM biology. It estimates whether Target preserved more receptive meaning/integration while Override diverted cognitive/autonomic work into extraction.

## Example

```bat
python scripts\praycg_unified_master_analysis_visualizer_v1_4.py ^
  --mode analysis_only ^
  --project-name Contact_Run1_TTI ^
  --xdf "C:\path\to\run.xdf" ^
  --event-log "C:\path\to\events.json" ^
  --cue-schedule-json "C:\path\to\cue_schedule.json" ^
  --out-root "C:\PRAYCG\outputs" ^
  --run-tti-modules ^
  --overwrite
```
