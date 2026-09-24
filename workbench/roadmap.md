# Workbench roadmap

This page identifies proposed software and documentation work. It is not a release commitment or a record of completed validation. The current packaged application is [Alpha 10.2.1](README.md); research hypotheses and study planning belong to the [PRAYCG Neuro Research Program](../research/README.md).

## Priorities

| Proposed work | Evidence needed to consider it complete |
| --- | --- |
| Publish a maintained application source tree | A traceable relationship to the release ZIP, documented build/packaging steps, retained licenses and an explicit release identity |
| Improve independent installation and reproduction | Recorded installation and representative workflow results on another machine, with versions and unresolved differences |
| Complete physical evaluation of experimental connectors | Device-specific transport, sample-delivery and timing evidence, documented conditions and clear limits for each route |
| Strengthen acquisition and artifact controls | Repeatable checks for stream continuity, marker alignment and applicable EOG/EMG, line-noise and other confound controls |
| Improve method review and negative controls | Clear numerical definitions, interpretable synthetic cases and results that distinguish estimator failure from missing evidence |
| Improve documentation and examples | Version-matched instructions, working navigation, reproducible example inputs and explicit media/attribution terms |

The [hardware-support index](docs/hardware-support.md) records the current route boundaries. Future testing should change a route's status only when the corresponding evidence supports that change. A proposed feature, a packaged connector and a validated physical setup are different milestones.

## Contributing to these priorities

Use [development guidance](development/README.md) to identify the starting release and preserve its history. Contributions are most useful when they pair a concrete change with a small reproducible example, relevant checks and a statement of remaining limitations.

[Workbench](README.md) · [Contributing](../CONTRIBUTING.md) · [Research program](../research/README.md)
