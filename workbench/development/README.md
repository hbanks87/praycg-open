# Workbench development

The authoritative Alpha 10.2.1 application code is preserved inside the [versioned application ZIP](../releases/alpha-10.2.1/PRAYCG_ControlCenter_v1_0_0_alpha_10_2_1.zip). There is no separate extracted Alpha 10.2.1 application source tree in this repository.

Extract the complete package into a new local development folder when inspecting or changing that release. Its `app/` directory contains the Control Center, tools, configuration, documentation and deployment resources. Keep the public launchers and release files beside that directory, and follow the [installation guide](../docs/installation.md).

## Preserve the starting point

Record the ZIP's filename and SHA-256 before development. Keep the original archive unchanged, and give modified builds their own identities. Do not merge different extracted releases or put study recordings inside a development checkout.

The package's `app/deployment/validation/` records evidence for the packaged release. The repository's [attribution evidence](../../docs/attribution/) describes a separate source-update review, including its own [validation scope](../../docs/attribution/VALIDATION.json). Neither record is evidence that a new local change has passed those checks or is already present in the original ZIP.

## Make changes reviewable

1. Describe the behavior being changed and the exact starting release.
2. Preserve protocol, hardware, run and analysis identities wherever the change affects existing evidence.
3. Use the package's relevant checks and a minimal synthetic reproduction for the affected behavior. Record what ran, its environment and its results.
4. Identify anything left untested. Keep software tests, physical-device tests, timing measurements and scientific validation distinct.
5. Update documentation, citations and notices when behavior or incorporated material changes.

Changes to estimators need a clear numerical definition and meaningful negative controls. Changes to acquisition need an explicit stream/transport contract and evidence appropriate to the device. A software-only test does not establish physical readiness.

For contributions, begin with [CONTRIBUTING](../../CONTRIBUTING.md), [citation and attribution guidance](../../CITATIONS_AND_ATTRIBUTION.md), and the applicable [third-party notices](../../THIRD_PARTY_NOTICES/). Preserve upstream credits and file-specific terms.

## Future source layout

Publishing a maintained extracted source tree would require a documented relationship to the release archive, reproducible packaging, retained notices and clear release ownership. That work is a [roadmap item](../roadmap.md); this directory currently provides development guidance only.

[Workbench](../README.md) · [Research program](../../research/README.md) · [Hardware projects](../../hardware/README.md)
