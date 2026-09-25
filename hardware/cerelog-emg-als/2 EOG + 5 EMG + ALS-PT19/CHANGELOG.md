# Changes and compatibility

## EMG5 / EOG2 / ALS1, identifier CERELOG_V1_EMG5_EOG2_ALS1_1K_V1

Compared with the previous custom `CERELOG_V1_EMG4_ALS1_1K_V1`:

- CH6, CH7, CH8 register values at 0x0A–0x0C change from 0x81 (powered down, internally shorted) to 0x60 (normal differential input, gain 24).
- CH6 is intended for right frontalis EMG; CH7/CH8 for horizontal/vertical EOG.
- Configuration reports the new identifier, gains `[24,24,24,24,1,24,24,24]`, and active channels `[1,2,3,4,5,6,7,8]`.
- Matching standalone reader checks the new identity/register contract and scales all eight channels. An explicit port and off-body confirmation are required for capture. Eighteen offline tests are included.
- CH1–5 settings, 1 kSPS, 9600 startup baud, 460800 reader streaming baud, packet format, differential routing, and BIAS-off configuration are unchanged.

## Inherited changes from the vendor differential sketch

The previous local adaptation raised the configured rate to 1 kSPS, set CH5 gain 1, initially disabled CH6–8, disabled BIAS contributions, added configuration query and register verification, validated command framing/checksum, refused insufficient streaming baud, and attached DRDY only after continuous-read mode was ready. Those host/configuration/startup protections remain.

`changes_from_EMG4_ALS1.diff` isolates the sketch changes from the previous custom build. `changes_from_upstream.diff` shows cumulative sketch changes from the saved vendor source at commit `af1a56e0127e71606afdc7e7ddf0ca831715e09c`.

## Boundaries

This firmware does not configure anatomical placement, filter EMG/EOG, validate a body-connected setup, or implement optical clock alignment. It does not add reference-channel regression to Gamma Scalpel. The separate PRAYCG Alpha 10.2.3 patch supports the new identifier; the prior four-EMG route must not be reused as though it were compatible.
