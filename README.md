# PRAYCG Workbench

Local-first tools for auditable neuroscience and psychophysiology studies.

**Documented release:** Control Center Alpha 10.0.4  
**PRAYCG development and adaptation:** Hoyt Banks

PRAYCG Workbench helps an operator move from a study question to protocol selection, stimulus preparation, hardware configuration, synchronized recording, analysis and a research bundle. The Windows application is still named **PRAYCG Control Center** in Alpha 10.0.4. Workbench describes the wider software and workflow; it is not a second application to install.

The workbench records selected protocols, materials, hardware profiles, analysis recipes and software identities so other people can inspect what was planned and what actually ran. It makes missing evidence, quality problems and analytical limitations visible. Successful execution does not make an experiment scientifically valid.

## Workbench and research program

There are two related but distinct parts of PRAYCG.

| | PRAYCG Workbench | PRAYCG neuroscience research program |
| --- | --- | --- |
| Main purpose | Provide reusable tools for conducting, documenting and exchanging studies. | Investigate particular questions about narrative reception, task demands, sensory structure, psychophysiology and related exploratory constructs. |
| Main products | Study workspaces, protocol and hardware records, recordings, analysis reports and verifiable bundles. | Hypotheses, experimental contrasts, operational definitions, datasets and scientific interpretations. |
| Examples | Hardware Forge, Protocol Atlas, Analysis Forge, Live Monitor and Research Exchange. | PRAYCG3, PRAYCG4, Semantic Meaning Gradient and PRAYCG-specific exploratory measures. |
| What counts as evidence | Software tests, provenance checks, numerical tests, apparatus checks and documented execution. | Appropriate study design, measurement validity, controls, uncertainty, replication and evidence against alternative explanations. |
| What use implies | You selected a workflow or tool. | You may be testing a particular hypothesis; using the tool does not establish or endorse it. |

You do not need to accept the Base Model or any PRAYCG-specific theoretical interpretation to use the workbench. A researcher can use suitable packaged tasks, inspect ordinary signal-quality results, or compare interpretations without adopting a PRAYCG construct. A protocol's presence in the Atlas means it has a packaged implementation and documented scope, not that its theory has been independently validated.

PRAYCG3, PRAYCG4 and SMG retain their own design limitations. For example, a fixed-order within-run contrast can combine condition effects with order, fatigue, habituation and carryover. A software gate cannot remove those confounds. Novel scores remain operational, exploratory quantities unless the relevant validation evidence supports a stronger claim.

## Documentation

- [Installation and detailed workflow](docs/INSTALLATION_AND_WORKFLOW.md) ([PDF](pdf/PRAYCG_Alpha_10_0_4_Installation_and_Workflow.pdf)): setup, acquisition, analysis, AI returns, recovery and bundling.
- [Analysis module guide](docs/ANALYSIS_MODULE_GUIDE.md) ([PDF](pdf/PRAYCG_Alpha_10_0_4_Analysis_Module_Guide.pdf)): each registered module, its inputs, outputs and interpretation limits.
- [Master changelog from 0.95a through Alpha 10.0.4](docs/MASTER_CHANGELOG.md) ([PDF](pdf/PRAYCG_Master_Changelog_0_95a_to_Alpha_10_0_4.pdf)): chronological release history and persistent limitations.
- [AI authoring boundaries](docs/AI_AUTHORING_WORKFLOW_REVIEW.md): supported recipe changes, protocol review and the remaining extension-development work.
- [Protocol credits](docs/PROTOCOL_CREDITS.md), [protocol citations](docs/PROTOCOL_CITATIONS.md) and [upstream attribution review](docs/UPSTREAM_ATTRIBUTION_REVIEW.md).

Printable versions of the three main guides accompany this documentation pack. Their Markdown files are the editable, GitHub-ready sources. This documentation update does not change the Alpha 10.0.4 software archive.

## What Alpha 10.0.4 provides

- A study workspace linking protocol choice, prepared materials, session identity, hardware, recordings and analysis history.
- A Protocol Atlas with **57 main-browser modules**: 54 Atlas definitions and 3 native protocols. **10 additional prospective sequence variants** belong to a separate workflow. These are 67 packaged definitions, not 67 independently validated experiments.
- Stimulus selection and preparation with file fingerprints and protocol-specific requirements.
- Hardware profiles and LSL stream checks that distinguish configured equipment from observed evidence. Device descriptions and adapters have different maturity levels; the catalog is not universal plug-and-play certification.
- A passive Live Monitor and synchronized offline XDF replay, with recorded auxiliary streams shown when supported and present.
- An Analysis Forge with mandatory initial QC, **23 registered analysis entries**, dependency-aware plans, retained results and plain-language reports. Individual workers can still find an outcome not estimable.
- Local Research Exchange bundles, verification, import, current-build reanalysis and a local DATA catalog prototype. The catalog is not an automatically published public repository.
- AI-assisted design packs and bounded recipe proposals that the operator reviews locally.

## Install the packaged Windows release

1. Obtain the complete `PRAYCG_ControlCenter_v1_0_0_alpha_10_0_4.zip` release archive. A GitHub source snapshot is not necessarily the packaged Windows distribution.
2. Stop recordings normally, close older Control Centers and back up studies separately.
3. Extract into a new writable local folder. Keep `app/` beside the top-level launchers. Do not merge it over an old release or run inside the ZIP.
4. Install native Windows **Python 3.11 with Tcl/Tk**. Run `INSTALL.bat` and check both Core and Live Monitor component results.
5. Run `START_PRAYCG.bat`. Verify external PsychoPy, LabRecorder and device/bridge settings before acquisition.

The archive does not include Python, all dependency wheels, PsychoPy or LabRecorder. Installation normally needs internet access. Core uses the selected Python 3.11 interpreter and may update its packages; Live Monitor uses a separate environment. See the detailed guide for minimal installation, repair and upgrade procedures.

## Typical study workflow

Create or open a workspace → choose a protocol → prepare and fingerprint its materials → select and check equipment → review pre-start settings → confirm, lock and arm → record and run → stop and save → run required QC → select and run analysis → review individual reports → verify and package the study.

Bench Test Mode is for **no-participant** demonstrations and software/equipment checks. It does not certify hardware or turn missing data into valid measurements. Shortening a protocol and selecting bench mode are separate actions. Set permitted timing changes before session confirmation and preserve the reason for the variant.

For existing data, start with the correct recorded run folder and XDF. Do not use today's hardware selection as a substitute for the recording's saved metadata. A noisy recording can support some descriptive analyses while being inadequate for others. `NOT_ESTIMABLE` means an estimate is unsupported or unavailable; it is not zero and is not automatically a software crash.

## AI assisted authoring

### Protocol proposals

Use **Create New Protocol with AI Docs…** to produce a local request pack, inspect `UPLOAD_PROTOCOL_AI_DOCS.zip`, and share only approved context with your chosen AI agent. Ask for the specified declarative JSON return, then use **Review AI Protocol Return…** to check and stage it.

**Alpha 10.0.4 does not install a reviewed candidate as a new runnable protocol.** Developer integration must still register and test the protocol, stimulus, pre-start configuration, runner and analysis relationships. A timeline preview is not a participant test, and AI-generated approval is not authorization.

### EEG recipe proposals

Use **Create / Revise Recipe → Export AI Recipe Request…**. After the AI returns the specified proposal JSON, select **Review AI Recipe Proposal…**, inspect the differences, choose **Load reviewed proposal into form**, then **Validate Draft** and **Lock Recipe**. Review the resulting analysis-plan revision before running it.

Recipe proposals change supported settings of existing methods. They cannot add a new estimator, arbitrary preprocessing operation or executable analysis module. Existing model matrices and unexposed settings must be preserved unless explicitly revised. A stale parent, malformed return or unsupported label must be resolved rather than forced through.

### AI assistance is not scientific approval

An external model can help articulate a hypothesis, identify missing controls, draft compatible parameters and propose tests. The operator remains responsible for checking sources, methods, consent, privacy and the output's meaning. Record the provider/model and relevant prompts as provenance where appropriate. Model branding is not an approval tier.

PRAYCG does not automatically upload recordings or connect to a cloud model through these workflows. Private full-data bundles can contain sensitive recordings, event logs, responses, stimuli and identifying context. Review the exact contents and the receiving service's applicable policies before sharing. A private bundle is not an anonymized or public-safe bundle.

## Reports and research exchange

Keep raw recordings, acquisition evidence, analysis derivatives, recipes, results and interpretations distinguishable. Preserve missing outcomes and quality cautions in the report. An offline interpreter explains available outputs; it does not supply missing observations or prove a mechanism.

Bundles help another person verify file integrity and inspect study lineage. Reanalysis under a different build is distinct from exact replay. Matching selected values is not proof of complete numerical equivalence, scientific replication or successful execution on a second machine.

The longer-term goal is an open, local-first neuroscience ecosystem in which studies can be audited, reproduced, extended and rerun by laboratories, companies and independent researchers. Public DATA exchange, broader device support and reviewed installation of new AI-assisted extensions remain development work, not blanket present-day guarantees.

## Validation and limits

Alpha 10.0.4 passed 58 declared software suites, reporting 1,710 tests or dry-run checks. Its release evidence includes 15 seeded synthetic signal cases, same-machine historical PRAYCG3 reanalysis and extracted-archive checks. The historical run produced 13 completed module outcomes and two `NOT_ESTIMABLE` outcomes; that distinction was retained.

These checks did not validate every physical device, participant protocol, display/audio timing path, fresh online installation or second-machine execution. Protocol software coverage includes compilation, binding and bounded simulated behavior; core and prospective definitions do not all receive full runner execution. Local AI-return fixtures do not establish the reliability of an external AI service.

This is research software, not a clinical diagnostic system, a consciousness detector, a spiritual ranking tool or evidence for a proposed biological mechanism by itself. Human studies need appropriate consent, risk review and applicable oversight. Self-experimentation does not remove electrical, privacy, stimulus or interpretation risks.

## Attribution and contribution

Hoyt Banks is credited for PRAYCG development and adaptation separately from original study, dataset, stimulus and software authors. All 67 protocol definitions carry structured attribution metadata. Citations do not imply endorsement, permission to redistribute materials or scientific validation. Original third-party license obligations remain applicable, and the bounded attribution review is not complete license clearance.

For a useful bug report, include the release, relevant protocol/module ID, reproduction steps, sanitized error text and the affected workflow stage. Do not post private XDFs, participant identifiers, access tokens or unrestricted full-data bundles in public issues.

For a proposed protocol or analysis contribution, supply the question, operational definitions, inputs and units, sources and rights, expected outputs, known limitations, and reproducible tests. Numerical methods need known-answer and missing/degenerate-input checks, not only a successful process exit. Keep generated code outside a live participant session until it has completed the separate review and integration process.
