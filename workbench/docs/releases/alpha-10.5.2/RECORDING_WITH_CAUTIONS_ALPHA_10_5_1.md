# Recording with cautions and Athena acquisition status

Alpha 10.5.1 separates permission to record from suitability for a particular analysis. Recording preserves observations. Forge assesses which electrodes, windows and outcomes those observations support.

## Recording readiness

The brief check samples actual streams from the reviewed hardware profile. It checks identity, channels/units, advancing timestamps, recent delivery and a writable Workbench run destination. Initial Athena timing calibration still occurs in the connector before this check.

The **Optional 30-Second Signal Check** provides longer contact and baseline guidance. Reaching all-green is not required. The existing red/yellow/green map remains available.

| Finding | Recording behavior | Analysis behavior |
|---|---|---|
| Slow baseline movement, high amplitude or line contamination | Show cautions; allow recording | Assess affected electrodes/windows and outcomes |
| Flat or clipped finite signals | Retain channel findings; allow recording | Describe missing usable signal and restrict unsupported outcomes |
| Isolated timing anomalies, gaps or rate uncertainty with usable intervals remaining | Preserve original timing; show cautions | Assess timing and coverage per method |
| Required stream absent, ambiguous identity, wrong mapping or unresolved EEG voltage units | Require correction | Do not presume identity or voltage conversion |
| No usable timestamped observations or interrupted required check | Require correction/reconnection | Preserve diagnostic evidence |
| Workbench run folder cannot be written | Require a writable destination | Do not claim a successful save |

**Ready to record — signal cautions present** offers one **Record with cautions** action. It confirms the setup and automatically records the decision and findings. A second warning confirmation and written override are not required for signal cautions. Operator/participant/session details and declared runner variants remain part of setup. Confirming does not itself start LabRecorder.

**Slow baseline movement** concerns the electrical signal. **Timing uncertainty** concerns timestamps, buffering and synchronization. Contact behavior does not by itself explain a clock finding. The brief check does not certify precise stimulus timing.

## Athena's scoped admission

The packaged BrainFlow p1041 route can enter ordinary EEG acquisition after its current source-bound physical acquisition receipt passes. Its state is **ACQUISITION_VERIFIED**, with physical scope **TRANSPORT_RECORDING_VERIFIED**. The receipt covers connection, EEG identity/units, timestamp progression, live display, finalized XDF reopening and clean disconnect on the tested configuration.

This scope does not assert that the headset was worn during an equipment test. Physiological accuracy, clinical suitability, precise ERP/cross-sensor timing, optical hemoglobin mapping and Zuna reconstruction accuracy retain separate requirements. A changed or unverified source/receipt binding cannot silently acquire admission.

Ordinary recordings retain **PARTICIPANT_ACQUISITION** purpose when Bench Test Mode is off, even with quality cautions. **Bench Test Mode** remains an explicit no-participant choice. Old recordings, including earlier bench runs, keep their original classification and evidence.

## Save and analyze

Start LabRecorder before the protocol. Include the separate Optical stream if desired. When finished, press **Stop** in LabRecorder and let the XDF close before disconnecting. Protocol completion does not close an externally operated recorder. LabRecorder independently checks its selected XDF destination when saving.

Forge shows recording integrity, signal quality and analysis coverage separately. Exploratory full-recording results and accepted-window results retain their respective support. Recording permission grants no automatic clean-data or analysis-validity label.

See the [installation guide](INSTALL_AND_WORKFLOW_ALPHA_10_5_1.md) and [Forge guide](ANALYSIS_FORGE_ALPHA_10_5_1.md). The [physical acquisition summary](validation/athena_eeg_acquisition_10_5_1.json) and [scoped admission receipt](config/athena_eeg_acquisition_admission_v1_0.json) identify the tested software and observed checks. The qualification used a forty-second live-monitor/XDF recording check, clean stop and a separate reconnection check; it does not assert headset wear or clean neural signals.
