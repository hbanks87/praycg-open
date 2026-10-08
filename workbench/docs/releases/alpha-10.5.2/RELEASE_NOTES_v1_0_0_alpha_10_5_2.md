# PRAYCG Workbench Alpha 10.5.2

This complete release adds Gamma Scalpel 2.0 and makes optical exploration adapt to the available recording. The Forge keeps its Recording → Analyze → Results workflow.

## Gamma Scalpel

Choose **Gamma Scalpel** in Analyze. It uses the EEG electrodes actually recorded and automatically checks for compatible EMG/EOG references in the same XDF. The result identifies its reference mode, the available electrode support, measured muscle/eye activity, and the original and reference-screened gamma results.

Suitable Cerelog and other labeled reference streams can be used. Missing, ambiguous, poorly supported or incorrectly assigned references have an explicit reason. Reference quality and independent-clock timing remain visible. Automatic signal subtraction is not part of this release; the comparisons preserve measured EEG. The previous Master Suite method remains available for comparison.

Athena results identify TP9, AF7, AF8 and TP10 individually. Outcomes requiring unavailable regional electrodes remain unavailable.

## Optical exploration

Choose **Explore optical signals** in Analyze. The default covers the whole selected optical recording, independently of EEG QC. Details contains the optional task scope, source selection and spectral preset. The same source and settings are saved with each attempt.

Automatic spectra use 30-second windows when possible and fall back to labeled 10- or 5-second windows. Full and screened spectra use the same selected resolution. Raw trends and descriptive statistics remain available when no complete spectral window is supported. Gaps remain gaps, and shorter windows have a correspondingly restricted frequency interpretation.

A reusable instrument profile can now hold fixed channel mapping and conversion information. The Workbench automatically creates the recording-specific binding and baseline. Verified conversion profiles enable relative HbO/HbR with their declared assumptions. The bundled Athena p1041 raw profile identifies the known connector configuration and explains unresolved mapping, geometry and intensity information. It does not enable Athena hemoglobin estimates until that information is established. Read the [source review](ATHENA_OPTICAL_SOURCE_REVIEW_ALPHA_10_5_2.md).

## Installation and verification

Extract the complete ZIP into a new writable folder. Run **INSTALL.bat**, then **START_PRAYCG.bat**. Core, Live Monitor and Hardware Connectors use separate environments. Optional Zuna uses **INSTALL_ZUNA.bat**.

The release includes public workflow and method guides, versioned profiles, software regression evidence and package checksums. The current acceptance receipt distinguishes synthetic numerical checks and offline checks of existing Athena recordings from physical validation. The unchanged Athena acquisition route retains its original scoped evidence. Cerelog physical qualification and measured Cerelog–Athena timing have separate requirements.
