# PRAYCG v1.6S ALS Fullscreen Start-Pulse QC Checklist

## Hardware placement
- Place the ALS-PT19 anywhere on the active display area where the full-screen white pulse is visible.
- Use black electrical tape / opaque shroud to reduce room-light leakage if practical.
- Confirm the ALS stream is recorded as `ALS_PT19_Timing` or inside `OpenBCIAnalogAux`.

## Required test before real run
1. Start the BrainFlow ALS bridge and LabRecorder.
2. Play the first 10 seconds of Control, Target, and Contextual Override.
3. Confirm the black settle screen -> full-screen white pulse -> black guard -> content pattern is visible in the ALS trace.
4. Confirm no branch misses the start pulse.

## Pass criteria
- Clear high-amplitude ALS rise during full-screen white pulse.
- Return to baseline during black guard.
- No full-duration clipping.
- Pulse appears for Control, Target, and Override.

## Boundary
The ALS signal is a physical display-timing channel and belongs to the external input vector `u(t)`, not to biological hidden `Y(t)`.
