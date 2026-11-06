# Cerelog V1 compact profile: 3 EMG + 2 EOG + ALS-PT19

[PRAYCG Workbench Public Alpha 11.10.1](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.10.1) includes the acquisition and review software for **`CERELOG_V1_EMG3_EOG2_ALS1_1K_V1`**. This directory identifies the matching firmware build, its channel assignments and the available verification evidence. Download the exact [Arduino sketch](source/Cerelog_V1_EMG3_EOG2_ALS1_1k/Cerelog_V1_EMG3_EOG2_ALS1_1k.ino) and [application image](firmware/Cerelog_V1_EMG3_EOG2_ALS1_1k.ino.bin). The [credits and redistribution review](CERELOG_FIRMWARE_REDISTRIBUTION.md), [build instructions](BUILD_AND_PROVENANCE.md) and [source and relink archive](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.10.1/PRAYCG_Cerelog_Compact_Firmware_Source_and_Relink_20261106.zip) accompany these files. Selecting the Workbench profile does not flash a board.

| Wire slot | Compact assignment | Nominal gain |
| --- | --- | ---: |
| CH1, CH2 | Disabled; raw slots retained, scaled values unavailable | 1 |
| CH3 | Left temporalis EMG | 24 |
| CH4 | Right temporalis EMG | 24 |
| CH5 | ALS-PT19 light sensor | 1 |
| CH6 | Right frontalis EMG | 24 |
| CH7 | Horizontal EOG | 24 |
| CH8 | Left-eye vertical EOG | 24 |

Left and right refer to the participant. At a nominal 1,000 samples/s, each record carries eight raw slots, six active. EMG/EOG are reported in microvolts and ALS in volts using a nominal reference. There is no sample sequence counter, so exact loss counts are unknown.

**Workbench compatibility.** Select **compact / 3 EMG + 2 EOG + ALS / 1000 Hz**. The connector checks the firmware identity and register readback; the legacy four- and five-EMG profiles are distinct. Off-body evaluation and `EXPERIMENTAL_PARTICIPANT` have separate admission checks. LabRecorder can record the five optional LSL feeds: EMG, EOG, ALS, timing and transport events. See the [11.10.1 operator guide](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.10.1/CERELOG_DGA_WORKFLOW.md).

**Verification.** [PROFILE.json](PROFILE.json) describes the Workbench contract. [VERIFICATION.json](VERIFICATION.json) records build details, file hashes and bench results. On October 20, 2026, readback verified the application on one board, and a 30-second off-body capture yielded 29,792 accepted records. This check does not establish electrical safety, physiological selectivity, long-duration stability or synchronization with a second device.

The image is application-only and retains two historical compiler paths containing the original builder account/workspace names. The original sketch header records its pre-flash preparation state. The subsequent readback and bench records identify the same source and image hashes. See [licensing notes](LICENSE_NOTICE.md) and [checksums](SHA256SUMS.txt) before redistributing.
