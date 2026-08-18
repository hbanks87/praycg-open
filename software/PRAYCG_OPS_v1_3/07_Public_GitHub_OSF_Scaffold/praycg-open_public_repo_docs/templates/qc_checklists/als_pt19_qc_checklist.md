# ALS-PT19 / photodiode timing QC checklist

## Required test before real run

1. Confirm ALS-PT19 is streaming to LSL.
2. Confirm signal appears in LabRecorder.
3. Play Target for at least 10 seconds.
4. Confirm strong analog rise during video-start pulse.
5. Confirm signal returns to baseline after pulse.
6. Repeat on Control and Override.

## Pass criteria

- Pulse visible in AUX / ALS stream.
- No clipping at maximum ADC value for full pulse duration.
- No missed pulse at video start.
- Target, Override, and Control all contain the timing pulse.

## Boundary

This timing channel validates physical display timing. It belongs to external input vector `u(t)`, not biological hidden variable `Y(t)`.
