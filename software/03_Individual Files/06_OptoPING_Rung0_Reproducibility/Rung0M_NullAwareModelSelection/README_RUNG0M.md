# OSM / Opto-PING Rung 0M - Null-Aware Model Selection v0.1

This package contains the Rung 0M synthetic specificity gate. It extends Rung 0L by adding:

- generator-specific null pass/fail thresholds;
- stronger model penalties and improved null alternatives;
- null-calibrated K significance using shuffled, permuted, and time-reversed controls;
- a simultaneous-lock rule: the full reciprocal model must win prediction and K must lock;
- permutation/shuffled-label/time-reversed null logic;
- an explicit doctrine that full-model prediction alone is not enough.

Overall result: `PARTIAL_OR_FAILED_NULL_AWARE_SPECIFICITY`.

Boundary: synthetic sensitivity/specificity calibration only. This does not prove or disprove biological OSM, PR-AYC-G human data, microtubular memory, biophotonic flickering, or human EEG mechanism.
