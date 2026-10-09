# Alpha 10.5.4 — visual entry points and Athena admission packaging

This complete Workbench release corrects three problems encountered when using Visual Analysis and the Athena profile workflow.

- **Live Monitor:** Visual Analysis is beside Time–Frequency.
- **Analysis Forge:** the Visual Analysis tab follows Analyze, before Results.
- **Recorded XDF:** Visual sources opens the source-selection dialog and reports a failure reason when selection cannot proceed.
- **Calibration:** an explicit start offset, default 0, can deliberately use the selected EEG stream’s recorded start while retaining the shared recording origin. Valid-support and gap requirements remain unchanged. Method labels are experimental_streaming_visual_state_v1_1 and experimental_streaming_api_a_v1_1.
- **Athena Human connected profiles:** the public package includes the exact retained admission receipt required by the active source ledger. Profile validation keeps its existing missing/tampered-evidence checks.
- **Empty profiles:** profile-draft actions explain that a device must be selected before attempting filesystem writes.

## Packaging correction

The earlier public package excluded the whole validation directory, unintentionally omitting a runtime dependency: validation/athena_eeg_acquisition_10_5_1.json. This release includes that single reviewed receipt at its original SHA256. The receipt retains its original 10.5.1 scope: single-unit EEG acquisition and recording checks. It does not establish physiological accuracy, clinical performance, cross-device timing, optical hemoglobin conversion or reconstruction accuracy.

The builder now audits active hardware and analysis hash dependencies recursively and checks local runtime configuration paths for missing or excluded files. It repeats these checks on the staged and extracted application. Fresh extracted tests exercise the actual Human connected Athena profile path, plus missing and altered evidence rejection. No missing dependency is repaired by weakening admission checks or rewriting its evidence.

All other private validation data, study recordings, replay arrays, native screenshots, environments and temporary test outputs remain excluded. The original 10.5.3 source and public package remain separate.

## Retained visual workflow

PRAYCG 3 Review, Time–Frequency, State landscape and Timescale inspector retain one source-bound cursor. Completed results, recorded prefix replay and passive live views remain distinct. Raw live EEG/RR continues to withhold unsupported CAI, NIP and CAI-SID components. Experimental Autonomic state, historical model values, measured and reconstructed signals remain separately labeled.

See the [Visual Analysis guide](VISUAL_ANALYSIS_ALPHA_10_5_4.md) and [installation guide](INSTALL_AND_WORKFLOW_ALPHA_10_5_4.md).

## Validation scope

Release packaging requires all nine declared regression groups against an unchanged current source fingerprint, current focused native acceptance, preservation of the preparation baseline, runtime dependency closure, and exact directory/ZIP hashes. Test-harness isolation keeps short Windows paths and Python-level output capture. Timing-sensitive retained hardware software tests run after the other groups; their existing deadlines and assertions remain intact.

The [current build evidence](BUILD_VALIDATION_v1_0_0_alpha_10_5_4.json) records results and limitations. The [current manifest](VERSION_MANIFEST_v1_0_0_alpha_10_5_4.json) identifies current source and the retained receipt. Fresh-extraction testing has a separate delivery receipt.

These are software and packaging checks. No fresh physical acquisition, full installation, optional model inference or physiological validation is claimed. Earlier evidence remains historical. See the [implementation and evidence guide](UPDATE_TRACEABILITY_ALPHA_10_5_4.md).
