# PRAYCG Workbench Alpha 10.5.3

Complete Workbench release published October 9, 2026. Adds shared **Visual Analysis** while retaining the normal installers, acquisition/recording tools, Live Monitor, protocol library, Gamma Scalpel, optical exploration and Analysis Forge.

## Changes since 10.5.2

- Four native linked views: **PRAYCG 3 Review**, **Time–Frequency**, **State landscape** and **Timescale inspector**, using one recording identity and cursor.
- Verified completed JSON attachment, recorded prefix replay and passive live viewing, with explicit source mapping, units, calibration, supported windows and availability. Seeking or changing sources resets/rebuilds history.
- Separates completed CAI and historical NIP from experimental Autonomic state. Raw EEG/RR leaves missing CAI, NIP and CAI-SID components unavailable.
- Separates gamma threshold events, delayed theta responses, media landmarks and inspection bookmarks. Original review and TFR workflows retain optional shared-cursor links.
- Adds **START.bat** alongside **START_PRAYCG.bat**, and records source/method/display context for visual review.

## Download and install

Download **PRAYCG_Workbench_Alpha_10_5_3.zip** and its SHA-256 sidecar. Extract the complete package into a new writable folder, run **INSTALL.bat**, then **START.bat** or **START_PRAYCG.bat**. Optional Zuna uses **INSTALL_ZUNA.bat**. Keep studies outside the release folder and close LabRecorder before analyzing an XDF.

[Installation guide](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.3/workbench/docs/releases/alpha-10.5.3/INSTALL_AND_WORKFLOW_ALPHA_10_5_3.md) · [Visual Analysis guide](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.3/workbench/docs/releases/alpha-10.5.3/VISUAL_ANALYSIS_ALPHA_10_5_3.md) · [Cumulative changelog](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.3/workbench/CHANGELOG.md) · [Complete changelog and evidence](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.3/workbench/docs/releases/alpha-10.5.3/README.md)

## Verification and limitations

Current shipped regression: **4,249 unique tests passed**, six skipped, zero failures/errors across nine groups. Native visual acceptance is recorded separately; 91 protocol definitions retain software certification. Fresh publication review: **57 focused visual tests passed**. ZIP CRC passes for all **1,783 files**; all **1,781 distribution-manifest entries** and shipped checksums match.

The default incremental visual recipe requires P7/P8 for gamma and Pz/P3/P4 for theta. Athena's four measured electrodes cannot supply these defaults. The surface is exploratory and does not establish an attractor, narrative absorption or physiological validity. The bundled Athena optical profile remains raw-only.

No fresh full installation, physical acquisition/timing or optional Zuna inference is claimed. Earlier SDK, installation, acquisition and reconstruction records retain their original scope. Private recordings, replay arrays and private screenshots are excluded.

**Metadata note:** the unchanged source manifest retains an inherited `release_date` of `2026-09-30`; the actual publication date is **October 9, 2026**. Current 10.5.3 identity, source hashes and validation records are preserved. Historical attribution headers remain historical; the repository's current attribution supplement documents this version.

**ZIP SHA-256:** `5b440d596afc17ae4b13ed7a5ef3084f543595ec7137d97694114c689dc10e38`
