# Workbench development

The authoritative Alpha 10.5.2 application code is preserved inside the complete [PRAYCG Workbench Alpha 10.5.2 ZIP](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_A10.5.2/PRAYCG_Workbench_Alpha_10_5_2.zip). This repository publishes release documentation and archives; this directory provides development guidance rather than a separate maintained extracted application source tree.

Extract the complete package into a new local development folder. Its `app/` directory contains the Control Center, tools, configuration, documentation and deployment resources. Keep the public launchers beside that directory, and follow the [installation guide](../docs/installation.md). Core, Live Monitor and Hardware Connectors use separate release-local environments; optional Zuna is installed separately.

## Preserve the starting point

Record the ZIP's filename and SHA-256 before development. Keep the original archive unchanged, and give modified builds their own identities. Keep releases in separate folders and study recordings in separate data locations.

The package's `app/deployment/validation/BUILD_VALIDATION_v1_0_0_alpha_10_5_2.json` records the packaged release's checks and declared limitations. The [implementation traceability guide](../docs/releases/alpha-10.5.2/UPDATE_TRACEABILITY_ALPHA_10_5_2.md) connects the Gamma Scalpel, optical, workflow and verification changes to their scope. Package evidence applies to its identified source and environment; a modified build needs its own evidence.

The repository's [attribution evidence](../../docs/attribution/) describes a separate source-update review, including its own [validation scope](../../docs/attribution/VALIDATION.json). Preserve the distinct identity and scope of each receipt.

## Make changes reviewable

1. Describe the behavior being changed and the exact starting release.
2. Preserve protocol, hardware, run, recording and analysis identities wherever the change affects existing evidence. Keep original XDF measurements available beside derived results.
3. Use relevant package checks and a minimal synthetic reproduction for the affected behavior. Record what ran, its environment and its results.
4. Identify anything left untested. Keep software tests, existing-recording checks, physical-device tests, timing measurements and scientific validation distinct.
5. Update documentation, citations and notices when behavior or incorporated material changes. Keep public launchers, manifests and release documentation consistent with the resulting version.

Estimator changes need a clear numerical definition and meaningful negative controls. Gamma reference screening requires explicit source, participant, units, quality and timing support; quiet references cannot establish neural origin. Optical conversion requires verified instrument facts and a recording-specific binding/baseline. The bundled Athena raw profile does not establish hemoglobin mapping.

Acquisition changes need an explicit stream/transport contract and device-appropriate evidence. Alpha 10.5.2 retains the unchanged Athena route's scoped transport/recording admission. Software checks and offline recordings do not qualify a changed physical route or Cerelog–Athena timing. The bundled timing-patched LabRecorder likewise retains its separately declared synthetic qualification.

For contributions, begin with [CONTRIBUTING](../../CONTRIBUTING.md), [citation and attribution guidance](../../CITATIONS_AND_ATTRIBUTION.md), and the applicable [third-party notices](../../THIRD_PARTY_NOTICES/). Preserve upstream credits and file-specific terms.

## Future source layout

Publishing a maintained extracted source tree would require a documented relationship to the release archive, reproducible packaging, retained notices and clear release ownership. That work is a [roadmap item](../roadmap.md).

For historical comparisons, the [Alpha 10.2.1 package](../releases/alpha-10.2.1/PRAYCG_ControlCenter_v1_0_0_alpha_10_2_1.zip) and its [installation guide](../docs/releases/alpha-10.2.1/INSTALLATION_ALPHA_10_2_1.md) remain available with their original release identities.

[Workbench](../README.md) · [Current Forge guide](../docs/releases/alpha-10.5.2/ANALYSIS_FORGE_ALPHA_10_5_2.md) · [Research program](../../research/README.md) · [Hardware projects](../../hardware/README.md)
