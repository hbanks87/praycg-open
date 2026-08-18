# The Box testing protocol

The Box should be tested before human sessions. These tests do not certify a perfect Faraday cage; they provide practical quality-control checks.

## Test 1 - Visual and safety inspection

Check:

- exit path clear;
- participant can leave quickly;
- ventilation present;
- no sharp mesh edges;
- no loose copper tape touching electronics unexpectedly;
- no trip hazards;
- no hot electronics or blocked fans;
- no unsafe ground/mains modifications.

## Test 2 - AM radio sanity check

1. Use a battery-powered AM/FM radio.
2. Tune to a weak or static-heavy AM station.
3. Compare signal outside vs inside the Box.
4. Record whether noise/signal changes.

This is crude and not a calibrated RF test.

## Test 3 - phone / Wi-Fi check

1. Compare phone signal or Wi-Fi reception outside vs inside.
2. Record qualitative attenuation.
3. Do not treat this as certification.

## Test 4 - EEG noise-floor check

1. Run acquisition without participant.
2. Run acquisition with participant seated and still.
3. Compare channel noise, line noise, packet loss, and gaps.
4. Save watchdog report.

## Test 5 - ALS-PT19 timing check

1. Run stimulus with full-screen ALS start pulse or timing marker.
2. Confirm ALS stream appears in LabRecorder.
3. Confirm clear rise and return to baseline.
4. Confirm no clipping and no missed pulse.

## Test 6 - full-stack smoke test

Run a short non-experimental session with:

```text
EEG
ALS_PT19_Timing
StasisMarkers
PolarHRV or ECG/R-R
respiration if used
LabRecorder
protocol runner
```

Verify all streams in the XDF before a real run.
