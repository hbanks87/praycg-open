# OSM / Opto-PING Rung 0K - External Reproducibility Handoff Pack v0.1

This package converts Rung 0J from an internal preregistered synthetic pass into an external reproducibility handoff.

## What is frozen

Do not edit:

- `01_LOCKED_PROTOCOL_DO_NOT_EDIT/LOCKED_SPEC_OSM_OptoPING_Rung0J_v0_1.json`
- `01_LOCKED_PROTOCOL_DO_NOT_EDIT/LOCKED_SPEC_SHA256.txt`
- `02_REPRODUCTION_SCRIPT/run_osm_opto_ping_rung0j_preregistered_lockin_v0_1.py`
- the seed policy
- the alternative models
- the pass/fail criteria
- the reporting template

Locked spec SHA-256:

```text
d93f6146e4e77ffeffbdd5c133250fd6d474317d8af6c34c3354dd6b28756282
```

## What I could and could not do here

I performed an internal clean-room replay by extracting the locked Rung 0J package into a fresh directory and running the frozen script without changing the design. That is not a true external reproduction by another person on another machine. It is a dry-run confirming that the handoff package executes and reproduces the locked metrics in this environment.

A true Rung 0K external reproduction requires another machine or person to run the same files without modifying the locked spec.

## How an external reproducer should run it

1. Install Python 3.10+.
2. Install requirements:

```bash
pip install -r 02_REPRODUCTION_SCRIPT/requirements.txt
```

3. Change into `02_REPRODUCTION_SCRIPT/`.
4. Run:

```bash
python run_osm_opto_ping_rung0j_preregistered_lockin_v0_1.py --out-dir reproduced_outputs
```

5. Verify:

```bash
python ../07_UTILITIES/verify_external_rung0j_results.py reproduced_outputs
```

Windows users may double-click:

```text
02_REPRODUCTION_SCRIPT/RUN_EXTERNAL_REPRODUCTION_WINDOWS.bat
```

## Pass rule

The reproduction passes if:

- locked spec hash matches `d93f6146e4e77ffeffbdd5c133250fd6d474317d8af6c34c3354dd6b28756282`
- n = 60 trials
- K within 15% in at least 90% of trials
- median K error <= 10%
- K within 10% in at least 80% of trials
- directional eta/zeta within 20% in at least 80% of trials
- full reciprocal model wins at least 80% of held-out perturbation-family CV folds

## Boundary

This is synthetic identifiability only. It does not prove OSM, microtubular memory, LTP, dendritic spine growth, quantum memory, or human EEG mechanism.
