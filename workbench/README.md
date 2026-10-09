# PRAYCG Workbench

PRAYCG Workbench is local-first research software for taking a study from its question and materials to a reviewable results package. The desktop application, called **Control Center**, connects protocol selection, stimulus preparation, hardware streams, acquisition, analysis and research exchange while keeping the identity and history of those steps available for inspection.

The [PRAYCG Neuro Research Program](../research/README.md) uses this infrastructure for particular hypotheses and protocols. Researchers can use the Workbench without adopting those hypotheses.

## Start with Alpha 10.5.3

1. Get the [Alpha 10.5.3 complete release and SHA-256 checksum](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.5.3).
2. Read [installation and first launch](docs/installation.md), including the Python and external-application requirements.
3. Follow the [study workflow](docs/workflow.md).
4. Review [hardware support and its limits](docs/hardware-support.md) before selecting an acquisition route.

Extract the complete ZIP into a new writable folder. Run **INSTALL.bat**, then **START.bat** or **START_PRAYCG.bat**. Core, Live Monitor and Hardware Connectors use separate environments; optional Zuna uses **INSTALL_ZUNA.bat**. The source, bundled recorder, launchers, documentation and release evidence are inside the ZIP. See [development guidance](development/README.md) for working from that package.

Alpha 10.5.3 adds **Visual Analysis** with four linked native views, verified completed JSON attachment, recorded prefix replay and passive live feeds. Source identity, actual electrodes, units, fixed calibration and unavailable values remain visible. Raw EEG/RR cannot supply missing CAI, NIP or CAI-SID components. The default visual gamma/theta recipe requires P7/P8 and Pz/P3/P4 respectively; Athena's four measured electrodes do not supply those defaults. The [Visual Analysis guide](docs/releases/alpha-10.5.3/VISUAL_ANALYSIS_ALPHA_10_5_3.md) explains supported sources and interpretation.

The existing **Recording → Analyze → Results** workflow, Gamma Scalpel 2.0, optical exploration, Live Time–Frequency, finalized-XDF replay and recording with cautions remain available. Read the [changelog](CHANGELOG.md) and [current release notes](docs/releases/alpha-10.5.3/RELEASE_NOTES_v1_0_0_alpha_10_5_3.md).

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
- [Current Visual Analysis methods](docs/releases/alpha-10.5.3/VISUAL_ANALYSIS_ALPHA_10_5_3.md)
- [Retained Gamma and optical Forge methods](docs/releases/alpha-10.5.2/ANALYSIS_FORGE_ALPHA_10_5_2.md)
- [Gamma Scalpel methods and reference profiles](docs/releases/alpha-10.5.2/Gamma_Scalpel_v2_0/README.md)
- [Optical methods and instrument profiles](docs/releases/alpha-10.5.2/Optical_Signal_Review_v1_0/README.md)
- [Earlier analysis methods and limitations](../docs/attribution/ANALYSIS_METHODS.md)
- [Citations and attribution](../CITATIONS_AND_ATTRIBUTION.md)

The [Alpha 10.5.3 guide collection](docs/releases/alpha-10.5.3/README.md) mirrors current documentation, with links adapted for repository browsing. Its build receipt records 4,249 passing tests and six skips, with separately recorded native visual acceptance. Earlier SDK, installation, acquisition and reconstruction evidence retains its historical scope. This release adds no fresh full installation, physical timing or physiological validation. The bundled Athena optical profile remains raw-only. Earlier guide collections and [attribution evidence](../docs/attribution/) retain their original scope.

## Data and reporting

Keep study workspaces, recordings, private bundles and backups outside the application release folder. Public export requires review of consent, sharing authority, media rights and identifiers; a hash verifies byte identity, and is not an anonymization or permission check.

For a problem report, include the exact release, action attempted, session mode, protocol and hardware route, error text and a minimal non-sensitive reproduction. Keep participant recordings, credentials, device identifiers and private paths out of public issues.

[Repository home](../README.md) · [Contributing](../CONTRIBUTING.md) · [License](../LICENSE.md) · [Third-party notices](../THIRD_PARTY_NOTICES/)
