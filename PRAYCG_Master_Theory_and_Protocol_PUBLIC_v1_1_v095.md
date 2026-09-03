# PRAYCG Master Theory and Protocol

**Public-Safe GitHub/OSF Release Draft v1.1**  
**Aligned software package:** PRAYCG Control Center v0.95 Public  
**Author:** Hoyt Banks  
**Document status:** exploratory methods architecture; not clinical, diagnostic, commercial, metaphysical, or confirmation-grade evidence.  
**Intended repository location:** `docs/PRAYCG_Master_Theory_and_Protocol_PUBLIC_v1_1_v095.md`

---

## Document status and claim boundary

PRAYCG is an exploratory psychophysiology protocol and open-source software architecture for studying whether naturalistic narrative stimuli produce measurable EEG/autonomic state trajectories beyond low-level sensory entrainment and beyond analytic task demand.

This document updates the earlier public master theory/protocol document to match the v0.95 software line. Version 0.95 turns PRAYCG from a single evolving protocol into a modular protocol-library and analysis workbench. It adds a clearer prospective-study pathway, continuous autonomic arrays, CAI/SID as a bounded state-integration analysis, and Micro Handoff as an isolated exploratory raw-EEG timing probe.

This document does **not** claim that PRAYCG proves:

- consciousness;
- the soul;
- love as a physical force;
- clinical efficacy;
- diagnosis or treatment capability;
- microtubular memory;
- biophotonic memory;
- Opto-Structural Memory biology;
- quantum biology;
- hidden molecular variables from scalp EEG;
- literal thermodynamic heat, ATP flow, or molecular substrate changes from EEG/HRV alone.

Current permitted claim:

> PRAYCG is an open, auditable naturalistic-stimulus protocol and analysis workbench for studying sensory entrainment, narrative reception, analytic task stance, artifact/confound structure, autonomic dynamics, and delayed after-state patterns under explicit quality gates.

Current evidentiary status:

> pilot, software-validation, and methods-development evidence only. Existing self-runs are scientifically useful as calibration and hypothesis-generation cases, but they are not confirmation-grade evidence.

---

# 1. Executive summary

PRAYCG asks a narrow question hidden inside a broad human intuition:

> When a story is allowed to matter, does the body-brain system show a measurable state trajectory that differs from the same audiovisual material with recognizable meaning damaged, and from the same intact story watched under analytic task demand?

The v0.95 public package supports three protocol families:

- **PRAYCG3 v3.0:** the standard three-branch protocol: PhaseScrambled Control, Target, Contextual Override.
- **PRAYCG4 v4.0:** a four-branch protocol that adds ShotOrderScramble as a high-order structural control.
- **SMG v1.0:** a separate Semantic Meaning Gradient protocol for comparing coherent low-meaning material with high-meaning narrative material and analytic override.

The practical contribution is a reproducible pipeline:

1. legally source a stimulus;
2. prepare Target, Override, PhaseScrambled Control, and optionally ShotOrderScramble media;
3. generate cue schedules, timing/QC files, anchor templates, and stimulus fingerprints;
4. record EEG, autonomic, respiration, ALS/photodiode, and marker streams through LSL and LabRecorder;
5. run the Master Comprehensive Analysis Suite;
6. generate time-resolved feature tables, event tables, branch summaries, visualizations, and offline plain-English reports;
7. keep strong claim boundaries and explicit falsification paths.

The current theoretical compression is:

> PRAYCG is a theory of availability: whether a living system is available to access, decode, receive, and integrate a meaningful perturbation under controlled sensory, task, and confound conditions.

---

# 2. Why PRAYCG exists

Everyone already knows that stories can move people. PRAYCG is not trying to prove that a person can understand a movie.

The scientific problem is different: naturalistic stimuli drive the nervous system through many overlapping channels at once. A film contains luminance changes, motion, cuts, faces, bodies, speech rhythm, audio envelope, music, semantic content, expectation, memory, autobiographical relevance, task demands, emotion, and artifact opportunities such as blinks, jaw tension, squinting, and posture shifts.

A loose interpretation - "the subject watched the movie and the brain responded" - is not enough. PRAYCG tries to separate layers:

1. **Exogenous sensory entrainment:** the nervous system follows physical features of the stimulus.
2. **High-order local structure:** the nervous system responds to faces, bodies, objects, biological motion, and intact shots.
3. **Semantic/narrative reception:** the participant receives coherent meaning, not merely sensory rhythm or local shot content.
4. **Analytic extraction:** the same narrative is processed under task demand.
5. **Integration/after-state:** the body-brain state after the stimulus may carry forward differently than during the stimulus.
6. **Gate availability:** a meaningful response may require both external access and an internal decoder state.

The core logic is not anti-neuroscience. It treats sensory entrainment, artifact, respiration, task load, order, and carryover as the first critiques that any interpretation must survive.

---

# 3. Public naming and acronym boundary

PRAYCG / PR-AYC-G began as a working codename inside a broader theoretical project. For the public open-source release, the acronym should be treated primarily as a project label.

The empirical object is not the acronym. The empirical object is the protocol system:

```text
baseline -> controlled stimulus branches -> washouts -> reports -> final reflection baseline -> analysis gates
```

A suitable public title is:

> **PRAYCG: An Open Psychophysiology Pipeline for Testing State-Locked Narrative Meaning Beyond Sensory Entrainment and Analytic Task Demand**

---

# 4. v0.95 development map

The v0.95 software line should be understood as an operational platform update, not an empirical validation claim.

## 4.1 Major development stages

- **v0.7:** added runner-generated ALS/photodiode barcode timing and improved timing-event registration.
- **v0.8:** added ShotOrderScramble stimulus generation, HOC-R support, and ALS holder calibration.
- **v0.81-v0.86:** repaired Windows launch issues, MediaPrep dependencies, MoviePy/NumPy audio handling, visible logs, process monitoring, per-tool shutdown, and public packaging.
- **v0.87-v0.92:** added canonical analysis frames, eligibility gates, explicit missingness, selected-folder propagation, improved visualization/interpreter status, and process controls.
- **v0.93:** introduced a plug-and-play protocol library.
- **v0.94:** added CAI/SID v0.2, continuous autonomic arrays, readiness checks, and prospective protocol templates.
- **v0.95:** added Micro Handoff v0.1 as an isolated exploratory raw-EEG module with synthetic acceptance tests, frozen hashes, historical auditing, and no effect on primary Master Suite eligibility.

## 4.2 What v0.95 changes conceptually

v0.95 does not make PRAYCG more aggressive. It makes PRAYCG more disciplined.

The major conceptual upgrades are:

- protocol identity is versioned and locked rather than informal;
- missing or bad data stays missing rather than being turned into a favorable score;
- autonomic data are represented as continuous arrays rather than only branch averages;
- CAI/SID is bounded as a state-integration density proxy, not a consciousness detector;
- Micro Handoff is isolated from the primary chain and labeled software-valid but construct-unvalidated;
- prospective variants are separated from retrospective pilot interpretation.

---

# 5. Theory in one page: meaning as gated interaction

The simplest model is too weak:

```text
stimulus -> meaning response
```

PRAYCG instead models meaning as an interaction:

```text
external semantic access
+ internal decoder availability
+ regulatory state
+ low enough task/confound burden
-> possible recognition and integration
```

A compact working form is:

```text
MR(t) = D_gate(t) * sim(phi(u(t)), P(t))
```

Where:

- `MR(t)` is a meaning-recognition proxy;
- `u(t)` is the external stimulus vector;
- `phi(u(t))` is the encoded sensory-semantic structure of the stimulus;
- `P(t)` is the participant's persistent learned state-space / prior model / attractor structure;
- `sim()` is a similarity or fit function;
- `D_gate(t)` is decoder-gate availability.

`D_gate(t)` is not a mystical variable. It is a practical gate:

```text
D_gate(t) increases when:
  audio is audible,
  visual access is adequate,
  the participant understands the context,
  fatigue is low,
  task burden is low,
  artifact/confound burden is low,
  and the stimulus matches available prior structure.

D_gate(t) decreases when:
  the participant cannot hear the dialogue,
  the video is confusing or unfamiliar in the wrong way,
  the participant is distracted,
  environmental noise intrudes,
  arithmetic/override burden dominates,
  or the branch is contaminated by artifact.
```

A meaningful stimulus can fail to generate a measurable response if the gate is closed. A low-bandwidth cue can generate a large response if it unlocks an already-structured prior state. This is the core of the current Decoder Gate Availability interpretation.

---

# 6. Availability under load

The earlier theoretical language can be reduced to a public-safe availability model:

```text
Availability under load
  ~ (coherence * adaptive update capacity * persistence)
    / (1 + mismatch + metabolic/executive load + artifact/confound burden)
```

This is not a biological law. It is an organizing model.

- **Coherence** means the system is organized enough to respond rather than scatter.
- **Adaptive update capacity** means the system can let new information matter.
- **Persistence** means the system can remain stable long enough for integration or after-state to occur.
- **Mismatch** means threat, contradiction, confusion, or model violation.
- **Load** means task effort, fatigue, defensive pressure, sensory burden, or metabolic/executive cost.
- **Artifact/confound burden** means signals that can mimic or obscure physiology.

PRAYCG does not claim to measure all of these directly. It operationalizes pieces of them through EEG, HR/HRV, respiration, stimulus features, task reporting, self-report, and QC flags.

---

# 7. Protocol families in v0.95

## 7.1 PRAYCG3 v3.0: standard three-branch protocol

PRAYCG3 is the current public continuation of the original three-prong protocol.

```text
Baseline 1
-> PhaseScrambled Control
-> Washout/report
-> Target
-> Washout/report
-> Contextual Override
-> Washout/report
-> Baseline 2 / final reflection
-> Final report
```

Primary questions:

- Does Target differ from a meaning-damaged sensory control?
- Does Target differ from the same intact stimulus under analytic task stance?
- Does any after-state persist into washout or Baseline 2?
- Does the interpretation survive timing, artifact, respiration, task, and self-report confounds?

The fixed-order PRAYCG3 protocol remains useful for feasibility and software validation. For confirmation-grade claims, fixed order must eventually be replaced or supplemented by counterbalanced designs.

## 7.2 PRAYCG4 v4.0: ShotOrder structural-control protocol

PRAYCG4 adds a ShotOrderScramble branch after the PhaseScrambled branch.

```text
Baseline 1
-> PhaseScrambled Control
-> Washout/report
-> ShotOrderScrambled Structural Control
-> Washout/report
-> Target
-> Washout/report
-> Contextual Override
-> Washout/report
-> Baseline 2 / final reflection
-> Final report
```

Why PRAYCG4 exists:

- PhaseScrambling damages narrative order, but it also damages high-order local structure.
- A Target-vs-Phase contrast cannot by itself separate narrative reception from face, body, object, or biological-motion processing.
- ShotOrderScramble preserves local shots more than PhaseScrambling while disrupting cross-shot narrative order.

ShotOrderScramble is not a perfect control. It can introduce abrupt discontinuities, altered cut rhythm, confusion, expectancy violations, and familiarity effects. Its value is that it adds a structurally informative middle control.

The future stronger contrast pattern is:

```text
Target > PhaseScrambled
Target > ShotOrderScrambled
Target > Contextual Override
```

at locked anchors and/or validated after-state windows, after timing, artifact, stimulus, task, gaze, respiration, and order/carryover gates.

## 7.3 SMG v1.0: Semantic Meaning Gradient

SMG is a separate protocol family.

```text
Semantic-Zero
-> High-Meaning Target
-> Arithmetic Override
```

Semantic-Zero should be coherent but low in intended narrative meaning. It should not simply be random noise. Randomness can create novelty, threat, prediction error, or puzzle demand.

Candidate semantic-density factors include:

- human or social presence;
- agency;
- vulnerability;
- causal continuity;
- repair/care structure;
- stakes;
- transformation;
- penalties for puzzle demand, overload, or confusion.

SMG indices and thresholds are unvalidated candidates. They are protocol-development tools, not diagnostic instruments and not proof of objective meaning.

---

# 8. Branch doctrines

## 8.1 PhaseScrambled Control doctrine

The PhaseScrambled Control should not be described as physiologically meaningless. It is a meaning-damaged sensory-control branch.

It may still produce:

- visual entrainment;
- auditory envelope tracking;
- confusion;
- boredom;
- scanning effort;
- artifact;
- low-level affect;
- sensory burden.

Correct claim:

> Control preserves aspects of sensory drive while damaging recognizable narrative meaning.

Incorrect claim:

> Control is physiologically meaningless.

## 8.2 ShotOrderScramble doctrine

ShotOrderScramble is a high-order structural-control branch. It detects local shots, permutes their order, and reassembles the video.

Its purpose is to preserve more local visible structure than PhaseScrambling:

- faces;
- bodies;
- objects;
- local motion;
- local speech fragments if audio is paired;
- intact shot-level image statistics.

But it disrupts the larger narrative sequence.

Correct claim:

> ShotOrderScramble makes Target effects less reducible to local face/object/biological-motion structure alone.

Incorrect claim:

> ShotOrderScramble definitively isolates meaning.

## 8.3 Target doctrine

Target is the intact stimulus watched naturally. It should be interpreted only in contrast to controls and confounds. A strong Target response is not sufficient by itself.

## 8.4 Contextual Override doctrine

Contextual Override uses the same intact cue-embedded stimulus as Target, but with an analytic task stance. In the default implementation, participants perform a running-sum number-cue task.

A Target-vs-Override difference supports the hypothesis that task stance matters. It does not automatically prove that Target is meaning and Override is non-meaning. Override changes attention, gaze, working memory, arithmetic load, cue monitoring, and potentially emotional availability.

---

# 9. Counterbalancing and Williams-sequence variants

Fixed branch order is useful for preserving novelty in early self-runs, but it creates order confounds:

- first exposure;
- repetition suppression;
- learning;
- fatigue;
- boredom;
- task carryover;
- long-memory carryover.

The v0.95 prospective package separates fixed legacy protocols from counterbalanced study candidates.

PRAYCG4 supports four sequence variants rotating PhaseScrambled, ShotOrderScrambled, Target, and Override. PRAYCG3 supports forward/reversed variants for the three-branch design. Williams-style balancing reduces systematic first-order order effects, but it does not eliminate fatigue, learning, long-memory carryover, or nonlinear sequence effects.

A confirmation-grade group study should use counterbalancing or a documented reason why novelty preservation requires a specific order.

---

# 10. Media procurement and stimulus selection

## 10.1 Legal and ethical sourcing

Public repositories should not include copyrighted stimulus media unless the media are legally shareable. The repository may include:

- code;
- templates;
- public-safe documentation;
- synthetic/demo fixtures;
- legally shareable media;
- derived reports without private biosignals.

It should not include:

- copyrighted film clips;
- private raw XDF recordings;
- unredacted self-report;
- local machine paths;
- credentials or tokens;
- private participant identifiers.

## 10.2 Practical stimulus criteria

A strong PRAYCG stimulus is usually:

- 2.5 to 5 minutes long;
- narratively self-contained enough to be understood;
- not so complex that unfamiliar viewers cannot access the scene;
- not so loud/chaotic that artifact and sensory overload dominate;
- capable of being phase-scrambled and shot-order-scrambled;
- legally usable under the intended private or public data policy;
- compatible with manual anchor locking.

## 10.3 Familiarity and decoder availability

Familiarity is not automatically bad. It changes the interpretation.

- Novel stimuli test first-pass reception.
- Familiar stimuli test reactivation, memory, and decoder-gate availability.
- Partially familiar stimuli require careful self-report and familiarity covariates.

PRAYCG should record familiarity and context because the same scene can function as a new stimulus for one participant and a memory key for another.

---

# 11. MediaPrep and stimulus generation

## 11.1 Standard MediaPrep outputs

A standard PRAYCG3/PRAYCG4 stimulus folder should contain:

```text
stimulus_master.mp4
stimulus_master_cleaned_*.mp4
stimulus_target_cued_*.mp4
stimulus_override_cued_*.mp4
stimulus_control_cued_phase_scrambled_*.mp4
optional stimulus_structural_control_cued_shot_order_scrambled_*.mp4
cue_schedule_*.json
cue_schedule_*.csv
media_prep_manifest_*.json
visual_QC_checklist_*.md
control_audio_QC_checklist_*.md
anchor templates / locked anchor files
stimulus fingerprint outputs
```

## 11.2 Critical MediaPrep rules

1. Target and Contextual Override should be generated from the same cue-embedded video.
2. Only participant instructions should differ between Target and Override.
3. Any watermark/source-stamp cleanup must be applied to the master before all branches are generated.
4. PhaseScrambled Control should be generated from the cue-embedded Target so cue timing and low-level cue energy remain represented.
5. ShotOrderScramble should normally be generated from the cleaned master first, then cued afterward with the same cue schedule.
6. Control audio must be manually QC-checked.
7. MediaPrep prepares stimuli; it does not certify meaning, task compliance, endpoints, or physiology.

## 11.3 Control audio QC

A control-audio pass requires:

- no recognizable spoken words;
- no intelligible sentence fragments;
- no distinct melody that carries narrative recognition;
- loudness/envelope that broadly tracks the original;
- human manual listening review.

Automated audio processing cannot certify unintelligibility.

## 11.4 Visual QC

A visual QC pass requires:

- Target and Override are viewable;
- cue badges are legible;
- no unexpected watermark/subtitle/source-stamp remains unless documented;
- cleanup was applied before branch generation;
- Target and Override remain bit-identical where required;
- Control was generated from the correct source;
- ShotOrderScramble was generated with a declared seed, shot table, and QC manifest.

---

# 12. Anchor doctrine

Anchors are predeclared time windows where a candidate recognition, integration, or resolution event is expected.

## 12.1 Anchor types

- **Primary A-MRED Peak anchors:** expected acute recognition/integration candidate.
- **Secondary context anchors:** useful for interpretation but not primary endpoints.
- **Resolution anchors:** expected delayed closure, repair, or after-state effects.
- **Clip-edge anchors:** anchors near the end of a clip that may require washout continuation rather than in-clip carryover.
- **Null or pseudo anchors:** timing-control windows used to test overfitting and false positives.

## 12.2 Strict anchor-lock workflow

1. Create draft anchors before the run.
2. Frame-verify anchor times on the final rendered Target MP4.
3. Freeze the locked anchor file before acquisition.
4. Record the locked anchor hash in the run configuration.
5. Treat estimated-time anchors as pilot-only.
6. Treat post-hoc anchors as exploratory.

Anchor registration freezes timing hypotheses. It does not certify MRED, CAI/SID, Micro Handoff, memory formation, consciousness, or mechanism.

---

# 13. Hardware and acquisition architecture

## 13.1 Core hardware

The current PRAYCG acquisition stack can include:

- OpenBCI Cyton + Daisy EEG;
- BrainFlow bridge;
- Lab Streaming Layer markers;
- LabRecorder XDF capture;
- ALS/PT19 or equivalent light sensor;
- Polar H10 RR interval stream;
- Vernier Go Direct Respiration Belt;
- optional shielding / controlled acquisition environment.

Future confirmation-grade work should add:

- EOG;
- EMG for jaw/forehead/temporal muscles;
- motion sensors;
- eye tracking or gaze proxy;
- independent stimulus display timing validation.

## 13.2 EEG stream

OpenBCI data should be treated as useful but artifact-sensitive. Gamma-band interpretations require special caution because jaw, eye, forehead, temporal muscle, and movement artifacts can produce high-frequency energy.

The v0.95 BrainFlow bridges are intended to preserve board/device timestamps separately, reconstruct sample timestamps consistently, track duplicates/out-of-order packets, retain nonfinite values as missing, and generate shutdown-safe QC reports.

## 13.3 ALS/PT19 physical timing channel

The ALS/PT19 channel validates physical display timing. It should not be interpreted as a biological signal.

v0.95 continues the runner-side barcode doctrine:

```text
software marker time
+ runner-rendered barcode
+ ALS sensor observation
-> stronger display-onset timing confidence
```

The embedded MP4 barcode is a backup. The primary timing channel should be the runner-side physical-screen barcode, calibrated to the actual sensor holder.

A good ALS pulse does not prove good EEG. Good EEG contact does not prove ALS visibility. Good timing does not prove interpretation.

## 13.4 Polar H10

In the current PRAYCG stack, Polar H10 is used primarily as an RR interval source for HR/HRV analysis. It should not be described as a full clinical ECG waveform in this setup unless a true ECG stream is acquired.

## 13.5 Vernier respiration belt

The Vernier respiration belt should be treated as a raw respiration movement stream. The raw force channel is preferred for offline inhale/exhale phase reconstruction. Built-in respiration-rate channels may be delayed or initially unavailable, so they should not be the sole respiration representation.

---

# 14. Protocol runner and Control Center

## 14.1 Control Center purpose

The Control Center is an orchestrator, not a proof engine. It provides one front door for:

- stimulus library management;
- MediaPrep launch;
- ShotOrderScramble launch;
- acquisition stream launchers;
- ALS holder calibration;
- LabRecorder and PsychoPy launch support;
- protocol-library selection;
- analysis suite launch;
- visualizer launch;
- offline interpreter launch;
- process monitoring and shutdown.

The Running Tools panel matters because orphaned acquisition tools can occupy hardware connections, continue publishing stale LSL streams, or make output provenance ambiguous.

## 14.2 Protocol-library lock model

The v0.95 protocol library separates protocol selection from protocol execution. A proper lock records:

- protocol ID and version;
- exact ordered branch list;
- SHA-256 of the protocol manifest;
- SHA-256 and path of the runner entry file;
- scientific boundary statement.

This lock prevents accidental configuration drift. It does not prove causal identification or acquisition validity.

---

# 15. Self-report and neurophenomenology

Self-report is not proof of internal state or mechanism. It is also not optional noise.

PRAYCG treats first-person reports as independent evidence streams. They can:

- converge with physiology;
- diverge from physiology;
- reveal confounds;
- explain decoder-gate closure;
- identify task burden;
- constrain interpretation.

Self-report should include, at minimum:

- meaning;
- absorption;
- emotional afterglow;
- story active during washout;
- task extraction load;
- confound burden;
- audio comprehension;
- cue legibility;
- eye strain/squint;
- external noise;
- familiarity;
- final comparative branch choices.

The boundary is:

> self-report contextualizes physiology; it does not prove consciousness, mechanism, or neural state by itself.

---

# 16. Master Comprehensive Analysis Suite v0.95 posture

The Master Suite should be understood as a layered falsification and interpretation system.

It does not ask: "Did Target win?"

It asks:

```text
Was timing good enough?
Was EEG usable?
Were artifacts low enough?
Was respiration measured?
Was the branch correctly identified?
Were anchors locked?
Did Target differ from sensory control?
Did Target differ from structural control?
Did Target differ from task stance?
Did after-state persist?
Do self-reports support access?
Do nulls and pseudo-events constrain overfitting?
```

## 16.1 Updated module tier map

### Primary/core path

- run provenance and file-hash checks;
- timing and ALS barcode QC;
- EEG stream QC and channel-map status;
- artifact sentinels;
- stimulus fingerprinting / CET-R;
- A-MRED;
- MRED-Peak;
- MRED-Resolution;
- reportable decision gates.

### Secondary interpretation layer

- DGA: Decoder Gate Availability;
- NUPI: Narrative Update Polarity Index;
- TTI: Target-vs-Task/Override attenuation;
- HOC-R: High-Order Control Residualization;
- OSA: Override Spatial Attention;
- OHC: Order/Habituation/Carryover;
- AAM: Afterglow Attribution Model;
- RespDualPath;
- CAA: Continuous Autonomic Arrays;
- CAI/SID: Controlled Access-Integration / State Integration Density.

### Exploratory / convergence layer

- KHT-topo and hidden-loop candidates;
- Topo-OSM network-state summaries;
- Micro Handoff v0.1;
- OCU / blink-unloading markers;
- additional experimental modules.

Exploratory modules must not alter primary eligibility or conclusions unless promoted through prospective validation.

---

# 17. Core analysis modules retained from v1.0

## 17.1 ArtifactScore

ArtifactScore estimates whether a candidate signal may be explained by eye, jaw, muscle, movement, line noise, or gross voltage instability. ArtifactScore should function as a veto or caution layer, not a cosmetic annotation.

## 17.2 GammaScalpel / lower-gamma work-signal proxy

GammaScalpel subdivides lower gamma or high-frequency bands into smaller regions and evaluates spatial pattern, power, phase-locking, and artifact sentinels.

Boundary:

> gamma is a candidate work-signal proxy, not a meaning biomarker.

## 17.3 TSP: Temporal Semantic Proxy

TSP is a time-resolved proxy for stimulus-linked recognition/access. It should be residualized against exogenous media structure when possible.

## 17.4 Theta handoff / integration proxy

Theta handoff is a delayed slower-band candidate for integration, sequencing, or after-state organization. It does not prove memory formation.

## 17.5 MRED

MRED means Meaning Recognition / Encoding Dissociation. It asks whether recognition-like events and integration-like after-state features can separate.

Possible patterns:

- high recognition / high integration;
- high recognition / low integration;
- low recognition / high delayed after-state;
- low recognition / low integration;
- confounded or unavailable.

## 17.6 A-MRED

A-MRED is the anchor-locked version of MRED. It requires predeclared anchors, valid timing, appropriate windows, and artifact/QC gates.

## 17.7 MRED-Peak and MRED-Resolution

MRED-Peak captures acute event-like recognition/integration candidates. MRED-Resolution captures slower reflective or regulatory after-state patterns.

This distinction is crucial because not all meaning behaves like an impact. Some meaning behaves like closure.

---

# 18. Expanded confound defenses

## 18.1 HOC-R: High-Order Control Residualization

HOC-R asks whether apparent Target effects are explainable by high-order local structure such as faces, bodies, objects, biological motion, shot content, speech fragments, or local area-of-interest features.

ShotOrderScramble makes HOC-R more meaningful by adding a branch that preserves more local structure than PhaseScrambling.

## 18.2 OSA: Override Spatial Attention

OSA asks whether Override differs from Target because the participant is monitoring the cue region, shifting gaze, squinting, or allocating attention away from the narrative event.

Target/Override hash identity is necessary but not sufficient. Identical video files can still be sampled differently by the viewer.

## 18.3 OHC: Order/Habituation/Carryover

OHC treats washout as measured after-state, not proof of reset. It tracks position, repetition, fatigue, and prior-branch carryover.

## 18.4 AAM: Afterglow Attribution Model

AAM asks whether Baseline 2 resembles Target afterglow, Override task-completion relief, fatigue, or mixed carryover.

## 18.5 RespDualPath

RespDualPath separates respiration as:

- a valid autonomic state signal;
- a potential contaminant of EEG/HRV interpretation.

A sigh may be meaningful physiology and an artifact risk at the same time.

## 18.6 DGA: Decoder Gate Availability

DGA explains why a stimulus can be meaningful in principle but unavailable in practice. DGA is especially important when audio clarity, familiarity, fatigue, noise, or task load changes between branches.

## 18.7 CET-R: Cinematic Entrainment residualization

CET-R asks whether candidate signals are explained by measurable exogenous stimulus features such as luminance, audio envelope, motion, cuts, cue timing, or detected shot structure.

Residual variance is not automatically meaning. It is only what remains after modeled alternatives are removed.

---

# 19. CAI/SID v0.2: Controlled Access-Integration / State Integration Density

## 19.1 Naming boundary

For public use, CAI should mean:

> **Controlled Access-Integration Index**

not "consciousness access meter."

SID means:

> **State Integration Density**

CAI/SID estimates whether a time window shows coordinated access-like and integration-like evidence under controlled conditions. It is not a probability, not a validated consciousness measurement, not a clinical score, and not proof of narrative reception.

## 19.2 Components

CAI/SID uses:

- fast access-like evidence;
- slower future integration-like evidence;
- positive-loop evidence;
- artifact penalties;
- task/extraction penalties;
- hard missingness for invalid windows.

DGA/contextual gating and continuous autonomic outputs are reported separately from the primary CAI score.

## 19.3 Fast component

```text
LE(t) = weighted_available(
          0.45*zMeaningGamma,
          0.35*zTSP,
          0.20*zNIP
        )
        - 0.10*max(zVisualGamma, 0)

E(t) = sigmoid(LE(t))
```

`E(t)` is a bounded access-like activation proxy. It is not a probability of consciousness.

## 19.4 Slow component

```text
LY(t) = 0.50*zThetaIntegration
      + 0.30*zNAS
      + 0.20*zPosteriorAlpha

Y(t) = sigmoid(LY(t))
```

`Y(t)` is a bounded integration-like state proxy. It does not prove memory formation.

## 19.5 Future integration window

```text
Y_future(t) = mean{Y(s): t+8 <= s <= t+30}
```

Rules:

- future windows must remain inside the same contiguous condition block;
- windows may not cross branch boundaries;
- missing windows remain missing;
- unavailable future data are not converted into favorable evidence.

## 19.6 Positive-loop correction

Jointly low fast and slow values cannot count as favorable evidence.

```text
e_plus(t) = max(E(t) - 0.5, 0)
y_plus(t) = max(Y_future(t) - 0.5, 0)

K_product(t) = 2 * sqrt(e_plus(t) * y_plus(t))
```

When local correlation is estimable:

```text
K(t) = 0.70*K_product(t) + 0.30*max(corr(E, Y_future), 0)
```

Otherwise:

```text
K(t) = K_product(t)
```

Non-estimable correlation is unavailable, not favorable.

## 19.7 Support, penalty, and core CAI

```text
Support(t) = mean(E_plus, Y_plus, K)
Penalty(t) = mean(A_plus, X_plus)
CAI_core(t) = Support(t) * (1 - Penalty(t))
```

Hard artifact, timestamp, high-frequency, or peak-to-peak failures make the window missing, not zero.

## 19.8 SID interval summary

```text
SID[a,b] = mean(CAI_core(t) over valid t in [a,b])
```

or in continuous notation:

```text
SID[a,b] = (1/(b-a)) * integral_a^b CAI_core(t) dt
```

The preferred public interpretation is:

> CAI/SID estimates whether a window shows coordinated access and delayed integration under quality-controlled conditions.

---

# 20. CAA v0.1 / Continuous Autonomic Arrays

## 20.1 Why CAA exists

Branch-level autonomic summaries are too coarse. Saying "Target HR was lower" or "Baseline 2 RMSSD was higher" is useful but incomplete.

CAA asks:

- when did HR change?
- did HRV rise before, during, or after a scene?
- was the HRV window long enough to trust?
- was the change respiration-driven?
- did a sigh or breath hold drive the result?
- did the final baseline resemble Target afterglow or task-completion relief?

## 20.2 Core autonomic vector

```text
A_auto(t) = [
  HR(t),
  IBI(t),
  RMSSD_W(t),
  SDNN_W(t),
  pNN50_W(t),
  Resp_z(t),
  RespPhase(t),
  BreathRate(t),
  RespDepth_z(t),
  RSA(t),
  RespRisk(t),
  Q_auto(t),
  R_auto(t)
]
```

## 20.3 Beat-event and HR formulas

For each RR interval:

```text
IBI_i = RR_i / 1000
HR_i = 60 / IBI_i
```

Physiologically implausible or abrupt beat intervals are flagged or removed depending on severity. Polar RR events are irregular beat events, not evenly sampled ECG waveforms.

## 20.4 Rolling HRV

Rolling HRV is not instantaneous. It is a windowed estimate.

```text
RMSSD_W(t) = sqrt(mean((IBI_i - IBI_{i-1})^2 in window W))
SDNN_W(t) = standard_deviation(IBI_i in window W)
pNN50_W(t) = fraction(|IBI_i - IBI_{i-1}| > 0.05 s in window W)
```

Recommended windows:

- 30 seconds: exploratory rapid RMSSD;
- 60 seconds: preferred continuous short-window HRV;
- 120 seconds: branch/washout/final-baseline compatible HRV.

## 20.5 Respiration arrays

Use the raw Vernier force channel:

```text
Resp_clean(t) = bandpass_0.05_to_1.0Hz(detrend(Resp_force_raw(t)))
Resp_z(t) = baseline_zscore(Resp_clean(t))
```

Respiration phase can be estimated by peak/trough detection or Hilbert phase:

```text
RespPhase(t) = angle(Resp_clean(t) + i*Hilbert(Resp_clean(t)))
```

For modeling, store both:

```text
sin(RespPhase(t))
cos(RespPhase(t))
```

## 20.6 Respiration events

CAA/RespDualPath should identify:

- breath holds;
- sigh-like depth events;
- abrupt respiration shifts;
- respiration artifact risk;
- respiration state-event candidates.

Core rule:

> A breath event can be preserved as physiology and penalized as possible artifact.

## 20.7 HR-respiration coupling

CAA should estimate whether HRV is respiration-driven:

```text
RSA_W(t) = local correlation or coherence between HR/IBI variation and respiration phase/depth
```

A large HRV increase that is fully explained by breathing should be interpreted differently from an HRV increase that persists after respiration modeling.

---

# 21. Micro Handoff v0.1

## 21.1 Status

Micro Handoff is an isolated exploratory raw-EEG module. It is not part of the primary Master Suite conclusion chain.

Current status:

> software-valid, construct-unvalidated, retrospectively mixed.

It does not prove discrete 40 Hz conscious frames, provide a consciousness RPM gauge, establish narrative meaning, or support clinical conclusions.

## 21.2 Plain-language purpose

Micro Handoff asks:

> Is a brief rise in temporal gamma activity followed shortly afterward by a rise in slower theta/integration-like activity?

It separates three quantities:

- **State coordination:** do fast and slow signals resemble each other?
- **Directional positive handoff:** does the fast signal rise first, followed by the slower signal?
- **Activation-weighted density:** are both signals meaningfully active rather than both low?

Low-low signals can resemble each other but should not count as positive handoff. Stationary high-high activity can contribute density but is not directional handoff.

## 21.3 Sampling and feature windows

Micro Handoff uses a 25 ms output grid, but not 25 ms spectral resolution.

- temporal gamma: T5/T6, 30-45 Hz, trailing 250 ms window;
- theta integration: Pz/P3/P4/T5/T6, 4-8 Hz, trailing 500 ms window;
- fixed lag bank: 100-1000 ms;
- Baseline 1 robust normalization only;
- no full-run normalization fallback;
- hard artifact and timestamp-gap windows are missing, not zero.

## 21.4 Core definitions

Baseline transform:

```text
z_B1(x_t) = 0.67448975 * (x_t - median_B1(x)) / MAD_B1(x)
```

Bounded activation proxies:

```text
F(t) = sigmoid(z_B1(log temporal-gamma power at t))
S(t) = sigmoid(z_B1(log theta-integration power at t))
```

Artifact quality:

```text
Q(t) = exp(-0.50 * max(Z_sentinel(t) - 2, 0))
     * exp(-0.15 * max(Z_global(t) - 4, 0))
```

Positive change evidence:

```text
O(t)      = clipped positive rise in fast activity
R(t,tau)  = clipped positive rise in slow activity at lag tau
```

Lag-wise outputs:

```text
C(t,tau) = state agreement
H(t,tau) = positive directional handoff evidence
D(t,tau) = activation-weighted coordination density
```

Primary candidate values are equal-weight means across the declared lag bank. No condition-specific winning lag is selected.

## 21.5 Synthetic and historical status

The v0.95 synthetic suite passed its declared tests, including known-lag recovery, low-low, stationary high-high, reverse-direction, independent, artifact, timestamp-gap, null, and deterministic-repeat behavior.

Historical retrospective evaluation was mixed. Only a subset of available recordings was computationally eligible with caution. Directional Target-minus-Control handoff was mixed around zero, no eligible recording passed both time-structure null families, and positive Target density was descriptive rather than a validated directional handoff.

Therefore Micro Handoff remains exploratory and isolated.

---

# 22. Visualizer and offline interpreter

## 22.1 Master Sync Visualizer

The visualizer is an audit artifact. It aligns selected stimulus video with processed signals, markers, and analysis overlays. It does not certify endpoints.

A useful v0.95 visualizer should show:

- stimulus video;
- EEG/MRED/CAI overlays;
- HR and HR baseline shift;
- rolling HRV and autonomic quality;
- respiration force and breath events;
- artifact/confound bands;
- branch and anchor markers;
- public/TSC mode versus lab diagnostic mode.

## 22.2 Offline interpreter

The offline interpreter converts module outputs into a structured human-readable report. It is rule-based. It is not an AI model and not a substitute for technical review.

Its best use is educational:

```text
This run is timing-cautioned.
This branch is audio-confounded.
This Target effect survives Control but not ShotOrder.
This Baseline 2 effect may be task relief rather than Target afterglow.
This gamma candidate overlaps artifact and should not be interpreted.
```

---

# 23. Baseline 2: promise and danger

Baseline 2 is one of the most interesting parts of PRAYCG and one of the easiest to overinterpret.

It can contain:

- Target afterglow;
- Override task-completion relief;
- fatigue;
- habituation;
- emotional carryover;
- respiratory settling;
- boredom;
- delayed autonomic recovery;
- memory reactivation.

Therefore Baseline 2 should be treated as cumulative after-state, not as Target-only evidence.

AAM and CAA exist partly to ask whether Baseline 2 resembles:

```text
post-Target washout,
post-Override relief,
respiratory shift,
fatigue,
or mixed carryover.
```

---

# 24. Pilot-derived archetypes

The current run archetypes are hypotheses, not validated classes.

## 24.1 Recognition-dominant / familiarity-limited

A run may show strong Target recognition-like activity without clean after-state integration. This may occur when the stimulus is recognizable, familiar, or cognitively salient but not deeply updating.

## 24.2 Peak-plus-late-density

A run may show a sharp MRED-like event plus a later continuous density region. This suggests that acute recognition and broader access-integration density may be distinct.

## 24.3 Resolution / afterglow density

A run may show modest in-clip impact but strong Baseline 2 or washout afterglow. This is compatible with closure or regulatory recovery, but requires AAM and RespDualPath caution.

## 24.4 Decoder-gate dissociation

A run may show large delayed physiology despite damaged sensory access or task interference. This should be interpreted through DGA: the stimulus may have served as a key to an already-structured prior state rather than simply transmitting meaning from scratch.

---

# 25. Topo-OSM, memory, and mechanism quarantine

PRAYCG can generate hypotheses about memory refresh, state persistence, and after-state dynamics. It cannot prove cellular memory biology from scalp EEG.

The safe public framing is:

> long-term memory and persistent meaning should be modeled as self-refreshing attractor dynamics distributed across structural state, synaptic/circuit activity, transcriptional or epigenetic bias, replay/reactivation, and behavioral context.

This framing does not require claiming that microtubules, biophotons, quantum biology, or any specific substrate has been demonstrated.

If OSM or related cellular hypotheses are discussed, they should remain in a quarantined mechanism layer:

- conditional;
- falsifiable;
- not inferred from PRAYCG alone;
- not promoted by EEG/HRV results;
- requiring independent cellular, molecular, or optical measurement.

---

# 26. Rung 0 / synthetic identifiability

Synthetic simulations are valuable because they test whether the software can detect known structures under controlled conditions.

They do not prove the biological target exists.

The correct interpretation is:

```text
Synthetic PASS:
  the algorithm can recover a planted pattern under declared conditions.

Synthetic FAIL:
  the algorithm cannot be trusted to test that pattern yet.

Synthetic PASS does not imply:
  human EEG contains that pattern,
  the biological mechanism is real,
  or the theory is confirmed.
```

This same boundary applies to Micro Handoff. Passing synthetic tests validates software behavior, not construct validity.

---

# 27. Confirmation-grade decision rule

A future confirmation-grade PRAYCG result must pass all of the following gates.

## 27.1 Stimulus and media gate

- legally sourced stimulus;
- validated MediaPrep output;
- Target/Override identity preserved where required;
- Control audio manually QC-checked;
- ShotOrderScramble QC completed if used;
- stimulus fingerprint generated.

## 27.2 Anchor gate

- predeclared anchors;
- local frame verification;
- locked anchor file hash recorded before run;
- pseudo/null anchors included when appropriate.

## 27.3 Timing gate

- LSL markers recorded;
- ALS/photodiode barcode passes;
- branch onset offsets inspected;
- clock/timestamp issues absent or explicitly cautioned.

## 27.4 Hardware gate

- EEG stream stable;
- channel map locked and confirmed;
- EOG/EMG or equivalent artifact controls present for gamma claims;
- Polar/Vernier streams valid when autonomic claims are made;
- no major acquisition dropout.

## 27.5 Confound gate

- audio/visual access adequate;
- environmental noise recorded;
- fatigue/discomfort recorded;
- cue legibility and squint recorded;
- task compliance recorded;
- respiration modeled;
- carryover/order assessed.

## 27.6 Analysis gate

- primary endpoints predeclared;
- exploratory modules separated;
- missing data not converted into favorable evidence;
- artifact/null/pseudo-event checks passed;
- results survive relevant contrasts.

## 27.7 Replication gate

- repeated across stimuli;
- repeated across sessions;
- tested across participants;
- analyzed without post-hoc tuning;
- ideally reviewed by external operators.

---

# 28. Prospective study roadmap

## 28.1 Stage 0: software/hardware reproducibility

Before biological claims, PRAYCG must show that another user can:

- install the Control Center;
- prepare media;
- run stream preflight;
- record XDF;
- generate analysis outputs;
- understand missingness and quality reports;
- reproduce the folder structure.

## 28.2 Stage 1: individual replication

Run repeated PRAYCG3 and PRAYCG4 sessions with:

- new stimuli;
- locked anchors;
- stable ALS barcode timing;
- CAA/CAI/SID outputs;
- Micro Handoff kept exploratory;
- strict confound reports;
- no post-hoc tuning.

## 28.3 Stage 2: small-N feasibility

Use counterbalanced or partially counterbalanced protocols. The goal is variance estimation, usability, and manipulation success, not proof.

## 28.4 Stage 3: prospective group study

A prospective group study should include:

- preregistered endpoints;
- multiple stimuli;
- group-level counterbalancing;
- EOG/EMG;
- eye tracking or gaze proxy;
- independent outcome measures;
- explicit nulls;
- external reproducibility.

---

# 29. File provenance and folder map

A recommended project root:

```text
PRAYCG_HOME/
  stimuli/
  runs/
  analysis/
  logs/
  config/
  protocols/
  docs/
```

Stimulus folder:

```text
stimuli/<stimulus_id>/
  master/
  mediaprep/
  anchors/
  fingerprint/
  qc/
```

Run folder:

```text
runs/<run_id>/
  acquisition/
  runner_logs/
  self_report/
  confounds/
  notes/
  inputs_snapshot/
```

Analysis folder:

```text
analysis/<run_id>_MasterComprehensive/
  tables/
  reports/
  figures/
  visualizer/
  offline_interpretation/
  exploratory/
```

Micro Handoff outputs should remain in an exploratory subfolder unless prospectively promoted.

---

# 30. Template files

## 30.1 MRED familiarity CSV

Records participant familiarity, prior exposure, autobiographical relevance, and stimulus-specific context. It is used to prevent novelty and memory from being confused.

## 30.2 MRED scene map CSV

Maps scenes, anchors, semantic roles, and expected interpretation windows.

## 30.3 Annotation CSV

Stores manual or semi-automated annotations such as event windows, face/body/shot features, audio issues, scene boundaries, or relevant contextual notes.

## 30.4 Feature table CSV

The Master Suite time-resolved feature table is the main bridge from raw data into module analysis. CAI/SID, visualizer, and offline interpreter modules depend on consistent feature naming or declared adapters.

## 30.5 CAA outputs

CAA should output synchronized cardiac and respiration grids, beat-event tables, respiration event tables, autonomic QC, and afterglow attribution support tables.

## 30.6 Micro Handoff outputs

Micro Handoff should output readiness reports, 25 ms feature/state series, lag series, branch summaries, contrasts, null checks, QC, provenance, and a human-readable report.

---

# 31. Safety, ethics, and public-release boundary

PRAYCG is research software. It is not a medical device.

Human-subjects work should include:

- informed consent;
- stimulus disclosure appropriate to the study;
- debriefing;
- withdrawal options;
- privacy protection;
- ethics/IRB review when required;
- data minimization;
- careful handling of emotional stimuli.

Public releases should exclude:

- raw private biosignals;
- copyrighted media;
- unredacted self-report;
- private addresses or local paths;
- credentials and tokens;
- speculative mechanism claims presented as empirical findings.

---

# 32. Current discovery map: hypotheses, not proofs

## 32.1 Recognition and integration can dissociate

A participant can recognize a meaningful event without showing a clean integration after-state. Conversely, a delayed after-state can occur when the acute peak is weak or confounded.

## 32.2 Peak-like meaning and resolution-like meaning differ

Some stimuli behave like impact. Others behave like closure. PRAYCG should not force both into one metric.

## 32.3 Analytic extraction does not erase meaning

Override can reduce reception, redirect attention, increase task-gamma, or allow story to break through. It is not a non-meaning condition.

## 32.4 Sensory clarity and emotional impact can dissociate

A participant may report emotional impact despite poor audio, or greater semantic clarity in Override than Target. DGA is the correct interpretive layer for these cases.

## 32.5 Meaning requires access conditions

A stimulus is not meaningful in the abstract. It is meaningful for a participant when sensory access, prior state, task stance, and confound burden allow it to function as meaning.

## 32.6 Control remains essential

Control branches are not proof of absence. They are defenses against simpler explanations.

---

# 33. What PRAYCG may eventually become

The strongest future version of PRAYCG is not a consciousness detector. It is a naturalistic psychophysiology workbench that helps researchers ask:

- when is the nervous system tracking sensory structure?
- when is it tracking high-order local shot structure?
- when does coherent narrative order matter?
- when does task stance alter reception?
- when does an after-state persist beyond the stimulus?
- when do respiration and autonomics explain the apparent effect?
- when do artifacts or missingness invalidate interpretation?

The project becomes stronger when it rejects weak positive findings.

---

# 34. Recommended next study design

The next serious PRAYCG study should use:

1. PRAYCG3 or PRAYCG4 selected before the run;
2. locked protocol manifest;
3. legally sourced stimulus;
4. phase and shot-order controls when feasible;
5. frame-verified anchors;
6. runner-side ALS barcode with holder calibration;
7. OpenBCI EEG plus EOG/EMG if possible;
8. Polar RR and Vernier respiration;
9. LabRecorder XDF;
10. preflight QC;
11. Master Suite core analysis;
12. CAA autonomic arrays;
13. CAI/SID as secondary state-density interpretation;
14. Micro Handoff as isolated exploratory output;
15. visualizer and offline interpreter for review;
16. no endpoint promotion without prospective replication.

---

# 35. Minimal glossary

- **AAM:** Afterglow Attribution Model.
- **A-MRED:** anchor-locked Meaning Recognition / Encoding Dissociation.
- **ALS/PT19:** light sensor used for physical display timing validation.
- **CAA:** Continuous Autonomic Arrays.
- **CAI:** Controlled Access-Integration Index.
- **CET-R:** residualization against cinematic/exogenous entrainment features.
- **DGA:** Decoder Gate Availability.
- **HOC-R:** High-Order Control Residualization.
- **MRED:** Meaning Recognition / Encoding Dissociation.
- **Micro Handoff:** exploratory raw-EEG timing probe from fast temporal activity to delayed theta/integration-like activity.
- **OSA:** Override Spatial Attention.
- **OHC:** Order/Habituation/Carryover.
- **RespDualPath:** respiration as both state signal and artifact/confound path.
- **SID:** State Integration Density.
- **SMG:** Semantic Meaning Gradient.
- **TSP:** Temporal Semantic Proxy.
- **TTI:** task/interference attenuation analysis.

---

# 36. Closing synthesis

PRAYCG v0.95 is best described as a disciplined open-methods workbench.

Its public claim is not that it measures consciousness. Its stronger claim is more useful:

> PRAYCG provides a structured way to test whether naturalistic narrative stimuli produce measurable body-brain state trajectories that survive increasingly strict controls for sensory drive, high-order local structure, analytic task stance, timing error, artifact, respiration, carryover, and self-report confounds.

The method matures by making interpretation harder, not easier.

A strong future PRAYCG result will not be one where a graph looks dramatic. It will be one where the result survives the machine built to defeat it.
