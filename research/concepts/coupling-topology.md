# Coupling, network topology and the Opto-PING bridge

The Opto-PING line asks whether reciprocal dynamics between an observed electrical signal and another state could be identified under declared measurement and noise conditions. Human KHT models translate that modeling question to EEG-derived features. Topo-OSM frames the human state as inferred network organization and persistence. A successful fit at one scale does not establish the proposed mechanism at another.

[Concept guide](README.md) · [Current algorithm map](../algorithms/README.md) · [Opto-PING programs and results](../optoping/README.md) · [Complete research ladders](../ladders/README.md)

## Keep the endpoints distinct

The [HumanTranslation KHT v0.2 note](../measures/originals/master-suite-v1-3-kht/HUMAN_TRANSLATION_KHT_v0_2.md) separates three endpoints:

| Quantity | Inputs and intended role | What the estimate does not establish |
| --- | --- | --- |
| `K_math` | Coupling endpoint recovered from a specified synthetic generator | Existence of that generator in biology |
| `K_HT` / `K_HT-topo` | Reciprocal association estimated from human feature/state proxies | Direct hidden cellular state or a cellular coupling parameter |
| `K_OSM` | Reserved for future mechanism-specific evidence at the relevant biological scale | Not measured merely by fitting scalp EEG proxies |

CAI v0.2 also uses a symbol `K` for its positive-product/local-correlation composite. That is a different definition, described in [the CAI guide](cai-sid.md).

## Synthetic reciprocal model and composite K

[Formula Report v1.0, section 38](../collections/public-docs/Formula_Module_Report_v1_0/PRAYCG_Formula_Module_Report_v1_0.md#38-opto-ping--rung-0-synthetic-model) describes the hidden reciprocal model:

```text
E_(t+1) = a_E*E_t + eta_E*Y_t + b_E*u_t + eps_E,t
Y_(t+1) = a_Y*Y_t + zeta_E*E_t + b_Y*u_t + eps_Y,t

K_loop = eta_E*zeta_E
K = sqrt(abs(eta_E*zeta_E))
```

`E` is the electrical/work state in that model, `Y` the candidate hidden state, and `u` the external input. `eta_E` and `zeta_E` describe the two modeled directions. Earlier positive-coupling synthetic specifications write `K=sqrt(eta_E*zeta_E)` within their positive domain. The later magnitude expression keeps the product sign conceptually separate; an equal magnitude does not imply equal directional signs or mechanisms.

The composite can be more identifiable than each directional coefficient when a ridge of different parameter pairs produces similar predictions. Recovering `K` therefore does not mean both directions were individually recovered. The model, observation equation, proxy calibration, noise assumptions, stimulus input and alternatives determine what is identifiable.

The report's joint innovation objective is:

```text
NLL(theta) = sum_c sum_k [log|S_k^(c)|
                        + v_k^(c)^T*inv(S_k^(c))*v_k^(c)]
```

`v` and `S` are Kalman innovations and their covariance, with fitting pooled over specified conditions. This report-level objective is not a statement that every human KHT module uses a Kalman/UKF estimator; the early human translation is explicitly simpler.

## Why recovery is insufficient without null specificity

The [Opto-PING inventory](../optoping/README.md) retains the complete documented Rung 0 sequence. Earlier 0A–0I stages are historical descriptions without located standalone packages; 0J–0O have preserved runnable synthetic packages. The sequence tests increasingly demanding questions:

- Positive-loop recovery and frozen fresh-seed sensitivity in 0J, followed by the 0K handoff/internal replay package.
- No-loop “empty sky” alternatives in 0L and stronger null-aware selection in 0M, both retaining partial/failed specificity results.
- A repaired specificity design in 0N and its unchanged, fresh-seed locked reproduction in 0O.

The final null-aware logic requires predictive model superiority **and** a K-significance threshold; a full model's predictive win alone can be too permissive under alternative generators. The [0O README](../studies/optoping-rung0/Rung0O_LockedNullAwareReproduction/README_RUNG0O.md) records a fixed penalty, generator-specific thresholds inherited from 0N without recalibration, and a locked synthetic reproduction pass.

That result supports sensitivity/specificity under the supplied synthetic design and seeds. It does not establish a cellular mechanism, validate a human proxy or demonstrate independent external reproduction. For exact program versions, result counts, frozen specifications and checksum/line-ending notes, use the [program hub](../optoping/README.md) and [reproducibility guide](../reproducibility/README.md).

## HumanTranslation KHT v0.2: feature-model bridge

The [v0.2 module note preserved with Suite v1.3](../measures/originals/master-suite-v1-3-kht/HUMAN_TRANSLATION_KHT_MODULE_v1_3.md) calls this a rough Rung 1 translation. Its variables are:

```text
E_human(t): EEG gamma/work proxy
Y_HT_proxy(t): TSP or posterior-temporal gamma proxy,
               adjusted against task, visual and artifact terms
V_proxy(t): first difference of Y_HT_proxy(t)
K_HT = sqrt(eta_(E<-Y)*zeta_(Y<-E))
```

The coefficients are standardized OLS/state-space **proxy** coefficients in human-feature tables. They are not the synthetic generator's directly known parameters. This early specification uses a positive-product expression; later CandidateLocal and topological notes define magnitude with an absolute product and retain sign separately. Preserve that version difference rather than silently applying an absolute value to every historical equation.

Minimum inputs are feature rows, segment/phase labels and window timing. Recommended covariates include media manifests/fingerprints, cue schedules, annotations, photodiode timing and available EOG/EMG/autonomic channels. Exogenous media and QC features belong in `u(t)` rather than being relabeled as the hidden state.

The module compares a full reciprocal model with E-autoregressive/replay-only, sensory/task/artifact, generic theta/artifact and Y-proxy-autoregressive alternatives. Outputs include requirements/input audits, phase-wise coefficients/coupling, leave-segment-out comparisons and gate decisions. The note explicitly reserves true UKF/state-space likelihood, richer media merging, timing correction and leave-stimulus-out validation for future development. Use the [current implementation map](../algorithms/README.md) for what the proposed Workbench package actually runs.

## CandidateLocal KHT v0.1: event-level coupling plus handoff

The [CandidateLocal note, filename v1.4](../measures/originals/master-suite-v1-5-5/CANDIDATE_LOCAL_KHT_v1_4.md) estimates local regressions:

```text
E_next ~ E_t + Y_HT_t + artifact_t
Y_HT_next ~ Y_HT_t + E_t + artifact_t

eta = Y_HT -> E coefficient
zeta = E -> Y_HT coefficient
K_local = sqrt(abs(eta*zeta))
```

The product sign is retained separately. The event lock requires local coupling **and** a post-event theta handoff; neither alone is sufficient. Timing, artifact, condition specificity and alternative-model checks remain necessary to interpreting an event.

Anchors discovered from the same physiology are exploratory in that run. Annotation-file anchors are secondary unless explicitly predeclared; prospective/media-structural anchors need their loading/locking history retained before any confirmatory interpretation. The outputs preserve local analysis, anchor manifest, random-anchor reference, interpretation and overlay tables. Passing a local event rule does not establish a human EEG mechanism.

## Topo-OSM v0.1: specify what “opto,” “structural” and “memory” mean

The [network-state reformulation v1.4.7](../measures/originals/master-suite-v1-5-5/TOPO_OSM_NETWORK_STATE_REFORMULATION_v1_4_7.md) defines the human-scale terms:

- **Opto:** externally structured audiovisual input, including luminance, motion, faces, cuts, speech, audio envelope, cues and scene structure. ALS/display measurements are input/timing evidence.
- **Structural:** geometry, graph organization and persistence of measured brain-body dynamics.
- **Memory:** hypothesized state persistence, retrievability and reactivation, requiring evidence beyond a score's name.

Its schematic state and model are:

```text
Y_topo(t) = Phi[A_theta(t), A_gamma(t), A_alpha(t),
                TSP(t), API_A(t), Resp(t), Artifact(t)]

E_(t+Delta) = a_E*E_t + eta_HT*Y_topo,t + B*u_t + eps_E
Y_topo,(t+Delta) = a_Y*Y_topo,t + zeta_HT*E_t + C*u_t + eps_Y
K_HT-topo = sqrt(abs(eta_HT*zeta_HT))
```

`Phi` is a proposed feature-to-state construction, not one fully specified frozen estimator. A topology claim requires the actual graph/state features, construction, normalization and persistence criterion to be declared. Merely renaming a gamma or coupling column does not demonstrate graph reconfiguration or persistent memory.

The [claim-boundary note](../measures/originals/master-suite-v1-5-5/TOPO_OSM_CLAIM_BOUNDARY_v1_4_7.md) separates **OSM-TOP**, which is studied indirectly through human network-state proxies, from **OSM-CELL**, which would require direct mechanism-specific measurements. Scalp EEG, physical display light and a fitted `K_HT-topo` do not identify biological photons, microtubule resonance, a cellular hidden state or molecular memory. The research question at the human scale is whether structured audiovisual input is associated with condition-specific, confound-controlled changes and persistence in measured brain-body dynamics.
