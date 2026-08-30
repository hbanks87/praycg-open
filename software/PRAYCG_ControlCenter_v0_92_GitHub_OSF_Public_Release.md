# PRAYCG Control Center v0.92

## Public release history from the v0.62-era build through v0.92

**Release date:** 2026-08-29  
**Suggested GitHub tag:** `v0.92`  
**Release type:** Public research-software release  
**Primary platform:** Windows  
**Approved author:** Hoyt Banks  
**Contact:** [hoytbanks@gmail.com](mailto:hoytbanks@gmail.com)  
**GitHub repository:** [hbanks87/praycg-open](https://github.com/hbanks87/praycg-open)  
**OSF project:** [PRAYCG — project 8n75v](https://osf.io/8n75v/overview?view_only=928f1fa1974b40e89252101d0ba356d3)  
**License:** Mixed-license repository; see **Licensing** below  
**Archive:** `PRAYCG_ControlCenter_v0_92_Public.zip`  
**Archive size:** 596,956 bytes (0.569 MiB)  
**SHA-256:** `936FA07D09136FFEE5EF6018DD0A892091983167A4A585FE12B16E38243FD58C`

## Release summary

PRAYCG Control Center v0.92 is a cumulative public build of the PRAYCG research-software workflow. Relative to the v0.62-era Control Center, the package has developed from a basic launcher into a provenance-aware workspace for stimulus preparation, protocol execution, multimodal acquisition, gated analysis, visualization, interpretation, and process management.

The principal changes are:

- a physical-screen ALS timing stack and per-session barcode placement/location test;
- a ShotOrder structural-control branch and HOC-R four-branch analysis;
- expanded audits for high-order stimulus structure, spatial attention, exposure order, habituation, afterglow attribution, and respiratory alternatives;
- more reliable Windows, PsychoPy, MediaPrep, and BrainFlow launching;
- explicit process tracking and per-tool shutdown controls;
- a canonical, non-overlapping analysis frame with run-eligibility and missingness gates;
- a dependency-aware chained analysis with distinct scientific, missing-input, applicability, exploratory, and software states;
- a more rigorous PRAYCG2.2 event and run-lifecycle record;
- acquisition diagnostics that preserve missing values and expose rate, timestamp, packet, backlog, saturation-review, and shutdown information;
- a gate-aware interactive visualizer and a manifest-driven offline interpreter; and
- Active Research Context v1.0, which resolves and prefills compatible stimulus, run, core-analysis, chain, and review inputs without automatically starting an analysis.

These are engineering, traceability, and confound-control improvements. They do not validate PRAYCG hypotheses, convert proxy measures into biomarkers, or establish narrative reception, memory formation, consciousness, biological mechanism, or clinical effect.

## Archival scope and versioning note

This history was reconciled from the surviving cumulative patch notes, component manifests, public release notes, and current package contents.

A separately archived v0.62 package or v0.62 manifest was not present in the reconciled local release set. The starting point is therefore described as the **v0.62-era build**: the basic dashboard and v0.6 Windows path repair, together with the Master Comprehensive Suite v1.5.7 confound-expansion layer documented in the v0.61 module update. No undocumented v0.62-specific change is asserted here.

Likewise, no separate public v0.88 or v0.89 release artifact was found. The next documented public build after v0.87 is v0.90. This document does not invent changes for absent version records.

Control Center versions and bundled component versions are independent. For example, Control Center v0.92 contains PRAYCG Runner 2.2, MediaPrep v1.9, Master Suite core v1.6.0, chained review layer v1.6.1, Visualizer v1.4.0, and Interpreter v1.6.0.

## Version-by-version history

### v0.62-era starting point

The starting workflow provided the main Control Center dashboard, a stimulus library, acquisition launch controls, a PsychoPy-oriented runner launcher, analysis launch controls, settings, and bundled Polar H10 and Vernier respiration streamers.

The inherited v0.6 Windows repair replaced unsafe parsing of Python executable paths, added current-Python and bundled-path recovery controls, routed batch files through the Windows command processor, and made file-not-found errors show the failed command.

The inherited Master Comprehensive Suite v1.5.7 confound expansion added:

- **HOC-R v0.1:** high-order control residualization;
- **OSA v0.1:** Override spatial-attention and area-of-interest burden;
- **OHC v0.1:** order, habituation, repetition, and carryover;
- **AAM v0.1:** afterglow attribution, including Target-afterglow-like versus task-relief-like patterns; and
- **RespDualPath v0.1:** separation of respiration as a possible measurement artifact from respiration as a potentially valid state event.

These modules were introduced as secondary or exploratory confound audits. They were not endpoint-certification tools.

### v0.7 — runner-level ALS barcode timing

v0.7 implemented an ALS timing-priority stack:

1. PRAYCG2.1 runner-level physical-screen barcode pulses;
2. a Control Center live ALS barcode test;
3. Master Suite v1.5.8 barcode-pattern detection; and
4. an optional MediaPrep v1.8B MP4-embedded barcode backup.

The PRAYCG2.1 runner added markers for barcode start, long/short pulse segments, barcode end, and content start. The intent was to create an external measurement of the physical display path rather than relying only on scheduled software time.

The embedded MP4 barcode remained a redundancy option. Later releases made the runner-level overlay the default timing method because an overlay presented by the runner is better positioned to measure the actual presentation path.

### v0.8 — ShotOrder control and ALS holder calibration

v0.8 added the ALS holder calibration workflow, an OpenSCAD holder source and profile scaffold, MediaPrep v1.9 ShotOrderScramble generation, and Master Suite v1.5.9 ShotOrder/HOC-R ingestion.

ShotOrder generation writes a shot manifest, shot table, preview contact sheet, and QC report. The documented workflow generates the control from the cleaned master before applying cues, then applies the same cue schedule after shot reassembly. This is intended to preserve cue timing across Target, Override, PhaseScrambled, and ShotOrderScramble branches.

PhaseScrambled remained part of the design. ShotOrder was added as a second structural control, not as its replacement.

### v0.81 — visible launch diagnostics and process controls

v0.81 added wrapper interfaces for MediaPrep, Master Suite, embedded-barcode backup, ShotOrder HOC-R, and ALS barcode detection. These wrappers exposed folder selection, live output, stop controls, and output-folder access instead of allowing a failing process to appear to do nothing.

The Running Tools dashboard began showing tool names, process identifiers, status, runtime, and logs. It added stop, force-close, log-opening, refresh, and quick-exit reporting.

### v0.82 — MediaPrep launch diagnosis

v0.82 put a visible diagnostic window in front of MediaPrep, streamed its output, checked common dependencies, tried multiple supported MediaPrep entry points, launched from the correct working folder, and supplied a direct debug starter.

This change isolated failures that occurred before the MediaPrep interface could appear.

### v0.83 — MediaPrep dependency repair

v0.83 identified a missing MoviePy environment dependency as the cause of a pre-interface exit. It added a common requirements file, dependency installers, a targeted MoviePy repair starter, and an install/fix control in the MediaPrep diagnostic interface.

### v0.84 — MediaPrep completion and timing-doctrine hardening

v0.84 mirrored MediaPrep stage progress into Control Center logs, used unbuffered child-process output, and added a success-sentinel file on completed preparation.

The optional MP4-embedded ALS pulse was changed to off by default and relabeled as a backup. The runner-level physical-screen barcode plus holder calibration remained the normal timing path.

### v0.85 — NumPy/MoviePy audio-stack compatibility

v0.85 repaired a control-audio failure caused by newer NumPy versions rejecting a generator passed to `vstack` through MoviePy. MediaPrep now materializes audio chunks before stacking them and retains a fallback path.

This was a compatibility repair. It did not certify speech-shaped noise, intelligibility, media validity, or experimental equivalence; manual media QC remained necessary.

### v0.851 — button-launch reliability

v0.851 addressed the launch failures observed during hands-on Windows testing:

- the starter no longer depended exclusively on the Windows `py` launcher;
- saved bundled paths were rebased to the active extraction;
- PsychoPy launched through its selected Python environment and opened the PRAYCG2.1 script directly in Coder;
- BrainFlow EEG-only and EEG+ALS launches requested and validated a COM port;
- selected ports were remembered;
- Python scripts and paths were normalized before validation; and
- every early exit, including exit code zero with no remaining interface, pointed to a log.

### v0.86 — public cleanup and selected-tool shutdown

v0.86 was the first cleaned public package in this sequence. It removed superseded launchers and tool copies, duplicate patch notes and document packs, generated examples, local state, logs, research data, and copyrighted media not required by the current runtime.

The Running Tools table gained persistent row selection, visible highlighting, normal process-tree shutdown for the selected tool, and a force-close follow-up when normal shutdown did not finish.

The current scientific components at that point were PRAYCG2.1, MediaPrep v1.9 ShotOrder, Master Suite v1.5.9 ShotOrder/HOC-R, Interpreter v1.5.6, EEG-only bridge v1.0, and EEG+ALS bridge v1.4.

### v0.87 — Master Comprehensive Suite v1.6.0

v0.87 introduced the largest analysis reliability update in the series.

#### Canonical analysis frame

Master Suite v1.6.0 added `PRAYCG_AnalysisFrame_v1_6_0`, a documented table and schema for chained modules. Overlapping stimulus and washout subwindows are excluded from the canonical frame so the same underlying interval is not inadvertently counted more than once. Unavailable measurements remain missing (`NaN`) rather than becoming favorable zeros.

The manifest records suite, schema, Python, NumPy, pandas, and SciPy versions. Heart-rate and RR streams are selected by identity and physiological plausibility, with respiration-identified streams explicitly rejected and the selection decision written to provenance.

#### Run eligibility and measurement availability

Eligibility checks cover required protocol phases, EEG coverage, effective versus nominal sample rate, and timestamp gaps. A failed primary QC gate does not erase exploratory output, but it blocks strict endpoint interpretation.

Spectral features are Nyquist-aware. A band that the recorded sample rate cannot support is marked unavailable rather than silently clipped. Raw, time-aligned respiration-window features were added for RespDualPath.

#### Recovery phase

`BASELINE_2_REFLECTION` became a first-class recovery phase when present. The suite exports Baseline 1 versus Baseline 2 feature, autonomic, and respiration comparisons. If Baseline 2 is absent, the suite reports the absence rather than substituting a washout or a zero.

#### Dependency-aware chain

The full-chain runner creates a new workspace for each execution and records each module as one of:

- `PASS`;
- `FAIL_PRIMARY_GATE`;
- `NOT_GRADABLE_MISSING_INPUT`;
- `NOT_APPLICABLE_PROTOCOL`;
- `EXPLORATORY_ONLY`; or
- `SOFTWARE_ERROR`.

This distinction prevents a scientific gate failure, an unavailable input, a protocol that lacks a branch, and an actual software failure from being collapsed into one generic failure state.

The v1.6.0 repair set also prevented output/input collisions, constrained ambiguous artifact selection, made A-MRED honor core run eligibility, and handled empty tables, optional columns, unavailable visual penalties, row-alignment problems, and missing optional formatting support more safely.

### v0.88–v0.89 — no separate public record located

No independently documented v0.88 or v0.89 public package was present in the reconciled archive. The next documented cumulative public release is v0.90.

### v0.90 — Runner 2.2, acquisition diagnostics, and optional 30-second validation

#### Protocol Runner PRAYCG2.2

Runner 2.2 uses one immutable run UUID in marker metadata, event rows, event filenames, run configuration, and lifecycle manifest. Its versioned event schema retains legacy phase/marker/time fields while adding event kind, condition, scheduled time, observed flip time, timing residual, clock source, and confidence.

Critical visible changes are flip-logged, including phase baselines, instructions and questionnaire transitions, content transitions, and each ALS barcode segment. Cue and locked-anchor rows retain both scheduled movie time and observed frame-loop time.

The runner records display refresh and dropped-frame information when available. It performs fail-closed checks for required media, cue and locked-anchor parsing, supplied ALS placement profiles, Target/Override media identity, and output writability. Inputs and supplied sidecars are hashed.

Lifecycle states are explicit: `PRECHECK`, `READY`, `RUNNING`, `ABORTING`, `COMPLETED`, and `INCOMPLETE`. An abort flushes partial artifacts and retains a machine-readable reason.

#### BrainFlow acquisition bridges

The EEG-only bridge advanced to v1.1 and the EEG+ALS bridge to v1.5, both using Acquisition Diagnostics Core v1.0.

The bridges now:

- retain reconstructed host/LSL timestamps separately from board/device timestamps;
- distinguish missing, duplicate, and out-of-order packet transitions;
- preserve non-finite EEG values as missing rather than changing them to zero;
- use separate typed EEG, raw AUX, ALS, and bridge-status streams;
- record effective rate, gaps, missingness, saturation-review counts, backlog, versions, board/port settings, channel mappings, source identifiers, timestamp configuration, run UUID, and optional calibration-profile hashes; and
- write a final `PASS`, `WARN`, or `FAIL` acquisition-QC JSON and update the session manifest on normal shutdown, signal shutdown, or exception.

#### Optional acquisition validation

The proposed mandatory 30–60 second arming gate was not implemented. Instead, v0.90 added a separate **Run Optional 30-Second Acquisition Validation** button beside the Signal Quality / Contact Index helper. The test never arms, unlocks, or blocks the runner.

It samples `obci_eeg1` and `ALS_PT19_Timing`; checks effective rate, timestamp monotonicity, large gaps, missingness, flat/noisy/saturation-review indicators, and ALS pulse visibility; and writes Markdown, JSON, and per-channel CSV results.

### v0.91 — gate-aware review and interpretation

#### MasterSync Visualizer v1.4.0

The visualizer added an interactive timeline with zoom, scrubbing, event selection, synchronized cursors, and snapshots. A persistent eligibility/module-status ribbon keeps exploratory or blocked material visibly distinct from inference-eligible output.

Event provenance includes measured versus estimated timing, scheduled and observed fields, ALS timing, residuals, source paths, and confidence where available. The interface offers source units and robust-z views, valid-sample coverage, PhaseScrambled and ShotOrder branch selection, and a four-branch/HOC-R review. MP4 rendering runs in the background with progress and cancellation.

#### Offline Interpreter v1.6.0

The interpreter replaced recursive fuzzy file selection with `PRAYCG_AnalysisArtifactIndex_v1_0`, an exact-filename provenance registry. It reads run eligibility, the chain manifest, and module states before interpreting any table.

It builds a source-linked evidence ledger before producing technical, research, and public-safe reports. It preserves the distinction among scientific gate failure, missing input, protocol non-applicability, exploratory output, malformed input, and software error. HOC-R contrasts, the expanded confound matrix, and convergence/contradiction review are included.

Optional cross-run review checks schema, conditions, eligibility, and software-version compatibility but does not pool effects automatically.

#### Master Suite chain v1.6.1

The canonical core calculations remained v1.6.0. Chain v1.6.1 publishes an authoritative preliminary manifest before interpretation and refreshes the manifest and artifact index after completion. Exact paths, hashes, selected canonical files, duplicates, gate states, and module outcomes control downstream review so a stale partial table cannot override its registered state.

### v0.92 — workflow continuity, provenance-aware prefill, and per-tool close controls

v0.92 is primarily an orchestration and organization release. It does not change the mathematical methods of the v1.6.0 core, v1.6.1 chain, Visualizer v1.4.0, Interpreter v1.6.0, HOC-R, or acquisition bridges.

#### Running Tools redesign

Each launched tool now has its own visible red **Close** button in a scrollable row. Each row also offers log access and a More menu with Force close, Open working folder, and Restart. Normal process-tree shutdown is attempted first. Exited rows can be cleared without deleting retained logs.

#### Active Research Context v1.0

A persistent context bar tracks the selected stimulus, raw run, canonical core output, chain output, and review readiness. The context is saved in the user's Control Center settings area rather than inside the public package or raw-data folder.

The resolver uses explicit `RESOLVED`, `MISSING`, `AMBIGUOUS`, `INCOMPATIBLE`, and manual-selection states. It does not select an artifact merely because it is the newest file. Recent and pinned stimulus/run catalogs support switching between projects.

#### Provenance-aware input population

Selecting a registered stimulus prefills MediaPrep with the master MP4, a dedicated output root, and a project name. Selecting a run resolves available XDF, preferred JSON event log, channel map, run UUID, protocol schema, cue schedule, locked anchor, and recorded branch videos.

Master Suite receives the compatible raw-run and stimulus inputs. Chain, HOC-R, and confound tools receive only a validated matching canonical core. Visualizer receives a compatible review folder plus available XDF, event log, and Target video. Interpreter receives the preferred compatible chain or core folder. ALS Barcode Detector receives the selected run and exact available timing artifacts.

Core/run matching uses the exact XDF and event paths in `config/run_config.json`; chain/core matching uses `chain_manifest.json`. Multiple plausible inputs are surfaced for manual resolution. New core outputs receive a snapshot of `PRAYCG_ActiveResearchContext_v1_0.json`, and the chain carries it forward.

All launches remain review-first. Prefill does not click Run or begin analysis automatically. Buttons whose prerequisites are unresolved are disabled, and the readiness view explains the missing or conflicting input.

The v0.92 integration also repaired GUI argument transfer in MediaPrep and Master Suite, including the visible Feature Table CSV field, and added prefill support to chain, HOC-R, confound, ALS Barcode, Visualizer, and Interpreter interfaces.

## Why the structural-control and confound additions matter

### ShotOrder structural control

Phase scrambling disrupts low-level spatial organization but also destroys faces, bodies, objects, biological motion, local action, and other high-order visual structure. A Target-versus-PhaseScrambled difference therefore cannot, by itself, distinguish response to low-level sensory organization from response to intact local content or to the larger temporal/narrative sequence.

ShotOrderScramble is intended to preserve local shots and much of their within-shot content while disrupting their global order. Used together, the controls support more informative contrasts:

- **Target versus PhaseScrambled:** intact stimulus structure versus strongly degraded spatial structure;
- **Target versus ShotOrderScramble:** intact global order versus preserved local content in disrupted order; and
- **Target versus Override:** nominally matched media with altered cue or instruction context, subject to spatial-attention and order checks.

This is an identification strategy, not proof of narrative meaning. Shot segmentation, edit boundaries, audio treatment, transition artifacts, unequal familiarity, and residual low-level differences can still confound the comparison and require media QC.

### ShotOrder HOC-R analysis

ShotOrder HOC-R places Target, PhaseScrambled, ShotOrderScramble, and Override branches into a common four-branch audit across available PRAYCG measures. Its purpose is to ask whether a Target-associated pattern remains after considering low-level degradation, preserved local content with disrupted order, and the Override condition.

The strongest future use is at prospectively locked anchors with adequate timing, acquisition eligibility, artifact review, multiplicity control, and the broader confound gates already passed. HOC-R is not causal residualization in the strong experimental or econometric sense unless its design assumptions are met. A favorable pattern should be described as surviving the implemented audit, not as proving narrative reception or mechanism.

### Expanded confound defenses

The chained confound layer asks whether an apparent Target effect has plausible alternatives:

- **HOC-R:** high-order stimulus structure and branch-specific residual patterns;
- **OSA:** cue-driven gaze, upper-right spatial attention, or area-of-interest burden;
- **OHC:** fixed order, later exposure, habituation, repetition suppression, and carryover;
- **AAM:** cumulative recovery, Target-afterglow-like patterns, task completion, or relief; and
- **RespDualPath:** respiration as contamination of other signals versus respiration as a genuine but nonspecific state event.

These modules strengthen criticism and attribution discipline. They cannot establish that all confounds have been measured or eliminated. Missing inputs, weak measurement, collinearity, fixed branch order, small samples, or post hoc anchor choice can still make a result non-identifiable.

## ALS timing, holder placement, and location testing

The current ALS stack separates four related tasks:

1. **Runner timing:** PRAYCG2.2 presents the physical-screen barcode and records scheduled and observed presentation events.
2. **Holder calibration:** `control_center/scripts/praycg_als_holder_calibration_v0_8.py` aligns the PT19 sensor aperture with the intended screen rectangle and can save a placement profile.
3. **Per-session placement/location validation:** `control_center/scripts/praycg_acquisition_preflight_v1_0.py` runs the optional 30-second EEG/ALS validation, presents repeated long/short lower-right pulses, and tests whether the live ALS stream can distinguish them at the recorded screen location.
4. **Post-run detection:** `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_als_barcode_detector_v1_5_8.py` evaluates recorded timing data.

The optional placement/location report records screen resolution, estimated physical dimensions, pixels per inch, the exact barcode rectangle and pulse schedule, stream names, holder-profile path and hash, robust black/white span, noise estimate, contrast-to-noise ratio, transition count, plateau fractions, candidate polarity, and pulse-visibility status.

The runner overlay should align with the sensor aperture, not merely the center of the holder flange. The holder must still be inspected physically. A software pass cannot prove that the aperture remained seated during a run, exclude room-light leakage, guarantee unchanged monitor scaling, or substitute for an independent TTL/photodiode reference.

ALS measures the physical display-input path. It is not a biological channel or endpoint.

## Current v0.92 component matrix

| Component | Version or schema | Public role |
|---|---:|---|
| PRAYCG Control Center | v0.92 | Dashboard, process control, context resolution, and launcher integration |
| Active Research Context | v1.0 | Provenance-aware stimulus/run/core/chain/review state |
| Protocol Runner | PRAYCG2.2 | Versioned event timing, run lifecycle, input hashes, and ALS overlay |
| MediaPrep / Stimulus Fingerprint | v1.9 ShotOrder | Media preparation, QC artifacts, structural-control generation, and GUI prefill |
| Master Comprehensive Suite core | v1.6.0 | Canonical analysis frame, eligibility gates, recovery phase, and core outputs |
| Master Suite chain | v1.6.1 | Dependency-aware modules, authoritative manifest, and artifact index |
| MasterSync Visualizer | v1.4.0 | Gate-aware interactive timeline and branch review |
| Offline Master Interpreter | v1.6.0 | Evidence ledger and technical/research/public-safe reports |
| Analysis Artifact Index | v1.0 | Exact-filename, hash, status, and duplicate provenance |
| BrainFlow EEG-only bridge | v1.1 | Typed EEG acquisition and diagnostics |
| BrainFlow EEG+ALS bridge | v1.5 | Typed EEG/AUX/ALS acquisition and diagnostics |
| Acquisition Diagnostics Core | v1.0 | Shared rate, timestamp, packet, missingness, and QC logic |
| Optional Acquisition Preflight | v1.0 | Separate 30-second signal and ALS placement/location validation |

## Installation and first use

1. Download and verify `PRAYCG_ControlCenter_v0_92_Public.zip` against the SHA-256 value above.
2. Extract the complete archive to a normal local folder. Do not run it from inside the ZIP preview.
3. Install Python 3.11 if needed.
4. Run `INSTALL_PRAYCG_REQUIREMENTS_v0_92.bat` once.
5. Run `run_PRAYCG_ControlCenter_v0_92.bat`.
6. In Settings, select **Use Bundled Paths**, configure external applications, and save.

PsychoPy and LabRecorder are external applications and are not included. Hardware acquisition also requires the relevant device, driver, dependencies, correct COM port, and exclusive access to that port.

For a new session, save or confirm the ALS holder profile, start the appropriate BrainFlow bridge, run the optional 30-second acquisition/placement validation, and inspect its report. This test is advisory and independent of runner arming.

For analysis, select the source run and create the canonical v1.6.0 core output first. Run the v1.6.1 chain on that matching core output, then use the compatible review folder with Visualizer or Interpreter. Prefilled values must still be reviewed before Run is clicked.

## Verification recorded for v0.92

The v0.92 release record reports:

- successful parsing of all bundled Python files;
- 13 focused unit and regression tests, including inherited analysis/review tests and new context-resolver tests;
- command-line argument checks for Master Suite, chain, HOC-R, ALS Barcode, Visualizer, Interpreter, and confound launch paths;
- a visible-interface construction smoke test confirming that launched tools receive genuine per-row Close controls; and
- a public-package scan excluding XDF, audio/video, generated logs, caches, and local settings.

Earlier v1.6.0 validation also included a complete Arrival test run and a full chain with zero `SOFTWARE_ERROR` states. Participant data and generated validation outputs are not distributed in the public archive.

These checks establish limited software behavior in the tested environment. They are not a substitute for independent code review, broader platform testing, hardware fault injection, prospective preregistration, blinded replication, or scientific validation.

## Public-package contents and exclusions

The public archive contains current software, configuration templates, dependency lists, component documentation, and ALS holder source/profile scaffolding.

It intentionally excludes:

- participant data and private biosignals;
- copyrighted stimulus audio or video;
- credentials and local machine settings;
- generated logs, analysis products, and validation outputs;
- Python cache files; and
- superseded Control Center, launcher, and component copies.

Users must supply media they are legally permitted to use and must protect participant information under their applicable ethics, consent, institutional, and legal requirements.

## Licensing

This repository uses a mixed-license layout. A more permissive license applying to one part of the repository does not relicense material governed by another category or by a third-party source license.

1. Code in `software/` and upload scripts is released under the MIT License unless an individual file states otherwise.
2. Repository documentation in `docs/`, templates, and non-personal example metadata are released under the Creative Commons Attribution 4.0 International license (CC BY 4.0) unless an individual file states otherwise.
3. Synthetic demonstration media in `examples/no_copyright_media_demo/` is released under CC0 1.0 Universal.
4. Third-party media generated or obtained through recipe scripts remains governed by the original source license. For the included Sintel recipe, users must follow the Creative Commons Attribution 3.0 license and applicable Blender Foundation attribution requirements.
5. Derived self-run example data are shared only as public-safe pilot examples. They must not be represented as clinical, diagnostic, or confirmatory data.

### MIT License for code

Copyright (c) 2026 Hoyt Banks

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Known limitations and non-claims

- The software is Windows-focused and has not been represented as comprehensively validated across operating systems, Python environments, displays, acquisition boards, or driver versions.
- The optional contact index, acquisition preflight, and ALS pulse-visibility result are transparent engineering heuristics, not impedance measurements, medical scores, or guarantees of valid acquisition.
- Automated provenance reduces accidental folder mismatches but cannot establish that the selected run, stimulus, condition labels, anchors, or sidecars are scientifically correct.
- `PASS` means that the implemented check passed; it does not mean that every relevant artifact, confound, bias, or alternative explanation was excluded.
- Exploratory metrics and module-derived composites are not validated biomarkers.
- Cross-run compatibility review does not justify automatic effect pooling.
- ShotOrder, PhaseScrambled, and Override contrasts improve the design's ability to examine alternatives but do not by themselves identify narrative meaning or a biological mechanism.
- Self-report is contextual evidence and not proof of an internal state.
- The package is not a medical device and is not intended for diagnosis, treatment, or clinical decision-making.

## Suggested citation

Until an OSF DOI or other persistent identifier is assigned, cite the approved author, exact software version, repositories, and archive hash:

> Banks, H. (2026). *PRAYCG Control Center v0.92: Public release history and cumulative research-software package* (Version 0.92) [Computer software]. GitHub: [hbanks87/praycg-open](https://github.com/hbanks87/praycg-open). OSF project 8n75v: [public project view](https://osf.io/8n75v/overview?view_only=928f1fa1974b40e89252101d0ba356d3). SHA-256: 936FA07D09136FFEE5EF6018DD0A892091983167A4A585FE12B16E38243FD58C.

After an OSF DOI is minted, add it to the citation while retaining the version number and archive hash so the cited software state remains identifiable.

## Publication metadata

The following publication metadata has been supplied:

- **Approved author:** Hoyt Banks
- **Contact:** [hoytbanks@gmail.com](mailto:hoytbanks@gmail.com)
- **GitHub repository:** [https://github.com/hbanks87/praycg-open](https://github.com/hbanks87/praycg-open)
- **OSF project ID:** `8n75v`
- **OSF public view:** [https://osf.io/8n75v/overview?view_only=928f1fa1974b40e89252101d0ba356d3](https://osf.io/8n75v/overview?view_only=928f1fa1974b40e89252101d0ba356d3)
- **OSF DOI:** https://doi.org/10.17605/OSF.IO/8N75V
- **Code license:** MIT License, unless a file states otherwise
- **Documentation license:** CC BY 4.0, unless a file states otherwise
- **Synthetic demonstration-media license:** CC0 1.0 Universal
- **Third-party media:** original source license and attribution requirements remain controlling

Before publication, complete or confirm the remaining fields as applicable:

- author affiliation, if one should be displayed;
- ethics, data-availability, and media-licensing statements appropriate to any separately deposited dataset.
