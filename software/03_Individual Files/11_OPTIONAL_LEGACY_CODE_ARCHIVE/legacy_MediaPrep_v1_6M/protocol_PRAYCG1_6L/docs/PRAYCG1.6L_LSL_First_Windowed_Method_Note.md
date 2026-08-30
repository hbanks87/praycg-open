# PRAYCG1.6L LSL-First Windowed Preflight Method Note

The marker stream must exist before LabRecorder starts recording. PRAYCG1.6L therefore creates `StasisMarkers` after configuration and before any fullscreen experiment window. The operator is held in a non-fullscreen preflight screen while preflight ping markers are broadcast.

The design goal is simple: make it physically possible for the operator to click LabRecorder **Update** and **Start** while `StasisMarkers` is already alive.

This does not replace final XDF verification. The definitive test is whether the XDF contains `StasisMarkers` after recording.

## Recommended censoring markers preserved

PRAYCG1.6L preserves the report and sum input markers from 1.6J/1.6K:

- `REPORT_INPUT_START`
- `REPORT_INPUT_END`
- `SUM_INPUT_START`
- `SUM_INPUT_END`
- `RETURN_TO_STILLNESS_START`
- `RETURN_TO_STILLNESS_END`

These windows should be excluded from EEG spectral, PLV, PAC, GammaScalpel, and PNCC analyses, with preregistered pre/post padding.
