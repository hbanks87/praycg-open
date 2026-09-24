# Attribution and redistribution review

This is a custom firmware review bundle, not a new blanket license grant. Original authors retain their notices. The included binaries incorporate third-party runtime code; the entire bundle must not be labeled as solely MIT-licensed.

## Cerelog source

Source provenance: `Cerelog-ESP-EEG/ESP-EEG`, commit `af1a56e0127e71606afdc7e7ddf0ca831715e09c`, `firmware/other/V1_special_differential_fw/V1_special_differential_fw.ino`.

The repository's [LICENSE at that commit](https://github.com/Cerelog-ESP-EEG/ESP-EEG/blob/af1a56e0127e71606afdc7e7ddf0ca831715e09c/LICENSE) declares the firmware folder MIT and names Copyright (c) 2025 Cerelog Inc. However, that file contains the literal placeholder `[Standard MIT License Text Continues...]` instead of the remaining standard terms. A verbatim copy is preserved in `licenses/CERELOG_UPSTREAM_LICENSE.txt`; this package does not silently replace or complete it.

Ask Cerelog/Simon to confirm the complete intended firmware license before public redistribution. This is a documented provenance gap, not a determination that redistribution is prohibited. No repository-wide license has been invented for the local changes or companion tools.

## Arduino ESP32 and ESP-IDF

The application uses **Arduino ESP32 core 3.3.12**, including its core and SPI library. The core package identifies LGPL-2.1-or-later; the official [3.3.12 license text](https://github.com/espressif/arduino-esp32/blob/3.3.12/LICENSE.md) is copied to `licenses/ARDUINO_ESP32_LGPL_2_1.md`. Corresponding upstream source is available at [the 3.3.12 tag](https://github.com/espressif/arduino-esp32/tree/3.3.12).

The installed prebuilt library metadata identifies **ESP-IDF v5.5.5, revision b774170ff46**. The exact-revision [Apache-2.0 license](https://github.com/espressif/esp-idf/blob/b774170ff46/LICENSE) and [third-party copyright index](https://github.com/espressif/esp-idf/blob/b774170ff46/docs/en/COPYRIGHT.rst) are included. Individual component notices can differ and take precedence. `licenses/BUILD_COMPONENT_VERSIONS.txt` records the supplied library package's version metadata; listing a component there does not establish that it was linked into this application.

Additional available Newlib, GCC runtime, FreeRTOS, and Xtensa notices are preserved under `licenses/`. They are reference material, not a certified exhaustive inventory of the application and bootloader's linked components.

## Before a public binary release

Have the repository owner review the complete upstream firmware terms and the applicable runtime attribution/source/relinking requirements, and arrange the corresponding source/rebuild materials where required. Toolchain links, a sketch, and license copies alone are not represented here as a completed binary-redistribution compliance package. This bundle has not been certified license-complete.

Also review the README's separate privacy warning: two compiler source paths in the exact application binary retain the original builder's Windows account/workspace names. No attempt was made to patch strings in the executable and pass it off as the flashed artifact.
