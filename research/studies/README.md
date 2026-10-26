# Studies and reproducibility

Use this page to distinguish human pilot observations, synthetic tests and programs you can rerun. Each report keeps its own inputs, method version, results and limitations.

**Maintained evidence catalog — reviewed 25 October 2026.** This catalog adds no new experimental results.

## Human pilot reports and exploratory reanalysis

| Material | Read or inspect | What is available |
| --- | --- | --- |
| Contact public self-run | [Original package README](contact-pilot/README.md) · [pilot interpretation](../ethics-and-claim-boundaries/originals/contact_gold_plated_not_gold_record.md) | Derived outputs for inspecting tables, visualizations and methods. Raw XDF and the copyrighted stimulus video are excluded. |
| Arrival analysis | [Report v1.0](reports/Arrival_LatestMods/report/Arrival_Run1_LatestModules_Rerun_Report_v1_0.md) · [report v1.1 PDF](reports/Arrival_LatestMods/report/Arrival_Run1_LatestModules_Rerun_Report_v1_1.pdf) | Analyses of an existing recording; “LatestMods” is a historical folder label. |
| Contact method-specific reruns | [CET-R](reports/Contact_CETR_v1_0/report/Contact_Run1_QC18_CETR_FullRerun_Report_v1_0.md) · [MRED/ITP v1.1](reports/Contact_MRED_ITP/report/Contact_Run1_MRED_ITP_Report_v1_1.md) · [NIP/CET/EET](reports/Contact_NIP_CET_EET/report/Contact_Run1_NIP_CET_EET_Report_v1_0.md) | Separate derived analyses with their own method and input identities. |
| Field of Dreams full suite | [Report v1.1](reports/Field_FULL_v1_1/report/FieldOfDreams_Run1_FULL_MasterComp_Report_v1_1.md) | The retained full-suite report and supporting bundle. |
| Cross-run NUPI companion | [Report](reports/NUPI_ACF/report/NUPI_Arrival_Contact_Field_Report_v1_0.md) · [reproduction script](../collections/public-docs/Framework_NUPI_Update_v0_5/scripts/run_nupi_arrival_contact_field_reproduction.py) | Reanalysis of historical derived inputs. Original input paths require the matching tables/JSON and explicit local setup; this is not a self-contained raw-recording kit. |

The [complete report catalog](reports/README.md) includes other versions, peak/resolution comparisons, tables, figures and packaged archives. Reanalyzing these exploratory records does not create a new participant sample or confirmatory replication.

## Opto-PING: model, rungs and runnable programs

Start with the [Opto-PING research account](../optoping/README.md) for the model and full preserved 0J–0O sequence. It retains the unsuccessful specificity results as well as the later repairs. The [ladder catalog](../ladders/README.md) places that sequence beside earlier documented and prospective work.

| Purpose | Open the package | Check the result against |
| --- | --- | --- |
| Inspect the locked synthetic identifiability test, 0J | [README and run context](optoping-rung0/Rung0J_PreregisteredSyntheticLockIn/README.md) · [runner](optoping-rung0/Rung0J_PreregisteredSyntheticLockIn/scripts/run_osm_opto_ping_rung0j_preregistered_lockin_v0_1.py) | [Locked protocol](optoping-rung0/Rung0J_PreregisteredSyntheticLockIn/locked_protocol/LOCKED_PROTOCOL.md) and [saved summary](optoping-rung0/Rung0J_PreregisteredSyntheticLockIn/tables/rung0j_pass_summary.json). |
| Perform the external reproduction handoff, 0K | [Setup and run instructions](optoping-rung0/Rung0K_ExternalReproducibilityHandoff/00_README_START_HERE/README_RUNG0K_EXTERNAL_REPRODUCIBILITY_HANDOFF.md) | [Verifier](optoping-rung0/Rung0K_ExternalReproducibilityHandoff/07_UTILITIES/verify_external_rung0j_results.py) and [external reporting checklist](optoping-rung0/Rung0K_ExternalReproducibilityHandoff/05_EXTERNAL_REPORT_TEMPLATE/EXTERNAL_REPRODUCER_CHECKLIST.md). The retained clean-room pass is internal. |
| Reproduce the locked null-aware test, **0O** | [README and run instructions](optoping-rung0/Rung0O_LockedNullAwareReproduction/README_RUNG0O.md) · [requirements](optoping-rung0/Rung0O_LockedNullAwareReproduction/requirements_rung0o_v0_1.txt) · [runner](optoping-rung0/Rung0O_LockedNullAwareReproduction/scripts/run_rung0o_locked_reproduction_v0_1.py) | [Locked 0O specification](optoping-rung0/Rung0O_LockedNullAwareReproduction/locked_protocol/LOCKED_SPEC_RUNG0O_v0_1.json), [frozen thresholds](optoping-rung0/Rung0O_LockedNullAwareReproduction/locked_protocol/LOCKED_RUNG0N_K_THRESHOLDS.csv) and [saved summary](optoping-rung0/Rung0O_LockedNullAwareReproduction/tables/rung0o_pass_summary.json). |

The [reproduction guide](../reproducibility/README.md) explains environment records, verification and how to report deviations. Use each rung's own criteria: the 0J verifier does not grade 0O. Synthetic sensitivity and specificity apply to the declared generators and settings; they do not establish a human EEG or cellular mechanism. A supplied external handoff is not itself an independent replication report.

## Plans and source preservation

The [research roadmap](../roadmap.md) and [protocol specifications](../protocols/README.md) describe prospective human work. Keep those plans separate from completed reports.

All study packages, scripts and reference outputs remain at their existing paths. The [original Opto-PING collection README](optoping-rung0/README.md), [NUPI framework package](../collections/public-docs/Framework_NUPI_Update_v0_5/README_NUPI_Framework_Update_v0_5.md) and [original-file locator](../../docs/reorganization/original-file-index.md) preserve the wider source trail. Review the [public data boundary](../ethics-and-claim-boundaries/originals/public_data_boundary.md) before sharing new outputs.

[Research home](../README.md) · [Methods catalog](../methods.md) · [Sources and history](../../docs/README.md)
