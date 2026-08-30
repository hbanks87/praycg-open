# TSC 2026 PR-AYC-G / OSM Priority Stack

## Objective

Prepare the accepted PR-AYC-G and OSM posters so they are bold, technically credible, and explicitly bounded.

## Tier 1: Must stabilize before TSC

1. **Acquisition stability**
   - Use BrainFlow-to-LSL rather than OpenBCI GUI for acquisition.
   - Run a 10-15 minute full-stack stress test before each important run.
   - Grade EEG timing in every report.

2. **Photodiode / physical display timing**
   - Add a screen-timing sensor to validate actual frame/cue onset.
   - Software LSL markers are necessary but not sufficient for frame-accurate claims.

3. **Artifact veto streams**
   - Add dedicated EOG and jaw/temporal EMG if possible.
   - Treat gamma as biological work, not direct meaning.

4. **Media/QC discipline**
   - Preserve Target/Override hash identity.
   - Keep phase-scrambled control generated from cue-embedded Target.
   - Manually QC speech-shaped control audio for unintelligibility.

5. **Frozen annotations**
   - Freeze semantic/reveal/climax/threat windows before physiology analysis.
   - Mark any reconstructed windows as exploratory only.

## Tier 2: Strongly recommended

1. **EDA/GSR** for arousal/threat/common-drive control.
2. **Raw ECG or validated R-R** for auditable autonomic timing.
3. **Pupil stream** for arousal/attention proxy if available.
4. **Motion/IMU** for posture and head-movement artifact.
5. **StimulusFingerprint v1.5+** for luminance, visual flux, cut rate, and audio envelope covariates.

## Tier 3: Poster strategy

### PR-AYC-G poster

Emphasize:

```text
same-source three-arm design
cue-embedded contextual override
TemporalSemanticProxy as scalp proxy, not source localization
PostPeak / State-Locked PNCC family
HumanTranslation_KHT as rough Rung-1 translation, not OSM proof
```

Avoid:

```text
proof of consciousness
proof of soul
proof of OSM
proof of STS/MTG source localization
proof that gamma is meaning
```

### OSM poster

Emphasize:

```text
conditional mechanism theory
Rung 0 synthetic identifiability ladder
Rung 0J/K locked reproducibility handoff
Hidden-Y taxonomy
K_math versus K_HT versus K_cell versus K_OSM
```

Avoid:

```text
human EEG proves microtubules
biophoton mechanism is established
Rung 0J proves biology
Y(t) has one meaning across all levels
```

## Tier 4: What would most improve the posters

1. One clean new PR-AYC-G run on the new laptop with BrainFlow, locked channel map, full media QC, and frozen annotations.
2. A companion analysis showing the v1.3 suite output, including `HumanTranslation_KHT_v0.2`, even if it reports no clean K_HT pass.
3. An external reproduction of the Rung 0K package by another machine/person.
4. A clean one-page claim boundary handout for poster visitors.

## Final doctrine

The TSC message should be:

```text
We built a disciplined ladder: synthetic identifiability first, human translation second, mechanism-specific cellular evidence later.
```

Not:

```text
We proved OSM with consumer EEG.
```
