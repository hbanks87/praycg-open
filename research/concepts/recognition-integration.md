# Recognition, integration and endpoint gates

MRED separates two questions that a single “meaning score” would blur: did an event show recognition-like features, and did it show a delayed integration-like marker? A familiar scene could be recognized strongly without a detected new theta handoff. That is a different result from weak recognition and weak handoff.

[Concept guide](README.md) · [Current algorithm map](../algorithms/README.md) · [Immersion and entrainment](immersion-entrainment.md) · [Update polarity](update-availability.md)

## MRED v0.1: two event scores

The [MRED v0.1 original note](../measures/originals/master-suite-v1-5-5/MRED_v0_1_Meaning_Recognition_Encoding_Dissociation.md) defines Meaning Recognition (`MR`) and Encoding/integration (`ENC`) from event-level features. Its preferred input is `candidate_local_kht_analysis.csv`, with optional familiarity/novelty covariates, scene maps and declared anchors. The note was motivated by an exploratory run; it does not make those discovered events prospectively locked endpoints.

The exact weighted recipe in that note is:

```text
MR_j = 0.35*z(MeaningGamma_j)
     + 0.35*z(TSP_j)
     + 0.30*z(K_local_j)
     - 0.20*z_positive(artifact_j)

ENC_j = 0.65*z(theta_handoff_best_j)
      + 0.15*z(API_A_j)
      + 0.20*z(novelty_j)
      - 0.20*z(familiarity_j)
      - 0.15*z_positive(artifact_j)
```

MeaningGamma, TemporalSemanticProxy (`TSP`) and local coupling supply recognition-like evidence. A post-event theta marker supplies most of this version's integration-like score, with autonomic availability (`API_A`), novelty, familiarity and artifact affecting interpretation. The standardization reference and exact input columns belong to the versioned analysis record; the coefficients alone are not a complete reproducibility specification.

When familiarity/novelty covariates are absent, this historical version gives them zero contribution **after event-level standardization**. That convention does not mean the participant was observed to have zero familiarity or novelty. It must not be generalized into a policy that every missing input becomes zero.

The module writes event scores, quadrant classification, scene/familiarity tables, an overlay and interpretation JSON. A “high” label requires both relative elevation and a positive score; a high percentile among negative scores is insufficient.

| Operational pattern | Output label | What it suggests for review |
| --- | --- | --- |
| High MR, high ENC | `MR_HIGH_ENC_HIGH` | Recognition plus a possible new integration/encoding candidate |
| High MR, low ENC | `MR_HIGH_ENC_LOW` | Recognition/schema reactivation without the detected theta integration marker |
| Low MR, high ENC | `MR_LOW_ENC_HIGH` | Inspect task, novelty, nonsemantic effects and artifact alternatives |
| Low MR, low ENC | `MR_LOW_ENC_LOW` | Weak or null evidence under these definitions |

Neither the high/high quadrant nor the `ENC` name proves memory formation. A missing theta handoff also does not prove that memory formation was absent.

## The topological extension is a different definition

The [MRED v0.2 topological update](../measures/originals/master-suite-v1-5-5/MRED_TOPOLOGICAL_UPDATE_v1_4_7.md) adds state-topology change and persistence:

```text
MR_j  = f(MeaningGamma_j, TSP_j, K_HT-topo,j, SelfReport_j, Artifact_j^-1)
ENC_j = f(H_theta,j, DeltaT_topo,j, Persistence_j,
          Novelty_j, Familiarity_j^-1, Artifact_j^-1)
```

Here `f` is schematic. The note does not supply one numerical estimator or coefficient set for it. The inverse-style artifact/familiarity notation expresses the proposed direction of influence; it does not specify a division-by-value implementation. Combining this schematic extension with the v0.1 weights would create a new recipe, rather than faithfully reproduce either source. The [coupling/topology guide](coupling-topology.md) explains the indirect human-state interpretation.

## A-MRED v1.5.3: lock the question before the recording

[A-MRED v1.5.3](../measures/originals/master-suite-v1-5-5/A_MRED_PrimaryEndpoint_Method_v1_5_3.md) proposes an anchor-locked primary endpoint for future confirmatory work. It asks whether Target has both recognition and delayed integration, exceeds both Control and Override, and survives the declared quality checks.

Its compact mathematical gate is:

```text
A-MRED_j = 1[MR_T,j > theta_MR]
         * 1[ENC_T,j > theta_ENC]
         * 1[MR_T,j > MR_C,j + delta]
         * 1[MR_T,j > MR_O,j + delta]
         * 1[ENC_T,j > ENC_C,j + delta]
         * 1[ENC_T,j > ENC_O,j + delta]
         * 1[QC_j = PASS]
```

The source's full strict-gate list also requires the anchor to be locked before acquisition, a predeclared delayed window, artifact/confound acceptance, CET-R correction that does not explain the event when available, and self-report that does not contradict the intended state. The compact expression does not replace these procedural requirements. Thresholds and margins must be fixed and versioned; the note does not establish universal biological cutoffs.

The source also gives a continuous backup:

```text
MREDScore_j = MR_j * ENC_j * QC_j
DeltaMRED_j = MREDScore_T,j - max(MREDScore_C,j, MREDScore_O,j)
```

The strict binary gate and continuous backup have different roles. A continuous product does not, by itself, establish that each positive-evidence threshold or prospective-lock requirement passed. Report the component scores and strict status. Failure means the operational gate was not met; it does not establish that the event was meaningless.

## MRED-Peak and MRED-Resolution v1.5.5

The [method note](../measures/originals/master-suite-v1-5-5/MRED_Peak_Resolution_Method_v1_5_5.md) and [endpoint-compression note](../measures/originals/master-suite-v1-5-5/MRED_Peak_Resolution_Endpoint_Method_v1_5_5.md) summarize existing outputs into two review families:

| Family | Input evidence and calculation role | Typical output status |
| --- | --- | --- |
| Peak | Acute predeclared Target-specific MR plus delayed ENC, Control/Override contrasts and artifact/confound/timing gates | Strict pass, timing caution, unlocked candidate, recognition-only, or unsupported |
| Resolution | Delayed washout/Baseline 2 echo, NUPI/RDI, EET resemblance, self-report and available autonomic/respiratory recovery | Candidate, weak support, negative/weak, or not gradable |

Inputs include A-MRED tables, CII anchor integrals, NUPI tables, EET, MRED-ITP and TTI summaries. Missing tables are not fabricated; absent supporting layers downgrade interpretation. Outputs include `mred_peak_resolution_anchor_table.csv`, a run summary, ranked candidate tables, overlay, interpretation and report.

This is endpoint compression, not an independent measurement. It cannot provide independent validation of the upstream scores it reads. A Resolution candidate does not establish healing, memory replay or a Target-specific cause of the final after-state. In the fixed-order protocol, Baseline 2 follows the whole sequence and may reflect cumulative exposure, Override relief, breathing, fatigue or drift as well as earlier Target responses.

## MRED-ITP v0.1: complexity and ocular companions

The [v1.5.2 MRED-ITP/ACG/OCU note](../measures/originals/master-suite-v1-5-5/MRED_ITP_ACG_OCU_Method_v1_5_2.md) defines exploratory companion signatures. They inspect event structure rather than measure literal thermodynamic entropy.

The raw-EEG Algorithmic Complexity Gate (`ACG`) uses normalized Lempel-Ziv complexity of a symbolic EEG state sequence:

```text
Delta_C_strike = C_LZ_peak - C_LZ_pre
Delta_C_settle = C_LZ_post - C_LZ_peak
ACG_gate = strike_gate AND settle_gate AND artifact_gate
CSI = z(Delta_C_strike) + z(-Delta_C_settle)
```

`CSI` rewards perturbation followed by settlement under the declared windows and normalization. Raw complexity depends on symbolization, windowing, channels and preprocessing. The historical default excludes Fp1 blink and T3/T4 jaw sentinels when the PRAYCG16 map is available. A feature-table fallback is explicitly `FEATURE_LEVEL_PROXY_NOT_RAW_EEG_LZC`; it is not the same measurement as raw EEG complexity.

Ocular-Cognitive Unloading (`OCU`) examines attention-hold and later release:

```text
BlinkSuppression_proxy = baseline_rate - hold_window_rate
BlinkRelease_proxy = release_window_rate - hold_window_rate
OCU_gate = suppression_gate AND release_gate AND artifact_gate
ORI = scaled(BlinkSuppression_proxy + BlinkRelease_proxy)
```

The note leaves the `scaled` operation schematic. True EOG/eye tracking, an Fp1 blink proxy (`RAW_FP1_BLINK_PROXY_NOT_CONFIRMED_EOG`), and a weaker feature-level P2P/global-artifact proxy must retain their different evidence grades. None is proof of memory “buffer dumping.”

Inputs are raw XDF where available, event logs, feature frames and anchor/MRED tables. Outputs retain complexity time series, blink events, ACG/OCU events, anchor-condition windows, condition specificity, phase summaries and interpretation. Read their raw/proxy labels and failed gates with the [current implementation map](../algorithms/README.md).
