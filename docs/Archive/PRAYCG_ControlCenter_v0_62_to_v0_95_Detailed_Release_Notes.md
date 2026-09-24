# PRAYCG Control Center — Detailed Public Release Notes

## v0.62-era baseline through v0.95

**Release period:** August 2026–September 2026  
**Approved author:** Hoyt Banks  
**Contact:** hoytbanks@gmail.com  
**GitHub:** https://github.com/hbanks87/praycg-open  
**OSF project:** https://osf.io/8n75v/overview?view_only=928f1fa1974b40e89252101d0ba356d3

## Scope and archival note

These notes describe the cumulative development of the PRAYCG Control Center from the requested v0.62 starting point through v0.95. The earliest retained standalone source archive in the reviewed materials is the v0.61 Module Update, which describes the software generation immediately surrounding the requested v0.62 baseline. Accordingly, this document calls that starting state the **v0.61/v0.62-era baseline** and does not invent a distinct v0.62 change list that is not supported by a surviving manifest.

Versions v0.63–v0.69 and v0.88–v0.89 are not represented as separate public releases in the retained package history. Later releases retain earlier functionality unless a note explicitly says that a component was replaced, isolated, or removed from the public package.

## Executive summary

The v0.62-era system was already more than a launcher. It bundled a three-branch PRAYCG runner, MediaPrep and StimulusFingerprint generation, EEG/autonomic acquisition bridges, a Master Comprehensive Analysis Suite, an Offline Interpreter, and the first explicit confound-defense modules. From that baseline through v0.95, development proceeded along six connected tracks:

1. **Reliable operation:** Windows path handling, Python/PsychoPy launch behavior, dependency repair, visible logs, process monitoring, and per-tool shutdown controls were progressively hardened.
2. **Timing and acquisition provenance:** runner-generated ALS barcodes, holder calibration, timestamp diagnostics, immutable run identifiers, richer event records, stream-specific QC, and an optional 30-second acquisition validation made synchronization failures more visible.
3. **Stronger experimental controls:** ShotOrderScramble was added alongside PhaseScrambled and Contextual Override so high-order narrative sequence could be tested without destroying all recognizable local content.
4. **Analysis integrity:** the Master Suite moved to a canonical versioned analysis frame, explicit eligibility gates, missingness rather than favorable zero substitution, dependency-aware chained execution, exact artifact indexing, and status-aware interpretation.
5. **Modular protocols and future studies:** PRAYCG3, PRAYCG4, and Semantic Meaning Gradient became selectable, hash-locked protocol modules. Prospective counterbalanced PRAYCG3/PRAYCG4 variants were then added separately without rewriting the original fixed-order public protocols.
6. **Exploratory theory development:** CAI/SID v0.2, continuous autonomic arrays, and Micro Handoff v0.1 were implemented as isolated candidates with visible claim boundaries. None of them changes Master Suite eligibility or a primary PRAYCG conclusion.

The current result is a provenance-aware research workbench rather than a single monolithic program. It is designed to make experimental inputs, timing, QC failures, analytical applicability, and epistemic limits visible at every stage.

## Version overview

| Release | Principal contribution |
|---|---|
| v0.61/v0.62 era | Consolidated Control Center, MediaPrep v1.8, PRAYCG2.0, Master Suite v1.5.7 confound expansion, Interpreter v1.5.6, and acquisition bridges |
| v0.7 | Runner-level ALS barcode timing and barcode-analysis priority stack |
| v0.8 | ShotOrderScramble, ShotOrder HOC-R support, and ALS holder calibration |
| v0.81 | Visible launcher wrappers, process status, logs, stop/force-kill controls, and quick-exit diagnosis |
| v0.82 | MediaPrep path, working-directory, dependency, fallback, and debug diagnostics |
| v0.83 | Reproducible dependency installation and MoviePy repair workflow |
| v0.84 | Unbuffered MediaPrep progress, success sentinel, and embedded-barcode backup disabled by default |
| v0.85 | NumPy 2/MoviePy control-audio stack compatibility fix |
| v0.851 | Windows/PsychoPy/OpenBCI button-launch reliability and saved-path migration |
| v0.86 | Clean public package and reliable selected-tool process-tree shutdown |
| v0.87 | Master Suite v1.6.0, canonical analysis frame, eligibility gates, Baseline 2 recovery, and dependency-aware full chain |
| v0.90 | PRAYCG2.2 provenance runner, hardened BrainFlow bridges, and optional 30-second acquisition/ALS validation |
| v0.91 | Visualizer v1.4.0, Interpreter v1.6.0, Artifact Index v1.0, and chain v1.6.1 |
| v0.92 | Active Research Context, automatic input propagation, ambiguity safeguards, and a visible Close button per running tool |
| v0.93 | Hash-locked protocol library with PRAYCG3, PRAYCG4, and Semantic Meaning Gradient modules |
| v0.94 | Exploratory CAI/SID v0.2, readiness preflight, Continuous Autonomic/RespDualPath v1.0, and prospective-study preparation |
| v0.95 | Exploratory Micro Handoff v0.1, synthetic acceptance, frozen hashes, historical audit, and Control Center integration |

## Detailed chronological changes

## v0.61/v0.62-era consolidated baseline

The early consolidated generation established the basic public architecture carried forward by every later release.

### Control Center and software organization

- Provided one Windows dashboard for launching acquisition, media-preparation, protocol, analysis, visualization, and interpretation tools as separate processes.
- Retained the Windows-safe Python command builder introduced to address `WinError 2` failures caused by splitting backslash paths or paths containing spaces.
- Added **Use Bundled Paths** and **Use Current Python** recovery controls while keeping PsychoPy and LabRecorder explicitly external.
- Bundled procedure manuals, theory documentation, templates, hardware guidance, and public-release boundaries alongside the software.

### Baseline component set

- MediaPrep/StimulusFingerprint v1.8.
- PRAYCG2.0 consolidated self-report runner.
- Master Comprehensive Suite v1.5.7.
- Offline Master Interpreter v1.5.6.
- BrainFlow EEG-only v1.0 and EEG+ALS/PT19 v1.4 bridges.
- Polar H10 and Vernier respiration LSL bridges.

### First expanded confound-defense layer

Master Suite v1.5.7 bundled five explicitly separated challenges to an overly simple narrative-effect interpretation:

- **HOC-R — High-Order Control Residualization:** asks whether a candidate effect remains after accounting for high-order stimulus organization and control-branch structure.
- **OSA — Override Spatial Attention/AOI Burden:** asks whether gaze location, subtitle/cue location, or analytic-task visual burden could explain a difference.
- **OHC — Order, Habituation, and Carryover:** asks whether fixed order, fatigue, novelty loss, habituation, or prior-condition carryover could explain the apparent effect.
- **AAM — Afterglow Attribution Model:** asks whether post-stimulus persistence is more consistent with the immediately preceding condition, generalized recovery, or a nonspecific aftereffect.
- **RespDualPath — Respiratory Artifact versus State-Event Split:** separates respiration as a physiological correlate from respiration as a source of movement or EEG contamination.

These modules were introduced because an effect should not be called narrative reception or persistent state change merely because a Target branch differs from one control. It must also survive plausible sensory, attentional, order, afterglow, respiratory, and artifact explanations.

## v0.7 — runner-level ALS barcode timing

v0.7 established a timing priority stack centered on a barcode rendered by the PsychoPy runner rather than permanently baked into the media.

- PRAYCG2.1 drew a physical-screen long/short ALS barcode before each analyzable video branch.
- The runner emitted local/LSL events for barcode start, pulse A, pulse B, barcode end, and content start.
- Master Suite v1.5.8 added barcode-pattern detection.
- The Control Center added a live barcode test.
- MediaPrep v1.8B retained an optional embedded-MP4 barcode only as a backup path.

The runner overlay became preferred because it is tied to the actual display event and is not shifted by media scaling, aspect ratio, safe-fit positioning, or re-encoding. A barcode detection improves timing confidence; it does not by itself improve the evidential grade of a physiological endpoint.

## v0.8 — ShotOrder structural control and ALS holder calibration

### ShotOrderScramble

MediaPrep v1.9 added a ShotOrderScramble control generated from the cleaned master before cue application. It preserves local shots, faces, bodies, objects, voice fragments, scene statistics, and biological motion more successfully than PhaseScrambling while disrupting the larger narrative-temporal sequence.

This control was added because PhaseScrambling changes both narrative order and much of the recognizable high-order visual structure. With only Target and PhaseScrambled, a difference can be attributed ambiguously to low-level sensory structure, recognizable local content, or coherent narrative sequence. The intended future contrast family became:

- Target versus PhaseScrambled: intact narrative/local structure versus low-level sensory control;
- Target versus ShotOrderScramble: coherent sequence versus recognizable but reordered local content;
- Target versus Contextual Override: natural reception versus analytic/task framing on substantially matched content.

ShotOrderScramble does not prove that any surviving Target difference is “meaning.” It narrows one important alternative explanation when cue timing, media construction, artifacts, task burden, order, and other confounds are also controlled.

### ShotOrder HOC-R

Master Suite v1.5.9 added native ingestion of Target, PhaseScrambled/Control, ShotOrderScramble, and Override branches. This created the structural basis for four-branch high-order-control contrasts while leaving three-branch modules three-branch unless they explicitly declare ShotOrder support.

### ALS holder calibration

- Added a holder profile scaffold and the `Laptop_ALS_PT19_holder_openscadfile2.scad` hardware file.
- Added a calibration utility for relating the physical PT19/ALS aperture to the runner's on-screen barcode rectangle.
- Retained the requirement to verify the barcode placement script and display location on the actual acquisition computer.

The holder profile and screen-location check address a practical failure mode: a correct software pulse can still be invisible if the physical sensor and rendered barcode do not overlap.

## v0.81–v0.85 — launchability and MediaPrep reliability

These versions were predominantly engineering releases. They did not change the intended scientific interpretation.

### v0.81 — visible wrappers and process controls

- Replaced silent or unexplained launches with GUI wrappers for MediaPrep, Master Suite, embedded-barcode backup, HOC-R ShotOrder, and the ALS detector.
- Added visible tool names, process IDs, status, runtime, and log paths.
- Added Stop Selected, Force Kill, Open Log, and Refresh controls.
- Added quick-exit detection that points users to the relevant log when a child process fails immediately.

### v0.82 — MediaPrep launch diagnostics

- Corrected the MediaPrep working directory.
- Added multi-candidate MediaPrep fallback and visible dependency checking.
- Added a direct debug launcher and dedicated MediaPrep logs.
- Made it easier to distinguish “button did nothing” from a script import, path, or dependency failure.

### v0.83 — dependency repair

- Added a versioned common-requirements file and installer.
- Added an **Install/Fix MediaPrep Dependencies** workflow.
- Exposed the missing MoviePy environment problem discovered by the more transparent v0.82 launcher.

### v0.84 — robust progress and completion detection

- Mirrored MediaPrep progress into Control Center logs with unbuffered output.
- Added a success-sentinel file so completion is distinguishable from a stalled or interrupted render.
- Disabled MediaPrep's embedded ALS backup by default, preserving the runner-level barcode as the normal timing path.

### v0.85 — audio-stack compatibility

- Fixed the control-audio crash caused when newer NumPy rejected a generator passed directly to `vstack` through MoviePy.
- Changed audio loading to materialize chunk sequences before stacking, with fallback behavior retained.

This was an engineering compatibility repair. It did not certify that a generated control audio track is unintelligible, perfectly matched, or scientifically adequate; manual media QC remains required.

## v0.851 — button-launch reliability

v0.851 addressed failures observed on the actual Windows/PsychoPy/OpenBCI host.

- Added a resilient starter that tries a local Python 3.11 installation, then the Windows `py` launcher, then `python` on PATH.
- Used PsychoPy's bundled Python and opened the PRAYCG2.1 runner directly in PsychoPy Coder, avoiding a failing `psychopy.exe` path-canonicalization route.
- Required and validated the OpenBCI COM port before either BrainFlow bridge launches.
- Remembered the selected COM port.
- Automatically rebased old bundled paths to the current extraction while preserving external PsychoPy and LabRecorder settings.
- Corrected internal application and configuration versions.

## v0.86 — clean public package and safer tool shutdown

v0.86 converted the accumulated development bundle into a smaller public-facing package.

- Removed superseded launchers, older tool copies, duplicate patch notes, redundant research packs, generated examples not needed at runtime, and other non-current files.
- Kept current software, configuration templates, component documentation, dependency lists, and ALS-holder materials.
- Made Running Tools rows selectable and visibly highlighted.
- Added **SHUT DOWN SELECTED TOOL** for normal process-tree shutdown, with a force-close prompt if normal shutdown does not finish.
- Preserved selection during dashboard refreshes.

The process-tree behavior matters because many dashboard buttons start a wrapper that then starts a child GUI. Closing only the wrapper can leave the real tool or acquisition process running.

## v0.87 — Master Comprehensive Suite v1.6.0

v0.87 was a major analysis-integrity release.

### Canonical analysis frame and full chain

- Introduced the canonical `PRAYCG_AnalysisFrame_v1_6_0`.
- Added a dependency-aware full chained-analysis launcher.
- Recorded each module as `PASS`, `FAIL_PRIMARY_GATE`, `NOT_GRADABLE_MISSING_INPUT`, `NOT_APPLICABLE_PROTOCOL`, `EXPLORATORY_ONLY`, or `SOFTWARE_ERROR` rather than collapsing different failure modes.

### Eligibility and missingness

- Added strict checks for required protocol phases, EEG coverage, effective-versus-nominal sample rate, and timestamp gaps.
- Preserved exploratory outputs after a failed primary gate while blocking strict endpoint interpretation.
- Treated absent or invalid measurements as missing rather than silently substituting zero.
- Made unavailable spectral bands explicitly unavailable when the sample rate cannot support them, rather than silently clipping the band.

### Baseline 2 and physiology

- Made Baseline 2/final reflection a first-class recovery phase.
- Exported Baseline 1 versus Baseline 2 feature and physiology summaries.
- Selected HR/RR streams by identity and physiological plausibility while explicitly excluding respiration streams from cardiac selection.
- Added raw-window respiration features for RespDualPath.

### Chained-module corrections

Fixed empty tables, missing columns, ambiguous input selection, recursive output selection, and row-alignment faults discovered while chaining the expanded modules.

These changes improved auditability and prevented software convenience from rescuing a run that failed acquisition or timing gates. They did not validate any exploratory proxy as a biomarker.

## v0.90 — provenance runner and acquisition diagnostics

### PRAYCG2.2 runner

- Introduced one immutable run UUID shared by stream metadata, event rows, filenames, configuration, and lifecycle manifest.
- Replaced the legacy event table with a versioned schema containing event kind, condition, scheduled time, observed flip time, timing delta, clock source, and confidence.
- Recorded visible phase, instruction, questionnaire, video, cue, anchor, and barcode transitions.
- Measured display refresh rate when available and retained dropped-frame summaries.
- Added fail-closed validation for required media, cue/anchor parsing, accidental bit-identical Target/Override media, optional ALS placement profiles, and output writability.
- Added durable `PRECHECK`, `READY`, `RUNNING`, `ABORTING`, `COMPLETED`, and `INCOMPLETE` lifecycle states.
- Preserved partial logs and the reason for escape-key or error aborts.
- Hashed selected stimuli, sidecars, anchors, and calibration profiles.

### BrainFlow acquisition bridges

- Advanced EEG-only to v1.1 and EEG+ALS to v1.5 on a shared Acquisition Diagnostics Core v1.0.
- Reconstructed per-sample timestamps consistently while preserving board/device timestamps separately.
- Distinguished missing, duplicate, and out-of-order packet transitions.
- Preserved non-finite EEG samples as missing rather than zero.
- Tracked buffer backlog, effective rate, gaps, missingness, saturation-review counts, software/board/port configuration, channel mapping, and calibration-profile hashes.
- Wrote PASS/WARN/FAIL acquisition-QC records on normal shutdown, signal shutdown, or exception.
- Kept EEG, raw AUX, ALS, and bridge-status streams separate and explicitly typed.

### Optional 30-second acquisition validation

The proposed mandatory 30–60 second arming gate was deliberately not imposed. Instead, v0.90 added a separate **Run Optional 30-Second Acquisition Validation** button next to the signal-quality/contact helper.

The test checks:

- effective sample rate;
- timestamp monotonicity and large gaps;
- missing, flat, noisy, or saturation-review channel indicators;
- ALS long/short pulse visibility;
- display resolution and estimated physical geometry;
- barcode rectangle and pulse schedule;
- saved holder-profile identity/hash when available.

It writes Markdown, JSON, and per-channel CSV diagnostics. It never arms, unlocks, or blocks the runner.

### ALS barcode placement script-location test

The validation displays the actual long/short barcode at the configured runner location and records its screen coordinates and geometry. This provides a direct placement test for aligning the physical PT19/ALS holder aperture with the runner-rendered barcode. It is intentionally separate from ordinary signal-quality scoring: good EEG contact does not demonstrate ALS visibility, and a visible ALS pulse does not demonstrate good EEG.

## v0.91 — Visualizer, Interpreter, and authoritative chain provenance

### MasterSync Visualizer v1.4.0

- Added interactive zoom, scrubbing, event selection, synchronized cursors, and snapshot support.
- Added a persistent eligibility/module-status ribbon so diagnostic plots cannot be mistaken for inference-eligible evidence.
- Exposed measured versus estimated timing, scheduled/observed/ALS times, residuals, source paths, and confidence.
- Added raw/source-unit and robust-z views, valid-sample coverage, PhaseScrambled and ShotOrder selection, and four-branch HOC-R review.
- Moved MP4 rendering to a background process with progress and cancellation.

### Offline Interpreter v1.6.0

- Replaced recursive fuzzy file selection with exact filenames from Analysis Artifact Index v1.0.
- Read run eligibility, chain manifests, and module statuses before interpreting tables.
- Preserved the distinction among failed gates, missing inputs, non-applicable modules, exploratory outputs, and software errors.
- Built a source-linked evidence ledger before creating technical, research, or public-safe reports.
- Added four-branch HOC-R contrasts, the HOC-R/OSA/OHC/AAM/RespDualPath confound matrix, and convergence/contradiction review.
- Added cross-run compatibility checks without automatic pooling.
- Fixed stale version/help text, flag handling, silent reads, and an obsolete subprocess call.

### Chain v1.6.1

- Retained the v1.6.0 canonical calculations.
- Published the authoritative chain manifest before interpretation.
- Refreshed the manifest and artifact index after completion with exact paths, hashes, duplicates, gate states, and module outcomes.

## v0.92 — Active Research Context and automatic input propagation

v0.92 reduced one of the largest practical sources of workflow error: launching the right tool with the wrong folder or stale remembered inputs.

### Active Research Context v1.0

- Added a persistent context bar for the active stimulus, raw run, canonical core output, chain output, and review readiness.
- Stored user selection under the user's Control Center settings rather than inside the public package or raw data.
- Used explicit `RESOLVED`, `MISSING`, `AMBIGUOUS`, `INCOMPATIBLE`, and manual-selection states.
- Refused to choose an artifact merely because it had the newest modification time.
- Added visible Media → Run → Core → Chain → Review organization plus recent and pinned catalogs.

### Context-aware launch population

- Stimulus selection prefilled MediaPrep's master MP4, output root, and project name.
- Raw-run selection resolved XDF, JSON event log, channel map, run UUID, protocol schema, cue schedule, locked anchors, and recorded condition media.
- Master Suite received available raw-run/stimulus inputs and the configured output root.
- Chain, HOC-R, and confound tools received only a validated canonical core output.
- Visualizer received the compatible review folder, XDF, event log, and Target media when available.
- Interpreter received the preferred compatible chain/core folder and run label.
- ALS Barcode Detector received the selected run, exact XDF, and JSON event log.

Input population remained review-first: the Control Center filled fields but did not press Run inside a launched analysis tool.

### Per-tool process controls

- Replaced the shared/off-screen shutdown area with a scrollable row layout.
- Added a visible red **Close** button to every running tool.
- Added per-tool Open Log and More actions for Force Close, Open Working Folder, and Restart.
- Retained process-tree shutdown, post-exit context refresh, and log preservation.

## v0.93 — plug-and-play protocol library

v0.93 separated protocol-specific scientific structure from shared PsychoPy/LSL execution mechanics.

### PRAYCG3 v3.0

Preserved the original fixed-order three-prong structure:

`CONTROL_1 → washout/report → TARGET_1 → washout/report → CONTEXTUAL_OVERRIDE_1 → washout/report`

Baseline 1, Baseline 2/final reflection, and the final report were retained.

### PRAYCG4 v4.0

Added ShotOrder after the completed PhaseScrambled washout/report:

`CONTROL_1 → washout/report → SHOT_ORDER_SCRAMBLE_1 → washout/report → TARGET_1 → washout/report → CONTEXTUAL_OVERRIDE_1 → washout/report`

PRAYCG4 also retains Baseline 1, Baseline 2/final reflection, and the final report. ShotOrder inputs and generation manifests receive path/hash provenance.

### Semantic Meaning Gradient v1.0

Translated the D205 proposal into a conditional acquisition module:

`SEMANTIC_ZERO_1 → HIGH_MEANING_TARGET_1 → ARITHMETIC_OVERRIDE_1`

- Required a distinct semantic-zero stimulus rather than automatically substituting PhaseScrambled media.
- Added ratings for meaning, empathy, absorption, threat, puzzle demand, narrative engagement, carryover, task extraction, analytic effort, and compliance.
- Preserved native SMG markers while providing explicitly labeled compatibility aliases for current segmentation.
- Recorded SZI, OPI, ΔM, MCS, and MRI as proposed/unvalidated concepts; the runner does not compute an MRI.
- Kept variance and rate-of-change separate unless a dimensionally coherent scaling is declared.

### Protocol discovery and locking

- Added versioned protocol manifests and schema validation.
- Displayed purpose, exact branch order, hashes, and scientific boundaries before locking.
- Separated Select from Lock.
- Rejected stale or modified protocol/runner locks.
- Wrote protocol snapshots, runner hashes, native order, media/sidecars, and integrity results into run provenance.

The protocol library permits future modules without duplicating timing, barcode, lifecycle, and acquisition-safety code. A static hash/structure check is not a substitute for an interactive PsychoPy/LSL/LabRecorder/ALS acceptance run.

## v0.94 — CAI/SID, continuous autonomic arrays, and prospective preparation

### CAI/SID v0.2

- Formalized **Controlled Access-Integration Index**.
- Corrected the positive-loop equation so jointly low fast and future-slow inputs do not create positive loop evidence.
- Used equal-weight primary support from positive fast evidence, positive slow evidence, and their corrected loop term.
- Treated non-estimable correlation as unavailable rather than favorable.
- Kept invalid hard-QC windows missing.
- Kept DGA/contextual gating and autonomic outputs separate from primary CAI.
- Added prospective PhaseScrambled and ShotOrder condition support while preserving legacy `CONTROL_1` compatibility.
- Recorded code/configuration hashes and stopped historical tuning at the frozen v0.2 candidate.

CAI/SID remains exploratory. It is a bounded, unitless operational proxy—not a probability, diagnosis, validated consciousness measurement, or proof of narrative reception.

### CAI analysis-readiness preflight

Added `PASS`, `CAUTION`, and `INELIGIBLE` readiness outcomes based on:

- recognized protocols and conditions;
- unique block-instance identifiers;
- timestamp monotonicity and gaps;
- Baseline 1 availability;
- required feature columns;
- branch coverage and artifact sentinels;
- ALS timing and legacy-adapter status;
- autonomic, DGA, ShotOrder, and anchor availability.

A readiness PASS means the computation can proceed under the declared schema. It does not mean that the construct is valid.

### Continuous Autonomic/RespDualPath v1.0

- Added a cardiac beat-event table and interpolation-flagged 4 Hz HR grid.
- Computed RMSSD, SDNN, and pNN50 from retained beat events rather than interpolated HR.
- Added respiration rate, depth/amplitude, Hilbert phase, velocity, acceleration, sigh, and hold candidates.
- Separated physiology and respiratory artifact/confound paths.
- Added exploratory HR–respiration lag coupling with circular time-shift nulls.
- Added source hashes, timestamp diagnostics, coverage, QC, and human-readable reports.

Autonomic outputs remain separate from primary CAI until independently validated.

### Prospective PRAYCG3/PRAYCG4 package

- Added six fixed PRAYCG3 and four fixed PRAYCG4 Williams-design sequence variants for future counterbalanced collection.
- Kept the original public fixed-order PRAYCG3 and PRAYCG4 modules unchanged.
- Retained Baseline 1, every branch washout/report, Baseline 2/final reflection, and the final report.
- Required runner-registered ALS events and the barcode placement script-location test.
- Added recognition, comprehension, confidence, narrative-coherence, and structured subjective outcomes independently of CAI construction.
- Added deterministic assignment, file hashing, blinded feasibility auditing, illustrative sample-size simulation, an OSF preregistration draft, and promotion Gates 7–10.

The supplied prospective configuration remains a template until real stimuli, derivatives, anchors, approvals, and hardware validation are provided.

## v0.95 — Micro Handoff v0.1

v0.95 added an isolated raw-EEG candidate motivated by the hypothesis that temporally local fast activity and slower integration may show measurable coordination over short lags.

### Frozen operational candidate

- Uses a 25 ms output update grid, not a claim of 25 ms spectral resolution.
- Estimates temporal gamma at T5/T6 with a 250 ms causal window.
- Estimates theta integration at Pz/P3/P4/T5/T6 with a 500 ms causal window.
- Uses Baseline 1 robust normalization with no full-run fallback.
- Uses a fixed equal-weight lag bank from 100 to 1000 ms rather than selecting a condition-specific best lag.
- Separates state coordination, directional positive handoff, and activation-weighted coordination density.
- Allows low-low signals to count as similar states but not as positive handoff or high density.
- Treats hard artifact and timestamp-gap windows as missing.
- Reports circular-shift, phase-randomized, block-label, and artifact-matched checks.
- Freezes the mathematical specification, configuration, implementation, tests, and synthetic-summary hashes.

### Synthetic acceptance

All 14 declared raw-signal synthetic checks passed. A planted 500 ms handoff was recovered at 600 ms, within the declared ±100 ms tolerance associated with unequal causal spectral windows. The suite also verified low-low, stationary high-high, reverse-direction, independent, artifact, timestamp-gap, null, and deterministic-repeat behavior.

### Historical evaluation

The frozen candidate inventoried 24 unique historical XDF recordings. Six were computationally eligible with caution, all at 125 Hz. Directional Target-minus-Control handoff was mixed around zero, diagnostic lags varied, and no recording passed both time-structure null families. Activation-weighted Target density was descriptively higher in five of six eligible runs, but density is not the same as directional handoff and the archive is confounded by repeated single-participant, stimulus, condition-order, acquisition-generation, and software-generation differences.

The appropriate status is:

**Software-valid, construct-unvalidated, retrospectively mixed.**

Micro Handoff is not a consciousness detector, probability, diagnosis, proof of discrete 40 Hz frames, or validated “consciousness RPM” gauge.

### Control Center integration

- Added a **Micro Handoff v0.1** button to the isolated Exploratory Analysis panel.
- Automatically passes the selected run, resolved XDF when available, preferred analysis folder, and a run-specific output folder.
- Added bundled-path rebasing and Settings support.
- Registered the module as unable to alter Master Suite eligibility, primary conclusions, or automatic chain execution.

## Why the principal scientific additions were made

### PhaseScrambled plus ShotOrder plus Override

No single control isolates “meaning.” PhaseScrambling is useful for reducing recognizable structure but also changes high-order visual and temporal organization. ShotOrder preserves more local content while disrupting sequence. Contextual Override keeps much of the media intact but changes task framing. Their joint use allows narrower questions about low-level drive, local recognizable content, coherent order, and analytic stance.

### HOC-R, OSA, OHC, AAM, and RespDualPath

These modules force an apparent Target effect to confront alternative explanations involving stimulus organization, spatial attention, task burden, order, habituation, carryover, afterglow attribution, respiration, and artifact. They are defenses against premature interpretation, not automatic correction mechanisms that guarantee causal identification.

### Canonical frame, gates, and status-aware chaining

As the module count increased, ambiguous folder selection and silent missingness became as dangerous as formula errors. The v1.6 architecture makes each input, exclusion, dependency, failure, and applicability decision inspectable. It permits exploratory output after a failed gate without letting that output silently inherit confirmatory status.

### CAI/SID and Micro Handoff

Both candidates translate theoretical intuitions into falsifiable operational quantities. Their implementations deliberately separate software readiness from construct validity, freeze choices before retrospective summaries, retain null/reversed outcomes, and require prospective reliability, calibration, independent criteria, and replication before any promotion.

## Current v0.95 component inventory

- PRAYCG Control Center v0.95.
- Active Research Context v1.0.
- Protocol Module Library v1.0 with shared engine v3.0.
- PRAYCG3 v3.0, PRAYCG4 v4.0, and SMG v1.0.
- MediaPrep/StimulusFingerprint v1.9 ShotOrder.
- Master Comprehensive Suite v1.6.0 canonical core and v1.6.1 chain.
- MasterSync Visualizer v1.4.0.
- Offline Interpreter v1.6.0.
- HOC-R/OSA/OHC/AAM/RespDualPath confound-defense path.
- BrainFlow EEG-only v1.1 and EEG+ALS v1.5 with Acquisition Diagnostics Core v1.0.
- Optional Acquisition Preflight v1.0.
- CAI/SID v0.2 exploratory candidate.
- Continuous Autonomic/RespDualPath v1.0 exploratory module.
- Prospective Study Package v0.1.
- Micro Handoff v0.1 exploratory candidate.

## Validation status of v0.95

- 36 focused regression and mathematical tests passed.
- 109 Python sources parsed.
- 53 JSON files parsed.
- All 24 bundled Control Center tool paths resolved.
- All frozen Micro Handoff hashes matched.
- The public archive contains no historical XDF/EDF/BDF recordings, private historical result tables, personal absolute paths, copyrighted research media, credentials, local settings, or Python caches.

The validated v0.95 public ZIP has SHA-256:

`5B36631A0D0E35EED9AE1E00F2F053F0B3634D7FE4E9AB41599C40A2486A9C4C`

## What has not been established

Software validation does not establish:

- timing performance on every acquisition computer;
- correct sensor placement or a successful real-hardware ALS test;
- artifact-free or inference-eligible acquisition;
- successful manipulation of narrative meaning;
- causal separation of every stimulus, order, task, and physiological confound;
- population generalizability from historical self-runs;
- clinical or diagnostic utility;
- a validated measure of consciousness;
- a biological, quantum, or metaphysical mechanism.

Prospective claims require a frozen protocol, ethics/consent as applicable, real hardware acceptance, multiple participants and stimuli, declared exclusions and nulls, multiplicity control, participant/stimulus random effects, independent validity outcomes, reliability/calibration, and publication of null or reversed findings.

## Public repository and licensing boundary

This project uses a mixed-license layout:

1. Code in `software/` and upload scripts is released under the MIT License unless a file states otherwise.
2. Documentation in `docs/`, templates, and non-personal example metadata is released under CC BY 4.0 unless a file states otherwise.
3. Synthetic demo media in `examples/no_copyright_media_demo/` is released under CC0 1.0.
4. Recipe-generated third-party media remains under its original source license. Sintel-derived material requires CC BY 3.0 and Blender Foundation attribution.
5. Derived self-run example data is public-safe pilot material only and must not be treated as clinical, diagnostic, or confirmatory evidence.

Public releases should exclude copyrighted stimulus media, private raw biosignals, personally identifying or health-sensitive data, local credentials/settings, and unredacted self-report. Large public-safe archives may be placed on OSF while source code, documentation, templates, and synthetic examples remain suitable for GitHub.

## Upgrade guidance

- Treat v0.95 as the current cumulative public build.
- Extract it to a normal folder rather than running from a ZIP preview.
- Run `INSTALL_PRAYCG_REQUIREMENTS_v0_95.bat` once.
- Start with `run_PRAYCG_ControlCenter_v0_95.bat`.
- In Settings, choose **Use Bundled Paths**, locate external PsychoPy and LabRecorder installations, and save.
- Recreate rather than blindly copy old local configuration if a path remains unresolved or points to an older extraction.
- Lock the intended protocol module before launching a runner.
- Review active stimulus/run/core/chain context and ambiguity warnings before analysis.
- Run the optional 30-second acquisition/ALS validation on the real display and holder arrangement before a study session, while remembering that it does not arm or certify the runner.
- Keep CAI/SID, continuous autonomic, and Micro Handoff outputs in their exploratory evidence grade unless their separately declared promotion requirements are met.
