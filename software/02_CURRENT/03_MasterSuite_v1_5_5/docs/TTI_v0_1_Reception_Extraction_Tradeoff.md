# TTI_v0.1 - Thermodynamic Theft Index / Reception-Extraction Tradeoff

## Status

Exploratory PR-AYC-G human-scale analysis module. This is not a moral score, clinical score, consciousness proof, or OSM biology proof.

## Core principle

Deep receptive absorption and high-load instrumental extraction compete for finite cognitive/autonomic budget when they target the same semantic payload. They can alternate, partially overlap, or coexist at low load, but they cannot both be maximized at the same moment under finite capacity.

## Formal budget statement

```text
c_R R(t) + c_X X(t) + c_M M(t) + c_Gamma Gamma(t) + c_RX R(t)X(t) <= B(t)
```

Where:

- `R(t)` = receptive narrative absorption / availability.
- `X(t)` = extractive or instrumental task stance.
- `M(t)` = semantic payload.
- `Gamma(t)` = metabolic / task exhaust.
- `B(t)` = available cognitive/autonomic budget.
- `c_RX R(t)X(t)` = collision cost when reception and extraction target the same payload.

## Dynamic form

```text
dR/dt = alpha_M M(t)(1-R) + alpha_A A(t)
        - beta_X X(t)R(t) - beta_Gamma Gamma(t)R(t) - lambda_R R(t)

dX/dt = alpha_T T(t)(1-X) + alpha_C Cue(t)
        - beta_R R(t)X(t) - lambda_X X(t)
```

## TTI composite

```text
TTI = w1 z(MR_Target - MR_Override)
    + w2 z(ENC_Target - ENC_Override)
    + w3 z(API_Target - API_Override)
    + w4 z(X_Override - X_Target)
    - w5 z(|Artifact_Target - Artifact_Override|)
    - w6 z(|VisualDrive_Target - VisualDrive_Override|)
```

Default v1.4.8 weights:

```text
MR:       0.28
ENC:      0.24
API-A:    0.14
X-load:   0.22
Artifact: 0.08 penalty
Visual:   0.04 penalty
```

## Interpretation

Positive TTI means the Target condition preserved more receptive meaning/integration while Override carried more extractive/task load.

Positive TTI does not mean Override erased meaning. It may mean Override rerouted or attenuated meaning into task extraction, cue maintenance, arithmetic burden, or analytic stance.

## Required interpretive checks

TTI cannot be interpreted without reviewing:

- Target/Override stimulus identity.
- Control validity.
- ALS / display timing.
- Artifact score.
- Respiration/common-drive controls when available.
- Cue visibility / RSM / OCM outputs for Override.
- Audio-video sync and acoustic intrusion confounds.
- Self-report consistency.
- Anchor status: runner-registered vs conceptually predeclared vs exploratory.

## Output files

The TTI module writes:

```text
tti_component_summary.csv
tti_global_summary.csv
tti_timewindow_paired_deltas.csv
tti_event_summary.csv
tti_ocm_extraction_summary.csv
tti_confound_context.csv
tti_visual_overlay.csv
tti_interpretation.json
```

## Falsification logic

The TTI claim weakens if:

- Override has equal or stronger MR/ENC than Target.
- Control explains the same pattern.
- Artifact, visual drive, respiration, cue burden, audio desync, or external noise explains the difference.
- Self-report indicates no absorption in Target or no task engagement in Override.
- Simpler models explain the data better.
