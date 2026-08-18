@echo off
setlocal
mkdir reproduced_outputs
python run_osm_opto_ping_rung0j_preregistered_lockin_v0_1.py --out-dir reproduced_outputs
python ..\07_UTILITIES\verify_external_rung0j_results.py reproduced_outputs
pause
