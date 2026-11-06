Download and extract the [source and relink archive](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.10.1/PRAYCG_Cerelog_Compact_Firmware_Source_and_Relink_20261106.zip). Run the build commands below from its extracted root.

# Compact Cerelog V1 firmware: source, build and relinking

Firmware identity: **`CERELOG_V1_EMG3_EOG2_ALS1_1K_V1`**. The distributed sketch and **application-only** image are the retained October 19 build for the compact 3 EMG / 2 EOG / ALS profile. On October 20 the application was written on one board and verified by independent readback; a 30-second off-body check yielded 29,792 accepted records. The sketch’s original “NOT FLASHED” comment describes its state on October 19. It is intentionally preserved so the reviewed sketch bytes still match their checksum. The 11.10.1 Workbench update for joint off-body recording did not change this firmware.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `Cerelog_V1_EMG3_EOG2_ALS1_1k.ino` | 14,544 | `cb68b05fe71aee0ef2088d43f4d39968687bf1db103a5ca53cab8e2df16f55c1` |
| `Cerelog_V1_EMG3_EOG2_ALS1_1k.ino.bin` | 281,136 | `bf13f11ac9a36be9d1cb64133f895a78c9fcc345f13932a4f5b2f7e051b2122f` |

**Source lineage.** This local PRAYCG adaptation descends through the preceding five-EMG profile from [Cerelog’s differential sketch at commit af1a56e](https://github.com/Cerelog-ESP-EEG/ESP-EEG/blob/af1a56e0127e71606afdc7e7ddf0ca831715e09c/firmware/other/V1_special_differential_fw/V1_special_differential_fw.ino). It powers down and internally shorts CH1/CH2, advertises the compact profile’s identity and gain/mask values, and requires ADS1299 ID 0x3E at register readback. The previous framing, acquisition loop and eight wire slots are retained. The sketch uses Arduino Core and SPI. Original notices and source credits apply separately; see the accompanying distribution notice.

**Historical image privacy.** The unmodified application contains two compiler source paths with the original Windows account and workspace names, in Arduino UART and ESP-IDF timer code. They were not patched because that would change the board-verified bytes. The relink archive also includes an Arduino Core object archive whose compiled strings contain source paths. No full-device flash backup, raw recording, participant response, live session log or board identifier is supplied.

**Build settings.** Arduino CLI 1.5.1, ESP32 Arduino Core 3.3.12, ESP32-WROOM-DA board, `esp32:esp32:esp32da:UploadSpeed=115200`, optimization `-Os`; Xtensa toolchain package `esp-x32` 2601, ESP32 SDK package `esp32-libs` 3.3.12 (ESP-IDF v5.5.5), esptool 5.3.1. The compiler reported 280,988 program bytes and 22,780 bytes of static RAM. Those numbers differ from the packaged image size. The application does not include the bootloader or partition table.

**Rebuild from source.** Extract the companion source/relink ZIP. With the pinned Arduino toolchain installed, run the following from its root, using a fresh build directory. This compiles without uploading:

```text
arduino-cli compile --fqbn esp32:esp32:esp32da:UploadSpeed=115200 --build-path rebuilt source/Cerelog_V1_EMG3_EOG2_ALS1_1k
```

The archive supplies the matching `cores/esp32`, SPI library, ESP32DA variant, configuration, partition definitions and build recipes under `platform/`. The files were checked against the [official core platform ZIP](https://github.com/espressif/arduino-esp32/releases/download/3.3.12/esp32-core-3.3.12.zip). To modify the libraries, use a separate 3.3.12 platform installation or working copy, replace its corresponding source with your edited files, and run the same compile command. `TOOLCHAIN.json` records the platform index and release-specific upstream compiler and SDK downloads and SHA-256 values.

**Relink without recompiling the sketch.** Use Python 3.9+ and the pinned compiler/esptool from your installation. Replace `ARDUINO_DATA/packages/esp32` with the actual package directory. The supplied application object, SPI object and Arduino Core archive omit debug sections but retain relocations. To use a rebuilt or modified library, pass your replacement `core.a` or `SPI.cpp.o`. Use a new empty output folder.

```text
python relink.py --packages "ARDUINO_DATA/packages/esp32" --core objects/core.a --spi objects/SPI.cpp.o --output relinked
```

The linker reads the installed ESP32 SDK’s response files, linker scripts and target libraries. If that SDK is not installed, save the [unmodified official ESP32 SDK ZIP](https://github.com/espressif/arduino-esp32/releases/download/3.3.12/esp32-libs-3.3.12.zip), then run:

```text
python prepare_sdk.py esp32-libs-3.3.12.zip verified-sdk
python relink.py --packages "ARDUINO_DATA/packages/esp32" --sdk verified-sdk --core objects/core.a --spi objects/SPI.cpp.o --output relinked-from-sdk
```

The SDK verifier checks the whole ZIP and each of 177 linking inputs before use. `sdk-link-recipes/` preserves the matching response files and linker scripts; `LINK_SDK.json` identifies the SDK inputs, and `LINK_MAP_RESOLUTION.json` records archive members considered by the historical linker. Not every considered library supplied bytes to the application.

**Verification of replaceability.** The application was relinked with the supplied objects and then with a separately compiled, deliberately modified SPI object. A diagnostic marker appeared only in the second image. Neither verification image was flashed. These checks establish that the library can be replaced, not that a rebuild reproduces the historical application checksum or is qualified for hardware use.
