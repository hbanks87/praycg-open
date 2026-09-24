# Cerelog V1 — 5 differential EMG + 2 EOG + 1 ALS

Firmware identifier: **`CERELOG_V1_EMG5_EOG2_ALS1_1K_V1`**  
Bundle prepared: September 24, 2026.

Custom experimental adaptation for manufacturer review, **not an official Cerelog release**. This bundle preserves the exact source and application binary from the latest successful local flash; packaging did not rebuild, reflash, open a serial port, or upload to GitHub.

**Before public upload:** the exact application binary contains two compiler-embedded source paths with the original builder's Windows account name and workspace folder. They are retained to preserve the flashed image's checksum. The binary is **not fully path-anonymized**. No device backup, board MAC, recording, personal project journal, or raw build/upload log is included. See [licensing and provenance](LICENSE_NOTICE.md) before redistribution.

## Channel configuration

| Hardware input | Intended signal | Gain | Matching reader unit |
| --- | --- | ---: | --- |
| IN1P / IN1N | Left masseter EMG | 24 | microvolts |
| IN2P / IN2N | Right masseter EMG | 24 | microvolts |
| IN3P / IN3N | Left temporalis EMG | 24 | microvolts |
| IN4P / IN4N | Right temporalis EMG | 24 | microvolts |
| IN5P / IN5N | Divided ALS-PT19 signal / board GND | 1 | ADC-input volts |
| IN6P / IN6N | Right frontalis EMG | 24 | microvolts |
| IN7P / IN7N | Horizontal EOG | 24 | microvolts |
| IN8P / IN8N | Vertical EOG | 24 | microvolts |

All eight hardware channels are active at **1,000 samples/second**. Every input measures its own P minus N. SRB1, SRB2, BIAS driver, and channel BIAS contributions are disabled. Body-channel N electrodes are not ground. Channel names describe the intended montage, not validated anatomical placement or signal origin.

This is five EMG channels **1, 2, 3, 4, 6**, two EOG channels **7, 8**, and ALS channel **5**; the fifth EMG channel is not hardware CH5. ALS values are voltage at the divided ADC input, not lux or undivided sensor voltage.

## What changed from the previous four-EMG build?

CH6–8 are enabled as normal differential gain-24 inputs rather than powered-down, internally shorted channels. Firmware identity and host metadata were updated accordingly. CH1–5 settings, 1 kSPS, startup/streaming protocol, packet length, and SRB/BIAS-off behavior are preserved. See [changes](CHANGELOG.md) and both source diffs in this bundle.

## Contents and use

- `source/Cerelog_V1_EMG5_EOG2_ALS1_1k/`: exact Arduino sketch.
- `firmware/`: archived application and matching build support images, plus partition layout. No full-flash backup or merged image.
- `reader/`: matching standalone Python off-body bench reader and 18 offline tests.
- [Build and protocol guide](BUILD_AND_PROTOCOL.md): build versions, offsets, guarded manual flash example, packet layout, and reader commands.
- [Verification and limits](VERIFICATION.md): sanitized historical bench evidence and current offline checks.
- `changes_from_upstream.diff`, `changes_from_EMG4_ALS1.diff`: reviewable changes.
- `MANIFEST.json`, `SHA256SUMS.txt`, `verify_bundle.py`: file provenance and offline integrity verification.

To inspect after extracting, run `python -B verify_bundle.py`, then from `reader/` run `python -B -m unittest test_reader -v`. These commands do not open hardware. Do not run the bench capture or flash commands merely to inspect this bundle.

For GitHub, extract the ZIP and add the contents of its top-level folder to the intended repository or review branch. Alternatively attach the ZIP to a reviewed release. This bundle does not choose a repository, create a release, or publish anything automatically. Resolve licensing and the binary-path privacy caveat before public posting.

## PRAYCG compatibility

The separate **PRAYCG Alpha 10.2.3** application patch supplies the matching `cerelog_v1_emg_eog_als` hardware-library route. It is not included here, and 10.2.3 is an application version, not this firmware's version. The old Alpha 10.2.2 four-EMG route and default EEG/BrainFlow configuration are not compatible with this mixed-gain firmware.

The matching 10.2.3 route publishes five-channel EMG, two-channel EOG, one-channel ALS, and timing/diagnostic streams. The standalone reader in this ZIP writes local CSV/JSON; it does **not** publish LSL or network streams. Do not run two readers against the same serial port.

PRAYCG's current route remains experimental/off-body bench evaluation. No new body-connected validation or electrical-safety approval is implied. This bundle does not change Gamma Scalpel or automatically incorporate these channels into MeaningGamma analysis.

## Safety and scientific limits

Keep every electrode disconnected from the body during flashing and initial bench checks. Disconnect power before changing wiring. Follow Cerelog's safety instructions and obtain manufacturer review of the complete connected setup; this work does not establish medical-grade isolation or authorize body-connected use. Gain 1 does not protect the ALS input from excessive voltage or invalid common-mode levels.

Electrode placement, usable EOG/EMG quality, connected ALS/divider behavior, and dual-device barcode alignment remain to be validated. Optical barcode matching is a planned analysis step, not synchronization implemented in this firmware. Millisecond loop timestamps, no sequence counter, and possible coalesced DRDY events limit loss/timing claims.

## Upstream

Adapted from Cerelog's [V1 special differential firmware](https://github.com/Cerelog-ESP-EEG/ESP-EEG/tree/af1a56e0127e71606afdc7e7ddf0ca831715e09c/firmware/other/V1_special_differential_fw), pinned to commit `af1a56e0127e71606afdc7e7ddf0ca831715e09c`. Cerelog attribution is preserved; no new license is assigned to upstream code or third-party runtime components.
