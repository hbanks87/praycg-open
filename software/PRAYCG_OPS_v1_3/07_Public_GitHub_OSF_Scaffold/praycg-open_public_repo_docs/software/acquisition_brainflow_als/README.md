# Acquisition - BrainFlow ALS-PT19 bridge

Recommended acquisition path when OpenBCI GUI cannot reliably publish EEG and AUX streams simultaneously.

## Current recommended branch

```text
PRAYCG OpenBCI BrainFlow ALS-PT19 Bridge v1.4
```

## Streams

```text
obci_eeg1
  16-channel EEG

OpenBCIAnalogAux
  A5/D11, A6/D12, A7/D13 analog AUX

ALS_PT19_Timing
  extracted single-channel ALS timing stream

OpenBCIStatusMarkers
  bridge status markers
```

## ALS wiring

```text
ALS-PT19 +   -> Cyton 3V3 / DVDD
ALS-PT19 -   -> Cyton GND
ALS-PT19 OUT -> Cyton D12 / A6
```

Default AUX mapping:

```text
0 = A5 / D11
1 = A6 / D12
2 = A7 / D13
```

## Rule

Do not run OpenBCI GUI and BrainFlow against the same COM port at the same time. One serial owner only.
