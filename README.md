# PRAYCG

**An open, local-first neuroscience workbench and an independently reviewable neuroscience research program.**

PRAYCG connects study preparation, synchronized acquisition, protocol execution, analysis and research exchange. Alongside the software, the Neuro Research Program develops testable questions about naturalistic stimuli, meaning, task stance and physiological state.

Using the Workbench does not require agreement with a research theory. Running a protocol does not establish that its hypotheses are correct.

## Choose your starting point

| I want to… | Start here |
| --- | --- |
| Install the software and run a study or demonstration | [PRAYCG Workbench](workbench/README.md) |
| Read the theories, protocols and research questions | [PRAYCG Neuro Research Program](research/README.md) |
| Follow Opto-PING and its synthetic tests | [Opto-PING research](research/optoping/README.md) |
| Trace the research ladders and individual rungs | [Ladders and rungs](research/ladders/README.md) |
| Find reproduction scripts, locked specifications and reference outputs | [Reproducibility programs](research/reproducibility/README.md) |
| Understand the project's concepts and calculations | [Research concepts](research/concepts/README.md) · [Algorithm and implementation guide](research/algorithms/README.md) |
| Browse original theory documents and earlier versions | [Theory reading index](research/theory/README.md) |
| Review device builds, sensor holders and experimental integrations | [Hardware projects](hardware/README.md) |
| Find synthetic demonstrations and stimulus recipes | [Examples](examples/README.md) |
| Find the original stimulus masters and bridge video | [Eleven-master catalog](examples/stimulus-masters/README.md) · [Demo Lantern Bridge](examples/bridge-demo/README.md) |
| Review authorship, sources and reuse boundaries | [Master citations and attribution](CITATIONS_AND_ATTRIBUTION.md) · [Current bibliography](research/bibliography/README.md) |

## PRAYCG Workbench

The Workbench helps preserve protocol, stimulus, hardware, stream, analysis and output identities. Its purpose is to make methods and limitations visible enough for other people to inspect, reproduce and challenge.

**Current public release: [Public Alpha 11.6.0 Revision 1](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.6.0).** This release adds explicit processing comparisons, paired CAI/SID feature regeneration where supported, clearer report coverage and measured reference/timing evidence. Revision 1 fixes the Windows startup check used during signed update preparation. See the [release guide](workbench/docs/releases/alpha-11.6.0/README.md), [changelog](workbench/CHANGELOG.md) and [processing workflow](workbench/docs/releases/alpha-11.6.0/package/WORKFLOW_COMPLETION_11_6.md). It retains the [11.4.1 optical-credit correction and attribution guide](docs/attribution/alpha-11.4.1/README.md), [current bibliography](research/bibliography/README.md), optional seven-film plus original Lantern installer, and public research collections.

## PRAYCG Neuro Research Program

The research program investigates controlled differences in audiovisual structure, narrative reception and analytic task demands. Its library preserves hypotheses, operational definitions, protocol explanations and exploratory study records.

Readers are invited to examine assumptions, identify confounds, propose falsifiable alternatives and attempt replication. Historical documents retain their original context; their preservation is not a declaration that every proposed mechanism is supported.

[Research program](research/README.md) · [Theory library](research/theory/README.md) · [Protocols](research/protocols/README.md) · [Measures](research/measures/README.md) · [Studies](research/studies/README.md)

[Opto-PING](research/optoping/README.md) · [Ladders and rungs](research/ladders/README.md) · [Reproducibility programs](research/reproducibility/README.md)

[Research concepts and definitions](research/concepts/README.md) · [Algorithms, inputs and implementation versions](research/algorithms/README.md)

The research indexes bring the preserved Opto-PING Rungs 0J–0O, external reproduction handoff, null controls, calibration and locked reproduction back into the main navigation. Earlier rungs described in the source documents remain visible with their artifact availability stated explicitly. See the [combined repository update](docs/updates/2026-10-14-public-workflow-release.md) and its [preserved research review](docs/updates/2026-10-13-public-research-update.md) for coverage and remaining gaps.

## Repository layout

```text
workbench/              Current software package, user guides and development orientation
research/               Theory, protocols, measures, studies and preserved research collections
hardware/               Device projects, source, firmware, CAD and project-specific evidence
examples/               Synthetic demonstration resources and stimulus recipes
docs/                   Project history, attribution evidence and reorganization records
THIRD_PARTY_NOTICES/     Preserved upstream notice texts
archive/                Earlier software and operating guides
```

The folder layout inside the application ZIP is different. Follow its installation instructions rather than running an arbitrary archived component.

## Research-use boundaries

PRAYCG is not a medical or diagnostic system. Appropriate scientific, ethical, consent, privacy and equipment review remains necessary. Software completion, a matching checksum or a successful connection does not establish scientific validity or participant safety.

Private study bundles may contain sensitive recordings, identifiers or copyrighted material. Bundle creation does not authorize publication.

## History and contributions

Every file from the reviewed repository snapshot is preserved byte-for-byte at a recorded destination, including every theory version and duplicate. New navigation pages and corrected attribution links are documented separately. Original copies of replaced root navigation files are retained in project history.

[Complete original-file locator](docs/reorganization/original-file-index.md) · [Reorganization and verification](docs/reorganization/README.md) · [Historical releases](docs/release-history/README.md)

[Contributing](CONTRIBUTING.md) · [Code of conduct](CODE_OF_CONDUCT.md) · [Disclaimer](DISCLAIMER.md) · [License](LICENSE.md) · [Project vision](docs/project-vision.md)

PRAYCG development and protocol adaptation: Hoyt Banks. Upstream work remains credited to its authors and rights holders.
