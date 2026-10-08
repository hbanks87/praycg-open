# Gamma Scalpel 2.0

Gamma Scalpel 2.0 reviews 30–45 Hz power at the EEG electrodes actually recorded. When the recording includes suitable muscle (EMG) or eye (EOG) measurements, it also shows how gamma changes after screening windows with elevated reference activity. The original recording and existing Master Suite reports remain untouched.

In the Analysis Forge, keep the recording selected and choose **Gamma Scalpel 2.0**. Open its report from Results. A failed strict EEG quality assessment does not prevent this exploratory review; each electrode receives its own continuity, sample coverage and amplitude assessment. A missing or unusable reference is reported as unassessed.

The report contains four views: all finite continuous EEG windows, windows passing the EEG engineering screen, an EEG-proxy comparison, and windows passing the measured-reference screen. It reports duration, mean, median, variability and the influence of the largest power bursts. Missing samples and unsupported windows remain missing.

## Measured reference inputs

The worker accepts recorded streams explicitly typed EEG, EMG and EOG. It requires unique channel labels, a source identity, declared voltage units and a plausible native sampling rate. Voltage and millivolt inputs are converted explicitly to microvolts; native units remain in the report. It does not identify muscles from amplitude or silently choose among multiple EEG streams.

The packaged Cerelog route provides left/right masseter, left/right temporalis and right frontalis EMG, horizontal/vertical EOG, ALS and timing. Its four outlets share a Cerelog clock. That does not synchronize Cerelog with another EEG device. This software does not change Cerelog's current physical validation or acquisition eligibility.

Automatic reference use requires an explicit matching recorded participant identity. A source-bound `gamma_reference_profile_v2_0.json` can supply a reviewed participant/source assignment when the recording does not contain it. Every recorded occurrence of participant, acquisition and sampling-clock identity must agree, including lists and nested metadata. Conflicting values are rejected; they never become missing values that a profile can replace. Duplicate identities, unknown units, invalid clocks and reference streams from another acquisition are excluded with reasons.

For screening, references must share the EEG sampling-clock identity or have documented measured alignment. Independent clocks without this evidence remain available as recorded context; they do not qualify a gamma window as artifact-screened. LSL clock correction alone does not establish physical synchronization. The separate profile guide describes measured offset/drift and residual evidence.

## Methods and interpretation

- EEG uses native samples, two-second **nonoverlapping** windows, linear detrending and Welch power with one-second subsegments. The action requires at least 100 Hz EEG. The displayed gamma bands never use interpolated or reconstructed electrodes.
- Continuity checks require at least 98% expected samples, finite values, edge coverage and no interval exceeding 1.5 native sample intervals. Constant input is unavailable. A 500 µV peak-to-peak engineering caution excludes only that electrode from its screened view; its finite original power remains visible. This limit is an explicitly uncalibrated analysis screen, not a recording gate.
- EMG uses a native-rate 20–min(250, 0.4 × sample-rate) Hz filter and RMS, with a 50 ms envelope percentile. EOG uses a 15 Hz low-pass movement burden, peak-to-peak amplitude and maximum filtered slew. These do not claim validated blink classification or complete microsaccade detection.
- Default reference thresholds are within-recording median plus six robust standard deviations, with a minimum 25% margin. At least five supported windows are needed. An explicit source-bound profile can provide thresholds. Neither mode automatically constitutes physiological calibration. Sustained muscle activation can escape a recording-relative screen.
- A usable measured EMG assessment replaces the corresponding high-frequency EEG proxy assessment in the new screened comparison. EEG integrity and amplitude findings remain. When EMG is unavailable, the 45–55 Hz proxy remains explicitly a proxy, when the rate supports it. EOG absence remains unassessed; EEG amplitude does not establish absence of eye activity. Completely unusable reference channels remain listed; supported channels can still contribute. A gap in an otherwise supported reference channel prevents acceptance of the affected window.
- The legacy Master Suite artifact-score formula is retained as a separate comparison using window median/max EEG amplitude and available measured 45–55 Hz sentinel/all-channel power, with the original sample-standard-deviation normalization. It is evaluated on this module's nonoverlapping windows. The new proxy **screen** is version 2 exploratory policy; it is not an old result or a reproduction of the complete TaskGamma/MeaningGamma scores.
- Alignment residuals up to 250 ms are supported for these two-second window comparisons. Nominal and ±residual shifts must all pass. The report counts acceptance changes under these shifts. Unknown or larger uncertainty cannot support reference-screened outcomes. The 250 ms engineering policy is not a guarantee of waveform alignment; no samplewise regression, subtraction or phase analysis is performed.
- Explicit condition blocks support matching on measured artifact covariates: pooled log-transformed reference features are standardized on one common scale, then matched within a 0.5-standard-deviation maximum-component caliper, without reusing windows. Both conditions have equal matched duration. Gamma is excluded from matching distance. Results remain descriptive; windows are not treated as independent experimental subjects. Unmatched or unsupported conditions are reported.

Condition comparison availability follows actual matched results: no supported pairs means unavailable; mixed available and unavailable electrodes/conditions means partial. Missing EOG is labeled `UNASSESSED_NO_MEASURED_EOG`; an EEG amplitude screen is not an eye-artifact assessment.

Athena has TP9, AF7, AF8 and TP10. This action reports those measured electrodes and their supported windows. It does not assign absent central, parietal or occipital regions, or use Zuna-generated electrodes to satisfy such requirements. Low reference activity does not prove that remaining gamma is neural, or establish a meaning or consciousness outcome.

## Files and provenance

Each attempt creates `report.html`, `gamma_trends.png`, `gamma_windows.csv`, `reference_windows.csv`, `gamma_summary.csv` and `gamma_scalpel_v2_0.json`. The JSON includes source/participant assignments, rates and units, reasons for excluded references, thresholds, timing evidence, exact condition pairs and source/output hashes. Inputs are hash-checked before and after processing. A nonempty attempt folder is refused. Failed attempts retain their error and do not publish valid output bindings.

The worker is `praycg_gamma_scalpel_v2_0.py`. Required arguments are `--run-folder`, `--analysis-root`, `--out-dir`, `--xdf` and `--analysis-window-manifest`. Optional arguments are `--events`, `--recording-conditions`, `--reference-profile` and `--stream-uid`. The analysis-window manifest must bind the exact XDF hash. No live device is opened.

Scientific motivation: [Whitham et al., scalp muscle contamination](https://pubmed.ncbi.nlm.nih.gov/17574912/) and [Yuval-Greenberg et al., eye movements and transient gamma](https://pubmed.ncbi.nlm.nih.gov/18466752/). These observations support measuring artifact references; they do not validate this engineering screen or establish neural origin after screening.
