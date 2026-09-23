# Sanitized verification summary

These results summarize the existing final firmware bench checks; they are
not new physical tests performed while creating this ZIP.

Source SHA-256:
`fbba9627e6a06d8bad8cc622d2547abc40eebd856b4c1c1e2ac4ff9cdec293e7`.

Application SHA-256:
`12738410fc3fd9ba9910eaa829178d238b2091006c48d0cd90d8c12f1ba462b0`.

Both were checked again during packaging. The final compile and upload
completed successfully, with uploaded images verified by the flashing tool.

## Observed ADS1299 boot readback

Addresses 0x00 through 0x17:

```text
3E B4 D0 E8 00 60 60 60 60 00 81 81 81 00 00 00 00 00 00 00 0F 00 00 00
```

## Final 30-second off-body transport check

- 29,989 valid frames with the expected ADC status prefix.
- Zero malformed/checksum-failed frames.
- Zero discarded bytes after the first valid frame.
- One initial alignment byte discarded during the baud transition.
- Eight trailing bytes at the recording cutoff (an incomplete final frame).
- Device-timestamp-derived rate: approximately 999.6666 SPS.
- Timestamp intervals: 29,978 at 1 ms; 10 at 2 ms.
- Powered-down channels 6-8 returned zero.

A separate five-second reset/reconnect check returned 4,998 valid frames
at approximately 999.7999 SPS, with no bad frames or midstream discarded bytes.

An earlier development run failed because the first ADC frame was all zero.
The packaged source includes the correction: enable the DRDY interrupt only
after RDATAC, and wait for a fresh falling edge. The results above are for
that corrected final build.

## Offline checks during packaging

All seven supplied reader tests passed again: host handshake, fragmented
frame parsing/signed counts, corruption recovery, mixed-gain scaling,
initial alignment accounting, register mismatch rejection, and quality-check
rejection of invalid ADC status/midstream discarded bytes.

## Limits

This validates register settings, serial framing, and approximate rate for
short bench runs. It does not prove every conversion was captured, validate
long-duration reliability, establish EMG selectivity/bandwidth, measure light
sensor edge latency/jitter, synchronize a second device, or certify electrical
safety. No subject recordings or physiological results are supplied.
