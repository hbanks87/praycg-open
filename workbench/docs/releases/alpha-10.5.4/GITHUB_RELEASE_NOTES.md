# PRAYCG Workbench Alpha 10.5.4

Complete Workbench release published October 9, 2026. Improves Visual Analysis setup and restores the required Athena admission evidence in the public package.

## Changes since 10.5.3

- Places **Visual Analysis** beside **Time–Frequency** in Live Monitor and immediately after **Analyze** in Analysis Forge.
- Repairs recorded-XDF **Visual sources**, keeps source selection available while streams load, and displays selection failures. Empty profile drafts explain that a device must be selected.
- Adds an explicit calibration start offset, default 0, with an option to use the selected EEG stream's recorded start. The shared recording origin, minimum valid support and gap checks remain unchanged. Experimental streaming visual-state/API-A methods are versioned v1.1.
- Restores the exact retained **10.5.1 Athena EEG admission receipt** required by the **Human connected** profile path. Missing or altered evidence is still rejected; this repair adds no new device qualification.
- Audits recursive hardware/analysis hash dependencies and local runtime configuration paths on source, public and extracted layouts. Includes positive and negative packaged admission tests.

The four shared Visual Analysis views, completed-result attachment, recorded prefix replay, passive live feeds, normal installers, Gamma Scalpel, optical exploration and existing recording/analysis workflows remain available.

## Download and install

Download **PRAYCG_Workbench_Alpha_10_5_4.zip** and its SHA-256 sidecar. Extract the complete package into a new writable folder, run **INSTALL.bat**, then **START.bat** or **START_PRAYCG.bat**. Optional Zuna uses **INSTALL_ZUNA.bat**. Keep studies outside the release folder and close LabRecorder before analyzing an XDF.

[Installation guide](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.4/workbench/docs/releases/alpha-10.5.4/INSTALL_AND_WORKFLOW_ALPHA_10_5_4.md) · [Visual Analysis guide](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.4/workbench/docs/releases/alpha-10.5.4/VISUAL_ANALYSIS_ALPHA_10_5_4.md) · [Cumulative changelog](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.4/workbench/CHANGELOG.md) · [Complete changelog and evidence](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.4/workbench/docs/releases/alpha-10.5.4/README.md)

## Verification and limitations

Shipped full regression: **4,285 unique tests passed**, six skipped, zero failures/errors across all nine declared groups. Native acceptance records **93 checks** separately; 91 protocol definitions retain software certification. Fresh publication review: **93 focused checks passed**. ZIP CRC passes for all **1,791 files**; all **1,789 distribution-manifest entries** and shipped checksums match. Separate delivery evidence records **191 passing extracted tests** and runtime dependency closure on public/extracted layouts. These counts are not added to the unique full-regression total.

The default incremental visual recipe requires P7/P8 for gamma and Pz/P3/P4 for theta; Athena's four measured electrodes cannot supply those defaults. Explicit calibration offsets do not guarantee usable support. Raw EEG/RR leaves unsupported CAI, NIP and CAI-SID unavailable. Visual state remains exploratory. The bundled Athena optical profile remains raw-only.

The restored receipt retains its original single-unit EEG acquisition/recording scope. No fresh full installation, physical acquisition/timing, current SDK descriptor acceptance, optional Zuna inference or physiological validation is claimed. Private recordings, replay arrays, screenshots, environments and temporary validation outputs remain excluded.

**Metadata note:** the unchanged source manifest retains an inherited `release_date` of `2026-09-30`; the actual publication date is **October 9, 2026**. Current version identity, source hashes and validation records are preserved.

**ZIP SHA-256:** `515ae2d3de8e78c6706744146e036cec371f4f912f83c19561afbecbb2e3ce43`
