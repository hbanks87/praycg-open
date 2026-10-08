# Study workflow in Alpha 10.5.2

Start with the [current installation and workflow guide](releases/alpha-10.5.2/INSTALL_AND_WORKFLOW_ALPHA_10_5_2.md). Alpha 10.5.2 keeps the Analysis Forge's **Recording → Analyze → Results** workflow and adds Gamma Scalpel 2.0 and improved optical exploration.

## Prepare and record

1. Review settings, study-data locations, protocol materials and the exact hardware profile. A **Study Workspace** holds persistent study history; a new **Equipment Session** creates a fresh acquisition/run identity. Review the intended identities before acquisition.
2. Connect the selected equipment. For Athena, use the red/yellow/green contact map. The brief recording-readiness check samples incoming data after the connector's startup timing calibration; **Optional 30-Second Signal Check** provides longer guidance.
3. Resolve missing required streams, ambiguous identity, wrong mapping, unresolved EEG voltage units, unusable timestamp progression or an unwritable Workbench run folder. Signal quality findings can allow **Record with cautions**, which retains the findings and decision with the recording. All-green is not required, and recording permission does not establish suitability for every analysis.
4. Confirm the setup, complete operator/participant/session details and mark it ready to run. Start LabRecorder before the protocol. Select the actual task markers and all intended device streams, including separate Optical data or EOG/EMG references needed later.
5. When finished, press **Stop** in LabRecorder and wait for the XDF to close before disconnecting and analyzing. Protocol completion does not close an externally operated recorder. LabRecorder independently checks its selected XDF destination.

The [recording-with-cautions guide](releases/alpha-10.5.2/RECORDING_WITH_CAUTIONS_ALPHA_10_5_1.md) describes exact findings and Athena's scoped acquisition admission. Review [route-specific restrictions](hardware-support.md) before connecting equipment. Live Monitor observes live streams and replay; LabRecorder saves the recording.

## Analyze a completed recording

Choose the completed recording in **Recording**, review its signal and any condition/activity notes, then choose an analysis in **Analyze** and open the report in **Results**. The recording remains selected. See the [Alpha 10.5.2 Forge guide](releases/alpha-10.5.2/ANALYSIS_FORGE_ALPHA_10_5_2.md) for controls and result behavior.

| Analysis | What to review |
| --- | --- |
| **Gamma Scalpel** | Recorded electrode support, usable measured EOG/EMG references, reference timing and quality, original versus screened results, retained duration and supported condition comparisons. Missing or ambiguous references have explicit reasons; EEG-only fallback remains available. |
| **Explore optical signals** | Whole-recording raw trends and descriptive statistics, quality annotations, full and screened spectra. Optional source, task scope and spectral settings are under **Details** and saved with the attempt. |

Gamma Scalpel preserves measured EEG and uses references for screening; automatic signal subtraction is not included. Quiet references do not establish a neural origin for gamma. Athena outcomes use the measured TP9, AF7, AF8 and TP10 electrodes; endpoints requiring unrecorded regional electrodes remain unavailable. Read the [Gamma method guide](releases/alpha-10.5.2/Gamma_Scalpel_v2_0/README.md) and optional [reference profile guide](releases/alpha-10.5.2/Gamma_Scalpel_v2_0/REFERENCE_PROFILE_GUIDE.md) for the exact contracts.

Offline optical spectra prefer 30-second windows and fall back to labeled 10- or 5-second windows. Full and screened results use the same resolution, gaps remain visible, and raw trends/statistics can remain available when a spectrum is unsupported. These adaptive windows apply to Forge; live/replay retains its existing spectral policy.

Optical exploration works across protocols and independently of EEG quality, provided optical data was saved in the XDF. Reusable verified instrument profiles can enable relative HbO/HbR under their declared assumptions. The bundled Athena raw profile leaves HbO/HbR unavailable until its missing mapping, geometry and intensity/firmware information is established. Read the [Athena optical source review](releases/alpha-10.5.2/ATHENA_OPTICAL_SOURCE_REVIEW_ALPHA_10_5_2.md) and [reusable instrument profile guide](releases/alpha-10.5.2/Optical_Signal_Review_v1_0/REUSABLE_PROFILE_GUIDE.md).

## Interpret, package and extend

Review recording integrity, signal quality and analysis coverage separately, including timing evidence, artifacts and unavailable or `NOT_ESTIMABLE` results. A locked plan records intended analyses; execution receipts show what actually ran. Locking a plan after inspecting outcomes does not make the analysis prospective.

Review consent, privacy, identifiers and stimulus rights before sharing a bundle. Private study and AI-review packages can contain sensitive data even when a smaller results package appears suitable for sharing. For a first software demonstration, use the [example materials](../../examples/README.md) and an explicitly labeled no-participant bench workflow.

The preserved [Alpha 10.2.1 detailed workflow](releases/alpha-10.2.1/WORKFLOW_ALPHA_10_2_1.md) remains a historical reference for workspace, packaging, authoring and recovery concepts. Use current guides for recording readiness, acquisition status and Forge controls.

[Workbench](../README.md) · [Installation](installation.md) · [Current Forge guide](releases/alpha-10.5.2/ANALYSIS_FORGE_ALPHA_10_5_2.md)
