# Research bibliography and software credits

**Supplement reviewed 13 October 2026 for the proposed Public Alpha 11.2.1 update.**

The [Public Alpha 11.2.2 supplement](../../CITATIONS_AND_ATTRIBUTION.md#public-alpha-1122-release-supplement) carries these references forward where the actual code uses them and identifies the new workflow/rating-credit changes. This page preserves its 11.2.1 source-review scope; it is not a second independent source audit.

This index connects PRAYCG's current integration code to upstream software and scientific methods. It supplements the [master attribution record](../../CITATIONS_AND_ATTRIBUTION.md), [historical reviewed estimators](../../docs/attribution/ANALYSIS_METHODS.md) and bibliographies retained within original research documents. It does not rewrite those originals or establish that every listed method ran in a study.

[Research entrance](../README.md) · [Concept definitions](../concepts/README.md) · [Implementation map](../algorithms/README.md) · [Exact notices and review evidence](../../docs/attribution/alpha-11.2.1/README.md)

## Cite the work actually used

A study should identify its PRAYCG release and protocol revision, actual software versions, selected algorithms and parameters, and the outputs that support its conclusions. Cite both an upstream implementation and its method paper where appropriate. An installed dependency, a candidate transform, a failed attempt and an adopted analysis are different facts. Retain applicable licenses as well as scholarly citations.

The code paths below are relative to `app/` inside the inspected Public Alpha 11.2.1 archive. Exact identities and selected source hashes are preserved in the [attribution source manifest](../../docs/attribution/alpha-11.2.1/SOURCE_MANIFEST.json). These code observations establish available routes; a study's own receipts establish execution.

## New software and method references

| Component or method | Relationship to the inspected Workbench | References |
| --- | --- | --- |
| NeuroKit2 0.2.13 | `tools/Signal_Review_v1_0/physiology.py` directly calls ECG, HRV and respiration functions | S1 plus applicable M1–M4 |
| PyWavelets 1.9.0 | Pinned installation dependency supporting NeuroKit2; no separate PRAYCG wavelet method is inferred | S2; main and bundled licenses retained |
| mne-denoise 0.0.3 | `tools/Signal_Review_v1_0/denoising.py` calls the actual upstream comparison implementations | S3 and M5/M6 |
| Pan–Tompkins detector | NeuroKit2 `ecg_clean` and `ecg_peaks` with `method="pantompkins1985"`, alongside the `neurokit` detector | S1, M1; implementation differs from an independent reproduction of the original hardware/software |
| Beat-correction candidate | NeuroKit2 `signal_fixpeaks(method="Kubios", iterative=True)`; candidate output retained without automatic adoption | S1, M2; does not imply a Kubios binary is distributed or used |
| Respiration reference pipeline | NeuroKit2 `rsp_process(method="khodadad2018", method_rvt="harrison2021")` | S1, M3, M4; current PRAYCG output retains traces/features but does not retain `RSP_RVT` as an endpoint |
| Spectrum interpolation | Upstream `SpectrumInterpolation`, applied separately within supported continuous pieces | S3, M5 |
| Fixed-selection ZapLine | Upstream `ZapLine` with recorded fixed component count and adaptive selection disabled | S3, M6; this route is not ZapLine-plus |
| Residual spectra | Four-second Hann Welch spectra, 50% overlap, common frequency grid and supported-piece pooling | M7 plus the actual NumPy/SciPy versions |

PRAYCG's own accepted-interval adjacency, support/gap rules, relative respiration trace and phase/RR regression require their versioned implementation description as well. They are not automatically NeuroKit RSA, a calibrated respiratory-volume measurement, normal-to-normal HRV or a validated neuroscience endpoint. NeuroKit's documentation also identifies differences between its `khodadad2018` implementation and the original paper. Keep the configured implementation and original scientific lineage visible together.

### Software

**S1 — NeuroKit2.** Makowski, D., Pham, T., Lau, Z. J., Brammer, J. C., Lespinasse, F., Pham, H., Schölzel, C., & Chen, S. A. (2021). *NeuroKit2: A Python toolbox for neurophysiological signal processing.* Behavior Research Methods, 53(4), 1689–1696. [DOI](https://doi.org/10.3758/s13428-020-01516-y) · [Official citation instructions](https://neuropsychology.github.io/NeuroKit/cite_us.html). Record the actual installed version alongside the paper; the inspected requirement is 0.2.13.

**S2 — PyWavelets.** Lee, G. R., et al. (2019). *PyWavelets: A Python package for wavelet analysis.* Journal of Open Source Software, 4(36), 1237. [DOI](https://doi.org/10.21105/joss.01237) · [Official citation instructions and contributor list](https://pywavelets.readthedocs.io/en/latest/#citing). The inspected requirement is 1.9.0. Installing it for NeuroKit2 does not establish that a specific wavelet analysis contributed to a reported result.

**S3 — mne-denoise.** Credit the mne-denoise contributors, including the copyright holders Sina Esmaeili and Hamza Abdelhedi named in the preserved notice. Cite *mne-denoise* [Computer software], version 0.0.3 for this inspected integration, its [official repository](https://github.com/mne-tools/mne-denoise), and the applicable original method paper below. The software attribution does not transfer authorship of SpectrumInterpolation or ZapLine to PRAYCG.

Authentication infrastructure is recorded separately: the package declares `PyJWT[crypto]>=2.8,<3`. [PyJWT](https://pyjwt.readthedocs.io/en/stable/) and its cryptographic dependencies require their actual installed-version and notice records, rather than a neuroscience method citation. See the [dated attribution review](../../docs/attribution/alpha-11.2.1/README.md).

### Methods

**M1 — ECG detection.** Pan, J., & Tompkins, W. J. (1985). *A Real-Time QRS Detection Algorithm.* IEEE Transactions on Biomedical Engineering, BME-32(3), 230–236. [DOI](https://doi.org/10.1109/TBME.1985.325532) · [NeuroKit ECG implementation documentation](https://neuropsychology.github.io/NeuroKit/functions/ecg.html).

**M2 — Beat correction.** Lipponen, J. A., & Tarvainen, M. P. (2019). *A robust algorithm for heart rate variability time series artefact correction using novel beat classification.* Journal of Medical Engineering & Technology, 43(3), 173–181. [DOI](https://doi.org/10.1080/03091902.2019.1640306) · [NeuroKit correction implementation](https://neuropsychology.github.io/NeuroKit/functions/signal.html#signal-fixpeaks).

**M3 — Respiration detection.** Khodadad, D., Nordebo, S., Müller, B., Waldmann, A. D., Yerworth, R., Becher, T., Frerichs, I., Sophocleous, L., van Kaam, A., Miedema, M., Seifnaraghi, N., & Bayford, R. H. (2018). *Optimized breath detection algorithm in electrical impedance tomography.* Physiological Measurement, 39(9), 094001. [DOI](https://doi.org/10.1088/1361-6579/aad7e6) · [Author manuscript and metadata](https://discovery.ucl.ac.uk/id/eprint/10054486/). Its original measurement setting is not interchangeable with every respiration signal accepted by PRAYCG.

**M4 — Configured RVT submethod.** Harrison, S. J., Bianchi, S., Heinzle, J., Stephan, K. E., Iglesias, S., & Kasper, L. (2021). *A Hilbert-based method for processing respiratory timeseries.* NeuroImage, 230, 117787. [DOI](https://doi.org/10.1016/j.neuroimage.2021.117787) · [NeuroKit respiration API](https://neuropsychology.github.io/NeuroKit/functions/rsp.html). This identifies a method configured inside the invoked upstream pipeline; the current PRAYCG output does not expose its `RSP_RVT` column as a reported endpoint.

**M5 — Spectrum interpolation.** Leske, S., & Dalal, S. S. (2019). *Reducing power line noise in EEG and MEG data via spectrum interpolation.* NeuroImage, 189, 763–776. [DOI](https://doi.org/10.1016/j.neuroimage.2019.01.026) · [mne-denoise implementation](https://mne.tools/mne-denoise/stable/generated/mne_denoise.spectrum_interpolation.SpectrumInterpolation.html).

**M6 — ZapLine.** de Cheveigné, A. (2020). *ZapLine: A simple and effective method to remove power line artifacts.* NeuroImage, 207, 116356. [DOI](https://doi.org/10.1016/j.neuroimage.2019.116356) · [mne-denoise implementation](https://mne.tools/mne-denoise/stable/generated/mne_denoise.zapline.ZapLine.html).

**M7 — Welch spectra.** Welch, P. D. (1967). *The use of fast Fourier transform for the estimation of power spectra: A method based on time averaging over short, modified periodograms.* IEEE Transactions on Audio and Electroacoustics, 15(2), 70–73. [DOI](https://doi.org/10.1109/TAU.1967.1161901) · [SciPy method reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html). This reference is retained in the package's Signal Review addendum; actual windowing, support and pooling choices are PRAYCG implementation records.

## EEGLAB and external analysis

**E1 — EEGLAB.** Delorme, A., & Makeig, S. (2004). *EEGLAB: an open source toolbox for analysis of single-trial EEG dynamics including independent component analysis.* Journal of Neuroscience Methods, 134(1), 9–21. [DOI](https://doi.org/10.1016/j.jneumeth.2003.10.009) · [Official EEGLAB citation guidance](https://eeglab.org/others/EEGLAB_References.html).

EEGLAB is recorded here as relevant external software. The inspected package has no identified bundled EEGLAB implementation or direct EEGLAB execution route. A LabRecorder README mention of an EEGLAB XDF importer and historical MNE optional I/O metadata are interoperability references, not evidence of use. No PRAYCG ASR, clean_rawdata or ICLabel integration was identified. Do not attach their citations as executed PRAYCG methods solely because those projects are related to EEG processing or an installed library offers them.

If a study independently uses EEGLAB or a plugin, record the exact software/plugin versions, actual operations, selected parameters and resulting outputs. Follow EEGLAB's official references and each plugin's own method and license requirements. EEGLAB's citation does not cover all independent plugins, and a citation is not a software license.

## Existing sources and project-specific concepts

| Research area | Preserved source records |
| --- | --- |
| MNE-Python, MNE-LSL, NumPy/SciPy, LSL, pyxdf, BrainFlow, PsychoPy, LabRecorder and acquisition tools | [Master software and hardware attribution](../../CITATIONS_AND_ATTRIBUTION.md#software-acknowledgments-and-references); keep the version actually used |
| Reviewed EEG estimators and their implementation differences | [Historical reviewed methods](../../docs/attribution/ANALYSIS_METHODS.md); this review does not silently refresh old source hashes |
| Adapted scientific protocols | [Protocol bibliography](../../CITATIONS_AND_ATTRIBUTION.md#scientific-protocol-bibliography) and [complete protocol-to-source index](../../CITATIONS_AND_ATTRIBUTION.md#complete-protocol-to-source-index); source lists retain their original review scope |
| MRED, NIP, NUPI, CAI/SID and related operational definitions | [Concept guides](../concepts/README.md), their linked original versioned definitions and [implementation map](../algorithms/README.md); cite PRAYCG's definition as well as constituent upstream methods |
| Opto-PING and research ladders | [Opto-PING source and rung records](../optoping/README.md), [ladder index](../ladders/README.md) and [reproducibility programs](../reproducibility/README.md); preserved reports retain their own bibliographies and evidence limits |
| Stimulus editions and demonstration media | [Original master catalog](../../examples/stimulus-masters/README.md) and [Bridge demo](../../examples/bridge-demo/README.md); scientific references do not replace media credits or redistribution terms |

This bibliography identifies contributions and source relationships. It does not establish scientific novelty, priority, validation, or complete historical code provenance. The [current attribution review](../../docs/attribution/alpha-11.2.1/README.md#coverage-and-remaining-gaps) distinguishes automatic-credit coverage from references that still require study-specific selection.
