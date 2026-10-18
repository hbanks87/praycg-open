# Public Alpha 11.4.1 attribution correction

Public Alpha 11.4.1 repairs the relative-hemoglobin citation metadata used by Optical Signal Review. The earlier entry omitted required citation fields. Receipt validation could consequently reject attribution and suppress the affected automatic method/software credits. The corrected metadata restores those credits for new affected executions without changing optical calculations or silently rewriting historical receipts. The method `optical_verified_relative_hemoglobin` now identifies `delpy1988_optical_pathlength` and `mne_fnirs_processing_tutorial` as separate references.

## Exact release evidence

The [source manifest](SOURCE_MANIFEST.json) identifies selected files copied from the release archive. The [corrected attribution registry](package/app/config/attribution_registry_v1.json), [package citation document](package/app/CITATIONS_AND_ATTRIBUTION.md) and [current attribution addendum](package/app/docs/ATTRIBUTION_ALPHA_11_4_1.md) preserve package content. The [release guide](../../../workbench/docs/releases/alpha-11.4.1/README.md) and [build report](../../../workbench/docs/releases/alpha-11.4.1/package/BUILD_REPORT.md) describe the fix and current verification scope. Earlier test counts and hardware receipts are not fresh evidence for this patch.

Package-internal links inside copied originals may refer to files available only in the complete application ZIP. Use the [repository bibliography](../../../research/bibliography/README.md), [master attribution](../../../CITATIONS_AND_ATTRIBUTION.md) and [notice index](../../../THIRD_PARTY_NOTICES/README.md) for repository navigation.

## Optical credit and method boundary

The corrected reference credits all six authors: Delpy, D. T., Cope, M., van der Zee, P., Arridge, S., Wray, S., & Wyatt, J. (1988). *Estimation of optical pathlength through tissue from direct time of flight measurement.* Physics in Medicine and Biology, 33(12), 1433–1442. [DOI](https://doi.org/10.1088/0031-9155/33/12/008) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/3237772/).

MNE-Python's [fNIRS tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/70_fnirs_processing.html) is a methodological reference. It does not establish that PRAYCG's native conversion calls MNE's optical-density or Beer–Lambert functions. Preserve actual instrument/profile identity, wavelengths, source-detector/pathlength assumptions, coefficients, baseline and numerical-library versions. The bundled Athena profile remains raw-only; this credit correction does not enable unsupported hemoglobin estimates.

Software import, method entry and a successfully estimated endpoint remain different facts. An unavailable endpoint or failed/skipped execution does not become completed evidence because it has a citation. Prior receipts may be supplemented only with an explicitly labeled correction; their original software versions and execution records must remain intact.

## Current upstream integration and notices

The current addendum also identifies retained NeuroKit2, PyWavelets and mne-denoise references and the later Signal Review routes. These include additional NeuroKit physiology comparisons; MNE EEGLAB-format I/O; optional ASRpy, MNE-ICALabel/ICLabel and Pycrostates; and native adaptation of pinned SPAR-EEG pass logic. Cite the particular operation and implementation used, retaining original method authors alongside software authors. No MATLAB EEGLAB runtime is bundled.

Applicable upstream license and author notices remain separate from bibliography metadata. The release preserves them; PRAYCG's license and an academic citation do not replace their terms. Original research documents, earlier attribution reviews, media permissions and historical results retain their own identity and scope. This focused correction is not a comprehensive source-origin audit, complete transitive-license inventory or scientific validation.
