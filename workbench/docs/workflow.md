# Study workflow

**Maintained guide · Public Alpha 11.9.2 · reviewed 2026-10-25.** Install using the [installation guide](installation.md). This page connects current tasks; the linked release documents preserve detailed behavior and evidence for their exact versions.

## Start with a synthetic example

On Home choose **Try an example** and select a destination for new files. Workbench creates a labeled **SIMULATED** recording with generated channels and an intentional timestamp gap, then opens inspection. It uses no hardware or AI provider and does not replace the active study, recording, settings or acquisition configuration. Synthetic results are not evidence about physical acquisition or physiology.

Read the context header: selected source, stream, channel labels, units, interval and available participant metadata. **Choose your question → What is in this recording?** leads to source inspection. Continue with [analysis and interpretation](analysis.md) to examine support, run analyses or compare processing.

## Inspect an existing recording

Choose **Inspect a recording**, select the saved source and confirm its stream/channel identities and units. Unknown participant identity stays unknown; a filename is not a participant record. **Inspect saved source…** reads metadata and samples in the background. It does not establish quality or run the analysis plan. A saved recording is distinct from the currently connected equipment and from a live or replay viewer.

## Prepare and record a study

1. Choose **Run a study**. Review the study workspace and the Equipment Session separately, and select the actual equipment before choosing a compatible task.
2. Review the task's required materials. Install optional movies only when needed; the [stimulus installation guide](releases/alpha-11.2.2/STIMULUS_INSTALLATION.md) explains the installer and preparation review. Generated or installed material still needs operator review.
3. Compile, review and lock the protocol where the workflow requires it. AI proposals remain declarative and subject to review; a proposal is not an executable asset or approval to run a participant protocol. See the [protocol evidence workflow](releases/alpha-11.9.2/package/PROTOCOL_EVIDENCE_11_7.md#run-a-new-task).
4. Check stream identities, channels, units, clocks, recording ownership, output destinations and device-specific cautions in [hardware and recording support](hardware-support.md).
5. Start LabRecorder before the protocol. Select every actual outlet required by the study, including separately published optical, auxiliary, marker or RR streams; a selected profile alone does not record them.
6. Stop and save the recording, then close the XDF before running saved-recording analysis. Retain the source with the protocol, settings and contemporaneous study records.

## Analyze and review

Open the saved recording in the analysis workspace. Recommended analyses and a custom plan are separate choices. **READY BUT NOT RUN** means the current plan still needs **Run pending analyses**; it is not a completed result. Read [analysis and interpretation](analysis.md) for coverage, availability states, figures, frozen comparisons and cleaning review.

Treat operator-reported conditions as reported metadata, and check whether timing and labels support the intended comparison. Preserve historical results as historical results; a new calculation should create a separate derivative.

## Export a reviewable package

Use Research Exchange to select the appropriate bundle or local browser inspection copy. Review consent, rights, identifiers, source scope and the file ledger before sharing. Export does not anonymize or upload the results. AI explanation is a separately configured and authorized step; numerical analysis and local inspection can be reviewed without it.

## Detailed and historical references

- [Guided workspace](releases/alpha-11.9.2/package/GUIDED_WORKSPACE_11_8.md): entry routes, source context, frozen samples and browser export carried in 11.9.2.
- [11.9 integration](releases/alpha-11.9.2/package/INTEGRATION_11_9.md): current integration details and remaining limits.
- [Installation and workflow reference](releases/alpha-11.9.2/package/INSTALL_WORKFLOW.md): the shipped operational reference.
- [Release history](../../docs/release-history/README.md): exact earlier guides and publication records.

[Workbench home](../README.md) · [Installation](installation.md) · [Analysis](analysis.md) · [Hardware](hardware-support.md)
