# PRAYCG software attribution and method-reference review

This historical review is retained as supporting evidence. The current public reference is [PRAYCG — Master Citations and Attribution](../CITATIONS_AND_ATTRIBUTION.md).

Review date: 2026-09-20. Inspected baseline: PRAYCG Control Center 1.0.0-alpha.10.0.3. Current guidance carried forward for Alpha 10.2.1.

This bounded review was performed against Alpha 10.0.3 and is retained as attribution guidance in Alpha 10.2.1. Links and line numbers describe the inspected baseline unless a later section says otherwise. Carrying the guidance forward is not a claim that a repository-wide provenance audit, dependency inventory, source-similarity review or legal clearance was subsequently completed. Installed applications, recordings and historical results were not changed for the review.

## Conclusion

Yes: analysis and Live Monitor should preserve appropriate software and method attribution, not just protocol citations. However, an imported library, copied source, an independently implemented mathematical method, and a repository merely reviewed for ideas are different relationships. They must not be represented as interchangeable.

Academic citations do not replace license notices or permission. A citation also does not imply that its authors reviewed, validated, sponsored or endorsed PRAYCG. Conversely, listing every previously suggested GitHub repository as software used would misdescribe the actual implementation.

## Verified implementation relationships

Paths below refer to the inspected Alpha 10.0.3 source, not the live installation.

| Component | Actual relationship observed | Evidence |
|---|---|---|
| Passive Live Monitor | Imports the MNE-LSL low-level inlet API; NumPy performs bounded display diagnostics. It does not use MNE-RT's high-level pipeline. | Installed-release source: `tools/Live_Monitor_v1_0/praycg_live_monitor_v1_0.py`, line 119. |
| XDF replay | Imports pyxdf, then uses PRAYCG replay transport and display logic. This is not MNE-LSL PlayerLSL replay. | Installed-release source: `tools/Live_Monitor_v1_0/praycg_xdf_replay_v1_0.py`, line 386. |
| EEG analysis worker | Direct numerical dependencies are NumPy and SciPy; pyxdf loads XDF. Included analysis families are not evidence that similarly named third-party packages were imported. | Installed-release source: `tools/EEG_Analysis_Modules_v0_1/praycg_eeg_analysis_modules_v0_1.py`, lines 24 and 349. |
| Master Comprehensive Suite | NumPy/SciPy computations and pyxdf input are present. These dependencies deserve software records; PRAYCG-specific endpoints additionally need their own precise method/provenance records. | Installed-release source: `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_master_comprehensive_suite_v1_6_0.py`, line 53. |
| BIDS export | Directly imports MNE-Python, MNE-BIDS, pyxdf and NumPy. MNE-Python creates the RawArray; MNE-BIDS writes BrainVision output. | Installed-release source: `tools/BIDS_Exporter_v0_1/praycg_bids_exporter_v0_1.py`, line 134. |
| Acquisition/LSL | pylsl is directly imported by multiple bridges, supervisors and protocol runners. It is distinct from the MNE-LSL binding used by Live Monitor. | Installed-release source: `tools/Acquisition/Polar_H10_to_LSL/polar_to_lsl.py`, line 34. |
| TorchEEG sandbox | Validates local dataset-manifest readiness and checks installed TorchEEG version metadata. It does not train or run a TorchEEG model. Do not claim a TorchEEG-generated analysis result. | Installed-release sources: `tools/TorchEEG_Research_Sandbox_v0_1/README.md` and `tools/TorchEEG_Research_Sandbox_v0_1/praycg_torcheeg_research_sandbox_v0_1.py`, line 117. |
| MNE-RT and previously suggested repositories | MNE-RT is explicitly documented as considered, not vendored/enabled. Scoped searches found no imports of EEGrunt, eegtools, mne-rsa, osl-ephys or the other suggested analysis repositories in the reviewed worker paths. This is not proof against unattributed copied fragments. | Installed-release source: `tools/Live_Monitor_v1_0/README.md`, line 25. |

The installed-release file `tools/Live_Monitor_v1_0/requirements.txt` pins NumPy 2.2.6, MNE 1.10.2, MNE-LSL 1.13.2 and pyxdf 1.17.0. These are declared installation requirements, not evidence that these exact versions ran in every user's session. Core requirements permit version ranges. Capture actual installed versions and relevant wheel/native-library identities for each environment and run.

## Verified upstream records for the next citation registry

These records were checked against primary project sources. Except the linked MNE 1.10.2 license, license pages below describe the upstream branch inspected on the review date; exact deployed release/license verification remains required.

| Suggested record ID | Upstream license evidence | Citation record and applicability |
|---|---|---|
| `software.mne_lsl` | [BSD-3-Clause license](https://github.com/mne-tools/mne-lsl/blob/main/LICENSE) | Scheltienne, Mathieu; Larson, Eric; Desvachez, Arnaud; Lee, Kyuhwa (2025). *MNE-LSL: Real-time framework integrated with MNE-Python for online neuroscience research through LSL-compatible devices.* JOSS 10(111), 8088. [DOI 10.21105/joss.08088](https://doi.org/10.21105/joss.08088). The [project's citation instructions](https://mne.tools/mne-lsl/stable/index.html) request this paper. Applies to live observation using its API, not as a claim that all PRAYCG replay/analysis code comes from MNE-LSL. |
| `software.mne_python` | [MNE 1.10.2 BSD-3-Clause license](https://raw.githubusercontent.com/mne-tools/mne-python/v1.10.2/LICENSE.txt) | Gramfort, Alexandre; Luessi, Martin; Larson, Eric; Engemann, Denis A.; Strohmeier, Daniel; Brodbeck, Christian; Goj, Roman; Jas, Mainak; Brooks, Teon; Parkkonen, Lauri; Hämäläinen, Matti S. (2013). *MEG and EEG data analysis with MNE-Python.* Frontiers in Neuroscience 7, 267. [DOI 10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267). Follow [MNE citation guidance](https://mne.tools/stable/documentation/cite.html); do not automatically claim use of inverse imaging or every MNE method merely because MNE is installed. |
| `software.pylsl` and `software.liblsl` | [pylsl MIT license](https://github.com/labstreaminglayer/pylsl/blob/main/LICENSE); inspect the separate [liblsl license](https://github.com/sccn/liblsl/blob/main/LICENSE) for the actual native library shipped/loaded. | The [LSL project's current citation](https://github.com/sccn/labstreaminglayer#cite-lsl) is Kothe, Christian; Shirazi, Seyed Yahya; Stenner, Tristan; Medine, David; Boulay, Chadwick; Grivich, Matthew I.; Artoni, Fiorenzo; Mullen, Tim; Delorme, Arnaud; Makeig, Scott (2025). *The Lab Streaming Layer for Synchronized Multimodal Recording.* Imaging Neuroscience 3, IMAG.a.136. [DOI 10.1162/IMAG.a.136](https://doi.org/10.1162/IMAG.a.136). Record wrapper and native-library versions separately. |
| `software.pyxdf` | [BSD-2-Clause license](https://github.com/xdf-modules/pyxdf/blob/main/LICENSE), with copyright notices naming Intheon, Chad Boulay, Tristan Stenner and Clemens Brunner. | Use a version-specific software reference to the [pyxdf project](https://github.com/xdf-modules/pyxdf) and its verified release. No preferred standalone publication was verified in this bounded review; do not invent one or conflate copyright holders with a complete scholarly author list. |
| `software.numpy` | [BSD-3-Clause project license](https://github.com/numpy/numpy/blob/main/LICENSE.txt) | Harris, Charles R., et al. (2020). *Array programming with NumPy.* Nature 585, 357–362. [DOI 10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2). Full author list and BibTeX are provided by [NumPy](https://numpy.org/citing-numpy/). Relevant to the numerical analysis and Live Monitor diagnostics. |
| `software.scipy` | [BSD-3-Clause project license](https://github.com/scipy/scipy/blob/main/LICENSE.txt) | Virtanen, Pauli, et al. (2020). *SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python.* Nature Methods 17, 261–272. [DOI 10.1038/s41592-019-0686-2](https://doi.org/10.1038/s41592-019-0686-2). [SciPy guidance](https://scipy.org/citing-scipy/) also recommends relevant original algorithm papers; a library citation is not a substitute for method-specific references. |
| `software.mne_bids` | [BSD-3-Clause license](https://github.com/mne-tools/mne-bids/blob/main/LICENSE) | Appelhoff, Stefan, et al. (2019). *MNE-BIDS: Organizing electrophysiological data into the BIDS format and facilitating their analysis.* JOSS 4, 1896. [DOI 10.21105/joss.01896](https://doi.org/10.21105/joss.01896). The [project's citation guidance](https://mne.tools/mne-bids/stable/index.html#citing-mne-bids) provides authors and additionally requests the appropriate modality-specific BIDS paper. Applies when this exporter is actually used. |

MNE-RT belongs in a separate `reviewed_not_integrated` record, not in a run's executed-software list. Its [README](https://github.com/mne-rt-org/mne-rt) requests the Shabestari et al. 2025 paper *Advances on Real Time M/EEG Neural Feature Extraction* if used. The same README currently says MIT while its actual [LICENSE file](https://github.com/mne-rt-org/mne-rt/blob/main/LICENSE) says BSD-3-Clause. Record that discrepancy and resolve the exact version's terms before any future integration; do not silently choose the more convenient label. No MNE-RT implementation change is proposed here.

## Gaps and prudent next work

1. **Separate notices from citations.** Preserve original copyright/license notices for copied or redistributed third-party code and binaries. BSD and MIT have their own retention conditions; the BSD-3-Clause records above also restrict endorsement uses. Include exact applicable texts in the distribution when required. A bibliography alone is insufficient.
2. **Do not broadly relabel dependencies.** PRAYCG's installed-release root `LICENSE.md` mixed-license notice cannot grant rights over upstream software. Clarify PRAYCG-owned code versus upstream components rather than treating all dependencies as Hoyt Banks MIT code.
3. **Inventory actual artifacts.** Distinguish packages installed from upstream during setup from code, wheels and native libraries shipped inside an archive. Inventory transitive components and their notices too; NumPy/SciPy wheels may contain separately licensed numerical libraries. This review did not enumerate installed environments, wheel contents or every dependency.
4. **Audit source provenance.** No repository-wide source-similarity or historical copy/paste audit was performed. An absence of an import or copyright header does not establish independent authorship. Inspect identified copied/adapted files against their exact upstream commit and retain their notices. Do not assert comprehensive clearance based on this report.
5. **Add method references per analysis.** The reviewed EEG worker/README does not yet provide a complete method bibliography. Verify the actual formulas and estimators for PSD, aperiodic regression, ERP/time-frequency, connectivity/PAC, entropy/complexity, microstates, CSP/decoding and RSA before attaching original method citations. Do not cite a famous method if the implementation differs materially; record the difference and PRAYCG-specific operational definition.
6. **Emit relevant credits automatically.** Each module should expose method records and actual software dependencies; each run should preserve observed versions. Aggregate only the methods/modules actually executed into a deduplicated report/bundle bibliography. Keep skipped/planned modules distinguishable from executed modules. A visible Methods and Credits panel can explain this without cluttering primary controls.
7. **Preserve reproducibility.** Citation/display-name changes should not silently alter old run identities, marker namespaces or historical outputs. Introduce versioned attribution records and explicit migration behavior. Adding attribution does not retroactively validate an experiment.

This is a bounded technical attribution review, not legal advice, an exhaustive license-compliance audit, a plagiarism determination or legal clearance. Protocol, stimulus, data, questionnaire, software, logo and name rights must be reviewed separately where applicable.
# Alpha 10.2.0 acquisition additions

The current source review and pinned references are in
`config/hardware_upstream_evidence_alpha_10_2_1.json` and
`docs/HARDWARE_ROUTES_ALPHA_10_2_1.md`. New PRAYCG connector implementation is
original code under the package license. BrainFlow, pylsl, NumPy and Bleak are
separately installed dependencies with their own licenses; dependency inclusion
does not transfer ownership or validate device timing.

No code from the linked programmatix Crown recorder, Cerelog LSL scripts,
OpenMuse, Pupil relay, hynchl GazePoint publisher or OpenViBE drivers is copied
into this release. External publisher profiles record source/version assumptions
and do not redistribute those applications. Polar PMD and GazePoint API documents
are cited as protocol references for independently authored implementations;
the Polar mobile SDK and its custom license are not bundled.
