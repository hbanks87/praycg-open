# Athena optical information reviewed for Alpha 10.5.2

Reviewed 8 October 2026. The Workbench can identify its frozen BrainFlow Athena p1041 route and automatically use the bundled raw optical profile. This review does not establish a complete Athena hemoglobin conversion profile.

## Information supported by public primary sources

| Information | Supporting source | Scope |
|---|---|---|
| Athena has a five-optode fNIRS sensor sampled at 64 Hz | [Muse device comparison](https://choosemuse.my.site.com/s/article/Comparing-Muse-Headbands?language=en_US) | Manufacturer specification; not a map of recorded channel columns |
| Athena PPG specifications list 660, 730 and 850 nm | [Muse device comparison](https://choosemuse.my.site.com/s/article/Comparing-Muse-Headbands?language=en_US) | These specifications alone do not assign those wavelengths to the Workbench's recorded optical columns |
| Muse SDK supports Athena fNIRS | [Muse Athena FAQ](https://choosemuse.my.site.com/s/article/Muse-S-Athena-What-s-New) | SDK availability is not a bundled conversion profile |
| Muse provides raw optical data through its research tools | [Muse Health platform and data](https://musehealth.ai/pages/platform-data) | Manufacturer description of its research tools |
| BrainFlow p1041 exposes 16 optical channels at 64 Hz | [BrainFlow Athena documentation](https://brainflow.readthedocs.io/en/stable/SupportedBoards.html#muses-athena), [pinned BrainFlow 5.23.0 documentation](https://github.com/brainflow-dev/brainflow/blob/5.23.0/docs/SupportedBoards.rst) | Connector channel count and nominal rate; not independently established optical geometry or hemoglobin concentrations |
| Hemoglobin conversion requires wavelength-specific pathlength information and source-detector distances | [MNE conversion documentation](https://mne.tools/stable/generated/mne.preprocessing.nirs.beer_lambert_law.html) | Processing requirements; MNE defaults are modeling assumptions, not Athena calibration |

## Information still missing for automatic Athena conversion

No complete manufacturer-provided profile matching the Workbench's pinned BrainFlow recording route was located in the reviewed public sources. The unresolved information is:

- The wavelength and source/detector identity for each recorded optical column, including background-light channels.
- Source-detector distances for the intended wavelength pairs.
- The relationship of the decoded values to positive light intensity, including dark offsets, automatic exposure, gain changes and any device preprocessing.
- The supported firmware range and whether the recorded column mapping changes across firmware versions.
- Appropriate, explicitly declared pathlength assumptions and extinction-coefficient conventions for the intended exploratory calculation.

The physical channel mapping and geometry can be established once per supported instrument/firmware/decoder configuration and reused. Each recording still has its own baseline, coverage, source identity and observable timing/quality findings. Biological pathlength factors remain model assumptions and are disclosed in the result.

## What this release provides

Raw optical trends, descriptive statistics, full and engineering-screened exploratory spectra, automatic shorter-window fallback, and automatic instrument-profile identification work without an HbO/HbR profile. A supported verified conversion profile enables relative hemoglobin estimates through the existing conversion calculation and an automatically created recording binding. The bundled Athena raw profile states the missing information and does not substitute guessed wavelength pairs or distances.

The report explains unavailable outputs individually. Recording and raw optical exploration remain usable while conversion information is incomplete. An optical signal change is not by itself a measurement of cortical oxygenation, oxygen saturation, or cognitive effort.
