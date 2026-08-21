# PRAYCG Master Theory and Protocol

**Public-Safe GitHub Release Draft v1.0**  
**Author:** Hoyt Banks  
**Status:** exploratory methods architecture; not clinical, diagnostic, commercial, metaphysical, or confirmation-grade evidence.  
**Intended repository location:** `docs/PRAYCG_Master_Theory_and_Protocol_PUBLIC_v1_0.md`

---

## Document status and claim boundary

PRAYCG is an exploratory psychophysiology protocol and open-source software architecture for testing whether naturalistic narrative stimuli produce measurable EEG/autonomic state trajectories beyond low-level sensory entrainment and beyond analytic task demand.

This document is public-safe. It is designed for GitHub/OSF upload and for technical review by OpenBCI, LSL, EEG, psychophysiology, and open-science communities.

**This document does not claim that PRAYCG proves:**

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
- literal thermodynamic heat or ATP flow from EEG/HRV alone.

**Current permitted claim:** PRAYCG is an open, auditable, three-arm naturalistic-stimulus protocol and analysis workbench for studying sensory entrainment, narrative reception, analytic task stance, artifact/confound structure, and delayed after-state dynamics.

**Current evidentiary status:** pilot and methods-development evidence only. Some self-runs are scientifically useful as calibration or hypothesis-generating cases, but they are not treated as confirmation-grade evidence.

---

# 1. Executive summary

PRAYCG asks a narrow question hidden inside a broad human intuition:

> When a story is allowed to matter, does the body-brain system show a measurable state trajectory that differs from the same audiovisual material with recognizable meaning damaged, and from the same intact story watched under analytic task demand?

The protocol compares three branches generated from the same source stimulus:

| Branch | What is shown | Participant stance | Primary question |
|---|---|---|---|
| Phase-scrambled Control | The same source material after phase scrambling / meaning damage | Watch normally | Is the response explainable by light, sound, motion, cuts, rhythm, cue timing, or audiovisual energy? |
| Target Narrative | The intact narrative | Watch naturally | What happens when the story is accessible and allowed to land? |
| Contextual Override | The same intact cued video | Perform analytic task, usually running-sum number cues | What changes when the same stimulus is processed under extraction/task stance? |

The public version of PRAYCG should be understood as a **measurement architecture**, not a finished theory of consciousness. Its practical contribution is a reproducible pipeline:

1. select and legally source a stimulus;
2. prepare Target, Override, and phase-scrambled Control media;
3. generate cue schedules, timing/QC files, anchor templates, and stimulus fingerprints;
4. record EEG/autonomic/respiration/marker streams through LSL and LabRecorder;
5. run a structured Master Comprehensive Analysis Suite;
6. generate feature tables, event tables, visualizations, and offline plain-English reports;
7. keep strong claim boundaries and explicit falsification paths.

The current theoretical compression is:

> PRAYCG is becoming a theory of availability: whether a living system is available to decode, receive, integrate, and be changed by meaning.

---

# 2. Why PRAYCG exists

Everyone already knows that stories can move people. PRAYCG is not trying to prove that a person can understand a movie.

The scientific problem is different: naturalistic stimuli drive the nervous system through many overlapping channels at once.

A film contains:

- luminance changes;
- motion;
- cuts;
- faces;
- audio envelope;
- speech rhythm;
- music;
- loudness;
- semantic content;
- expectation;
- memory;
- autobiographical relevance;
- task demands;
- emotion;
- artifact opportunities: blinks, jaw tension, squinting, posture shifts.

A conventional “the subject watched the movie and the brain responded” interpretation is too loose. PRAYCG tries to separate layers:

1. **Exogenous sensory entrainment:** the nervous system follows physical features of the stimulus.
2. **Semantic / narrative reception:** the participant receives coherent meaning, not merely sensory rhythm.
3. **Analytic extraction:** the same narrative is processed under task demand.
4. **Integration / after-state:** the state of the body-brain system after the stimulus may carry forward differently than during the stimulus.
5. **Gate availability:** a meaningful response may require both external access and an internal decoder state.

The core logic is not anti-neuroscience. It accepts that sensory entrainment is real and treats it as the first critique to survive.

---

# 3. The phase-scrambled Control doctrine

The phase-scrambled Control should not be described as “meaningless” in an absolute sense. It is better described as a **meaning-damaged sensory-control branch**.

The Control branch is expected to preserve some low-level audiovisual drive while damaging recognizable narrative structure. Therefore, Control can still produce:

- visual entrainment;
- auditory envelope tracking;
- confusion;
- boredom;
- effortful scanning;
- artifact;
- low-level affect;
- sensory burden;
- physiological response.

That is not a failure. That is the point. The Control branch asks whether any Target effect is reducible to the stimulus as a sensory object.

**Correct claim:**

> Control preserves sensory drive while damaging recognizable narrative meaning.

**Incorrect claim:**

> Control is physiologically meaningless.

The strongest PRAYCG result is not “Target moved and Control did nothing.” The stronger result is:

> Target shows a pattern that Control does not reproduce, even though Control retains a matched sensory scaffold and cue timing.

This is why Control remains required for serious runs. A Target-vs-Override-only design can test reception versus extraction, but it cannot cleanly test meaning beyond sensory entrainment.

---

# 4. The acronym and public naming

PRAYCG / PR-AYC-G began as a working codename inside a broader theoretical framework. For the public open-source release, the acronym should be treated primarily as a project label.

The empirical object is not the acronym. The empirical object is the protocol:

> baseline -> phase-scrambled sensory-control -> washout -> intact target -> washout -> contextual override -> washout -> final reflection baseline -> final comparative report.

The public-facing title can be:

**PRAYCG: An Open Three-Arm Psychophysiology Pipeline for Testing State-Locked Narrative Meaning Beyond Sensory Entrainment and Analytic Task Demand**

---

# 5. Theory in one page: meaning as gated interaction

The simplest model is wrong:

```text
stimulus -> meaning response
```

PRAYCG instead models meaning as an interaction:

```text
external semantic access + internal decoder availability + regulatory state + low enough task/confound burden -> possible recognition and integration
```

The current working formulation is:

```text
MR(t) = D_gate(t) * sim(phi(u(t)), P(t))
```

Where:

- `MR(t)` = meaning-recognition proxy;
- `u(t)` = external stimulus vector;
- `phi(u(t))` = encoded sensory-semantic geometry of the stimulus;
- `P(t)` = persistent learned state-space / prior model / attractor structure;
- `sim()` = geometric fit between incoming cue and internal decoder;
- `D_gate(t)` = decoder gate availability.

This means a stimulus is not a full download of meaning. It may function as a key that activates a pre-existing learned state-space.

This formulation explains why:

- a familiar scene can be recognized without requiring strong new integration;
- a novel scene can produce strong acute update;
- a closure scene can produce delayed afterglow rather than sharp peak;
- degraded audio can block semantic access while visual/emotional geometry still moves the participant;
- analytic task stance can alter reception without changing the physical video.

---

# 6. Availability under load

A simplified availability equation helps organize the project:

```text
Availability(t) = [C(t) * U(t) * P(t)] / [1 + M(t) + N(t) + D(t)]
```

Where:

- `C(t)` = coherence: the system is gathered enough to respond;
- `U(t)` = update capacity: new information can matter;
- `P(t)` = persistence: the system remains present long enough to integrate;
- `M(t)` = mismatch: threat, contradiction, confusion, unabsorbed prediction error;
- `N(t)` = noise: fatigue, distraction, artifact, environmental interference;
- `D(t)` = defensive / extractive pressure: bracing, task load, performance pressure.

This is not a moral score. It is a practical model of state availability.

A high-meaning event may fail physiologically if the gate is closed by noise, task load, fatigue, or poor sensory access. A modest stimulus may produce a large after-state if it precisely fits a current-life or autobiographical decoder.

---

# 7. Experimental protocol overview

## 7.1 Standard PRAYCG2.0 branch sequence

A standard PRAYCG2.0 run uses the following structure:

| Step | Phase | Typical duration | Purpose |
|---|---:|---:|---|
| 1 | Setup / stream validation | variable | Verify streams, media files, cue schedule, anchors, LabRecorder, hardware. |
| 2 | Baseline 1 | 120 s | Initial eyes-open stillness baseline. |
| 3 | Control | stimulus length | Meaning-damaged sensory-control viewing. |
| 4 | Washout 1 | 120 s | Post-control after-state. |
| 5 | Control report | variable | Meaning, absorption, afterglow, task/confound ratings. |
| 6 | Target | stimulus length | Natural intact narrative reception. |
| 7 | Washout 2 | 120 s | Post-target after-state. |
| 8 | Target report | variable | Meaning, absorption, afterglow, confounds. |
| 9 | Contextual Override | stimulus length | Same intact cued video under analytic task. |
| 10 | Washout 3 | 120 s | Post-override after-state. |
| 11 | Override report | variable | Meaning, absorption, afterglow, confounds, task experience. |
| 12 | Final reflection baseline | 120 s | Reflective after-state after all branches. |
| 13 | Final master report | variable | Comparative branch selection and summary ratings. |

The final reflection baseline is important because some narrative effects may appear less as sharp peaks and more as delayed state resolution.

## 7.2 Branch order

The default order is:

```text
Baseline 1 -> Control -> Washout 1 -> Target -> Washout 2 -> Override -> Washout 3 -> Baseline 2 -> Final report
```

The Control branch usually comes first so it does not spoil the intact story. The Target comes before Override so natural reception is attempted before analytic task stance.

Order effects remain a limitation. The sequence is chosen for practical and interpretive reasons, not because it eliminates all order confounds.

## 7.3 Contextual Override task

The default Override task is an upper-right number-cue running sum.

A typical cue schedule uses:

```text
cue interval: 3.0 seconds
cue display duration: 0.85 seconds
cue values: 1-10
position: upper right
fixed-position reason: reduce visual search and saccade confounds
```

Target and Override should use the same cue-embedded stimulus. Only the instructions should differ.

The Override task is not merely a distraction. It creates an analytic, extractive stance. PRAYCG asks whether this stance changes the physiological trajectory of the same story.

---

# 8. Media procurement and stimulus selection

## 8.1 Legal and ethical sourcing

Public PRAYCG repositories should not redistribute copyrighted media.

GitHub may contain:

- code;
- documentation;
- templates;
- synthetic/demo videos created for the project;
- public-safe derived data;
- public-domain or properly licensed media recipes.

GitHub should not contain:

- copyrighted film clips;
- raw private biosignal recordings;
- private self-report logs;
- third-party proprietary assets;
- passwords or tokens.

A user must supply any copyrighted stimulus locally and must follow copyright, institutional, and ethical requirements.

## 8.2 Practical stimulus criteria

A good PRAYCG stimulus candidate usually has:

- 2.5-5 minutes duration;
- coherent emotional or cognitive arc;
- clear audio;
- minimal sudden extreme loudness;
- limited strobing / flash risk;
- a few identifiable predeclared anchor moments;
- strong enough narrative structure that a phase-scrambled version meaningfully damages recognition;
- no visible source stamp or subtitle artifact unless intentionally documented;
- legal permission or local-use-only status.

Stimulus selection should be documented before analysis. If the viewer has prior exposure, familiarity should be recorded and used as an MRED covariate.

## 8.3 Stimulus categories

Useful categories include:

| Category | Expected PRAYCG profile |
|---|---|
| Awe / model expansion | acute MRED-Peak or high-load-with-recovery profile |
| Closure / repair | MRED-Resolution, Baseline2 echo, regulatory recovery |
| Familiar meaningful scene | meaning recognition may occur without strong new integration |
| Ambiguous / subtle scene | may require stronger self-report and anchor mapping |
| Overstimulating scene | high sensory entrainment and artifact risk |
| Text/subtitle-heavy scene | may confound semantic access and reading load |

---

# 9. MediaPrep and stimulus generation

MediaPrep prepares the stimulus files and supporting cue/QC artifacts. It does not certify empirical endpoints.

## 9.1 MediaPrep outputs

A typical MediaPrep output folder contains:

```text
stimulus_master_cleaned_<project>.mp4
stimulus_target_cued_<project>.mp4
stimulus_override_cued_<project>.mp4
stimulus_control_cued_phase_scrambled_<project>.mp4
cue_schedule_<project>.json
cue_schedule_<project>.csv
predeclared_anchors_<project>_DRAFT.json
qc/
  stimulus_exogenous_regressor_frame_all_conditions.csv
  cet_regressors_all_conditions.csv
  stimulus_rhythm_summary_all_conditions.csv
  stimulusfingerprint_cet_eet_manifest.json
```

## 9.2 Critical MediaPrep rules

1. Apply any watermark/source-stamp cleanup to the master before branches are generated.
2. Generate Target and Contextual Override from the same cue-embedded video.
3. Generate Control by phase-scrambling the cue-embedded Target.
4. Preserve cue timing and low-level cue energy in the Control branch.
5. Run manual Control audio QC.
6. Run visual QC on Target, Override, and Control.
7. Run StimulusFingerprint / CET regressors when possible.
8. Save hashes and manifests.

## 9.3 Control audio QC

The phase-scrambled Control audio should be manually checked at the same speaker/headphone settings used in the protocol.

Pass criteria:

- no recognizable words;
- no intelligible sentence fragments;
- no distinct musical melody carrying narrative recognition;
- loudness/envelope broadly tracks original;
- sounds like speech-shaped or scene-shaped noise, not understandable dialogue.

If recognizable words remain, the Control branch is invalid or pilot-only.

## 9.4 Visual QC

Visual QC should check:

- no readable watermark/source stamp/platform logo/subtitle artifact remains unless documented;
- cleanup was applied before branch generation;
- Target and Override remain bit-identical after cue rendering;
- Control was generated from cleaned cue-embedded Target;
- cue badges are legible;
- contrast is sufficient across the scene;
- ALS timing square does not obscure cue or stimulus content.

---

# 10. Anchor doctrine

PRAYCG uses predeclared anchors to prevent post-hoc story-time fishing.

## 10.1 Anchor types

| Anchor status | Meaning | Claim level |
|---|---|---|
| Conceptual | Anchor chosen after watching/analysis but before formal next run | exploratory only |
| Estimated | Time estimated from web/source clip or approximate viewing | runner-registered pilot |
| Blind estimated | Time estimated while preserving participant novelty | runner-registered blind pilot |
| Frame-verified locked | Exact rendered time checked on final MediaPrep Target MP4 before acquisition | potential confirmation-grade input |

## 10.2 Strict anchor-lock workflow

For confirmation-grade A-MRED attempts:

1. run MediaPrep;
2. open final rendered Target MP4;
3. verify each anchor time in the final rendered timebase;
4. update `rendered_time_sec` values;
5. mark each anchor as frame verified;
6. save as `*_LOCKED.json`;
7. load the locked file into PRAYCG2.0 before acquisition;
8. confirm the runner logs the anchor file hash.

Estimated anchors are better than no anchors, but they are not confirmation-grade.

## 10.3 Clip-edge policy

Anchors near the end of a video should not be treated as strict in-clip theta-carryover endpoints unless there is enough post-event footage to calculate the delayed window. If the anchor is near the end, declare it as:

```text
MRED-Resolution / paired-washout continuation / Baseline2 / EET support
```

rather than a strict in-clip A-MRED theta-handoff endpoint.

---

# 11. Hardware and acquisition architecture

## 11.1 Core hardware

A typical PRAYCG setup includes:

- OpenBCI Cyton + Daisy for 16-channel EEG;
- OpenBCI gelless/gelfree cap or Ultracortex Mark IV;
- BrainFlow bridge to LSL;
- ALS-PT19 or equivalent analog light sensor for physical screen-timing validation;
- Polar H10 chest strap for RR intervals / HRV context;
- Vernier Go Direct Respiration Belt for respiration force channel;
- LabRecorder for XDF capture;
- stimulus laptop/display;
- optional shielding / Faraday enclosure;
- optional EOG/EMG channels for stronger artifact control.

## 11.2 EEG stream

The EEG stream should be started before the protocol runner and visible in LabRecorder. A useful stream name convention is:

```text
obci_eeg1
OpenBCIStatusMarkers
```

The protocol should record:

- nominal sampling rate;
- effective sampling rate;
- channel count;
- packet gaps;
- status marker heartbeat;
- channel-map confirmation;
- channel-map confidence.

For new public runs, use a locked physical channel map and document electrode-to-channel mapping with photos or a physical trace.

## 11.3 ALS/PT19 timing channel

The ALS/PT19 timing square is a physical display-timing validation channel. It belongs to the external stimulus input `u(t)`, not to any biological hidden variable.

Recommended hardware practice:

- attach sensor directly over the timing square;
- use an opaque shroud / black tape to block room light;
- strain-relieve the cable;
- verify the sensor signal in OpenBCI analog AUX / Analog Read LSL;
- repeat test on Control, Target, and Override.

Recommended future improvement:

```text
black pre-guard: 0.5 s
white pulse: 2.0 s
black guard: 0.5 s
white pulse: 0.75 s
black guard: 1.0 s
```

This barcode-like start pulse is more robust than a single short white block. A 3D-printed holder should ensure the sensor sits over the actual rendered pulse area, especially when the runner uses safe-fit video scaling.

## 11.4 Polar H10

The Polar H10 stream should be treated as RR interval telemetry, not a continuous ECG waveform unless a separate ECG waveform mode is implemented.

The PRAYCG Polar bridge pushes RR intervals in milliseconds to an LSL stream typically named:

```text
PolarHRV
```

RR intervals support:

- HR estimate;
- RMSSD;
- SDNN;
- pNN50;
- post-branch regulatory summaries;
- API_A-like availability indices.

## 11.5 Vernier respiration belt

The Vernier Go Direct Respiration Belt should stream the raw Force channel to LSL so respiratory phase can be reconstructed offline.

Typical LSL stream name:

```text
VernierRespirationBelt
```

Default channel:

```text
force_N
```

USB is preferred for stability and to avoid Bluetooth contention with Polar H10. BLE can work but should be treated as more fragile.

## 11.6 LabRecorder

LabRecorder should record all active streams into one XDF file:

```text
EEG / BrainFlow
OpenBCIStatusMarkers
PolarHRV
VernierRespirationBelt
PRAYCG / Stasis marker stream
```

Before pressing record:

1. confirm all required streams are visible;
2. confirm the marker stream is online;
3. confirm LabRecorder output path;
4. record the full run from before Baseline 1 until after the final report.

---

# 12. PRAYCG2.0 runner

The current runner layer is PRAYCG2.0. It records structured event logs and a media-selection configuration.

The runner should log:

- participant ID;
- session ID;
- run label;
- Control video path/hash;
- Target video path/hash;
- Override video path/hash;
- cue schedule path/hash;
- predeclared anchor file path/hash;
- Target/Override hash match;
- baseline and washout durations;
- final reflection baseline status;
- calibration status;
- confound-report settings;
- channel-map label and confidence;
- StasisMarkers / LSL marker stream source.

If the runner only works reliably through PsychoPy Coder on a given system, the public workflow should state that directly:

```text
Launch PRAYCG2.0 from PsychoPy Coder if direct Python launch fails.
```

The PRAYCG Control Center should orchestrate tool launching, but not force the runner to run outside PsychoPy if the local PsychoPy environment is required.

---

# 13. Self-report and neurophenomenology

Self-report is an independent evidence stream. It contextualizes physiology but does not prove internal state, mechanism, consciousness, or memory formation.

PRAYCG2.0 reports typically include:

- branch-level Meaning;
- Absorption;
- EmotionalAfterglow;
- StoryActiveWashout;
- TaskExtractionLoad;
- ConfoundBurden;
- detailed audio/video/cue/noise/eye-strain reports;
- Override task reports;
- final comparative branch choices;
- familiarity and new-meaning ratings.

The correct stance is:

```text
self-report constrains interpretation; it does not certify physiology.
physiology constrains interpretation; it does not replace experience.
```

A run where self-report and physiology diverge is not automatically failed. It may reveal an unmodeled gate, confound, or analysis limitation.

---

# 14. Master Comprehensive Analysis Suite

The Master Comprehensive Suite is the post-processing engine.

It should produce:

- time-resolved feature table;
- QC reports;
- event tables;
- anchor tables;
- artifact/confound summaries;
- branch summaries;
- MRED/A-MRED outputs;
- NIP/TTI/NUPI/DGA outputs;
- CET-R and stimulus residualization outputs;
- visual overlays;
- offline interpretive report.

## 14.1 Module tier map

### Boxed primary path

```text
Timing/QC
+ StimulusFingerprint/CET-R
+ artifact/confound gates
-> A-MRED / MRED-Peak / MRED-Resolution
```

### Secondary interpretation layer

```text
NIP / BIT / CII / IAQ
TTI
NUPI
DGA
Baseline 1 vs Baseline 2
```

### Exploratory / convergence layer

```text
KHT-topo
NAST
EET
MRED-ITP / ACG / OCU
OCM025 / RSM / CVB / SquintProxy
LSO / Subtitle Override, when applicable
Topo-OSM network-state modeling
```

No module should be treated as proof by itself.

---

# 15. Core analysis modules

## 15.1 ArtifactScore

ArtifactScore penalizes windows likely contaminated by:

- peak-to-peak voltage outliers;
- high-frequency sentinel features;
- line-noise proxies;
- blinks/ocular bursts;
- forehead/jaw/EMG-like activity;
- dropouts or flatlines.

ArtifactScore has veto power. A physiologically beautiful candidate is not trustworthy if it is artifact-driven.

## 15.2 GammaScalpel / lower-gamma work-signal proxy

GammaScalpel subdivides high-frequency EEG features into smaller bands and compares their behavior by condition, ROI, and artifact burden.

Public wording:

```text
Lower-gamma/high-frequency features are artifact-sensitive candidate work-signal proxies, not biomarkers of meaning.
```

The goal is not “gamma equals meaning.” The goal is to ask whether a high-frequency candidate survives artifact penalties, Control comparison, Override comparison, and delayed integration checks.

## 15.3 TSP: Temporal Semantic Proxy

TSP is an operational proxy for candidate semantic/meaning-recognition pressure.

It may combine:

- MeaningGamma-like features;
- task-gamma suppression/contrast;
- artifact penalties;
- visual/audio confound penalties;
- timing around predeclared anchors.

TSP should be interpreted only as a feature, not as proof of meaning.

## 15.4 Theta handoff / integration proxy

Theta handoff asks whether an event produces delayed low-frequency carryover after a high-frequency recognition candidate.

Typical windows:

```text
recognition / strike: anchor to anchor + 5-12 s
delayed carryover: anchor + 8 s to anchor + 30 s
```

The exact windows should be specified before analysis.

## 15.5 MRED

MRED means Meaning Recognition / Encoding Dissociation.

It distinguishes:

| MRED quadrant | Interpretation |
|---|---|
| MR_HIGH_ENC_HIGH | recognition and integration/carryover candidate |
| MR_HIGH_ENC_LOW | recognition without clear integration |
| MR_LOW_ENC_HIGH | non-semantic state update, artifact, respiration, task, or unmodeled process |
| MR_LOW_ENC_LOW | no structured MRED event |

MRED does not prove memory formation. It classifies operational evidence.

## 15.6 A-MRED

A-MRED is the compressed primary endpoint.

A locked anchor `j` passes only if Target shows both meaning recognition and delayed integration greater than Control and Override after QC.

Formula:

```text
A_MRED_j =
  1[MR_T,j  > theta_MR]
* 1[ENC_T,j > theta_ENC]
* 1[MR_T,j  > MR_C,j + delta]
* 1[MR_T,j  > MR_O,j + delta]
* 1[ENC_T,j > ENC_C,j + delta]
* 1[ENC_T,j > ENC_O,j + delta]
* 1[QC_j = PASS]
```

This is a gate, not a score. It intentionally fails often.

## 15.7 MRED-Peak and MRED-Resolution

MRED-Peak asks whether a predeclared anchor produces an acute Target-specific recognition-plus-integration event.

MRED-Resolution asks whether a stimulus produces delayed reflective/regulatory recovery rather than a sharp event peak.

Approximate formulation:

```text
PeakScore_j = MR_T,j * ENC_T,j * QC_j * specificity_j
```

```text
ResolutionScore_j = RDI_j * Echo_j * SelfReportEcho_j * QC_j
```

Where `RDI` is regulatory dividend index and `Echo` may include Baseline2, EET, and post-run after-state evidence.

This distinction emerged because some scenes behave like acute shock/recognition events, while others behave like slower closure/recovery events.

## 15.8 NIP / BIT / CII / IAQ

NIP means Narrative Immersion Proxy. It translates attention-plus-resonance into an auditable macroscopic proxy.

- `BIT` = Bivariate Immersion Threshold: requires both semantic attention and integration/resonance, not merely one high score.
- `CII` = Continuous Immersion Index: integrates immersion-density across a window.
- `IAQ` = Immersion Attenuation Quotient: estimates Target-vs-Override attenuation of the immersion proxy.

Safe interpretation:

```text
These are immersion proxies, not dopamine/oxytocin measures and not proof of subjective experience.
```

## 15.9 TTI

TTI means reception-extraction tradeoff or task-theft index.

It asks whether the analytic Override reroutes the same story away from receptive integration toward task extraction.

Formula sketch:

```text
TTI =
  w1*z(MR_T - MR_O)
+ w2*z(ENC_T - ENC_O)
+ w3*z(API_T - API_O)
+ w4*z(TaskGamma_O - TaskGamma_T)
- artifact/confound penalties
```

Positive TTI suggests Target carried more receptive/meaning structure while Override carried more task/extraction structure.

## 15.10 NUPI

NUPI means Narrative Update Polarity Index.

It separates two types of meaningful update:

- **Accommodative load:** the story imposes model-expansion cost or semantic shock.
- **Resolutive recovery:** the story closes an unresolved loop and is followed by regulatory recovery.

Formula:

```text
ALI = mean(semantic_intensity, target_specificity, complexity_perturbation, TTI, endpoint_pass)
RDI = mean(Baseline2_regulation, Baseline2_semantic_echo, EET_afterstate_echo, self_report_echo)
NUPI = RDI - ALI
```

NUPI is not literal thermodynamics. It is a proxy-level profile classifier.

## 15.11 DGA

DGA means Decoder Gate Availability.

DGA formalizes the insight that meaning is not a simple payload transfer. It depends on external access and internal decoder availability.

Branch-level variables:

```text
SA_b = semantic access
DA_b = decoder availability
EI_b = emotional/integrative impact
X_b  = extraction/task load
C_b  = confound/noise burden
```

Operational formulas:

```text
SA_b = 1 - mean(AudioComprehensionDifficulty,
                SpeakerVolumeDifficulty,
                ExternalNoiseIntrusion,
                AudioVideoSyncProblem) / 9

DA_b = mean(Meaning, Absorption, EmotionalAfterglow, StoryActiveWashout) / 9

EI_b = mean(Absorption, EmotionalAfterglow, StoryActiveWashout) / 9

X_b = max(core_TaskExtractionLoad, OverrideTaskBurden) / 9

C_b = max(core_ConfoundBurden, DetailedConfoundMean) / 9

D_gate,b = sigmoid(2.0*SA_b + 1.4*DA_b + 1.1*EI_b
                   - 1.2*X_b - 1.8*C_b - 0.75)
```

Gate Dissociation Index:

```text
GDI = mean(SA_Override - SA_Target,
           EI_Target - EI_Override,
           X_Override - X_Target,
           C_Target - C_Override)
```

DGA is a secondary interpretation layer. It explains why A-MRED may pass, fail, or split.

## 15.12 CET / CET-R / EET

CET means Cinematic Entrainment Tracking. It asks how much EEG features track stimulus-side variables:

- luminance;
- visual change;
- cuts;
- audio RMS/envelope;
- cue timing;
- cue value;
- ALS/start-pulse regressors.

CET-R residualizes EEG/feature outputs against those exogenous regressors:

```text
Y_EEG(t) = beta_0 + sum_m beta_m * u_m(t - lag_m) + beta_A * Artifact(t) + epsilon(t)
```

If a Target effect disappears after CET-R, it may be reducible to exogenous stimulus rhythm. If it survives, interpretation strengthens but is still not proven.

EET means Endogenous Echo Tracking. It asks whether a state-vector pattern from a meaningful window resembles later washout or Baseline2 state. EET is not replay proof; it is state-vector resemblance.

## 15.13 MRED-ITP / ACG / OCU

MRED-ITP is the information-thermodynamic proxy layer.

- `ACG` = Algorithmic Complexity Gate: complexity perturbation and settlement proxy.
- `OCU` = Ocular-Cognitive Unloading: blink suppression/release as event-boundary or attention-release proxy.

These are exploratory convergence layers. Lempel-Ziv-like complexity is not literal thermodynamic entropy. Blink timing is not proof of memory encoding.

---

# 16. Baseline 2: promise and danger

Baseline2 is the final reflection baseline after all branches. It is often one of the most interesting parts of the protocol, but it is cumulative.

Baseline2 may reflect:

- Target afterglow;
- Override semantic clarification;
- task completion relief;
- fatigue;
- emotional reflection;
- environmental changes;
- respiration changes;
- cumulative memory activation;
- confound resolution.

Therefore Baseline2 should not be automatically attributed to Target only.

Correct interpretation:

```text
Baseline2 reflects the integrated after-state of the whole run unless the design specifically isolates its source.
```

---

# 17. Pilot-derived archetypes

The current self-run evidence is exploratory. It should be used to develop hypotheses, not to claim proof.

## 17.1 Recognition-dominant archetype

Some stimuli appear to produce meaning recognition without clean new integration. This is especially plausible for familiar scenes. The subject recognizes the meaningful geometry, but the system may not need to perform a major new update.

## 17.2 MRED-Peak archetype

Some stimuli appear as acute, anchor-like meaning-impact events. These are best tested with frame-locked anchors and strict A-MRED.

## 17.3 MRED-Resolution archetype

Some stimuli may be less peak-like and more reflective. The important signal may appear in washout, Baseline2, HRV, respiration, and self-report echo.

## 17.4 Decoder-gate dissociation archetype

Some runs reveal that semantic access and emotional impact can dissociate. For example:

- Target may be more emotionally absorbing but have degraded audio.
- Override may be semantically clearer but task-loaded.

This motivates DGA. It does not rescue a confounded run as confirmation-grade; it makes the confound theoretically informative.

---

# 18. Topo-OSM and OSM-CELL quarantine

The current human PRAYCG layer should be called **Topo-OSM** only in a cautious interpretive sense: macroscopic network-state topology, not cellular proof.

Public-safe rule:

```text
PRAYCG scalp EEG does not measure microtubules, biophotons, cytoskeletal state, molecular memory traces, or hidden cellular Y(t).
```

The cellular/mechanism layer should remain quarantined as **OSM-CELL** until there is direct cellular evidence.

The safer memory hypothesis is:

```text
long-term memory should be modeled as a self-refreshing attractor distributed across structural state, scaffold stabilization, synaptic/circuit activity, transcriptional/epigenetic bias, and replay/reactivation.
```

Formula:

```text
M(t) = [P(t), B(t), W(t), Z(t), R(t)]
```

Where:

- `P(t)` = candidate structural trace strength;
- `B(t)` = stabilization/scaffold state;
- `W(t)` = synaptic/circuit weight pattern;
- `Z(t)` = transcriptional/epigenetic regulatory bias;
- `R(t)` = replay, recall, cue reactivation, activity-dependent refresh.

This remains a theory constraint, not a demonstrated PRAYCG result.

---

# 19. Rung 0 / Opto-PING synthetic identifiability

The Opto-PING / Rung 0 work is synthetic identifiability testing.

Purpose:

```text
Can the software detect a hidden reciprocal loop when that loop is deliberately placed into simulated data under known conditions?
```

It does **not** prove that the biological loop exists.

Core idea:

```text
K_loop = eta * zeta
K = sqrt(eta * zeta)
```

Rung 0 helps verify the analysis machinery before applying similar logic to biology. It is a radar test with a simulated target, not proof that the real target exists.

---

# 20. Confirmation-grade decision rule

A future PRAYCG run should be called **confirmation-grade** only if all of the following are true:

## 20.1 Stimulus and anchor standard

- final rendered Target MP4 was inspected;
- anchor times were frame-verified before acquisition;
- `*_LOCKED.json` loaded into the runner;
- runner recorded anchor file hash;
- Target/Override hashes match;
- Control generated from cue-embedded Target;
- Control audio passed human QC;
- visual source-stamp QC passed.

## 20.2 Timing standard

- LSL marker stream online before recording;
- LabRecorder captured all required streams;
- ALS/PT19 pulse passed in Control, Target, and Override;
- no major branch-start ambiguity;
- effective EEG rate acceptable;
- no unrecoverable stream dropouts.

## 20.3 Hardware standard

- channel map locked and documented;
- EEG stream stable;
- respiration and RR streams available if intended;
- EOG/EMG preferred for strong gamma claims;
- cap/electrode quality acceptable.

## 20.4 Confound standard

- audio comprehension adequate and roughly balanced across Target/Override;
- no severe external noise asymmetry;
- cue legibility acceptable;
- no major audio-video sync mismatch;
- artifact gates pass.

## 20.5 Analysis standard

- A-MRED passes at locked anchor(s);
- Target > Control;
- Target > Override;
- CET-R does not explain away result;
- artifact/confound gates pass;
- self-report supports intended state but is not treated as proof;
- sensitivity analyses do not reverse the conclusion.

## 20.6 Replication standard

A single self-run should not be treated as final confirmation. Confirmation requires replication, ideally with:

- multiple subjects;
- preregistered anchors;
- locked analysis plan;
- EOG/EMG;
- external review;
- no post-hoc threshold changes.

---

# 21. File provenance and folder map

## 21.1 Recommended project root

```text
C:\PRAYCG\
  stimuli\
  runs\
  analysis\
  logs\
  config\
```

## 21.2 Stimulus folder

```text
stimuli\<stimulus_id>\
  master\
    stimulus_master.mp4
    master_media_validation_report.json
    master_sha256.txt
  mediaprep\
    <timestamped_mediaprep_folder>\
      stimulus_target_cued_*.mp4
      stimulus_override_cued_*.mp4
      stimulus_control_cued_phase_scrambled_*.mp4
      cue_schedule_*.json
      cue_schedule_*.csv
      qc\
  anchors\
    *_DRAFT.json
    *_LOCKED.json
    *_annotation_windows.csv
    *_MRED_scene_map.csv
    *_MRED_familiarity_covariates.csv
```

## 21.3 Run folder

```text
runs\<run_id>\
  acquisition\
    *.xdf
  runner_logs\
    *_events.csv
    *_events.json
    *_run_config_media_selection.json
    *_core_report.json
    *_confound_report.json
    *_override_task_report.json
    *_final_master_report.json
  inputs_snapshot\
  notes\
```

## 21.4 Analysis folder

```text
analysis\<run_id>_MasterComprehensive\
  tables\
    *_time_resolved_feature_frame.csv
    *_amred_anchor_endpoint_table.csv
    *_mred_peak_resolution_anchor_table.csv
    *_tti_global_summary.csv
    *_nupi_summary.csv
    *_dga_branch_gate_table.csv
  reports\
  figures\
  visualizer\
```

---

# 22. Template files: what they are and where they come from

## 22.1 MRED familiarity CSV

Purpose: manual covariate file for novelty/familiarity/personal resonance.

Generated by: template copied and filled manually.

Common location:

```text
analysis_inputs\<run_id>\<run>_MRED_familiarity_covariates.csv
```

It should include ratings such as:

- prior exposure;
- scene remembered;
- beat anticipated;
- new meaning today;
- current-life connection;
- autobiographical resonance;
- meaningful but already known.

## 22.2 MRED scene map CSV

Purpose: anchor-to-scene translation table.

Generated by: anchor file plus manual scene mapping.

Common location:

```text
analysis_inputs\<run_id>\<run>_MRED_scene_map.csv
```

## 22.3 Annotation CSV

Purpose: bridge file for human review and visualizer overlays.

Generated by: anchor file, scene map, or analysis output.

Common columns:

```text
anchor_id, condition, start_sec, end_sec, time_sec, label, claim_level, category, notes
```

## 22.4 Feature table CSV

Purpose: canonical time-resolved physiological feature table.

Generated by: Master Comprehensive Analysis Suite.

Common location:

```text
analysis\<run_id>_MasterComprehensive\tables\<run>_time_resolved_feature_frame.csv
```

The feature table is not manually created. If it is missing, the Master Suite has not completed feature extraction.

---

# 23. Visualizer and offline interpreter

## 23.1 Master Sync Visualizer

The visualizer creates a synchronized video artifact:

```text
stimulus video on top
rolling EEG/autonomic/respiration graphs below
event overlays aligned to XDF marker intervals or feature-table time
```

It is an audit and communication tool, not proof of endpoint validity.

## 23.2 Offline interpretive report generator

The offline interpreter reads the Master Suite output folder and generates local plain-English reports.

Purpose:

- help public users understand results without uploading data;
- prevent overinterpretation;
- explain module hierarchy;
- label pilot/timing/confound limitations;
- distinguish primary, secondary, and exploratory modules.

It is rule-based and deterministic. It is not an AI model and cannot replace expert review.

---

# 24. PRAYCG Control Center

The PRAYCG Control Center is a usability layer, not a new analysis engine.

It should launch and organize:

- MediaPrep Suite;
- acquisition scripts;
- Polar H10 stream;
- Vernier respiration stream;
- BrainFlow EEG-only;
- BrainFlow EEG+ALS;
- LabRecorder;
- PsychoPy runner launcher;
- Master Comprehensive Analysis Suite;
- Visualizer;
- Offline Interpreter.

Design principle:

```text
orchestrate tools as separate subprocesses; do not merge everything into one fragile mega-program.
```

This allows PsychoPy, BrainFlow, BLE, LabRecorder, and analysis tools to fail independently without killing the Control Center.

---

# 25. Safety, ethics, and public-release boundary

PRAYCG is not a medical device.

Public users should not:

- use PRAYCG for diagnosis;
- use PRAYCG for treatment decisions;
- claim it measures consciousness;
- upload private participant data without consent;
- redistribute copyrighted media;
- run human-subjects research outside applicable ethical and institutional rules;
- treat self-report as proof of internal state;
- treat EEG/HRV as a replacement for experience.

If PRAYCG is used beyond personal engineering tests, users should consider IRB/ethics review, consent forms, privacy protection, and deidentification.

---

# 26. Current discovery map: hypotheses, not proofs

The project has not proven a final theory, but it has produced a coherent set of working hypotheses.

## 26.1 Meaning recognition and integration can dissociate

A meaningful scene may be recognized without producing a strong new after-state. Familiarity may create recognition without new integration.

## 26.2 Peak-like meaning and resolution-like meaning differ

Some stimuli produce acute anchor-like impact. Others produce delayed afterglow and regulatory recovery.

## 26.3 Analytic extraction does not simply erase meaning

Override can reroute, attenuate, delay, clarify, or reshape meaning rather than merely suppress it.

## 26.4 Sensory clarity and emotional impact can dissociate

A branch can be emotionally powerful but semantically degraded, or semantically clear but task-loaded.

## 26.5 Meaning requires access conditions

Meaning is not just stimulus energy. It requires semantic access, decoder availability, prior state-space, personal relevance, regulatory capacity, and low enough noise/task burden.

## 26.6 Control remains essential

Phase-scrambled Control is not dead. It is the guardrail against sensory-entrainment overclaiming.

---

# 27. What PRAYCG may eventually become

If replicated, simplified, and externally audited, PRAYCG could become useful as:

- an OpenBCI/LSL naturalistic-stimulus protocol;
- an educational multimodal EEG acquisition workflow;
- a media-cognition and psychophysiology testbed;
- a task-load vs narrative-reception paradigm;
- an artifact/QC teaching suite;
- a framework for comparing sensory entrainment, semantic access, and after-state physiology;
- a methodological bridge between first-person report and physiological measurement.

It is too early to claim clinical, diagnostic, consumer, or commercial applications.

---

# 28. Recommended next study design

A stronger next-stage study should include:

1. multiple participants;
2. locked frame-verified anchors;
3. quiet controlled audio or headphones;
4. physical ALS holder and barcode start-pulse pass;
5. EOG and EMG channels;
6. respiration and RR streams;
7. full StimulusFingerprint/CET-R;
8. preregistered A-MRED primary endpoint;
9. secondary NIP/TTI/NUPI/DGA reports;
10. external code review;
11. explicit null and sensitivity analyses.

The analysis plan should specify which modules are confirmatory, which are secondary, and which are exploratory before data collection.

---

# 29. Minimal glossary

| Term | Meaning |
|---|---|
| PRAYCG | Public project label for the three-arm narrative psychophysiology protocol. |
| Control | Phase-scrambled meaning-damaged sensory-control branch. |
| Target | Intact narrative watched naturally. |
| Override | Same intact cued narrative watched under analytic task demand. |
| MRED | Meaning Recognition / Encoding Dissociation. |
| A-MRED | Anchor-locked MRED primary gate. |
| MRED-Peak | Acute recognition-plus-integration event profile. |
| MRED-Resolution | Delayed reflective/regulatory recovery profile. |
| NIP | Narrative Immersion Proxy. |
| TTI | Reception-extraction / task-theft index. |
| NUPI | Narrative Update Polarity Index. |
| DGA | Decoder Gate Availability. |
| CET-R | Cinematic Entrainment Tracking residualization. |
| EET | Endogenous Echo Tracking. |
| OCU | Ocular-Cognitive Unloading. |
| ACG | Algorithmic Complexity Gate. |
| Topo-OSM | Human-scale network topology interpretation layer. |
| OSM-CELL | Quarantined cellular mechanism hypothesis, not established by PRAYCG. |
| ALS/PT19 | Physical light sensor used to validate display timing. |
| LSL | Lab Streaming Layer, used to synchronize data streams. |
| XDF | LabRecorder multimodal recording file format. |

---

# 30. Closing synthesis

PRAYCG began as an attempt to measure whether meaning leaves a trace. Its current form is more disciplined:

> PRAYCG tests whether the body-brain system is available to decode, receive, integrate, and carry forward a meaningful stimulus in ways not reducible to low-level sensory entrainment or analytic task demand.

The project is at its strongest when it refuses to overclaim. The phase-scrambled Control protects the sensory-entrainment question. The Override branch protects the task-stance question. The self-report layer protects the lived-experience question. The artifact and CET-R layers protect the measurement question. A-MRED protects the endpoint question.

If future data survive those gates, the result will be worth taking seriously. If they do not, PRAYCG remains useful as an unusually detailed open-source measurement workbench and a public record of disciplined hypothesis refinement.

The work is not finished. The current contribution is the architecture: a way to turn human meaning into a falsifiable timing problem without pretending the timing exhausts the meaning.
