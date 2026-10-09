# Alpha 10.5.4 implementation and evidence

The release uses a separate 10.5.4 source tree. Original 10.5.3 source preservation is checked against its preparation inventory. This release's generated manifest, build validation and source ledger are separate from retained historical evidence.

## Runtime admission packaging repair

The 10.5.3 public layout omitted validation/athena_eeg_acquisition_10_5_1.json even though the active Athena admission configuration requires it. Alpha 10.5.4 ships only this explicitly allowlisted receipt from that directory, at its exact reviewed SHA256 4cf2a6b468f46bc5191f993d75b9543a40bb1a837c1d5620153ea8ae600da17e. It remains a retained, bounded 10.5.1 acquisition/recording receipt, not fresh device evidence. Private recordings, screenshots and temporary validation files remain excluded.

The builder checks active hardware/analysis hash dependencies recursively, scans local runtime configuration references for missing or excluded files, and repeats those checks on the staged and extracted application. Explicit upstream repository paths remain external references. The runtime receipt enters current source and distribution hashes. The original baseline uses the exact preparation inventory, which excludes validation scratch; the retained receipt is checked separately against its fixed hash. Fresh extraction tests exercise the Athena Human connected profile path, including rejection when evidence is missing or changed.

## Implementation map

| Area | Source in the application tree | Responsibility |
| --- | --- | --- |
| Incremental state | platform_core/praycg_visual_state_core_v1_0.py | Fixed calibration, trailing EEG/RR features, support and availability, delayed event responses, bounded history. |
| Passive/replay feeds | tools/Live_Monitor_v1_0/praycg_live_monitor_v1_0.py; praycg_xdf_replay_v1_0.py | Explicit stream identity, selected electrode/units mapping, prefix feed, seek reset and clock handling. |
| Shared session | control_center/scripts/praycg_visual_analysis_session_v1_0.py | Source-bound cursor, selection, view normalization and per-metric availability. |
| Native viewer | control_center/scripts/praycg_visual_analysis_viewer_v1_0.py | Four views, paired display, separate event/landmark/bookmark navigation and saved view context. |
| Application integration | control_center/scripts/praycg_visual_analysis_forge_ui_v1_0.py; praycg_visual_monitor_ui_v1_0.py; praycg_visual_analysis_data_v1_0.py | Forge/monitor entry points, source settings, verified completed attachment and cursor linkage. |
| Original review | tools/MasterComprehensiveSuite_v1_6_1_CURRENT/scripts/praycg_master_sync_visualizer_v1_4_0.py | Optional shared selection around the preserved review layout. |
| Time–Frequency | tools/Time_Frequency_Explorer_v1_0 and existing Forge TFR integration | Optional linked selection retaining the spectral workflow. |

The analysis orchestration registry retains its scientific module IDs, dependencies, method metadata and binding keys. Current hashes are refreshed for already declared implementation/configuration bindings. New display sources are bound by current release and native acceptance evidence; they do not alter frozen offline algorithm definitions.

## Explicit calibration start

`config.calibration_start_seconds` specifies the baseline start relative to the unchanged shared recording origin; default 0. The dialog can deliberately select the recorded EEG start. The v1.1 streaming visual-state and API-A methods retain fixed-interval calibration, availability and strict support checks. Tests cover nonzero starts, unchanged clock alignment, prefix independence and insufficient support. Selecting a later baseline does not imply successful calibration. Neither the local Contact nor the short October 8 Muse raw-data check met the required valid support; completed historical results remain separate.

## Current engineering checks

The release gate requires nine regression groups: attribution; control center; report/bundle roundtrip; analysis/bundling; protocol/installer; BrainFlow connector; retained hardware software; numerical/managed analyses; and release contracts. Tests run in isolated temporary/configuration directories with fresh logs and JUnit output. The source fingerprint is checked before and after execution, and again before packaging.

Focused visual checks cover future-suffix invariance, rechunking, exclusive availability, gaps, source changes, finite calibration, pending-to-completed responses, bounded retention, recording seek/reset, source binding and native render integration. Synthetic fixtures exercise engineering behavior; they do not validate the physiological interpretation of a surface or event.

The current [build validation](BUILD_VALIDATION_v1_0_0_alpha_10_5_4.json) supplies counts, implementation bindings and limitations. The [version manifest](VERSION_MANIFEST_v1_0_0_alpha_10_5_4.json) identifies source. The distribution manifest and SHA256SUMS in app/deployment bind every shipped file to the public layout. Fresh extraction verification, when performed, has a separate receipt outside the ZIP to avoid changing the artifact being tested.

## Explicit boundaries

- The raw incremental feed supplies measured gamma/theta features and eligible cardiac features. CAI, NIP and CAI-SID remain unsupported without their required completed-analysis components.
- Experimental API-A and Autonomic state have distinct versioned recipes and names. They do not inherit frozen CAI/SID validation.
- Explicit electrode positions and units are required; generic channel labels are not guessed. Missing channels prevent the corresponding EEG features.
- Represented time, window support and availability are separate. A shared cursor does not establish physical device synchronization or repair an uncertain media/CSV clock mapping.
- Basic amplitude/gap screens cannot establish removal of eye or muscle artifacts. Reconstructed signals are not independent physiology.
- Live history is bounded; a request older than retained history requires a reset/rebuild.
- Offline/source, native GUI and extracted smoke tests are software checks. Fresh full installation, SDK hardware acceptance, physical cross-device timing and clinical/physiological validation were not reexecuted as part of this release gate.
- Historical manifests, acceptance records and source references remain historical, even when retained in the software tree.

The public distribution contains the complete application and matching regression assets. Private study data, completed demonstration payloads, private screenshots, local environments and caches are excluded. See the [Visual Analysis guide](VISUAL_ANALYSIS_ALPHA_10_5_4.md) for interpretation and the [release notes](RELEASE_NOTES_v1_0_0_alpha_10_5_4.md) for changes.