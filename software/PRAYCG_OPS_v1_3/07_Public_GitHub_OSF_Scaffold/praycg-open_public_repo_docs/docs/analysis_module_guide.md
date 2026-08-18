# Master Comprehensive Analysis Suite - module guide

This file is the short public guide. The full TSC handout should be placed under `docs/tsc_handouts/`.

## Module families

### 1. Stream inventory and timing QC

Checks which streams are present, estimates sample rates, detects obvious gaps, and verifies whether required LSL streams were recorded.

### 2. ALS-PT19 timing QC

Checks whether the physical display-timing pulse appears in the ALS stream. The ALS signal validates screen timing and belongs to `u(t)`, not biological `Y(t)`.

### 3. EEG windowed feature extraction

Computes time-resolved EEG band features. These are used by later modules and by the visualizer feature CSV.

### 4. GammaScalpel

Slices gamma-like activity into small bands rather than treating gamma as a single broad bucket. Typical bands include:

```text
20-25 Hz
25-30 Hz
30-35 Hz
35-40 Hz
40-45 Hz
45-50 Hz
50-55 Hz
```

The module compares band behavior across Control, Target, and Override while applying artifact penalties.

### 5. TemporalSemanticProxy (TSP)

TSP is a scalp-level posterior-temporal semantic-load proxy. It is not STS/MTG localization. It tests whether posterior-temporal features behave differently from visual-control and artifact-sensitive features during narrative state transitions.

### 6. TSP-to-theta handoff

Finds TSP peaks, identifies taper points, then tests whether theta carryover follows in a non-overlapping later window.

### 7. Gamma-to-theta handoff

Similar to TSP-to-theta, but starts from gamma or lower-gamma peak/taper behavior.

### 8. PNCC theta family

Separates post-video washout carryover, annotation-locked carryover, and post-peak carryover.

### 9. API_A_v1

Autonomic availability proxy. It combines lower heart strain, higher variability, and lower acceleration/instability where those features are available. It is not a clinical diagnostic index.

### 10. HumanTranslation_KHT

A human-translation coupling proxy between EEG work signals and a TSP-like latent state. It is not `K_OSM`.

### 11. CandidateLocal_KHT

Event-level module that estimates local reciprocal coupling around candidate anchors and tests whether theta carryover follows.

Core rule:

```text
K alone is not enough.
Theta handoff alone is not enough.
Final human-event lock requires local coupling + theta carryover + condition specificity + artifact/timing pass.
```

### 12. MasterSync Visualizer

Renders synchronized stimulus video and scrolling graphs from feature CSVs plus event overlays.

Important distinction:

```text
Analysis folder:
  root Master Suite output folder containing overlay/event tables.

Feature CSV:
  continuous time-resolved table used to draw theta/gamma/HR/HRV/API/respiration/ALS.
```

## Claim levels

```text
confirmatory:
  predeclared anchor/rule, valid timing, artifact pass, condition specificity.

secondary:
  planned but not primary.

exploratory:
  discovered after seeing physiology.

future-freeze:
  exploratory event now converted into a future predeclared anchor.
```
