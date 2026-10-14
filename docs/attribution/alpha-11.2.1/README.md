# Public Alpha 11.2.1 attribution review

**Reviewed 13 October 2026. Repository supplement for a proposed release; application archive unchanged.**

The repository's master record previously stopped at Alpha 10.5.4. The inspected Public Alpha 11.2.1 package already contains newer Signal Review credits, method records and upstream notices. This supplement preserves selected evidence from that package and connects it to the [current research bibliography](../../../research/bibliography/README.md) and [master attribution record](../../../CITATIONS_AND_ATTRIBUTION.md).

Source: `PRAYCG_Workbench_Public_Alpha_11_2_1.zip`, **43,737,009 bytes**, SHA-256 `cb65ec3180a59a9181e4fecd9bb94a2b136ab158f0f275eaf49b01dc3386c42b`. The [source manifest](SOURCE_MANIFEST.json) gives archive paths, sizes and hashes for copied records and inspected implementation evidence. Its preserved files retain their original bytes; this page and the research bibliography are new repository documentation.

## What is current

| Record | Finding |
| --- | --- |
| NeuroKit2 0.2.13 | Required during setup and directly called by physiology review. MIT license and AUTHORS text are preserved. The package already credits Makowski et al., Pan–Tompkins and Lipponen–Tarvainen. |
| PyWavelets 1.9.0 | A direct installation requirement supporting NeuroKit2. Main MIT license and bundled NumPy/SciPy notices are preserved; distribution metadata reports `MIT AND BSD-3-Clause`. No independent PRAYCG wavelet execution is inferred from installation. |
| mne-denoise 0.0.3 | Real spectrum-interpolation and fixed-selection ZapLine calls, with method records and BSD-3-Clause license. Method citations and integration authorship remain separate. |
| New bibliography | Adds a readable software/method map, full scholarly references and EEGLAB's external-reference status. Existing research manuscripts and original bibliographies are preserved. |
| Automatic credits | The active `app/config/attribution_registry_v1.json` has revision `1.1.1-alpha11.2.1`, 40 module records and 34 method records. Its module IDs match the 40 managed orchestration IDs. All 34 declared method source hashes match the inspected archive. |

The [original Signal Review addendum](package/app/THIRD_PARTY_NOTICES/SIGNAL_REVIEW_11_2_0.md) links the six retained upstream texts. Their hashes were checked against the archive and addendum. These notices accompany PRAYCG integration code and installation requirements; the application ZIP does not include the NeuroKit2, PyWavelets or mne-denoise implementation distributions. Setup obtains those separately.

The addendum retains its original Public Alpha 11.2.0 heading because it first shipped with that feature. It is also present in the exact 11.2.1 archive reviewed here. A preserved heading is not a claim that the inspected package is 11.2.0.

## EEGLAB and related methods

No bundled MATLAB EEGLAB implementation, direct EEGLAB invocation, or PRAYCG ASR, clean_rawdata or ICLabel integration was identified in this package review. LabRecorder's README lists an EEGLAB XDF importer, and historical MNE metadata includes optional EEGLAB I/O support. Those mentions do not establish an executed EEGLAB analysis.

The bibliography therefore records Delorme & Makeig (2004) as an external software reference. A study that separately processes data in EEGLAB must record its actual EEGLAB version, plugin versions and operations, and cite the corresponding methods. The existence of additional methods in an installed upstream library is not evidence that PRAYCG called them. This bounded inspection is not a complete historical source-origin audit.

## Coverage and remaining gaps

The active registry includes all four new Signal Review modules. Twenty-three of its 40 module records have nonempty method lists; 17 have none. The historical `app/attribution/attribution_registry_v1.json` remains revision 1.0.0 with 23 modules and 14 methods. It must not be presented as the active 11.2.1 registry.

Source-hash agreement verifies the link between a record and inspected code. It does not show that a function ran or returned a usable result. SpectrumInterpolation and fixed-selection ZapLine retain declared citations without observer function-entry claims; the comparison's candidate and segment statuses provide the execution evidence. Installed distribution capture, declared references and successfully produced results are distinct records. Full automatic method-level bibliography coverage is not established by this documentation update.

The new research bibliography fills manual citation gaps that remain in generated reports: the ECG registry references NeuroKit2 and Pan–Tompkins, while the correction citation appears in `physiology.py`; complete Khodadad/Harrison respiration references are not present in those automatic records. Adding these references to the repository does not change the packaged reporting behavior.

**A release issue was also reproduced in the new protocol-ratings credit record.** Its missing observer-required `functions` field raises `KeyError` before the worker starts; `definition` is also absent. An isolated check used the exact packaged observer with a harmless sentinel worker, without running the scientific analysis. The [proposed metadata fix and verification](proposed-fixes/README.md) are kept separately for review. The original package and preserved registry remain unchanged. Registry membership and matching source hashes alone therefore do not establish that all 40 managed launch paths work.

The four direct requirement additions since Alpha 10.5.4 are NeuroKit2, PyWavelets, mne-denoise and `PyJWT[crypto]>=2.8,<3`. The latter is authentication infrastructure, not a neuroscience method, and its requirement range is not an exact installed-version record. The Signal Review package notice set does not cover PyJWT/cryptography; the separate observed-environment supplement below is a bounded addition. Record actual resolved versions and retain their distribution notices when preparing or redistributing an installed environment.

A separate local Core environment record captured on 13 October 2026 reports **PyJWT 2.15.1** and **cryptography 50.0.2**. Five upstream notice texts were preserved from matching installed distribution metadata: PyJWT's [MIT license](observed-environment/pyjwt-2.15.1.dist-info/licenses/LICENSE) and [authors](observed-environment/pyjwt-2.15.1.dist-info/licenses/AUTHORS.rst), and cryptography's [dual-license statement](observed-environment/cryptography-50.0.2.dist-info/licenses/LICENSE), [Apache-2.0 text](observed-environment/cryptography-50.0.2.dist-info/licenses/LICENSE.APACHE) and [BSD-3-Clause text](observed-environment/cryptography-50.0.2.dist-info/licenses/LICENSE.BSD). The source manifest keeps these observed-environment records separate from package bytes. They do not pin every installation to those versions or inventory all embedded/native dependencies.

Older estimator reviews, unresolved historical source provenance, native/transitive component inventories and observation of external or child-process analyses retain their earlier limits. See the [historical reviewed methods](../ANALYSIS_METHODS.md) and [master maintenance record](../../../CITATIONS_AND_ATTRIBUTION.md#attribution-maintenance-and-remaining-work). Apart from the isolated observer check described above, no application workflow test was run for this supplement. No scientific analysis, fresh installation or device qualification was run, and no previous execution receipt was backfilled.

## Use this record in the proposed update

Link the [research bibliography](../../../research/bibliography/README.md) from the release notes and research entrance. Cite only the methods and software actually used in a study, with the producing release and input/output provenance. These added repository references are not automatically inserted into the unchanged application's generated reports.

[Update proposal](../../updates/2026-10-13-public-research-update.md) · [Package documentation](../../../workbench/docs/releases/alpha-11.2.1/README.md)
