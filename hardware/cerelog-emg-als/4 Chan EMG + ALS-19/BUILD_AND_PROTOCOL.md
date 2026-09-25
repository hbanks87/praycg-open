# Build, binary map, and host protocol

## Existing build

- Arduino CLI: 1.5.1.
- Espressif ESP32 Arduino core: 3.3.12.
- Board selection: ESP32-WROOM-DA Module.
- FQBN: `esp32:esp32:esp32da:UploadSpeed=115200`.
- Other board menus: core defaults; 4 MB flash, default partition scheme.
- Compiler optimization: `-Os`.
- Upload utility: esptool 5.3.1; upload baud 115200; erase-all disabled.
- Final compilation: 280,964 bytes program storage; 22,780 bytes globals.
- Libraries: Arduino.h and SPI.h from the selected ESP32 core.

After installing that exact core/toolchain, rebuild from the package root:

```text
arduino-cli compile --fqbn esp32:esp32:esp32da:UploadSpeed=115200 --output-dir rebuilt source/Cerelog_V1_EMG4_ALS1_1k
```

This command compiles only, not uploads. Toolchain dependencies must be
installed separately. Build timestamps/paths can affect regenerated binary
hashes; the included binaries are the archived final build, not a promised
bit-for-bit reproducible fresh compilation.

## Exact images from the final upload

| Flash offset | File in firmware/ |
|---|---|
| 0x1000 | Cerelog_V1_EMG4_ALS1_1k.ino.bootloader.bin |
| 0x8000 | Cerelog_V1_EMG4_ALS1_1k.ino.partitions.bin |
| 0xE000 | boot_app0.bin |
| 0x10000 | Cerelog_V1_EMG4_ALS1_1k.ino.bin |

The final upload log reported verification of the written images. Archived
`_flashed` copies also match the packaged images byte-for-byte. These are
separate images, not files to concatenate or write at address zero. A full
device backup and merged image are deliberately not included. No automatic
flashing script is provided. Confirm the target, preserve its own backup,
and use the manufacturer's appropriate flashing procedure after review.

## Startup and command envelope

The board initializes the ADS1299 and captures a 24-byte register readback.
It then waits at 9600 baud for a host. Query configuration before streaming.

Host command: 12 bytes, `AA BB`, seven-byte payload, checksum, `CC DD`.
Payload: message type (1 byte), timestamp (4 bytes, big-endian), register
(1 byte), value (1 byte). Checksum is the sum of those seven payload bytes
modulo 256.

- Type 0x03: query; returns a line beginning `CERELOG_CFG ` followed by JSON.
- Type 0x02, register 0x01, value 0x06: start at 460800 baud.
- Value 0x07 selects 921600, accepted by firmware but not exercised by the
  supplied reader/bench check. Lower rates and invalid codes are refused.
- The reader changes baud after the start command, validates frames, and
  resets the board when closing. Reset is how a streaming session is stopped;
  commands are not processed during the acquisition loop.

The command timestamp does not turn data into synchronized Unix acquisition
timestamps. Packets contain elapsed milliseconds since the host-start
reference. The SPI read and timestamp are handled in the main loop, not
latched as an acquisition timestamp in the DRDY interrupt.

## Data frame and scaling

Each frame is 37 bytes:

| Zero-based byte offsets | Contents |
|---|---|
| 0-1 | AB CD |
| 2 | 31 (payload length) |
| 3-6 | Device elapsed milliseconds, unsigned big-endian |
| 7-9 | ADS1299 status |
| 10-33 | Eight signed 24-bit big-endian channel counts |
| 34 | Sum of bytes 2-33 modulo 256 |
| 35-36 | DC BA |

Nominal reference is 4.5 V, not independently calibrated:

- CH1-4 microvolts = counts * 4.5 * 1,000,000 / (24 * 2^23).
- CH5 volts at the ADC input = counts * 4.5 / 2^23. This is not the
  pre-divider sensor voltage and is not calibrated illuminance.
- CH6-8 remain in the frame but are disabled and not meaningful inputs.

No sequence counter, hardware trigger, cross-device clock synchronization,
or optical edge calibration has been added. The boolean DRDY flag can
coalesce events if processing stalls; valid checksums alone do not prove
lossless acquisition. Host arrival timestamps are not acquisition timestamps.

## Matching reader and offline checks

Python 3.11 and pyserial 3.5 were used. From `reader/`:

```text
python -m pip install -r requirements.txt
python -B -m unittest test_reader -v
```

The seven tests do not open a serial port. An optional off-body bench capture
can be started with `python cerelog_reader.py --port PORT --seconds 30`,
replacing PORT with the intended device's actual port. Do not rely on the
reader's historical default port. This command resets and starts the device
and creates new CSV/JSON files in `reader/recordings/`; no such files are
included in this package. Close other software using that port first.
