# Alpha 11.4.0 / AUL 1.3.0: recommendation ledger and honest limits

## Changes in this release

The updated EEG/cap review shifted priority from adding algorithms to support, integration and preservation evidence. This release follows that order where the required evidence is available:

| Recommendations | New delivery / remaining boundary |
|---|---|
| 5, 11 | Explicit baseline/response usable-duration coverage, largest gaps, finite support, compatible clocks, beat timing semantics and filter-edge/retrospective availability checks. Defaults are versioned operational policies, not acquisition exclusions or universal validity criteria. |
| 7, 14 | Exact selected annotation file/hash and source-bound active exclusions in Signal Review, reviewed-candidate reopening and comparison. Every historical governed worker is not yet migrated; plans are not silently changed. |
| 26, 32 | Verified saved comparison playback with original, current preview, candidate and removed signal; source-bound shared cursor. No automatic CAI/SID/TFR endpoint recalculation from a candidate. |
| 27, 36 | Operator-facing delayed recording replay, explicit interval up to 60 seconds, measured processing time, cancellation, gap resets and bounded loading. Physical live acquisition cleaning is not enabled. |
| 28 | Supported Athena result-to-report associations preserve exact evidence and qualifications. Model prose still requires review; no universal mapping or semantic validation is claimed. |
| 29, 33, 34, 37 | Frozen nine-case synthetic collection across three methods (27 executions), separate development/held-out waveforms, pass-specific distortion, no-op policy and source-bound independent-evidence correction policy. Wanted slow activity can still be strongly attenuated; no overall winner is claimed. |
| 8–10, 12–13, 15–24, 31, 35, 37 | Representative real/device/independently adjudicated validation, authentic MATLAB reference fixtures, cross-rate artifact review and fully linked endpoint comparison remain incomplete. No clean human ground truth was invented. |
| 21, 25, 30 | Isolated EEGPrep integration, complete study-management GUI and specialist source methods remain deferred. |

The real Athena checks in BUILD_REPORT.md verify execution, persistence and unchanged source bytes. They do not supply clean-control labels, validate SPAR preservation or qualify live hardware. The earlier 21-execution benchmark is retained unchanged alongside the new frozen benchmark.

## Retained Alpha 11.3.0 implementation baseline

All 37 recommendations were considered. This is a substantial implementation pass, **not completion or scientific validation of all 37**. The table distinguishes implemented software, partial integration, evidence still required, and deliberately deferred work. Existing historical tests do not prove newly added methods.

| Item | Delivered scope / remaining work |
|---|---|
| 1 | Common description extended with participant/device identity, explicit pairings, declared electrode geometry and rank status. Unknown values remain unknown; numerical magnitude is not signal identity. |
| 2 | HR-only stays HR-only; historical fallback audit retained. No invented RR/HRV from reciprocal sampled HR. |
| 3 | Legacy Master Sync raw-XDF RMSSD uses original beat adjacency, including missing intervals and gaps. |
| 4 | Legacy interpolation/PSD/respiration and new candidates respect continuous pieces. Targeted audits/tests do not certify every historical estimator. |
| 5 | Timing, retrospective support and estimator delays are retained. Extending these displays to every legacy trace remains incomplete. |
| 6 | Channel, pair and group support stays distinct from artifact screening and endpoint eligibility. Explicit available-duration explanations retained. |
| 7 | Immutable exclusions support retraction/correction, source hashes, reasons and retained duration. Existing governed workers are not all migrated to this new annotation ledger. |
| 8 | Reviewed-beat comparison software measures missed/extra detections and timing errors. Representative independently adjudicated real Polar beats are still required. |
| 9 | Adjacency-preserving HRV, reviewer-labeled interval exclusions, duration-qualified Welch/Poincaré comparisons implemented. This does not certify normal-to-normal intervals. |
| 10 | Explicit cardiac/respiration participant/channel/timing pairing; actual optional NeuroKit RSA kept separate from PRAYCG harmonic coupling. Real physiological validation remains. |
| 11 | Independently anchored autonomic response comparisons with baseline/support requirements. Reviewers must supply legitimate anchors. |
| 12 | Actual NeuroKit PPG/PRV and EDA processing/comparisons added to signal review. PRV remains distinct from ECG-derived HRV. Not a validated optical/clinical pipeline. |
| 13 | Heuristic EOG/EMG/motion evidence and review overlays exist; propagation across every TFR/time-scale view remains partial. Detection does not authorize subtraction. |
| 14 | Shared candidate adapter, original/candidate/difference, explicit immutable reviewed-input receipt and downstream research comparisons. No silent governed-plan replacement. |
| 15 | Existing actual spectrum interpolation and fixed ZapLine retained and regression-tested. Representative neighboring-frequency preservation and device-specific validation remain. Not ZapLine-plus. |
| 16 | Offline fixed-seed ICA, rank/fit/convergence checks, component loadings/traces/spectra and explicit removal preview. Sparse recordings remain limited; unmeasured geometry is not invented. |
| 17 | Actual advisory ICLabel in an isolated worker with preprocessing/geometry restrictions, separate fit identity and no automatic deletion. |
| 18 | Actual calibrated offline ASRpy candidate in an isolated NumPy 1.26 environment, gap resets and support edges. Neural preservation and live use remain unqualified. |
| 19 | Explicitly paired reference-assisted linear regression implemented. It is not an iCanClean implementation; comparative sensor-benefit validation remains. |
| 20 | Governed EDF/BDF, EEGLAB and BrainVision imports, source-sidecar ledger and round-trip checks. External identities retained. |
| 21 | Deferred: reviewed EEGPrep requires Python 3.12+, while this release uses 3.11. No substitute is labeled EEGPrep; no selected EEGPrep processing route is claimed. |
| 22 | Mean/median Welch, baseline-subtracted ERP, trial-bootstrap uncertainty and actual Morlet power/ITPC comparison added. Existing aperiodic estimator identity unchanged. Further estimator choices remain. |
| 23 | Before/after native/average-reference PLV and explicitly defined PAC with shift controls. Screening p-values are unadjusted, not causal evidence; ecological/event-confound validation remains. |
| 24 | Independent Pycrostates comparison and matched-window ordinal/spectral entropy comparisons added. Comprehensive cross-implementation validation remains partial; complexity is not meaning/consciousness. |
| 25 | Participant-level paired comparisons and group-separated decoding available through documented worker interface. Full study-management GUI and general repeated-measures modeling remain future work. |
| 26 | Linked original/current/candidate review, pass/component inspector and downstream comparison reports added. CAI fabric/SID residence/autonomic linked-state integration is not completed. |
| 27 | Bounded, gap-reset and future-invariance tests for the new delayed replay candidate. Each other live estimator still needs separate qualification; no new live acquisition cleaner enabled. |
| 28 | Source-linked six-question processing explanations and saved numerical evidence added; Public Assistant/AUL boundaries retained. No model selects a cleaner. Not every old report has been redesigned. |
| 29 | Synthetic tests cover artifacts, gaps, units, missing data, malformed identities, sample rates and multichannel cases. Held-out real/adjudicated validation is still needed. |
| 30 | Source localization, SOUND, AMICA and specialist EEG-fMRI/TMS additions deliberately deferred, as recommended. |
| 31 | Attributed native SPAR reference candidate pinned to upstream source, exact MIT notice and per-pass implementation records. MATLAB fixture comparator exists; no actual MATLAB numerical equivalence established. |
| 32 | Saved pass outputs, removed signal, detection weights, correction strength and bypass/unsupported evidence; native pass inspector with separate diagnostic scales. |
| 33 | Separately versioned residual-preserving variant tested alongside reference. Synthetic results do not show uniform superiority. |
| 34 | Independent reference-evidence API is source/participant/time bound; available EOG/EMG evidence remains separate. Automatic cross-rate evidence alignment/complete GUI handoff is not implemented. |
| 35 | Multichannel wrapper retains grid/identity and reports spatial distortion; cleaning does not qualify KHT/connectivity/spatial endpoints. |
| 36 | Replay-only delayed candidate with past calibration, chunk/future invariance tests and bounded buffers. Physical passive-acquisition integration deliberately withheld pending qualification. |
| 37 | Seven synthetic cases × unchanged/reference/preservation = 21 executions. Measured shielded controls and held-out Arrival/Contact have not been evaluated here. Zuna is not ground truth. |

## Unfavorable results must remain visible

In the shipped synthetic benchmark, clean-control normalized mean squared error was approximately **0.083671 for the reference candidate and 0.029058 for the preservation variant**, versus **0 for unchanged input**. Both modified a signal that was intended to remain clean. The preservation variant was worse in some contaminated cases: the 250 Hz mixture had NMSE approximately 3.7640 versus 2.9586 for reference. These are measurements of this synthetic corpus, not accuracy claims about human EEG.

See [the full synthetic preservation benchmark](app/tools/Signal_Review_v1_0/validation/SPAR_SYNTHETIC_PRESERVATION_BENCHMARK.json), [SPAR method/provenance records](app/tools/Signal_Review_v1_0/methods_spar_v1.json), [EEG comparison definitions](app/tools/Signal_Review_v1_0/methods_eeg_extensions_v1.json) and [physiology definitions](app/tools/Signal_Review_v1_0/methods_physiology_v1_1.json). Execution success is not physiological validity.

## Preservation and distribution

Both editions share the same application code. Public has no private AUL implementation; AUL remains a separate private-development edition. This build does not install either edition, migrate studies, publish a release, call a paid provider, modify hardware, replace Zuna or alter earlier release archives. Exact third-party notices remain separate from citations. Optional packages are downloaded during explicitly requested setup, not bundled environments.
