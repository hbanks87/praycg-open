# PRAYCG Control Center Alpha 10.0.4 — Analysis Module Guide

This guide describes the **23 entries in the active Analysis Forge orchestration registry** shipped with Alpha 10.0.4. It explains what the software computes, what evidence it needs, and what its results do not establish. Component numbers such as v0.1 and v1.6.0 identify preserved method contracts; they do not mean that you opened the wrong Control Center release.

## Read the result on two levels

**Software execution** answers whether a tool ran and wrote its expected artifacts. **Scientific estimability** answers whether the recording supports a particular calculation. A completed Master Suite or chain can contain unavailable endpoints. A report full of missing values is not automatically a crash, and a successful process is not automatically a successful experiment.

- `COMPLETE` means the relevant execution/output contract was met. Read the individual endpoint gates and coverage next.
- `CAUTION` means usable evidence carries limitations. It does not mean “clean EEG.”
- `INELIGIBLE`, `NOT_ESTIMABLE`, `NOT_GRADABLE`, or a documented unavailable result means a prerequisite, measurement, contrast, or estimator requirement was not satisfied. Names differ across preserved components.
- `FAILED` or `SOFTWARE_ERROR`, especially with an exception traceback, means a software or infrastructure problem. Keep the module report and process log.

Do not replace missing measurements with zeros. Zero can be a real result; missing means the result was not available. Repeatedly retrying the same scientific non-estimability does not create missing evidence.

The default route is: select the correct run, save/stop recording, run required QC, then add individual modules to the locked plan. Prerequisites are included automatically. The current Forge creates a revision when you choose **Add to locked plan**; there is no separate obligatory lock button in that consolidated workflow. Adding modules after inspecting results remains post-hoc/exploratory even when the new revision is immutable.

The active registry is `config/analysis_orchestration_registry_v0_1.json`. The older `analysis_module_registry_v0_1.json` is a ten-entry discovery/preflight catalog with legacy launch labels. It is not the authoritative count of current managed analyses. All 23 active entries use managed command-line execution; that includes reporting, visualization, and readiness tools, not 23 independent biological estimators.

## 1. Run Integrity and Event-Timing QC

ID: `run_integrity_timing_qc_v0_1`

**Question:** Do the selected files and recorded timing evidence describe one coherent run?

This required gateway inspects the XDF inventory, event records, run identity, composite/run-state manifests, and runtime session lock. It checks matters such as missing or ambiguous files and backwards timestamps. JSON and CSV representations of one event log can form one logical event set; two unrelated recordings must not be silently combined.

The output is `run_integrity_timing_qc_v0_1.json`, including findings and input evidence. It applies across protocols; no EEG recipe is needed. Its result is an integrity diagnostic, not proof of accurate stimulus onset, acceptable electrodes, correct consent, or physiological validity. Marker ordering alone cannot establish photodiode-verified display timing. Fix wrong-file selections before downstream analysis; preserve genuine incomplete-run evidence rather than editing a run into apparent completeness.

## 2. Universal EEG Signal Quality and Line-Noise Audit

ID: `eeg_signal_quality_v0_1`

**Question:** What quality problems are visible in the preserved raw EEG?

After integrity QC, this tool uses the selected XDF and governed analysis window. It examines channel variability, flatness, finite samples, timing gaps, and spectral evidence around 50 and 60 Hz. The registered capability floor is one channel and ten seconds; each measurement still needs an adequate sampling rate. An unmeasurable frequency is unavailable, not absent.

Outputs include a JSON quality report and per-channel CSV. No event recipe is required. A strong 60 Hz component is a reason to label the recording contaminated, not automatically a reason to prohibit every descriptive analysis. Conversely, low line noise does not prove neural origin: muscle, eye movement, motion, clipping, and reference problems remain possible. Downstream reports retain upstream cautions; they do not erase them after filtering.

## 3. Governed EEG Preprocessing Derivative

ID: `eeg_preprocessing_derivative_v0_1`

**Question:** Can we create a reproducible, explicitly documented EEG working copy?

This depends on signal-quality QC and the selected XDF/window. The shipped configuration uses a zero-phase 1–45 Hz filter, no notch by default, flat-channel exclusion without interpolation, and common-average referencing over retained channels. At least two retained channels are needed. Nonfinite data, unsuitable timestamps, insufficient signal, or invalid filter requirements can prevent a derivative.

Outputs are the `eeg_preprocessed_derivative_v0_1.npz` array and its provenance manifest. Raw recording files remain separate. Filtering may use declared supporting samples outside the experiment interval, but inference samples are cropped to the governed interval.

This is one declared processing choice, not automatic expert cleaning or a guarantee that artifacts disappeared. It is also not the preprocessing branch used by every legacy tool: the Master Suite, Micro Handoff, and some protocol-specific analyses own their methods. Compare processing histories before comparing their numbers.

## 4. EEG Spectral and Aperiodic Screening

ID: `eeg_spectral_aperiodic_v0_1`

**Question:** How is recorded EEG power distributed across frequencies?

This reads a hash-validated governed derivative. The frozen configuration needs five complete four-second epochs. It computes Welch power spectra and delta, theta, alpha, beta, and low-gamma summaries across 1–45 Hz; it also searches for an alpha peak and fits a robust log–log spectral screening slope using declared exclusions.

Outputs include a JSON report, spectral-feature table, and PSD table. No event recipe is required. The slope uses a Theil–Sen screening procedure; it is **not** a specparam/FOOOF decomposition. A missing peak is not proof that a physiological rhythm is absent. Short data, unresolved peaks, unsuitable spectra, or inadequate epochs leave individual results unavailable. Band power is descriptive and processing-dependent; it is not a diagnosis, mental-state reading, or demonstrated excitation/inhibition mechanism.

## 5. Master Comprehensive Suite

ID: `master_comprehensive_suite_v1_6_0`

**Question:** What does the native PRAYCG recording show across its declared phases and measurement families?

The managed route supports PRAYCG3, PRAYCG4, and SMG. It depends on integrity QC, XDF, event evidence, analysis-window manifest, and the bound analysis-input manifest. Baseline evidence and correct phase identities matter. It uses module-owned preprocessing rather than automatically consuming the generic derivative. A recorded channel map is especially important for anatomical/topographic interpretations; sixteen anonymous columns do not verify sixteen scalp locations.

The central output is `tables/praycg_analysis_frame_v1_6_0.csv`, accompanied by segments, features, reports, provenance, and `run_eligibility.json`. This frame supplies several later modules. Managed completion requires a nonempty canonical frame; it does not guarantee every feature or endpoint is estimable.

### What is inside the Master Suite?

Core analyses include spectral/condition summaries, artifact-aware contrasts, gamma-related screening, theta persistence/carryover, frequency-sequence descriptions, and optional autonomic summaries. Names such as “MeaningGamma,” “TaskGamma,” and “TemporalSemanticProxy” identify operational feature combinations, not sensors that directly measure meaning or thought.

**Gamma-to-theta handoff and K_HT:** the suite evaluates lagged feature relationships, including event-local comparisons. These are associations between derived signals, not cellular memory measurements or a proof of a mechanism. Physiology-selected peaks remain exploratory when evaluated in the same data.

**MRED:** Meaning Recognition/Encoding Dissociation compares operational recognition-related and delayed-integration-related features around anchors. Optional familiarity, novelty, annotations, and scene maps add context. High/low quadrant labels are classifications of these proxies. Missing theta carryover does not demonstrate that no memory formed.

Some older method notes describe a recommended “primary” path. Registry inclusion or a historical label cannot make a dirty, shortened, retrospective demonstration confirmatory. Read the actual run disposition and anchor/QC gates.

## 6. Full Dependency-Aware Chained Analysis

ID: `full_chained_analysis_v1_6_1`

**Question:** Which downstream PRAYCG analyses can be computed from the canonical results and recorded supporting files?

For PRAYCG3/4/SMG, this follows the Master Suite. It stages the canonical frame and bound context, runs constituent tools, and writes `chain_manifest.json`, individual module folders, tables, and interpretation artifacts. Inspect the manifest's per-tool statuses: the overall chain may complete while particular calculations are inapplicable or missing. A software error in a constituent is different from an explicitly gated endpoint.

### NIP, BIT, CII, IAQ, CET-R, and EET

These are nested outputs of the `nip_cet_eet` chain component, not six additional Forge entries.

**NIP**, Narrative Immersion Proxy, combines available attention/recognition-related features with delayed theta/integration-related features, with artifact and visual-drive penalties. The product is an operational proxy, not measured immersion. Reuse of inputs means agreement with other composites is not independent confirmation.

**BIT**, Bivariate Immersion Threshold, is a conjunction of gates, including recognition/integration, local coupling, and artifact conditions. The stricter variant also requires event-lock/Target conditions. It is not an average that can compensate for a missing gate.

**CII** averages NIP density within an annotation/anchor window, so duration alone does not automatically increase it. **IAQ** compares Target with Contextual Override; its ratio needs suitable nonzero Target support. Both need matching recorded conditions and usable windows.

**CET**, Cinematic Entrainment Tracking, examines associations with cue timing and supplied stimulus features. **CET-R** fits an available-regressor residualization of NIP and reports residualized summaries. Its fitted R² is an in-sample description, not held-out prediction or proof that stimulus confounding has been eliminated. Missing stimulus measurements cannot be declared controlled.

**EET**, Endogenous Echo Tracking, compares feature patterns with later washout or Baseline 2 patterns. “Echo” means operational similarity, not replayed memories or a measured endogenous mechanism. Missing after-state periods prevent the relevant comparison; fixed order and cumulative carryover remain alternative explanations.

### Other nested chain components

**A-MRED** evaluates recognition-plus-integration contrasts at predeclared anchors with timing, QC, and comparison-condition gates. A strict prospective claim requires a genuinely pre-acquisition locked anchor. An anchor created while examining this run cannot acquire prospective status later.

**TTI** is a weighted reception-versus-extraction feature contrast, including artifact/visual penalties. Its historical “thermodynamic” name does not mean the software measured heat, metabolism, or an actual conservation law.

**MRED-ITP/ACG/OCU** examine algorithmic-complexity change and ocular-release patterns around supplied events. Raw EEG complexity differs from a feature-level fallback. An Fp1 blink proxy is not confirmed EOG/eye tracking. The chain requires XDF, events, annotations, and MRED event evidence for this route.

**NUPI** summarizes load-versus-recovery proxy profiles and needs CII plus adequate after-state evidence; absent Baseline 2 can leave polarity unresolved. **MRED-Peak/Resolution** separates anchor types and gate status. **DGA** summarizes self-reported access, availability, task burden, and confounds, optionally alongside feature evidence. None validates a literal neural decoder or replaces the separate acquisition protocol bearing a related name.

The chain also invokes ShotOrder HOC-R, cue/confound tools, expanded confounds, an ALS barcode audit, and offline interpretation. An ALS audit needs actual recorded sensor/timing evidence; an ALS hardware selection alone is insufficient.

## 7. HOC-R ShotOrder Structural-Control Audit

ID: `hocr_shotorder_v1_6_0`

**Question:** Does the PRAYCG4 ShotOrder control help distinguish a Target effect from preserved visual structure?

This standalone registry entry follows the Master Suite and accepts PRAYCG4, where ShotOrder and Target conditions are expected. It reads the canonical frame and bound analysis context and produces the ShotOrder interpretation and contrast tables. Missing either condition prevents the contrast. A PRAYCG3 recording without ShotOrder should not be relabeled to make this entry appear applicable.

Do not confuse this with the HOC-R **regressor-inventory** component inside Confound Expansion. They share a family name but have different input and result contracts. A structural-control contrast does not prove meaning, consciousness, or mechanism; it addresses a specific alternative explanation, with residual artifact and design limitations still present.

## 8. Confound-Expanded Analysis

ID: `confound_expansion_v1_5_7`

**Question:** Which recorded circumstances weaken particular interpretations?

For PRAYCG3/4/SMG, this follows the Master Suite and uses its canonical frame, supplied stimulus-fingerprint material, and bound run/self-report evidence. It writes separate interpretation JSONs, CSVs, and a report. Successful reporting can include ungradable components.

Its nested **HOC-R** reports higher-order stimulus-regressor availability. In this release it does **not** fit a residualization or report training R² without a validated condition/time/window alignment contract. **OSA** describes cue-monitoring/spatial-attention burden; without eye tracking it is not a measured gaze trajectory. **OHC** flags order, habituation, and carryover: a washout is not an established biological reset. **AAM** compares afterglow-like with task-relief-like evidence while treating Baseline 2 as cumulative. **RespDualPath** keeps respiratory state events separate from respiratory artifact concerns.

The chain's separate RSM/CVB/Squint component reconstructs arithmetic cue load and reports visibility, audiovisual, acoustic, and ocular-strain context. RSM “microstate” is not EEG topographic microstate clustering. No confound report proves that all alternative explanations were removed.

## 9. CAI / SID Exploratory

ID: `cai_sid_exploratory_v0_2`

**Question:** Is there sufficient valid feature evidence to summarize the frozen CAI proxy and its time-weighted persistence?

This managed module supports PRAYCG3/4 after the Master Suite, using XDF, events, and the canonical/time-resolved feature frame. CAI combines bounded fast/slow support and their positive coordination, penalized by artifact/task features. Hard-QC failures remain missing. Its zero-to-one range is not a probability or validated consciousness scale.

**NAST versus NAS:** NAST is the Narrative Absorption State Transition method; NAS is its resulting score. Neither is a separate active Forge entry. If the selected source has no usable NAS, the managed adapter may derive it with packaged NAST when required source families have at least 70% finite coverage. It does not blend partly observed NAS with invented replacements. This reuses CAI-related EEG features and is not independent validation or direct DMN measurement.

**SID** is the valid-time weighted mean: `sum(CAI × valid duration) / sum(valid duration)`. The module also reports integrated CAI load and threshold occupancy. It avoids counting overlapping support twice or filling long gaps. Branches require the configured 70% valid-time coverage; relevant PRAYCG3 contrasts need both contributing branches estimable. The 8–30-second future-integration window makes shortened branches particularly limiting.

Read `cai_sid_v0_2_managed_result.json` and valid-time summary/contrast tables. Exit code 2 means governed `NOT_ESTIMABLE`, not a crash. The valid-time layer does not invent bootstrap intervals; frozen-core uncertainty is a separate legacy output.

## 10. Continuous Autonomic / RespDualPath

ID: `continuous_autonomic_respdualpath_v1_0`

**Question:** What do recorded cardiac beat intervals and respiration show over time?

This cross-protocol route follows integrity QC and uses XDF plus the analysis-window manifest. The tool also has direct CSV input routes. Actual cardiac and respiration streams must be present; checking Polar or Vernier in the hardware profile does not supply missing data.

It builds 4 Hz cardiac/respiration arrays and 1 Hz summaries, preserving quality and interpolation flags. Outputs include beat tables, HR/HRV measures, respiratory events, separate physiological/artifact paths, and coupling time-shift nulls. HR interpolation is not converted into manufactured beat observations. The frozen configuration uses 30-second RMSSD and 60-second SDNN windows with minimum valid beat support.

Short runs, long gaps, invalid intervals, or absent sensors leave measurements unavailable. These autonomic associations are nonspecific; they do not establish cortical origin, narrative reception, autonomic diagnosis, or a causal direction. Centered windows are retrospective, not instant live estimates.

## 11. Micro Handoff

ID: `micro_handoff_v0_1`

**Question:** Is a declared temporal-gamma increase followed by a theta-proxy increase across a fixed short-lag bank?

This separate exploratory module supports PRAYCG3/4/SMG after the Master Suite supplies a canonical segment table; it analyzes raw XDF rather than the generic derivative. The frozen implementation assumes the PRAYCG16 channel ordering/sentinels, at least 16 channels, a minimum 125 Hz rate, and at least 30 seconds of valid Baseline 1. There is no full-run baseline fallback. Verify channel meaning before interpreting its spatial labels.

Gamma and theta use trailing 250 and 500 ms windows. The 25 ms output cadence is **not** 25 ms spectral resolution or an independent observation count. The 100–1000 ms lag-bank summary distinguishes positive changes from stationary high-high agreement.

Outputs include readiness, feature/lag series, branch summaries, contrasts, null tests, QC, and provenance. Insufficient baseline, gaps, poor coverage, or fewer than two analyzable branches block inference. This is not CAI/SID, EEG microstate clustering, or evidence of discrete conscious frames.

## 12. Cue-Locked Gamma Forensics

ID: `cue_locked_gamma_forensics_v0_1`

**Question:** Are cue-related high-frequency patterns compatible with artifact, timing, spatial, or autonomic explanations?

For PRAYCG3/4 with cue evidence, this follows integrity QC and uses the bound data-audit inventory and analysis-input manifest. Its managed adapter invokes the packaged forensic analysis and requires recorded analyzed runs, not merely a nonempty output folder.

Outputs include analysis provenance and cue-locked summaries of spectrum, timing, topographic context, and available autonomic context. Missing cues, channels, frequency support, or measurements remain unavailable. Correct channel metadata is necessary for anatomical interpretations.

This can be useful on a dirty demonstration precisely because it investigates competing explanations. It does not issue a definitive “brain versus muscle” verdict, reconstruct missing auxiliary channels, or repair the primary conclusion. A line-frequency peak or facial-muscle-compatible pattern requires cautious reporting even if some cue contrasts are computable.

## 13. MasterSync Visualizer

ID: `master_sync_visualizer_v1_4_0`

**Question:** Can we inspect the canonical results across the full run?

For PRAYCG3/4/SMG, the managed route follows the Master Suite and reads its canonical frame and bound context. In Alpha 10.0.4 this route produces **static HTML/PNG displays**, feature diagnostics, and a display report. It is not the older interactive/video renderer, nor the separate Live Monitor XDF replay.

The managed display preserves source values without resampling or interpolation. It does not guess missing cardiac/ALS columns from partial names or infer event overlays without clock-bound evidence. A `z` or score axis is not raw physiological units.

Blank or missing series should be checked against the feature-diagnostics table. A rendered image is an audit aid, not an independent analysis, proof that every calculation succeeded, or confirmation that a historical eligibility label is the current QC decision.

## 14. Offline Master Interpreter

ID: `offline_master_interpreter_v1_6_0`

**Question:** What do the recorded analysis artifacts say in readable language?

This PRAYCG3/4/SMG reporting entry depends on the chained analysis and its manifest, plus bound analysis context. It produces human-readable reports and supporting interpretation records. It summarizes available evidence, unavailable paths, software failures, and eligibility boundaries; it does not compute missing physiology from prose.

The Forge also maintains per-module result summaries and links to native artifacts. Those convenient summaries do not mean this separate master interpretation entry ran, and they are not external-AI consultations. When a summary is terse, open the specific module's tables, interpretation JSON, and native report.

The interpreter is a reporting layer, not an independent replication or endorsement. Repeatedly describing several composites derived from the same features does not create several independent lines of evidence. Its conclusions must remain subordinate to source measurements and their recorded gates.

## 15. Atlas Meditation versus Active Thinking

ID: `atlas_meditation_vs_thinking_v0_1`

**Question:** How do EEG spectral descriptions differ between the recorded meditation and thinking blocks?

This entry is specific to `ATLAS_MEDITATION_VS_ACTIVE_THINKING_ADAPTATION`; it is not a generic PRAYCG3 analysis. After integrity QC it needs XDF EEG, the exact event set, the four declared block-onset markers, and adequate sampling/coverage. The registry specifies a 125 Hz minimum with a caution policy.

It uses two-second nonoverlapping protocol-bound epochs, timestamp/flat-channel/robust peak-to-peak gates, and Welch spectra with frozen bands. Outputs are the analysis JSON, block spectral-feature CSV, and condition-contrast CSV.

Incomplete blocks or rejected epochs remain unavailable. A within-run contrast is descriptive: it does not show a population meditation effect, establish what the participant was thinking, validate an adapted protocol, or diagnose an attention state. Fixed order, fatigue, movement, and other uncontrolled differences remain relevant.

## 16. Event-Related Potential and Time-Frequency

ID: `eeg_erp_time_frequency_v0_1`

**Question:** What EEG pattern recurs at the exact events selected in a frozen recipe?

This cross-protocol method needs the governed derivative, event set, and a hash-locked recipe declaring condition markers, epoch limits, baseline and frequencies, plus optional channel-specific ERP peak windows. It requires at least ten retained trials per condition. It performs event-locked averaging and Morlet time-frequency estimation with the declared settings, producing a report, waveform tables, and time-frequency data.

“All protocols” means eligibility is evidence-driven, not that every protocol supplies repeated suitable events. A single onset for each PRAYCG3 video does not create ten independent stimulus trials. A cue series may support a carefully declared cue analysis, but not an invented scene-onset experiment.

Invalid/missing baselines or insufficient retained epochs can make the analysis unavailable; omitted optional peak windows simply produce no corresponding peak estimates. A waveform peak is not automatically an N400/P300 or evidence for a particular cognitive process. Post-hoc recipes remain explicitly exploratory.

## 17. Sensor Connectivity and Phase-Amplitude Coupling

ID: `eeg_connectivity_pac_v0_1`

**Question:** How do recorded channel signals covary in frequency and phase?

This uses the governed derivative without an event recipe. The frozen configuration requires at least two channels and ten four-second epochs. It estimates coherence, imaginary coherence, PLI, and wPLI in declared bands; theta-phase/low-gamma-amplitude coupling uses Tort's modulation-index approach, deterministic circular-shift surrogates, and Benjamini–Hochberg correction.

Outputs are a JSON report, connectivity matrices, and PAC tables. Undefined denominators, inadequate epochs, or unmeasurable bands stay unavailable. Matrix entries are sensor associations. Shared reference, common sources, filtering, waveform shape, and artifact can influence them.

A significant surrogate comparison does not prove anatomical communication, information transfer, causality, or independence from every artifact. Contaminated PRAYCG3 can support an explicitly exploratory calculation if sufficient derivative data survive, but the quality warning remains part of the result.

## 18. EEG Complexity and Entropy

ID: `eeg_complexity_v0_1`

**Question:** How regular or varied is the signal under several explicitly defined algorithms?

This cross-protocol entry consumes the governed derivative and requires five complete eight-second epochs. It computes normalized LZ76 complexity, permutation entropy, spectral entropy, and multiscale sample entropy using frozen choices and bounded sample counts. Outputs are a report and per-channel/epoch-derived summary table.

No event recipe is required. Non-estimable entropy values remain null with available-epoch counts; they are not silently made zero. Flat signals, insufficient pattern matches, preprocessing, sample length, and noise can materially change these descriptors.

More complexity is not automatically better brain function. In particular, contamination can add apparent irregularity. These algorithms do not measure consciousness, health, literal thermodynamic entropy, or the truth of a psychological theory. Compare like-for-like preprocessing and record the analysis choices before interpreting differences.

## 19. EEG Run-Local Microstates

ID: `eeg_microstates_v0_1`

**Question:** Can this run's scalp voltage patterns be summarized by four recurring map shapes?

This uses the governed derivative, at least four retained channels, and at least sixty seconds. It selects global-field-power peaks, performs deterministic polarity-invariant clustering with a fixed four-state solution, and labels states by run-local coverage. Outputs include the report, maps, and state sequence with descriptive summaries.

No event recipe or registered channel-position file is required for the numerical clustering. That does not supply missing anatomical information. Insufficient peaks, degenerate maps, or too little usable data make the method unavailable.

Its `MS1`–`MS4` labels are not automatically the canonical A–D microstates from another study. They are not diagnoses, anesthesia states, or decoded thoughts. This is distinct from Micro Handoff and from the running-sum “microstate” model inside confound analysis. Cross-run map matching requires additional justified work.

## 20. Motor-Imagery CSP/LDA Decoding

ID: `eeg_motor_imagery_v0_1`

**Question:** Can the declared two classes be distinguished within this run?

The module needs the governed derivative, exact labeled events, and a locked two-class recipe with at least twenty complete trials per class and at least two channels. It uses an 8–30 Hz branch, fold-local common spatial patterns, fixed ridge LDA, participant-local stratified cross-validation, and a permutation null. Outputs include balanced accuracy, fold results, and the report.

The classifier does run; it is different from the TorchEEG readiness-only entry below. However, its score is not subject-independent validation or a deployable BCI. Autocorrelation, block structure, and confounds can limit within-run estimates.

A PRAYCG3 Target/Override contrast is not automatically a motor-imagery task. Do not rename video phases as left/right imagery simply to satisfy an input contract. Missing classes, too few trials, or degenerate covariance prevent a defensible result.

## 21. Sensor-Level Representational Similarity

ID: `eeg_sensor_rsa_v0_1`

**Question:** Which declared conditions have similar or different sensor-level response patterns?

This requires the governed derivative, event set, and frozen multi-condition recipe. The current worker needs at least four conditions and four complete trials per condition. It computes an odd/even two-fold crossvalidated, diagonal-shrinkage Mahalanobis distance matrix. An optional frozen model dissimilarity matrix can be compared using a condition-label permutation null.

Outputs are the report and sensor representational-dissimilarity table. This is the packaged estimator, not an automatic invocation of every method in external RSA libraries. Insufficient trials, degenerate residual variance, or an undefined model correlation remain unavailable. No model comparison is established merely by producing a data matrix.

Sensor geometry is not anatomical localization or proof of a cognitive representation. A standard three-branch PRAYCG3 run generally does not supply this module's four-condition repeated-trial design just because it contains many EEG samples.

## 22. TorchEEG Isolated Research-Sandbox Readiness

ID: `torcheeg_research_sandbox_v0_1`

**Question:** Is a proposed machine-learning dataset organized with basic provenance and leakage safeguards?

After integrity QC, this entry reads a dataset manifest with local file hashes, labels, frozen preprocessing, and participant-disjoint folds. The implementation requires at least five explicit participants and two labels; five is a software-readiness floor, not a statistical power recommendation. It checks that each participant appears in a test fold exactly once and that files match their declared hashes.

The output is a readiness JSON with `training_performed: false`. The optional isolated TorchEEG environment is not bundled. This entry does not train a neural network, return accuracy, download models, or create an emotion classifier. One person's repeated PRAYCG runs are not five independent participants.

Passing metadata checks does not demonstrate calibration, fairness, adequate power, external generalization, or clinical usefulness. Actual model development remains separate research work.

## 23. Atlas Research Protocol Analysis

ID: `atlas_research_analysis_v1_0`

**Question:** What behavioral responses were recorded for one of the fourteen supported research Atlas protocols?

This entry follows integrity QC and uses the exact selected Atlas manifest and its event log, bound explicitly rather than guessed from a nearby file. It supports adaptive choice/reversal, signal structure/processing stance, analytic load, information pressure, static-image meaning, subjective time, agency, inhibitory control, aesthetic response/memory, playful flexibility, purpose/persistence, stability/recovery, cardiorespiratory task performance, and observedness protocols.

It computes protocol-declared counts, accuracy, response times, ratings, differences, or slopes as applicable. Outputs include `atlas_research_analysis_v1_0.json`, a narrative report, trial-response CSV, and condition summaries. It does not run the native PRAYCG Master Suite or require an EEG event recipe for these behavioral summaries.

Missing response fields/counts remain `NOT_ESTIMABLE`. The cardiorespiratory protocol's physiological endpoints cannot be inferred from breathing instructions or button presses: real synchronized streams need separate analysis. Behavioral completion does not validate the protocol's theoretical construct or establish causality.

## Choosing analyses for a contaminated PRAYCG3 demonstration

First bind the actual XDF and event set, verify the run identity, and retain the contamination/incomplete-run label. If LabRecorder continued after the experiment, use the governed analysis window; do not pretend the extra tail is a new baseline. Keep raw files intact.

Start with required QC. If enough valid EEG survives, add preprocessing and spectral screening, then optional connectivity, complexity, or run-local microstates according to their data requirements. These can provide meaningful descriptions of a contaminated recording without declaring it clean.

Use the Master Suite and chain for native phase-based analyses. They need trustworthy event timing and baseline/condition evidence; anchors, familiarity, cue schedules, stimulus regressors, self-reports, and channel maps make particular downstream questions answerable. Their absence should be visible in reports. Autonomic analysis additionally needs actual retained beat/respiration data. CAI/SID may remain non-estimable after successful Master execution because valid-time or future-window coverage fails. Micro Handoff cannot make a ten-second baseline satisfy its thirty-second rule.

Do not select ShotOrder HOC-R for missing PRAYCG4 conditions, meditation analysis for PRAYCG3, or a repeated-trial estimator without the required repeated trials. Those are design mismatches, not problems solved by unlocking another button.

Finally, inspect individual reports and native tables, not only the master summary. Preserve plan/recipe revisions and artifact hashes in the research bundle. Label retrospective exploration honestly. An informative result can be “this recording supports descriptive spectral analysis, but not the proposed anchor contrast.” That is a limitation established by the evidence, not a scientific failure to conceal.

## Scope and documentation limits

This guide was checked against the Alpha 10.0.4 active registry, managed adapters, current worker configurations, and preserved method specifications. It is a software guide, not independent validation of custom neuroscience constructs or an assurance that every recording will run every method. Synthetic test success establishes tested software behavior only. Legacy/direct GUIs can expose options or outputs not produced by a managed Forge entry; keep their separate manifests and do not treat manual completion as a managed receipt.

No module here establishes consciousness, a clinical diagnosis, quantum effects, cellular memory, or a causal mechanism merely by producing a score. Optional missing evidence, different preprocessing branches, nested unavailable results, and unsupported machine-learning execution remain important boundaries of this release.
