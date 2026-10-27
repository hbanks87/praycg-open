# Attribution guide

**Current application: Public Alpha 11.9.2. Guidance reviewed 26 October 2026.**

Use this guide to find the references for the software, methods and materials actually used in a study. The [master attribution record](../../CITATIONS_AND_ATTRIBUTION.md) contains the project citation and retained source reviews; the [research bibliography](../../research/bibliography/README.md) supplies method and software references.

## Current evidence and where to find it

| Record | Purpose and scope |
| --- | --- |
| [Public Alpha 11.9.2 release](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.9.2) | The application ZIP, checksum, updater companion and separately published attribution guide. Cite the version actually used. |
| [11.9.2 source manifest](../../workbench/docs/releases/alpha-11.9.2/SOURCE_MANIFEST.json) and [build report](../../workbench/docs/releases/alpha-11.9.2/package/BUILD_REPORT.md) | Exact release identity and stated software checks; neither is a complete scholarly or transitive-license audit. |
| [Expanded optical and upstream attribution guide](alpha-11.4.1/package/app/docs/ATTRIBUTION_ALPHA_11_4_1.md) | The 11.4.1 correction and full NeuroKit2, MNE/EEGLAB, ASRpy, ICLabel, Pycrostates and SPAR-EEG references. The same guide is a separate 11.9.2 release asset; it is not inside the 11.9.2 ZIP. |
| [11.4.1 correction evidence](alpha-11.4.1/README.md) | The original optical-credit fix, selected registry/source snapshot and its evidence boundaries. |
| [11.2.2 supplement](alpha-11.2.2/README.md) and [11.2.1 source review](alpha-11.2.1/README.md) | Earlier release and dependency reviews. Their statements about absent routes and inspected versions remain historical. |
| [Third-party notices](../../THIRD_PARTY_NOTICES/README.md) | Upstream rights and notices, distinct from bibliographic references. Preserve notices with redistributed components. |

The checked 11.9.2 ZIP is **44,734,605 bytes**, SHA-256 `b63a7f071e243d0d3a09a77600387d9c4082148c33f4aae68bff21af0446324c`. The focused review inspected its active `app/config/attribution_registry_v1.json`, selected Signal Review sources and method inventories, Core requirements and optional Signal Extras requirements. The registry SHA-256 is `4f25e299a0fcf7135183354b7471c8a2ce8fbaed48d1b719e2450082fcf739fc`. This identifies the inspected record; it does not replace execution evidence.

## Credits retained in 11.9.2

- **Optical:** the corrected `optical_verified_relative_hemoglobin` entry retains the six-author Delpy citation and separate MNE fNIRS context reference unchanged from 11.4.1. Instrument mapping, wavelengths, pathlength assumptions, coefficients and baseline remain necessary; the Athena profile remains raw-only.
- **NeuroKit2:** Core requirements retain 0.2.13. Credit the actual ECG, respiration, PPG, EDA, HRV or paired-signal RSA operation and its method sources. Native PRAYCG phase/RR association has a separate definition.
- **EEGLAB and optional EEG methods:** file import through MNE, eeglabio support, ASRpy 0.0.8, MNE-ICALabel 0.10.0 and Pycrostates 0.6.1 retain their own software and method credits. A MATLAB EEGLAB runtime is not bundled. ICLabel requires both the Python implementation and model references; modified k-means requires both Pycrostates and its method lineage.
- **Denoising and numerical methods:** retain the actual implementation, selected recipe and upstream notices. The Core requirements still pin mne-denoise 0.0.3 and PyWavelets 1.9.0. A smoother output or a successfully imported library does not establish physiological validity or actual use in a reported result.
- **PRAYCG adaptations:** keep their versioned definitions and differences visible alongside upstream authors. The [methods catalog](../../research/methods.md) points to original specifications; its detailed implementation inspection remains scoped to 11.2.1.

## Before citing a study

Record the application edition/version and archive hash, locked protocol revision, source recording and actual installed software versions. Select references from the methods that completed and contributed to the report, retaining parameters, component availability, exclusions and any manual adoption decision. Planned, skipped, failed or unavailable analyses do not become executed methods because their names appear in a registry.

The 11.9.2 registry contains `protocol_evidence_v1_0` with no method-level entries and the explicit state `MODULE_REGISTERED_METHOD_LEVEL_ATTRIBUTION_REVIEW_PENDING`. Its static import declaration is not complete automatic credit coverage. Preserve the protocol's original sources and per-result method descriptions and review the resulting Methods and Credits before publication.

For research definitions, cite the original document and exact method version. For reused stimuli, retain the [edition-specific media credits](../../examples/stimulus-masters/README.md). Original papers, older receipts, versioned reviews and license notices remain unchanged by this maintained guide.

[Sources and history](../README.md) · [Master citations](../../CITATIONS_AND_ATTRIBUTION.md) · [Bibliography](../../research/bibliography/README.md) · [Workbench](../../workbench/README.md)
