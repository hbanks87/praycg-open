# Stream preflight QC

Before a real run, confirm all expected streams in LabRecorder.

## Minimum desired streams

```text
obci_eeg1
OpenBCIAnalogAux
ALS_PT19_Timing
OpenBCIStatusMarkers
StasisMarkers
PolarHRV or ECG/R-R
Respiration stream if used
```

## Checks

- EEG sample rate plausible.
- No major packet loss or stream gaps.
- StasisMarkers online before LabRecorder starts.
- ALS pulse visible in bench test.
- HR/R-R stream visible.
- Respiration stream visible if used.
- Event log path created.
- Media hashes logged.
- Channel map confirmed or caveated.
