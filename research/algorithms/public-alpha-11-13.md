# Public Alpha 11.13 endpoint and support map

Public Alpha 11.13.0 revised three reporting definitions and added six. A study can yield a low score, a failed condition, or too little usable data to estimate a score. The table describes how to tell those outcomes apart for these nine entries. The saved execution record identifies which version actually produced a historical result.

| Calculation | Required inputs or support | How to read missing or partial support |
| --- | --- | --- |
| **CAI and SID** | The selected feature table or explicitly generated NAST derivative, finite required features, accepted rows and enough unique time points within the continuous block. | CAI uses future slow activity. Managed SID averages finite CAI over usable duration. Rejected, duplicate or unsupported time cannot supply the missing future observations. |
| **NIP, CET, CET-R and EET** | Full NIP needs current and delayed theta, MeaningGamma or TSP, and artifact support. EET needs measured features in both the anchor and after-state windows. | A reduced-input NIP has its own label. EET reports shared features and the two vectors. Resemblance describes those vectors. CET-R residuals depend on the regressors and timing used. |
| **Master Suite and MRED** | Recording, identified condition and event feature tables, each with its own component and artifact coverage. | MRED can retain recognition when theta handoff is missing. Encoding then remains unavailable. A high-recognition/low-encoding classification requires a measured encoding value. |
| **A-MRED** | An identified anchor, acute observations, and full continuous coverage of the delayed interval in each compared condition. | Acute recognition can survive a missing delayed endpoint. Duplicates and gaps cannot fill delayed support. A strict software pass alone cannot establish new memory encoding. |
| **NAST** | Positive alpha decrease together with positive MeaningGamma or TSP, score and artifact checks, and eight seconds of observed continuous support. | An isolated row or artifact relief alone cannot count as sustained onset. Inspect component values and usable time before interpreting a missing candidate. |
| **TTI** | Condition-specific reception, encoding and extraction inputs with the expected field identities. | The weighted contrast and the Boolean test for joint positive support are separate outputs. Task load alone can contribute a positive contrast. Missing components remain visible. |
| **NUPI** | Canonical TTI, available load components, unique anchor rows for pass fractions, and usable final-baseline evidence for recovery. | An absent or all-invalid final baseline leaves recovery unresolved. Missing complexity stays missing. Report the load and recovery components alongside their difference. |
| **MRED Peak and Resolution** | Upstream A-MRED fields, with finite anchor-specific after-state evidence for a Resolution candidate. | A run-wide recovery value can describe the run. It cannot establish resolution for each anchor. Missing echo remains unavailable. |
| **MRED-ITP** | Usable pre-event, peak and post-event complexity features, declared relative thresholds and an artifact check. | A complexity candidate requires a positive peak-minus-pre change and a negative post-minus-peak change. A relative ranking alone cannot establish that pattern. |

## Locate the calculation in the Workbench

Paths below start at the extracted package's `app/` folder. The reporting catalog is `tools/Analysis_Results_Dashboard_v0_1/implemented_measure_definitions_v1.json`. Each entry's `version` identifies the method and its `reviewed_implementations` records complete paths and SHA-256 values. Some filenames retain an older version number. Use the recorded method version when citing a result.

| Catalog entry | Recorded method version | Worker file under `app/` |
| --- | --- | --- |
| `cai_sid` | `CAI-core-0.2.1; managed-0.2.1-alpha.11.13.0; alpha11.13.0.dependency-qc-source-v1` | `tools/CAI_SID_Exploratory_v0_2/scripts/praycg_cai_sid_v0_2.py`<br>`tools/CAI_SID_Exploratory_v0_2/scripts/praycg_cai_sid_managed_v0_2.py` |
| `nip_cet_eet` | `packaged-NIP-CET-EET-1.6.2-alpha11.13.0; PRAYCG_DESCRIPTIVE_STIMULUS_ADJUSTMENT_v1.0` | `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_nip_cet_eet_modules_v1_6_0.py` |
| `master_comprehensive` | `master-1.6.0; alpha10.3.8.rank-descriptive-v1; distinct-phase-shot-conditions-v1; RRClockSemantics-v2-and-gap-support-review; alpha11.13.0.separate-endpoint-availability-v1` | `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_master_comprehensive_suite_v1_6_0.py` |
| `amred` | `A-MRED-1.6.2; alpha11.13.0.separate-acute-delayed-support-v1` | `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_amred_endpoint_module_v1_6_0.py` |
| `nast` | `NAST-1.4.4; alpha11.13.0.joint-evidence-continuous-support-v1` | `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_nast_ocm_modules_v1_4_4.py` |
| `tti` | `TTI-1.4.9-alpha11.13.0` | `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_tti_reception_extraction_module_v1_4_8.py` |
| `nupi` | `NUPI-1.6.2; alpha11.13.0.usable-baseline-contract-v1` | `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_nupi_module_v1_6_0.py` |
| `mred_peak_resolution` | `MRED-PeakResolution-1.6.2-alpha11.13.0` | `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_mred_peak_resolution_module_v1_6_0.py` |
| `mred_itp` | `MRED-ITP-1.6.2-alpha11.13.0; positive-strike-negative-settle-v1` | `tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_mred_itp_modules_v1_6_0.py` |

The 11.13.0 archive has SHA-256 `5c34cf6c24e2030deb35c699650ab4fad46fce2e8551a4a5ecf17bf87c25fe44`. Its reporting catalog has SHA-256 `fc890a8e6c420471254147e74308855926c6475df5ca5fb5930ded14f6b4d808`. The Public Alpha 11.13.1 build carries the same catalog and matching worker files for all nine entries. The two release archives have their own identities. [11.13.0 release and build evidence](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.13.0)

Gamma Scalpel 2.1, experimental API-A component comparisons and Decoder Gate item review also shipped in 11.13.0. They have their own methods and records outside these nine entries. [11.13.0 build report](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.13.0/BUILD_REPORT.md) · [Decoder Gate guide](../theory/extensions/decoder-gate.md) · [Methods catalog](../methods.md) · [Earlier 11.2.1 implementation map](README.md)
