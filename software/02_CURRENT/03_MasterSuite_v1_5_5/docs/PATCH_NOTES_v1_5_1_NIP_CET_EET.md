# PRAYCG Unified Master Suite v1.5.1 - NIP/CET/EET Patch

Adds the Narrative Immersion Proxy family and cinematic entrainment/echo tracking modules.

## Modules

- NIP_v0.1 - Narrative Immersion Proxy: macroscopic attention + integration proxy.
- BIT_v0.1 - Bivariate Immersion Threshold: event-level AND-gate requiring meaning recognition and integration.
- CII_v0.1 - Continuous Immersion Index: mean NIP density inside predeclared/annotation windows.
- IAQ_v0.1 - Immersion Attenuation Quotient: Target-vs-Override attenuation of CII.
- CET_EET_v0.1 - Cinematic Entrainment and Endogenous Echo Tracking.

## Boundary

These modules do not measure dopamine, oxytocin, OSM biology, microtubules, biophotons, consciousness, or hidden cellular Y. They are macroscopic PRAYCG proxy layers.

## Minimal command

```bat
python scripts\praycg_nip_cet_eet_modules_v1_5_1.py ^
  --feature-csv "C:\path\to\feature_frame.csv" ^
  --event-csv "C:\path\to\candidate_local_kht_topo_mred_event_table.csv" ^
  --annotation-csv "C:\path\to\annotation_windows.csv" ^
  --cue-schedule-json "C:\path\to\cue_schedule.json" ^
  --out-dir "C:\path\to\analysis_output"
```

Use `--stimulus-video-proxy` only when a lawful local stimulus or visualizer proxy MP4 is available.
