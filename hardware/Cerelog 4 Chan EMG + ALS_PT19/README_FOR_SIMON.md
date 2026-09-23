# Cerelog V1 EMG4 + ALS1 firmware: review package

Prepared September 23, 2026. This is the exact locally adapted source and
application binary used in the final successful flash, not a new rebuild.
It is a custom adaptation for review, not an official Cerelog release.

Firmware identifier: `CERELOG_V1_EMG4_ALS1_1K_V1`.

Based on Cerelog's
[V1 differential sketch at commit af1a56e0127e71606afdc7e7ddf0ca831715e09c](https://github.com/Cerelog-ESP-EEG/ESP-EEG/tree/af1a56e0127e71606afdc7e7ddf0ca831715e09c/firmware/other/V1_special_differential_fw).
The original Cerelog authors retain attribution; this package does not assign
a new license to upstream code or bundled runtime components.

## Configuration

| Channel | Intended signal | Gain | Routing |
|---|---|---:|---|
| 1 | Left masseter | 24 | IN1P / IN1N, differential |
| 2 | Right masseter | 24 | IN2P / IN2N, differential |
| 3 | Left temporalis | 24 | IN3P / IN3N, differential |
| 4 | Right temporalis | 24 | IN4P / IN4N, differential |
| 5 | Divided analog light sensor | 1 | IN5P signal / IN5N board GND |
| 6-8 | Unused | N/A | Powered down, internally shorted |

All channels retain positions in the eight-channel data frame. Sampling is
1,000 SPS. SRB1/SRB2 shared-reference routing, BIAS driver, and channel BIAS
contributions are disabled. These are firmware settings, not validation of
electrode placement, sensor input limits, or electrical safety.

## Changes to review

- CONFIG1: 0xB6 to 0xB4 (250 to 1,000 SPS).
- CH1-4: 0x60; CH5: 0x00; CH6-8: 0x81.
- CONFIG3: 0xE8; BIAS_SENSP/N: zero; MISC1: zero.
- Register-table size is computed; trailing entries removed.
- New configuration query reports the firmware identity and 24 boot register
  values. Streaming is refused if configured register readback fails.
- Validates host-command framing/checksum and rejects insufficient baud rates.
- Starts at 9600 baud, waits for a compatible host, then streams at 460800 baud
  with the supplied reader. A low activity LED while waiting is intentional.
- Attaches DRDY only after RDATAC is ready, avoiding the invalid initial zero
  frame observed during development.
- Retains the 37-byte data frame, millisecond timestamps, and no sequence counter.

`changes_from_upstream.diff` shows the source changes against the locally saved
upstream sketch. `MANIFEST.json` records both source hashes and the binary map.

## Package contents

- `source/`: exact Arduino sketch, byte-for-byte preserved.
- `firmware/`: exact application, bootloader, partition table, and boot_app0
  images used for the final upload. No full-flash backup or merged image.
- `reader/`: matching Python serial reader, seven offline tests, dependencies.
- `BUILD_AND_PROTOCOL.md`: toolchain, rebuild command, image offsets, protocol.
- `BENCH_CHECKS.md`: sanitized transport/bench summary and limitations.
- `SHA256SUMS.txt`: hashes for every other packaged file.

The default EEG/BrainFlow Cerelog path is not compatible with this mixed-gain,
1 kSPS configuration. The matching host must handle its handshake, baud,
channel gains, and timestamps. This ZIP is firmware review material, separate
from the PRAYCG 10.2.2 application patch; 10.2.2 is not a firmware version.

## Review scope

Please review the register choices, gain-1 light-sensor input arrangement,
BIAS-off/GND arrangement, startup sequence, and host protocol before wider use.
The board has not been certified for electrical safety by this work. Keep all
electrodes off-body for any firmware update or initial bench check.

No recordings, physiological results, device-specific flash backup, board MAC,
or raw build/upload logs are included. Packaging did not reflash the device.

Privacy note: the original compiled application contains two compiler-embedded
source paths that include the builder's Windows username and workspace folder
name. They are retained to preserve the exact flashed binary and its checksum;
this is not a fully path-anonymized binary. The source and review notes do not
contain those local absolute paths.
