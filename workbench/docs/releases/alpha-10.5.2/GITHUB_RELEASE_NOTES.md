# PRAYCG Workbench Alpha 10.5.2

Complete Workbench release dated October 8, 2026, with Gamma Scalpel 2.0 and adaptive optical exploration. Includes the normal installers, application source, bundled timing-patched LabRecorder, protocol library, method guides, attribution and validation records.

## New in 10.5.2

- **Gamma Scalpel 2.0:** one Forge action using measured EEG and optional recorded EOG/EMG references. Checks participant/source identity, units, continuity, reference quality and timing. Reports original and screened gamma, retained duration and supported matched-duration condition comparisons. Athena results use its measured TP9, AF7, AF8 and TP10 electrodes.
- **Optical exploration:** whole-recording defaults independent of EEG quality, automatic 30-, 10- or 5-second spectral windows, preserved gaps, and matching full/screened resolution. Raw trends remain available when spectra are unsupported.
- **Reusable instrument profiles:** versioned instrument facts with recording-specific bindings and baselines. Verified conversion profiles can enable relative HbO/HbR; the bundled Athena profile supports raw exploration because required conversion facts remain unresolved.
- **Forge workflow:** persistent Recording → Analyze → Results, shared progress/cancel/retry, source and scope settings saved with each attempt, and corrected saved-tool migration from earlier public folders.

## Included since the previous published release, 10.4.10

- **10.5.0:** live electrode-specific Time–Frequency views and an offline Forge Explorer, recorded quality/support information, compatible recording comparisons and exportable reports.
- **10.5.1:** optional longer signal checks, brief actual-data recording readiness and Record with cautions; reorganized Forge; full-rate finalized-XDF replay; raw optical trends/spectra; and source-bound scoped Athena EEG transport/recording admission.

The [cumulative changelog](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.2/workbench/CHANGELOG.md) and [complete packaged changelog](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.2/workbench/docs/releases/alpha-10.5.2/CHANGELOG.md) retain earlier changes. The repository's download, installation, workflow, hardware, development, history and attribution pages now describe the current release.

## Install

Download **PRAYCG_Workbench_Alpha_10_5_2.zip** and its **.sha256.txt** sidecar from the release assets. Extract into a new writable folder, run **INSTALL.bat**, then **START_PRAYCG.bat**. Optional Zuna uses **INSTALL_ZUNA.bat**. Keep existing recordings and studies outside the application folder. Stop LabRecorder and let the XDF close before analysis.

[Installation and workflow](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.2/workbench/docs/releases/alpha-10.5.2/INSTALL_AND_WORKFLOW_ALPHA_10_5_2.md) · [Forge guide](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.2/workbench/docs/releases/alpha-10.5.2/ANALYSIS_FORGE_ALPHA_10_5_2.md) · [Methods and current guides](https://github.com/hbanks87/praycg-open/blob/PRAYCG_Workbench_A10.5.2/workbench/docs/releases/alpha-10.5.2/README.md)

## Verification and scope

- Shipped build receipt: **4,192 unique passing tests, six skips, zero failures/errors**. Separate pinned BrainFlow SDK acceptance: **89 passed**. Full isolated Core/Live Monitor/Hardware installation acceptance and **91 protocol definitions** retain their recorded scope.
- Fresh release review: **98 focused tests passed** for Gamma, optical exploration and Forge integration. ZIP CRC passes for all **1,765 files**; all **1,763 distribution-manifest entries** and shipped checksums match.
- Current documentation links were checked against the repository and the full Git tree, including paths omitted by the local sparse checkout.

Reference screening is exploratory and does not establish that remaining gamma is neural. The bundled Athena optical profile does not enable HbO/HbR. No new physical Cerelog–Athena timing or physiological validation is claimed. Optional Zuna installation/inference and installation of this exact extracted delivery were not repeated in the repository review; existing acceptance records state what was actually checked.

**ZIP SHA-256:** `fc86175ab71aaa230456190c0b8b01caf3f5e5926db85ad5a92448c0ac009318`
