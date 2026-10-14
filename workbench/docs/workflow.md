# Study workflow

## Public Alpha 11.2.2 workflow

The [11.2.2 release guide](releases/alpha-11.2.2/README.md) records current build/publication status. Keep the exact version with a study; older release behavior is documented below rather than silently rewritten.

1. **Study and protocol.** Create or select the persistent workspace, then select a shipped or reviewed imported protocol. A successful AI return installs a reviewed declarative proposal, not new hardware or arbitrary analysis code. Review required materials and hardware before acquisition.
2. **Materials.** Choose a master or install the optional seven-film and original Lantern packages. Refresh installed masters, select one and prepare the protocol's required variants, cues, fingerprints and review records. A protocol requiring forward, retrograde and ambient movies still needs those actual assets; merely importing its definition does not construct them.
3. **Connect, record and run.** Select the real device profile, verify required streams, resolve identity/ownership/operational issues, start LabRecorder and run the protocol. Record actual eye/activity instructions and condition events. Do not infer what happened from a protocol title or folder name. Stop LabRecorder so the XDF closes before analysis.
4. **Analyze.** Open the completed recording. Run recommended analyses or choose modules. Required integrity and signal reviews establish what is available. Distinguish a finished worker from a supported endpoint; narrower descriptions cannot silently unlock a stricter prerequisite.
5. **Visual Analysis.** Start with the views available for the selected recording and verified saved outputs. Open saved TFR, measured sensor maps, traces or raw optical trends without demanding a separate state estimate. Advanced calibrated views explain their additional requirements. An unavailable state metric must not hide an otherwise available TFR pane.
6. **Results and explanation.** Read the individual native reports and local study summary. Generate an AI explanation only when wanted and configured. Numerical claims should identify their source, electrodes, support, units and screening scope. Missing ECG, respiration, calibration or optical mapping stays explicit; useful EEG/optical descriptions remain available.
7. **Ratings.** For a protocol with a supported rating contract, use the recommended native rating analysis. Read response selection, exclusions, missing windows, ordinal-category comparisons and scoring version. Newly specified rules applied to older records are post hoc. Do not borrow another protocol's question labels or contrasts.
8. **Share.** Review the bundle contents, consent, identifiers, media rights and file ledger. Public bundles, private full-telemetry bundles and AI evidence packages serve different purposes. Exporting or hashing a file does not grant permission to publish it.

The public Assistant can explain saved evidence and draft supported protocol proposals without private extensions. Provider failures do not invalidate successful numerical work. Regenerating an explanation should preserve earlier reports and the locked analysis history.

Use **Recording conditions (optional)** for explicit eye/activity context, including a short note for mixed conditions or activities not represented by the broad categories. Unknown stays unknown. These annotations are post-hoc operator reports, not measured or independently verified conditions. Revisions preserve prior files and source references; names such as “eyes closed” in a task or folder do not automatically populate them.

[Installation](installation.md) · [Optional stimuli](releases/alpha-11.2.2/STIMULUS_INSTALLATION.md) · [Hardware and endpoint limits](hardware-support.md)

## Preserved Alpha 10.5.4 workflow

Start with the [current installation and workflow guide](releases/alpha-10.5.4/INSTALL_AND_WORKFLOW_ALPHA_10_5_4.md). Alpha 10.5.4 repairs Visual Analysis entry points, recorded source selection and Athena profile validation. It retains the shared recording cursor across PRAYCG 3 Review, Time–Frequency, State landscape and Timescale inspector. The existing Analysis Forge **Recording → Analyze → Results** workflow, Gamma Scalpel 2.0 and optical exploration remain available.

## Prepare and record

1. Review settings, study-data locations, protocol materials and the exact hardware profile. A **Study Workspace** holds persistent study history; a new **Equipment Session** creates a fresh acquisition/run identity. Review the intended identities before acquisition.
2. Connect the selected equipment. For Athena, use the red/yellow/green contact map. The brief recording-readiness check samples incoming data after the connector's startup timing calibration; **Optional 30-Second Signal Check** provides longer guidance.
3. Resolve missing required streams, ambiguous identity, wrong mapping, unresolved EEG voltage units, unusable timestamp progression or an unwritable Workbench run folder. Signal quality findings can allow **Record with cautions**, which retains the findings and decision with the recording. All-green is not required, and recording permission does not establish suitability for every analysis.
4. Confirm the setup, complete operator/participant/session details and mark it ready to run. Start LabRecorder before the protocol. Select the actual task markers and all intended device streams, including separate Optical data or EOG/EMG references needed later.
5. When finished, press **Stop** in LabRecorder and wait for the XDF to close before disconnecting and analyzing. Protocol completion does not close an externally operated recorder. LabRecorder independently checks its selected XDF destination.

The [recording-with-cautions guide](releases/alpha-10.5.2/RECORDING_WITH_CAUTIONS_ALPHA_10_5_1.md) describes exact findings and Athena's scoped acquisition admission. Review [route-specific restrictions](hardware-support.md) before connecting equipment. Live Monitor observes live streams and replay; LabRecorder saves the recording.

## Open Visual Analysis

Select the intended XDF in Forge, then open the **Visual Analysis** tab immediately after **Analyze** and choose **State landscape**, **Timescale inspector** or **Paired well + TFR**. In Live Monitor, **Visual Analysis** sits beside **Time–Frequency**. **Visual sources** opens while a recording loads, updates when its streams arrive and keeps setup errors visible. Select the exact EEG and optional RR streams, declared EEG units and electrode names, and calibration interval. Generic channel numbers are not electrode positions. See the [current Visual Analysis guide](releases/alpha-10.5.4/VISUAL_ANALYSIS_ALPHA_10_5_4.md) for the supported views and recipes.

Calibration starts at shared-recording time 0 by default. When EEG begins later, deliberately select its recorded start and the intended calibration duration. This sets an offset from the shared origin; it does not move the clock or relax gap and valid-support requirements. EEG calibration still needs at least 30 seconds of valid feature support, and insufficient support leaves metrics unavailable. The revised streaming visual-state and API-A method labels are v1.1; completed historical methods keep their own identities.

Recorded replay uses one playback clock. **As seen live** uses only the recording prefix available at the playhead; backward seeks rebuild the engine. Playback speed changes presentation, while gaps, warming-up windows, missing support and stale data remain explicit. Live Monitor uses the same views as a passive consumer of selected sources; the visual feed does not start acquisition or recording.

For a compatible completed result, choose **Attach completed visual analysis…**, select its JSON, then **Open attached completed view**. Its identity must verify against the selected recording and is checked again when reopened. Full-recording estimates stay labeled **Completed analysis** and are withheld from **As seen live**. **Save view record** preserves review context, not a replacement analysis payload.

Completed CAI, historical NIP and experimental Autonomic state remain distinct choices. Raw EEG/RR does not supply all required CAI, NIP or CAI-SID components, so those incremental values remain unavailable. Gamma threshold events, media landmarks and inspection bookmarks are separate navigation choices. A shared cursor does not establish physical device synchronization or an unsupported media clock relation; a flowing surface does not establish an attractor, absorption or a physical force.

## Run the retained analyses

Choose the completed recording in **Recording**, review its signal and any condition/activity notes, then choose an analysis in **Analyze** and open the report in **Results**. The recording remains selected. The [retained Gamma Scalpel and optical Forge guide](releases/alpha-10.5.2/ANALYSIS_FORGE_ALPHA_10_5_2.md) documents these unchanged implementations.

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

[Workbench](../README.md) · [Installation](installation.md) · [Visual Analysis guide](releases/alpha-10.5.4/VISUAL_ANALYSIS_ALPHA_10_5_4.md) · [Retained Gamma and optical guide](releases/alpha-10.5.2/ANALYSIS_FORGE_ALPHA_10_5_2.md)
