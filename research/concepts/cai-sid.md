# Controlled Access-Integration Index and state density

CAI v0.2 asks whether specified fast access-like and slower integration-like features exceed their own Baseline 1 references while surviving artifact and task-load penalties. SID summarizes that candidate score over time. They make a declared composite inspectable; they do not turn it into a direct measure of consciousness or meaning.

[Concept guide](README.md) · [Current algorithm map](../algorithms/README.md) · [Availability/context](update-availability.md) · [Protocols](../protocols/README.md)

## Source, version and prerequisites

The formulas below follow [the v0.93–v0.95 protocol/theory methods supplement, common notation and section 4](../protocols/originals/docs/PRAYCG_v0_93_to_v0_95_Protocols_Theory_and_Analysis_Methods.md). CAI means **Controlled Access-Integration Index**, and SID means **State Integration Density**. The earlier v0.1 hand-weighted logistic proposal is historical; it is not the v0.2 core defined here.

Inputs are synchronized, quality-checked feature rows with a usable Baseline 1 reference, contiguous block identity, fast/slow candidate features, artifact measures and task-load evidence. General gamma is not automatically measurement-equivalent to MeaningGamma. The selected source columns, adapters and evidence grades belong to the result.

The preferred normalization is:

```text
MAD_B1(x) = median_B1(abs(x - median_B1(x)))
z_B1(x_t) = 0.67448975*(x_t - median_B1(x)) / MAD_B1(x)
```

The implemented candidate clips transformed values at ±6. A full-run fallback is limited to explicitly graded legacy CAI inputs and is recorded. Degenerate reference distributions, missing inputs and source substitutions require the version's actual handling; the equation is not permission to create a favorable value. Here `sigmoid(x)=1/(1+exp(-x))`, `[x]+=max(x,0)`, and `clip01` clips to `[0,1]`.

## Fast and slow components

Let `z_M`, `z_T`, `z_N` and `z_V` be standardized MeaningGamma, TSP, optional NIP and VisualGamma. `I_j=1` when a positive input is available and zero otherwise. The fast component uses an available-input weighted mean:

```text
L_E(t) = (0.45*I_M*z_M + 0.35*I_T*z_T + 0.20*I_N*z_N)
           / (0.45*I_M + 0.35*I_T + 0.20*I_N)
         - 0.10*[z_V(t)]+
E(t) = sigmoid(L_E(t))
```

Renormalization over available positive inputs is a defined operation; it does not permit replacing all unavailable fast evidence with zero. VisualGamma contributes the declared nonnegative visual-drive penalty. The slow component is:

```text
L_Y(t) = 0.50*z_theta(t) + 0.30*z_NAS(t) + 0.20*z_alpha(t)
Y(t) = sigmoid(L_Y(t))
```

These inputs represent theta integration, NAS and posterior alpha candidate families. The feature names do not prove comprehension or memory consolidation. For current adapters and the separately versioned NAST derivation available in the managed pipeline, use the [implementation map](../algorithms/README.md).

## Delayed support is retrospective

Within the same contiguous block instance `b`:

```text
Y_future(t) = mean(Y(s) for s in b with t+8 <= s <= t+30)
```

At least five future samples are required. The method does not fill the branch end with a median when future coverage is insufficient. Those values become missing. Consequently, completed CAI is an offline retrospective quantity, not a causal live readout. Ordinary live EEG/RR capture alone is insufficient to establish that all required analysis features, reference distributions, future coverage and QC are available.

## Positive product and local association

The v0.2 product uses only above-neutral evidence:

```text
e_plus(t) = [E(t) - 0.5]+
y_plus(t) = [Y_future(t) - 0.5]+
K_product_plus(t) = 2*sqrt(e_plus(t)*y_plus(t))
```

If either component is at or below 0.5, the **product term** is zero. That AND-like property prevents jointly low values from contributing through the product merely because they resemble each other. It does not assert that the entire correlation-blended `K` below must be zero.

When local correlation is estimable in the declared 31-second window:

```text
rho_plus(t) = [corr_local(E,Y_future)]+
K(t) = 0.70*K_product_plus(t) + 0.30*rho_plus(t)
```

When it is not estimable, `K=K_product_plus`. Local correlation remains an association of derived features; it is not causal direction, a state-space coupling parameter, or the same `K` as the Opto-PING/KHT models. Shared symbols must not erase those distinctions.

## Artifact, task and the primary composite

The artifact latent uses only available standardized artifact components under the defined weighted-available rule:

```text
L_A(t) = weighted_available(0.55*z_artifact, 0.25*z_HF, 0.20*z_P2P)
A(t) = sigmoid(L_A(t))
X(t) = sigmoid(z_task(t))
A_plus(t) = clip01(2*(A(t) - 0.5))
X_plus(t) = clip01(2*(X(t) - 0.5))
```

Hard QC fails for standardized artifact or high-frequency sentinel values above 5, or P2P above 5 when available. Hard-failed rows are missing, not zero. The primary calculation is:

```text
E_plus(t) = clip01(2*(E(t) - 0.5))
Y_plus(t) = clip01(2*(Y(t) - 0.5))
Support(t) = (E_plus(t) + Y_plus(t) + K(t))/3
Penalty(t) = (A_plus(t) + X_plus(t))/2
CAI_core(t) = Support(t)*(1 - Penalty(t))
```

The direct slow-support term uses current `Y(t)`; the product/association term uses `Y_future(t)`. This timing distinction is part of the recipe. Required unavailable fast, slow, loop, artifact or task values leave primary CAI missing.

Each displayed support/penalty component is bounded, which bounds the core to `[0,1]`. This mathematical bound is not empirical probability calibration. A value of 0.7 does not mean a 70% probability of consciousness, meaning, comprehension or memory formation.

## Context and autonomic evidence remain separate

With independent context/DGA information, the supplement defines:

```text
Reliability_context = D_gate*(1 - ConfoundLoad)*(1 - ExtractionLoad)
CAI_context_gated = CAI_core*Reliability_context
```

This is an attribution-confidence sensitivity output, not a replacement for primary CAI or an independent physiological channel. Autonomic/respiratory series likewise retain their own quality, interpolation and confound rules rather than being silently inserted into the v0.2 primary equation.

## Time summaries and the SID denominator

The methods supplement defines these summaries over valid support:

```text
Mean_CAI = integral CAI_core(t) dt / T_valid
CAI_load = integral CAI_core(t) dt
CAI_occupancy(tau) = valid_time{CAI_core(t) >= tau} / T_valid
```

Its exploratory occupancy threshold is `tau=0.50`, not a validated state boundary. It also gives the general nominal-interval expression:

```text
SID_[a,b] = integral_a^b CAI_core(t) dt / (b - a)
```

The supplement's nominal interval denominator and a valid-time denominator differ when data are missing. Do not use a favorable value, silently bridge a gap, or treat missing CAI as an observed zero. Report valid coverage, integration conventions and the actual denominator with the result.

The **managed implementation in the proposed Public Alpha 11.2.1 package uses timestamp-weighted valid-time SID**. It retains CAI equation version `0.2.0` while identifying managed/core revisions separately. See the [implementation map](../algorithms/README.md) for exact paths and version strings; the historical general expression above must not be presented as a complete description of that current aggregation.

The supplement's moving-block bootstrap uses 30-second blocks and 1,000 replicates. Such intervals describe temporal stability within the observed run. Repeated time rows and bootstrap replicates do not create independent participants or population evidence.

## What a result can say

A completed CAI result can state that the declared proxy features jointly supported the operational v0.2 composite under its reference, timing, penalty and coverage rules. It should retain the fast/slow/product/correlation/artifact/task components, source grades, missingness and context sensitivity. Agreement with MRED or NIP partly reflects shared inputs and is not independent validation. Prospective tests and independent construct validation remain separate steps in the [research ladders](../ladders/README.md).
