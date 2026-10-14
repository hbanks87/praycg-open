# Immersion, stimulus entrainment and later echoes

NIP describes the joint presence of attention-like and delayed integration-like features. CET asks whether measured responses track the media or cue rhythm. CET-R asks what remains after modeling that external drive. EET asks whether an earlier feature pattern resembles a later after-state. These are related questions, with different inputs and different failure modes.

[Concept guide](README.md) · [Current algorithm map](../algorithms/README.md) · [Recognition and integration](recognition-integration.md) · [Update polarity](update-availability.md)

## Version and input frame

The [v1.5.1 NIP/CET/EET note](../measures/originals/master-suite-v1-5-5/NIP_CET_EET_Method_v1_5_1.md) gives the conceptual relationships. The equations below reproduce [Formula and Module Report v1.0, sections 16–19 and 28–30](../collections/public-docs/Formula_Module_Report_v1_0/PRAYCG_Formula_Module_Report_v1_0.md), whose stated scope is Master Comprehensive Suite v1.5.5. They are historical method definitions, not a claim that every branch in the proposed Public Alpha 11.2.1 code uses every displayed term.

Inputs are synchronized feature time series, branch/anchor windows, quality and timing information, and media/cue regressors when supplied. `rz` is robust standardization against a declared reference, `clip_plus(x)=max(0,x)`, and `ell` is the declared integration lag. The report specifies `alpha=beta=1` for NIP, but leaves the component weights and lag symbolic in these equations. Reproduction requires the versioned implementation/configuration that resolves them.

## NIP: attention-like support multiplied by integration-like support

The semantic-attention component is:

```text
A_sem(t) = clip_plus(
      w_G*rz(MeaningGamma(t)) + w_T*rz(TSP(t)) + w_N*rz(NAST(t))
    - w_V*rz(VisualDrive(t)) - w_A*rz(ArtifactScore(t)) - w_X*rz(TaskGamma(t))
)
```

The integration/resonance component is:

```text
R_int(t) = clip_plus(
      w_H*rz(H_theta(t)) + w_K*rz(KHT_topo(t))
    + w_TOPO*rz(TopoShift(t)) + w_API*rz(API_A(t))
    - w_A*rz(ArtifactScore(t))
)
```

The report then defines Narrative Immersion Proxy density:

```text
NIP_density(t) = A_sem(t)^alpha * R_int(t + ell)^beta * Penalty(t)
Penalty(t) = ArtifactPass(t) * ConfoundPenalty(t) * TimingPass(t)
alpha = 1
beta = 1
```

The multiplication makes the intended distinction explicit: high attention alone cannot compensate for a zero integration component. The lag makes temporal alignment part of the construct. The factor called `Penalty` here is retained-support multiplication: a failed gate can reduce the product. This differs from CAI v0.2's separately defined penalty average, which is subtracted from one. Shared terminology does not imply shared algebra.

These features remain proxies. NIP does not measure dopamine, oxytocin, proprietary immersion biology or subjective experience directly. Artifact and task inputs can overlap with the features being summarized; inspect their contribution rather than interpreting a high composite in isolation.

## BIT, CII and IAQ/ITQ answer different summary questions

**Bivariate Immersion Threshold (`BIT`)** is an event-level AND gate:

```text
BIT_j = 1[A_sem_j > theta_A]
      * 1[R_int_j > theta_R]
      * 1[Artifact_j < theta_artifact]
      * 1[Specificity_j = 1]

Specificity_j = 1[Target_j > Control_j + delta]
              * 1[Target_j > Override_j + delta]
```

Every required condition must pass. The specific feature aggregation, thresholds and margin belong to the declared recipe; the symbolic specification does not supply validated universal cutoffs. High recognition without integration fails this operational gate.

**Continuous Immersion Index (`CII`)** averages NIP density over a declared anchor window `W_j`:

```text
CII_condition(W_j) = integral_Wj NIP_density_condition(t) dt / |W_j|
CII_margin_j = CII_T,j - max(CII_C,j, CII_O,j)
```

The report's discrete form is the mean of samples in the window. That approximates the duration mean on an appropriate time grid; irregular timestamps or missing windows require an explicit time/coverage policy. Normalization by duration prevents a longer scene from automatically receiving a larger total solely because it lasts longer.

**Immersion Attenuation Quotient (`IAQ`)** and its difference companion compare Target with Override:

```text
IAQ_j = 1 - (CII_O,j + eps) / (CII_T,j + eps)
ITQ_j = CII_T,j - CII_O,j
```

The original report calls ITQ an “equivalent difference form.” It is a related contrast, but the displayed expressions are not numerically equal: IAQ is a ratio-based attenuation, while ITQ retains the CII difference scale. Record which one was computed. The size of `eps` and behavior near a small Target denominator affect IAQ and must be specified.

Under the intended nonnegative CII interpretation, IAQ near one indicates strong attenuation in Override, near zero indicates similar values, and below zero indicates a larger Override value. None of these establishes why the conditions differ. Task demands, cue monitoring, gaze, stimulus drive and condition order remain competing explanations.

## CET: measure external tracking before attributing meaning

Cinematic Entrainment Tracking (`CET`) uses stimulus streams such as audio envelope, luminance, visual change, cuts and cues, aligned to EEG. Formula Report v1.0 defines their short-time Fourier transforms and coherence:

```text
U_m(f,tau) = STFT[u_m(t)]
X_ch(f,tau) = STFT[x_ch(t)]
Coh_u,x(f,tau) = |S_u,x(f,tau)|^2 / (S_u,u(f,tau)*S_x,x(f,tau) + eps)
phi_u,x(f,tau) = angle(S_u,x(f,tau))
lag_u,x(f,tau) = phi_u,x(f,tau) / (2*pi*f)
```

Cross-spectrum estimation, windows, frequency and phase conventions are essential to reproducing a lag. A stable lag or coherence can indicate stimulus tracking; it does not establish semantic integration or a stalled biological state. A physical display/ALS signal belongs on the stimulus/timing side of this comparison, not as a direct internal optical measurement.

## CET-R: model external drive, then inspect the residual

For a candidate feature `Y(t)` such as NIP, MeaningGamma, TSP, MR or ENC, the report defines:

```text
Y(t) = beta0 + beta_u^T U(t) + beta_art*Artifact(t) + eps(t)
Y_resid(t) = Y(t) - Y_hat(t)
```

Candidate columns in `U` include audio envelope, luminance, visual change, optical flow, cut/flash trains, cue onset/value/phase and ALS pulses. Only actually available, declared regressors can be used. Their absence is a limitation, not evidence that external drive was eliminated.

The specified blocked cross-validation score is:

```text
R2_blocked = 1 - sum((Y_test - Y_hat_test)^2)
                  / sum((Y_test - mean(Y_train))^2)
CII_resid(W_j) = mean_Wj(clip_plus(Y_resid(t)))
```

Time blocks reduce leakage from neighboring samples. A Target-dominant residual is a narrower candidate effect after the fitted explanation. Poor held-out prediction means these regressors did not generalize as an explanation; it does not prove the remainder is meaning. Unmeasured drive, inadequate regressors and model misspecification remain possibilities. Residualizing can also remove variance shared with the response of interest, so retain both raw and residualized results.

## EET: resemblance of an anchor state and an after-state

Endogenous Echo Tracking (`EET`) compares vectors with the same feature definitions and scaling:

```text
StateVec_anchor,j = [MR, ENC, NIP, TSP, MeaningGamma, Theta, Alpha, API_A, HRV, Resp, ...]_Wj
StateVec_after,q  = [same features]_Wq

EET_j,q = dot(V_j,V_q) / (norm(V_j)*norm(V_q) + eps)
DeltaEET_j = EET_Target-anchor-j->B2 - EET_Control-matched-window-j->B2
```

Cosine similarity describes vector alignment, not necessarily equal magnitude. Feature inclusion, normalization and missingness can change that alignment. Shared features also connect EET to upstream MRED/NIP/NUPI calculations, so an echo is not an independent physiological channel.

The result supports a statement about feature-pattern resemblance under the declared comparison. It does not prove memory replay or establish that Target uniquely caused Baseline 2. The [protocol methods supplement](../protocols/originals/docs/PRAYCG_v0_93_to_v0_95_Protocols_Theory_and_Analysis_Methods.md) explains why the fixed-order final after-state may include cumulative exposure, task relief, fatigue, breathing and drift.

## What to retain with a reported result

Keep the component time series and artifact/timing gates with the NIP summary; window duration and coverage with CII; the actual ratio or difference definition with IAQ/ITQ; regressor availability, held-out performance and raw/residualized effects with CET-R; and feature/scaling/matched-window provenance with EET. The [implementation map](../algorithms/README.md) identifies version-specific table outputs and code locations. The preserved equations explain the intended research logic, while those implementation records determine what a particular run actually calculated.
