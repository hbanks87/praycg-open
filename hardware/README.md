# Hardware projects

This directory contains physical designs, build documents and project evidence. For the Workbench's acquisition routes, use [hardware support](../workbench/docs/hardware-support.md) and the [operating workflow](../workbench/docs/workflow.md).

## Browse the projects

| Project | Start here | Scope |
| --- | --- | --- |
| ALS PT19 holders | [Designs and photos](als-pt19/) | Sensor-holder geometry, printable parts and placement photographs |
| OpenBCI gelless cap | [Build document](openbci-gelless-cap/OpenBCI%20Gelless%20Cap.pdf) | Cap construction documentation |
| Cerelog EMG + ALS | [Review-package introduction](cerelog-emg-als/README_FOR_SIMON.md), [manifest](cerelog-emg-als/MANIFEST.json), [bench checks](cerelog-emg-als/BENCH_CHECKS.md) | Custom firmware adaptation, exact binaries, matching reader and review evidence |
| Shielding enclosure / The Box | [Project notes](shielding-enclosure/README.md), [safety notes](shielding-enclosure/grounding_and_electrical_safety.md), [test protocol](shielding-enclosure/testing_protocol.md) | Enclosure documentation and proposed environmental/QC checks |

A design or connector listing does not certify electrical safety, electrode contact, calibration, signal origin or synchronization. Use each project's specific instructions and evidence. Shielding does not guarantee valid signals or remove the need for physiological and environmental QC.

## Provenance and project boundaries

Keep each project's source, build configuration, binaries, checksums, manifest, upstream credits and test evidence together. Distinguish intended channel roles and settings from measured performance.

The Cerelog package is a custom adaptation for review, not an official Cerelog release. Its mixed-gain EMG/light-sensor configuration requires its matching host protocol; it is distinct from a general EEG route and from the withheld Cerelog 16 route in Alpha 10.2.1. The package's own notes describe its bench scope and binary privacy limitations. A Workbench application inventory does not automatically cover these firmware binaries.

Project files and manifests are preserved as supplied. Consult the [repository license](../LICENSE.md), [citations and attribution](../CITATIONS_AND_ATTRIBUTION.md), and each project's upstream notices for the applicable terms.

[Repository home](../README.md) · [Workbench](../workbench/README.md) · [Research program](../research/README.md)
