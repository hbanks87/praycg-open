# The Future of PRAYCG — Public GitHub Roadmap v1.2

**Version:** 1.2 public clean  
**Prepared:** 2026-08-27T19:25:03Z  
**Status:** Public-facing research roadmap for GitHub and OSF.

## Executive summary

PRAYCG should advance as a staged open-methods program for naturalistic psychophysiology. The project is strongest when it is presented not as a finished theory of consciousness, but as a reproducible workbench for testing how sensory entrainment, narrative reception, analytic task stance, artifact, respiration, and after-state dynamics interact.

The next phase should move from single-operator exploratory runs toward controlled individual replication, then small group replication, then confound-expanded variants using higher-order stimulus controls, eye tracking, EOG/EMG, counterbalanced order, and improved timing validation.

## Current safest thesis

```text
PRAYCG is a theory of availability:
whether a living system is available to decode, receive, integrate, and be changed by a meaningful stimulus.
```

This thesis does not require proving microtubules, biophotons, quantum biology, metaphysics, or clinical mechanism. It requires showing that state trajectories differ across carefully controlled conditions.

## What should remain stable

The core PRAYCG structure should remain:

```text
PhaseScrambled Control
Target
Contextual Override
Baseline and washout windows
Final reflection baseline
Physical display-timing validation
Artifact/confound reporting
Self-report as independent context
```

Future work should not remove the phase-scrambled Control. It is not a perfect meaning-null branch, but it is the first defense against sensory-entrainment overinterpretation.

## Why phase-scrambled Control remains necessary

A movie can drive EEG and autonomic changes through luminance, cuts, audio envelope, rhythm, faces, salience, and shared attention. The phase-scrambled branch asks whether the Target response is reducible to low-level audiovisual drive.

The correct interpretation is not:

```text
Control is meaningless.
```

The correct interpretation is:

```text
Control is meaning-damaged but sensory-active.
```

## Why phase-scrambled Control is not sufficient

Phase scrambling also damages high-order visual structure: faces, bodies, edges, biological motion, and object continuity. Therefore Target > PhaseScrambled could reflect intact face/object/social perception rather than narrative order.

This motivates the high-order structural-control variant.

## Variant 4: High-Order Visual Control / Structural Defense

### Structure

```text
PhaseScrambled -> ShotOrderScramble -> Target -> Override
```

### Rationale

ShotOrderScramble preserves local shots, faces, bodies, objects, voice fragments, and biological motion while disrupting the narrative temporal arc. It is not a replacement for phase scrambling. It is a second control layer.

### Stronger future contrast

```text
Target > PhaseScrambled
Target > ShotOrderScramble
Target > Override
```

at locked anchors and after timing/artifact/confound gates.

### Correct claim

If Target survives ShotOrderScramble, the result becomes less likely to be explained by faces, bodies, objects, or local biological motion alone, and more consistent with narrative-order or temporal-meaning structure.

### Incorrect claim

It would still not “definitively prove meaning.” It would strengthen the interpretation while leaving open artifact, gaze, order, familiarity, and physiology confounds.

## Four-day individual study design

### Day 1 — Acclimation and setup

- Fit cap and sensors.
- Test ALS holder and runner-side barcode.
- Run LabRecorder and stream checklist.
- Run short non-emotional stimulus test.
- Confirm participant can tolerate setup.

### Day 2 — Calibration battery

- Eyes-open baseline.
- Neutral breathing.
- Paced breathing.
- Mild cognitive load.
- Neutral naturalistic media.
- Artifact provocation: blink, jaw, eyes, motion labels.
- Optional EOG/EMG calibration.

### Day 3 — Hypothesis-critical PRAYCG run

- Frame-locked anchors.
- PRAYCG2.1 runner-side barcode.
- PhaseScrambled, Target, Override.
- Optional ShotOrder branch if PRAYCG2.2 is available.
- Full self-report/confound reports.
- No public claim if timing/QC fails.

### Day 4 — Recovery / retest

- Baseline retest.
- Short Target-memory/reactivation check.
- Debrief.
- Withdrawal option.
- Confound review.
- Post-run qualitative interview.

## Group-study roadmap

### Stage 0 — Software/hardware validation

Run synthetic and local pilot workflows until:
- ALS barcode passes,
- stream watchdog passes,
- MediaPrep outputs validate,
- Control audio QC passes,
- visual QC passes,
- offline interpreter outputs are understandable.

### Stage 1 — Small N feasibility

Use 8–12 participants to estimate variance, artifact rate, task compliance, comfort, and timing success.

### Stage 2 — Counterbalanced replication

Use counterbalanced orders:
```text
Control -> Target -> Override
Control -> Override -> Target
PhaseScrambled -> ShotOrder -> Target -> Override
```

### Stage 3 — Confirmatory endpoint

Preregister:
- primary anchors,
- bands/channels/features,
- timing gates,
- artifact thresholds,
- Target > Control / Target > ShotOrder / Target > Override contrasts,
- self-report as covariate rather than proof.

## Required hardware upgrades

High-priority:
- EOG
- EMG/jaw or forehead artifact channel
- robust ALS/PT19 holder
- runner-side ALS barcode
- stable OpenBCI stream monitoring
- eye tracking or at least webcam gaze proxy

Useful:
- EDA/GSR
- pupilometry
- higher-density EEG
- better headphones or controlled audio

## Software roadmap

### PRAYCG2.1

Runner-side ALS barcode before each branch.

### PRAYCG2.2

Four-branch protocol support:
```text
PhaseScrambled
ShotOrderScramble
Target
Override
```

### MediaPrep v1.9+

ShotOrderScramble generator:
- detect shots,
- shuffle shot order,
- apply same cue schedule after shuffle,
- write shot table and QC report.

### Master Suite v1.6+

Unify:
- A-MRED,
- MRED-Peak/Resolution,
- NUPI,
- DGA,
- HOC-R,
- OSA,
- OHC,
- AAM,
- RespDualPath,
- ALS barcode detector,
- ShotOrder condition handling.

## Institutional deployment

The best academic home is not only psychology and not only computer science. The ideal home is:

```text
cognitive neuroscience / neuroaesthetics / media psychology
+ biomedical engineering / signal processing / machine learning collaboration
```

The psychological side is needed for stimulus design, self-report, experience, narrative theory, and ethics. The engineering side is needed for timing, artifacts, LSL, signal processing, classifiers, and reproducibility.

## Ethics and public release

- Do not use copyrighted stimuli in public repositories.
- Do not publish raw private biosignal data without consent and proper review.
- Do not call self-run data confirmatory.
- Do not present speculative mechanism as established biology.
- Keep OSM/cellular/microtubule content quarantined from PRAYCG empirical claims.
- Use clear participant consent and debriefing for any human study.

## Bottom line

PRAYCG’s future is not to become a grand proof machine. Its future is to become a stricter measurement workbench:

```text
Can we tell when the nervous system is tracking sensory structure,
when it is receiving meaning,
when task stance changes reception,
and when an after-state persists beyond the stimulus?
```

That is enough. It is testable, useful, and worth building.
