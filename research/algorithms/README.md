# Algorithms and implementation map

This page connects PRAYCG's named research concepts to inspected code, configuration, inputs and outputs. It distinguishes an implemented calculation from a historical recipe, a proposed measurement and a validated scientific construct. Naming an algorithm here does not certify novelty, biological validity or priority over other work.

[Bibliography and upstream method credits](../bibliography/README.md) · [Concept definitions](../concepts/README.md) · [Measures](../measures/README.md) · [Research ladders](../ladders/README.md) · [Reproducibility](../reproducibility/README.md) · [Workbench](../../workbench/README.md)

## Source and version being described

The implementation reference is the inspected **Public Alpha 11.2.1** distribution, `PRAYCG_Workbench_Public_Alpha_11_2_1.zip`, SHA-256 `cb65ec3180a59a9181e4fecd9bb94a2b136ab158f0f275eaf49b01dc3386c42b`. Its [documentation snapshot and edition boundary](../../workbench/docs/releases/alpha-11.2.1/README.md) describe a proposed update; this page does not imply that the archive is already the published GitHub release. Current-code paths below are relative to its `app/` directory, not paths to an extracted application source tree in this repository.

The [implementation source manifest](SOURCE_MANIFEST.json) records 28 selected implementation/configuration/specification files checked against that archive's bytes, plus nine registry entry identities. It includes exact archive paths, sizes, SHA-256 values and method-version distinctions. This inspection did not execute a scientific analysis, install dependencies, run model inference or test a device. The package's existing [build receipt](../../workbench/docs/releases/alpha-11.2.1/package/app/deployment/validation/ALPHA_11_2_1_BUILD.json) has its own stated scope.

Two registries have different jobs:

- `config/analysis_orchestration_registry_v0_1.json` declares managed module IDs, versions, dependencies, input/output contracts, execution paths and source/configuration hashes. Registration grants no primary-conclusion authority.
- `config/analysis_module_registry_v0_1.json` is a discovery/preflight catalog explicitly marked non-authoritative. Its GUI launcher descriptions do not replace the orchestration contract or a worker's scientific gates.

The paths and versions below identify the implementation to inspect. They are not permission to bypass input resolution, source binding or the Analysis Forge's eligibility checks.

## Managed entry points

| Calculation | Registry ID and module version | Execution source in the inspected package | Status and distinction |
| --- | --- | --- | --- |
| Canonical features, MRED events and human KHT | `master_comprehensive_suite_v1_6_0`, `1.6.0` | `tools/Legacy_Analysis_Managed_v1_0/praycg_legacy_analysis_managed_v1_0.py` dispatches `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_master_comprehensive_suite_v1_6_0.py` | Implemented secondary analysis; actual electrode, protocol, timing and quality requirements still apply. |
| Dependency-aware interpretation chain | `full_chained_analysis_v1_6_1`, `1.6.1` | Same managed adapter; native `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_chain_runner_v1_6_1.py` | Executes named producer steps and preserves their separate missing-input, error and scientific statuses. |
| CAI/SID | `cai_sid_exploratory_v0_2`, `0.2.0` | `tools/CAI_SID_Exploratory_v0_2/scripts/praycg_cai_sid_managed_v0_2.py` | Implemented exploratory diagnostic; equation version `0.2.0`, managed revision `0.2.0-alpha.10.3.8`. |
| Gamma Scalpel | `gamma_scalpel_v2_0`, `2.0.0` | `tools/Gamma_Scalpel_v2_0/praycg_gamma_scalpel_v2_0.py` | Measured-electrode gamma and optional measured-reference screening; separate from regional MeaningGamma/TaskGamma constructs. |
| Optical signal review | `optical_signal_review_v1_0`, `1.1.0` | `tools/Optical_Signal_Review_v1_0/praycg_optical_signal_review_v1_0.py`; profile support in `praycg_optical_profiles_v1_0.py` in the same folder | Raw exploration is implemented. Relative hemoglobin conversion is conditional on a verified profile and supported recorded data. |
| Signal support review | `signal_quality_review_v1_0`, `1.0.0` | `tools/Signal_Review_v1_0/review_service.py`, mode `quality`; source contract in `recording_contract.py` | Inspection/visualization scope; does not alter another module's eligibility. |
| Line-noise comparison | `line_noise_comparison_v1_0`, `1.0.0` | `tools/Signal_Review_v1_0/review_service.py`, mode `denoising`; transforms in `denoising.py` | Exploratory comparison, method revision `PRAYCG_DenoisingComparison_v1.0.0`; no automatic adoption. |
| ECG/HRV and respiration review | `ecg_heartbeat_hrv_review_v1_0` and `respiration_rsa_review_v1_0`, both `1.0.0` | `tools/Signal_Review_v1_0/review_service.py` and `physiology.py` | Offline physiology review; `physiology.py` identifies revision `1.0.0-alpha11.2.0`. |

NIP, A-MRED, NUPI, TTI and DGA are native steps inside the full chain, not separately named top-level orchestration entries in this map. Their scientific names, conceptual versions, script filenames and runtime versions are distinct identifiers.

## Native concept implementations inside the Master Suite

All native filenames in this table are within `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/` in the inspected package.

| Concept family | Source and callable or chain step | Implementation identity and limits |
| --- | --- | --- |
| MRED event candidates and KHT | `praycg_master_comprehensive_suite_v1_6_0.py`: `run_human_translation_kht()`, `run_candidate_local_kht()` and their feature/event producers | HumanTranslation KHT v0.2 and CandidateLocal computations are retained exploratory human-feature models. They do not observe cellular hidden Y or estimate K_OSM. |
| NIP, BIT, CII, IAQ, CET/CET-R and EET | `praycg_nip_cet_eet_modules_v1_6_0.py`: `run()`; chain step `nip_cet_eet` | The filename says v1.6.0, while the inspected code declares `VERSION="1.6.1"`. Concept labels such as `NIP_v0.1` remain separate. |
| A-MRED | `praycg_amred_endpoint_module_v1_6_0.py`: `run_amred()`; chain step `amred` | Version `1.6.0`, schema `PRAYCG_A_MRED_PrimaryEndpoint_v1_6_0`. Uses anchor lock, recognition/integration comparisons and eligibility evidence; “PrimaryEndpoint” in a name does not establish successful confirmation. |
| MRED/ITP, ACG and OCU | `praycg_mred_itp_modules_v1_6_0.py`: `run_analysis()`; chain step `mred_itp` | Version `1.6.0`. Requires XDF, event, annotation, canonical-feature and MRED-event inputs; contains montage-specific assumptions that cannot be transferred to arbitrary electrodes. |
| MRED-Peak / MRED-Resolution | `praycg_mred_peak_resolution_module_v1_6_0.py`: `load_inputs()`, `build_anchor_table()`; chain step `mred_peak_resolution` | Runtime version/schema `1.6.0`, despite a retained v1.5.5 description in the file header. Compresses prior outputs; it is not independent physiological evidence. |
| NUPI | `praycg_nupi_module_v1_6_0.py`: `run_module()`; chain step `nupi` | Output identifies `NUPI_v0.1`, implementation version `1.6.0`, revision `alpha10.3.8.optional-table-schema-v1`. Its current component recipe differs from historical companion formulas. |
| TTI / reception-extraction | `praycg_tti_reception_extraction_module_v1_4_8.py`: `build_composite_feature_scores()` and downstream contrasts; chain step `tti` | Version `1.4.8`; exploratory contrast of receptive feature support and task/extraction burden, not a thermodynamic or moral measurement. |
| DGA | `praycg_decoder_gate_availability_module_v1_5_6.py`: `compute_branch()`, `analyze()`; chain step `dga` | DGA v0.1 in the v1.5.6 component; deterministic rule-based availability/profile interpretation, not a validated decoder of consciousness. |
| Topo-OSM overlays | `praycg_topo_osm_network_state_module_v1_4_7.py`: `main()` | Retained standalone post-analysis v1.4.7 source, distinct from the chain steps listed above. Aliases human K outputs and builds review overlays; no cellular mechanism measurement. |

The chain first copies identified producer artifacts into a separate dependency workspace. Its `producer_completed()` and `publish_tables()` functions admit tables only from completed producer steps. For example, `nupi` requires a completed `nip_cet_eet` producer and its CII anchor table; a failed producer's partial CII file cannot silently become successful NUPI input. A process exit of zero still does not mean the scientific gates passed.

## CAI/SID: from feature frame to valid-time summaries

The implementation sources are `scripts/praycg_cai_sid_v0_2.py`, `scripts/praycg_cai_sid_managed_v0_2.py`, `scripts/praycg_cai_nast_adapter_v0_2.py` and `config/analysis_config_v0_2.json` under `tools/CAI_SID_Exploratory_v0_2/`. Its packaged mathematical specification is `docs/CAI_SID_MATHEMATICAL_SPECIFICATION_v0_2.md`. The [preserved public specification](../protocols/originals/docs/PRAYCG_v0_93_to_v0_95_Protocols_Theory_and_Analysis_Methods.md#4-caisid-v02--controlled-access-integration-index) and [concept guide](../concepts/cai-sid.md) explain the candidate's interpretation.

1. **Resolve inputs and readiness.** Select a time-resolved feature frame and record its adapters, conditions, block instances, timestamps and required components. The managed adapter may derive NAS with the separately versioned NAST v0.1 component only when NAS is wholly missing. It does not mix partially supplied NAS with automatically generated values or overwrite the original frame.
2. **Reference features.** `robust_reference_z()` uses `0.67448975 × (x − baseline median) / baseline MAD`. The frozen exploratory configuration requires 30 reference rows, clips z scores at ±6 and permits a recorded full-run fallback for legacy data when Baseline 1 is inadequate. That is an explicit exploratory fallback, not an independently validated reference distribution.
3. **Build fast and slow candidates.** Fast E uses sigmoid-transformed available-weight combinations of MeaningGamma/TSP/optional NIP, with nominal weights 0.45/0.35/0.20 and a positive VisualGamma penalty of 0.10. Slow Y also uses an available-input weighted mean, with theta integration/NAS/posterior alpha weights 0.50/0.30/0.20, before the sigmoid. These features are operational inputs, not interchangeable with arbitrary raw band power.
4. **Compute the retrospective loop.** `future_mean_by_block()` takes slow Y from +8 to +30 seconds within the same block, requiring at least five future observations. `corrected_loop_product()` computes `P = 2 × sqrt(max(E−0.5,0) × max(Y_future−0.5,0))`. `combine_loop()` uses `K = 0.70P + 0.30max(rho,0)` when local correlation is estimable; otherwise K remains P. The default correlation window is 31 seconds with at least ten observations. Future values make this a retrospective computation.
5. **Apply penalties and missingness.** `compute_run()` averages positive fast evidence, positive current slow evidence and K, then multiplies by one minus the mean positive artifact/task burden. Required missing components and failed hard-QC windows leave CAI missing. Hard-QC defaults use standardized artifact/HF/P2P thresholds of 5, where the relevant input exists. DGA/context reliability produces a separate sensitivity output and does not replace primary `CAI_core`.
6. **Measure supported time.** The managed revision `alpha10.3.8.condition-alias-v1` retains equation version `0.2.0` and adds `support_duration_weights()`: declared intervals are clipped at neighboring timestamp midpoints, duplicate timestamps share support, and missing intervals receive nominal support without filling long gaps. Only finite CAI contributes to valid-time means, loads and occupancy. This differs from treating every historical row as equal elapsed duration.

The worker preserves the original frozen hash as provenance and binds the corrected implementation separately. Its terminal outcomes distinguish `COMPLETE_WITH_LIMITATIONS`, `NOT_ESTIMABLE` and `SOFTWARE_ERROR`. Bootstrap intervals describe within-run temporal stability; they do not make repeated windows independent participants. A bounded CAI or SID output is not a probability or a validated consciousness measurement.

## NIP to NUPI: a dependency chain, not one universal formula

In `praycg_nip_cet_eet_modules_v1_6_0.py`, the inspected `run()` forms a nonnegative semantic-activation candidate from MeaningGamma, TSP, NAS and alpha-drop inputs, and a resonance/integration candidate using current and future theta support. NIP density multiplies those candidates by artifact and, where available, visual-drive penalties. CII summarizes anchor windows; IAQ compares Target with Override. BIT combines event, recognition, integration, K, artifact and event-lock criteria. CET fits cue/visual tracking and residualization; EET compares supported feature patterns. These are related derived outputs, not independent replications of one result.

Current NUPI `run_module()` then reads CII, ITP, TTI, EET, primary-pass and Baseline-2 tables. Its run-level recipe is:

```text
ALI = mean_available(semantic_intensity, target_specificity,
                     complexity_perturbation, tti_score, primary_pass_score)
RDI = mean_available(B2_regulation, B2_semantic_echo, EET_echo), if B2 is available
NUPI = RDI - ALI
```

The code applies its declared component scaling, clipping and fallback rules before these means. Without Baseline 2 it retains `POLARITY_UNRESOLVED_NO_BASELINE2` and leaves NUPI unavailable. Its current RDI expression has **three terms**; the [historical framework companion](../collections/public-docs/Framework_NUPI_Update_v0_5/README_NUPI_Framework_Update_v0_5.md) includes a self-report echo term, and other historical formula reports have additional components. Preserve the source/recipe identity rather than merging these into a single claimed implementation. See [NUPI, TTI and DGA concepts](../concepts/update-availability.md).

## Human KHT and synthetic Opto-PING are different calculations

The Master Suite's `_phasewise_reciprocal_fit()` fits two ordinary least-squares equations within phases: E from lagged Y/E and available controls, and Y from lagged E/Y and controls. The cross-coefficients are labeled eta and zeta; the code reports their product, a signed square-root magnitude and `K_HT_positive_loop = sqrt(eta×zeta)` when that product is positive. Its `_cv_model_comparison()` uses deterministic five-way interleaved row folds to compare reciprocal and alternative feature models. Those folds do not establish generalization to new participants, stimuli or independent sessions.

The separate CandidateLocal routines evaluate event-local feature patterns. Both use human-derived proxy features; neither observes the true hidden state supplied by an [Opto-PING synthetic generator](../optoping/README.md). [KHT/Topo-OSM concept notes](../concepts/coupling-topology.md) distinguish K_HT, K_HT-topo and mechanism-level K_OSM. Similar symbols do not establish equivalent measurements or causal coupling.

## Gamma Scalpel: measured reference screening

`praycg_gamma_scalpel_v2_0.py` separates source/reference selection (`descriptor()`, `select_references()`), supported native windows (`native_window()`), band power (`bandpower()`), reference activity (`reference_metric()`) and condition matching (`common_scale_matches()`). The retained [method guide](../../workbench/docs/releases/alpha-10.5.2/Gamma_Scalpel_v2_0/README.md) supplies the full estimator and reference contract.

The worker uses native EEG at at least 100 Hz, two-second nonoverlapping windows, linear detrending and Welch power with one-second subsegments for 30–45 Hz gamma. Optional EMG and EOG provide measured muscle/eye screening. Participant/source/units/clock evidence must support their use; independent clocks need measured alignment rather than an assumed synchronization from LSL alone. It compares original continuous, EEG-screened, proxy-screened and measured-reference-screened outcomes, with matched supported portions for eligible conditions.

The output includes retained duration, original versus screened power, reference exclusions and source hashes. It performs no samplewise subtraction, phase alignment or reconstruction of absent regional electrodes. Athena's TP9/AF7/AF8/TP10 support those measured-site results; they cannot supply unrecorded regions required by separate TaskGamma/MeaningGamma endpoints. Quiet references do not establish neural origin.

## Optical review: raw observations and conditional conversion

`optical_spectra()` tries 30-, 10- then 5-second windows and selects the longest preset with full-data support in any sensor. Full and screened spectra share that selected resolution. `normalized_recorded_change()` computes `100 × (value / median_positive_baseline − 1)` only with supported positive baseline observations. This is a change in recorded values, not automatically optical density or hemoglobin.

Reusable instrument profiles are matched and bound by `praycg_optical_profiles_v1_0.py`: `select_instrument()`, `bind_instrument()` and `conversion_profile()` preserve instrument facts and recording-specific identity/baseline. `validate_conversion_profile()` checks distinct measured wavelength pairs, positive source-detector distance/pathlength factors, extinction-matrix dimensions and conditioning. With supported positive intensities, `hemoglobin()` calculates `OD = −ln(I/I0)` and solves the declared modified Beer–Lambert system `diag(distance × pathlength) × extinction × concentration = OD`, reporting relative concentration changes in µM.

The bundled profile `profiles/muse_s_athena_brainflow_raw_v1_0.json` is explicitly a draft raw profile with an empty wavelength mapping and unresolved intensity/geometry/firmware information. Its recognition enables raw review, not Athena HbO/HbR. Read the [reusable profile guide](../../workbench/docs/releases/alpha-10.5.2/Optical_Signal_Review_v1_0/REUSABLE_PROFILE_GUIDE.md) and [Athena source review](../../workbench/docs/releases/alpha-10.5.2/ATHENA_OPTICAL_SOURCE_REVIEW_ALPHA_10_5_2.md) alongside the implementation.

## Signal review: preserve time support and compare transformations

`recording_contract.py` keeps explicit signal types, units, original sample indices and timestamp segments. `quality_review()` in `review_service.py` applies operator exclusions and a new at-most-four-second EEG inspection screen: finite selected support, peak-to-peak at most 500 µV and SD at least 0.1 µV. It can instead use an existing governed Athena mask only when recording identity, mask hash, timestamps and channel labels match exactly. The inspection screen does not grant another worker eligibility.

`compare_denoising()` in `denoising.py` compares the original with the selected current numerical transform, upstream spectrum interpolation and fixed-count ZapLine. The shipped `methods_denoising_v1.json` records PRAYCG's adapter revision, upstream credits and assumptions. Candidates use `mne-denoise==0.0.3`; spectrum interpolation cites Leske/Dalal, and ZapLine cites de Cheveigné. These upstream algorithms should not be attributed as newly invented PRAYCG methods.

By default, the comparison requires independent continuous pieces of at least 16 seconds and five-second edge guards. It preserves gaps and exclusions, uses explicit voltage conversion, and does not resample or repair clocks. Candidate suppressors operate on original data; the current preview can also alter bandwidth/reference. Four-second Hann Welch spectra with 50% overlap describe the transformations and original-minus-transformed signal. Processing uses each whole segment retrospectively. Lower line-frequency power does not identify everything removed as noise, and no method is automatically selected or adopted.

The related `physiology.py` preserves accepted original RR neighbors for RMSSD rather than joining across rejected beats or converting HR into RR. Its comparison methods identify pinned NeuroKit2 and named QRS/peak-correction implementations. Respiration remains a measured relative-signal review. These supporting analyses do not supply absent semantic inputs to CAI or validate a mental-state label.

## Historical source, proposals and remaining evidence

The [preserved Master Suite v1.5.5 source collection](../../archive/software/components/02_CURRENT/03_MasterSuite_v1_5_5/) includes older NIP/CET/EET v1.5.1, A-MRED v1.5.3, NUPI v1.5.4, MRED-Peak/Resolution v1.5.5 and other component scripts. The [legacy KHT v1.3 source](../../archive/software/components/03_Individual%20Files/11_OPTIONAL_LEGACY_CODE_ARCHIVE/legacy_MasterSuite_v1_3_KHT/) and [human-translation note](../measures/originals/master-suite-v1-3-kht/HUMAN_TRANSLATION_KHT_v0_2.md) retain earlier prototype context. They are historical snapshots, not interchangeable replacements for the inspected package's files.

Prospective construct validation, generalization across independent people/stimuli, mechanism-specific cellular evidence and clinical use require separate evidence. The [ladders](../ladders/README.md) state those questions; the [reproducibility hub](../reproducibility/README.md) distinguishes runnable synthetic kits from planned human replication. Keep frozen algorithms, input adapters, quality policies, descriptive profiles and interpretive labels separately versioned. Use the [original-file locator](../../docs/reorganization/original-file-index.md) for former paths and [citations/attribution](../../CITATIONS_AND_ATTRIBUTION.md) for incorporated methods.
