# HumanTranslation_KHT_v0.2 Module Note

## Purpose

The `HumanTranslation_KHT_v0.2` module is a rough Rung-1 human-data translation of the Opto-PING synthetic lock-in logic. It estimates whether a reciprocal loop-like relationship exists between:

```text
E_human(t): EEG gamma / work proxy
Y_HT_proxy(t): human translation proxy, usually TemporalSemanticProxy or posterior-temporal gamma adjusted against task, visual, and artifact terms
V_proxy(t): first difference of Y_HT_proxy(t)
```

The endpoint is:

```text
K_HT = sqrt(eta_{E<-Y} * zeta_{Y<-E})
```

where the parameters are standardized OLS/state-space proxy coefficients in a human-feature table.

## What it does not claim

This module does not estimate `K_OSM`. It does not identify `Y_cell` or `Y_OSM`. It does not prove Opto-Structural Memory, microtubular memory, LTP, dendritic spine growth, quantum memory, biophoton emission, or a human EEG mechanism.

## Required inputs

Minimum:

```text
window feature table or XDF-derived EEG features
segments/phase labels
window timing columns
```

Recommended:

```text
media manifest
StimulusFingerprint folder
cue schedule
annotation CSV
photodiode timing stream
EDA/pupil/raw ECG/EOG/EMG streams
```

## Exogenous input inventory

Media/QC features belong in `u(t)`, not in `Y(t)`. They help prevent the model from mistaking luminance, visual flux, cuts, audio envelope, cue timing, or task demand for a meaning-linked state transition.

## Model comparison

The module fits a full reciprocal model and compares it against simpler alternatives:

```text
full reciprocal
E autoregressive/replay-only
sensory-task-artifact
generic theta/artifact
autoregressive Y-proxy-only
```

This is deliberately minimal in v0.2. Future versions should support true UKF/state-space likelihood, time-resolved media covariate merging, photodiode timing correction, and leave-stimulus-out validation.
