# PRAYCG — Master Citations and Attribution

**PRAYCG Workbench / Control Center Alpha 10.2.1**  
**Document revision:** 2.0 · **Updated:** 22 September 2026  
**PRAYCG development and protocol adaptation:** Hoyt Banks

PRAYCG brings together original project software, scientific methods, public research paradigms and independently maintained software. This page credits those contributions and gives researchers a single reference for citing the parts of PRAYCG they use.

This is the canonical public attribution page for Alpha 10.2.1. It consolidates software acknowledgments, acquisition references, protocol citations, the complete packaged-protocol index and the project's attribution policy. Source author lists and historical protocol identities are retained. A project's appearance here does not imply its authors' affiliation with, endorsement of, or review of PRAYCG.

Revision 2 adds an artifact-level inventory, preserved upstream notices, commit-pinned source comparisons and reviewed estimator definitions. The accompanying **Attribution Update v1** implements new-run credits in the development source. It is a separately identified source update, not a claim that these features were already present in the original Alpha 10.2.1 download. That original archive remains unchanged.

## Contents

- [How to cite PRAYCG and a study](#how-to-cite-praycg-and-a-study)
- [Authorship, copyright and licenses](#authorship-copyright-and-licenses)
- [Software acknowledgments and references](#software-acknowledgments-and-references)
- [Declared installation dependencies](#declared-installation-dependencies)
- [Hardware and acquisition credits](#hardware-and-acquisition-credits)
- [Analysis methods and citation coverage](#analysis-methods-and-citation-coverage)
- [Artifact inventory and preserved notices](#artifact-inventory-and-preserved-notices)
- [Automatic Methods and Credits](#automatic-methods-and-credits)
- [Scientific protocol bibliography](#scientific-protocol-bibliography)
- [Complete protocol-to-source index](#complete-protocol-to-source-index)
- [Data, stimuli and media credits](#data-stimuli-and-media-credits)
- [Attribution maintenance and remaining work](#attribution-maintenance-and-remaining-work)
- [Document provenance](#document-provenance)

## How to cite PRAYCG and a study

Suggested software citation:

> Banks, Hoyt. (2026). *PRAYCG Workbench / Control Center* (Alpha 10.2.1) [Computer software].

Add the repository release URL or permanent archive identifier for the exact copy used when publishing this citation. No PRAYCG DOI is asserted here. Preserve the release checksum in the study's provenance records.

A study should also cite its selected protocol's original sources, the relevant software references below and the methods actually used. Give the protocol identifier and revision, software versions, analysis recipe and any changes to the source paradigm. Cite a dataset when its data are used; adapting a task does not establish that its source dataset was analyzed. A planned or skipped module should not be reported as an executed analysis.

For a PRAYCG-defined protocol, use:

> Banks, Hoyt. (2026). *[Protocol title]* ([protocol identifier], version [version]) [PRAYCG protocol definition]. In *PRAYCG Workbench / Control Center*, [release actually used].

The bracketed fields are filled from the study's locked definition. For a third-party adaptation, retain the original authors' citation alongside this PRAYCG implementation credit.

## Authorship, copyright and licenses

Hoyt Banks is credited for PRAYCG development and protocol adaptation. Original papers, datasets, software, stimuli and hardware remain credited to their own authors and rights holders. Scientific authorship of an individual study depends on contributions to that study.

The project mixed-license notice assigns MIT terms to original PRAYCG-owned code unless a file states otherwise, CC BY 4.0 to project documentation/templates/non-personal example metadata unless otherwise specified, and CC0 1.0 to the designated synthetic demo media. The root `LICENSE.md` and artifact-specific notices govern those grants. They do not relicense upstream components.

Software notices and scholarly references serve different purposes. Preserve applicable copyright statements, license texts, NOTICE files and modification notices for copied, adapted or redistributed third-party material. An MIT or BSD project citation does not replace notice retention. BSD-3-Clause also contains an endorsement restriction. Apply the exact terms of each artifact and version; this page is not a substitute for the required texts.

The companion [Third-party Notices index](THIRD_PARTY_NOTICES/README.md) links exact retained texts and their provenance. The [MIT](https://opensource.org/license/mit) and [BSD-3-Clause](https://opensource.org/license/bsd-3-clause) license pages explain the standard terms; the actual upstream texts, including their copyright holders, remain controlling. No dependency has been relabeled as Hoyt Banks MIT software.

This page documents known relationships and limitations. It does not certify a complete copyright, source-provenance or license-compliance audit.

## Software acknowledgments and references

The following relationships were identified in the packaged source and prior component reviews:

| PRAYCG function | Upstream contribution |
| --- | --- |
| Stream publishing and acquisition coordination | pylsl and its underlying liblsl implementation provide LSL interfaces. |
| Passive Live Monitor | MNE-LSL provides the low-level inlet API; NumPy supports display diagnostics. |
| XDF replay | pyxdf loads the recording; PRAYCG provides the replay transport and display logic. |
| EEG workers and Master Comprehensive Suite | NumPy/SciPy numerical routines and pyxdf input. Individual estimator choices remain PRAYCG implementation decisions. |
| BIDS export | MNE-Python, MNE-BIDS, pybv and supporting numerical/XDF packages, when that export route runs. |
| New managed acquisition routes | BrainFlow and/or Bleak with pylsl; see route-specific credits below. |
| Protocol presentation | Separately installed PsychoPy, when a PsychoPy runner is used. |
| XDF recording | Separately installed LabRecorder, operated by the user. |

### Core software references

The records below credit the relevant projects. License links identify upstream records reviewed for attribution; exact installed files and native dependencies still require their own notices and version inventory.

| Software record | Upstream license evidence | Citation record and applicability |
|---|---|---|
| MNE-LSL | [BSD-3-Clause license](https://github.com/mne-tools/mne-lsl/blob/main/LICENSE) | Scheltienne, Mathieu; Larson, Eric; Desvachez, Arnaud; Lee, Kyuhwa (2025). *MNE-LSL: Real-time framework integrated with MNE-Python for online neuroscience research through LSL-compatible devices.* JOSS 10(111), 8088. [DOI 10.21105/joss.08088](https://doi.org/10.21105/joss.08088). The [project's citation instructions](https://mne.tools/mne-lsl/stable/index.html) request this paper. Applies to live observation using its API, not as a claim that all PRAYCG replay/analysis code comes from MNE-LSL. |
| MNE-Python | [MNE 1.10.2 BSD-3-Clause license](https://raw.githubusercontent.com/mne-tools/mne-python/v1.10.2/LICENSE.txt) | Gramfort, Alexandre; Luessi, Martin; Larson, Eric; Engemann, Denis A.; Strohmeier, Daniel; Brodbeck, Christian; Goj, Roman; Jas, Mainak; Brooks, Teon; Parkkonen, Lauri; Hämäläinen, Matti S. (2013). *MEG and EEG data analysis with MNE-Python.* Frontiers in Neuroscience 7, 267. [DOI 10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267). Follow [MNE citation guidance](https://mne.tools/stable/documentation/cite.html); do not automatically claim use of inverse imaging or every MNE method merely because MNE is installed. |
| pylsl and liblsl | [pylsl MIT license](https://github.com/labstreaminglayer/pylsl/blob/main/LICENSE); inspect the separate [liblsl license](https://github.com/sccn/liblsl/blob/main/LICENSE) for the actual native library shipped/loaded. | The [LSL project's citation](https://github.com/sccn/labstreaminglayer#cite-lsl) is Kothe, Christian; Shirazi, Seyed Yahya; Stenner, Tristan; Medine, David; Boulay, Chadwick; Grivich, Matthew I.; Artoni, Fiorenzo; Mullen, Tim; Delorme, Arnaud; Makeig, Scott (2025). *The Lab Streaming Layer for Synchronized Multimodal Recording.* Imaging Neuroscience 3, IMAG.a.136. [DOI 10.1162/IMAG.a.136](https://doi.org/10.1162/IMAG.a.136). Record wrapper and native-library versions separately. |
| pyxdf | [BSD-2-Clause license](https://github.com/xdf-modules/pyxdf/blob/main/LICENSE), with copyright notices naming Intheon, Chad Boulay, Tristan Stenner and Clemens Brunner. | pyxdf contributors. *pyxdf* [Computer software]. Cite the [project](https://github.com/xdf-modules/pyxdf) with the version used to load the recording. The recorded attribution review did not identify a preferred standalone paper. |
| NumPy | [BSD-3-Clause project license](https://github.com/numpy/numpy/blob/main/LICENSE.txt) | Harris, Charles R., et al. (2020). *Array programming with NumPy.* Nature 585, 357–362. [DOI 10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2). Full author list and BibTeX are provided by [NumPy](https://numpy.org/citing-numpy/). Relevant to the numerical analysis and Live Monitor diagnostics. |
| SciPy | [BSD-3-Clause project license](https://github.com/scipy/scipy/blob/main/LICENSE.txt) | Virtanen, Pauli, et al. (2020). *SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python.* Nature Methods 17, 261–272. [DOI 10.1038/s41592-019-0686-2](https://doi.org/10.1038/s41592-019-0686-2). [SciPy guidance](https://scipy.org/citing-scipy/) also recommends relevant original algorithm papers; a library citation is not a substitute for method-specific references. |
| MNE-BIDS | [BSD-3-Clause license](https://github.com/mne-tools/mne-bids/blob/main/LICENSE) | Appelhoff, Stefan, et al. (2019). *MNE-BIDS: Organizing electrophysiological data into the BIDS format and facilitating their analysis.* JOSS 4, 1896. [DOI 10.21105/joss.01896](https://doi.org/10.21105/joss.01896). The [project's citation guidance](https://mne.tools/mne-bids/stable/index.html#citing-mne-bids) provides authors and additionally requests the appropriate modality-specific BIDS paper. Applies when this exporter is actually used. |

**PsychoPy.** Peirce, J. W.; Gray, J. R.; Simpson, S.; MacAskill, M. R.; Höchenberger, R.; Sogo, H.; Kastman, E.; Lindeløv, J. (2019). *PsychoPy2: Experiments in behavior made easy.* Behavior Research Methods, 51, 195–203. [DOI: 10.3758/s13428-018-01193-y](https://doi.org/10.3758/s13428-018-01193-y). Cite when used for protocol presentation and record the installed version. See the [project's citation guidance](https://devdocs.psychopy.org/about/index.html).

**LabRecorder.** Lab Streaming Layer / LabRecorder contributors. *LabRecorder* [Computer software]. Record the application version or commit used to record the XDF, alongside the LSL reference above. [Official repository](https://github.com/labstreaminglayer/App-LabRecorder).

**BrainFlow.** BrainFlow contributors. *BrainFlow*, version 5.23.0 for the isolated Alpha 10.2.1 connector environment [Computer software]. [Official documentation](https://brainflow.readthedocs.io/en/stable/) and [reviewed source revision](https://github.com/brainflow-dev/brainflow/tree/7994b54b4ee23898456d96446dc7e51ebfa18840). Core permits a version range, so the isolated connector pin must not be assigned to every run automatically.

**Python and Tcl/Tk.** Credit the Python Software Foundation, Python contributors and Tcl/Tk contributors for the runtime and desktop interface foundation. Preserve the notices supplied with the actual distributions. [Python](https://www.python.org/) · [Tcl/Tk](https://www.tcl-lang.org/).

### Reviewed projects and optional readiness tools

MNE-RT was considered during Live Monitor development; the recorded implementation uses MNE-LSL instead. MNE-RT must not be listed as executed software in a PRAYCG run merely because it was reviewed. The earlier review also recorded inconsistent license labels between its README and LICENSE; any future integration requires verification of its exact revision. [MNE-RT project](https://github.com/mne-rt-org/mne-rt).

The TorchEEG sandbox checks local readiness and installed package metadata. That activity does not establish model training, inference or a TorchEEG-derived result. [TorchEEG project](https://github.com/torcheeg/torcheeg).

EEGrunt, eegtools, mne-rsa, osl-ephys and other repositories suggested during development should be credited as dependencies or adapted source only when an actual relationship is documented. Their names are not evidence that their algorithms or code ran.

## Declared installation dependencies

The Core requirement file declares the following 29 packages. This is a direct-dependency inventory drawn from the Alpha 10.2.1 installer requirements, with descriptive roles. Inclusion indicates an installation requirement; it does not establish execution in every study or a complete inventory of transitive/native components. Package links provide upstream distribution records, whose exact version metadata and license files must be retained when applicable.

| Upstream package | Declared Core requirement | Role |
| --- | --- | --- |
| [setuptools](https://pypi.org/project/setuptools/) | `setuptools>=80.9,<82` | Packaging support |
| [pyserial](https://pypi.org/project/pyserial/) | `pyserial>=3.5,<4` | Serial-device access |
| [numpy](https://pypi.org/project/numpy/) | `numpy>=1.26,<3` | Numerical arrays |
| [scipy](https://pypi.org/project/scipy/) | `scipy>=1.11,<2` | Signal processing and statistics |
| [pandas](https://pypi.org/project/pandas/) | `pandas>=2.1,<3` | Tabular data |
| [tabulate](https://pypi.org/project/tabulate/) | `tabulate>=0.9,<1` | Text tables |
| [matplotlib](https://pypi.org/project/matplotlib/) | `matplotlib>=3.8,<4` | Plots |
| [opencv-python](https://pypi.org/project/opencv-python/) | `opencv-python>=4.8,<5` | Video and image processing |
| [moviepy](https://pypi.org/project/moviepy/) | `moviepy==1.0.3` | Media preparation |
| [imageio](https://pypi.org/project/imageio/) | `imageio>=2.31,<3` | Image and video input/output |
| [imageio-ffmpeg](https://pypi.org/project/imageio-ffmpeg/) | `imageio-ffmpeg>=0.4.9,<1` | FFmpeg integration |
| [decorator](https://pypi.org/project/decorator/) | `decorator>=4.4,<6` | Function-decorator support |
| [proglog](https://pypi.org/project/proglog/) | `proglog>=0.1,<1` | Progress logging |
| [requests](https://pypi.org/project/requests/) | `requests>=2.31,<3` | HTTP access where invoked |
| [tqdm](https://pypi.org/project/tqdm/) | `tqdm>=4.66,<5` | Progress display |
| [pillow](https://pypi.org/project/pillow/) | `pillow>=10,<13` | Image processing |
| [pylsl](https://pypi.org/project/pylsl/) | `pylsl>=1.16,<2` | LSL Python binding |
| [pyxdf](https://pypi.org/project/pyxdf/) | `pyxdf>=1.16,<2` | XDF loading |
| [mne](https://pypi.org/project/mne/) | `mne>=1.6,<2` | MNE-Python data structures and tools |
| [mne-bids](https://pypi.org/project/mne-bids/) | `mne-bids>=0.16,<1` | BIDS export |
| [pybv](https://pypi.org/project/pybv/) | `pybv>=0.7,<1` | BrainVision export |
| [pyyaml](https://pypi.org/project/pyyaml/) | `pyyaml>=6,<7` | YAML parsing |
| [brainflow](https://pypi.org/project/brainflow/) | `brainflow>=5.12,<6` | Device acquisition API |
| [bleak](https://pypi.org/project/bleak/) | `bleak>=0.21,<2` | Bluetooth Low Energy access |
| [godirect](https://pypi.org/project/godirect/) | `godirect>=1.2,<2` | Vernier Go Direct access |
| [scenedetect](https://pypi.org/project/scenedetect/) | `scenedetect[opencv]>=0.6,<1` | Scene detection |
| [openpyxl](https://pypi.org/project/openpyxl/) | `openpyxl>=3.1,<4` | Excel workbook support |
| [scikit-learn](https://pypi.org/project/scikit-learn/) | `scikit-learn>=1.3,<2` | Machine-learning support |
| [pytest](https://pypi.org/project/pytest/) | `pytest>=8,<9` | Software testing |

The Live Monitor environment additionally pins `numpy==2.2.6`, `mne==1.10.2`, `mne-lsl==1.13.2` and `pyxdf==1.17.0`. The isolated hardware environment pins `brainflow==5.23.0`, `numpy==2.2.6`, `pylsl==1.17.6` and `bleak==1.1.1`. Installer tooling also uses pip and wheel.

The public software archive's packaging declaration excludes Python, dependency wheels, PsychoPy, LabRecorder and separately managed publishers. Installing those packages can introduce additional native libraries and license obligations. NumPy/SciPy numerical libraries, FFmpeg/codecs, Qt or other application dependencies must be inventoried in the actual environment or redistributed artifact. A requirements list is not a complete software bill of materials.

## Hardware and acquisition credits

The table records the project's acquisition-source review of 21 September 2026. Commit links preserve the inspected source; they do not certify physical device performance. The integration includes five managed and eight external experimental routes. Cerelog 16 remains withheld. Existing OpenBCI/ALS, Polar RR and Vernier paths remain separate.

| Upstream project or specification | Relationship to PRAYCG | Recorded source and licensing boundary |
| --- | --- | --- |
| BrainFlow / BrainFlow contributors | Installed dependency; PRAYCG connector uses BrainFlow 5.23.0. Crown OSC, Athena presets and synthetic testing use the shared interface. | [7994b54b4ee2](https://github.com/brainflow-dev/brainflow/tree/7994b54b4ee23898456d96446dc7e51ebfa18840). Upstream BrainFlow licensing applies to separately downloaded wheels and included dependencies; no upstream binaries redistributed in PRAYCG ZIP. |
| Polar Electro / Polar BLE SDK documentation | Protocol documentation for PRAYCG's H10 ECG implementation. Polar mobile SDK source and binaries are not included in the release declaration. | [a693e9e944c9](https://github.com/polarofficial/polar-ble-sdk/tree/a693e9e944c9bc925addbdd8cf07fb9b28748bf7). Polar mobile SDK custom license; SDK code and binaries not bundled. |
| Cerelog ESP-EEG contributors | Hardware/firmware reference; Cerelog 16 remains withheld. The source record does not establish a supported 16-channel acquisition path. | [af1a56e0127e](https://github.com/Cerelog-ESP-EEG/ESP-EEG/tree/af1a56e0127e71606afdc7e7ddf0ca831715e09c). Composite firmware MIT-intent text has standard-license placeholder; hardware CC-BY-NC-SA-4.0; PCB layouts excluded. |
| Cerelog LSL compatibility project contributors | Reviewed for compatibility only; the recorded route is 8-channel and is not promoted to Cerelog 16. | [e70fcf9a7fa1](https://github.com/Cerelog-ESP-EEG/Lab-Stream-Layer-LSL-Compatability/tree/e70fcf9a7fa16a7b7847b51116680b17dd34079b). No license grant was found in the inspected source tree. |
| Cerelog custom BrainFlow fork contributors | Reviewed custom fork; no fork code or binary is declared bundled. Its X8 route does not establish Cerelog 16 support. | [932b3944bfe6](https://github.com/shakimiansky/Shared_brainflow-cerelog/tree/932b3944bfe6c0f4e29a46b4a34afdeba39edd85). MIT core plus additional SimpleBLE incorporation restrictions. |
| programmatix / Neurosity-Crown-LSL | Reviewed reference only. The inspected program is an LSL consumer/exporter; the PRAYCG Crown publisher instead uses BrainFlow OSC. | [521bd20003da](https://github.com/programmatix/Neurosity-Crown-LSL/tree/521bd20003dad2adae3d31fc548c28c58693a2c9). No license grant was found in the inspected source tree. |
| Dominique Makowski and OpenMuse contributors | External publisher: EEG, motion, optics and battery profiles. Operator installs and starts OpenMuse separately; recorded source version is 0.1.8. | [a9be25218832](https://github.com/DominiqueMakowski/OpenMuse/tree/a9be252188321e269537eabf609bc207be293f8c). pyproject MIT classifier only; no LICENSE grant file found. |
| Lab Streaming Layer / App-PupilLabs contributors | External Pupil Core Capture relay, version 2.3; separate gaze and pupillometry contracts. Relay code is not declared bundled. | [37dedd64c6a7](https://github.com/labstreaminglayer/App-PupilLabs/tree/37dedd64c6a7691f9d8d3900f46d9b89f8e35e7e). LGPL-3.0. |
| hynchl / lsl-gp3 | Reviewed reference only. PRAYCG's connector is recorded as a separately authored, selected-field GazePoint client. | [9bd790d98fc0](https://github.com/hynchl/lsl-gp3/tree/9bd790d98fc0d9e6256a58cd4d326bd5ebc926d9). CC0-1.0. |
| Pupil Labs / Neon Companion | External Companion application and vendor LSL documentation; record the actual app version and observed stream fields per session. | [Source](https://docs.pupil-labs.com/neon/data-collection/lab-streaming-layer/). External vendor app; no redistribution. |
| GazePoint / API specification | Version 2.0 protocol specification used by the PRAYCG GP3 and GP3 HD client. | [Version 2.0](https://www.gazept.com/dl/Gazepoint_API_v2.0.pdf). Vendor protocol specification; no document copied. |
| OpenViBE contributors | External LSL template only. Current canonical source access was blocked during the recorded review; no OpenViBE driver is declared bundled. | [Source](https://gitlab.inria.fr/openvibe/sdk). License verification remains unresolved because the canonical source could not be accessed. |

Additional existing-route credits: [OpenBCI](https://docs.openbci.com/) for device documentation; Polar Electro for H10 interfaces; Vernier for Go Direct devices and the [godirect package](https://pypi.org/project/godirect/). Device manufacturers retain their trademarks and product documentation rights. An ALS sensor profile does not itself identify a third-party software author; retain source-specific notices for any actual holder design, firmware or copied bridge component used.

External publishers are installed and started separately. OpenMuse, Pupil Core/Neon and OpenViBE credits describe those optional relationships. The hardware source record describes the new PRAYCG connector implementations as independently authored and lists the reviewed reference repositories as unbundled. This is the recorded implementation provenance, not a repository-wide source-similarity finding.

## Analysis methods and citation coverage

A library citation credits software; it does not describe every estimator, parameter or inference. Revision 2 reviews the EEG worker's PSD, aperiodic, ERP/time-frequency, connectivity/PAC, complexity, microstate, CSP/decoding and sensor-RSA implementations. The examples below are supplemented by fourteen source-hashed records in [Reviewed analysis methods](attribution/ANALYSIS_METHODS.md).

**Welch power spectral density.** The signal-quality, spectral and spectral-entropy code calls `scipy.signal.welch`. The methodological reference is P. D. Welch (1967), *The use of the fast Fourier transform for the estimation of power spectra: A method based on time averaging over short, modified periodograms*, IEEE Transactions on Audio and Electroacoustics, 15, 70–73, as listed in [SciPy's Welch documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html). A result must also preserve segment size, window, overlap, detrending, scaling, sampling rate and installed SciPy version.

**Aperiodic screening.** The PRAYCG worker applies `scipy.stats.theilslopes` to log10 power against log10 frequency after configured frequency exclusions, reports exponent as negative slope and retains the intercept and median absolute residual. References listed by [SciPy's Theil–Sen documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.theilslopes.html) include H. Theil (1950), *A rank-invariant method of linear and polynomial regression analysis I, II and III*, and P. K. Sen (1968), *Estimates of the regression coefficient based on Kendall's tau*, Journal of the American Statistical Association, 63, 1379–1389. This identifies the regression lineage. PRAYCG's screening procedure and frozen exclusions are its own operational definition; the implementation is not specparam/FOOOF and should not be cited as such.

The reviewed definitions distinguish scientific lineage from exact estimator equivalence. Connectivity uses band-averaged cross-spectra within epochs, non-debiased wPLI and a mirrored signed imaginary-coherency matrix; the latter is not the conventional antisymmetric matrix. Entropy tolerance is recalculated at each coarse scale. Microstate centers and restart selection use different weighting, labels remain run-local, and decoding is exploratory within-run. RSA estimates noise precision from all trials, so a fully unbiased crossnobis claim is not supported. These are implementation findings, not issues repaired by adding citations.

PRAYCG-specific endpoints such as CAI/SID, Micro Handoff and other exploratory suite constructs should cite the exact PRAYCG definition, formula, configuration and code version. No external validation paper or universal construct validity is asserted by this page.

### Packaged analysis-module index

This release's execution registry contains 23 modules. The index identifies their packaged implementation versions; it is not a record that they executed in any particular study. The companion attribution registry explicitly marks reviewed subsets and pending legacy-method coverage; a complete original-method bibliography is not asserted.

| Analysis module | Stable identifier | Packaged module version |
| --- | --- | --- |
| Run Integrity and Event-Timing QC v0.1 | `run_integrity_timing_qc_v0_1` | 0.1.0 |
| Atlas Meditation vs Active Thinking v0.1 | `atlas_meditation_vs_thinking_v0_1` | 0.1.0 |
| Master Comprehensive Suite v1.6.0 | `master_comprehensive_suite_v1_6_0` | 1.6.0 |
| Full Dependency-Aware Chained Analysis v1.6.1 | `full_chained_analysis_v1_6_1` | 1.6.1 |
| HOC-R ShotOrder Structural-Control Audit v1.6.0 | `hocr_shotorder_v1_6_0` | 1.6.0 |
| Confound-Expanded Analysis Modules v1.5.7 | `confound_expansion_v1_5_7` | 1.5.7 |
| CAI / SID Exploratory v0.2 | `cai_sid_exploratory_v0_2` | 0.2.0 |
| Continuous Autonomic / RespDualPath v1.0 | `continuous_autonomic_respdualpath_v1_0` | 1.0.0 |
| Micro Handoff v0.1 | `micro_handoff_v0_1` | 0.1.0 |
| Cue-Locked Gamma Forensics v0.1 | `cue_locked_gamma_forensics_v0_1` | 0.1.0 |
| MasterSync Visualizer v1.4.0 | `master_sync_visualizer_v1_4_0` | 1.4.0 |
| Offline Master Interpreter v1.6.0 | `offline_master_interpreter_v1_6_0` | 1.6.0 |
| Universal EEG Signal Quality and Line-Noise Audit v0.1 | `eeg_signal_quality_v0_1` | 0.1.0 |
| Governed EEG Preprocessing Derivative v0.1 | `eeg_preprocessing_derivative_v0_1` | 0.1.0 |
| EEG Spectral and Aperiodic Screening v0.1 | `eeg_spectral_aperiodic_v0_1` | 0.1.0 |
| Event-Related Potential and Time-Frequency v0.1 | `eeg_erp_time_frequency_v0_1` | 0.1.0 |
| Sensor Connectivity and Phase-Amplitude Coupling v0.1 | `eeg_connectivity_pac_v0_1` | 0.1.0 |
| EEG Complexity and Entropy v0.1 | `eeg_complexity_v0_1` | 0.1.0 |
| EEG Run-Local Microstates v0.1 | `eeg_microstates_v0_1` | 0.1.0 |
| Motor-Imagery CSP/LDA Decoding v0.1 | `eeg_motor_imagery_v0_1` | 0.1.0 |
| Sensor-Level Representational Similarity v0.1 | `eeg_sensor_rsa_v0_1` | 0.1.0 |
| TorchEEG Isolated Research-Sandbox Readiness v0.1 | `torcheeg_research_sandbox_v0_1` | 0.1.0 |
| Atlas Research Protocol Analysis v1.0 | `atlas_research_analysis_v1_0` | 1.0.0 |

## Scientific protocol bibliography

The 16 records below cover 23 externally sourced packaged protocols. They are consolidated from the project's primary-source bibliography reviewed on 20 September 2026. This document preserves those source records and their stated limits; it does not claim a fresh review of all underlying studies. The other 44 packaged definitions have PRAYCG local-definition attribution and retained internal lineage where available.

Article, preprint and dataset references remain distinct. Dataset author order follows the dataset record where it differs from the paper. A missing dataset publication year is shown as undated rather than inferred. The P-numbers are document reference labels.

<a id="p01"></a>

### P01 — Multiple event segmentation mechanisms in the human brain

Tan T Nguyen; Joset A Etzel; Matthew A Bezdek; Jeffrey M Zacks. (2026). *Multiple event segmentation mechanisms in the human brain*. Article. [DOI: 10.7554/eLife.107955.3](https://doi.org/10.7554/eLife.107955.3). [Source record](https://elifesciences.org/articles/107955).

Version of Record, 7 July 2026. The passive PRAYCG task adapts the source task; the active boundary-marking runner adds a PRAYCG response task and is not the original fMRI acquisition or exact normative segmentation procedure. Paper-author order is preserved separately from dataset-author order.

<a id="p02"></a>

### P02 — Testing neural mechanisms of event segmentation with fMRI

Matthew Bezdek; Jeffrey Zacks; Tan T. Nguyen; Joset Etzel. (undated dataset record). *Testing neural mechanisms of event segmentation with fMRI*. Dataset. [DOI: 10.18112/openneuro.ds005551.v1.0.4](https://doi.org/10.18112/openneuro.ds005551.v1.0.4). [Source record](https://openneuro.org/datasets/ds005551/versions/1.0.4).

Author spelling and order follow the dataset metadata. Dataset License field is CC0; this is not a blanket permission for source movies, other materials, trademark use or endorsement. Dataset year was not established in the inspected description. Existing OSF 3EMBR/v562e stimulus references remain a separate retained provenance link and were not freshly verified in the recorded review.

<a id="p03"></a>

### P03 — A large dataset of human EEG responses to short naturalistic videos for studying dynamic visual event processing

Alessandro T. Gifford; Pablo Oyarzo; Anne W. Zonneveld; Christina Sartzetaki; Iris I.A. Groen; Radoslaw M. Cichy. (2026). *A large dataset of human EEG responses to short naturalistic videos for studying dynamic visual event processing*. Preprint. [DOI: 10.48550/arXiv.2608.28768](https://doi.org/10.48550/arXiv.2608.28768). [Source record](https://arxiv.org/abs/2608.28768).

The recorded review inspected arXiv v2, 1 September 2026; a preprint, not described here as a peer-reviewed article. Dataset metadata explicitly requests this citation. Source-code repository is https://github.com/gifale95/EMD. PRAYCG is an adaptation and is not the source MATLAB/Psychtoolbox acquisition stack.

<a id="p04"></a>

### P04 — EEG Moments Dataset (EMD)

Alessandro T. Gifford; Pablo Oyarzo; Anne W. Zonneveld; Christina Sartzetaki; Iris I.A. Groen; Radoslaw M. Cichy. (2026). *EEG Moments Dataset (EMD)*. Dataset. [DOI: 10.18112/openneuro.ds008257.v1.0.1](https://doi.org/10.18112/openneuro.ds008257.v1.0.1). [Source record](https://openneuro.org/datasets/ds008257/versions/1.0.1).

Dataset metadata reports CC0. This is not blanket rights clearance for every underlying audiovisual clip, source code or lab branding. No original audiovisual clips are bundled in the PRAYCG adaptation.

<a id="p05"></a>

### P05 — ERP CORE: An open resource for human event-related potential research

Emily S. Kappenman; Jaclyn L. Farrens; Wendy Zhang; Andrew X. Stewart; Steven J. Luck. (2021). *ERP CORE: An open resource for human event-related potential research*. Article. [DOI: 10.1016/j.neuroimage.2020.117465](https://doi.org/10.1016/j.neuroimage.2020.117465). [Source record](https://doi.org/10.1016/j.neuroimage.2020.117465).

Journal year 2021; published online 21 October 2020. The official ERP CORE site states its resources are CC BY-SA 4.0 and requires credit and share-alike for shared adaptations of those resources. That obligation must be assessed separately from independently implementing a scientific method. Existing PRAYCG metadata asserts no upstream executable code or media is bundled; the recorded review does not independently establish that assertion. Original resources: https://doi.org/10.18115/D5JW4R.

<a id="p06"></a>

### P06 — Meditation vs thinking task

Arnaud Delorme; Claire Braboszcz. (undated dataset record). *Meditation vs thinking task*. Dataset. [DOI: 10.18112/openneuro.ds003969.v1.0.0](https://doi.org/10.18112/openneuro.ds003969.v1.0.0). [Source record](https://openneuro.org/datasets/ds003969/versions/1.0.0).

Names and order are dataset authors, not automatically the complete author list of the linked study. Source metadata reports CC0 and references https://doi.org/10.1371/journal.pone.0170647. Dataset year not established in inspected metadata.

<a id="p07"></a>

### P07 — EEG meditation study

Arnaud Delorme; Tracy Brandmeyer. (undated dataset record). *EEG meditation study*. Dataset. [DOI: 10.18112/openneuro.ds001787.v1.1.1](https://doi.org/10.18112/openneuro.ds001787.v1.1.1). [Source record](https://openneuro.org/datasets/ds001787/versions/1.1.1).

Names and order follow dataset metadata. Source metadata reports CC0 and references PMID 27815577. Dataset year not established in inspected metadata.

<a id="p08"></a>

### P08 — The Effect of Buddhism Derived Loving Kindness Meditation on Modulating EEG: Long-term and Short-term Effect

SUN, Rui; Ven WONG, Goon Fui; GAO, Jungling. (undated dataset record). *The Effect of Buddhism Derived Loving Kindness Meditation on Modulating EEG: Long-term and Short-term Effect*. Dataset. [DOI: 10.18112/openneuro.ds003816.v1.0.1](https://doi.org/10.18112/openneuro.ds003816.v1.0.1). [Source record](https://openneuro.org/datasets/ds003816/versions/1.0.1).

Author names are preserved verbatim, including name order, capitalization and honorific; no unverified normalization or spelling correction. Source metadata reports CC0. Dataset year not established in inspected metadata.

<a id="p09"></a>

### P09 — A resource for assessing information processing in the developing brain using EEG and eye tracking

Nicolas Langer; Erica J. Ho; Lindsay M. Alexander; Helen Y. Xu; Renee K. Jozanovic; Simon Henin; Agustin Petroni; Samantha Cohen; Enitan T. Marcelle; Lucas C. Parra; Michael P. Milham; Simon P. Kelly. (2017). *A resource for assessing information processing in the developing brain using EEG and eye tracking*. Article. [DOI: 10.1038/sdata.2017.40](https://doi.org/10.1038/sdata.2017.40). [Source record](https://www.nature.com/articles/sdata201740).

Original data descriptor, distinct from the later 2026 NEMAR repackaging. NEMAR nm000153 lists CC-BY-NC-SA-3.0 and non-commercial use only; do not transfer that license to PRAYCG code or assume imported MIPDB data are unrestricted. The three-minute PRAYCG rest duration is an operational default, not an authenticated source constant.

<a id="p10"></a>

### P10 — Narratives: fMRI data for evaluating models of naturalistic language comprehension

Samuel A. Nastase; Yun-Fei Liu; Hanna Hillman; Asieh Zadbood; Liat Hasenfratz; Neggin Keshavarzian; Janice Chen; Christopher J. Honey; Yaara Yeshurun; Mor Regev; Mai Nguyen; Claire H. C. Chang; Christopher Baldassano; Olga Lositsky; Erez Simony; Michael A. Chow; Yuan Chang Leong; Paula P. Brooks; Emily Micciche; Gina Choe; Ariel Goldstein; Tamara Vanderwal; Yaroslav O. Halchenko; Kenneth A. Norman; Uri Hasson. (2019). *Narratives: fMRI data for evaluating models of naturalistic language comprehension*. Dataset. [DOI: 10.18112/openneuro.ds002345.v1.1.4](https://doi.org/10.18112/openneuro.ds002345.v1.1.4). [Source record](https://openneuro.org/datasets/ds002345/versions/1.1.4).

Title/year follow the dataset's HowToAcknowledge citation; full author order retained. Dataset reports CC0. Audio/story permissions and any derivative rights must be checked independently; the PRAYCG package does not bundle those source recordings. Source code is https://github.com/snastase/narratives.

<a id="p11"></a>

### P11 — An open-access dataset of naturalistic viewing using simultaneous EEG-fMRI

Qawi K. Telesford; Eduardo Gonzalez-Moreira; Ting Xu; Yiwen Tian; Stanley J. Colcombe; Jessica Cloud; Brian E. Russ; Arnaud Falchier; Maximilian Nentwich; Jens Madsen; Lucas C. Parra; Charles E. Schroeder; Michael P. Milham; Alexandre R. Franco. (2023). *An open-access dataset of naturalistic viewing using simultaneous EEG-fMRI*. Article. [DOI: 10.1038/s41597-023-02458-8](https://doi.org/10.1038/s41597-023-02458-8). [Source record](https://www.nature.com/articles/s41597-023-02458-8).

Authors verified against the publisher's article PDF. PRAYCG uses its own timing shell and does not reproduce the source scanner, EyeLink, Psychtoolbox, MPlayer or hardware. Source code and video rights are separate and are not cleared by this reference.

<a id="p12"></a>

### P12 — Thinking out loud, an open-access EEG-based BCI dataset for inner speech recognition

Nicolás Nieto; Victoria Peterson; Hugo Leonardo Rufiner; Juan Esteban Kamienkowski; Ruben Spies. (2022). *Thinking out loud, an open-access EEG-based BCI dataset for inner speech recognition*. Article. [DOI: 10.1038/s41597-022-01147-2](https://doi.org/10.1038/s41597-022-01147-2). [Source record](https://www.nature.com/articles/s41597-022-01147-2).

Paper author names retained, including Nicolás. Dataset ds003626 and source code https://github.com/N-Nieto/Inner_Speech_Dataset have distinct artifact/version identities. The paper is CC BY 4.0; dataset metadata reports CC0; neither fact alone determines all source-code obligations.

<a id="p13"></a>

### P13 — EEG dataset and OpenBMI toolbox for three BCI paradigms: an investigation into BCI illiteracy

Min-Ho Lee; O-Yeon Kwon; Yong-Jeong Kim; Hong-Kyung Kim; Young-Eun Lee; John Williamson; Siamac Fazli; Seong-Whan Lee. (2019). *EEG dataset and OpenBMI toolbox for three BCI paradigms: an investigation into BCI illiteracy*. Article. [DOI: 10.1093/gigascience/giz002](https://doi.org/10.1093/gigascience/giz002). [Source record](https://doi.org/10.1093/gigascience/giz002).

Authors verified against the original article in PubMed Central. The article is CC BY 4.0, but source-code licensing must be checked independently. This record identifies the methodological source, not a claim that PRAYCG vendors OpenBMI.

<a id="p14"></a>

### P14 — EEG Motor Movement/Imagery Dataset

Gerwin Schalk. (2009). *EEG Motor Movement/Imagery Dataset*. Dataset. [DOI: 10.13026/C28G6P](https://doi.org/10.13026/C28G6P). [Source record](https://physionet.org/content/eegmmidb/1.0.0/).

Version 1.0.0. Dataset citation follows the official record; acknowledgements credit W. A. Sarnacki (collection), Aditya Joshi (compilation/documentation), D. J. McFarland (design) and J. R. Wolpaw (oversight), not collapsed into an invented paper author list. Official files are under Open Data Commons Attribution License v1.0. The page additionally requests the original BCI2000 paper and the PhysioNet platform citation when using the resource. PRAYCG adapts task structure rather than bundling the dataset.

<a id="p15"></a>

### P15 — A Computational Framework to Study Hierarchical Processing in Visual Narratives

Aditya Upadhyayula; Neil Cohn. (2025). *A Computational Framework to Study Hierarchical Processing in Visual Narratives*. Article. [DOI: 10.1111/cogs.70050](https://doi.org/10.1111/cogs.70050). [Source record](https://onlinelibrary.wiley.com/doi/10.1111/cogs.70050).

Publisher lists first publication 2 May 2025. OSF public materials: https://osf.io/s2h5x/. No Peanuts-derived source panels are bundled; source-publication access is not permission to redistribute those panels. The PRAYCG six-panel/five-gutter task is an adaptation, not an exact replication.

<a id="p16"></a>

### P16 — A Benchmark Dataset for SSVEP-Based Brain-Computer Interfaces

Yijun Wang; Xiaogang Chen; Xiaorong Gao; Shangkai Gao. (2017). *A Benchmark Dataset for SSVEP-Based Brain-Computer Interfaces*. Article. [DOI: 10.1109/TNSRE.2016.2627556](https://doi.org/10.1109/TNSRE.2016.2627556). [Source record](https://doi.org/10.1109/TNSRE.2016.2627556).

Journal date October 2017; online publication 10 November 2016. This replaces dependence on a downstream MOABB code link as the sole scientific citation, without claiming MOABB code was incorporated. Source dataset/code/stimulus rights are not established by this paper citation.


## Complete protocol-to-source index

All 67 packaged definitions are indexed below: 57 entries in the main protocol browser and 10 prospective counterbalance sequences. Public display names are taken from the current Alpha 10.2.1 files; stable identifiers are retained for traceability. Hoyt Banks is the PRAYCG development/adaptation byline for these entries. The external authors credited in P01–P16 retain authorship of their source works.

“Local definition” means a PRAYCG-defined operational protocol with no verified external article/dataset citation in the present registry. Retained D-number lineage identifies internal source documents, not independently published evidence. It does not establish that a protocol is scientifically novel or lacks relevant prior literature.

| Public protocol name | Stable protocol identifier | Original sources / local lineage |
| --- | --- | --- |
| Adaptive Choice Flexibility and Reversal Learning | `ATLAS_ADAPTIVE_CHOICE_FLEXIBILITY_REVERSAL` | PRAYCG local definition; retained D199, D200 |
| Adaptive Regulation Under Information Pressure | `ATLAS_ADAPTIVE_REGULATION_INFORMATION_PRESSURE` | PRAYCG local definition; retained D172, D178, D179 |
| Aesthetic Response and Memory | `ATLAS_AESTHETIC_RESPONSE_MEMORY` | PRAYCG local definition; retained D103, D114 |
| Agency Under Constraint | `ATLAS_AGENCY_UNDER_CONSTRAINT` | PRAYCG local definition; retained D120 |
| Analytic Load Dose–Response | `ATLAS_ANALYTIC_LOAD_DOSE_RESPONSE` | PRAYCG local definition; retained D226, D227 |
| Autonomic Response and Recovery Calibration | `ATLAS_API_A_CALIBRATION_RECOVERY` | PRAYCG local definition; retained D32, D33, D36, D159, Master Comprehensive Suite API_A_v1 |
| Caregiver–Child Interaction and Recovery | `ATLAS_BIOLOGICAL_ANCHOR_CHILD_SAFE` | PRAYCG local definition; retained D11, D12 |
| Cardiorespiratory Regulation and Task Performance | `ATLAS_CARDIORESPIRATORY_REGULATION_TASK_PERFORMANCE` | PRAYCG local definition; retained D156 |
| Cognitive State Stability and Recovery | `ATLAS_COGNITIVE_STATE_STABILITY_RECOVERY` | PRAYCG local definition; retained D137 |
| Social Feedback and Task Engagement | `ATLAS_CONFORMITY_FLOW_BOUNDARY_LAYER` | PRAYCG local definition; retained D61, D62, D63 |
| EEG Moments-Derived Repeated Audiovisual Clips - PRAYCG Adaptation | `ATLAS_EEG_MOMENTS_CLIPS_ADAPTATION` | [P03](#p03), [P04](#p04) |
| ERP CORE - Arrow Conflict and Error Monitoring - PRAYCG Adaptation | `ATLAS_ERP_CORE_FLANKER_LRP_ERN_ADAPTATION` | [P05](#p05) |
| ERP CORE - Sound Change (MMN) - PRAYCG Adaptation | `ATLAS_ERP_CORE_MMN_ADAPTATION` | [P05](#p05) |
| ERP CORE - Face/Car Recognition (N170) - PRAYCG Adaptation | `ATLAS_ERP_CORE_N170_ADAPTATION` | [P05](#p05) |
| ERP CORE - Left/Right Visual Attention (N2pc) - PRAYCG Adaptation | `ATLAS_ERP_CORE_N2PC_ADAPTATION` | [P05](#p05) |
| ERP CORE - Word Meaning Match (N400) - PRAYCG Adaptation | `ATLAS_ERP_CORE_N400_ADAPTATION` | [P05](#p05) |
| ERP CORE-Derived P3b Visual Oddball - PRAYCG Adaptation | `ATLAS_ERP_CORE_P3B_ADAPTATION` | [P05](#p05) |
| Caregiver–Child Play and Engagement | `ATLAS_FATHERS_DAY_PRESENCE` | PRAYCG local definition; retained D13, D14 |
| Subjective Experience and Physiology | `ATLAS_FIRST_PERSON_PRESENCE` | PRAYCG local definition; retained D28, D35, D36 |
| Multiscale Physiology and Behavior | `ATLAS_FRACTAL_EXISTENCE_MEASURED_SCALES` | PRAYCG local definition; retained D15, D16, D25, D26 |
| Gratitude and Paced Breathing | `ATLAS_GRATITUDE_CARDIO_AFFECTIVE_LITE` | PRAYCG local definition; retained D07, D08 |
| Gratitude, Rumination and Physiological Response | `ATLAS_GRATITUDE_NEUROCHEMICAL_TENSOR_PROXY` | PRAYCG local definition; retained D05, D06, D07, D08 |
| Inhibitory Control and Choice Architecture | `ATLAS_INHIBITORY_CONTROL_CHOICE_ARCHITECTURE` | PRAYCG local definition; retained D133 |
| Loving-Kindness - Self and Other - PRAYCG Adaptation | `ATLAS_LOVING_KINDNESS_SELF_OTHER_ADAPTATION` | [P08](#p08) |
| Meditation - Concentration Check-ins - PRAYCG Adaptation | `ATLAS_MEDITATION_THOUGHT_PROBE_ADAPTATION` | [P07](#p07) |
| Meditation - Breath Counting vs Active Thinking - PRAYCG Adaptation | `ATLAS_MEDITATION_VS_ACTIVE_THINKING_ADAPTATION` | [P06](#p06) |
| MIPDB-Derived Eyes-Closed Rest - PRAYCG Adaptation | `ATLAS_MIPDB_EYES_CLOSED_REST_ADAPTATION` | [P09](#p09) |
| NARR-Derived Coarse-Order Audio Story - PRAYCG Adaptation | `ATLAS_NARR_AUDIO_COARSE_SCRAMBLE_ADAPTATION` | [P10](#p10) |
| NARR-Derived Fine-Order Audio Story - PRAYCG Adaptation | `ATLAS_NARR_AUDIO_FINE_SCRAMBLE_ADAPTATION` | [P10](#p10) |
| NARR-Derived Intact Audio Story - PRAYCG Adaptation | `ATLAS_NARR_AUDIO_INTACT_ADAPTATION` | [P10](#p10) |
| NATVIEW-Derived Repeated Naturalistic Viewing - PRAYCG Adaptation | `ATLAS_NATVIEW_REPEATED_VIDEO_ADAPTATION` | [P11](#p11) |
| Inner Speech - Four Directions - PRAYCG Adaptation | `ATLAS_NIETO_INNER_SPEECH_DIRECTION_ADAPTATION` | [P12](#p12) |
| Inner Speech - Speech and Imagery Controls - PRAYCG Adaptation | `ATLAS_NIETO_INNER_SPEECH_TRIAD_CONTROL_ADAPTATION` | [P12](#p12) |
| Observedness and Task Performance | `ATLAS_OBSERVEDNESS_TASK_PERFORMANCE` | PRAYCG local definition; retained D154, D239, D240 |
| OpenBMI - Four-Target Visual Flicker - PRAYCG Adaptation | `ATLAS_OPENBMI_4_TARGET_SSVEP_ADAPTATION` | [P13](#p13) |
| Individual Task-Load and Recovery Calibration | `ATLAS_PERSONALIZED_TRANSITION_CALIBRATION` | PRAYCG local definition; retained D160 |
| PhysioNet EEGMMIDB-Derived Motor Execution and Imagery - PRAYCG Adaptation | `ATLAS_EEGMMIDB_MOTOR_ADAPTATION` | [P14](#p14) |
| Playful Cognitive Flexibility | `ATLAS_PLAYFUL_COGNITIVE_FLEXIBILITY` | PRAYCG local definition; retained D101 |
| Evidence Updating and Confidence | `ATLAS_PRAYCG_D_NEUTRAL_BELIEF_UPDATE` | PRAYCG local definition; retained D52, D53 |
| Shared Narrative Viewing and Interpersonal Physiological Synchrony | `ATLAS_PRAYCG_G_DYADIC_HYPERSCANNING` | PRAYCG local definition; retained D02, D198, D206 |
| Narrative Structure and Interpretation | `ATLAS_PRAYCG_G_MATURE_GRADIENT` | PRAYCG local definition; retained D01, D02, D198, D206, internal protocol integration register, PRAYCG Meta-Analysis Style Port v1.0 |
| Partner Support and Cognitive Task Performance | `ATLAS_PRAYCG_T_TRUST_OFFLOADING` | PRAYCG local definition; retained D50, D51 |
| Purpose, Positive Affect and Goal Persistence | `ATLAS_PURPOSE_POSITIVE_AFFECT_GOAL_PERSISTENCE` | PRAYCG local definition; retained D112 |
| Rhythmic Cues and Autonomic Response | `ATLAS_RHYTHMIC_AUTONOMIC_STABILIZATION` | PRAYCG local definition; retained D190, D191, D192, D194, D195 |
| Signal Structure × Processing Stance | `ATLAS_SIGNAL_STRUCTURE_PROCESSING_STANCE` | PRAYCG local definition; retained D223, D224 |
| Static-Image Semantic Meaning Gradient | `ATLAS_STATIC_IMAGE_SEMANTIC_MEANING_GRADIENT` | PRAYCG local definition; retained PR-AYC-G-IMG |
| Subjective Time Perception Under Attention and Load | `ATLAS_SUBJECTIVE_TIME_ATTENTION_LOAD` | PRAYCG local definition; retained D116 |
| SVNA-Derived Six-Panel Gutter Ranking - PRAYCG Adaptation | `ATLAS_SVNA_GUTTER_RANKING_ADAPTATION` | [P15](#p15) |
| Cognitive Load and Physiological Response | `ATLAS_THERMODYNAMIC_WEIGHT_THOUGHT` | PRAYCG local definition; retained D18, D19, D37 |
| Multimodal State and Recovery | `ATLAS_UNIFIED_PRESENCE_AVAILABILITY` | PRAYCG local definition; retained D09, D10, D28, D36 |
| Wang - 40-Target Visual Speller - PRAYCG Adaptation | `ATLAS_WANG_40_TARGET_JFPM_SSVEP_ADAPTATION` | [P16](#p16) |
| Zacks-Derived Silent Everyday-Event Boundary Marking - PRAYCG Adaptation | `ATLAS_ZACKS_EVENT_BOUNDARY_ADAPTATION` | [P01](#p01), [P02](#p02) |
| Zacks-Derived Silent Everyday-Event Viewing - Passive PRAYCG Adaptation | `ATLAS_ZACKS_EVENT_PASSIVE_ADAPTATION` | [P01](#p01), [P02](#p02) |
| Individual Resting-State Calibration | `ATLAS_ZERO_STATE_BASELINE_CALIBRATION` | PRAYCG local definition; retained D157, D158, D159 |
| PRAYCG3 - Original Three-Prong Protocol | `PRAYCG3` | PRAYCG local definition |
| PRAYCG4 - ShotOrder Four-Branch Protocol | `PRAYCG4` | PRAYCG local definition |
| Semantic Meaning Gradient - Three-State Protocol | `SMG` | PRAYCG local definition |
| PRAYCG3 prospective counterbalance sequence 01 | `PRAYCG3P_SEQ01` | PRAYCG local definition |
| PRAYCG3 prospective counterbalance sequence 02 | `PRAYCG3P_SEQ02` | PRAYCG local definition |
| PRAYCG3 prospective counterbalance sequence 03 | `PRAYCG3P_SEQ03` | PRAYCG local definition |
| PRAYCG3 prospective counterbalance sequence 04 | `PRAYCG3P_SEQ04` | PRAYCG local definition |
| PRAYCG3 prospective counterbalance sequence 05 | `PRAYCG3P_SEQ05` | PRAYCG local definition |
| PRAYCG3 prospective counterbalance sequence 06 | `PRAYCG3P_SEQ06` | PRAYCG local definition |
| PRAYCG4 prospective counterbalance sequence 01 | `PRAYCG4P_SEQ01` | PRAYCG local definition |
| PRAYCG4 prospective counterbalance sequence 02 | `PRAYCG4P_SEQ02` | PRAYCG local definition |
| PRAYCG4 prospective counterbalance sequence 03 | `PRAYCG4P_SEQ03` | PRAYCG local definition |
| PRAYCG4 prospective counterbalance sequence 04 | `PRAYCG4P_SEQ04` | PRAYCG local definition |

### Versioned local definitions

Each registry entry retains a historical source-definition citation, commonly tied to Alpha 10.0.3. Those historical release labels and hashes must remain attached to their original artifacts. They are not hashes of current Alpha 10.2.1 manifests.

For a published study, cite the current locked protocol version and file hash from that study alongside the intellectual sources above. The packaged files `protocol_scholarly_attribution_v1_0.json` and `protocol_verified_source_records_v1_0.json` under `config/` retain the detailed author, source, path and historical-hash records. A later metadata correction should be preserved as a separate revision; it must not rewrite an old run's identity, marker namespace, original output or evidence.

## Data, stimuli and media credits

Source papers, datasets, software and stimulus media may have different rights. Credits must follow the actual material used.

- EEG Moments, NATVIEW, Narratives, event-segmentation and visual-narrative adaptations identify scientific sources. Their citations do not grant blanket permission to distribute audiovisual clips, stories, comic panels or branding.
- ERP CORE's source resources carry the terms recorded in P05, including share-alike requirements where applicable. Distinguish use of those resources from implementation of a scientific method.
- The source records distinguish CC0 dataset metadata, CC BY articles, non-commercial dataset restrictions and Open Data Commons Attribution terms. Apply each to its own artifact, rather than to the entire PRAYCG project.
- The designated synthetic demo-media folder is declared CC0 1.0 in the project license. For a Sintel-based recipe, credit the Blender Foundation and retain the source's CC BY 3.0 requirements, as specified in the packaged mixed-license notice.
- User-provided stimuli, questionnaires and recordings require their own author, source, license/access and consent records. Their inclusion in a private bundle does not authorize public redistribution.

When using a source dataset, follow its complete acknowledgment instructions. P14, for example, records additional BCI2000 and PhysioNet references required by the EEG Motor Movement/Imagery Dataset's source page; cite those when the resource itself is used.

## Artifact inventory and preserved notices

The audit distinguishes three different things: files actually distributed in the original release, packages observed in selected local environments, and source notices retrieved to supplement incomplete installed metadata. These are not interchangeable.

| Evidence | Result and boundary |
| --- | --- |
| Original Alpha 10.2.1 ZIP | All 747 file entries were enumerated and SHA-256 hashed. No wheels, executables, DLLs, Python native extensions, shared libraries or nested archives were found by the listed suffix checks. This is an archive-content observation, not proof of independent source authorship. |
| Observed Python installations | 121 distribution installations were enumerated across the sampled core, monitor-validation and connector-validation environments. These include transitive packages and packages not necessarily used by PRAYCG. A user-site location was also checked. |
| Native components | 841 native file records were hashed across the sampled environments. They are installed artifacts, not files shipped inside the original PRAYCG ZIP. File hashing does not identify every embedded native dependency. |
| Installed notices | 217 notice files were copied byte-for-byte from installed package records, including numerical-library notices associated with NumPy/SciPy. Both LICENSE and LICENCE spellings were checked. |
| Supplemental notices | Missing installed texts were sought in exact-version upstream artifacts. MNE and PyWinRT release-source notices were additionally retrieved at immutable commits. Supplemental source notices are not evidence that a binary contains only that source's dependencies. |
| Source screening | A 420-code-file snapshot was hashed and screened for attribution/provenance markers. Exact-byte comparison with installed Python source found no matches. This narrow negative result does not establish independent authorship. |

Original release SHA-256: `9b1645741f63157e1a15a8c5d8b818e47f48b0f5a65bed67f636bf8412eb0f08`.

The [artifact inventory](attribution/ARTIFACT_INVENTORY.md), [machine-readable audit](attribution/artifact_audit.json), [upstream recovery records](attribution/upstream_notice_recovery.json) and [release-source notice records](attribution/repository_notice_recovery.json) provide versions, hashes and distinctions. The source screening snapshot preceded the final attribution tests and publication scripts; it is not a hash inventory of the final patch.

The environment inventory records observed installations, not a recommended lockfile or a reproduction of every supported setup. It does not include a complete PsychoPy installation, separately installed LabRecorder, every user's environment, all wheel variants, firmware or operating-system components. Packages downloaded during a future installation must retain their own notices. Any future release that embeds wheels or binaries requires a new artifact inventory and notice review.

### Bounded source-provenance comparisons

Two entropy-code candidates were compared with AntroPy's functions at commit `dfbe688744021eb79c4745ceb02a1efc7cd3fbd8`: PRAYCG's binary parsing complexity and permutation entropy. The comparison records local and upstream file hashes, normalized-function similarity and the retained exact upstream license. Neither function was an exact normalized match.

See the [comparison ledger](attribution/source_comparisons.json) and [commit-pinned upstream source](https://github.com/raphaelvallat/antropy/blob/dfbe688744021eb79c4745ceb02a1efc7cd3fbd8/src/antropy/entropy.py). This is a comparison reference, **not a discovered historical origin commit**. Similarity neither proves copying nor clears provenance; the notice is retained conservatively without asserting AntroPy endorsed or authored PRAYCG.

A comprehensive historical copy/paste audit remains unresolved. No complete source history establishing the origin of every implementation was available for this review. In particular, missing imports, headers or exact matches are not evidence of original ownership.

## Automatic Methods and Credits

Attribution Update v1 adds a versioned registry covering all 23 analysis module identifiers. Each record exposes the entry point, static import candidates and method-review status. Fourteen method records describe the reviewed EEG implementations, with source hashes, function names, scientific lineage and material differences. [Reviewed analysis methods](attribution/ANALYSIS_METHODS.md) contains the readable definitions and references; [the registry](attribution/attribution_registry_v1.json) is the machine-readable counterpart.

New managed Analysis Forge launches run an observer in the selected worker interpreter. It records:

- The module and receipt identity, registry revision, source hashes and observer hash.
- Reviewed functions actually entered, rather than citing every planned method.
- Installed distribution versions corresponding to packages imported in that worker.
- Exit status and whether separate descendant processes were launched.

The execution receipt incorporates the credits record under its existing content hash. The results index exposes a **Methods and Credits** section, and individual module summaries link to it. The session report retains attempt states and deduplicates references from observed methods. Failed attempts remain labeled failed; merely planned modules do not contribute executed-method citations. Historical receipts without records say that credits were not recorded.

The report is written as JSON and HTML inside the session's analysis results. Research Bundle export preserves these files when that analysis folder is selected; a synthetic export-and-verification test checks preservation. Credits do not bypass the existing privacy review or authorize public sharing.

Coverage is deliberately bounded. Function entry is not proof that a valid estimate was returned. Imported software is not proof that all its algorithms ran. Native libraries do not have complete run-time version capture yet. Worker threads, external tools, direct unwrapped launches and separately launched child analyses are not fully observed. Legacy module-specific method bibliographies remain pending where the registry says so. Registry source-hash mismatches suppress the affected observed-method claims rather than applying old citations to changed code.

### Reproducibility and migration

Attribution revision 1.0.0 is an additive schema for **new executions only**. This update does not rename protocol IDs, marker namespaces, session IDs or existing outputs, and does not backfill old runs with current software versions. Rebuilding a derived dashboard may add a credits view but does not rewrite its historical execution receipts or scientific outputs. The original release archive is unchanged.

Future attribution revisions must retain their revision and source hashes. A correction to an old study must be an explicitly labeled supplementary record, not a silent rewrite of that study's evidence. Numerical or estimator corrections require their own versioned analysis changes and, where appropriate, a new analysis run. Attribution alone never validates an experiment.

## Attribution maintenance and remaining work

The notice archive, artifact inventory, source comparisons, reviewed-method registry and automatic new-run reporting described above have been implemented, rather than left as documentation-only promises. They do **not** complete every part of a legal or scientific clearance process.

Remaining work is specific: establish historical provenance for unresolved source; audit embedded/native transitive components beyond their file inventories; verify the remaining legacy estimators; extend observation to child processes and external analysis routes; and validate the identified estimator limitations before promoting those outputs to stronger scientific claims. In particular, signed imaginary-coherency mirroring, scale-dependent entropy tolerance, stride decimation, wavelet boundary handling and RSA precision estimation remain unchanged and are disclosed in the method records.

Submit attribution corrections through the project's public issue tracker or repository contribution process, identifying the component, exact version, primary source and requested correction. Preserve original notices while a correction is reviewed.

## Document provenance

This public master page was prepared from the Alpha 10.2.1 source tree, the 67-entry protocol attribution registry, the 16-record verified protocol-source registry, the 23-module execution registry, Core/Live Monitor/hardware requirements and the hardware-source evidence record. The older analysis/Live Monitor review covered an Alpha 10.0.3 baseline; its observations are distinguished here from the newer hardware records and the current implementation checks.

Official NumPy, SciPy, MNE-LSL, MNE-Python, MNE-BIDS, LSL, BrainFlow, PsychoPy and LabRecorder documentation was consulted while consolidating the software references. The source links above provide the relevant public records. External protocol records retain their original review date; no independent legal clearance, comprehensive source audit or scientific validation is claimed.

Copyright © 2026 Hoyt Banks for this PRAYCG-authored document, subject to the project's documentation license. Quoted titles, upstream notices and third-party material retain their respective rights.
