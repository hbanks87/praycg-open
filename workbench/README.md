# PRAYCG Workbench

PRAYCG Workbench is local-first research software for taking a study from its question and materials to a reviewable results package. The desktop application, called **Control Center**, connects protocol selection, stimulus preparation, hardware streams, acquisition, analysis and research exchange while keeping the identity and history of those steps available for inspection.

The [PRAYCG Neuro Research Program](../research/README.md) uses this infrastructure for particular hypotheses and protocols. Researchers can use the Workbench without adopting those hypotheses.

## Start with Alpha 10.5.2

1. Get the [Alpha 10.5.2 complete release and SHA-256 checksum](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.5.2).
2. Read [installation and first launch](docs/installation.md), including the Python and external-application requirements.
3. Follow the [study workflow](docs/workflow.md).
4. Review [hardware support and its limits](docs/hardware-support.md) before selecting an acquisition route.

Extract the complete ZIP into a new writable folder. Run **INSTALL.bat**, then **START_PRAYCG.bat**. Core, Live Monitor and Hardware Connectors use separate environments; optional Zuna uses **INSTALL_ZUNA.bat**. The source, bundled recorder, launchers, documentation and release evidence are inside the ZIP. See [development guidance](development/README.md) for working from that package.

Alpha 10.5.2 adds **Gamma Scalpel 2.0** with optional measured EOG/EMG reference screening and **Explore optical signals** with whole-recording defaults, automatic 30/10/5-second spectral windows and reusable instrument profiles. The Forge keeps its **Recording → Analyze → Results** workflow. Live Time–Frequency, finalized-XDF replay, recording with cautions and the improved recording comparisons from 10.5.0 and 10.5.1 are included. Read the [changelog](CHANGELOG.md) and [current release notes](docs/releases/alpha-10.5.2/RELEASE_NOTES_v1_0_0_alpha_10_5_2.md).

PRAYCG is alpha research software. Software checks do not establish scientific validity, participant safety, physical timing or clinical suitability. Consult the [project disclaimer](../DISCLAIMER.md) and the exact release's instructions.

## From a question to a research package

| Stage | What the Workbench connects |
| --- | --- |
| Prepare | Persistent study workspace, versioned protocol, required materials and stimulus fingerprints |
| Acquire | Reviewed hardware profile, equipment-session identity, live checks, locked runner and external LabRecorder recording |
| Analyze | Recording and source checks, module-specific quality/coverage decisions and persistent per-module results |
| Review | Reports, figures, execution receipts, estimability and plain-language findings |
| Exchange | Local results packages, private study bundles and explicitly reviewed Research Exchange exports |

Analysis Forge keeps an unavailable estimate distinguishable from a numerical result. Preserve `NOT_ESTIMABLE`, failed checks and warnings when interpreting outputs. A completed software workflow does not by itself validate an endpoint.

The Workbench also supports protocol and EEG-recipe document packs for AI-assisted authoring. Returned proposals pass through the documented review, validation and installation workflow. New device code, acquisition engines and numerical estimators remain development work.

## Documentation and materials

- [Installation and repair](docs/installation.md)
- [Workflow, analysis, recovery and exchange](docs/workflow.md)
- [Hardware routes and evidence boundaries](docs/hardware-support.md)
- [Physical hardware projects](../hardware/README.md)
- [Example stimuli and recipes](../examples/README.md)
- [Development and release provenance](development/README.md)
- [Workbench roadmap](roadmap.md)
- [Current Forge methods](docs/releases/alpha-10.5.2/ANALYSIS_FORGE_ALPHA_10_5_2.md)
- [Gamma Scalpel methods and reference profiles](docs/releases/alpha-10.5.2/Gamma_Scalpel_v2_0/README.md)
- [Optical methods and instrument profiles](docs/releases/alpha-10.5.2/Optical_Signal_Review_v1_0/README.md)
- [Earlier analysis methods and limitations](../docs/attribution/ANALYSIS_METHODS.md)
- [Citations and attribution](../CITATIONS_AND_ATTRIBUTION.md)

The [Alpha 10.5.2 guide collection](docs/releases/alpha-10.5.2/README.md) mirrors the shipped current documentation, with links adapted for repository browsing. Its build receipt records 4,192 passing tests and six skips; a separate pinned-SDK check passed 89 tests. A fresh repository review also passed 98 focused Gamma, optical and Forge tests and verified the archive and its manifests. These records retain their declared software and offline scope. The bundled Athena optical profile remains raw-only, and this release adds no physical Cerelog–Athena timing or physiological validation. Earlier guide collections and [attribution evidence](../docs/attribution/) retain their historical scope.

## Data and reporting

Keep study workspaces, recordings, private bundles and backups outside the application release folder. Public export requires review of consent, sharing authority, media rights and identifiers; a hash verifies byte identity, and is not an anonymization or permission check.

For a problem report, include the exact release, action attempted, session mode, protocol and hardware route, error text and a minimal non-sensitive reproduction. Keep participant recordings, credentials, device identifiers and private paths out of public issues.

[Repository home](../README.md) · [Contributing](../CONTRIBUTING.md) · [License](../LICENSE.md) · [Third-party notices](../THIRD_PARTY_NOTICES/)
