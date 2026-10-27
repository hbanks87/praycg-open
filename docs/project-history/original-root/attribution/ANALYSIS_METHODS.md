# Reviewed analysis methods

Attribution registry revision 1.0.0; source-formula review, not scientific validation. Definitions below describe PRAYCG's actual implementation and record important differences from the cited lineage. No numerical code was changed by this update.

## Module coverage

| Module | Reviewed method records | Status |
| --- | --- | --- |
| `run_integrity_timing_qc_v0_1` | none assigned | METHOD_REVIEW_PENDING |
| `atlas_meditation_vs_thinking_v0_1` | none assigned | METHOD_REVIEW_PENDING |
| `master_comprehensive_suite_v1_6_0` | none assigned | METHOD_REVIEW_PENDING |
| `full_chained_analysis_v1_6_1` | none assigned | METHOD_REVIEW_PENDING |
| `hocr_shotorder_v1_6_0` | none assigned | METHOD_REVIEW_PENDING |
| `confound_expansion_v1_5_7` | none assigned | METHOD_REVIEW_PENDING |
| `cai_sid_exploratory_v0_2` | none assigned | METHOD_REVIEW_PENDING |
| `continuous_autonomic_respdualpath_v1_0` | none assigned | METHOD_REVIEW_PENDING |
| `micro_handoff_v0_1` | none assigned | METHOD_REVIEW_PENDING |
| `cue_locked_gamma_forensics_v0_1` | none assigned | METHOD_REVIEW_PENDING |
| `master_sync_visualizer_v1_4_0` | none assigned | METHOD_REVIEW_PENDING |
| `offline_master_interpreter_v1_6_0` | none assigned | METHOD_REVIEW_PENDING |
| `eeg_signal_quality_v0_1` | welch | REVIEWED_SUBSET |
| `eeg_preprocessing_derivative_v0_1` | none assigned | REVIEWED_SUBSET |
| `eeg_spectral_aperiodic_v0_1` | welch, aperiodic | REVIEWED_SUBSET |
| `eeg_erp_time_frequency_v0_1` | erp | REVIEWED_SUBSET |
| `eeg_connectivity_pac_v0_1` | connectivity, pac, bh | REVIEWED_SUBSET |
| `eeg_complexity_v0_1` | sample_entropy, permutation_entropy, lz, spectral_entropy | REVIEWED_SUBSET |
| `eeg_microstates_v0_1` | microstates | REVIEWED_SUBSET |
| `eeg_motor_imagery_v0_1` | csp, lda | REVIEWED_SUBSET |
| `eeg_sensor_rsa_v0_1` | rsa | REVIEWED_SUBSET |
| `torcheeg_research_sandbox_v0_1` | none assigned | METHOD_REVIEW_PENDING |
| `atlas_research_analysis_v1_0` | none assigned | METHOD_REVIEW_PENDING |

## Welch PSD

**Definition:** SciPy Welch PSD: average of segment periodograms; parameters come from the module configuration and installed SciPy defaults.

**Limitations and material differences:** Different call sites use different segment lengths. Preserve configuration and SciPy version; no claim that all call sites share one estimator configuration.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_quality_scope`, `run_spectral`, `_spectral_entropy`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

- Welch PD (1967). The use of the fast Fourier transform for the estimation of power spectra. [Primary reference](https://doi.org/10.1109/TAU.1967.1161901).

## Log-log robust aperiodic screening

**Definition:** Theil-Sen fit of log10 PSD against log10 frequency after configured exclusions; exponent=-slope, intercept and median absolute residual retained.

**Limitations and material differences:** Not specparam/FOOOF; excluded bands and positive-power masking define the PRAYCG screen.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_aperiodic_screen`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

- Sen PK (1968). Estimates of the regression coefficient based on Kendall's tau. [Primary reference](https://doi.org/10.1080/01621459.1968.10480934).

## Recipe-defined ERP and Morlet power

**Definition:** Trial baseline subtraction, trial mean and SEM; Gaussian complex carrier sigma=cycles/(2*pi*f), truncated to min(half epoch, ceil(3.5*sigma*fs)), L2 normalization, convolution power averaged across trials; baseline ratio in dB.

**Limitations and material differences:** PRAYCG operational implementation, not a validated named ERP component. No zero-mean wavelet correction or cone-of-influence exclusion; epoch boundaries can bias power.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_morlet_power`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

PRAYCG operational definition; no external exact-estimator equivalence asserted.

## Band-pooled spectral connectivity

**Definition:** Hann-window FFT; cross spectra averaged over frequencies within each epoch and then epochs. Coherence=abs(mean cross)^2/(mean power x * mean power y); PLI=abs(mean sign(imag cross_epoch)); wPLI=abs(mean imag cross_epoch)/mean abs(imag cross_epoch).

**Limitations and material differences:** wPLI is not debiased squared wPLI. Band pooling differs from frequency-resolved estimators. Signed imaginary coherency is mirrored into both matrix triangles; it must not be interpreted as a conventional antisymmetric imaginary-coherency matrix. References identify lineage, not estimator equivalence.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_connectivity_matrices`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

- Vinck M et al. (2011). An improved index of phase-synchronization for electrophysiological data in the presence of volume-conduction, noise and sample-size bias. [Primary reference](https://doi.org/10.1016/j.neuroimage.2011.01.055).
- Nolte G, Bai O, Wheaton L, Mari Z, Vorbach S, Hallett M (2004). Identifying true brain interaction from EEG data using the imaginary part of coherency. [Primary reference](https://doi.org/10.1016/j.clinph.2004.04.029).
- Stam CJ, Nolte G, Daffertshofer A (2007). Phase lag index: assessment of functional connectivity from multi channel EEG and MEG with diminished bias from common sources. [Primary reference](https://doi.org/10.1002/hbm.20346).

## Binned phase-amplitude modulation index

**Definition:** Mean amplitude per phase bin, normalize to probabilities p; MI=(log(K)+sum(p*log(p)))/log(K), empty bins initially zero.

**Limitations and material differences:** Tort-style modulation index; filtering, surrogate construction and trial handling are PRAYCG-specific. MI alone does not establish physiological coupling.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_pac_mi`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

- Tort ABL, Komorowski R, Eichenbaum H, Kopell N (2010). Measuring phase-amplitude coupling between neuronal oscillations of different frequencies. [Primary reference](https://doi.org/10.1152/jn.00106.2010).

## Benjamini-Hochberg adjustment

**Definition:** Sort p-values, multiply by comparison count/rank, apply reverse cumulative minimum and restore order.

**Limitations and material differences:** The code supplies the family of comparisons. Appropriate dependence assumptions and family definition remain necessary.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_benjamini_hochberg`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

- Benjamini Y, Hochberg Y (1995). Controlling the false discovery rate: a practical and powerful approach to multiple testing. [Primary reference](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).

## Sample entropy and coarse-scale screening

**Definition:** Aligned m and m+1 embeddings; unordered non-self pairs within Chebyshev distance r*SD; SampEn=-log(A/B). Missing when either pair count is zero.

**Limitations and material differences:** Coarse-graining uses non-overlapping means, but tolerance is recomputed at each scale rather than fixed to original-signal SD. Complexity input may be stride-decimated without a new antialias filter. Do not present this as equivalent to canonical multiscale entropy.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_sample_entropy`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

- Richman JS, Moorman JR (2000). Physiological time-series analysis using approximate entropy and sample entropy. [Primary reference](https://doi.org/10.1152/ajpheart.2000.278.6.H2039).
- Costa M, Goldberger AL, Peng CK (2002). Multiscale entropy analysis of complex physiologic time series. [Primary reference](https://doi.org/10.1103/PhysRevLett.89.068102).

## Normalized permutation entropy

**Definition:** Delayed ordinal patterns with stable sorting for ties; Shannon entropy divided by log(order factorial).

**Limitations and material differences:** Ties are assigned by temporal index, not discarded or jittered; result depends on recipe order and delay.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_permutation_entropy`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

- Bandt C, Pompe B (2002). Permutation entropy: a natural complexity measure for time series. [Primary reference](https://doi.org/10.1103/PhysRevLett.88.174102).

## Binary parsing complexity screen

**Definition:** Binary parsing count c normalized by c*log2(n)/n.

**Limitations and material differences:** Lempel-Ziv lineage only. Equivalence of this parser to a reference implementation has not been certified; do not claim independent authorship from its header.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_lz76_complexity`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

- Lempel A, Ziv J (1976). On the complexity of finite sequences. [Primary reference](https://doi.org/10.1109/TIT.1976.1055501).

## Normalized spectral entropy

**Definition:** Welch PSD over 1 Hz to min(45 Hz, Nyquist); normalized positive-bin probabilities; entropy/log(number of bins).

**Limitations and material differences:** A PRAYCG operational bandwidth-limited entropy measure, dependent on sampling and frequency resolution.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_spectral_entropy`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

- Welch PD (1967). The use of the fast Fourier transform for the estimation of power spectra. [Primary reference](https://doi.org/10.1109/TAU.1967.1161901).

## Run-local polarity-invariant topographic clustering

**Definition:** GFP-peak centered maps; unit-norm topographies; absolute-correlation assignment and principal-eigenvector centers; seeded restarts with GFP-squared weighted explained variance.

**Limitations and material differences:** Update centers are unweighted within each cluster although restart selection is GFP-weighted. No canonical A-D labels, cross-run alignment or temporal smoothing; states sorted by coverage.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_microstate_fit`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

- Pascual-Marqui RD, Michel CM, Lehmann D (1995). Segmentation of brain electrical activity into microstates: model estimation and validation. [Primary reference](https://doi.org/10.1109/10.391164).

## Train-fold CSP and ridge discriminant decoding

**Definition:** Trace-normalized uncentered trial.T@trial matrices averaged within class, generalized eigenproblem C0 v=lambda(C0+C1)v, extreme eigenvectors; log normalized projected variance.

**Limitations and material differences:** Uncentered covariance differs when means are nonzero. CSP fitted in training folds; trial-level cross-validation does not establish subject/session generalization.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_csp_features`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

- Ramoser H, Mueller-Gerking J, Pfurtscheller G (2000). Optimal spatial filtering of single trial EEG during imagined hand movement. [Primary reference](https://doi.org/10.1109/86.895946).

## PRAYCG ridge linear discriminant

**Definition:** Pooled within-class covariance with trace-scaled ridge, pseudoinverse and equal-prior linear discriminant scores.

**Limitations and material differences:** Custom implementation, not a claim that scikit-learn LDA ran. Frozen regularization and split design matter.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `_ridge_lda_predict`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

PRAYCG operational definition; no external exact-estimator equivalence asserted.

## Sensor-time split-half representational distances

**Definition:** Flatten sensor-time features; even/odd condition mean differences; mean product weighted by inverse diagonal-shrunk residual variance. Optional Spearman upper-triangle model comparison with condition-label permutations.

**Limitations and material differences:** Noise precision is estimated using all trials, not independent training data. Do not label this fully unbiased crossnobis. Negative distances are retained; sensor-level representations are not localized brain mechanisms.

**Source:** `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`; functions: `run_sensor_rsa`

**Reviewed source SHA-256:** `a306c0621ac110dd7f82ace5ea55cae058bbdce8e4e5fc14c6b003048344e2c5`

**References:**

- Kriegeskorte N, Mur M, Bandettini P (2008). Representational similarity analysis: connecting the branches of systems neuroscience. [Primary reference](https://doi.org/10.3389/neuro.06.004.2008).

## Verification boundary

Synthetic spot checks verify constant-amplitude PAC, ordered-sequence permutation entropy, sample-entropy pair counting against a separate brute-force calculation, and BH adjustment. They do not validate every estimator, clinical meaning or inference assumption. Bibliographic lineage does not establish source-code provenance.
