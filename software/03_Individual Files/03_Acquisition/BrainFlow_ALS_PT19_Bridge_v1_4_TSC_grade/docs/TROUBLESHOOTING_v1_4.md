# Troubleshooting — PRAYCG BrainFlow ALS v1.4

## Error: could not open board / access denied

Close OpenBCI GUI. Only one program can own the Cyton COM port.

Also close serial monitors, old bridge terminal windows, Arduino IDE, PuTTY, and anything else using the port.

## Error: no serial ports found

1. Plug in the OpenBCI dongle.
2. Make sure the dongle switch is in the correct position.
3. Try a different USB port.
4. Wait 3-5 seconds after plugging it in.
5. Open Windows Device Manager and check Ports (COM & LPT).

## LabRecorder does not show streams

1. Start the BrainFlow bridge first.
2. Then open LabRecorder.
3. Press Update.
4. Run `python scripts\praycg_list_lsl_streams_v1_4.py` to confirm the streams exist.

## ALS stream exists but pulse is weak

1. Sensor must be taped directly over the lower-right timing square.
2. Use an opaque shroud to block room light.
3. Confirm the video was made with v1.6R ALS timing square enabled.
4. Increase monitor brightness.
5. Confirm ALS OUT is on D12/A6 and script uses `--als-aux-channel 1`.

## ALS stream clips or saturates

1. Lower monitor brightness.
2. Put translucent tape over the sensor.
3. Slightly offset the sensor from the brightest part of the square.

## EEG stream is present but ALS is flat

The board may not be in analog mode. Confirm the bridge was launched with:

```text
--enable-analog-aux
```

The bridge sends `/2` to the Cyton. That replaces accelerometer AUX with analog A5/A6/A7.

## Need to go back to OpenBCI GUI

Stop this bridge with Ctrl+C. The script tries to restore default mode with `/0`. If the GUI still looks strange, power-cycle the Cyton board.
