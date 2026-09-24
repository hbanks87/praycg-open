# NAST_v0.1 - Narrative Absorption State Transition

NAST is an EEG-proxy state-transition module. It does **not** claim to directly measure the fMRI-defined Default Mode Network. It asks whether the viewer moves from idle/passive sensory processing into a sustained narrative-absorption proxy state.

## Core features

- `alpha_proxy_z`: posterior/parietal/primary alpha proxy, interpreted cautiously as internal-idle / disengagement proxy.
- `alpha_drop_z`: local decrease in alpha over a rolling pre/post window.
- `meaning_gamma_z`: lower-gamma meaning-work proxy.
- `tsp_z`: TemporalSemanticProxy.
- `task_gamma_z`: frontoparietal analytic-task gamma proxy.
- `artifact_z`: artifact penalty.
- `visual_gamma_z`: visual/sensory-control gamma proxy.
- `api_a_z`: optional autonomic availability proxy.

## Default score

```text
NAS(t) = 0.30 z(alpha_drop)
       + 0.25 z(MeaningGamma)
       + 0.25 z(TSP)
       + 0.10 z(API_A)
       - 0.20 z(TaskGamma)
       - 0.20 z(Artifact)
       - 0.10 z(VisualGamma)
```

A window becomes a candidate when NAS exceeds the baseline/control null threshold and artifact remains below the artifact veto threshold. A sustained candidate requires repeated candidate windows in a short neighborhood.

## Transition contrasts

The module reports:

```text
BASELINE_1 -> CONTROL_1
WASHOUT_1 -> TARGET_1
WASHOUT_2 -> CONTEXTUAL_OVERRIDE_1
```

Interpretation:

- Baseline -> Control: sensory capture / exogenous load.
- Washout 1 -> Target: narrative absorption candidate.
- Washout 2 -> Override: analytic-task state transition.

## Boundary

Alpha suppression alone is not narrative absorption. Control can suppress alpha through sensory capture. A stronger target-absorption candidate requires alpha suppression plus MeaningGamma/TSP rise and non-dominant task/artifact/sensory explanations.
