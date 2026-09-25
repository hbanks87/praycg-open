# Verification evidence and limits

This is a sanitized summary, not a distribution of private logs or recordings.

## Historical source/build/flash check

- Source SHA256: `be3f9afabab75a3743d04557d42d8c0f291561f12a60a7ab8e53993b0ada7326`.
- Application SHA256: `7b97aa310ce98f15ce380376ab1b4e9be7be41e1cb414b7fe261845b0ecbd955`.
- Application image: 281,136 bytes, written at 0x10000 with successful upload hash verification.
- Existing bootloader, partition table and boot-app layout were checked before that application-only update. No erase-all or NVS update was performed.
- Body electrodes were disconnected for the update and subsequent new-firmware bench check. Acquisition was stopped/reset and the port closed afterward.

The public manifest provides checksums for all packaged build components. The private target identity, full-flash backup and raw flash logs are deliberately not included. Hash verification documents bytes, not device safety or physiological validity.

## Historical 30-second off-body check

Capture began September 24, 2026 at 01:40:59 UTC (September 23 local time). The configuration query matched the new identifier, mixed gains, and eight active channels.

ADS1299 readback, addresses 0x00–0x17:

```text
3E B4 D0 E8 00 60 60 60 60 00 60 60 60 00 00 00 00 00 00 00 0F 00 00 00
```

- 29,974 valid frames; no malformed/checksum-failed frames.
- One initial alignment byte; no discarded bytes after the first valid frame.
- Nineteen partial trailing bytes at the capture cutoff.
- Approximate device-timestamp rate: 999.533 samples/second.
- Intervals: 29,959 of 1 ms; fourteen of 2 ms; maximum 2 ms.
- All ADC status prefixes were 0xC; no samples reached the digital rails.

This establishes only the recorded configuration/transport observations. It does not prove exact conversion continuity, physiological quality, electrode placement, or electrical safety.

**The ALS input was unplugged during this capture.** Its floating-input voltage is not a light-sensor/divider measurement, a successful connected ALS check, or evidence of sensor-circuit overvoltage. A connected off-body sensor/divider check and dual-board optical offset/drift validation remain outstanding.

No earlier body-connected recordings are offered as facial EMG validation. This bundle makes no claim of a successful on-body EOG/EMG demonstration.

## Packaging-day checks — September 24, 2026

- Matching reader offline suite: **18 tests passed**, with no real serial device opened.
- Packaging uses an explicit file allowlist and fixed historical sketch/application/support-image hashes.
- Source and firmware bytes are preserved, with old/new sketch diffs and a manifest.
- Every archive member is checked against its staged content and checksum; ZIP CRC and an extracted-copy integrity check are required before delivery.
- Private logs, board identity, backups, recordings, ELF/map/cache files, and the project record book are excluded. The only allowed personal path strings are the two disclosed compiler-embedded strings in the exact application image; see README.

No new compilation, flash, body-connected test, connected ALS test, PRAYCG physical collection, or public upload is performed as part of packaging.
