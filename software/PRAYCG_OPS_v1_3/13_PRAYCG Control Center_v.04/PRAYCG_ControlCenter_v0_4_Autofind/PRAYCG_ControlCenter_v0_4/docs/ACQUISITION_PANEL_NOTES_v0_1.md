# Acquisition Panel Notes v0.4

## Included buttons

- Start Polar H10 RR stream.
- Start Vernier Respiration Belt USB stream.
- Start Vernier Respiration Belt BLE stream.
- Start BrainFlow EEG only.
- Start BrainFlow EEG + ALS.
- Check visible LSL streams.
- Signal Quality / Contact Index.
- ALS Screen Pulse Barcode Test.
- Open LabRecorder.

## Polar H10

The included script creates an LSL stream named `PolarHRV`. It pushes R-R intervals in milliseconds when RR packets are present.

## Vernier Respiration Belt

The included script creates an LSL stream named `VernierRespirationBelt`. USB is recommended first for stability and to avoid Bluetooth contention.

## Signal Quality / Contact Index

This is a practical 0.4.0 channel-quality score computed from live LSL samples. It checks finite fraction, flatline/dropout, amplitude spread, high-frequency difference ratio, and stream timing gaps.

It is **not true OpenBCI Cyton impedance**.

## ALS Screen Pulse Barcode Test

The barcode pattern is:

```text
black 0.5 s
white 2.0 s
black 0.5 s
white 0.75 s
black 1.0 s
```

The long pulse is meant to improve detection relative to a short single flash. The barcode structure helps separate real screen response from noise.

## Future upgrade

A true Cyton impedance mode should be added later as an advanced pre-run feature using OpenBCI lead-off commands. It should not be run during acquisition.
