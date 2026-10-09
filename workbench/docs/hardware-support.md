# Hardware support in Alpha 10.5.3

The Workbench's software routes and the repository's [physical hardware projects](../../hardware/README.md) answer different questions. Review each route's exact source, firmware, mapping, timing and acquisition evidence. A connector or successful installation alone does not certify an attached device, electrode placement, electrical safety or stimulus synchronization.

The [complete Alpha 10.5.3 package](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_A10.5.3/PRAYCG_Workbench_Alpha_10_5_3.zip) contains the route-specific profiles, source evidence and acquisition guides. The [retained recording guide](releases/alpha-10.5.2/RECORDING_WITH_CAUTIONS_ALPHA_10_5_1.md) defines the unchanged readiness checks and Athena admission scope. Current software and native-view checks do not constitute new physical hardware acquisition or cross-device timing validation.

## Athena EEG acquisition

The packaged BrainFlow Athena p1041 route has **ACQUISITION_VERIFIED** admission with **TRANSPORT_RECORDING_VERIFIED** physical scope when its source-bound acquisition receipt passes. That scoped evidence covers connection, EEG identity/units, timestamp progression, live display, finalized XDF reopening and clean disconnect on the tested configuration. Alpha 10.5.3 retains this unchanged route; its earlier acquisition evidence keeps its original scope.

The receipt does not establish that the headset was worn during the equipment check, physiological accuracy, clinical suitability, precise ERP/cross-sensor timing, optical hemoglobin mapping or Zuna reconstruction accuracy. Changed or unverified source/receipt bindings require review. Ordinary recordings can retain **PARTICIPANT_ACQUISITION** purpose when Bench Test Mode is off, including recordings with signal cautions. Bench Test Mode remains an explicit no-participant choice; earlier recordings keep their original classification.

Athena provides four measured EEG electrodes: TP9, AF7, AF8 and TP10. Its separate raw Optical stream has sixteen channels at nominal 64 Hz and must be selected in LabRecorder for later optical analysis. Athena provides no ALS. The [optical source review](releases/alpha-10.5.2/ATHENA_OPTICAL_SOURCE_REVIEW_ALPHA_10_5_2.md) explains why the bundled raw profile supports exploration while HbO/HbR remains unavailable.

## Visual sources and passive viewing

Alpha 10.5.3's **Visual sources** requires an explicitly selected EEG stream, electrode names, units and calibration, plus an optional RR source. Source changes reset calibration and history. The default incremental gamma recipe needs measured P7/P8, and theta needs Pz/P3/P4; Athena's four named electrodes do not supply those positions. Missing required channels leave the corresponding features unsupported rather than inventing electrode locations. The retained Gamma Scalpel analysis uses its separate, recorded-electrode contract.

Passive live views consume incoming samples and issue no acquisition, stimulation, outlet or recording commands. Raw EEG/RR leaves CAI, NIP and CAI-SID unavailable without their required completed-analysis components. Generated Zuna channels remain reconstructions and do not count as independent measured electrodes. See the [Visual Analysis guide](releases/alpha-10.5.3/VISUAL_ANALYSIS_ALPHA_10_5_3.md) and [current validation boundaries](releases/alpha-10.5.3/UPDATE_TRACEABILITY_ALPHA_10_5_3.md).

## Other route boundaries

| Category | Routes | Operating boundary |
| --- | --- | --- |
| Managed connectors | Neurosity Crown OSC through BrainFlow; Polar H10 ECG; GazePoint GP3 and GP3 HD | Review the packaged route's experimental status and physical/timing evidence. Athena admission does not promote other products. |
| External publishers | OpenMuse Athena EEG, motion, optics and battery; Pupil Core scene gaze and pupillometry; Pupil Neon gaze; OpenViBE LSL | Install/manage the publisher separately, inspect its exact live outlet and preserve version and metadata evidence. |
| Retained routes | OpenBCI with or without ALS, Polar RR, Vernier and generic LSL routes | The selected route's readiness, identity, units and timing requirements still apply. |
| Cerelog V1 EMG/EOG/ALS | Five EMG, two EOG, one ALS and timing outlets with matching `CERELOG_V1_EMG5_EOG2_ALS1_1K_V1` firmware | The packaged connector remains experimental and restricted to off-body, no-participant bench evaluation. Physical qualification and measured Cerelog–Athena timing remain separate requirements. |
| Cerelog 16 | Withheld/catalog candidate | Exact firmware, transport, scaling, timing and physical contract remain unresolved. |

The package's `app/docs/HARDWARE_ROUTES_ALPHA_10_2_1.md` records the historical introduction and pinned-source contracts of several retained routes. Its original blanket experimental status predates the current Athena admission. The package's `app/docs/CERELOG_EMG_EOG_ALS_ALPHA_10_2_3.md` describes the Cerelog five-EMG/two-EOG firmware mapping and off-body procedure; use current Gamma guides for the analysis behavior added in 10.5.2.

## Details that affect recording and interpretation

- Crown uses the reviewed BrainFlow OSC route; retain its exact signal identity in reports.
- An OpenMuse p1041 EEG outlet may contain four named electrode channels and four AUX channels. Preserve that distinction and its publisher/preset identity.
- Polar H10 ECG and the irregular RR stream are separate routes. Concurrent BLE clients can be unsupported by the device or operating system.
- GazePoint requires GazePoint Control and calibration. GP3 and GP3 HD have separate route identities.
- Restarting a publisher can change its outlet identity. Re-review the outlet in a fresh equipment session instead of retaining a stale lock.
- Save EOG/EMG references in the same XDF for Gamma Scalpel discovery. Compatible labels do not establish useful reference quality or independent-clock alignment. Missing or ambiguous references remain explicit in the report.

The [Cerelog five-EMG/two-EOG/ALS firmware project](../../hardware/cerelog-emg-als/2%20EOG%20%2B%205%20EMG%20%2B%20ALS-PT19/README.md) is a separate custom hardware review package. Its presence does not resolve the withheld Cerelog 16 contract or qualify participant acquisition.

[Workbench](../README.md) · [Installation](installation.md) · [Workflow](workflow.md) · [Hardware projects](../../hardware/README.md)
