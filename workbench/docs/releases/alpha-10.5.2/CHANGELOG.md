# PRAYCG Workbench changelog

## Alpha 10.5.2 — Gamma Scalpel 2.0 and simpler optical exploration

- Adds one governed Gamma Scalpel action with measured EEG and optional Cerelog or compatible EOG/EMG references.
- Checks participant, source, units, continuity and timing; rejects ambiguous metadata and explains missing or unusable references.
- Uses measured references for the corresponding artifact assessment, retaining EEG integrity checks and the original legacy method comparison.
- Reports original and screened gamma, retained duration and supported condition comparisons using matched portions without reusing windows.
- Limits Athena gamma outcomes to its measured TP9, AF7, AF8 and TP10 electrodes.
- Makes optical review default to the whole recording, independently of EEG QC; saves source, scope and settings with each attempt.
- Adds automatic 30-, 10- or 5-second spectral windows with matching full/screened resolution, gap handling and explicit frequency support.
- Adds reusable versioned instrument profiles and automatic recording bindings/baselines; verified profiles can enable relative HbO/HbR. The bundled Athena profile remains raw-only because required conversion facts are unresolved.
- Keeps recording selection and progress visible, with optional optical settings under Details.
- Corrects migration of saved tools from prior public Workbench folders to the current release.
- Includes complete installers, public method/workflow guides, regression evidence and checksums; original recordings and prior releases stay intact.

## Alpha 10.5.1 — Recording with cautions, Forge organization and optical/replay review

- Adds source-bound scoped Athena EEG acquisition/recording admission, separately identifying transport verification and other unvalidated capabilities.
- Makes the thirty-second signal check optional, with brief actual-data recording readiness and retained connector startup timing calibration.
- Allows finite signal-quality cautions through one Record with cautions action; saves findings for analysis and removes repeated quality confirmation/freeform override.
- Separates slow electrical baseline movement from timing uncertainty and retains actual capture, identity, units and write-failure correction requirements.
- Keeps recording purpose independent of quality; historical bench labels and evidence are preserved.
- Reorganizes Forge into Recording / Analyze / Results with persistent recording context, analysis cards, result shortcuts and one current-operation area.
- Makes eligible dedicated Muse Zuna comparison visible; keeps generated signals and hardware QC distinct.
- Enables full-rate Time–Frequency XDF replay with history rebuilding, gaps and presentation-only playback speed.
- Adds raw optical trends and slower spectra to live, replay and Forge; relative HbO/HbR requires verified source-bound metadata.
- Ships complete installers and public installation, recording, Forge, replay/optical and release documentation. Current acceptance artifacts retain their observed scope.

## Alpha 10.5.0 — Live Time–Frequency and Forge Explorer

- Adds an optional Live Time–Frequency popup using the full-resolution EEG already received by the Live Monitor. A bounded rolling spectral history supports electrode heatmaps and a rotatable three-dimensional categorical-channel view.
- Adds a separate exploratory Time–Frequency Explorer module to the Analysis Forge, retaining the selected recording, original timeline, quality evidence and actual-condition notes.
- Shares viewer controls for live and recorded data, including fixed color scales, electrode labels, source selection, visual pause, inspection and export.
- Supports continuous measured-signal exploration and eligible saved event-related results with their original estimator, baseline and trial-support information.
- Shows per-electrode accepted support, gaps and recorded quality reasons. Compatible conventional and saved Zuna derivatives retain source labels and generated-sample provenance.
- Adds compatible recording comparisons and portable interactive HTML, static-image and numerical reports with source and processing information.
- Uses independently implemented Workbench code. The upstream eeg-tfr-volume project informed the requested visual concept; its code and example recording are not bundled.
- Provides the complete installers and current source-bound validation. Historical acquisition and reconstruction qualifications keep their original scope.

## Alpha 10.4.10 — Forge quality, comparisons and consistent Zuna processing

- Exploratory full-recording reporting remains available when accepted coverage is insufficient for an outcome.
- Per-electrode and per-analysis eligibility, paired-channel windows, and separate recording-integrity, signal-quality and coverage descriptions.
- Versioned Athena QC recipe, retained prior recipe, and local artifact guards in place of blanket neighboring-window exclusion; amplitude and clipping screens remain explicit engineering choices.
- Median, variability, large-burst influence and consistent full/accepted/equal-duration recording comparisons.
- Consistent preprocessing and baseline for optional Zuna comparisons, sample-aligned generation masks and audited joins.
- Optional Zuna comparison with actual generated coverage, processing duration, distortion metrics and checked supported-device metadata.
- Actual recording-condition notes, stable recording selection and progress for long operations.
- Complete installers and fresh release validation. No change to existing recordings or prior releases.

# PRAYCG Workbench — Changelog

## Alpha 10.4.9 — Cerelog off-body bench controls and bundled timing-patched recorder

- Promotes the patched 10.4.8 Workbench into a separate complete release, retaining the normal installers, 91 protocol definitions, 20 Athena editions and existing Forge/Muse workflows. Earlier releases and user studies are not merged or rewritten.
- Adds the exact Cerelog V1 **5 EMG / 2 EOG / 1 ALS** off-body recording controls through **Hardware Selection → reviewed and locked Hardware Profile → Connect & Launch**. Eight physical channels publish three signal feeds plus Timing diagnostics. Generic Home connector management does not authorize a recording.
- Requires explicit Bench Test Mode, battery-only/off-body and trusted-network/local-recording consent, an unlocked equipment session and matching run/launch/firmware/stream identities. Each recording uses a new output path and remains non-participant equipment data without task markers.
- Gives owned bench recordings a graceful-stop lifecycle, independent file-closure check and raw timing audit. Connector stop, generic force-close and session replacement remain guarded while recording or evidence finalization is unfinished. Failure evidence is preserved without claiming successful closure or timing.
- Bundles the timing-patched LabRecorder GUI and CLI, required runtime, per-binary build identity and synthetic qualification summaries. Launch rejects an unverified selection; GUI configuration is hash-bound and explicit, with AutoStart and remote control disabled and online synchronization unset. GUI remote control remains **NOT QUALIFIED**.
- Fresh settings use the bundled recorder; nonblank saved recorder selections are preserved. **Use Bundled Paths** explicitly selects the current bundle. Protocol recording through the LabRecorder GUI remains an operator action, separate from the owned Cerelog equipment recorder.
- Retains twelve synthetic recorder trials from the unchanged 10.4.8 patch build, covering both shutdown orders three times per binary. CLI evidence does not qualify the GUI, and synthetic qualification does not establish physical synchronization, electrical safety, participant approval or scientific validity. Raw generated XDF fixtures are excluded from the public Workbench; the bundled distribution note identifies the full companion archive.
- Does not change Bench Test Mode's protocol/hardware compatibility boundary. A four-channel Muse profile still cannot satisfy a sixteen-measured-channel reconstruction protocol. No automatic firmware flash, reconnect, optical alignment or cross-board synchronization approval is added.
- New 10.4.9 acceptance is source-bound offline contract/regression checking only. Copied 10.4.8 full-install, saved-recording and model acceptance remain historical; no fresh full installation, model execution, physical acquisition, manual whole-workflow or second-machine validation is claimed. Consult the current build record for exact results.
- See the [10.4.9 installation and workflow guide](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.10).

## Alpha 10.4.8 — Live Athena signal map and optional Zuna Signal Review

- Adds an automatically opened four-electrode Signal Check map after Muse connection, with red/yellow/green signal states, grey waiting/disconnected state, short sensor-specific advice and a reopen button in Muse Connect and Live Monitor.
- Scores the latest five seconds of the existing full-resolution EEG stream about once a second. Repeated passing windows are needed for green; source mismatch, frozen/stale data, viewer shutdown, replay and demonstration data clear live readiness.
- Adds a read-only finalized-XDF guard before Forge preparation and QC. Active, unclosed or changing recordings explain that LabRecorder must be stopped and saved. Raw recordings remain unchanged.
- Binds subsequent processing to the exact current authenticated QC report and recording, including after repeated checks. Fixes the existing Muse reconstruction worker's explicit QC selection.
- Adds optional general Zuna Signal Review for compatible EEG recordings, including ordinary Athena rest protocols. The historical Muse and sixteen-channel reconstruction benchmarks retain their original methods and requirements.
- Checks actual units, sampling, channel positions, reference and available context before processing. Generates separate recorded/conventional/Zuna branches, repair masks, progress/checkpoint records and comparison reports.
- Limits targeted repair to short portions of measured channels with sufficient remaining context. Generated samples and any exploratory extra channels remain visibly distinct from measured data. No missing acquisition gap is silently filled and no raw QC verdict is promoted by model output.
- Adds explicit measured/conventional/Zuna source choices for compatible spectral and complexity analyses, with measured input selected by default and separate output provenance.
- Reuses the verified optional model through the normal Zuna installer. Model processing stays local; ordinary QC does not require the model. Progress, cancellation and identity-checked resume are provided.
- Adds tests for live-map freshness, finalized recordings, exact QC binding, immutable processing inputs, masks, source selection and controlled model comparisons. Acceptance evidence distinguishes software/model execution from physical or physiological validation.
- Full Workbench with normal Core, Live Monitor, Hardware Connectors and optional Zuna installers. Retains all 91 protocol definitions, 20 Athena editions and the previous recording-selection, protocol-selection and acquisition UUID repairs.
- See the [10.4.8 installation and workflow guide](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.8).

## Alpha 10.4.7 — Keep the selected recording when checking its signal

- Fixes Analysis Forge searching beyond an explicitly selected recording folder and becoming blocked by another complete copy of the same run.
- Treats the sole XDF in a folder chosen through Open recording as the explicit choice, then verifies it against the governed run UUID.
- Preserves that choice through rescans and successful preparation. A folder with multiple XDF files, a missing selected file, or a different run UUID stays unresolved and displays the reason.
- Displays and logs the actual preparation failure instead of referring users to an empty log or concealing the cause behind a generic message.
- Adds current-handler tests for folder selection through Check signal, duplicate copies elsewhere, refresh persistence and incompatible inputs.
- Preserves raw recordings, previous analysis attempts, the 10.4.6 new UUID repair, the 10.4.5 protocol-selection repair and all prior Muse Forge fixes.
- Full application and normal installers, retaining all 91 protocol definitions and 20 Athena editions.
- See the [10.4.7 installation and workflow guide](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.8).

## Alpha 10.4.6 — Start a new equipment session after a completed Athena run

- Fixes the new hardware acquisition UUID button being blocked by an intact completed Athena session from an earlier release.
- Uses the same verified historical-session checks for protocol selection and new-session allocation. Completed records must still pass identity, completion, runner and ownership checks.
- Creates a fresh, disjoint UUID with recording readiness reset. Existing recordings, completed locks and released ownership records are preserved.
- Keeps active runners, unresolved acquisition, damaged records and uncertain ownership blocked. New acquisition continues to require a current reviewed hardware route.
- Adds regression coverage for the actual current Workbench handlers, including protocol selection followed by new UUID creation and unsuccessful attempts that must preserve the existing session.
- Retains all 91 protocol definitions, 20 Athena editions, Muse Forge fixes and full installation tools.
- See the [10.4.6 installation and workflow guide](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.6).

## Alpha 10.4.5 — Select a new protocol after an earlier Athena session

- Fixes the “Archived session lock is invalid” error when a completed experimental-hardware session was recorded with an earlier Workbench release or installation location.
- Separates historical terminal-session integrity from current connector admission. Archived identities, completion history and inactive runner/ownership checks remain required; active, unfinished, inconsistent or changed evidence still blocks editing.
- Preserves previous session records. This correction does not re-arm a completed run or approve an old hardware profile for new acquisition.
- Retains all 10.4.4 Muse Forge fixes, 91 protocol definitions, 20 Athena editions and complete installers.
- See the [10.4.5 installation and workflow guide](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.6).

## Alpha 10.4.4 — Athena signal checks and simpler Analysis Forge

- Uses one versioned raw Athena readiness screen across quality checks, descriptive analysis and preprocessing, with accepted time and channel-specific reasons. Advanced results cannot silently use windows rejected by this shared screen.
- Preserves the native reference for the Athena preprocessing route and exact rest/meditation event windows; keeps separate Zuna reference rules.
- Corrects the false “missing or empty output” message when a valid worker report declines an estimate because usable input is insufficient.
- Recognizes recorded Muse streams independently of the protocol label. Shows supported Athena guidance and optional advanced controls without granting an unrelated run the dedicated reconstruction protocol's authority.
- Distinguishes model installation from preparation and actual inference.
- Preserves earlier signal reports, analysis attempts and prepared inputs when a recording is checked again. New analyses select the exact current quality report.
- Retains final connection diagnostics and replay-audit evidence on errors, with sensor-specific messages and a clear separation from task/recording completion.
- Full standalone application and installers; all 91 protocol definitions and 20 Athena editions retained. Saved bench data are used privately for software regression and are excluded from the distribution. No new physical or physiological validation is claimed.
- See the [10.4.4 installation and Forge guide](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.6).

## Alpha 10.4.3 — Simpler Muse connection inside Workbench

- Adds **Connect Muse S Athena…** in equipment setup and **Connect Muse…** in Live Monitor. The usual path scans nearby devices, lets the operator choose the headset, starts the managed LSL connection and opens its exact EEG outlet in the viewer.
- First use collects the setup reviewer and explicit bench-only confirmation, then prepares the packaged Athena profile without separate draft/save/lock navigation. It does not arm a protocol or start a recording.
- Keeps **Find again**, connection progress, **Show live EEG** and **Disconnect** together; manual Bluetooth-address entry is under Advanced. There is no stream-name copying in the normal connection workflow.
- Preserves the four-channel timing repair, 91 protocol definitions, separate Athena editions, analysis and optional Zuna workflows. The distribution includes the full application and complete installers.
- Current automated checks and full installation results belong to this build. Alpha 10.4.2 hardware observations remain historical; no new physical streaming, wearer-contact or EEG-quality test is claimed. Athena stays experimental and bench-only.
- See the [10.4.3 installation and connection guide](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.6).

## Alpha 10.4.2 — Full Workbench release with explicit Athena timing

- Windows connector status writes retry a temporary file-lock conflict for up to one second; a persistent write failure still fails the acquisition instead of hiding the error.
- Retains the complete standalone application, all 91 protocol definitions, normal Core/Live Monitor/Hardware installers, and the separate optional Zuna installer and shared-model storage.
- Adds the p1041-only `athena_p1041_counter_host_causal_regression_v1` timing policy: two-second host-read calibration, causal per-sensor counter/host fits, explicit missing-block gaps, and bounded clock estimates. Published unique values and their original BrainFlow timestamps remain in matching streams. Only a same-full-counter replay within 250 ms whose every non-timestamp row, including markers, matches exactly is suppressed; both complete original/repeated blocks are durably retained in a private audit first. No interpolation, insertion, sorting or resampling conceals gaps, and nonmatching duplicates fail the segment.
- Keeps nominal EEG/IMU/optical rates distinct from estimated rates. Derived published times do not recover a hardware sample clock or certify ERP, optical or cross-sensor synchronization. Ambiguous counters and discontinuities terminate the segment instead of silently reconnecting.
- Full source-candidate installation passed for Core, Live Monitor and Hardware Connectors after using the system certificate store for Core downloads. The optional Zuna model was not installed as part of that check; the extracted delivery and a second machine were not tested by the installer receipt.
- Publication requires fresh, source-bound physical LSL, live monitor worker/render, EEG plus Diagnostic plus marker XDF, Workbench reopen and clean-stop evidence. See the current build record for actual results and counts. Athena remains experimental and bench-only.
- See the [10.4.2 installation and workflow guide](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.0). The historical 10.4.1 results below are retained unchanged.

## Alpha 10.4.1 — Full Workbench release with Athena address correction

- Distributed the complete standalone Workbench with `INSTALL.bat`, `START_PRAYCG.bat`, optional `INSTALL_ZUNA.bat`, and the full application. Normal setup retains separate Core, Live Monitor, and Hardware Connectors environments.
- Corrected Muse S Athena Bluetooth-address normalization for BrainFlow's native matching, with input validation and clearer connection diagnostics. Matching Athena/Crown hardware definitions retain their source identities. Existing user profiles and locked sessions are not silently rewritten.
- Preserved all 91 protocol definitions, including the 20 separate Athena editions, and the existing acquisition, analysis, reconstruction, and research-bundle workflows.
- A bounded test on the same physical headset reached p1041 streaming and outlet creation using the corrected address. Streaming then stopped with `BrainFlow source timestamps are invalid or non-increasing.` The managed LSL test received zero EEG samples; a separate eight-second native probe confirmed non-increasing source timestamps. The timestamp guard remains intact.
- Usable Muse LSL streaming, Live Monitor display, saved-XDF acceptance, and a fresh full installation remain unverified. The physical connection result applies to the identical connector bytes included here, not a completed end-to-end validation of the whole release. Athena remains experimental and bench-only.
- See the [10.4.1 installation and workflow guide](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.0) for installation, the measured blocker, and the retained protocol scope. Exact automated release results are recorded in the current build evidence.

## Alpha 10.4.0 — Athena protocol compatibility and descriptive EEG

- Added compatibility profiles for every protocol: 91 definitions across 71 main-browser and 20 prospective modules. Task execution, measurement support and implemented analysis coverage are shown separately.
- Added 20 distinct Athena editions: three core protocols, ten prospective sequences, six exploratory ERP tasks and EEG-only resting calibration. Original scientific contracts remain separate. Prospective selection and freezing explicitly preserve the chosen edition and counterbalancing.
- Added a guided, equipment/session-bound setup check for discovery, stream continuity, markers, live-monitor observations and reopening a saved recording. It records evidence without approving experimental hardware for participant acquisition.
- Replaced hardcoded recording instructions with the selected EEG stream. Original prospective barcode requirements are enforced; Athena editions explicitly omit unsupported optical claims.
- Added a pinned raw four-channel descriptive recipe with artifact, gap, window, coverage and referencing rules. Insufficient EEG produces NOT_ESTIMABLE while behavioral results remain available. Muse Zuna reference rules remain separate.
- Fixed motor execution/imagery and effector selection, post-exclusion class counts, N2pc target-side selection, and SVNA ranking correction/timestamp alignment. Added measured-source, extra-sensor and participant ownership checks.
- Validation is software-only; exact test counts, skips and extracted-package results are recorded in the build evidence. No physical headset, fresh-machine installation or scientific validation is claimed.
- See the [current operator guide](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.0) and [twelve-item traceability](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.0).

## Alpha 10.3.14 — Separate Muse S Athena Zuna feasibility study

- Added **Muse S Athena EEG Reconstruction Validation**, a separate ten-minute generated-cue protocol for the managed BrainFlow Muse S Athena p1041 route. Four native EEG channels are declared and reviewed; auxiliary electrodes, fNIRS and ALS are not invented or required.
- Added **Zuna Muse S Athena Reconstruction — Experimental**, with four fixed three-input/one-hidden-channel folds and separate Muse evidence. Reports compare generated predictions against withheld measurements, three-electrode spherical splines and a fixed-zero baseline. Sparse interpolation limitations and non-independent channels/windows remain explicit.
- Connected the new protocol, analysis selection, optional local model runtime, reports and bundle provenance without treating Muse data as the original sixteen-channel benchmark. Model weights remain pinned and installed separately; no automatic download, upload or live AI control is added.
- Prevented a slightly lower recording-wide effective rate from falsely excluding the Muse analysis during planning. The worker still requires the exact nominal 256 Hz native stream and checks local continuity, piece rate and coverage; this is not permission to analyze an incompatible sampling route.
- Preserved the Alpha 10.3.13 sixteen-channel validation plan, receipt and authoring documents unchanged. A separate historical-context record states that the new shared runtime is not its exact frozen implementation. No old results, raw recordings or protocol identities are relabeled, and Muse runs are not automatically enrolled in that old plan.
- Kept shared model caching, prior ALS geometry/session-binding fixes and ordinary QC workflows. Headless and synthetic software acceptance do not establish physical headset support, clean-signal reconstruction or scientific efficacy. Exact tests, environment-related skips and extracted-package checks are recorded in the current build-validation evidence.
- See the [current installation and Muse workflow](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.0).

## Alpha 10.3.13 — Zuna error context and shared ALS setup evidence

- Added explicit absolute-error and fixed-zero comparison reporting alongside existing Zuna/interpolation metrics. Target variance, evaluated coverage and aggregation rules remain visible; undefined normalized scores stay unavailable rather than becoming zero or silently dropping electrodes. A relative improvement over a poor baseline is not automatically adequate reconstruction.
- Added a shared ALS placement geometry contract for calibration, placement checking and supported runner presentation. Saved pixel position/size and display identity are checked explicitly; placement review is distinct from measured optical-timing evidence.
- Bound new optional ALS selection to the current acquisition session, locked hardware profile and actual outlet identity. An older attempt's source identifier is not silently reused. Existing post-hoc corrections and historical recorded evidence remain separate.
- Added a separately frozen next-validation plan with explicit engineering success criteria, independent-session requirements, attempt limits and stopping rules. The declared margins are project choices, not universal neuroscience-validity thresholds. Freezing a plan does not start a study or turn development data into prospective evidence.
- Preserved original model weights, reconstruction settings, existing XDFs and prior comparison results. Saved-output diagnostic review does not perform new model inference or retroactively validate a recording. Shared model caching and release-local environments/receipts from 10.3.12 remain supported.
- Release evidence distinguishes behavioral/synthetic checks and extracted-package verification from private saved-data review, physical acquisition, display/sensor timing and prospective validation. No new installation, model run, physical hardware test or generalizable model benefit is claimed.

## Alpha 10.3.12 — Verified shared Zuna model cache

- Added a reusable, revision-and-asset-manifest-keyed Zuna model cache. New release folders can reuse verified model files and the pinned Zuna wheel while keeping their own isolated Python environment, installation receipt and license notices.
- Added configurable shared storage and explicit import from an existing installation through `-SharedZunaRoot` and `-ImportZunaFrom`. Imports copy only verified pinned assets; old installations are retained, and study data, reports, inference checkpoints and Python environments are not imported.
- Bound runtime model selection to the current release's installation record. A missing, corrupt or mismatched cache is not silently accepted, and analysis does not download or install anything automatically. `-CheckOnly` remains a non-installing inspection.
- Excluded private local storage pointers, installation receipts/notices and environments from the public software archive and its immutable source inventory. The shared model itself is not shipped in the ZIP.
- Preserved the 10.3.11 timing policy, earlier ALS/contract fixes, protocol identities, EEG estimators, model weights and original recordings. Release verification uses synthetic storage fixtures and regression/package checks; this build does not migrate the user's installed files, perform a fresh download/installation or demonstrate a new model benefit.

## Alpha 10.3.11 — Evidence-bound host-receipt timing for Zuna

- Added a versioned Zuna preparation route that distinguishes supported host-receipt timestamp jitter from acquisition discontinuity using exact same-run bridge and packet-counter diagnostics. A derived sample clock is an analysis estimate; original XDF timestamps and QC are not rewritten or reclassified as physically validated timing.
- Bound optional bridge-manifest and chunk-diagnostic inputs through the Analysis Forge inventory, managed module arguments and guided comparison workflow. Missing, ambiguous, stale, wrong-run or incompatible evidence remains explicit; it is not silently borrowed from another recording.
- Retained actual packet-loss, duplicate/reset, invalid-time, sample-coverage and unsupported-route checks. No EEG amplitude-quality threshold, electrode map, target selection, filter or model weight was loosened to obtain a favorable result.
- Preserved original contracts, prior analysis outputs/checkpoints, protocol identities, reviewed ALS correction, research bundles and installation boundaries. Preparation does not start inference automatically, and a preparation pass is not a demonstrated model benefit or optical-timing pass.
- Current release evidence distinguishes source-bound behavioral tests, broader regression suites, synthetic numerical-chain checks and extracted-package verification from optional private recording inspection. No fresh physical acquisition, full model inference, clean-machine installation or second-machine replication is claimed.

## Alpha 10.3.10 — Zuna input discovery and reviewed ALS binding

- Fixed Analysis Forge's run-evidence discovery for the reviewed `zuna_validation_contract_v2_0.json`, while retaining supported legacy contracts. Selection is tied to the exact run and observed-block evidence; conflicting or mismatched contracts remain actionable errors, not silently selected substitutes.
- Added **Review ALS stream binding** after Required QC. An explicit reviewer and reason can bind the correct source actually present in the selected XDF through a separate immutable, hash-bound post-hoc artifact. The original acquisition contract, raw recording and previously prepared or locked work are not rewritten.
- Carried the selected optional correction through guided preparation, managed execution and reporting, with stale/tampered/wrong-recording rejection and explicit corrected-versus-original provenance. A corrected source identity is not a measured optical-timing PASS or a change to EEG reconstruction evidence.
- Retained protocol identities, the ten-minute schedule, numerical methods, held-out electrodes, model weights, quality policy, startup fixes, Results and research bundles. No model efficacy claim, live AI, automatic source correction, automatic upload or new participant acquisition is added.
- Release evidence records current source-bound behavioral regressions, broader suites, a synthetic analysis chain and extracted-package checks. Physical acquisition, a new full model run, clean-machine installation and second-machine replication are not claimed.

## Alpha 10.3.9 — ALS ownership and accessible Zuna setup

- Fixed the barcode ownership check counting a Windows virtual-environment launcher and its base-interpreter child as two independent OpenBCI bridges. Grouping requires matching full script/arguments, session, port, process lineage/creation evidence and virtual-environment/base-executable identity. Unknown or competing processes remain separate; inspection does not stop processes.
- Retained raw process identities for guarded shutdown/recovery. Updated the barcode error text to remove the obsolete Alpha 9.3 label and direct operators to managed stopping rather than killing individual launcher/child windows.
- Moved reviewed Zuna channel/reference, template-geometry and optional optical-source dialogs ahead of fullscreen PsychoPy and timed content. Retained explicit review, the fullscreen R confirmation, authority revalidation, recorded declarations and cancellation/finalization evidence.
- Preserved both reviewed protocol identities, the legacy fixed-map protocol, existing analysis methods and the 10.3.8 correctness changes. No acquisition-quality threshold, model weight, numerical estimator, raw recording or historical result was changed.
- See this release's build-validation record for executed tests and limitations. Mocked process trees and headless runner tests are not a physical device test, proof of every Windows focus configuration, a new model comparison or scientific validation.

## Alpha 10.3.8 — Correctness, timing and evidence integrity

- Repaired A-MRED/ITP/NIP annotation and time-column compatibility, exact anchor-lock interpretation, phase-scramble inclusion and CAI shot-order aliases. Failed producers cannot supply partial tables as completed dependencies.
- Replaced affected sign-only claims and unsupported overlapping-window inference with descriptive effects and explicit uncertainty limitations. Preserved the Micro Handoff algorithm and its unfavorable positive-control evidence; sensitivity remains unvalidated.
- Added hash- and timing-bound fingerprint-window alignment, audited raw/standardized covariates and descriptive adjusted/unadjusted comparisons. Missing, collinear or unsupported alignment is reported without blocking unrelated descriptive analyses.
- Corrected requested-duration/tail acquisition checks, optical pulse/noise checks and ALS grade compatibility; added graceful OpenBCI stop requests and native flip-timed marker evidence. Physical device/display timing is not certified by software tests.
- Anchor hashes use the actual runner field. Bundle reviews verify pre-existing checksums and original content before writing versioned review receipts. Historical recordings, theory documents and results are retained.
- Corrected BIDS event origins/native column aliases, headerless regular physiology and explicit unit handling. Pseudonymous labels do not anonymize raw XDF. Independent synthetic readback is distinct from whole-dataset BIDS validation.
- Tightened common numeric-text screening in AI explanation returns; checked placeholders are not semantic validation. Six-question reports and consolidated Results remain, with failures and unavailable estimates visible.
- Core installation is isolated and direct requirements are constrained to the observed release-test versions. Matching source/tests ship; public release verification does not rewrite manifests. Full transitive artifact locks, fresh-machine installation, physical Cerelog validation and new Zuna efficacy studies remain separate work.
- Exact executed coverage and skips belong to the current build-validation record. Earlier evidence is retained as historical, not newly certified. No ISC requirement, new exploratory module expansion, automatic AI upload or adaptive human experimentation is introduced.

## Alpha 10.3.7 — Boundary-safe Zuna integration and transparent comparison

- Integrated the separately tested preparation correction: center each channel within each independent continuous preparation segment before line-padded resampling, retaining the declared filter, reference, clock mapping and scoring boundaries. Processing remains offline/noncausal.
- Added versioned preparation provenance and explicit checkpoint bindings. Historical recordings, recipes, reports and incompatible checkpoints are preserved, not silently converted or reused.
- Added automatic descriptive overall and eye-condition summaries, reconstruction errors, contiguous-window spectral comparisons and a mandatory endpoint before the final comparison filter. No unfavorable block is dropped because the model loses.
- Tiny or unsupported groups report insufficient data, not misleading numerical conclusions. Measured targets, conventional interpolation and model-generated estimates remain distinct; repeated windows are not independent replications.
- Preserved Alpha 10.3.6 per-module/study explanations and reviewed AI returns, optional local Zuna installation, private telemetry boundaries and ordinary acquisition/analysis workflows. No live AI, automatic upload, new participant recording or new full model comparison is part of this build.
- Exact executed tests and limitations are recorded in the shipped build-validation evidence. Correcting preparation does not establish scientific efficacy or clean-signal restoration.

## Alpha 10.3.6 — Evidence-grounded explanations and reviewed AI returns

- Added six-question per-module explanations, linked literal measurements and versioned descriptions of implemented CAI/SID, NIP/CET/CET-R/EET and Zuna measures. Chained child outputs retain their own explanations and limitations. Numerical estimators are unchanged.
- Added a consolidated study explanation with execution coverage, unfavorable findings, unavailable endpoints, source links and shared-input/dependency disclosures. Cross-method agreement is not automatically asserted; unknown recorded conditions remain unknown.
- Added **Explain existing results** in Analysis Forge Results. Reports are content-addressed derivatives tied to saved plans, attempts and reporting code. Historical explanations do not unlock plans, rerun workers or replace original outputs.
- Isolated interpretation, child rendering, Markdown, credits, study rendering and saving failures from numerical execution status. Same-session UI refresh failures retain the previous clearly labeled snapshot instead of blanking results.
- Extended the existing AI-ready explain export with an evidence packet and structured return instructions/template. New returns receive identity/attempt/source/value checks and a separate named human review before display. External module and study explanations remain labeled derivatives; stale results are withheld.
- Retained local-only packaging, private-data review, inert legacy return staging, method credits, raw-data boundaries and optional Zuna installation. No automatic AI upload/API, live protocol control, new model inference or hardware validation is claimed. See the scoped build record for checks actually executed.

## Alpha 10.3.5 — Tolerant recording, precise analysis windows

- Separated recording readiness from analytical suitability. Reviewable drift, intermittent transport/timestamp findings and partial-channel faults remain warnings with exact evidence, not automatic BENCH requirements. Missing or wholly unusable required inputs and identity/units errors still block.
- Added explicit readiness policy, dimensioned findings and hash-bound operator warning acknowledgment. Partial preflight capture evidence is preserved; historical reports are not relabeled.
- Added independent continuous-segment preprocessing with declared edge guards, retained/excluded coverage and boundary-aware spectral, complexity, microstate, connectivity/PAC, ERP, RSA and motor-imagery consumers. Fixed train-only CSP covariance-rank handling after common-average reference.
- Analysis protocol identity follows the selected recording rather than an unrelated active acquisition selection. Results distinguish execution, module assessment and inherited cautions; uncomputed modules retain explanations.
- Guided historical Zuna preparation routes incompatible old contracts to explicit block-wise review, suggests same-run clock evidence and preserves selected reviewed recipes. Added all-eight-block eligibility receipts; earlier calibration gaps do not veto intact evaluation blocks. The legacy endpoint and original BENCH records stay unchanged.
- Added a separate optional ALS optical-timing Zuna protocol, with pre/post sequences outside the 600-second content and settling guards. Independent edge reports preserve missing/extra-pulse and clock uncertainty. Optical validation is not acoustic-onset or continuous synchronization proof.
- Retained private/public bundle boundaries and optional local model installation. See the release notes and build-validation record for executed tests, private preparation/analysis checks and limitations. No new participant model comparison or physical-device validation is claimed.

## Alpha 10.3.2 — Zuna validation and guided offline workflow

- Made the adapter's coordinate contract explicit and versioned, with upstream-FIF configuration evidence and disclosed clipping. Retained-only referencing/normalization prevents hidden target leakage; the old comparison remains immutable.
- Added engineering checks for scaling, metrics, filtering, token handling, invalid inputs and execution identity. These are not claims of improved EEG or clinical validity.
- Added a separately reviewed prospective montage variant while preserving legacy protocol/contract support. A suggested cap map requires explicit operator review before acquisition.
- Added guided Zuna review, preparation and results inside the Forge, separate execution/comparison/evidence states, resource selection and compatible-checkpoint interruption/resume.
- Preserved fixed development-comparison plans, all declared attempts and original recording identities. No automatic best-result selection, original-data modification, model promotion or live feedback.
- Retained optional local installation, private derivative handling, inert bundle review and acquisition/QC fixes. See the current build record for exact executed regression and real-model smoke coverage and its exclusions.

## Alpha 10.3.1 — Acquisition evidence and Atlas analysis reliability

- Fixed Atlas-to-Forge run-state discovery using typed FINALIZE path/hash evidence and UUID-bound historical filename support. Completed Atlas runs no longer fail merely because their state file is named `*_run_state.json`.
- Added Atlas boundary-marker recognition and event-clock parsing. Duplicate, conflicting, missing or mismatched identities remain explicit errors; planned times do not replace recorded boundaries.
- Separated advisory signal-quality findings from integrity/transport/required-input failures. Permitted warning continuation requires the operator's recorded acknowledgement, not automatic Bench Test Mode. Experimental hardware retains its non-participant restrictions.
- Retained new private raw preflight captures as separate, hash-referenced evidence. Historical acquisition warnings can accompany analysis without being mistaken for a fresh assessment of the full dataset; absent historical preflight does not itself block QC.
- Repaired publisher clock/rate handling and Vernier buffered-sample timing for future recordings. Approximate host/batch timing is labeled; physical synchronization is not claimed. Existing raw timestamps are preserved.
- Made EEG QC spectral estimates use independent contiguous pieces rather than windows spanning acquisition gaps. Added optional descriptive EEG–respiration association summaries inside existing EEG QC, with observed rates, recorded-clock limitations, coverage/edge exclusions and no causal/artifact claims or new prerequisite.
- Added a private aligned shape-only trace preview of analyzed one-second EEG/belt means, with gap/exclusion breaks, a file hash and explicit timing/interpretation limits. It is derived telemetry, not automatically shareable public content; optional plot failures remain nonblocking.
- Added a separately reviewed post-hoc Zuna recipe route for supported recorded evidence, with actual physical-map/reference confirmation, frozen input hashes, explicit timestamp policy, preparation-only checking and private resumable model checkpoints. It does not rewrite the original prospective contract or upgrade an original BENCH recording.
- Included the double-click `INSTALL_ZUNA.bat` as the sixth top-level release file. Default installation remains Core + Live Monitor + Hardware Connectors; Zuna is optional and isolated.
- Consolidated current instructions in the Alpha 10.3.1 installation/workflow guide, while preserving previous release history and upstream attribution. Exact executed test scope belongs to the build-validation record; no physical hardware validation or completed actual-data model-inference claim is implied by this entry.

## Alpha 10.3.0 — Optional local EEG reconstruction validation

- Added one explicit optional Zuna installation: `INSTALL.bat -Mode zuna`.
  Default full setup remains unchanged. A separate environment and locally
  verified model cache preserve pinned source/model identities; no EEG upload
  or automatic model download occurs during analysis.
- Added the ten-minute **AI-Assisted EEG Reconstruction and Signal Preservation**
  Atlas protocol: two minutes eyes-open calibration, then eight one-minute
  balanced eye-state blocks with audible cues and a frozen order.
- Added explicit operator review of the sixteen-channel physical wiring,
  microvolt units and external reference, plus a fingerprinted contract and
  incrementally saved actual block-boundary evidence. No ALS is required.
- Added **Zuna EEG Reconstruction — Experimental** to Analysis Forge. It compares
  four predetermined held-out measured electrodes with both Zuna and MNE
  spherical splines. Targets never enter input reference or normalization.
- Added automatic plain-language comparison reports, per-electrode errors,
  spectral/condition descriptions where supported, model/software provenance,
  generated-data masks and original-to-model timestamp/sample mapping.
- Preserved raw XDF and original QC cautions. Complete observed-block evidence
  supports the prospective scoring window; absent evidence is labeled exploratory
  or not estimable, not silently replaced with planned timestamps.
- Carried comparison reports into research bundles. Waveform derivative arrays
  require private full-telemetry opt-in; model weights/environments are not study
  bundle contents. Generated channels never become measured hardware evidence.
- Added installation/operator and method guides, protocol credits and explicit
  upstream notice/provenance limitations. Zuna's Apache metadata coexists with
  embedded Meta/Llama 2 notices; comprehensive upstream clearance is not claimed.
- Preserved the Alpha 10.2.3 hardware baseline, including both exact Cerelog
  firmware routes and their existing experimental restrictions. No new live-AI,
  thought-to-text, diagnostic, GPU-performance or physical-device claim is made.
- Validation evidence separates automated, synthetic, headless and actual
  model checks; consult the release build record for executed scope. Software
  success is not scientific validation or a guarantee of better reconstruction.

## Alpha 10.2.3 — Cerelog V1 five EMG / two EOG / ALS profile

- Added a separate exact-firmware Hardware Library route for all eight active
  inputs: EMG on CH1–4 and CH6, EOG on CH7–8, and divided ALS on CH5.
- Added four synchronized outlets: EMG5, EOG2, ALS1 and timing diagnostics.
  Channel metadata preserves physical input numbers, mixed gains and units;
  rail diagnostics cover all eight hardware channels.
- Extended managed launch, run/segment identity and exact-route preflight to
  the new profile. The older EMG4/ALS1 profile remains available and unchanged
  in its firmware contract; neither profile accepts the other's firmware.
- Preserved experimental, no-participant bench restrictions, battery checks,
  explicit network confirmation and stop-on-integrity-failure behavior.
- No physical device was opened or flashed during this application patch.
  Connected ALS verification and actual PRAYCG hardware recording remain pending.
  This patch does not modify Gamma Scalpel or validate cross-board alignment.

## Alpha 10.2.2 — Cerelog V1 differential EMG / ALS patch

- Added the exact custom-firmware Hardware Library route: four differential
  EMG channels at gain 24, one divided ALS channel at gain 1, 1,000 Hz.
- Added firmware/register verification, exact COM selection, battery/network
  confirmations, graceful stop, and immutable run/segment identity.
- EMG, ALS and timing diagnostics share device-derived timestamps without
  gap filling or invented precision. Cross-device alignment remains unverified.
- Extended exact preflight checks and Live Monitor channel labels/units.
- Preserved no-participant bench restrictions. No hardware was opened or
  reflashed during patch development; actual PRAYCG recording remains pending.

The current [README](README.md) contains installation and workflow instructions.
Historical entries below retain their original release scope.

## Alpha 10.2.1 — Hardware Library integration hotfix

- Connected the exact Crown OSC, Muse S Athena, Polar H10 ECG, GazePoint GP3/GP3 HD, Pupil Core, Neon, OpenMuse and OpenViBE routes to the main Hardware Library and hardware profile workflow. The library now distinguishes an implemented connector, an external publisher requirement, physical testing pending and withheld/catalog-only entries.
- Added explicit experimental profile selection and preserved the required no-participant bench confirmation. The profile records exact selected routes and external outlet reviews; its locked launch actions cannot silently substitute another product, publisher or restarted outlet.
- Connected managed-route actions to restricted device controls and external-route actions to publisher guidance and exact outlet attachment. Existing run identity, recording, replay and private/public exchange checks remain applicable; catalog visibility or a software pass does not grant participant approval.
- Updated the installation/workflow guide, current device-route notes and neutral research-program wording. Historical source records, author credits, third-party citations and license notices remain preserved.
- Added tests starting from the Hardware Library and continuing through profile creation, locked actions and recording evidence. Exact executed results are recorded in the release validation files. Physical devices, absolute sensor timing and independent second-machine execution remain unverified. Cerelog 16 remains withheld.

## Alpha 10.2.0 — Multimodal connectors and exact product routes

- Added a shared BrainFlow 5.23.0 connector with runtime descriptor validation, distinct preset buffers, modality-specific LSL outlets, source counters/timestamps, run identities, finite startup/shutdown and graceful stop. Crown uses its OSC route; Athena retains EEG, motion and raw optical streams without assuming ALS or interpreting optical data as validated fNIRS.
- Added an independent Polar H10 PMD ECG bridge with signed 24-bit decoding, 130 Hz microvolt samples, exact device timestamps, explicit arrival-clock mapping, packet-gap diagnostics and cleanup. Existing RR acquisition remains separate.
- Added an independently authored GazePoint TCP/XML bridge with explicit field order and product-specific GP3/GP3 HD settings. External route review records product, software, channel, calibration and timestamp provenance for Pupil Core, Neon, OpenMuse and OpenViBE.
- Added the Multimodal connectors panel, run-local launch evidence, graceful stop controls and an isolated Hardware Connectors installation component. Full installation includes the component; `INSTALL.bat -Mode hardware` repairs it separately.
- Reviewed the linked Cerelog, Crown recorder and OpenMuse repositories. The linked Crown program consumes existing LSL; OpenMuse remains an externally installed Athena option; Cerelog 16 stays withheld pending its exact transport/scaling/timing route. No OpenViBE driver source or unlicensed upstream publisher is bundled.
- Added packet, descriptor, lifecycle, failure-path, installer and integration checks. Physical hardware, absolute device timing and independent second-machine verification remain untested; exact executed evidence accompanies the release. Existing participant authorization, protocol, analysis and private/public bundle boundaries are preserved.

## Alpha 10.1.1 — LSL metadata and external recording reliability

- Fixed generic LSL discovery, the contract-bound observer and the Control Center stream list reading incomplete resolver descriptions as though they were full metadata. Shared retrieval now has finite deadlines, exact UID/source checks, temporary-inlet cleanup and separate unavailable, incomplete, malformed, restarted and ambiguous outcomes. UI discovery runs in the background.
- Added **Use existing LSL stream…** for additional observed attachments, with ordered channel/unit/rate review. Original vendor XML is preserved privately, without adding a false upstream PRAYCG run UUID or granting authority over the external publisher. Required reviewed hardware and participant-readiness checks remain separate.
- Session confirmation freezes a binding hash before the immutable runtime lock is created. Confirm, arm and direct runner launch recheck exact live identities. XDF preparation, replay and integrity QC independently reconcile the recording, selected outlet, metadata and segment with the same-run marker evidence. Checksums establish consistency, not signed authenticity or scientific validity.
- Preserved external provenance through analysis and private full-telemetry export. Public/privacy-restricted exports exclude identifying stream metadata rather than silently adding hostnames, device identities or raw XML through recursive report folders.
- Added hardware-free success and adverse-case regressions and actual synthetic XDF decoding. Original recordings, raw sample values, raw timestamps and previous-release files are not rewritten. See current validation records for executed coverage and exclusions.
- Retained legacy OpenBCI/ALS, Polar and Vernier acquisition routes and owner protections. No new device drivers, OpenViBE code/dependency, physical-hardware verification, fresh online dependency installation or independent second-machine acceptance is claimed.

## Alpha 10.1.0 — Data-only protocol installation and AI round trip

- Added one strict, bounded protocol extension contract for supported existing task components, explicit assets, semantic hardware roles, consumed duration/repetition controls, sources, limitations and existing-analysis bindings. No imported executable code, arbitrary expressions, dependency installation or new algorithms.
- Added My Protocols with local template editing, independent structural checks and bounded fake-I/O runner rehearsal, explicit human acceptance, immutable local installation, version activation and rollback. Installation does not start a participant session or grant ARM authority.
- Connected verified user protocols to Atlas discovery, material preparation, protocol-specific pre-start configuration, runtime locks and the trusted packaged engine without hand-editing packaged catalogs. Selected historical locks retain their exact version; damaged entries are visibly quarantined without disabling other verified protocols.
- Extended AI design packs with the exact installable format/capabilities. Returned definitions are checked against the original complete document ledger and parent revision; the review shows requested/returned design fields. Repair requests preserve linkage and never upload automatically. Wider legacy candidates remain review-only.
- Preserved exact user-protocol definition, compiled manifest, receipt and rehearsal evidence with the acquisition for analysis/private-context bundling. Imported originals remain inert; bundle import does not install or activate protocols.
- Added regression, security, hidden-interface and previously unseen protocol-path acceptance checks. Clean/contaminated/short/gap cases retain their correct cautions and non-estimable outcomes. Read the current validation evidence for executed counts and limits.
- Retained acquisition ownership, participant/bench distinctions, existing EEG recipes, reports, hardware contracts and historical studies. No new physical-hardware certification, cloud-AI execution, fresh online dependency installation or independent second-machine validation is claimed.

## Alpha 10.0.4 — Authorship, AI handoff clarity and recipe preservation

- Added structured author/source metadata to all 67 protocol definitions, with Hoyt Banks credited separately for PRAYCG development/adaptation. Sixteen verified references cover all 23 externally sourced protocols; dataset authors, paper authors, preprints and retained local research lineages remain distinct. Historical source hashes, protocol IDs and old study records are preserved.
- Added readable protocol credits in the selection preview, complete citation registries, generation-preservation hooks and an upstream software attribution review. Clarified that the MIT grant covers original PRAYCG-owned code, not third-party artifacts. Citations do not replace license obligations or establish endorsement/scientific validity.
- Made the AI protocol return endpoint explicit: review and immutable candidate staging, not automatic runner installation. Handoff materials describe exact supported return contracts and implementation limitations. Arbitrary returned code remains unexecuted.
- Added a bounded AI-assisted recipe handoff for existing EEG analysis settings. Returns are tied to the parent recipe, reviewed as data and require normal human validation/locking; they do not register new executable analysis modules.
- Fixed recipe revision dropping unexposed settings, including event-condition subsets and RSA model matrices. Incompatible condition changes must be resolved explicitly, not silently reinterpreted.
- Fixed the shared runner for 14 behavioral protocols requiring a CLI manifest while Control Center supplied the manifest through its environment. The wrapper now accepts that handoff; packaged-path, runtime-lock and acquisition-lease checks remain intact.
- Retained one current install/workflow guide and changelog, clean ZIP layout, isolated monitor environment and previous session protections. New runtime extension admission remains a separate milestone. No physical-hardware, cloud-AI, fresh dependency-install or second-machine validation is implied.

## Alpha 10.0.3 — Stimulus loading, profile-driven checks and validation foundations

- Fixed three workflow catalog identity checks that incorrectly treated the installation folder name (`app`) as the release identity. Explicit build metadata now governs consistency; malformed or mismatched identity remains blocked.
- Added fresh-process acceptance of actual protocol locks, compatible stimulus choices and preparation routes from the extracted ZIP. A blocked workflow is a test failure even if the application starts without an exception.
- Detailed equipment checks use the selected reviewed hardware profile for EEG identity, channel count, sample rate and voltage units. Both launch paths share those requirements; legacy OpenBCI defaults no longer govern other profiles. New native watchdog settings follow the selected EEG stream and rate without changing historical locks.
- Removed the unconditional ALS requirement from optional preflight. Profiles without ALS do not capture it, start an OpenBCI ALS bridge or run placement barcodes. Missing optical timing is explicit; actual required ALS is not waived. No-EEG profiles retain full-profile checks without invented EEG.
- Restricted automatic native PRAYCG16 map emission to matching carried OpenBCI16 routes. Other headsets do not inherit fictitious electrode maps; location-dependent analyses still require independently verified metadata.
- Corrected protocol certification's catalog-position-as-session-number error. Explicit visit, sequence, condition, marker and substantive-task checks replace empty-timeline success; dry-run coverage remains separate from physical execution.
- Added seeded offline XDF fixtures for OpenBCI-shaped EEG+ALS, Crown-shaped EEG without ALS, and Cerelog16 streaming-shaped EEG without an assumed ALS interface. Vernier-shaped respiration and Polar-shaped RR streams are test inputs. Athena remains NOT_TESTED while its exact stream contract is unresolved. No simulated result promotes real hardware support.
- Added clean, 60 Hz, flat-channel, gap and short-recording cases through the actual EEG quality/preprocessing/spectral workers. Known synthetic expectations—not process exit alone—determine test success. Optional private QA bundles are verified, imported and numerically rerun in a fresh folder; they are not public example studies or full Forge-plan replay.
- Synthetic gap testing exposed unsafe filtering across missing time. The continuous derivative now returns an actionable NOT_ESTIMABLE result rather than joining disconnected samples. Raw QC remains available; contiguous contaminated data still runs with cautions.
- Preserved prior releases, recordings, immutable session history, clean installation layout, one current workflow guide, and the existing synthetic/non-participant boundary. No physical-device, actual display/audio timing, online dependency installation or second-machine validation is claimed.

Consult the shipped validation evidence for executed coverage. Exhaustive real protocol-runner × hardware × analysis execution and privacy-reviewed per-protocol public bundles are not claimed by this hotfix.

## Alpha 10.0.2 — Completed-session and reused-process hotfix

- Corrected the 10.0.1 protocol-change guard, which could mistake saved ACQUIRE status for a live run even when the exact archived run was already finalized.
- Protocol selection, clearing and pre-start configuration share an evidence-based assessment. Only verified inactive terminal runs can refresh cached status. Historical locks, exit records, recordings and analysis results are not rewritten; ARM is never restored by reconciliation.
- Added a bounded Windows process-identity fallback for protected/reused process numbers. A sufficiently different verified creation time can establish that a current process is not the historical runner. Matching, malformed, unavailable or insufficiently precise identity evidence cannot release authority.
- Genuine ACQUIRE-stage interruptions retain explicit cancellation/interrupted-run recovery. No process is killed and no gate is bypassed solely because a process name changed or a heartbeat is old.
- Retained the clean release layout, shared Core/Live Monitor installer, neutral protocol aliases and protocol-dependent settings from 10.0.1.

See the included validation reports for executed checks. Physical hardware, a fresh online dependency installation and independent second-machine verification are not established by these software checks.

## Alpha 10.0.1 — Protocol-aware setup and cleaner installation

- Protocol-dependent pre-start configuration replaces the shared universal timing form. Displayed editable settings correspond to supported runner inputs; fixed designs remain read-only. Restore Protocol Defaults replaces the universal 120-second reset.
- Native PRAYCG3/4/SMG support their governed custom timings and explicitly defined short-demonstration preset. Atlas duration controls are limited to the schedules that actually consume them. Session numbers follow supported Atlas contracts. Demonstration and Bench Test Mode are separate decisions.
- Configuration drafts are isolated by protocol/version and hardware identity. Confirmation binds the configuration; later edits require reconfirmation, and active acquisition cannot be silently reconfigured. A permitted pre-run custom variant is not automatically post hoc or preregistered.
- Seventeen public protocol titles now describe tasks or measurements. Stable IDs, former-name search aliases and historical recordings/locks preserve provenance. Renaming supplies no new scientific validation.
- One top-level installer installs Core and the isolated Live Monitor by default, using a shared native Python 3.11 discovery path. Minimal/Core-only, monitor repair and check-only modes are available. Component failures remain explicit; no nested installer pauses.
- Environment records identify the current release and Core/monitor component instead of stale release labels. Existing dependency constraints are retained.
- The public ZIP has five top-level files and one app folder. One current README and changelog replace competing public installation guides. Runtime/module/scientific/license references and labeled validation evidence remain internal; no previous source release is deleted.

### Public title changes

| Previous title | Public title |
|---|---|
| Fractal Existence | Multiscale Physiology and Behavior |
| Thermodynamic Weight of Thought | Cognitive Load and Physiological Response |
| Unified Presence Availability | Multimodal State and Recovery |
| Gratitude–Neurochemical Tensor | Gratitude, Rumination and Physiological Response |
| Gratitude Cardio-Affective Tensor Lite | Gratitude and Paced Breathing |
| Biological Anchor Integration | Caregiver–Child Interaction and Recovery |
| Father's Day Presence | Caregiver–Child Play and Engagement |
| Conformity–Flow Boundary Layer | Social Feedback and Task Engagement |
| Zero-State Baseline Calibration | Individual Resting-State Calibration |
| First-Person Presence and Physiology | Subjective Experience and Physiology |
| Personalized Safe Transition and Recovery | Individual Task-Load and Recovery Calibration |
| Rhythmic Autonomic Stabilization | Rhythmic Cues and Autonomic Response |
| API-A Autonomic Availability, Mobilization and Recovery | Autonomic Response and Recovery Calibration |
| PR-AYC-T Trust Offloading | Partner Support and Cognitive Task Performance |
| PR-AYC-D Neutral Belief Update and Dissonance | Evidence Updating and Confidence |
| PR-AYC-G Mature Meaning Gradient | Narrative Structure and Interpretation |
| PR-AYC-G Dyadic Narrative Hyperscanning | Shared Narrative Viewing and Interpersonal Physiological Synchrony |

## Alpha 10.0.0 — Reproducible Research Exchange foundation

- Research Bundle 1.0 unifies private replay, AI-review and results-review exports with dataset identity, file ledger and environment/provenance descriptors.
- Explicit privacy tiers and raw/private switches; publication-candidate review records are not automatic permission to publish.
- Safe verified import preserves original bytes and separates new work. Imported code remains inert.
- Current-installed-build reanalysis freezes source-plan selection, input bindings and comparison tolerances; required QC/dependencies run first. Original and derived authority remain distinct.
- Supported numeric-output comparisons report coverage, missingness and limitations; selected agreement is not full scientific equivalence.
- Local DATA catalog supports registration, re-verification, inert report review and reanalysis/replication lineage. No upload or automatic dependency installation.
- Acceptance evidence included same-machine PRAYCG3 reanalysis. It did not establish second-machine or physical-hardware validation.

## Alpha 9.10.2 — Session-safe planning and multi-stream replay

- Prevented stale analysis envelopes from being reattached to another session; preserved historical plans, receipts and recovery backups.
- Added replay Play/Pause, Stop-and-rewind, ten-second jumps, seek, speed and elapsed/total time.
- Displayed supported recorded EEG, auxiliary, ALS, RR, respiration and marker streams together on a common timeline, with saved hardware-profile matching and explicit mismatch/missing-data warnings.

## Alpha 9.10.1 — Restored methods, reporting and private study packages

- Restored explicit input inventory/overrides, EEG recipe review/revision and earlier bundling capabilities.
- Added actual scientific report access, automatic offline plain-English summaries, a readable master index and Full Chain child report links.
- Added private full-study and AI-ready packaging with explicit purpose, source inventory, available raw/supporting records and optional theory/porting background.
- Added staged AI return review and continuing AI-assisted protocol draft/context workflows; external code stays untrusted.

## Alpha 9.10.0 — Consolidated Analysis Forge and protocol expansion

- Consolidated QC, plan building/execution and persistent per-module results into a guided Analysis Forge workflow.
- Required QC saves dataset-bound evidence before module selection; automatic dependency handling remains separate from scientific estimability.
- Added fourteen exploratory behavioral adaptations and seven managed legacy analysis adapters.
- Added optional passive Live Monitor, synthetic inspection and XDF replay. Closed-loop MNE-RT feedback was not enabled.

## Earlier foundations — summary, not a reconstructed per-patch ledger

The v0.95a and Alpha 8–9 lineage established native PRAYCG acquisition/analysis, Atlas protocol adapters, session locks and runner ownership, bridge recovery, bench-only testing, readiness evidence, Hardware Forge contracts, analysis eligibility/plans/receipts, persistent result history, scientific-module integration and local bundling. The 9.9 line iteratively repaired plan/dependency/workflow and report issues. This summary does not invent missing build-by-build evidence or claim every historical problem was solved merely by incrementing a version.

## Validation boundaries

Read the current reports under app/deployment/validation for actual executed checks. Public distribution hashes describe the shipped files; source-build evidence refers to the tested development source. Hardware, participant safeguards, scientific validity, privacy clearance and second-machine reproduction require their own evidence. A protocol alias, passing software test or complete dependency node cannot supply it.
