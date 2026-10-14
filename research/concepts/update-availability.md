# Narrative update polarity, task tradeoff and availability

NUPI, TTI and DGA organize different parts of a narrative-response interpretation. NUPI compares load with a later recovery profile. TTI compares receptive/integration-like response with a competing extraction task. DGA records whether sensory access, reported availability and confounds support the intended interpretation. None measures literal thermodynamic energy.

[Concept guide](README.md) · [Current algorithm map](../algorithms/README.md) · [Recognition and integration](recognition-integration.md) · [Immersion and echoes](immersion-entrainment.md)

## NUPI v0.1: recovery minus load

The [NUPI v0.1 note preserved with Suite v1.5.4](../measures/originals/master-suite-v1-5-5/NUPI_Narrative_Update_Polarity_Method_v1_5_4.md) defines the Narrative Update Polarity Index as an exploratory secondary summary. Inputs include CII/NIP anchor summaries, TTI, available MRED-ITP and EET outputs, Baseline 1/2 feature/autonomic comparisons, and optional final self-report.

Its Accommodative Load Index (`ALI`) and Regulatory Dividend Index (`RDI`) are:

```text
ALI = mean(semantic_intensity,
           target_specificity,
           complexity_perturbation,
           TTI_score,
           primary_endpoint_pass_score)

RDI = mean(Baseline2_regulation,
           Baseline2_semantic_echo,
           EET_afterstate_echo,
           self_report_echo)

NUPI = RDI - ALI
```

Positive NUPI means a recovery tilt and negative NUPI a load tilt within this recipe. The component scores must be constructed on the declared comparable scales; a mean of raw quantities with unrelated units would not reproduce the intended composite. Missing-component policy and coverage are also part of the implementation.

The two axes matter alongside their difference. A small difference can arise from low load/low recovery or high load/high recovery. The source retains categories including `ACCOMMODATIVE_LOAD`, `RESOLUTIVE_RECOVERY`, `HIGH_LOAD_WITH_RECOVERY` and `RECOGNITION_WITH_WEAK_RECOVERY` rather than reducing all profiles to a sign.

If Baseline 2 or an equivalent final reflective after-state is absent, the method does not grade polarity and uses `POLARITY_UNRESOLVED_NO_BASELINE2`. Missing after-state evidence is not zero recovery and is not an unfavorable biological outcome. Outputs include `nupi_run_summary.csv`, `nupi_anchor_polarity_table.csv`, an overlay and interpretation JSON.

## NUPI recipes must not be merged

Three inspected sources use different RDI component lists:

| Source | RDI recipe | Reproducibility implication |
| --- | --- | --- |
| NUPI v0.1 note, filename v1.5.4 | Four components: B2 regulation, B2 semantic echo, EET after-state echo, self-report echo | The explicit historical formula above |
| [Formula Report v1.0, section 21](../collections/public-docs/Formula_Module_Report_v1_0/PRAYCG_Formula_Module_Report_v1_0.md#212-regulatory-dividend-index-rdi) | Five standardized components: the preceding families plus `z(API_A_B2 - API_A_B1)`; self-report is named `TargetEchoedDuringBaseline2_selfreport` | An expanded, standardized report formulation |
| Proposed Public Alpha 11.2.1 NUPI runtime | Three direct RDI terms: B2 regulation score, B2 semantic echo score and EET echo, when B2 is available | See the [current implementation map](../algorithms/README.md) for the exact script and revision |

The common identity `NUPI=RDI-ALI` does not make results interchangeable. Report the actual recipe, source revision, scales and available components. Self-report or API-A may appear elsewhere in an analysis pipeline; that does not make them additional direct terms in the current three-term RDI expression.

The [Framework NUPI update v0.5](../collections/public-docs/Framework_NUPI_Update_v0_5/README_NUPI_Framework_Update_v0_5.md) preserves a historical reproduction/report package. It is a separate artifact from the current Workbench implementation. NUPI characterizes proxy-level response shape; it does not establish healing, moral value, consciousness, ATP/glucose use, heat release or oxygen metabolism.

## TTI v0.1: reception versus extraction

The [TTI v0.1 note](../measures/originals/master-suite-v1-5-5/TTI_v0_1_Reception_Extraction_Tradeoff.md) historically uses “Thermodynamic Theft Index” and the technical description **Reception-Extraction Tradeoff**. Its hypothesis is that receptive absorption and a demanding instrumental task can compete for limited cognitive/autonomic capacity when directed at the same material.

The operational composite, using the note's default v1.4.8 weights, is:

```text
TTI = 0.28*z(MR_Target - MR_Override)
    + 0.24*z(ENC_Target - ENC_Override)
    + 0.14*z(API_Target - API_Override)
    + 0.22*z(X_Override - X_Target)
    - 0.08*z(abs(Artifact_Target - Artifact_Override))
    - 0.04*z(abs(VisualDrive_Target - VisualDrive_Override))
```

The API term is labeled API-A in the weight list. These are standardized contrasts, so the reference distribution matters: standardizing an absolute artifact difference is not identical to directly subtracting a raw positive artifact penalty. Retain the declared standardization and components with the composite.

Positive TTI means that, under this recipe, Target preserved more recognition/integration-like response while Override carried more task/extraction load. It does not mean Override erased meaning. Override may reroute attention, increase arithmetic or cue-maintenance demand, alter gaze, or preserve semantic processing despite the task.

Required interpretation checks include Target/Override stimulus identity, Control validity, display/ALS timing, artifact, available respiration/common-drive controls, cue visibility, task engagement, audio/video synchronization, external noise, self-report and anchor provenance. Outputs preserve component/global summaries, paired windows, event summaries, extraction/confound context, overlays and interpretation.

The note also proposes a conceptual capacity inequality:

```text
c_R*R(t) + c_X*X(t) + c_M*M(t) + c_Gamma*Gamma(t)
    + c_RX*R(t)*X(t) <= B(t)
```

This is a motivating budget model with unspecified capacity/cost parameters. It is not the measured TTI composite and is not an energy-balance measurement in joules. A scalar TTI result cannot demonstrate the inequality or identify all of its latent terms. The claim weakens when Override matches/exceeds Target on MR/ENC, Control or confounds explain the effect, self-report contradicts engagement, or a simpler model explains the data better.

## DGA v0.1: availability and gate dissociation

The [DGA v0.1 note, Suite v1.5.6](../measures/originals/offline-interpreter-v1-5-6/DGA_Decoder_Gate_Availability_Method_v1_5_6.md) treats sensory access and internal availability as context for receiving the material. It reads PRAYCG2.0 branch core/confound reports, Override task reports, and available feature/A-MRED tables.

For branch `b`, the historical 0–9 self-report recipe is:

```text
SA_b = 1 - mean(AudioComprehensionDifficulty, SpeakerVolumeDifficulty,
                ExternalNoiseIntrusion, AudioVideoSyncProblem)/9

DA_b = mean(Meaning, Absorption, EmotionalAfterglow, StoryActiveWashout)/9
EI_b = mean(Absorption, EmotionalAfterglow, StoryActiveWashout)/9
X_b = max(core TaskExtractionLoad, Override task burden)/9
C_b = max(core ConfoundBurden, detailed confound mean)/9

D_gate,b = sigmoid(2.0*SA_b + 1.4*DA_b + 1.1*EI_b
                   - 1.2*X_b - 1.8*C_b - 0.75)

GDI = mean(SA_Override - SA_Target,
           EI_Target - EI_Override,
           X_Override - X_Target,
           C_Target - C_Override)
```

`SA` represents sensory access, `DA` reported decoder availability, `EI` emotional/integrative impact, `X` extraction burden and `C` confound burden. Mapping reports to the required scales and handling absent answers are necessary preprocessing steps; an absent answer is not an observed zero. `DA` and `EI` deliberately share report items, so they are not independent measurements. The sigmoid gives a bounded score, not an empirically calibrated probability of successful decoding.

`GDI` preserves a particular signed contrast: stronger Override sensory access, stronger Target impact, more Override extraction and more Target confound can all increase it. It is not simply “Target minus Override” on every component. A high value therefore calls for component inspection, not a generic quality ranking.

Outputs include branch gates, gate-dissociation summary, gate-adjusted MRED anchor table and a report. Older runs without the relevant self-report/Baseline 2 evidence remain feature-proxy-only rather than strict DGA endpoint evidence. DGA is interpretive context/triage; it does not establish consciousness, memory formation or cellular biology. In [CAI v0.2](cai-sid.md), DGA/context gating is a separate sensitivity output and does not replace primary CAI.
