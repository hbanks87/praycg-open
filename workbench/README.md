# PRAYCG Workbench

PRAYCG Workbench is local-first research software for taking a study from its question and materials to a reviewable results package. The desktop application, called **Control Center**, connects protocol selection, stimulus preparation, hardware streams, acquisition, analysis and research exchange while keeping the identity and history of those steps available for inspection.

The [PRAYCG Neuro Research Program](../research/README.md) uses this infrastructure for particular hypotheses and protocols. Researchers can use the Workbench without adopting those hypotheses.

## Start with Alpha 10.2.1

1. Get the [Alpha 10.2.1 application ZIP](releases/alpha-10.2.1/PRAYCG_ControlCenter_v1_0_0_alpha_10_2_1.zip).
2. Read [installation and first launch](docs/installation.md), including the Python and external-application requirements.
3. Follow the [study workflow](docs/workflow.md).
4. Review [hardware support and its limits](docs/hardware-support.md) before selecting an acquisition route.

Extract the complete release into a new writable folder. The authoritative Alpha 10.2.1 application code is inside the versioned ZIP; this repository does not provide a separate extracted source tree for that release. The ZIP contains its own `app/` directory, launchers, documentation and release evidence. See [development guidance](development/README.md) for working from that package.

PRAYCG is alpha research software. Software checks do not establish scientific validity, participant safety, physical timing or clinical suitability. Consult the [project disclaimer](../DISCLAIMER.md) and the exact release's instructions.

## From a question to a research package

| Stage | What the Workbench connects |
| --- | --- |
| Prepare | Persistent study workspace, versioned protocol, required materials and stimulus fingerprints |
| Acquire | Reviewed hardware profile, equipment-session identity, live checks, locked runner and external LabRecorder recording |
| Analyze | Required quality-control checks, a dependency-aware analysis plan and persistent per-module results |
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
- [Analysis methods and limitations](../docs/attribution/ANALYSIS_METHODS.md)
- [Citations and attribution](../CITATIONS_AND_ATTRIBUTION.md)

The release guides under `docs/releases/alpha-10.2.1/` are preserved release documents. The repository's separate [attribution evidence](../docs/attribution/) records its own scope; it does not establish that a separately prepared source update was incorporated into the preserved application ZIP.

## Data and reporting

Keep study workspaces, recordings, private bundles and backups outside the application release folder. Public export requires review of consent, sharing authority, media rights and identifiers; a hash verifies byte identity, and is not an anonymization or permission check.

For a problem report, include the exact release, action attempted, session mode, protocol and hardware route, error text and a minimal non-sensitive reproduction. Keep participant recordings, credentials, device identifiers and private paths out of public issues.

[Repository home](../README.md) · [Contributing](../CONTRIBUTING.md) · [License](../LICENSE.md) · [Third-party notices](../THIRD_PARTY_NOTICES/)
