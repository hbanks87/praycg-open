# Hardware and recording support

**Maintained guide · Public Alpha 11.9.2 · reviewed 2026-10-25.** Current software behavior is described in the [11.9 integration guide](releases/alpha-11.9.2/package/INTEGRATION_11_9.md); the [build report](releases/alpha-11.9.2/package/BUILD_REPORT.md) records the checks actually completed. Neither replaces a route's physical evidence.

## Before recording

Atlas separates **can record this task** from **supports its intended endpoint**. Select the actual hardware and task, then inspect required channels, source identity, units, clocks, recording ownership and output destinations. Exploratory recording does not supply missing task-critical streams or timing evidence.

Select every required actual outlet in LabRecorder before starting the protocol. A connected but unrecorded sensor cannot be recovered later. For an external-publisher profile, a changed outlet UID or descriptor requires a newly built and reviewed profile and a new Equipment Session. The [retained external-profile workflow](releases/alpha-10.2.1/WORKFLOW_ALPHA_10_2_1.md) explains why a same-name replacement cannot satisfy the old lock.

| Recorded source | What it can support | Boundary to retain |
| --- | --- | --- |
| Athena TP9, AF7, AF8 and TP10 EEG | Supported per-channel and explicitly named pair descriptions, saved time-frequency results and measured-sensor views | Four measured electrodes do not supply a full scalp montage. |
| Athena raw Optical stream | Raw trends and descriptive analysis when recorded | HbO/HbR needs verified instrument mapping and declared conversion assumptions. |
| Measured RR or ECG | Supported cardiac calculations with sufficient valid timing and data | EEG does not substitute for measured cardiac input. |
| Measured respiration | Supported respiration calculations under their own data requirements | Respiratory support does not establish cardiac support. |
| EOG, EMG and ALS | Their declared signal and timing roles | Do not relabel an auxiliary signal as a different measured modality. |

Reconstructions and derived estimates remain labeled as such; they do not become additional measured electrodes or physical qualification.

## Athena EEG and raw optical acquisition

The retained BrainFlow Athena p1041 route has **ACQUISITION_VERIFIED** admission with **TRANSPORT_RECORDING_VERIFIED** physical scope when its source-bound acquisition receipt passes. That evidence covers connection, EEG identity/units, timestamp progression, live display, finalized XDF reopening and clean disconnect on the tested configuration. It does not establish that the headset was worn during the check, physiological accuracy, precise ERP/cross-sensor timing, hemoglobin mapping or reconstruction accuracy. See the retained [recording cautions and admission scope](releases/alpha-10.5.2/RECORDING_WITH_CAUTIONS_ALPHA_10_5_1.md).

The current catalogs and software qualification are bound to the current release. Historical acquisition evidence retains its original scope; 11.9.2 is not a new physical device test. Changed or unverified source/receipt bindings need review. Older locally approved AI protocols are not silently reapproved after an engine change. For legacy Zuna tasks requiring 16 physical EEG channels, choose the dedicated Athena variant rather than inventing channels or weakening the task declaration.

Athena's separate raw Optical stream must be selected in LabRecorder for later optical analysis. Athena provides no ALS. The retained [optical source review](releases/alpha-10.5.2/ATHENA_OPTICAL_SOURCE_REVIEW_ALPHA_10_5_2.md) explains the raw profile's scope and why HbO/HbR remains unavailable without the required mapping.

## Other routes

| Route | Setup and evidence to review |
| --- | --- |
| Neurosity Crown, Polar H10 ECG, GazePoint GP3/GP3 HD | Use the exact packaged route identity. GazePoint requires GazePoint Control and calibration; GP3 and GP3 HD are distinct. ECG and irregular Polar RR are separate routes; concurrent BLE clients can be unsupported. Athena admission does not promote other devices. |
| OpenMuse, Pupil Core/Neon and OpenViBE publishers | Manage the publisher separately, inspect the actual outlet and retain its version and metadata. Keep EEG and auxiliary stream identities distinct. |
| OpenBCI, Polar RR, Vernier and generic LSL | Apply the selected profile's readiness, identity, units and timing requirements. |
| Cerelog five-EMG/two-EOG/ALS | The off-body bench route and bounded experimental participant-pilot route are separate. The pilot requires its own fresh confirmations and recording controls; it is not a safety qualification. Follow the [11.6 pilot workflow](releases/alpha-11.9.2/package/WORKFLOW_COMPLETION_11_6.md#cerelog-experimental-pilot). |
| Compact Cerelog three-EMG/two-EOG/ALS | The [compact capture review](releases/alpha-11.9.2/package/INTEGRATION_11_9.md#compact-cerelog-capture-review) reads a closed standalone capture and can explicitly export a new derivative. This review action does not open a serial port, flash firmware, record, publish LSL or manufacture an XDF. Live acquisition remains in its separately reviewed standalone tool. |
| Cerelog 16 | Withheld/catalog candidate: exact firmware, transport, scaling, timing and physical contract remain unresolved. |

The compact and five-EMG Cerelog layouts are different routes. Physical response, temple leads, eye cross-axis response, rail events and cross-device timing still need physical validation. Preserve the actual layout and capture identity with any result.

## Review the recording

Check source/channel identity, units, participant metadata, timing, gaps and coverage before interpreting results. A completed recording or software worker does not establish that every endpoint is estimable. See [analysis and interpretation](analysis.md) and the [Signal Review guide](releases/alpha-11.9.2/package/SIGNAL_REVIEW_GUIDE.md).

For construction and original hardware records, use the [hardware index](../../hardware/README.md), including the [five-EMG/two-EOG/ALS project](../../hardware/cerelog-emg-als/2%20EOG%20%2B%205%20EMG%20%2B%20ALS-PT19/README.md).

[Workbench home](../README.md) · [Study workflow](workflow.md) · [Analysis](analysis.md) · [Troubleshooting](troubleshooting.md)
