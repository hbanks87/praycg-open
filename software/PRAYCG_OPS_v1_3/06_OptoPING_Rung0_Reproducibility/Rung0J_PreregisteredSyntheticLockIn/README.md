# OSM / Opto-PING Rung 0J - Preregistered Synthetic Lock-In Pack

This package freezes the Rung 0I ridge-reduction design and reruns it on a fresh seed set without modifying the design.

## Main files

- `locked_protocol/LOCKED_SPEC_OSM_OptoPING_Rung0J_v0_1.json`
- `locked_protocol/LOCKED_SPEC_SHA256.txt`
- `locked_protocol/LOCKED_PROTOCOL.md`
- `scripts/run_osm_opto_ping_rung0j_preregistered_lockin_v0_1.py`
- `tables/rung0j_trial_results.csv`
- `tables/rung0j_pass_summary.json`
- `report/OSM_OptoPING_Rung0J_PreregisteredSyntheticLockIn_Report_v0_1.pdf`

## Reproduce

```bash
pip install -r requirements.txt
python scripts/run_osm_opto_ping_rung0j_preregistered_lockin_v0_1.py --out-dir reproduced_rung0j
```

The locked spec hash is:

`d93f6146e4e77ffeffbdd5c133250fd6d474317d8af6c34c3354dd6b28756282`

The run is synthetic only. It is a parameter-identifiability test, not biological proof.
