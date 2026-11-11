# Attribution guide

**Current application: [Public Alpha 11.12.0](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.12.0). Focused attribution check: 11 November 2026.**

Use this guide to find the references for the software, methods and materials actually used in a study. The [master attribution record](../../CITATIONS_AND_ATTRIBUTION.md) contains the project citation and retained source reviews; the [research bibliography](../../research/bibliography/README.md) supplies method and software references.

## Current evidence and where to find it

| Record | Purpose and scope |
| --- | --- |
| [Public Alpha 11.12.0 release](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.12.0) and [release attribution ledger](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.12.0/RELEASE_11_12_0_ATTRIBUTION.md) | Current archive, adaptation boundaries and Literary Pilot v3 provenance. The [11.12.0 bibliography](../../research/bibliography/README.md#public-alpha-11120-citation-scope) identifies retained software credits and all four literary source editions. |
| [Public Alpha 11.10.1 release](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.10.1) | The off-body recorder uses LabRecorder to save the XDF and pyxdf to reopen it. The [expanded attribution guide](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.10.1/ATTRIBUTION_ALPHA_11_4_1.md) carries forward the optical correction and upstream method credits. |
| [Public Alpha 11.10.0 release](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.10.0) and [Cerelog / Decoder Gate guide](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.10.0/CERELOG_DGA_WORKFLOW.md) | 11.10.0 software citation, compact connector provenance and new behavioral pilot. Cite the actual profile, protocol revision and release. |
| [Public Alpha 11.9.2 release](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.9.2) | The application ZIP, checksum, updater companion and separately published attribution guide. Cite the version actually used. |
| [11.9.2 source manifest](../../workbench/docs/releases/alpha-11.9.2/SOURCE_MANIFEST.json) and [build report](../../workbench/docs/releases/alpha-11.9.2/package/BUILD_REPORT.md) | Exact release identity and stated software checks; neither is a complete scholarly or transitive-license audit. |
| [Expanded optical and upstream attribution guide](alpha-11.4.1/package/app/docs/ATTRIBUTION_ALPHA_11_4_1.md) | The 11.4.1 correction and full NeuroKit2, MNE/EEGLAB, ASRpy, ICLabel, Pycrostates and SPAR-EEG references. The same guide is a separate download for both 11.9.2 and 11.10.0; neither application ZIP embeds it. |
| [11.4.1 correction evidence](alpha-11.4.1/README.md) | The original optical-credit fix, selected registry/source snapshot and its evidence boundaries. |
| [11.2.2 supplement](alpha-11.2.2/README.md) and [11.2.1 source review](alpha-11.2.1/README.md) | Earlier release and dependency reviews. Their statements about absent routes and inspected versions remain historical. |
| [Third-party notices](../../THIRD_PARTY_NOTICES/README.md) | Upstream rights and notices, distinct from bibliographic references. Preserve notices with redistributed components. |

## Focused 11.12.0 check

The checked public ZIP is **46,509,219 bytes**, SHA-256 `d2980869ce3e3a1693a7efcee6f0859ef07b3d561874f46cde23c313f7e6d684`. Its active `app/config/attribution_registry_v1.json` has SHA-256 `4f25e299a0fcf7135183354b7471c8a2ce8fbaed48d1b719e2450082fcf739fc`, matching the earlier registry identified below: 41 modules and 34 methods, including the corrected Delpy optical citation and separate MNE tutorial credit. The pending method-level review for `protocol_evidence_v1_0` is unchanged. This check covers selected requirements, source routes, attribution records and literary materials; it does not extend the older comprehensive review to all newer code or dependencies.

Core still declares NeuroKit2 0.2.13, PyWavelets 1.9.0 and mne-denoise 0.0.3. Signal Extras still declares MNE 1.11.0, ASRpy 0.0.8, MNE-ICALabel 0.10.0, Pycrostates 0.6.1 and eeglabio 0.1.2. Retain implementation and original-method credits according to actual use. The [preserved expanded guide](alpha-11.4.1/package/app/docs/ATTRIBUTION_ALPHA_11_4_1.md) supplies those references; it is not embedded in the 11.12.0 ZIP or listed among that release's assets.

Decoder Gate Literary Pilot v3 credits Hoyt Banks for the November 10, 2026 local protocol design and separately credits Baum, Nesbit, Alcott and O. Henry for 38 literary passage records from four Project Gutenberg editions. Within `app/tools/Decoder_Gate_Pilot_v3_0/`, preserve `SOURCES_AND_CREDITS.html`, `materials/participant_bank.json` and `notices/PROJECT_GUTENBERG_LICENSE.txt`. The source records and license travel with the component. Its protocol-level attribution does not create a global method-registry entry or validate the pilot's measures. The [bibliography](../../research/bibliography/README.md#decoder-gate-literary-pilot-v3) gives source editions, citation and adaptation boundaries.

## Retained earlier checks

The 11.10.0 active credit registry, packaged master citation file and all 234 bundled third-party notice files match 11.9.2 byte for byte. The new Decoder Gate protocol credits Hoyt Banks for the October 30, 2026 PRAYCG pilot design. The compact Cerelog connector records its source files and adaptations in `compact_backend/PORT_PROVENANCE.json`; use the [bibliography](../../research/bibliography/README.md#public-alpha-11100-citation-scope) for the in-archive paths. This comparison does not resolve the pending protocol-evidence method credits or revisit the licenses of every dependency.

The checked 11.9.2 ZIP is **44,734,605 bytes**, SHA-256 `b63a7f071e243d0d3a09a77600387d9c4082148c33f4aae68bff21af0446324c`. The focused review inspected its active `app/config/attribution_registry_v1.json`, selected Signal Review sources and method inventories, Core requirements and optional Signal Extras requirements. The registry SHA-256 is `4f25e299a0fcf7135183354b7471c8a2ce8fbaed48d1b719e2450082fcf739fc`. This identifies the inspected record; it does not replace execution evidence.

## Credits retained in 11.9.2

- **Optical:** the corrected `optical_verified_relative_hemoglobin` entry retains the six-author Delpy citation and separate MNE fNIRS context reference unchanged from 11.4.1. Instrument mapping, wavelengths, pathlength assumptions, coefficients and baseline remain necessary; the Athena profile remains raw-only.
- **NeuroKit2:** Core requirements retain 0.2.13. Credit the actual ECG, respiration, PPG, EDA, HRV or paired-signal RSA operation and its method sources. Native PRAYCG phase/RR association has a separate definition.
- **EEGLAB and optional EEG methods:** file import through MNE, eeglabio support, ASRpy 0.0.8, MNE-ICALabel 0.10.0 and Pycrostates 0.6.1 retain their own software and method credits. A MATLAB EEGLAB runtime is not bundled. ICLabel requires both the Python implementation and model references; modified k-means requires both Pycrostates and its method lineage.
- **Denoising and numerical methods:** retain the actual implementation, selected recipe and upstream notices. The Core requirements still pin mne-denoise 0.0.3 and PyWavelets 1.9.0. A smoother output or a successfully imported library does not establish physiological validity or actual use in a reported result.
- **PRAYCG adaptations:** keep their versioned definitions and differences visible alongside upstream authors. The [methods catalog](../../research/methods.md) points to original specifications; its detailed implementation inspection remains scoped to 11.2.1.

## Before citing a study

Record the application edition/version and archive hash, locked protocol revision, source recording and actual installed software versions. Select references from the methods that completed and contributed to the report, retaining parameters, component availability, exclusions and any manual adoption decision. Planned, skipped, failed or unavailable analyses do not become executed methods because their names appear in a registry.

The identical 11.9.2 and 11.10.0 registries contain `protocol_evidence_v1_0` with no method-level entries and the explicit state `MODULE_REGISTERED_METHOD_LEVEL_ATTRIBUTION_REVIEW_PENDING`. Its static import declaration is not complete automatic credit coverage. Preserve the protocol's original sources and per-result method descriptions and review the resulting Methods and Credits before publication.

For research definitions, cite the original document and exact method version. For reused stimuli, retain the [edition-specific media credits](../../examples/stimulus-masters/README.md). Original papers, older receipts, versioned reviews and license notices remain unchanged by this maintained guide.

[Sources and history](../README.md) · [Master citations](../../CITATIONS_AND_ATTRIBUTION.md) · [Bibliography](../../research/bibliography/README.md) · [Workbench](../../workbench/README.md)
