# Alpha 10.5.3 — shared visual review, recorded replay and passive live state

This complete Workbench release adds Visual Analysis to Analysis Forge and Live Monitor. A recording can be inspected through PRAYCG 3 Review, Time–Frequency, State landscape and Timescale inspector using a shared source identity, cursor and selection.

## Changes

- Native completed-result review accepts supported JSON attachments bound to the selected recording. Payload changes are detected on reopening; historical methods retain their original labels and scope.
- Recorded prefix replay and passive live viewing share an incremental visual-state engine. A seek or source change rebuilds/reset state. Future recording samples cannot change an already available result.
- Fixed source mapping, calibration and scales are recorded. EEG support, represented time, window bounds and availability remain distinct. Gaps, missing channels and insufficient calibration stay explicit.
- The timescale view separates gamma threshold events, delayed theta responses at +0.5 to +1 seconds, and slower +8 to +30 second responses. Pending and unsupported responses are visible.
- State depth offers completed CAI, historical NIP and explicitly experimental Autonomic state as distinct choices. Raw EEG/RR never fabricates missing CAI, NIP or CAI-SID components.
- Media landmarks and inspection bookmarks remain separate from qualifying physiological events. Measured, spline and generated signals retain their provenance.
- The original review and TFR tools remain available through optional shared-cursor links. Unsupported clock or original CSV mapping prevents an assumed synchronization.
- **START.bat** provides a short public launcher alongside **START_PRAYCG.bat**. Normal installers and optional Zuna installation remain included.

## Validation scope

The current release gate requires all nine declared offline regression groups to pass against an unchanged source fingerprint, current native-view acceptance bound to source hashes, preservation of the original 10.5.2 source, and exact directory/ZIP file verification. Counts and hashes are recorded in the [current build evidence](BUILD_VALIDATION_v1_0_0_alpha_10_5_3.json); the [current version manifest](VERSION_MANIFEST_v1_0_0_alpha_10_5_3.json) identifies the shipped source. Fresh-extraction smoke testing has a separate delivery receipt and does not constitute an installation test.

This release does not claim new physical hardware acquisition, cross-device timing, a fresh full installation, optional Zuna installation/inference, or physiological validation. Earlier SDK, acquisition and model evidence remains historical. Preserved historical build files do not describe current tests.

Private Contact/Arrival/EO–EC recordings, study arrays, generated replay payloads, native screenshots, environments and test caches are excluded from the public software package. The visualizer opens compatible results supplied locally by the operator.

The landscape is an exploratory display. Its geometry does not establish an attractor, a meaning force, narrative absorption or consciousness. Gamma threshold events are neither 40 events per second nor individual oscillatory cycles. See the [Visual Analysis guide](VISUAL_ANALYSIS_ALPHA_10_5_3.md) and [installation guide](INSTALL_AND_WORKFLOW_ALPHA_10_5_3.md).