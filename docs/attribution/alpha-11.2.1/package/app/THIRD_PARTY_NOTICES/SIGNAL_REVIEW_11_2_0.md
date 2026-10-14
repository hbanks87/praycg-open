# Signal Review: software, methods and preserved notices

Public Alpha 11.2.0 / AUL Alpha 1.1.0 · Attribution addendum revision 1 · 13 October 2026

This addendum covers the first-cycle signal, heartbeat, respiration and line-noise review tools. It supplements the historical [master attribution review](../CITATIONS_AND_ATTRIBUTION.md); it is not a new clearance audit of every Workbench component.

## What the release ships

The release ships PRAYCG integration code, pinned installation requirements, method records and the six preserved upstream notice files listed below. It does **not** ship the NeuroKit2, PyWavelets or mne-denoise implementation packages, wheels or native libraries. The Core installer obtains those packages and their dependencies from upstream package distributions. Existing recordings and historical analysis outputs are not rewritten.

| Distribution installed during setup | Exact pin | Role | Applicable collected notices |
| --- | --- | --- | --- |
| NeuroKit2 | 0.2.13 | ECG detector comparison, time-domain HRV reference and respiration reference pipeline | MIT license and AUTHORS.rst |
| PyWavelets | 1.9.0 | NeuroKit2 runtime dependency; not a claim that wavelet analysis ran | Main MIT license plus bundled NumPy and SciPy notices; package metadata reports MIT AND BSD-3-Clause |
| mne-denoise | 0.0.3 | SpectrumInterpolation and fixed-selection ZapLine comparison candidates | BSD-3-Clause license |

These are independently licensed upstream components, not Hoyt Banks MIT code. Their copyright, notice-retention and applicable non-endorsement terms remain intact. Bibliographic references do not replace those terms. The copied notice texts were byte-checked against the exact installed distribution metadata used in testing.

This focused inventory does not enumerate every installed transitive package, wheel-internal binary or historical copy/paste relationship. It does not authorize redistribution of other artifacts. Setup records and the run's observed environment remain necessary to establish what was actually installed and used.

## Methods and limits

- **Signal review:** PRAYCG reports supported samples, exclusions, gaps and descriptive quality measures. Its operational thresholds are review aids, not validated physiological or clinical cutoffs.
- **Heartbeat and HRV:** NeuroKit2's `neurokit` and `pantompkins1985` ECG routes provide detector comparisons. Candidate artifact corrections are retained for review, not silently adopted. Time-domain interval summaries preserve accepted original adjacency; interval variability is not automatically certified normal-to-normal HRV. The PRAYCG ledger and window handling are separately identified implementation choices. NeuroKit2 software reference: Makowski et al. (2021), [DOI](https://doi.org/10.3758/s13428-020-01516-y). Detector reference: Pan and Tompkins (1985), [DOI](https://doi.org/10.1109/TBME.1985.325532). See the [official ECG API](https://neuropsychology.github.io/NeuroKit/functions/ecg.html).
- **Respiration:** A PRAYCG bandpass/Hilbert trace expresses relative respiration timing and amplitude, not calibrated volume. A separate NeuroKit2 reference calls `rsp_process(method="khodadad2018", method_rvt="harrison2021")`. The method names identify the actual configured routes; they do not establish equivalence of a belt to airflow measurements. See the [official respiration API](https://neuropsychology.github.io/NeuroKit/functions/rsp.html).
- **Respiration-related cardiac coupling:** PRAYCG fits accepted RR intervals to an intercept plus sine and cosine of measured respiration phase within supported same-clock windows. The reported harmonic semiamplitude is an exploratory association. It is not NeuroKit RSA, an independent estimate of vagal tone or a causal effect.
- **Existing processing comparison:** The comparison uses the shipped Standard v0.1 or Athena v1.2 recipe's filtering and reference choices, records which was used and retains the original trace. It is a transform preview, not a replay of every governed derivative eligibility or epoching step. An unknown processing route does not receive an invented preset.
- **SpectrumInterpolation:** The real mne-denoise 0.0.3 implementation is called with recorded line frequency, harmonics, band half-width and neighbour width. Reference: Leske and Dalal (2019), [DOI](https://doi.org/10.1016/j.neuroimage.2019.01.026); [official implementation API](https://mne.tools/mne-denoise/stable/generated/mne_denoise.spectrum_interpolation.SpectrumInterpolation.html).
- **Fixed-selection ZapLine:** The real mne-denoise 0.0.3 implementation uses a recorded fixed component count with adaptive selection disabled. It is not represented as ZapLine-plus. Reference: de Cheveigné (2020), [DOI](https://doi.org/10.1016/j.neuroimage.2019.116356); [official implementation API](https://mne.tools/mne-denoise/stable/generated/mne_denoise.zapline.ZapLine.html).
- **Residual spectra:** The comparison uses Welch spectra on common supported samples, with four-second Hann windows, 50% overlap and a shared frequency grid. Supported pieces are estimated separately and combined by their window counts, without joining across gaps. Reference: Welch (1967), [DOI](https://doi.org/10.1109/TAU.1967.1161901).

Original-minus-transformed traces show what changed, not proof that the removed component was an artifact. Harmonic attenuation, off-band change and known synthetic controls are reported together. A cleaner-looking trace or a lower residual line peak does not validate a neuroscience endpoint. The comparison never automatically adopts a candidate or modifies the original recording.

## Automatic credits and historical records

The active attribution registry adds versioned records for these four modules. Observed function entry, imported distribution versions and completion status are different facts. Function entry alone does not mean a method produced a valid result. For the inline SpectrumInterpolation and ZapLine candidates, declared citations are retained without falsely marking both methods executed; the comparison's per-candidate and per-segment status is the execution evidence. Full automatic method-level bibliography coverage is not asserted.

Existing attribution records, run identities, marker names and historical outputs remain unchanged. New attribution records describe new executions; they do not retroactively validate earlier studies.

## Preserved text ledger

| Notice path relative to this folder | SHA-256 |
| --- | --- |
| [core/neurokit2-0.2.13/neurokit2-0.2.13.dist-info/licenses/LICENSE](core/neurokit2-0.2.13/neurokit2-0.2.13.dist-info/licenses/LICENSE) | `89a0c90cb8331319e1baea34b004fd6121247e89d132c3fcd01c86353aac8733` |
| [core/neurokit2-0.2.13/neurokit2-0.2.13.dist-info/licenses/AUTHORS.rst](core/neurokit2-0.2.13/neurokit2-0.2.13.dist-info/licenses/AUTHORS.rst) | `3e314a0baadd077a82c834c6d5c6c92eab681ec5d33c74917168af55dce85820` |
| [core/PyWavelets-1.9.0/pywavelets-1.9.0.dist-info/licenses/LICENSE](core/PyWavelets-1.9.0/pywavelets-1.9.0.dist-info/licenses/LICENSE) | `c11ed9dd380510d277ca9e57d3820f680c4c0c58bfd3ff5c18272bea1cdd6779` |
| [core/PyWavelets-1.9.0/pywavelets-1.9.0.dist-info/licenses/licenses_bundled/LICENSE_numpy.txt](core/PyWavelets-1.9.0/pywavelets-1.9.0.dist-info/licenses/licenses_bundled/LICENSE_numpy.txt) | `2b3e076071410ffafe86fa9ddaff63f5ae3c50056f7802f13a87386c6921f526` |
| [core/PyWavelets-1.9.0/pywavelets-1.9.0.dist-info/licenses/licenses_bundled/LICENSE_scipy.txt](core/PyWavelets-1.9.0/pywavelets-1.9.0.dist-info/licenses/licenses_bundled/LICENSE_scipy.txt) | `0bc9049fda0257f1aa8128e3e13c431af7267e25ba93562baeb4b545a8fc02bc` |
| [core/mne-denoise-0.0.3/mne_denoise-0.0.3.dist-info/licenses/LICENSE](core/mne-denoise-0.0.3/mne_denoise-0.0.3.dist-info/licenses/LICENSE) | `4bc26bbf85dd083e877c4c4d12746afd0fde984bb5f599c3333bba60d6bf2237` |

