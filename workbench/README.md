# PRAYCG Workbench

PRAYCG Workbench is local-first research software for taking a study from its question and materials to a reviewable results package. The desktop application, called **Control Center**, connects protocol selection, stimulus preparation, hardware streams, acquisition, analysis and research exchange while keeping the identity and history of those steps available for inspection.

The [PRAYCG Neuro Research Program](../research/README.md) uses this infrastructure for particular hypotheses and protocols. Researchers can use the Workbench without adopting those hypotheses.

## Current release: Public Alpha 11.9.2

[Download Public Alpha 11.9.2](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.9.2). Use the named **PRAYCG_Workbench_Public_Alpha_11_9_2.zip** archive. Unchanged Results dashboards now retain their widgets, expanded child results and layout during background refresh; relevant changes to results, evidence, context, actions or widget lifecycle still rebuild the view. Read the [release guide](docs/releases/alpha-11.9.2/README.md), [changelog](CHANGELOG.md) and [build report](docs/releases/alpha-11.9.2/package/BUILD_REPORT.md) for evidence and limits.

The cumulative changes since the prior public 11.6.0 release add three Home paths—Run a study, Inspect a recording and Try an example—plus source context, frozen same-sample processing comparisons, question-first analysis navigation, evidence-type labels and a portable local Research Bundle viewer export. The example creates explicitly synthetic data in a chosen folder. Export creates a local copy; browser rendering remains unverified in the build's test record.

Eight original research task packages add frozen materials, response evidence and a shared protocol-analysis route. Recording-bound signal selections, bounded independent numerical checks, optional HED event-description validation and processing-history review preserve original events, plans and outputs. These research implementations are not normative or clinically validated tests. See the [protocol evidence guide](docs/releases/alpha-11.9.2/package/PROTOCOL_EVIDENCE_11_7.md).

The 11.9 integration clarifies Athena acquisition compatibility versus endpoint support, checks breathing-task cardiac and respiration support separately, opens verified paired Original/Processed views and adds offline compact Cerelog capture review with separate exports. The 11.9.1 corrections address SVNA/NATVIEW preparation, stable physiology method attribution, bounded timestamp roundoff and protocol/catalog verification. Current guides distinguish these software checks from physical acquisition and scientific validation.

Start with the [guided workspace](docs/releases/alpha-11.9.2/package/GUIDED_WORKSPACE_11_8.md), [integration guide](docs/releases/alpha-11.9.2/package/INTEGRATION_11_9.md) and [Signal Review guide](docs/releases/alpha-11.9.2/package/SIGNAL_REVIEW_GUIDE.md). The [11.6 processing workflow](docs/releases/alpha-11.9.2/package/WORKFLOW_COMPLETION_11_6.md) remains available for paired CAI/SID and report continuity. The [11.4.1 optical-credit correction and attribution guide](../docs/attribution/alpha-11.4.1/README.md) remain retained; historical receipts and results keep their original identities.

## Install or update

1. For a first installation or an older release without the updater, download the named Workbench ZIP and its SHA-256 checksum. Extract into a **new writable folder**, run **INSTALL.bat**, then **START.bat**. GitHub's generated source archives contain repository documents and research files; they are not the Workbench installer.
2. Updater-enabled Public installations can use **Settings → Updates**. For offline import, keep the release ZIP and its matching signed `.zip.update.json` together. Dependency setup may still need network access or cached packages.
3. Keep previous installations, study folders, recordings, settings and existing Zuna assets. Follow [installation and first launch](docs/installation.md) and the [exact packaged instructions](docs/releases/alpha-11.9.2/package/INSTALL_WORKFLOW.md).
4. Review [hardware support and its limits](docs/hardware-support.md) before selecting an acquisition route.

Core, Live Monitor and Hardware Connectors use separate release-local environments.

The signed `.zip.update.json` published with this release is the updater companion to the unchanged archive. The mirrored package documents describe the original manual build; the [release guide](docs/releases/alpha-11.9.2/README.md) records publication and updater verification separately. Optional ASR, ICLabel and Pycrostates comparisons use **INSTALL_SIGNAL_EXTRAS.bat**; **INSTALL_EVENT_DESCRIPTIONS.bat** provides optional isolated HED validation. Optional Zuna remains separate. Existing QC and locked plans retain their original identity. New executions must satisfy the current release's normal QC and revision workflow.

The optional [seven-film and original Lantern packages](docs/releases/alpha-11.2.2/STIMULUS_INSTALLATION.md) remain pinned to their published media assets. They provide eight masters across two packages. The full eleven-film companion is not included in the public release. See the [original master catalog](../examples/stimulus-masters/README.md) and [Demo Lantern Bridge](../examples/bridge-demo/README.md).

The [Opto-PING](../research/optoping/README.md), [ladder](../research/ladders/README.md) and [reproducibility](../research/reproducibility/README.md) indexes preserve the research programs and Rung 0O materials. The [concept](../research/concepts/README.md) and [algorithm](../research/algorithms/README.md) guides connect definitions to versioned inputs and calculations.

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
- [Retained Visual Analysis methods](docs/releases/alpha-10.5.4/VISUAL_ANALYSIS_ALPHA_10_5_4.md)
- [Retained Gamma and optical Forge methods](docs/releases/alpha-10.5.2/ANALYSIS_FORGE_ALPHA_10_5_2.md)
- [Gamma Scalpel methods and reference profiles](docs/releases/alpha-10.5.2/Gamma_Scalpel_v2_0/README.md)
- [Optical methods and instrument profiles](docs/releases/alpha-10.5.2/Optical_Signal_Review_v1_0/README.md)
- [Earlier analysis methods and limitations](../docs/attribution/ANALYSIS_METHODS.md)
- [Citations and attribution](../CITATIONS_AND_ATTRIBUTION.md)

The [current guide collection](docs/releases/alpha-11.9.2/README.md) preserves selected package documents and the build's verification record. Fresh Public checks record **979 passed, 1 skipped and 10 installer-wrapper checks refused by the isolated test guard**. Those refused checks are unverified, not passes; this focused regression does not rerun the entire preceding audit. The [11.6.0 Revision 1 guide](docs/releases/alpha-11.6.0/README.md), [11.4.1 release guide](docs/releases/alpha-11.4.1/README.md), [Alpha 10.5.4 guides](docs/releases/alpha-10.5.4/README.md) and earlier attribution snapshots remain historical. Their test counts and device receipts retain their original scope. The bundled Athena optical profile remains raw-only; citation repair does not qualify hemoglobin conversion or new device capabilities.

## Data and reporting

Keep study workspaces, recordings, private bundles and backups outside the application release folder. Public export requires review of consent, sharing authority, media rights and identifiers; a hash verifies byte identity, and is not an anonymization or permission check.

For a problem report, include the exact release, action attempted, session mode, protocol and hardware route, error text and a minimal non-sensitive reproduction. Keep participant recordings, credentials, device identifiers and private paths out of public issues.

[Repository home](../README.md) · [Contributing](../CONTRIBUTING.md) · [License](../LICENSE.md) · [Third-party notices](../THIRD_PARTY_NOTICES/)
