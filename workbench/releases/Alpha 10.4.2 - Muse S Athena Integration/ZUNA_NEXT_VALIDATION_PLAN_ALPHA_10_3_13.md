# Zuna missing channel replication plan

This plan asks whether the frozen PRAYCG Zuna pipeline provides a repeatable, practically useful reconstruction of withheld measured electrodes. Previous recordings are development data: their conflicting results motivate replication but cannot count as independent confirmation. A lower error than a poor interpolation baseline is not enough.

The machine-readable plan is `../config/zuna_next_validation_plan_v1_0.json`. Its companion frozen receipt binds the exact plan, model lock, adapter, numerical preparation, reporting implementation and optical design by SHA-256. These are local records, not external preregistration, automatic study enrollment or automatic enforcement of the criteria below. Preserve both files with each intended replication session before collecting data. The operator and reviewer must check compliance; the normal Run button does not certify it.

## Before the next recording

First resolve the software placement and stream-identity checks in Alpha 10.3.13. Use ALS Holder Calibration, perform the placement check, then confirm the steady patch preview in the actual runner window. The saved square must be wholly under the sensor on the selected display. Keep the discovered current-session ALS identity; do not paste an older run's identifier. These setup checks are not measured optical timing. Inspect recorded light edges afterward, and retain any optical limitation separately from EEG eligibility.

Use **EEG reconstruction validation with optional optical timing version 3.1**, the updated optical protocol in this release. Keep the 120-second calibration followed by eight 60-second evaluation blocks. The protocol allocates one of two complementary eye-condition orders before acquisition; preserve the assigned compiled timeline rather than choosing an order after results. Keep the declared 16-channel PRAYCG order and the physically reviewed reference; retain F3, F4, P3 and P4 as the four hidden targets. Do not remove C4 because of the earlier result. Check wiring/contact prospectively and record what was actually done. Template geometry is not an individually measured electrode map.

Use the pinned model and adapter, seed 20260924, 16 sampling steps, five-second contexts and eight CPU threads. Keep the release's boundary-safe preparation, retained-only reference/normalization, filtering and original spherical-spline baseline unchanged. All methods must score the same measured targets on the same masks. Do not align predictions to the answers, fit a target-based amplitude correction, try alternate seeds, or stitch missing samples.

## Sessions and stopping rule

Collect at most four acquisition attempts on separate calendar days. Evaluate the first three eligible sessions in acquisition order. Determine eligibility from identity, coverage and timing evidence before examining reconstruction errors. Keep an attempt ledger with every recording, failure and exclusion; sessions with unfavorable model scores cannot be replaced.

Every eligible session must have all eight observed blocks and at least 40 scored seconds per block, matching the existing reviewed analysis route, after its five-second boundary exclusion and analysis-window checks. Missing or nonfinite data, ambiguous identity/reference and unsupported timing remain analysis limitations; recording-level warnings alone do not exclude data. A zero-variance target makes the normalized endpoint not estimable rather than silently removing that channel.

Stop after three eligible sessions or four attempts, whichever comes first. Fewer than three eligible sessions is inconclusive. Failure to meet the criteria means no demonstrated benefit under this plan, not permission to keep collecting until results improve. Infrastructure checkpoint resume may continue an identical computation, with the interruption recorded; it is not an opportunity to change the seed or method.

## What counts as a useful result

The following numerical margins are explicit **project engineering choices**, not universally accepted neuroscience thresholds or a powered statistical test. Every criterion must hold in each of the three eligible sessions:

1. Zuna's mean normalized squared error is at least 10% lower than the original spline baseline, both overall and separately for eyes-open and eyes-closed blocks. The primary mean gives equal weight to all 32 block-by-target cells; condition means use their 16 cells, and each-target means use its eight blocks. These use the common final-filter endpoint, not pooled-sample scores.
2. For every hidden electrode, Zuna's mean normalized error is lower than the fixed all-zero prediction and no more than 10% worse than spline. The zero comparator has no fitted parameters; it is a diagnostic benchmark, not an EEG reconstruction method.
3. For every target and eye condition, the predicted-to-measured standard-deviation ratio is between 0.80 and 1.25. The plan specifies within-block variance aggregation so changes in block means are not miscounted as reconstructed fluctuation.
4. For every target and eye condition, the integrated absolute PSD difference over 0.5–40 Hz is no more than 25% of the measured total power over that band. This is a planned reviewer calculation from saved common-final-filter arrays, not a score that Forge newly emits or automatically enforces. Use two-second periodic-Hann Welch windows at 256 Hz with 50% overlap, constant detrending, one-sided density scaling and mean aggregation. Within each block, weight contiguous intervals by their complete Welch-window counts; then average the four block spectra equally within each condition. Compute the ratio only after that aggregation, including bin centers from 0.5 through 40 Hz. Do not concatenate across gaps. The JSON specifies the formula and minimum-support rules exactly.
5. The complete comparison takes no more than 40 minutes on the declared eight-thread machine, excluding model installation/download. Preserve hardware, software, workload, timing and failure information.

Report RMSE and MAE in microvolts, normalized errors, target variance, sample counts and all comparator results. Target variance at or below 1e-12 microvolts squared makes NMSE undefined. Spectral results require at least one complete Welch window in every block and measured condition band power above 1e-12 microvolts squared. Undefined metrics are not success. Preserve both the primary equal-cell score and supplementary pooled scores with their different weighting made explicit.

## Blinks and eye condition

The earlier idea that blinking increases after eye opening remains a hypothesis, not a measured explanation. Keep those samples in the primary endpoint except for the unchanged five-second edge exclusion. Separately describe early eyes-open samples from 5–20 seconds and later samples from 20–55 seconds, with matched eyes-closed intervals. Do not call an amplitude proxy a confirmed blink count or choose exclusions after seeing which method benefits.

Report measured and reconstructed eyes-open/eyes-closed alpha differences as secondary descriptive outcomes. A small measured contrast does not prove poor instruction compliance, and additional alpha power does not prove successful cleaning.

## Interpretation and amendments

Three recordings from one person provide personal feasibility evidence, not three independent participants or population validation. Many windows within a recording are not independent replications. The withheld targets are measured EEG, including its contamination, rather than clean neural ground truth. The offline filtering, timing approximation, model context seams and template coordinates remain limitations.

Passing this plan supports only the specified missing-channel use case. It does not establish artifact removal, clinical usefulness, extra physically measured channels, an effective decoder or safe real-time adaptation. Mixed or negative results keep Zuna optional and experimental, with interpolation remaining the conventional default. Live adaptation still needs separate downstream usefulness, causal replay, measured latency and shadow-mode evidence.

Any change to the scientific recipe, targets, thresholds or stopping rule requires a new plan identifier and a new freeze before new data. Preserve this plan, original reports and all attempts. Do not rewrite earlier bench/acquisition labels, optical evidence or historical conclusions.
