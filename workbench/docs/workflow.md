# Study workflow

Use the preserved [Alpha 10.2.1 detailed workflow guide](releases/alpha-10.2.1/WORKFLOW_ALPHA_10_2_1.md) for the application's exact controls, recording order, state transitions and recovery instructions.

## Find the right part of the guide

| Your task | Sections in the full guide |
| --- | --- |
| Prepare a study | 1–4: settings, workspace, protocol and materials |
| Configure equipment | 5–7: hardware profile, equipment session, streams and checks |
| Record a session | 8–9: pre-start configuration, confirmation, arming, runner and LabRecorder |
| Analyze and interpret | 10–11: required QC, locked analysis plan, module results and interpretation |
| Package and exchange | 12–13: local/private bundles, Research Exchange and the local DATA catalog |
| Extend a workflow | 14–15: AI-assisted protocol and EEG-recipe authoring |
| Replay or recover | 16–18: XDF replay, common blockers and end-of-session checklist |

## Keep these distinctions visible

A **Study Workspace** holds the persistent study history. A new logical session belongs to that workspace; a new **Equipment Session** creates a fresh acquisition/run identity. Review the intended identities before acquisition.

LabRecorder is the external recorder. Follow the release guide's recording order and confirm that the required device outlets and marker stream are included. Live Monitor observes streams and replay; it does not replace the recorder.

Required QC comes before interpretation. Review failures, timing evidence, artifacts and `NOT_ESTIMABLE` results alongside numerical findings. A locked plan records intended analyses; execution receipts show what actually ran. Locking a plan does not make an analysis prospective after outcomes have been examined.

Review consent, privacy, identifiers and stimulus rights before sharing a bundle. Private study and AI-review packages can contain sensitive data even when a smaller results package appears suitable for sharing.

For a first software demonstration, start with the [example materials](../../examples/README.md) and the guide's explicitly labeled bench workflow. Check [route-specific restrictions](hardware-support.md) before connecting equipment.

[Workbench](../README.md) · [Installation](installation.md) · [Full workflow guide](releases/alpha-10.2.1/WORKFLOW_ALPHA_10_2_1.md)
