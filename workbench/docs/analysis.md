# Analyze a recording and interpret results

**Maintained guide · Public Alpha 11.9.2 · reviewed 2026-10-25.** This is an operational reading guide, not a replacement for scientific definitions or a claim of endpoint validity. The detailed sources are the shipped [workflow reference](releases/alpha-11.9.2/package/INSTALL_WORKFLOW.md), [guided workspace](releases/alpha-11.9.2/package/GUIDED_WORKSPACE_11_8.md) and [integration guide](releases/alpha-11.9.2/package/INTEGRATION_11_9.md).

## Run and inspect an analysis

1. In **PRAYCG AI Assistant → Analyze a recording**, choose **Open recording…**. Confirm the exact recording/run, selected streams, channel labels, units and participant metadata. The [synthetic example](workflow.md#start-with-a-synthetic-example) is a way to learn this path without hardware.
2. Choose **Run recommended analyses**, or **Choose modules…** for custom work. Required QC runs first when needed. If the plan is **READY BUT NOT RUN**, choose **Run pending analyses**. Local numerical analysis does not contact an AI provider.
3. Choose **View latest report**. **Individual module reports**, **Open selected report** and **Advanced details… → Create / view local numerical summary** expose saved evidence.
4. Read coverage and omissions alongside results. Distinguish included results, failed attempts, unavailable endpoints and skipped dependencies. Select prior results explicitly when reviewing an older run; do not treat an empty current run as evidence that an earlier run completed it.

Preserve historical results and plans. Recalculation creates a separate derivative; changing identifiers or hashes to force a historical result into a current pairing destroys the evidence the viewer is checking.

## Read result status before interpreting values

| Label or state | How to read it |
| --- | --- |
| Recorded measurement | Values observed from an identified recording in declared units; acquisition quality still matters. |
| Calculated estimate | A result calculated from identified data using a stated method and support. |
| Exploratory construct | An interpretation, reconstruction, simulation or research construct; not a directly measured mental state. |
| Unclassified | No reviewed mapping is registered. Do not infer measurement status or established validity. |
| NOT_ESTIMABLE / unavailable | The stated prerequisites or support were not met. Read the reason; absence is not a zero value. |
| Worker completed | The software task finished. Check which endpoints were actually available and which attempts failed or were skipped. |

Classification does not validate an endpoint. Four-channel Athena is not a full-montage CAI/SID recording. Measured respiration and cardiac support are checked separately; one can be available while the other is unavailable. Missing autonomic position remains missing. See [hardware and recording support](hardware-support.md) for measured-source boundaries.

## Open figures and paired processing results

**Visual Analysis** opens recording-specific saved figures. Batch time-frequency work saves plots without opening a window automatically; choose **Open latest time-frequency view** to inspect them.

Open a registered paired result from the processing-results area. The viewer checks registration, source receipt and array hashes before displaying **Original** or **Processed**. Compare the same supported samples using the fixed original calibration and scales. Older results without adequate recording-clock metadata may need a new comparison derivative; do not guess the origin. The [paired-results reference](releases/alpha-11.9.2/package/INTEGRATION_11_9.md#paired-processing-results) records this behavior and the limits of the CAI/SID display.

## Compare a frozen interval

1. Open a saved recording or compatible review, and verify source, stream, labels and units.
2. Choose a display channel and interval in **Seconds from recording start**, select an output destination and choose **Freeze interval**.
3. All channels of the stream are frozen together. The channel chooser changes only the display; another stream or interval requires a new freeze.
4. Leave **None — original only**, or select an existing current-recipe preview. **Select receipt…** can add an existing reviewed candidate.
5. Choose **Compare frozen samples**, then read **Same-sample traces** and **Evidence and limitations**. **Review comparison evidence…** reads selected existing JSON evidence; it does not run a benchmark or adopt a candidate.

The limit is 600 seconds and two million channel-values. Timestamps must be finite and strictly increasing. Gaps and exclusions stay explicit, and filtering retains its minimum continuous-support and edge-guard requirements. Candidates must match the same source, stream, annotations, channels, units and exact timestamps. Unaligned candidates are rejected rather than silently interpolated.

A smoother trace is not proof of preserved physiology. Numerical change, artifact-reduction evidence and desired-signal preservation are separate findings. A current preview is not a replay of a historical locked derivative. See the [full frozen-comparison contract](releases/alpha-11.9.2/package/GUIDED_WORKSPACE_11_8.md#3-freeze-and-compare-identical-samples).

## Review cleaning choices

Use **Signal Quality & Cleaning Review** for reviewable processing candidates. ICA defaults to removing nothing; inspect components before selecting zero-based removal indexes. ASR requires a deliberately reviewed clean calibration interval of at least 30 seconds and the optional signal-extras environment. A reviewed receipt does not automatically establish valid physiology or remove QC requirements. Follow the [Signal Review guide](releases/alpha-11.9.2/package/SIGNAL_REVIEW_GUIDE.md) for setup, pairing, events and method limits.

## Explain or share the result

AI explanation requires its separate provider configuration and explicit authorization. Provider failure does not invalidate or replace the local numerical reports. Review the evidence and omissions directly.

Research Exchange can export a Research Bundle or a local browser inspection copy. The browser copy verifies the archive/ledger and contains bounded previews; it is not analysis replay, automatic anonymization or upload. Choose a new HTML destination in an existing folder on a filesystem supporting hard links. Review identifiers, private paths, consent and rights before sharing. Browser rendering was not observed in the shipped validation; the [export reference](releases/alpha-11.9.2/package/GUIDED_WORKSPACE_11_8.md#7-export-a-local-browser-inspection-copy) records the exact limits.

[Workbench home](../README.md) · [Study workflow](workflow.md) · [Hardware](hardware-support.md) · [Troubleshooting](troubleshooting.md)
