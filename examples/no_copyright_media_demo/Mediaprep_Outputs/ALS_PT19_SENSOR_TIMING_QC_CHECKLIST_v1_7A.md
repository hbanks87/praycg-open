# PRAYCG v1.7A ALS-PT19 / Photodiode Timing QC Checklist

Project: `stimulus_master_Demo_Lantern_Bridge_CC0`
Sensor timing enabled: `True`
Pulse mode: `fullscreen_start`
White pulse duration: `0.75` sec
Black guard duration: `0.5` sec
Content start offset: `1.25` sec

## Hardware placement

- In `fullscreen_start` mode, place the ALS-PT19 anywhere securely over the active display area where it can see the full-screen white flash.
- A black electrical tape / opaque shroud is still recommended to reduce room-light contamination.
- The old lower-right square mode remains available, but exact corner placement is no longer required in fullscreen mode.
- Confirm the sensor signal is recorded in the OpenBCI analog AUX / Analog Read LSL stream.

## Required test before real run

1. Play the generated Target video for at least 10 seconds.
2. Confirm a strong analog rise during the full-screen white pulse.
3. Confirm the signal returns to baseline during the black guard.
4. Repeat on Control and Override.

## Pass criteria

- Pulse visible in AUX stream.
- No clipping at maximum ADC value for the full pulse duration.
- No pulse missed at video start.
- Target, Override, and Control all contain the full-screen timing prefix.
- Cue markers use the shifted v1.7A cue schedule.

Boundary: this timing prefix validates physical display timing. It belongs to the external input vector u(t), not to any biological hidden variable Y(t).
