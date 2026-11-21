# Workbench roadmap

These proposals identify useful next tests for the software. For shipped changes, read the [Workbench changelog](CHANGELOG.md). For research hypotheses and study design, see the [research program](../research/README.md).

## Release acceptance

Exercise the complete path from selecting materials or a recording to reopening the saved result. Keep physical-device evidence, provider/model evaluation and independent scientific reproduction separate when reporting which checks passed. The [11.2.2 workflow record](../docs/updates/2026-10-14-public-workflow-release.md) documents an earlier application of these checks.

## Priorities

| Proposed work | Evidence needed to consider it complete |
| --- | --- |
| Publish a maintained application source tree | A traceable relationship to the release ZIP, documented build/packaging steps, retained licenses and an explicit release identity |
| Improve independent installation and reproduction | Recorded installation and representative workflow results on another machine, with versions and unresolved differences |
| Complete physical evaluation of experimental connectors | Device-specific transport, sample-delivery and timing evidence, documented conditions and clear limits for each route |
| Extend physical timing and artifact evaluation | Independent device-specific evaluation beyond the shipped stream checks and Gamma Scalpel EOG/EMG screening, with timing uncertainty and negative controls |
| Improve method review and negative controls | Clear numerical definitions, interpretable synthetic cases and results that distinguish estimator failure from missing evidence |
| Improve documentation and examples | Version-matched instructions, working navigation, reproducible example inputs and explicit media/attribution terms |

The [hardware-support index](docs/hardware-support.md) records the current route boundaries. Future testing should change a route's status only when the corresponding evidence supports that change. A proposed feature, a packaged connector and a validated physical setup are different milestones.

## Contributing to these priorities

Use [development guidance](development/README.md) to identify the starting release and preserve its history. Contributions are most useful when they pair a concrete change with a small reproducible example, relevant checks and a statement of remaining limitations.

[Workbench](README.md) · [Contributing](../CONTRIBUTING.md) · [Research program](../research/README.md)
