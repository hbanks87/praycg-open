# Build, flash map, and host protocol

## Archived build

| Component | Recorded version / selection |
| --- | --- |
| Arduino CLI | 1.5.1 |
| Espressif ESP32 Arduino core | 3.3.12 |
| FQBN | `esp32:esp32:esp32da:UploadSpeed=115200` |
| Board menu | ESP32-WROOM-DA Module; other menus default |
| Actual flash arguments | DIO, 80 MHz, 4 MB |
| Optimization | `-Os` |
| Upload utility | esptool 5.3.1; baud 115200 |
| Compile-reported program size | 280,980 bytes |
| Compile-reported globals | 22,780 bytes |
| Application file size | 281,136 bytes |

Arduino.h and SPI.h are supplied by that core. Install the pinned toolchain separately. From the extracted bundle root, a compile-only example is:

```text
arduino-cli compile --fqbn esp32:esp32:esp32da:UploadSpeed=115200 --output-dir rebuilt source/Cerelog_V1_EMG5_EOG2_ALS1_1k
```

Build paths and timestamps may change a rebuilt image's hash; byte-for-byte reproducibility is not claimed. The included application is the historical flashed image, not a fresh build. See README's compiler-path privacy notice.

## Flash layout

| Offset | File |
| --- | --- |
| 0x1000 | `firmware/Cerelog_V1_EMG5_EOG2_ALS1_1k.ino.bootloader.bin` |
| 0x8000 | `firmware/Cerelog_V1_EMG5_EOG2_ALS1_1k.ino.partitions.bin` |
| 0xE000 | `firmware/boot_app0.bin` |
| 0x10000 | `firmware/Cerelog_V1_EMG5_EOG2_ALS1_1k.ino.bin` |

The historical update wrote **only the application at 0x10000** after checking the existing layout/support images and preserving a private device-specific backup. The support images here match that layout; they were not rewritten by the latest update. `firmware/partitions.csv` documents it. These are separate images, not a merged file and not files to concatenate or write at address zero.

No automatic flashing script or erase-all command is included. For an application-only update, first confirm the exact supported Cerelog V1 target, its current partition layout and boot selection, preserve that target's own recovery backup, verify bundle hashes, close other readers, and keep all electrodes off-body. An example **only after those checks** is:

```text
python -m esptool --chip esp32 --port YOUR_VERIFIED_PORT --baud 115200 write-flash 0x10000 firmware/Cerelog_V1_EMG5_EOG2_ALS1_1k.ino.bin
```

Replace `YOUR_VERIFIED_PORT` deliberately; no historical user's port is prescribed. This command writes the device and resets it. Review the flashing tool's verification output. For a blank board or different boot/partition layout, ask the manufacturer for the appropriate full installation procedure instead of applying this example blindly.

## Startup and commands

After initializing the ADS1299 and taking its 24-byte boot register readback, the board waits at **9600 baud**. It does not stream until a compatible host starts it. The matching reader checks identity, rate, gains, all active channels, BIAS state, ADS1299 ID and configured register values.

A command is 12 bytes: `AA BB`, a seven-byte payload, its byte-sum modulo 256, then `CC DD`. Payload fields: message type (1 byte), timestamp (4 bytes big-endian), register (1 byte), value (1 byte).

- Type `0x03`: configuration query; reply is `CERELOG_CFG ` followed by JSON and newline.
- Type `0x02`, register `0x01`, value `0x06`: start streaming at **460800 baud**.
- Value `0x07` / 921600 is also accepted by firmware but is not exercised by the supplied reader or cited bench capture. Lower/invalid rates are refused.
- Streaming is refused when the configured boot-register readback fails.
- Commands are not processed during the acquisition loop. Reset stops the stream and returns the board to its startup handshake; the reader resets when closing.

The host-command timestamp is not a shared acquisition clock. Stream timestamps are elapsed milliseconds since the session's local start reference, generated in the main loop rather than latched at conversion time in the DRDY interrupt.

## Frame layout and scaling

All eight hardware channels retain their original order in every **37-byte frame**:

| Zero-based bytes | Contents |
| --- | --- |
| 0–1 | `AB CD` |
| 2 | `31` decimal (payload length) |
| 3–6 | Device elapsed milliseconds, unsigned big-endian |
| 7–9 | ADS1299 status |
| 10–33 | Eight signed 24-bit big-endian counts, CH1 through CH8 |
| 34 | Sum of bytes 2–33 modulo 256 |
| 35–36 | `DC BA` |

Nominal Vref is 4.5 V, not an independent calibration:

- CH1–4 and CH6–8: microvolts = counts × 4.5 × 1,000,000 / (24 × 2^23).
- CH5: ADC-input volts = counts × 4.5 / 2^23.

No filtering, rectification, resampling, interpolation, sequence counter, event matching, or hardware synchronization is added. A boolean DRDY flag may coalesce events if processing stalls. Valid framing/checksums and a plausible mean rate cannot prove that every conversion was captured exactly once.

## Matching off-body reader

Python 3.11 and pyserial 3.5 were used. From `reader/`:

```text
python -m pip install -r requirements.txt
python -B -m unittest test_reader -v
```

The 18 tests use synthetic/mock data; they do not open a serial port. The optional command below **does** open/reset the selected device, starts acquisition, and writes CSV/JSON to `reader/recordings/`:

```text
python -B cerelog_reader.py --port YOUR_VERIFIED_PORT --seconds 30 --confirm-off-body
```

Use it only for an intentional bench check with every electrode off-body for the entire capture. The confirmation flag does not establish electrical safety. The reader requires an explicit port, accepts captures of 2–300 seconds, validates the configuration before streaming, and publishes no network feed. It records CH5 in volts and the other seven channels in microvolts, with raw counts retained.
