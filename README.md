# PRAYCG

**PRAYCG** is an exploratory, open-source psychophysiology protocol and software pipeline for studying whether naturalistic narrative stimuli produce measurable EEG/autonomic state trajectories that differ from low-level audiovisual stimulation and from the same intact stimulus under analytic task demand.

This repository is **methods-first**. It contains software, documentation, templates, and public-safe example materials for stimulus preparation, protocol execution, acquisition support, physiological analysis, visualization, and offline interpretation.

PRAYCG should be read as an open research workbench, not as a finished neuroscience claim.

---

## Current claim boundary

PRAYCG does **not** prove:

- consciousness,
- the soul,
- love as a number,
- clinical efficacy,
- diagnosis or treatment capability,
- memory biology,
- microtubules,
- biophotons,
- quantum biology,
- or hidden biological variables from scalp EEG.

The current permitted claim is narrower:

> PRAYCG is an open, auditable naturalistic-stimulus protocol and analysis workbench for studying sensory entrainment, narrative reception, analytic task stance, artifact/confound structure, and delayed after-state dynamics.

Pilot examples are useful for software testing, file-layout demonstration, and hypothesis generation. They are **not** confirmation-grade evidence.

---

## The basic research question

Everyone already knows stories can move people. PRAYCG is not trying to prove that a person can understand a movie.

The technical question is more specific:

> When a story is accessible and allowed to matter, does the body-brain system show a measurable state trajectory that differs from a meaning-damaged sensory control and from the same intact story watched under analytic task load?

Naturalistic video is complicated. A film contains light, sound, motion, cuts, faces, speech rhythm, music, semantic content, memory, expectation, task demand, emotion, and many opportunities for artifact. PRAYCG tries to separate these layers instead of treating “watched a movie” as one undifferentiated event.

---

## Core protocol logic

PRAYCG compares controlled media-viewing branches.

### Phase-scrambled Control

A version of the source video where recognizable narrative content is damaged while some low-level audiovisual timing remains.

This branch asks:

> Is the response explainable by light, sound, motion, cuts, rhythm, cue timing, or audiovisual energy?

The Control is **not** assumed to be physiologically meaningless. It can still create visual entrainment, auditory tracking, confusion, boredom, scanning, low-level affect, and artifact. That is why it is useful.

### Target

The intact narrative watched naturally.

This branch asks:

> What happens when the story is accessible and the participant is allowed to receive it?

### Contextual Override

The same intact cue-embedded video watched under an analytic task, usually a running-sum number-cue task.

This branch asks:

> What changes when the same stimulus is processed under extraction/task stance rather than natural reception?

The important rule is that **Target and Override should use the same cue-embedded stimulus**. The video should stay the same; the participant instructions change.

---

## Current public software release

Current package:

**PRAYCG Control Center v0.95 Public**

The Control Center is a Windows dashboard for organizing, launching, monitoring, and reviewing the PRAYCG workflow. It is an orchestrator, not a replacement for PsychoPy, LabRecorder, OpenBCI, BrainFlow, or the individual analysis tools.

Major current components include:

- MediaPrep / StimulusFingerprint v1.9 with ShotOrderScramble support,
- PRAYCG protocol library,
- Master Comprehensive Analysis Suite v1.6.1,
- MasterSync Visualizer v1.4.0,
- Offline Interpreter v1.6.0,
- CAI/SID v0.2 exploratory module,
- Continuous Autonomic / RespDualPath tools,
- Micro Handoff v0.1 exploratory raw-EEG module,
- BrainFlow EEG-only bridge,
- BrainFlow EEG + ALS/PT19 bridge,
- Polar H10 RR-to-LSL bridge,
- Vernier respiration belt-to-LSL bridge,
- ALS/PT19 holder calibration and timing tools,
- optional acquisition preflight and signal-quality checks.

---

## Protocol modules

### PRAYCG3

PRAYCG3 is the standard three-branch protocol:

```text
Baseline 1
→ Phase-scrambled Control
→ washout / report
→ Target
→ washout / report
→ Contextual Override
→ washout / report
→ Baseline 2 / final reflection
→ final report
```

PRAYCG3 is the continuity path from the earlier PRAYCG2 workflow, with cleaner packaging, provenance, readiness checks, and public naming.

### PRAYCG4

PRAYCG4 adds a fourth branch:

```text
Baseline 1
→ Phase-scrambled Control
→ washout / report
→ ShotOrderScramble
→ washout / report
→ Target
→ washout / report
→ Contextual Override
→ washout / report
→ Baseline 2 / final reflection
→ final report
```

The purpose of ShotOrderScramble is to create a structural middle control. Phase scrambling damages narrative order, but it also damages faces, bodies, objects, scene structure, speech, and biological motion. ShotOrderScramble preserves local shots more strongly while disrupting their larger order.

A future strong PRAYCG4 pattern would be:

```text
Target differs from PhaseScrambled,
Target differs from ShotOrderScrambled,
Target differs from Override,
and the result survives timing, artifact, respiration, task, order, and self-report checks.
```

ShotOrderScramble is not a perfect meaning-null condition. It can introduce abrupt cuts, unusual rhythm, novelty, confusion, or familiarity effects. Its purpose is to make interpretation harder to fool, not to guarantee causal proof.

### SMG — Semantic Meaning Gradient

SMG is a separate protocol concept for comparing coherent stimuli with different intended meaning density.

The intended structure is:

```text
low-meaning coherent stimulus
→ high-meaning target stimulus
→ analytic / arithmetic override
```

The low-meaning stimulus should not simply be random noise. Randomness can create novelty, threat, puzzle demand, or prediction error. A proper low-meaning stimulus should be coherent but semantically and emotionally light.

Legally shareable demo media and templates may be added separately when available.

---

## Recommended analysis hierarchy

PRAYCG should not be interpreted from one number or one graph. The analysis is organized as a gated hierarchy.

### Primary path

Use this path first:

```text
Timing / file provenance / stream QC
+ StimulusFingerprint / CET-R
+ artifact and confound review
→ A-MRED / MRED-Peak / MRED-Resolution
```

This is the main endpoint path. A result should not advance if timing, file identity, stream quality, anchor timing, artifact review, or branch provenance fails.

### Confound-defense and context modules

These modules challenge the interpretation before it becomes a claim:

- **HOC-R:** high-order control review, including faces, bodies, objects, local shot structure, and ShotOrderScramble support.
- **OSA:** override spatial-attention review, including cue burden, gaze/AOI concerns, cue legibility, and squint risk.
- **OHC:** order, habituation, fatigue, and carryover review.
- **AAM:** afterglow attribution, especially Target after-state versus task-completion relief.
- **RespDualPath:** respiration as both possible physiology and possible artifact/confound.
- **DGA:** decoder-gate availability, including semantic access, familiarity, confounds, task burden, and subjective availability.
- **CET-R:** stimulus-feature residualization for luminance, audio envelope, cut rate, motion, cues, and other exogenous media properties.

These modules do not automatically “correct” the data. They identify plausible alternative explanations.

### Secondary and exploratory interpretation

Use these after the primary path and confound review:

- **CAA:** Continuous Autonomic Arrays.
- **CAI/SID:** Controlled Access-Integration / State Integration Density.
- **NUPI:** Narrative Update Polarity Index.
- **TTI:** task-theft / task-interference interpretation.
- **NIP / BIT / CII / IAQ:** narrative immersion and attenuation proxies.
- **EET:** Endogenous Echo Tracking.
- **NAST:** Narrative Absorption State Transition.
- **OCM / RSM / CVB / SquintProxy:** cue-task, running-sum, cognitive-visual burden, and artifact context.

These outputs are useful, but they do not override the primary QC path.

### Isolated exploratory raw-EEG module

**Micro Handoff v0.1** is intentionally isolated from the primary chain.

It asks a narrow timing question:

> Is a brief rise in temporal gamma-like activity followed shortly afterward by a rise in theta/integration-like activity?

Micro Handoff is not a consciousness detector, not evidence for 40 Hz conscious frames, and not a “consciousness RPM” gauge.

Its current status is:

```text
software-valid,
construct-unvalidated,
retrospectively mixed.
```

Synthetic tests show the code behaves as intended on artificial data. That does not validate the biological interpretation.

---

## Continuous physiology

PRAYCG v0.95 adds stronger continuous physiology support.

### CAA — Continuous Autonomic Arrays

CAA converts heart, HRV, and respiration into time-resolved traces rather than only branch averages.

It asks questions like:

- When did heart rate change?
- Did HRV rise before, during, or after a scene?
- Was the HRV window long enough to trust?
- Did a sigh or breath hold drive the result?
- Did respiration explain the heart-rate pattern?
- Did the final baseline resemble Target afterglow, task relief, fatigue, or a mixed state?

This is important because respiration can be both a meaningful physiological event and a source of artifact. A breath shift may be part of the response, but it may also contaminate EEG or HRV interpretation.

### CAI/SID — Controlled Access-Integration / State Integration Density

CAI/SID is an exploratory state-density layer.

It estimates whether a time window shows coordinated fast access-like activity, slower integration-like activity, acceptable artifact burden, acceptable task/confound burden, and enough data quality to interpret the window.

It is not a probability, not a validated consciousness measurement, and not proof of narrative reception. Missing or bad data remains missing; it is not treated as favorable evidence.

For public use, **Controlled Access-Integration** is the preferred expansion of CAI. The stronger phrase “Conscious Access” should be avoided unless the non-claim boundary is stated explicitly.

---

## Acquisition and timing stack

The current workflow can include:

- OpenBCI Cyton + Daisy EEG,
- BrainFlow-to-LSL EEG bridge,
- optional ALS/PT19 analog light-sensor timing bridge,
- Polar H10 RR-interval-to-LSL bridge,
- Vernier Go Direct Respiration Belt-to-LSL bridge,
- PsychoPy protocol runner,
- LabRecorder XDF recording,
- PRAYCG Control Center launch/monitoring layer.

### ALS/PT19 timing

The ALS/PT19 layer is a physical display-timing check. It helps verify when light appeared on the screen.

It does **not** validate meaning, EEG quality, consciousness, or hidden biology.

A valid ALS workflow requires:

- sensor aligned to the displayed barcode/pulse region,
- opaque shrouding from room light,
- visible non-clipped pulse in the recorded stream,
- branch-level timing documentation,
- and post-run barcode/timing review.

### Polar H10

The included Polar bridge is used for RR intervals. It should be treated as beat-interval telemetry for HR/HRV analysis, not as a full clinical ECG waveform.

### Vernier respiration belt

The Vernier bridge is intended to preserve raw respiration movement so inhale/exhale phase can be reconstructed offline and aligned with EEG, HR/HRV, and event markers.

---

## What is included

The public package is organized around the Control Center and its bundled tools.

```text
control_center/
  Control Center dashboard, active context, launchers, process manager,
  LSL checks, ALS tests, signal-quality tools, acquisition preflight.

tools/MediaPrep_StimulusFingerprint_v1_9_SHOTORDER/
  Media preparation, cue generation, phase-scrambled control,
  ShotOrderScramble structural control, stimulus QC support.

tools/ProtocolRunner_ModuleLibrary_v1_0/
  PRAYCG3, PRAYCG4, and SMG protocol modules and runner templates.

tools/MasterComprehensiveSuite_v1_6_1_CURRENT/
  Core analysis chain, MRED/A-MRED, DGA, NUPI, TTI, HOC-R,
  OSA/OHC/AAM/RespDualPath, barcode detector, visualizer support,
  offline interpretation support, and chain manifests.

tools/CAI_SID_Exploratory_v0_2/
  Controlled Access-Integration / State Integration Density exploratory module,
  readiness preflight, frozen candidate config, and documentation.

tools/Continuous_Autonomic_RespDualPath_v1_0/
  Continuous HR/HRV/respiration arrays, respiratory event flags,
  HR-respiration coupling, autonomic QC, and synthetic examples.

tools/Micro_Handoff_v0_1/
  Isolated exploratory raw-EEG temporal-gamma/theta handoff module,
  frozen configuration, tests, synthetic validation, and docs.

tools/Offline_Master_Interpreter_v1_6_0/
  Offline rule-based report generator.

tools/Acquisition/
  BrainFlow EEG-only bridge, BrainFlow EEG+ALS bridge,
  Polar H10 bridge, Vernier respiration bridge, and diagnostics.

hardware/ALS_PT19_Holder/
  ALS/PT19 holder design files and placement notes.

validation/
  Build validation and public package checks.
```

Public packages should exclude:

```text
raw private biosignals,
copyrighted stimulus videos,
unredacted self-report,
local machine settings,
private source PDFs,
credentials,
API tokens,
and historical result tables that are not public-safe.
```

---

## Contact pilot / historical examples

Where included, the Contact pilot should be treated as:

```text
gold-plated, but not gold-record.
```

That means it may be useful for showing file layout, output structure, analysis vocabulary, and workflow logic. It is not presented as confirmatory evidence.

Historical self-runs are methods-development cases. They should not be used to claim population-level effects.

---

## Installation quick start

For the current Windows release:

1. Download the latest PRAYCG Control Center release ZIP.
2. Extract the ZIP to a short path, for example:

```text
C:\PRAYCG_CC_v095\
```

3. Install Python 3.11 if needed.
4. Run:

```text
INSTALL_PRAYCG_REQUIREMENTS_v0_95.bat
```

5. Run:

```text
run_PRAYCG_ControlCenter_v0_95.bat
```

6. In the Control Center:

```text
Settings → Use Bundled Paths
Settings → Use Current Python
Settings → Save Settings
```

7. Locate external tools such as PsychoPy and LabRecorder if they are not auto-detected.

PsychoPy and LabRecorder are external applications and are not bundled inside the PRAYCG ZIP.

---

## Recommended workflow

1. Select a legally usable stimulus.
2. Add it to the PRAYCG stimulus library.
3. Run MediaPrep.
4. Review Target, Override, Control, cue schedule, and QC outputs.
5. Manually QC phase-scrambled Control audio.
6. Optionally generate ShotOrderScramble for PRAYCG4 or structural-control studies.
7. Prepare hardware and acquisition streams.
8. Run ALS/PT19 holder calibration and timing preflight if using ALS.
9. Start EEG, Polar H10, Vernier respiration, and marker streams.
10. Open LabRecorder and confirm streams.
11. Run the selected PsychoPy protocol module.
12. Save all run logs, event files, XDF, self-reports, and manifests.
13. Run the Master Comprehensive Analysis Suite.
14. Review primary QC and MRED/A-MRED outputs first.
15. Review confound-defense modules next.
16. Review CAA, CAI/SID, Micro Handoff, and other exploratory outputs last.
17. Generate visualizer and offline interpreter reports.
18. Label the result honestly: valid, cautioned, pilot-only, failed-QC, exploratory, or candidate for prospective replication.

---

## Public interpretation rules

Use cautious language:

```text
Supported:
  “This run produced a Target-dominant exploratory pattern after QC.”
  “This branch showed a stronger after-state candidate than the control.”
  “This result is confounded by respiration / task load / timing / audio access.”
  “This module is software-valid but construct-unvalidated.”

Avoid:
  “This proves consciousness.”
  “This proves meaning was measured directly.”
  “This proves memory formation.”
  “This proves quantum biology.”
  “This proves love as a number.”
```

Self-report is an independent evidence stream. It can constrain or contextualize physiology, but it does not prove internal state by itself. Physiology does not replace first-person experience.

---

## Current development priorities

Near-term priorities:

- simplify installation for outside users,
- improve documentation for non-experts,
- strengthen EOG/EMG artifact controls,
- improve gaze / AOI measurement for Override and cue burden,
- improve ALS/PT19 timing validation on multiple machines,
- prospectively test PRAYCG3 and PRAYCG4 sequence variants,
- use counterbalanced designs rather than only fixed order,
- keep exploratory modules isolated until they pass prospective reliability and validity tests.

Long-term goal:

> Build an open, reproducible, artifact-aware naturalistic EEG/autonomic workbench that makes claims about narrative physiology harder to fool.

---

## Citation

See `CITATION.cff`.

If you reuse synthetic demo materials from this repository, cite this repository. If you generate or use third-party Creative Commons media through included recipes, follow the original creator’s license and attribution requirements.

---

## Contact

Author: Hoyt Banks  
GitHub: <https://github.com/hbanks87/praycg-open>  
OSF: <https://osf.io/8n75v/overview?view_only=928f1fa1974b40e89252101d0ba356d3>

---

## Release alignment

This README is aligned with:

```text
PRAYCG Control Center v0.95 Public
Release date: 2026-09-01
```
