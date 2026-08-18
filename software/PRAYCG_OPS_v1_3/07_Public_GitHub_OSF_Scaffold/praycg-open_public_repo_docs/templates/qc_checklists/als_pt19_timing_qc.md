# ALS-PT19 timing QC

## Setup

- ALS-PT19 signal visible in acquisition software.
- ALS stream appears in LabRecorder.
- If using fullscreen pulse: confirm black -> white -> black pattern.
- If using timing square: confirm sensor is taped over square and shielded from ambient light.

## Required test

1. Play Target for at least 10 seconds.
2. Confirm strong rise during video-start pulse.
3. Confirm signal returns to baseline.
4. Repeat Control and Override.

## Pass criteria

- Pulse visible in AUX/ALS stream.
- No missed branch start pulse.
- No clipping for full pulse duration.
- Return to black/baseline before content begins.
- Same behavior for Control, Target, and Override.

## Boundary

ALS validates physical display timing. It belongs to `u(t)`, not biological `Y(t)`.
