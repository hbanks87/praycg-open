# PRAYCG v0.93–v0.95: Protocols, Theory, and Exploratory Analysis Methods

**Detailed public methods supplement for PRAYCG Control Center**  
**Author:** Hoyt Banks  
**Contact:** hoytbanks@gmail.com  
**Repository:** [hbanks87/praycg-open](https://github.com/hbanks87/praycg-open)  
**OSF project:** [PRAYCG, project 8n75v](https://osf.io/8n75v/overview?view_only=928f1fa1974b40e89252101d0ba356d3)  
**Document status:** Public-facing technical explanation of implemented, proposed, and exploratory components through Control Center v0.95  
**Documentation license:** CC BY 4.0 unless a file states otherwise

## Executive summary

Versions v0.93–v0.95 moved PRAYCG from one hard-coded experiment toward a modular research framework. The additions were made to answer different questions that one comparison cannot answer by itself:

1. **PRAYCG3** retains the original three-condition logic: damaged sensory/narrative structure, intact target, and intact target under an analytic working-memory task.
2. **PRAYCG4** adds a ShotOrder structural control so local shots can remain recognizable while their larger temporal order is disrupted.
3. **Semantic Meaning Gradient (SMG)** asks whether responses scale across a deliberately low-meaning state, a high-meaning target, and the same target under arithmetic override.
4. **CAI/SID v0.2** converts fast access-like activity, slower integration-like activity, delayed joint support, artifact, and task burden into a bounded exploratory index.
5. **Continuous Autonomic/RespDualPath v1.0** replaces coarse branch-level autonomic labels with time-resolved cardiac and respiratory measurements, while preserving respiration as both physiology and a possible artifact source.
6. **The prospective package** creates fixed Williams-design sequence variants, deterministic assignment, hashing, preregistration materials, and promotion gates without changing the public fixed-order protocols.
7. **Micro Handoff v0.1** operationalizes a narrower hypothesis: whether local temporal-gamma activation is followed over a fixed short-lag bank by posterior/parietal-temporal theta activation.
8. **HOC-R, OSA, OHC, AAM, and RespDualPath** make alternative explanations visible instead of allowing a Target difference to be interpreted automatically as meaning, narrative reception, or persistent state change.

The central methodological principle is that **software-valid does not mean construct-valid**. A formula can be implemented correctly and still fail to measure the intended phenomenon. Every new measure therefore retains an evidence grade, a missing-data policy, falsification conditions, and a public claim boundary.

## How to read the status labels

| Label | Meaning |
|---|---|
| **Implemented protocol** | The runner and manifest exist and can acquire a study using the declared sequence. |
| **Implemented exploratory analysis** | The code computes the declared output reproducibly, but the construct has not been prospectively validated. |
| **Prospective template** | The software infrastructure exists, but real stimuli, approvals, apparatus validation, registration, or participant data are still required. |
| **Proposed formula** | A theory document defines the quantity, but the current runner or analysis does not compute it as a validated endpoint. |
| **Diagnostic** | Useful for inspection or sensitivity analysis; not a confirmatory endpoint. |
| **Unavailable/missing** | The evidence was not estimable. It must not be converted to a favorable zero or a favorable score. |

## Common notation

Let (t) denote synchronized PRAYCG time, (i) a participant or run, (b) a contiguous block instance, and (c) a condition. Define:

$$
\sigma(x)=\frac{1}{1+e^{-x}},
\qquad
[x]_+=\max(x,0),
\qquad
\operatorname{clip}_{[0,1]}(x)=\min(1,\max(0,x)).
$$

The preferred within-run Baseline 1 robust transform is

$$
z_{B1}(x_t)
=0.67448975\frac{x_t-\operatorname{median}_{B1}(x)}{\operatorname{MAD}_{B1}(x)},
$$

where

$$
\operatorname{MAD}_{B1}(x)
=\operatorname{median}_{B1}\left|x_t-\operatorname{median}_{B1}(x)\right|.
$$

The constant (0.67448975) makes the median/MAD transform comparable in scale to an ordinary standard score under a normal reference distribution. In the implemented CAI candidate, transformed values are clipped at (pm6). A full-run fallback is permitted only for explicitly graded legacy CAI inputs and is recorded. Micro Handoff allows no full-run fallback.

---

## 1. PRAYCG3 v3.0 — original three-prong protocol

### Implemented sequence

PRAYCG3 preserves the original fixed-order acquisition structure:

```text
BASELINE_1
→ CONTROL_1
→ WASHOUT_1 → control report
→ TARGET_1
→ WASHOUT_2 → target report
→ CONTEXTUAL_OVERRIDE_1
→ WASHOUT_3 → override report
→ BASELINE_2_REFLECTION
→ final report
```

`CONTROL_1` is the PhaseScrambled control. `TARGET_1` is the natural target. `CONTEXTUAL_OVERRIDE_1` uses the same cue-embedded target media while the participant performs the running-sum task. Baseline 1, Baseline 2/final reflection, every washout/report, and the final report are retained.

### What each comparison asks

For an outcome (Y), define condition summaries (\bar Y_P), (\bar Y_T), and (\bar Y_O) for PhaseScrambled, Target, and Override:

$$
\Delta_{T-P}=\bar Y_T-\bar Y_P,
$$

$$
\Delta_{T-O}=\bar Y_T-\bar Y_O.
$$

- (\Delta_{T-P}) asks whether the intact target differs from a control in which recognizable and high-order structure has been damaged.
- (\Delta_{T-O}) asks whether the response differs when the same target is viewed under a competing analytic/working-memory stance.

Neither contrast identifies “meaning” by itself. Target versus PhaseScrambled changes more than meaning, while Target versus Override changes task demands, cue monitoring, and possibly visual sampling.

### Why Baseline 1, washouts, and Baseline 2 matter

Baseline 1 defines the run-local reference distribution. Washouts are treated as measured post-condition states, not blank intervals and not guaranteed biological resets. Baseline 2/final reflection asks whether the final state differs from the initial baseline after the entire sequence:

$$
\Delta B_2(Y)=\operatorname{summary}(Y_{B2})-\operatorname{summary}(Y_{B1}).
$$

This is a **cumulative after-state contrast**. Because Baseline 2 follows all three branches, it cannot be attributed uniquely to Target. It may include Target carryover, Override relief, fatigue, habituation, respiration, cumulative exposure, or drift.

### Fixed-order limitation

In the public PRAYCG3 runner, condition and period are inseparable. A conceptual decomposition is

$$
\widehat\Delta_{a-b}
=(\tau_a-\tau_b)
+(\pi_{p(a)}-\pi_{p(b)})
+(\lambda_{\mathrm{prev}(a)\to a}-\lambda_{\mathrm{prev}(b)\to b})
+\varepsilon,
$$

where (\tau) is the condition effect, (\pi) is the period/fatigue/habituation effect, and (\lambda) is carryover from the preceding branch. One fixed sequence cannot estimate these terms separately. This is why the public fixed-order runner remains useful for continuity and exploratory within-run description, while the prospective package uses counterbalanced variants.

### Plain-language explanation

PRAYCG3 asks three practical questions: What happens when the media is structurally damaged? What happens when it is watched naturally? What happens when the same meaningful media must compete with a deliberate arithmetic task? It preserves the original protocol so older and newer data remain structurally comparable, but its fixed order prevents strong causal claims about condition alone.

---

## 2. PRAYCG4 v4.0 — adding ShotOrder structural control

### Implemented sequence

PRAYCG4 inserts ShotOrder immediately after the completed PhaseScrambled washout/report:

```text
BASELINE_1
→ CONTROL_1
→ WASHOUT_1 → control report
→ SHOT_ORDER_SCRAMBLE_1
→ SHOT_ORDER_WASHOUT_1 → ShotOrder report
→ TARGET_1
→ WASHOUT_2 → target report
→ CONTEXTUAL_OVERRIDE_1
→ WASHOUT_3 → override report
→ BASELINE_2_REFLECTION
→ final report
```

### Formal ShotOrder operator

Let the intact target be divided at declared shot boundaries into (m) local segments:

$$
V_T=S_1\oplus S_2\oplus\cdots\oplus S_m,
$$

where (\oplus) denotes temporal concatenation. A ShotOrder derivative applies a recorded permutation (\pi):

$$
V_{SO}=S_{\pi(1)}\oplus S_{\pi(2)}\oplus\cdots\oplus S_{\pi(m)}.
$$

The intended manipulation is:

- preserve the within-shot pixels, faces, bodies, objects, voices, and biological motion as much as the editing procedure permits;
- reduce or alter cross-shot adjacency, causal continuity, anticipation, and narrative order;
- record the input path/hash, shot boundaries, permutation, processing settings, and output hash.

This is not perfect matching. New cut transitions, audio discontinuities, shot-length structure, familiarity, and residual low-level differences can remain.

### Three structural contrasts

PRAYCG4 supports the declared contrasts

$$
\Delta_{T-P}=\bar Y_T-\bar Y_{Phase},
$$

$$
\Delta_{T-SO}=\bar Y_T-\bar Y_{ShotOrder},
$$

$$
\Delta_{T-O}=\bar Y_T-\bar Y_{Override}.
$$

Their intended interpretation is narrower when considered jointly:

| Contrast | Primary question | Major remaining caution |
|---|---|---|
| Target − PhaseScrambled | Does the intact target differ from strongly structure-damaged sensory input? | Phase scrambling also damages local objects, faces, contours, and motion structure. |
| Target − ShotOrder | Does intact larger-scale sequence add something beyond locally intact shots? | Editing artifacts, familiarity, audio treatment, and fixed order remain. |
| Target − Override | Does natural viewing differ from analytic task engagement with the same target? | Task load, cue monitoring, gaze/AOI changes, and task relief remain. |

### Why ShotOrder was added

PhaseScrambling is useful but too destructive to serve as the only control for a narrative question. Research on scrambled visual controls likewise warns that phase scrambling can alter image properties beyond the intended high-level manipulation; this supports treating it as a useful but incomplete control rather than a pure “meaning-null” stimulus ([Stojanoski & Cusack, 2014](https://doi.org/10.1167/14.12.6)). ShotOrder creates an intermediate rung: more local content is retained, while the larger temporal sequence is disrupted.

### Plain-language explanation

PhaseScrambling asks, “Does intact media differ from visual/audio material whose structure has been heavily damaged?” ShotOrder asks, “If the individual shots are still there but the story order is broken, does the response change?” The two controls together help separate low-level drive, recognizable local content, and larger narrative-temporal organization.

---

## 3. Semantic Meaning Gradient v1.0

### Implemented acquisition states

The SMG runner operationalizes three conditional states:

```text
SEMANTIC_ZERO_1
→ washout/report
→ HIGH_MEANING_TARGET_1
→ washout/report
→ ARITHMETIC_OVERRIDE_1
→ washout/report
```

It retains Baseline 1, Baseline 2/final reflection, and the final report. Compatibility aliases map these native labels to the current analysis frame, but the native SMG labels remain in provenance.

The Semantic-Zero stimulus must be a distinct, coherent, deliberately low-meaning stimulus. PhaseScrambled or chaotic media is not substituted automatically because randomness can create novelty, threat, prediction error, or puzzle demand.

### 3.1 Proposed Semantic Meaning Density

The D205 theory defines a bounded candidate function

$$
\operatorname{SMD}(t)=\sigma\!\left[
w_HH(t)+w_AA(t)+w_VV(t)+w_CC(t)+w_RR(t)+w_KK(t)+w_TT(t)
-w_PP_{puzzle}(t)-w_OO_{overload}(t)
\right].
$$

The positive terms represent:

- (H(t)): human/social presence;
- (A(t)): agency or goal-directed action;
- (V(t)): vulnerability, need, grief, fear, hope, or tenderness;
- (C(t)): causal continuity;
- (R(t)): repair, reunion, care, forgiveness, protection, or restored attachment;
- (K(t)): stakes or consequence;
- (T(t)): visible transformation of state or relationship.

The subtractive terms represent puzzle demand and sensory overload. All weights should be nonnegative, normalized, and fixed without examining the physiological outcomes used to test the theory.

This formula is a **proposed stimulus annotation model**, not an objective meter of meaning. Several inputs require manual coding, transcripts, post-block reports, or future validated automated detectors.

### 3.2 Total, peak, and arc summaries

The proposed total and peak summaries are

$$
M_{total}=\frac{1}{T}\int_0^T \operatorname{SMD}(t)\,dt,
$$

$$
M_{peak}=\max_t \operatorname{SMD}(t).
$$

The D205 proposal also wrote

$$
M_{arc}=\operatorname{Var}[\operatorname{SMD}(t)]
+\max_t\left|\frac{d\operatorname{SMD}(t)}{dt}\right|.
$$

The raw sum is dimensionally incoherent: variance is dimensionless when SMD is dimensionless, while the slope has units of inverse time. The v1.0 runner therefore keeps variance and maximum absolute slope separate. If a future preregistration requires one arc index, it must first declare a time scale (T_0) and dimensionless weights, for example

$$
M_{arc}^{*}=a\,\operatorname{Var}[\operatorname{SMD}(t)]
+b\,T_0\max_t\left|\frac{d\operatorname{SMD}(t)}{dt}\right|,
$$

with (a,b\ge0) frozen before outcome review.

### 3.3 Proposed Meaning Response Index

The source theory proposes

$$
MRI_i=
\frac{
z(PNCC_{\theta,i})+z(PNCC_{HR,i})+z(PNCC_{RMSSD,i})
+z(Meaning_i)+z(Absorption_i)+z(Empathy_i)
}{
1+A_{artifact,i}+E_{entrainment,i}+C_{contamination,i}
}.
$$

This expresses a useful design principle: convergent carryover, physiology, and subjective report should be attenuated by artifact and stimulus-locking concerns. However, **the current runner does not compute MRI**. A legitimate implementation still requires a declared z-score reference distribution, component direction, missing-data policy, entrainment definition, contamination rule, weighting rule, and prospective validation.

### 3.4 Manipulation-validity indices

All self-report inputs must first be mapped explicitly to ([0,1]).

Semantic-Zero Validity Index:

$$
SZI=(1-Meaning)(1-Empathy)(1-Absorption)(1-Threat)(1-PuzzleDemand).
$$

Override Performance Index:

$$
OPI=TaskCompliance\cdot AnalyticEffort\cdot(1-Empathy)\cdot(1-Meaning)\cdot(1-NarrativeEngagement).
$$

Meaning separation:

$$
\Delta M=M_{target}-M_{semantic\text{-}zero}.
$$

Meaning Carryover Score:

$$
MCS_i=\frac{
StoryActive_{washout}+EmotionalAfterglow_{washout}+Replay_{washout}+FeltReturnDelay_{washout}
}{4}.
$$

The proposed thresholds are (SZI\ge0.60), (OPI\ge0.50) exploratory or (OPI\ge0.65) strong, and (\Delta M\ge0.35). These are **unvalidated candidate thresholds**, not discovered biological constants.

The multiplicative form makes the manipulation checks conjunctive. For example, an otherwise low-rated Semantic-Zero condition with high puzzle demand receives a low SZI. That is intentional: a control that provokes strong puzzle solving has not instantiated the proposed low-meaning/low-demand state.

### 3.5 Proposed post-narrative carryover

With ([x]_+=\max(x,0)), the source theory proposes

$$
PNCC_{\theta,i}
=\frac{
\int_0^{T_w}[\kappa_{\theta,washout,i}(t)-\kappa_{\theta,pre,i}]_+\,dt
}{1+A_{artifact,i}},
$$

and

$$
PNCC_{phys,i}=w_{HR}WCI_{HR,i}+w_{RMSSD}WCI_{RMSSD,i}.
$$

These formulas express persistence above a pre-condition reference while penalizing artifact. They remain candidate signatures. A slow return, HR decrease, or RMSSD increase can also arise from fatigue, relief, breathing, posture, or drift.

### Why SMG was added

PRAYCG3 and PRAYCG4 compare kinds of structure and task context. SMG asks a different question: whether responses vary with a deliberately designed **gradient of semantic and social content**. It also makes failed manipulations visible. If the Semantic-Zero stimulus evokes strong meaning or puzzle demand, or if the arithmetic task fails to suppress engagement despite high compliance, the intended contrast was not established.

### Plain-language explanation

SMG does not assume that a random-looking video is meaningless. It first checks whether the low-meaning condition was actually experienced as low in meaning, empathy, threat, absorption, and puzzle demand. It then asks whether the high-meaning target and its post-stimulus carryover differ, and whether a demanding arithmetic task reduces that response.

---

## 4. CAI/SID v0.2 — Controlled Access-Integration Index

### Construct boundary

CAI means **Controlled Access-Integration Index**, not Conscious Access Index. It asks a bounded operational question:

> Do specified fast access-like features and slower integration-like features jointly exceed their Baseline 1 references while surviving declared artifact and task-load penalties?

CAI is unitless and bounded. It is not a probability, diagnosis, direct consciousness measurement, proof of narrative reception, or validated measure of meaning.

### 4.1 Why v0.1 was revised

An earlier proposal used a hand-weighted logistic score:

$$
CAI_{v0.1}(t)=G_{QC}(t)\,\sigma(2Z(t)),
$$

$$
\begin{aligned}
Z(t)=&\,1.15E_{fast}+1.00Y_{slow}+1.20K_{loop}+0.90D_{gate}+0.55R_{auto}\\
&-1.15A_{artifact}-0.85X_{task}-0.80C_{confound}-1.10.
\end{aligned}
$$

Those coefficients were theoretical choices, not fitted biological constants. More importantly, the earlier loop logic could treat fast-low/slow-low similarity as favorable loop evidence. v0.2 removed that ambiguity, adopted an equal-weight primary support composite, and separated contextual and autonomic evidence from primary CAI.

### 4.2 Fast access-like component

Let (z_M,z_T,z_N,z_V) denote Baseline-1-referenced MeaningGamma, TSP, optional NIP, and VisualGamma. With (I_j(t)=1) when component (j) is available at (t), the implemented available-input mean is

$$
L_E(t)=
\frac{0.45I_Mz_M+0.35I_Tz_T+0.20I_Nz_N}
{0.45I_M+0.35I_T+0.20I_N}
-0.10[z_V(t)]_+,
$$

and

$$
E(t)=\sigma(L_E(t)).
$$

The denominator renormalizes only over available positive inputs. The selected source column and adapter grade are recorded. General gamma is not assumed to be measurement-equivalent to MeaningGamma.

### 4.3 Slow integration-like component

For Baseline-1-referenced theta integration, NAS, and posterior alpha,

$$
L_Y(t)=0.50z_{\theta}(t)+0.30z_{NAS}(t)+0.20z_{\alpha}(t),
$$

$$
Y(t)=\sigma(L_Y(t)).
$$

These are candidate feature families. They do not independently prove comprehension, memory consolidation, or conscious integration.

### 4.4 Retrospective future-slow value

Within the same contiguous block instance (b), v0.2 computes

$$
Y_{future}(t)=
\operatorname{mean}\{Y(s):s\in b,\ t+8\le s\le t+30\}.
$$

At least five future samples are required. There is no branch-end median fill; values near the end of a block become missing when future coverage is insufficient. Because this term uses future samples, CAI is an offline retrospective estimate, not a live causal state readout.

### 4.5 Corrected positive loop

Define above-neutral evidence

$$
e^+(t)=[E(t)-0.5]_+,
\qquad
y^+(t)=[Y_{future}(t)-0.5]_+.
$$

The positive product is

$$
K_{product}^{+}(t)=2\sqrt{e^+(t)y^+(t)}.
$$

If a local correlation is estimable in the declared 31-second window,

$$
\rho^+(t)=[\operatorname{corr}_{local}(E,Y_{future})]_+,
$$

$$
K(t)=0.70K_{product}^{+}(t)+0.30\rho^+(t).
$$

If correlation is not estimable, (K=K_{product}^{+}); unavailability never becomes positive evidence.

#### Why fast-low/slow-low is not positive loop evidence

If (E\le0.5) or (Y_{future}\le0.5), then one positive-excess term is zero, so

$$
K_{product}^{+}=2\sqrt{0\cdot y^+}=0
\quad\text{or}\quad
2\sqrt{e^+\cdot0}=0.
$$

Thus jointly low signals can be similar or correlated, but they do not support the positive loop. The geometric mean also imposes an “AND-like” rule: both above-neutral components are required, and an imbalance is penalized relative to two jointly high components.

### 4.6 Artifact and task penalties

The implemented artifact latent uses available standardized artifact components:

$$
L_A(t)=\operatorname{weighted\_available}
\left(0.55z_{artifact},0.25z_{HF},0.20z_{P2P}\right),
$$

$$
A(t)=\sigma(L_A(t)),
\qquad
X(t)=\sigma(z_{task}(t)).
$$

Only above-neutral penalty evidence is used:

$$
A^+(t)=\operatorname{clip}_{[0,1]}(2[A(t)-0.5]),
$$

$$
X^+(t)=\operatorname{clip}_{[0,1]}(2[X(t)-0.5]).
$$

Hard QC fails when declared standardized artifact sentinels exceed their thresholds: artifact (>5), high-frequency sentinel (>5), or P2P (>5) when P2P is available. A hard-failed row is missing, not zero.

### 4.7 Primary v0.2 composite

Fast and slow positive evidence are

$$
E^+(t)=\operatorname{clip}_{[0,1]}(2[E(t)-0.5]),
$$

$$
Y^+(t)=\operatorname{clip}_{[0,1]}(2[Y(t)-0.5]).
$$

The equal-weight support and penalty terms are

$$
Support(t)=\frac{E^+(t)+Y^+(t)+K(t)}{3},
$$

$$
Penalty(t)=\frac{A^+(t)+X^+(t)}{2}.
$$

The current primary score is

$$
CAI_{core}(t)=Support(t)[1-Penalty(t)].
$$

If required fast, slow, loop, artifact, or task values are unavailable, or hard QC fails, (CAI_{core}(t)) is missing.

#### Boundedness

Because each support and penalty component lies in ([0,1]), their arithmetic means also lie in ([0,1]). Therefore

$$
0\le Support\le1,
\qquad
0\le1-Penalty\le1,
$$

and

$$
0\le CAI_{core}\le1.
$$

This mathematical bound does **not** make CAI a probability. Probability requires empirical calibration against an independently defined event or state.

### 4.8 Contextual reliability is separate

When independent DGA/context information exists,

$$
Reliability_{context}
=D_{gate}(1-ConfoundLoad)(1-ExtractionLoad),
$$

$$
CAI_{context\text{-}gated}
=CAI_{core}\,Reliability_{context}.
$$

This is an attribution-confidence sensitivity output. It does not replace primary CAI and is not an independent physiological channel.

### 4.9 Time summaries and SID-style density

For valid duration (T_{valid}),

$$
Mean\_CAI=\frac{\int CAI_{core}(t)\,dt}{T_{valid}},
$$

$$
CAI_{load}=\int CAI_{core}(t)\,dt,
$$

$$
CAI_{occupancy}(\tau)
=\frac{\operatorname{valid\ time}\{CAI_{core}(t)\ge\tau\}}{T_{valid}}.
$$

The current exploratory occupancy threshold is (\tau=0.50). A general interval density is

$$
SID_{[a,b]}=\frac{1}{b-a}\int_a^b CAI_{core}(t)\,dt,
$$

computed discretely on the available time grid. Moving-block bootstrap intervals use 30-second blocks and 1,000 replicates. They describe within-run temporal stability; they do not turn one participant into a population sample.

### Why CAI/SID was added

Earlier PRAYCG analyses produced multiple partially overlapping features. CAI/SID creates one frozen, inspectable candidate that requires joint above-reference support and explicitly penalizes artifact and task burden. Its purpose is falsifiability and disciplined comparison—not to compress consciousness into a number.

### Plain-language explanation

CAI asks whether the fast candidate signals are elevated, whether slower candidate signals are elevated now and shortly afterward, whether the two support each other, and whether artifact or task load weakens that interpretation. It refuses to count “both low” as a positive loop and refuses to turn bad data into a low score.

---

## 5. Continuous Autonomic/RespDualPath v1.0

### Why continuous arrays were added

A branch average cannot answer when heart rate changed, whether an HRV estimate was supported by enough beats, whether a sigh caused the apparent response, or whether a post-Target pattern began only after the arithmetic task ended. The v1.0 module therefore represents autonomic state as synchronized time series rather than a condition-coded constant.

The implemented outputs remain separate from primary CAI.

### 5.1 Time grids and beat-event table

The primary display/alignment grid is 4 Hz:

$$
t_k=t_0+k\Delta t,
\qquad
\Delta t=0.25\ \mathrm{s}.
$$

The report grid is 1 Hz. A new 4 Hz or 1 Hz row is a repeated estimate, not a new independent biological observation.

For retained beat (j),

$$
IBI_j=\frac{RR_j}{1000}\ \mathrm{s},
\qquad
HR_j=\frac{60}{IBI_j}=\frac{60000}{RR_j}\ \mathrm{bpm}.
$$

The implemented physiological range is

$$
300\ \mathrm{ms}\le RR_j\le2000\ \mathrm{ms},
$$

equivalent to approximately 200–30 bpm. Values outside the range are excluded and recorded; v1.0 does not silently correct them.

### 5.2 Interpolated HR versus beat-derived HRV

Valid instantaneous HR is linearly interpolated onto the 4 Hz grid only when the nearest valid beat is within 3 seconds and the surrounding source gap is no more than 6 seconds. Every non-exact value carries an interpolation flag.

The critical rule is:

> Interpolation may support display and time alignment of HR, but interpolated samples are never used to manufacture HRV observations.

### 5.3 Rolling HRV

For valid beat intervals in a centered window (W_k),

$$
RMSSD_{W_k}
=\sqrt{\frac{1}{N_{diff}}\sum_{j=1}^{N_{diff}}(RR_{j+1}-RR_j)^2}.
$$

v1.0 uses a 30-second centered window and requires at least 15 valid successive differences.

For the 60-second centered window,

$$
SDNN_{W_k}
=\sqrt{\frac{1}{N-1}\sum_{j=1}^{N}(RR_j-\overline{RR})^2},
$$

$$
pNN50_{W_k}
=\frac{1}{N-1}\sum_{j=1}^{N-1}\mathbf 1(|RR_{j+1}-RR_j|>50\ \mathrm{ms}).
$$

At least 30 valid beats are required for SDNN and pNN50. The output also reports valid-pair counts, beat counts, expected-beat coverage, and the fraction excluded. These definitions follow conventional time-domain HRV quantities, while the short, overlapping PRAYCG windows remain exploratory and should not be treated as independent or clinical measurements ([1996 ESC/NASPE Task Force standard](https://pubmed.ncbi.nlm.nih.gov/8598068/)).

### 5.4 Respiration signal

The implementation interpolates raw belt samples onto the 4 Hz grid with a maximum 1-second source distance, fills internal gaps for filtering, and applies an offline fourth-order zero-phase Butterworth bandpass from 0.05 to 0.7 Hz:

$$
r_f(t)=\operatorname{Bandpass}_{0.05-0.7\,Hz}(r_{raw}(t)).
$$

The analytic signal is

$$
z_r(t)=r_f(t)+i\mathcal H[r_f(t)],
$$

where (\mathcal H) is the Hilbert transform. The implemented phase and amplitude are

$$
\phi_r(t)=\operatorname{unwrap}(\arg z_r(t)),
$$

$$
a_r(t)=|z_r(t)|,
\qquad
Depth(t)=2a_r(t).
$$

Instantaneous breathing rate is

$$
BR(t)=\frac{60}{2\pi}\frac{d\phi_r(t)}{dt},
$$

followed by a centered five-second rolling median. Values outside 2–60 breaths/minute are invalid. Phase is also invalid when amplitude is below 20% of the median amplitude or the row is inside a hold candidate.

Respiratory velocity and acceleration are

$$
v_r(t)=\frac{dr_f(t)}{dt},
\qquad
a_r^{(2)}(t)=\frac{d^2r_f(t)}{dt^2}.
$$

### 5.5 Sigh, hold, and motion candidates

The implemented sigh candidate marks robust amplitude peaks satisfying

$$
z_{robust}(a_r(t))\ge3.0
$$

with an 8-second refractory interval.

The implemented motion caution is

$$
MotionRisk(t)=\max\left(
|z_{robust}(v_r(t))|,
|z_{robust}(a_r^{(2)}(t))|
\right),
$$

with a caution threshold of 4.0.

The current hold detector is a permissive candidate. It marks a contiguous interval of at least 4 seconds when

$$
a_r(t)<0.20\operatorname{median}(a_r)
\quad\mathbf{or}\quad
|z_{robust}(v_r(t))|<0.05.
$$

The source theory described the stricter conjunction “low amplitude **and** low velocity.” The shipped v1.0 implementation uses **OR**, so hold labels must remain candidate events and should be sensitivity-tested before scientific promotion.

### 5.6 Dual-path rule

The same respiratory event can legitimately receive both labels:

$$
RespStateEvent(t)=1,
\qquad
RespArtifactCaution(t)=1.
$$

This is not contradictory. A sigh may be a genuine autonomic event while its chest/head movement or breathing-linked physiology also contaminates EEG or changes HRV. The state event is preserved; the overlapping clean-EEG interpretation is weakened.

### 5.7 HR–respiration lag coupling

Within each centered 60-second window, the implementation evaluates Pearson correlation over a fixed lag grid

$$
\ell\in\{-10.00,-9.75,\ldots,9.75,10.00\}\ \mathrm{s}.
$$

For lag (\ell),

$$
r_{HR,Resp}(\ell;t)
=\operatorname{corr}_{W_t}(HR(u),r_f(u+\ell)).
$$

The diagnostic best lag is

$$
\ell^*(t)=\arg\max_{\ell}|r_{HR,Resp}(\ell;t)|,
$$

and the signed correlation at that lag is retained. At least 80% paired coverage is required. Searching many lags is multiplicity-sensitive; the best correlation is not a confirmatory statistic by itself.

For (B=200) circular-shift replicates, respiration is shifted by an admissible offset of at least 30 seconds, the entire lag search is repeated, and the empirical two-sided absolute-tail diagnostic is

$$
p_{shift}
=\frac{1+\sum_{b=1}^{B}\mathbf 1(|r_b^*|\ge|r_{obs}^*|)}{B+1}.
$$

### 5.8 Implemented versus future autonomic formulas

The source proposal also described HR–respiration coherence, phase-locking value, a regulatory-recovery composite, continuous autonomic support (R_{auto}(t)), and continuous AAM. Those formulas are scientifically useful candidates, including

$$
Coh_{HR,Resp}(f,t)=
\frac{|S_{HR,Resp}(f,t)|^2}{S_{HR,HR}(f,t)S_{Resp,Resp}(f,t)},
$$

$$
PLV(t)=\left|\frac{1}{N}\sum_{n\in W_t}e^{i(\phi_{HR}(n)-\phi_{Resp}(n))}\right|,
$$

but v1.0 does **not** currently implement coherence or PLV and does not insert (R_{auto}(t)) into primary CAI. They must remain proposed future extensions until their estimators, windows, quality rules, nulls, and validation criteria are frozen.

### Plain-language explanation

The module keeps a clean record of actual heartbeats, draws a clearly flagged HR line between them, computes HRV only from real retained beat intervals, reconstructs breathing, and asks whether HR and breathing move together more than expected after time shifting. A breath can be meaningful physiology and a measurement problem at the same time.

---

## 6. Prospective PRAYCG3/PRAYCG4 package v0.1

### Why a separate prospective package was needed

The public PRAYCG3 and PRAYCG4 protocols preserve continuity with the historical fixed-order design. Changing their order in place would make protocol identity ambiguous. The prospective package therefore creates separately named, immutable variants while leaving the public runners unchanged.

### 6.1 Williams first-order balance

With (q) conditions, a Williams design aims to balance both period and first-order carryover. Informally, across the complete sequence set:

$$
N_{p,c}\approx \text{constant for every period }p\text{ and condition }c,
$$

and

$$
N_{a\rightarrow b}\approx \text{constant for every ordered pair }a\ne b.
$$

For an even number of treatments, (q) sequences are sufficient; for an odd number, the reversed sequences are added, yielding (2q). This is why PRAYCG3 has six variants and PRAYCG4 has four. The design follows the residual-effect balancing logic introduced by E. J. Williams ([Williams, 1949](https://doi.org/10.1071/CH9490149)).

The generated sequences are:

| Variant | Fixed condition order |
|---|---|
| PRAYCG3P_SEQ01 | Phase → Target → Override |
| PRAYCG3P_SEQ02 | Target → Override → Phase |
| PRAYCG3P_SEQ03 | Override → Phase → Target |
| PRAYCG3P_SEQ04 | Override → Target → Phase |
| PRAYCG3P_SEQ05 | Phase → Override → Target |
| PRAYCG3P_SEQ06 | Target → Phase → Override |
| PRAYCG4P_SEQ01 | Phase → ShotOrder → Override → Target |
| PRAYCG4P_SEQ02 | ShotOrder → Target → Phase → Override |
| PRAYCG4P_SEQ03 | Target → Override → ShotOrder → Phase |
| PRAYCG4P_SEQ04 | Override → Phase → Target → ShotOrder |

Each assigned sequence is fixed before the run starts. The runner never searches for a favorable order.

### 6.2 Deterministic assignment

The current template sorts variants by sequence index and assigns participant (p) and stimulus (s) by

$$
j(p,s)=((p-1)+(s-1))\bmod m,
$$

where (m) is the number of variants. This stimulus offset prevents every stimulus from occupying the same sequence within a participant while remaining fully reproducible.

This is a template allocation rule, not concealed randomization. A confirmatory study must declare allocation, masking, exclusions, and analysis before outcome inspection.

### 6.3 Independent outcomes

Prospective reports add recognition, comprehension, recognition confidence, comprehension confidence, narrative coherence, subjective meaning, absorption, afterglow, washout activity, extraction load, and confound burden. The first six are declared independent validity outcomes and are not inputs used to construct CAI.

This separation matters. If the same report both defines CAI and “validates” CAI, the validation is circular.

### 6.4 ALS and provenance

Every video phase requires runner-registered ALS barcode events. Before collection, the real apparatus must pass the **barcode placement script-location test**: the launch path, working directory, expected script, event registration, photodiode/ALS visibility, and recovered timing offset must be verified on the actual acquisition computer.

This test answers a software-and-apparatus question—whether the intended barcode script really ran from the expected location and produced detectable events. It does not establish neural validity, but without it, anchor-level timing can be misassigned.

The freeze package hashes the protocol engine, protocol manifest, runner, CAI code/configuration, allocation file, stimuli, derivatives, anchors, and other declared inputs:

$$
h_f=SHA256(\operatorname{bytes}(f)).
$$

A later file is identical to the frozen file only if its recorded hash matches. A hash proves file identity, not scientific validity.

### 6.5 Prospective mixed model

A suitable preregistered participant-by-stimulus analysis can be written conceptually as

$$
Y_{isc}=\beta_0+\beta_c+\pi_{period}+u_i+v_s+\epsilon_{isc},
$$

where (u_i\sim N(0,\sigma_u^2)) is a participant random effect, (v_s\sim N(0,\sigma_v^2)) is a stimulus random effect, and (\beta_c) represents the predeclared condition contrasts. Additional carryover terms may be included only if declared in advance and estimable from the design.

### 6.6 Current readiness boundary

The package is **not collection-ready by default**. Real stimuli and derivatives, locked anchor files, ethics/consent approvals where required, real-hardware ALS validation, blinded feasibility data, final variance inputs, multiplicity rules, exclusions, and OSF registration are still required.

### Plain-language explanation

The prospective package prevents “condition” from always meaning “the part that happened second or third.” It rotates condition order across fixed variants, locks each assigned runner, checks that timing markers really work, and fingerprints all critical files so the registered study can be reproduced.

---

## 7. Micro Handoff v0.1

### Hypothesis and boundary

Micro Handoff tests whether a posterior-temporal 30–45 Hz activation proxy is followed, within a fixed 100–1000 ms lag bank, by a posterior/parietal-temporal 4–8 Hz activation proxy.

It does not prove that consciousness is generated in discrete 25 ms or 40 Hz frames. “RPM” and “density” are engineering metaphors for exploratory displays, not established biological quantities.

Scalp gamma is particularly vulnerable to ocular and muscle contamination; miniature saccades can generate broadband gamma-range EEG transients ([Yuval-Greenberg et al., 2008](https://pubmed.ncbi.nlm.nih.gov/18466752/)). That is why the candidate preserves jaw, ocular, and global-amplitude sentinels and treats hard failures as missing.

### 7.1 Sampling and causal feature windows

The output cadence is

$$
\Delta t=0.025\ \mathrm{s}.
$$

This is a refresh grid, not 25 ms spectral resolution. At time (t):

- temporal gamma uses a trailing 250 ms Hann-window periodogram at T5/T6, 30–45 Hz;
- theta integration uses a trailing 500 ms Hann-window periodogram at Pz/P3/P4/T5/T6, 4–8 Hz;
- visual gamma at O1/O2 is retained as a comparison family;
- T3/T4 high-frequency power, Fp1 peak-to-peak, and global neural peak-to-peak are artifact sentinels.

Only samples at or before (t) enter either spectral estimate. Because the windows differ in length, a planted raw-signal lag need not equal the diagnostic feature-series lag exactly.

### 7.2 Fast and slow activations

Using valid Baseline 1 rows only,

$$
F(t)=\sigma\left(z_{B1}[\log P_{30-45Hz,T5/T6}(t)]\right),
$$

$$
S(t)=\sigma\left(z_{B1}[\log P_{4-8Hz,Pz/P3/P4/T5/T6}(t)]\right).
$$

Both are bounded activation proxies, not probabilities.

### 7.3 Artifact quality

Let (Z_s(t)) be the maximum positive standardized jaw-HF/Fp1 sentinel value and (Z_g(t)) global neural peak-to-peak. The soft quality score is

$$
Q(t)=
\exp[-0.50(Z_s(t)-2)_+]
\exp[-0.15(Z_g(t)-4)_+].
$$

Rows become missing if sentinel artifact exceeds 5, global P2P exceeds 8, a timestamp gap crosses a feature window, required values are nonfinite, or the row is outside an identified block.

### 7.4 State agreement, positive directional handoff, and density

Define a 100 ms smooth of fast activation and a 250 ms smooth of slow activation. The positive changes are

$$
O(t)=\operatorname{clip}_{[0,1]}\left(
\frac{[F_{100}(t)-F_{100}(t-0.1)]_+}{0.25}
\right),
$$

$$
R(t,\tau)=\operatorname{clip}_{[0,1]}\left(
\frac{[S_{250}(t+\tau)-S_{250}(t+\tau-0.1)]_+}{0.25}
\right).
$$

For every fixed lag

$$
\tau\in\{0.1,0.2,\ldots,1.0\}\ \mathrm{s},
$$

state coordination is

$$
C(t,\tau)=1-|F(t)-S(t+\tau)|,
$$

paired quality is

$$
Q_{pair}(t,\tau)=\sqrt{Q(t)Q(t+\tau)},
$$

positive directional handoff is

$$
H(t,\tau)=Q_{pair}(t,\tau)\sqrt{O(t)R(t,\tau)},
$$

mean activation is

$$
A(t,\tau)=\frac{F(t)+S(t+\tau)}{2},
$$

and activation-weighted coordination density is

$$
D(t,\tau)=Q_{pair}(t,\tau)A(t,\tau)C(t,\tau).
$$

The primary candidate values are equal-weight means across the complete lag bank:

$$
\bar H(t)=\frac{1}{10}\sum_{\tau}H(t,\tau),
\qquad
\bar D(t)=\frac{1}{10}\sum_{\tau}D(t,\tau).
$$

No condition-specific winning lag is selected. A 500 ms trace and a full-run best lag are diagnostic only.

### 7.5 Why the three outputs are separate

The separation prevents three different states from being conflated:

| State | (C) | (H) | (D) | Interpretation |
|---|---:|---:|---:|---|
| Low fast, low slow | Can be high | Low | Low | Similarity without positive activation or handoff. |
| High fast, high slow, stationary | High | Low | High | Sustained activated coordination without positive transition. |
| Fast rises, then slow rises | Potentially high | High | Potentially high | Candidate positive directional handoff. |

The geometric means in (Q_{pair}) and (H) impose joint support: one poor-quality endpoint or one absent positive transition limits the score.

### 7.6 Nulls and uncertainty

The module does not treat 25 ms rows as independent observations. It summarizes non-overlapping 30-second blocks and evaluates time-structure nulls on a 100 ms diagnostic grid.

- **Circular-shift null:** disrupts absolute alignment while preserving each series’ internal shape.
- **Phase-randomized null:** preserves the approximate spectrum while disrupting specific timing structure.
- **Block-label permutation:** tests label association when exchangeability is defensible.
- **Artifact-matched contrast:** checks whether condition differences persist under comparable artifact distributions.

### 7.7 Synthetic acceptance

All 14 declared synthetic software checks passed. A planted 500 ms raw-signal handoff was recovered at a 600 ms diagnostic lag, within the declared (pm100) ms tolerance for unequal causal spectral windows. The suite also verified low-low, stationary high-high, reverse-direction, independent, artifact, timestamp-gap, null, and deterministic-repeat behavior.

This validates declared software behavior on synthetic fixtures. It does not validate a consciousness construct.

### 7.8 Historical result

The frozen batch inventoried 24 unique XDF recordings; six were computationally eligible with caution, all at 125 Hz. For Target minus Control across those six runs:

| Metric | Mean difference | Median | Positive runs | Descriptive run-bootstrap interval |
|---|---:|---:|---:|---:|
| Positive directional handoff | +0.00056 | +0.00078 | 3/6 | [−0.0016, +0.0026] |
| Activation-weighted density | +0.0441 | +0.0293 | 5/6 | [+0.0050, +0.0926] |
| Coordination | +0.00127 | −0.00346 | 3/6 | [−0.0228, +0.0305] |

The specifically directional effect was mixed around zero, best diagnostic lags varied from 0.2 to 0.7 seconds, only one of six runs passed the circular-shift check at uncorrected (p<.05), and none passed the phase-randomized check. The density pattern was more consistently Target-positive, but density can rise during stationary high-high activity and is not interchangeable with directional handoff.

These intervals resample predominantly repeated runs from one participant, not a participant population. Modern named runs with serious timestamp-rate disagreement were excluded rather than repaired silently.

The correct disposition is:

> **Software-valid, construct-unvalidated, retrospectively mixed.**

### Plain-language explanation

Micro Handoff asks whether fast activity rises and is followed shortly afterward by a rise in slower activity. It separately reports whether the two signals merely look alike, whether both are strongly active, and whether a positive fast-to-slow change occurred. Historical data did not show a stable directional effect, even though one density-style output was often higher in Target.

---

## 8. Confound-defense modules

These modules do not “correct away” every confound. They determine whether required evidence exists, compute bounded diagnostics where possible, and constrain interpretation.

### 8.1 HOC-R — High-Order Control Residualization

HOC-R inventories low-level visual, low-level audio, cue, and high-order social/visual regressors. Where rows align and enough complete data exist, it fits

$$
\mathbf y=\mathbf X\boldsymbol\beta+\boldsymbol\varepsilon
$$

by ordinary least squares with an intercept, and reports in-sample

$$
R^2=1-\frac{\sum_t(y_t-\hat y_t)^2}{\sum_t(y_t-\bar y)^2}.
$$

It is currently a residualization **audit**: the shipped output reports model availability, terms, row count, and training (R^2). It does not automatically replace the outcome with a causal residual endpoint. If face/body/object/AOI regressors are absent, Target versus PhaseScrambled remains high-order-control-cautioned.

### 8.2 OSA — Override Spatial Attention/AOI burden

Cue duty cycle is

$$
duty=\frac{cue\ display\ duration}{cue\ interval}.
$$

Each available 0–9 report is mapped to ([0,1]) by (x/9). The report burden is the mean of available cue-legibility, cue-blur/smallness, eye-strain/squint, running-sum-stall, and task-load ratings:

$$
B_{report}=\operatorname{mean\_available}(L,B,E,S,T).
$$

The OSA score is

$$
OSA=\operatorname{mean\_available}(duty,B_{report}).
$$

The current flag is raised when (OSA\ge0.35) and no gaze/AOI evidence is found. The threshold is exploratory. The purpose is to prevent Target-minus-Override from being called pure “task theft” when cue monitoring may have changed where the participant looked.

### 8.3 OHC — Order, habituation, and carryover

OHC records inferred branch order, washout duration, and whether the historical default order was used. In the default Target-before-Override sequence, the implemented heuristic assigns habituation risk 1.0 and carryover risk 0.8 unless a washout of at least 600 seconds is documented; even then, carryover risk remains 0.3.

These are warning heuristics, not fitted probabilities. Their function is to make the non-identifiability in the fixed-order contrast explicit.

### 8.4 AAM — Afterglow Attribution Model

For a feature vector (\mathbf x) and (\mathbf y), similarity is

$$
sim(\mathbf x,\mathbf y)=\frac{\mathbf x^\top\mathbf y}{\|\mathbf x\|\|\mathbf y\|}.
$$

The current implementation computes Baseline-2 similarity to post-Target Washout 2 and post-Override Washout 3 where available. Narrative-afterglow-like evidence is the mean of available terms:

$$
NAI=\operatorname{mean\_available}
\left(sim(B2,W2),TargetEcho_{B2},TargetAfterglow,TargetStoryActive_{W2}\right).
$$

Task-completion-relief-like evidence is

$$
TCRI=\operatorname{mean\_available}
\left(OverrideTaskLoad,TaskCompliance,RunningSumStall,sim(B2,W3)\right).
$$

Then

$$
AAM=NAI-TCRI.
$$

Current descriptive labels use (AAM>0.20) for Target-afterglow-like, (AAM<-0.20) for task-relief-like, and the middle range for mixed/ambiguous. Missing evidence remains unavailable; the available-term means can differ in composition and therefore require provenance review.

### 8.5 RespDualPath v0.1 confound audit

The earlier confound-layer implementation selects a dimensionally coherent respiration signal where available and computes

$$
d_t=|r_t-r_{t-1}|,
$$

$$
\theta_d=\operatorname{mean}(d)+2.5\operatorname{SD}(d).
$$

Rows with (d_t>\theta_d) become respiratory-event candidates. They receive a state-event flag when they occur in declared target/override/washout/Baseline-2 phases and an artifact flag when the available artifact score exceeds 1.0.

The newer Continuous Autonomic/RespDualPath v1.0 is the preferred time-resolved path when raw cardiac and belt data are available. The v0.1 confound module remains a simpler audit for legacy feature tables.

### Why these modules were added

An apparent Target effect can arise from intact faces and objects, different gaze position, task difficulty, presentation order, task-ending relief, breathing, or artifact. These modules force the report to state which alternatives were measured, which were not, and which remain plausible.

---

## 9. Canonical frame, gates, and status-aware chaining

As the suite grew, data routing became part of scientific validity. The canonical frame requires explicit time, condition, block instance, source column, adapter, evidence grade, and missingness. Repeated instances of the same condition receive unique block IDs so future-window calculations cannot leak across blocks.

The general gate logic is

$$
Status\in\{PASS,CAUTION,INELIGIBLE,NOT\_APPLICABLE,FAILED\}.
$$

- `PASS` means declared computational requirements were satisfied.
- `CAUTION` means computation is possible but limitations must travel with the result.
- `INELIGIBLE` means the declared endpoint must not be interpreted for that run.
- `NOT_APPLICABLE` means the protocol lacks the condition or input needed for that module.
- `FAILED` means execution failed and downstream modules must not silently treat the missing output as evidence.

Status-aware chaining allows exploratory outputs to be produced for troubleshooting after a failed primary gate, but those outputs cannot inherit confirmatory status or change Master Suite eligibility.

### Why this was added

A mathematically correct formula applied to the wrong folder, duplicated block, incompatible protocol, missing baseline, or silently adapted feature can still produce a plausible-looking wrong answer. Provenance and gates make those errors inspectable.

---

## 10. Unified inferential logic

The additions form a ladder rather than one omnibus proof:

1. **Manipulation:** Did the intended stimulus/task state actually occur according to independent reports and QC?
2. **Measurement:** Were timing, channels, coverage, artifact sentinels, cardiac beats, respiration, and required features adequate?
3. **Within-run contrast:** Did the frozen endpoint differ across declared conditions?
4. **Alternative explanations:** Do ShotOrder, HOC-R, OSA, OHC, AAM, respiration, or artifact weaken the attribution?
5. **Time structure:** Does the effect exceed declared circular-shift, phase-randomized, or label nulls where applicable?
6. **Prospective validity:** Does the frozen candidate predict independent recognition, comprehension, confidence, or other criteria in new participants and stimuli?
7. **Reliability and calibration:** Is it stable enough for a declared secondary role, and if probabilistic language is ever used, has that probability been independently calibrated?

The primary prospective condition model can be summarized as

$$
Outcome\sim Condition+Period+(1|Participant)+(1|Stimulus),
$$

with the three predeclared PRAYCG4 contrasts:

$$
Target-PhaseScrambled,
\qquad
Target-ShotOrder,
\qquad
Target-Override.
$$

Multiplicity correction, exclusions, lag windows, nulls, coverage thresholds, and any carryover terms must be frozen before confirmatory outcome review.

## 11. Promotion and falsification criteria

CAI/SID and Micro Handoff should remain exploratory unless all relevant gates are passed. Evidence against or constraining a candidate includes:

- failure to exceed time-shift or phase-randomized nulls;
- reversal under counterbalancing;
- disappearance under reasonable artifact, lag, or missingness sensitivity analyses;
- dependence on one optional component or one stimulus;
- failure to predict independent behavioral/report outcomes;
- poor test-retest or held-out reliability;
- failure in new participants and stimuli;
- inability to distinguish the intended condition from ShotOrder, task, gaze, respiratory, or order explanations.

Null and reversed results must be retained. A failed manipulation means the intended hypothesis was not adequately tested; it does not automatically prove or disprove the underlying theory.

## 12. Public claim boundaries

Permitted wording includes:

- “The frozen exploratory CAI v0.2 score was higher/lower under this operational model.”
- “The Micro Handoff directional candidate was/was not supported relative to the declared nulls.”
- “ShotOrder adds a locally intact but temporally disrupted structural control.”
- “Continuous autonomic arrays estimate the timing, quality, and respiratory dependence of measured autonomic changes.”
- “The result requires prospective, independent replication.”

Prohibited wording includes:

- “CAI measures or proves consciousness.”
- “A bounded CAI value is the probability of consciousness.”
- “Gamma-to-theta handoff proves discrete 40 Hz conscious frames.”
- “Target greater than Control proves meaning or narrative reception.”
- “Baseline 2 proves Target afterglow.”
- “HRV increase proves meaning, parasympathetic truth, or emotional recovery.”
- “A file hash proves scientific validity.”

## 13. Methodological references and source hierarchy

The authoritative source hierarchy for a software result is:

1. the versioned implementation and frozen configuration;
2. the versioned mathematical specification and protocol manifest;
3. generated provenance, QC, warnings, and source hashes;
4. theory proposals, release notes, and explanatory documents.

Where a theory proposal differs from shipped v0.95 code, this document reports both and labels the implemented behavior as the current computational definition. External references provide methodological context; they do not validate PRAYCG-specific constructs.

- Task Force of the European Society of Cardiology and the North American Society of Pacing and Electrophysiology. “Heart rate variability: standards of measurement, physiological interpretation and clinical use.” *Circulation* 93 (1996): 1043–1065. [PubMed](https://pubmed.ncbi.nlm.nih.gov/8598068/)
- Williams, E. J. “Experimental Designs Balanced for the Estimation of Residual Effects of Treatments.” *Australian Journal of Scientific Research, Series A* 2 (1949): 149–168. [DOI](https://doi.org/10.1071/CH9490149)
- Stojanoski, B., and Cusack, R. “Time to wave good-bye to phase scrambling: Creating controlled scrambled images using diffeomorphic transformations.” *Journal of Vision* 14(12) (2014). [DOI](https://doi.org/10.1167/14.12.6)
- Yuval-Greenberg, S., Tomer, O., Keren, A. S., Nelken, I., and Deouell, L. Y. “Transient induced gamma-band response in EEG as a manifestation of miniature saccades.” *Neuron* 58(3) (2008): 429–441. [PubMed](https://pubmed.ncbi.nlm.nih.gov/18466752/)

## Final perspective

The v0.93–v0.95 additions were not made to multiply endpoints until one became positive. They were made to decompose a difficult inference into narrower, falsifiable questions:

- Is the signal low-level sensory drive, locally recognizable structure, or coherent temporal order?
- Does an analytic task alter the response, and can cue monitoring or task relief explain it?
- Do fast and slow candidate signals jointly exceed baseline, or are they merely both low or both stationary?
- Did the autonomic change occur at the relevant time, with adequate beat and respiration quality?
- Does the result survive artifact, order, carryover, and time-structure nulls?
- Does a frozen candidate generalize prospectively to new participants and stimuli and predict independent outcomes?

That structure is the scientific significance of the upgrade: it makes positive, null, mixed, and ineligible results interpretable under the same declared rules while keeping the strongest claims conditional on future prospective validation.
