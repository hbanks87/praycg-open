# Hardware projects

For connecting equipment to Public Workbench **11.13.1**, start with [recording routes and support](../workbench/docs/hardware-support.md). This directory holds preserved physical designs, firmware packages and project evidence.

## Choose a project

| Project | Read first | Supporting material |
| --- | --- | --- |
| ALS PT19 sensor holders | [Designs and placement photographs](als-pt19/) | Printable parts and mechanical geometry |
| OpenBCI gelless cap | [Cap build document](openbci-gelless-cap/OpenBCI%20Gelless%20Cap.pdf) | Original construction documentation |
| Cerelog: four EMG + ALS | [Original review-package introduction](cerelog-emg-als/4%20Chan%20EMG%20%2B%20ALS-19/README_FOR_SIMON.md) | [Build and protocol](cerelog-emg-als/4%20Chan%20EMG%20%2B%20ALS-19/BUILD_AND_PROTOCOL.md) · [bench checks](cerelog-emg-als/4%20Chan%20EMG%20%2B%20ALS-19/BENCH_CHECKS.md) · [manifest](cerelog-emg-als/4%20Chan%20EMG%20%2B%20ALS-19/MANIFEST.json) |
| Cerelog: five EMG + two EOG + ALS | [Original bundle introduction](cerelog-emg-als/2%20EOG%20%2B%205%20EMG%20%2B%20ALS-PT19/README.md) | [Verification](cerelog-emg-als/2%20EOG%20%2B%205%20EMG%20%2B%20ALS-PT19/VERIFICATION.md) · [source and licensing notes](cerelog-emg-als/2%20EOG%20%2B%205%20EMG%20%2B%20ALS-PT19/LICENSE_NOTICE.md) |
| Compact Cerelog, three EMG + two EOG + ALS | [Compact profile, channel map and evidence](cerelog-emg-als/3%20EMG%20%2B%202%20EOG%20%2B%20ALS-PT19/README.md) | [Sketch](cerelog-emg-als/3%20EMG%20%2B%202%20EOG%20%2B%20ALS-PT19/source/Cerelog_V1_EMG3_EOG2_ALS1_1k/Cerelog_V1_EMG3_EOG2_ALS1_1k.ino) · [Binary](cerelog-emg-als/3%20EMG%20%2B%202%20EOG%20%2B%20ALS-PT19/firmware/Cerelog_V1_EMG3_EOG2_ALS1_1k.ino.bin) · [Build and notices](cerelog-emg-als/3%20EMG%20%2B%202%20EOG%20%2B%20ALS-PT19/CERELOG_FIRMWARE_REDISTRIBUTION.md) · [11.13.1 workflow](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.13.1/CERELOG_DGA_WORKFLOW.md) |
| Shielding enclosure / The Box | [Project notes](shielding-enclosure/README.md) | [Grounding and electrical safety](shielding-enclosure/grounding_and_electrical_safety.md) · [test protocol](shielding-enclosure/testing_protocol.md) |

The four- and five-EMG firmware bundles each have a matching reader. The compact three-EMG route requires its own firmware identity and register readback. Workbench 11.10.0 adds managed live acquisition for that route. The [11.9 integration guide](../workbench/docs/releases/alpha-11.9.2/package/INTEGRATION_11_9.md) documents its earlier closed-capture review.

## Use the right evidence

The four- and five-EMG project folders include source and binary review packages. The compact profile links its matching firmware, the versioned source/relink archive, checksums and bench verification. Check the exact firmware and reader pairing before interpreting channel units or timing. A project listing does not qualify electrical safety or physical synchronization, and a shielding design does not establish signal validity.

Cerelog packages are experimental custom adaptations with their own manufacturer-review and binary-provenance notes. Read those notes with the [current Workbench route requirements](../workbench/docs/hardware-support.md). Earlier bench records retain their original scope.

For stimuli used alongside equipment, open the [stimulus and example library](../examples/README.md). Keep project-specific rights and notices with any reused materials.

[Repository home](../README.md) · [Study workflow](../workbench/docs/workflow.md) · [Attribution](../CITATIONS_AND_ATTRIBUTION.md) · [Sources and history](../docs/README.md)
