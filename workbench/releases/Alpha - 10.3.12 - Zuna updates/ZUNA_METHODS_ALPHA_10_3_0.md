# Alpha 10.3.0 — Zuna reconstruction methods and limitations

## Scope and estimand

**Zuna EEG Reconstruction — Experimental** asks a narrow question: after hiding four measured scalp electrodes, how closely do Zuna and a conventional spherical-spline method predict the same processed held-out recordings from the remaining twelve electrodes?

It is not an EEG cleaner certified to recover neural ground truth. The measured targets can contain electrical noise, muscle activity, eye artifacts and other contamination. This release does not implement thought-to-text, clinical diagnosis, live model control or an arbitrary-channel consumer-device benchmark.

The companion protocol is **AI-Assisted EEG Reconstruction and Signal Preservation**, `ATLAS_AI_EEG_RECONSTRUCTION_VALIDATION` v1.0. Its task duration is 600 scheduled seconds: 120 seconds eyes-open calibration and eight 60-second eye-state blocks. Four blocks per condition and two complementary orders are fixed by the compiled, fingerprinted session plan. One run is descriptive, not a randomized population trial.

## Frozen input contract

The first profile accepts sixteen physically recorded channels in this exact order:

```text
Fp1 Fp2 C3 C4 P7 P8 O1 O2 F7 F8 F3 F4 T7 T8 P3 P4
```

The predetermined hidden targets are **F3, F4, P3 and P4**. The other twelve electrodes are the only measured model inputs. The operator must explicitly review the real channel-index map, microvolt units and external physical acquisition reference before timed content. Nominal stream labels do not prove electrode placement.

The runner records that declaration in `zuna_validation_contract_v1_0.json`, bound to the protocol, run UUID and compiled timeline. Its self-excluding canonical fingerprint is distinct from the file-byte hash used by the observed-block ledger. This is an operator declaration, not an independent hardware measurement.

A stream already digitally average-referenced across all sixteen electrodes is unsupported. The hidden targets would already have influenced retained inputs. Renaming channels or hiding target columns afterward cannot undo that leakage.

Recorded nonfinite data, backward timestamps, unacceptable acquisition gaps, incompatible rates, flat retained inputs or missing identity evidence are not silently repaired. Required QC remains a separate preserved record.

## Dedicated preprocessing branch

The worker reads the selected raw EEG/XDF analysis window, verifies the relevant QC belongs to that XDF and creates a separate model-input derivative. It does not consume the ordinary all-channel common-average derivative from another module.

The operations are:

1. Resample each channel independently to 256 Hz with SciPy `resample_poly`, preserving the original source timestamps and fractional source-sample map.
2. Apply the same fourth-order Butterworth 0.5–40 Hz bandpass to every channel in second-order-section forward/backward form. This is zero-phase offline filtering, not a causal live filter. Forward/backward application squares the one-pass magnitude response; “fourth order” identifies the one-pass design.
3. Compute the samplewise average of the twelve retained channels only. Subtract that same reference from both the retained inputs and the four held-out measured targets.
4. Run both predictors with those identical retained signals and the same template geometry. No held-out measurement is passed into either predictor.
5. Before scoring, apply a common additional fourth-order 0.5–40 Hz SOS forward/backward filter independently to the measured targets, spline predictions and Zuna predictions. This aligns the comparison bandwidth. Measured targets and spline predictions therefore have both preparation and comparison passes; this is an explicit PRAYCG operational definition, not the upstream benchmark recipe. Unfiltered model predictions remain separately preserved for an out-of-band audit.

Channelwise filtering and resampling do not mix targets into inputs. Input reference, normalization and inverse scaling are calculated from retained data only. The held-out channel set is not selected after examining reconstruction error.

The first 120 seconds are labeled calibration, not an independently validated training dataset. No subject-specific fine-tuning of model weights is performed. With a complete observed eight-block ledger, the prospective endpoint scores only the actual evaluation blocks after their fixed five-second boundary exclusions; calibration is excluded. If that complete ledger is absent, useful whole-window reconstruction metrics can still be labeled exploratory, but the prospective endpoint is explicitly NOT_ESTIMABLE. Planned times never stand in for missing observations. The report and evaluation masks identify the samples actually scored.

The fixed common filter limits the benchmark to its processed bandwidth. A 40 Hz low-pass is not proof that a 60 Hz-contaminated recording has become scientifically clean, and cannot recover physiology lost during acquisition. Original QC warnings remain in force.

## Zuna adapter

The PRAYCG adapter uses the pinned low-level Zuna sampling interface, not the upstream end-to-end preprocessing pipeline. It deliberately bypasses upstream automatic reference, per-channel normalization, masking heuristics, filtering and seam correction.

For each nominal five-second window, it computes one scalar mean and population standard deviation from the twelve retained channels only. Retained input is transformed as:

```text
normalized retained value = (value − retained-window mean) / (10 × retained-window standard deviation)
```

This gives retained inputs a standard deviation of 0.1. Hidden target token rows are zero placeholders added after those statistics are calculated. Model predictions are converted back using the same retained-only scalar transformation. A short final window is padded to the model's token-grid requirements; padded samples are dropped and do not receive invented original timestamps.

The frozen default is 256 Hz, 1,280-sample windows, 16 diffusion sampling steps, guidance 1.0, float32 CPU inference and seed 20260924. Per-window seeds and normalization values are recorded. The adapter caps CPU compute threads at two. The report preserves the actual runtime versions and model/adapter hashes.

MNE standard-1020 template electrode coordinates are transformed into head coordinates and supplied to both methods. These are not participant-specific digitized locations. Zuna's pinned spatial token encoding is separately recorded, including any coordinates clipped to its encoding bounds.

This operationalization differs materially from the original paper's evaluation and the upstream default pipeline. A PRAYCG result must not be presented as a replication of published benchmark accuracy. Fixed seeds improve traceability but do not promise bitwise equality across processors, libraries or operating systems.

## Conventional comparator

The comparator uses MNE's public `Raw.interpolate_bads` API with EEG spherical splines, `mode="accurate"`, and the explicit sphere origin `(0, 0, 0)` in the same head-coordinate frame.

The twelve retained signals are measured inputs. Four zero placeholder rows mark targets as bad before interpolation. No held-out measured samples are used to fit the interpolation. Results are converted back to microvolts for comparison. Template geometry and the fixed origin are assumptions disclosed here, not individual head-model measurements.

Method lineage: Perrin, Pernier, Bertrand and Echallier, “Spherical splines for scalp potential and current density mapping,” 1989, [DOI:10.1016/0013-4694(89)90180-6](https://doi.org/10.1016/0013-4694(89)90180-6). The operational implementation is the installed [MNE interpolation API](https://mne.tools/1.10/generated/mne.io.Raw.html#mne.io.Raw.interpolate_bads), with its version preserved per run.

## Numerical comparison

For measured target samples `y` and predictions `p`, over the same accepted sample mask:

```text
MSE    = mean((p − y)²)
RMSE   = sqrt(MSE)                          [microvolts]
MAE    = mean(abs(p − y))                   [microvolts]
NMSE   = MSE / mean((y − mean(y))²)         [dimensionless]
```

Errors are reported per held-out electrode. The primary displayed summary is the mean of estimable per-electrode NMSE values—not a claim that electrodes or windows are independent participants. The report also shows **Zuna NMSE minus spherical-spline NMSE**: negative favors Zuna, positive favors the conventional baseline.

The target variance uses the population divisor on the observed evaluation samples. A target variance at or below the implementation's numerical tolerance yields an undefined/null NMSE with an explanation. Zero is reserved for an actual zero error, not missing data.

Pearson correlation is secondary and is undefined when either series has inadequate variance. Correlation alone does not demonstrate calibrated amplitude or remove shared-artifact explanations. A high correlation with a large RMSE is possible.

No inferential p-value, population confidence interval, effective independent sample count or superiority claim is obtained by treating successive samples/windows as separate participants. One recording can support a descriptive comparison and motivate further controlled validation.

## Timing and spectral descriptions

The runner writes `zuna_observed_blocks_v1_0.json` incrementally and atomically only after real block offset markers occur. It contains actual LSL-clock onset/offset values and the exact validation-contract file hash. Calibration is a separate interval. An interrupted block never receives a fabricated completion time.

Eye-state comparisons use observed intervals, not the planned schedule and not labels inferred from EEG amplitude. The protocol's fixed transition exclusion is five seconds at each block boundary; this is a conservative analysis convention, not measured evidence of how quickly a participant changed eye state. Outer filtering-edge exclusions are separately recorded. Audio-play requests coincide with display-flip callbacks, but speaker latency and physical eye closure/opening are not measured.

Spectral summaries are descriptive. The fixed Welch estimator uses two-second Hann windows, 50% overlap, constant detrending and density scaling. It operates separately within each contiguous included interval and combines spectra using the number of complete Welch windows as weights; it never treats separated blocks as adjacent samples. Trapezoidal band integration produces microvolt-squared values. The reported operational bands are theta 4–8 Hz, alpha 8–13 Hz and beta 13–30 Hz. Band names do not establish a mental state. Eye-state contrast is closed minus open alpha-band power where usable observed blocks support both conditions. Missing boundaries or inadequate support remain not estimable. These filtered comparisons do not validate out-of-band fidelity of the raw model output.

Welch method lineage: P. D. Welch, 1967, [DOI:10.1109/TAU.1967.1161901](https://doi.org/10.1109/TAU.1967.1161901); operational API: [SciPy 1.16.2 Welch](https://docs.scipy.org/doc/scipy-1.16.2/reference/generated/scipy.signal.welch.html). Actual settings are those above and in the saved worker provenance, not an unspecified appeal to a standard method.

## Outputs and boundaries

Each successful module execution writes:

- HTML and JSON comparison reports, with a plain-language interpretation.
- A per-method, per-electrode metrics CSV.
- Model/software/method provenance, frozen settings, observed versions and hashes.
- A generated-data mask description.
- A separate array archive containing prepared retained inputs, held-out measured targets, Zuna estimates, spline estimates, sample masks, retained-only reference and original-to-model timestamp/sample mapping.

The original XDF is not edited. Generated values are explicitly distinguished from measured targets. They do not satisfy measured-hardware eligibility and do not automatically feed other analysis modules. Interrupted or failed jobs retain their disclosed status; an error report is not a successful analysis.

The comparison report and relevant provenance are automatically eligible for the selected analysis folder's Research Bundle export. Waveform arrays require the private full-telemetry opt-in. Model weights and virtual environments are software installation artifacts, not study telemetry and not study-bundle contents.

## Upstream identity and rights

The authoritative local record is [the model lock](../config/zuna_model_lock_v1_0.json).

| Item | Frozen identity |
| --- | --- |
| Upstream package | Zuna 1.1.6, exact publisher-wheel SHA-256 in the lock |
| Model | `Zyphra/ZUNA1.1` |
| Model revision | `10b9d6c8285ab808685f079f586bdafe3ad2c9a3` |
| Weight SHA-256 | `295fcddb42ab4623dc1346fba12176798d97ab95389c666907e32cbce23f7f33` |
| Distribution | Explicit optional installation from upstream; neither wheel nor weights shipped in the PRAYCG release |

Primary project records are [Zyphra's Zuna page](https://www.zyphra.com/our-work/zuna), the [upstream source repository](https://github.com/Zyphra/zuna), the [pinned model revision](https://huggingface.co/Zyphra/ZUNA1.1/tree/10b9d6c8285ab808685f079f586bdafe3ad2c9a3), and the [original technical report](https://arxiv.org/abs/2602.18478). The separately observed repository-main commit is not substituted for the exact executed wheel identity.

Project/model metadata identifies Apache-2.0. The reviewed wheel also includes Meta copyright headers and a Llama 2 notice in an embedded file. This discrepancy remains an unresolved upstream provenance/licensing limitation. PRAYCG does not overwrite those notices, claim complete upstream clearance, or treat all dependencies as Hoyt Banks MIT code.

The installer inventories installed distributions and retains available license/notice files beside its receipt. Top-level dependency versions are specified; an observed inventory is not a promise that all transitive resolutions or native-library builds will be identical forever. Imported libraries, their native dependencies, the model and this PRAYCG adapter have separate identities and rights.

Citations identify intellectual or software lineage; they are not permission to redistribute everything encountered and do not imply upstream endorsement. The [master attribution document](../CITATIONS_AND_ATTRIBUTION.md) describes the broader existing audit and its limitations.

## What would justify a stronger claim later?

A larger prospectively specified comparison should include multiple independent recordings/participants, verified wiring and reference, independently checked timing, diverse artifact conditions, alternative conventional baselines, sensitivity to montage and preprocessing, and held-out evaluation that does not guide model or parameter selection. Subject overlap with upstream training data and external generalization also require scrutiny.

Until that evidence exists, the correct statement is bounded: this exact pinned implementation produced the reported reconstruction errors on this exact recording under these declared assumptions.
