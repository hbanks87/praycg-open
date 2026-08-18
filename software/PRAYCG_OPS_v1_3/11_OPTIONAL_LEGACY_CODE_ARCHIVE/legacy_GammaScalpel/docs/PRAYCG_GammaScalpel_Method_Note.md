# PR-AYC-G GammaScalpel Method Note v1.0

## Purpose

The GammaScalpel analysis was created after Snack Attack Run 1 showed a central problem: the broad 30-45 Hz lower-gamma band can reflect more than one kind of biological work. It may contain task demand, visual attention, artifact, and meaning-related processing in the same frequency range.

## Core decomposition

The working decomposition is:

```text
P_gamma = P_meaning + P_task + P_visual + P_artifact + error
```

The analysis therefore splits gamma by:

1. **Spectral micro-band**: 30-35 Hz, 35-40 Hz, 40-45 Hz.
2. **Spatial ROI**: frontoparietal task, meaning-candidate central/posterior-temporal, visual control, artifact sentinel.
3. **Rigidity feature**: PLV as a phase-lock/task-rigidity marker.
4. **Artifact pressure**: peak-to-peak scores, 45-55 Hz proxy, Fp1/T3/T4 sentinels.
5. **Cue/task context**: number-cue schedule and arithmetic outcome.

## Scores

`TaskGamma` is a candidate task-lock score:

```text
TaskGamma_b = z(frontoparietal power_b) + z(frontoparietal PLV_b) - artifact_composite
```

`MeaningGamma` is a candidate relative openness/payload score:

```text
MeaningGamma_b = z(meaning-candidate power_b) - z(meaning-candidate PLV_b)
                 - 0.5 z(visual-control power_b) - artifact_composite
                 - 0.5 TaskGamma_b
```

These are exploratory indices. They are not validated biomarkers.

## Key limitation

Cue visibility cannot be corrected unless the cue embedding pipeline measures the local contrast behind every number cue. If a white number appears over a bright/white region of the film, the cue may be physically present but functionally unreadable. GammaScalpel currently reports this as a missing QC layer.

## Permitted claim

GammaScalpel may support statements like:

```text
This run showed broad override-dominant gamma power and phase-locking, consistent with analytic task-lock.
```

It must not be used to say:

```text
This frequency is meaning.
```

or:

```text
This frequency proves consciousness, empathy, or a molecular mechanism.
```
