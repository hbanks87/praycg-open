# Opto-PING research and synthetic reproducibility

Opto-PING asks whether a measured electrical signal and a candidate hidden state could form a detectable reciprocal loop. The preserved Rung 0 programs test that question in simulated data. They do not establish that the proposed cellular mechanism exists or that scalp EEG measures it.

This page brings the existing research back into the main reading path. The public record contains historical descriptions of Rungs 0A-0I and executable research packages for 0J-0O. The original files, including unsuccessful gates, remain unchanged.

[Research entrance](../README.md) · [All ladders and research stages](../ladders/README.md) · [Reproducibility programs](../reproducibility/README.md) · [Preserved Rung 0 collection](../studies/optoping-rung0/README.md)

## Start here

- Read the [16-point everyday explanation v1.1](../studies/optoping-rung0/OptoPING_16_Point_Everyday_Explanation_v1_1_NullAware_LO.pdf). Pages 4-7 trace the rungs and the sensitivity/specificity distinction; pages 11-14 describe reproduction targets and evidence boundaries.
- For the mathematical definition, read [Formula and Module Report v1.0, section 38](../collections/public-docs/Formula_Module_Report_v1_0/PRAYCG_Formula_Module_Report_v1_0.md#38-opto-ping--rung-0-synthetic-model).
- For the positive-loop reproduction target, open the [Rung 0K handoff instructions](../studies/optoping-rung0/Rung0K_ExternalReproducibilityHandoff/00_README_START_HERE/README_RUNG0K_EXTERNAL_REPRODUCIBILITY_HANDOFF.md).
- For the later null-aware target, open the [Rung 0O locked reproduction](../studies/optoping-rung0/Rung0O_LockedNullAwareReproduction/README_RUNG0O.md).

The primary composite endpoint is `K = sqrt(eta_E * zeta_E)` in the positive-coupling synthetic specification. Later signed interpretations retain the product's sign and use its magnitude separately. Recovering the composite loop is distinct from identifying its two directional parameters. See the original definitions rather than treating a shared symbol as evidence that different models or scales are equivalent.

## Complete documented Rung 0 ladder

The earlier stages are grouped as they appear in the everyday explanation, pages 4-5. That handout describes their outcomes; separate 0A-0I scripts, locked specifications and result packages were not located in the reviewed public tree or the preserved Opto-PING ZIP. These rows provide historical coverage, not newly reconstructed programs.

| Rung | Question or correction | Preserved status and source |
| --- | --- | --- |
| 0A-0B | Recover directional coupling in easier synthetic data with the hidden state or a clean proxy available | Historical handout reports recovery in the easier case; standalone artifacts not located |
| 0C | Recover coupling from the electrical signal alone while the other state is hidden | Historical handout reports weak naive E-only recovery; standalone artifacts not located |
| 0D-0F | Test whether a proxy survives gain, delay, nonlinearity, noise and mistiming | Historical handout says a proxy helps only with calibration; standalone artifacts not located |
| 0G-0I | Reduce directional ridge ambiguity and prioritize the composite loop endpoint K | Historical handout describes the transition to K; [0J's report](../studies/optoping-rung0/Rung0J_PreregisteredSyntheticLockIn/report/OSM_OptoPING_Rung0J_PreregisteredSyntheticLockIn_Report_v0_1.md) identifies 0I as its source design |
| 0J | Freeze the positive-loop design and test fresh synthetic seeds | [Recorded synthetic lock-in pass](../studies/optoping-rung0/Rung0J_PreregisteredSyntheticLockIn/README.md), 60 trials |
| 0K | Package 0J for unchanged reproduction by another operator | [Handoff and internal clean-room replay](../studies/optoping-rung0/Rung0K_ExternalReproducibilityHandoff/00_README_START_HERE/README_RUNG0K_EXTERNAL_REPRODUCIBILITY_HANDOFF.md); independent external reproduction remains a separate step |
| 0L | Test whether model selection stays quiet when no reciprocal loop is present | [Partial/failed specificity](../studies/optoping-rung0/Rung0L_EmptySkySpecificity/report/OSM_OptoPING_Rung0L_EmptySky_Report_v0_1.md), 360 trials; full-model prediction was too permissive under some null generators |
| 0M | Add stronger alternatives, penalties and a combined predictive-win/K-significance rule | [Partial/failed null-aware specificity](../studies/optoping-rung0/Rung0M_NullAwareModelSelection/README_RUNG0M.md), 120 trials; false final lock fell to zero in the tested nulls, but positive sensitivity was only 0.600 |
| 0N | Repair K-null calibration while retaining strong alternatives | [Recorded calibration-repair pass](../studies/optoping-rung0/Rung0N_KNullCalibrationRepair/README.md), 410 trials; positive full-plus-K lock 0.967, tested null final false lock 0.000 |
| 0O | Freeze 0N's choices and test fresh seeds without recalibration | [Recorded locked null-aware reproduction pass](../studies/optoping-rung0/Rung0O_LockedNullAwareReproduction/README_RUNG0O.md), 410 trials; positive full-plus-K lock 0.950, tested null final false lock 0.000 |

The null-aware rule is **full reciprocal predictive win AND K significance against the appropriate locked null threshold**. Prediction alone and K alone are insufficient. The reported rates describe the stated synthetic generators and settings; they are not biological accuracy estimates.

## Runnable packages, locks and outputs

These links open preserved files. This navigation update does not rerun them, change their dependencies or certify their behavior in a current environment.

| Package | Script or launcher | Specification, checks and reference outputs |
| --- | --- | --- |
| 0J | [Reproduction script](../studies/optoping-rung0/Rung0J_PreregisteredSyntheticLockIn/scripts/run_osm_opto_ping_rung0j_preregistered_lockin_v0_1.py) | [Locked protocol](../studies/optoping-rung0/Rung0J_PreregisteredSyntheticLockIn/locked_protocol/LOCKED_PROTOCOL.md) · [locked JSON](../studies/optoping-rung0/Rung0J_PreregisteredSyntheticLockIn/locked_protocol/LOCKED_SPEC_OSM_OptoPING_Rung0J_v0_1.json) · [results](../studies/optoping-rung0/Rung0J_PreregisteredSyntheticLockIn/tables/rung0j_pass_summary.json) |
| 0K | [Windows launcher](../studies/optoping-rung0/Rung0K_ExternalReproducibilityHandoff/02_REPRODUCTION_SCRIPT/RUN_EXTERNAL_REPRODUCTION_WINDOWS.bat) · [Unix launcher](../studies/optoping-rung0/Rung0K_ExternalReproducibilityHandoff/02_REPRODUCTION_SCRIPT/RUN_EXTERNAL_REPRODUCTION_UNIX.sh) | [Checksums](../studies/optoping-rung0/Rung0K_ExternalReproducibilityHandoff/00_README_START_HERE/SHA256SUMS.txt) · [result verifier](../studies/optoping-rung0/Rung0K_ExternalReproducibilityHandoff/07_UTILITIES/verify_external_rung0j_results.py) · [external checklist](../studies/optoping-rung0/Rung0K_ExternalReproducibilityHandoff/05_EXTERNAL_REPORT_TEMPLATE/EXTERNAL_REPRODUCER_CHECKLIST.md) |
| 0L | [Specificity script](../studies/optoping-rung0/Rung0L_EmptySkySpecificity/scripts/run_rung0l_empty_sky_v0_1.py) | [Locked spec](../studies/optoping-rung0/Rung0L_EmptySkySpecificity/locked_protocol/RUNG0L_SPEC_v0_1.json) · [results](../studies/optoping-rung0/Rung0L_EmptySkySpecificity/tables/rung0l_pass_summary.json) |
| 0M | [Null-aware script](../studies/optoping-rung0/Rung0M_NullAwareModelSelection/scripts/run_rung0m_null_aware_model_selection_v0_1.py) | [Locked spec](../studies/optoping-rung0/Rung0M_NullAwareModelSelection/locked_protocol/RUNG0M_SPEC_v0_1.json) · [results](../studies/optoping-rung0/Rung0M_NullAwareModelSelection/tables/rung0m_pass_summary.json) |
| 0N | [Calibration-repair script](../studies/optoping-rung0/Rung0N_KNullCalibrationRepair/scripts/run_rung0n_k_null_calibration_repair_v0_1.py) | [Locked spec](../studies/optoping-rung0/Rung0N_KNullCalibrationRepair/locked_protocol/LOCKED_SPEC_RUNG0N_v0_1.json) · [method note](../studies/optoping-rung0/Rung0N_KNullCalibrationRepair/docs/RUNG0N_METHOD_NOTE.md) · [results](../studies/optoping-rung0/Rung0N_KNullCalibrationRepair/tables/rung0n_pass_summary.json) |
| 0O | [Locked reproduction script](../studies/optoping-rung0/Rung0O_LockedNullAwareReproduction/scripts/run_rung0o_locked_reproduction_v0_1.py) | [Reproduction spec](../studies/optoping-rung0/Rung0O_LockedNullAwareReproduction/locked_protocol/LOCKED_SPEC_RUNG0O_v0_1.json) · [source 0N spec](../studies/optoping-rung0/Rung0O_LockedNullAwareReproduction/locked_protocol/SOURCE_LOCKED_SPEC_RUNG0N_v0_1.json) · [results](../studies/optoping-rung0/Rung0O_LockedNullAwareReproduction/tables/rung0o_pass_summary.json) |

The 0J/0K locked-spec SHA-256 is `d93f6146e4e77ffeffbdd5c133250fd6d474317d8af6c34c3354dd6b28756282`. The source 0N spec frozen by 0O is `f11cc9662d5a666c10f29e11f70c88a04e377e6499e87ae0bb1f1632e884a6b8`. Changing a model, threshold, seed policy or source specification creates a new analysis version rather than an unchanged reproduction.

## Download and provenance

The [preserved complete J-O program ZIP](../../archive/software/components/03_Individual%20Files/10_SANITIZED_COMPONENT_ZIPS/06_OptoPING_Rung0_Reproducibility.zip) contains 126 files: J 22, K 27, L 15, M 18, N 23 and O 21. Its SHA-256 is `96bab92b39f0c9dfa60e9b7d78c10c1228d579e752973dbf0be780096fe77270`. The expanded [study collection](../studies/optoping-rung0/) contains those six rung collections plus its original README and two companion PDFs, 129 files in total. Earlier rung packages are not hidden inside this ZIP.

All 126 ZIP file payloads match their canonical Git blobs byte-for-byte. For unchanged reproduction and supplied-checksum verification, use the preserved ZIP or a checkout that preserves those blob bytes. Automatic line-ending conversion can change working-copy hashes without changing the canonical research record.

The [original-file locator](../../docs/reorganization/original-file-index.md) maps the old `software/03_Individual Files/06_OptoPING_Rung0_Reproducibility/` paths to the expanded collection and the sanitized archive. Separate PDF occurrences under [analysis-module explanations](../measures/originals/analysis-module-explanations/) remain preserved as separate source occurrences.

The [0K clean-room result](../studies/optoping-rung0/Rung0K_ExternalReproducibilityHandoff/04_CLEANROOM_REPLAY_RESULTS/CLEANROOM_REPLAY_RESULT.md) documents an internal fresh-directory replay. The later everyday handout also reports user-run multi-machine repetition. Those descriptions are retained with their own scope; neither supplies an independently authored third-party reproduction report in the reviewed collection. Use the [reproducibility program guide](../reproducibility/README.md) to distinguish a supplied handoff from a completed independent replication.

## Human translation and later mechanism work

The [HumanTranslation KHT v0.2 note](../measures/originals/master-suite-v1-3-kht/HUMAN_TRANSLATION_KHT_v0_2.md) calls human-feature modeling a rough Rung 1 bridge. [CandidateLocal KHT](../measures/originals/master-suite-v1-5-5/CANDIDATE_LOCAL_KHT_v1_4.md), the [Topo-OSM reformulation](../measures/originals/master-suite-v1-5-5/TOPO_OSM_NETWORK_STATE_REFORMULATION_v1_4_7.md) and [KHT-to-KHT-topo migration](../measures/originals/master-suite-v1-5-5/KHT_TO_KHT_TOPO_MIGRATION_v1_4_7.md) retain human-scale proxy interpretations. They do not turn synthetic K into cellular K_OSM.

Direct cellular, optical or structural mechanism evidence is a separate future requirement. See the [cross-scale ladder and prospective stages](../ladders/README.md). This update adds navigation to already public material; it publishes no private recordings, participant data, restricted media or newly inferred research results.
