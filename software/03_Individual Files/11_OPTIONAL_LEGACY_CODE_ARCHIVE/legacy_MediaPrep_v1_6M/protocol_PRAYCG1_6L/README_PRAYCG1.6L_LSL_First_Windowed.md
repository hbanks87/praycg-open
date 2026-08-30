# PRAYCG1.6L — LSL-First Windowed Preflight Runner

This runner patches the usability problem in PRAYCG1.6K: the LSL marker stream came online before LabRecorder, but the preflight hold could appear in fullscreen and trap the operator away from LabRecorder.

PRAYCG1.6L keeps the LabRecorder preflight as a normal window. Fullscreen begins only after LabRecorder is recording.

## Required run order

1. Start OpenBCI / Polar / Vernier LSL streams.
2. Launch `run_PRAYCG1_6L_LSL_First_Windowed.py` from PsychoPy Coder or a PsychoPy terminal.
3. Fill out the configuration dialog and press OK.
4. The script creates `StasisMarkers` and shows a windowed preflight screen.
5. Open LabRecorder or Alt-Tab to it.
6. Click **Update**.
7. Confirm `StasisMarkers`, `obci_eeg1`, and any Polar/Vernier streams are visible and checked.
8. Click **Start** in LabRecorder.
9. Return to the PRAYCG preflight window.
10. Right-click the PRAYCG preflight window to begin the experiment.
11. The script closes the windowed preflight and opens the fullscreen experiment window.

## Why this matters

LabRecorder generally records the streams that are visible and selected when recording starts. If the marker outlet is created after LabRecorder has already started, the local event CSV/JSON can look complete while the final XDF contains no marker stream.

The preflight ping markers are intentionally sent before acquisition:

- `LSL_PREFLIGHT_HOLD_START`
- `LSL_PREFLIGHT_PING_001`, `LSL_PREFLIGHT_PING_002`, etc.
- `LSL_PREFLIGHT_HOLD_END`

If these markers do not appear in the final XDF, do not run a real PRAYCG session yet.

## Verification

First run a smoke test:

```bash
python scripts/lsl_stasismarkers_smoke_test.py
```

Record 20-30 seconds in LabRecorder, then verify the XDF:

```bash
python scripts/verify_xdf_stasis_markers.py path/to/test.xdf
```

Proceed only after the verifier reports that a marker stream is present.

## Files

- `scripts/run_PRAYCG1_6L_LSL_First_Windowed.py` — main runner.
- `scripts/run_praycg_v1_6L.py` — lowercase alias.
- `scripts/lsl_stasismarkers_smoke_test.py` — marker smoke test.
- `scripts/verify_xdf_stasis_markers.py` — final XDF verification tool.
