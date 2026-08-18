# Acquisition preflight checklist

## Streams

Confirm all expected streams appear in LabRecorder:

```text
obci_eeg1
OpenBCIAnalogAux
ALS_PT19_Timing
OpenBCIStatusMarkers
StasisMarkers
PolarHRV
VernierRespirationBelt
```

## Hardware

- OpenBCI connected and stable.
- BrainFlow owns the COM port; OpenBCI GUI is closed.
- ALS-PT19 wired to D12/A6 and powered from 3.3V.
- Respiration belt streaming.
- Polar H10 or ECG/R-R source streaming.
- Cap/electrode map photographed or physically verified.

## Timing

- ALS pulse bench test passed.
- StasisMarkers online before LabRecorder starts.
- Protocol event log path visible.

## Participant

- Consent / self-run note complete.
- Stop option clear.
- Comfort and cable routing checked.
