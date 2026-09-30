> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

# PRAYCG Alpha 10.3.0 — Zuna bench-run review and patch recommendations

Reviewed 26 September 2026. Run `RUN_1`.

## Outcome

The runner completed, the sixteen-channel recording exists, and all eight evaluation blocks were recorded. The Analysis Forge's pre-start/incomplete classification is inconsistent with those artifacts. Its required QC never launched: an input-discovery error stopped it first.

The detailed 30-second preflight rejected a broad residual-amplitude measure, primarily sensitive here to slow, nonlinear drift. This supports redesigning the classifier and its explanation. It does not justify disabling transport, clipping, identity, timing or physical-safety checks.

A separate bridge timestamp defect and a protocol/stream electrode-map mismatch must also be corrected. No full Zuna inference or Zuna-versus-spline reconstruction comparison has been executed in this review. The raw data, application code and saved session records were not changed.

## Recorded evidence and descriptive signal audit

- XDF: `[LOCAL_PATH_REMOVED]`.
- SHA-256: `1937dad998f3cf265df32d3e235429a877b3f650f64c4ffde1b7e3d642b7c303` (unchanged before/after the audit).
- Seven recorded streams: EEG, ALS, analog auxiliary channels, OpenBCI status, StasisMarkers, Polar RR intervals, Vernier respiration. No Cerelog stream is present in this recording.
- EEG: 84,886 sixteen-channel samples across approximately 679.64 seconds; nominal 125 Hz.
- Timed protocol: 600.489 seconds from observed calibration onset to final evaluation offset. Calibration plus eight approximately sixty-second blocks completed; the runner state is COMPLETED and its process exit code is zero.
- 75,007 EEG sample rows fall within the recorded protocol timestamps; all values are finite. Effective rate over that span is approximately 124.91 Hz.
- Seven source-timestamp intervals exceed 20 ms, all in calibration by the recorded clocks; the largest is 136 ms. Bridge packet diagnostics also identify calibration anomalies. Each five-second-trimmed evaluation interval has uniformly approximately 8 ms source intervals. This alone does not establish accurate physical timing.
- A separate gap-aware descriptive 0.5–40 Hz filter gives channel standard deviations of approximately 6.47–37.89 microvolts. These are descriptive filtered amplitudes, not a validated quality grade.
- Native-rate 58–62 Hz power is approximately 0.023%–1.55% of measured 0.5–62 Hz power across channels. This is not a percentage of noise: large low-frequency power enlarges the denominator. It does not prove the signal is artifact-free.

Methods and exact per-channel/per-block measurements are retained in [recording_diagnostic_audit.json](recording_diagnostic_audit.json). The audit preserves native XDF timestamps without clock correction/dejitter, splits the main spectrum/filter analysis at intervals above 20 ms, and does not fill gaps. Software versions and the diagnostic script hash are recorded. Its outputs are private diagnostics, not replacements for Forge QC or acquisition evidence.

### Electrode-map conflict

The operator states that this run used the usual PRAYCG cap wiring, not a rewired Zuna montage. The bridge's hardcoded stream map is explicitly marked `channel_map_confirmed=False` and lists:

`Fz, Cz, Pz, F3, F4, C3, C4, P3, P4, T5, T6, O1, O2, T3, T4, Fp1`.

The Zuna contract instead assumes:

`Fp1, Fp2, C3, C4, P7, P8, O1, O2, F7, F8, F3, F4, T7, T8, P3, P4`.

Neither changing text labels nor confirming a preset changes electrode wiring. The numeric signal audit therefore identifies physical channels by number and retains both declarations. An exploratory channel-7/8 spectral contrast in the JSON must not be described as posterior O1/O2 activity while the maps conflict.

**Recommendation:** make the reviewed acquisition channel map the single source for bridge metadata, protocol compatibility, model coordinates and analysis. Support a separately reviewed Zuna benchmark profile for the usual PRAYCG montage, with actual available electrodes and prospectively chosen retained/held-out channels. Do not silently convert this run to the incompatible frozen profile. A revised analysis of this existing recording must be labeled post-hoc/exploratory; a later fresh recording can test the revised frozen profile.

## Why the 30-second test failed

| Attempt started, local | Detailed result | Score | Hard-flagged channels / 16 | Other timing finding |
|---|---|---:|---:|---|
| 08:20:12 | WARN | 88 | 3 | 125 Hz; no reported gaps |
| 08:21:47 | FAIL | 79 | 9 | 125 Hz; no reported gaps |
| 08:22:33 | FAIL | 69 | 14 | 125 Hz; no reported gaps |
| 08:23:41 | FAIL | 39 | 11 | 98.25 Hz; maximum gap 112 ms |
| 08:25:09 | FAIL | 57 | 14 | 121.75 Hz; maximum gap 88 ms |
| 08:27:28 | FAIL | 81 | 7 | 125 Hz; no reported gaps |
| 08:28:43 | FAIL | 68 | 14 | 125 Hz; no reported gaps |
| 08:29:42 | FAIL | 75 | 11 | 125 Hz; no reported gaps |
| 08:30:23 | FAIL | 81 | 8 | 125 Hz; no reported gaps |

Every hard channel flag in these captures was `high_residual_noise_scale`; there were no hard nonfinite, flat/disconnected or saturation flags. This reflects the current detector, not independent proof of electrode quality.

The classifier fits one straight line over an entire thirty-second channel, subtracts it, and computes the residual standard deviation. Above 150 microvolts produces a hard flag; more than four flagged channels among sixteen produces FAIL. The separate 0–100 score uses different rules, so a score of 81 can coexist with FAIL. No frequency-specific attribution or rolling-window aggregation is used for this hard flag.

In the final capture, the eight flagged channels had residual standard deviations around 196–322 microvolts. Using the same capture for an illustrative 0.5–40 Hz diagnostic filter produces approximately 9.4–49.9 microvolts across all sixteen channels; the robust sample-to-sample step scales are only approximately 3.5–7.6 microvolts. Five-second subdivisions also produce substantially smaller residuals. Together these support slow, non-straight-line drift as an important contributor, not a conclusion that all contamination is absent.

All nine generic full-profile reports were CAUTION, not FAIL. Routine warnings concerned device-specific checks that generic stream inspection had not performed; some also noted Polar RR outliers. The detailed EEG gate caused the repeated blocking.

### Recommended preflight redesign

1. Separate transport/identity integrity, amplitude saturation, flat channels, slow drift, mains contamination and analysis-band contamination.
2. Use a common, versioned quality engine for rolling and thirty-second displays. Aggregate short windows and show persistence, transient events, median and worst-window results; do not disguise them as an impedance percentage.
3. Make recoverable drift a clearly explained caution where appropriate for the intended analysis, rather than equating every broad residual-amplitude excess with unusable EEG. Validate thresholds on good and deliberately corrupted recordings before adopting replacements.
4. Retain hard stops for genuinely invalid identity/units/maps, missing required channels, sustained clipping/disconnection, invalid timestamps and applicable physical-safety restrictions.
5. Expose exact failed channels and numbers beside the overall status. A warning should explain whether acquisition can proceed with acknowledgment and which later analyses may be affected.
6. Do not require optional Polar/Vernier/Cerelog evidence for a protocol's EEG-only scientific endpoint unless the protocol actually depends on it. Still enforce applicable safety rules for every connected device.
7. Preserve preflight history. Toggling bench mode currently resets a freshness epoch and can misleadingly turn already-run evidence into 'has not run' or 'stale'. Invalidate by relevant configuration/source changes, not an unexplained blanket reset.

## Bridge timing and ALS diagnosis

The ALS test passed at approximately 08:27 after the bridge restart. Earlier MISSING results contained approximately 750 finite samples, but no samples in the expected display phase windows. They were not evidence that no sensor samples existed.

Reconstructing the prior bridge epoch from saved chunk diagnostics indicates timestamps roughly seven seconds ahead of host time during those failures. The optical sequence was only 4.75 seconds long, explaining why phase windows could be empty. This is an inference from bridge diagnostics because the barcode receipt did not preserve raw sample timestamps. The reported loose ground may also have affected the sensor; these logs cannot exclude that.

For the final bridge epoch used in the run, the offset was smaller but remained significant: approximately 1.309–1.366 seconds ahead of host chunk time during the eight evaluation blocks. The first-to-last block-onset estimates were approximately 1.313–1.353 seconds. These are reconstructed software-clock offsets, not calibrated physical acquisition latency. All calibration packet anomalies occur outside the later evaluation interval, but that does not erase the remaining offset.

**Recommendation:** repair timestamp reconstruction and anomalous packet handling, retain per-segment clock evidence, and test prolonged operation/restarts/stalls/duplicates/reordering. Do not simply clamp or overwrite historical timestamps. Any offline correction must be a separately versioned derivative with an explicit method and uncertainty.

ALS results should distinguish missing samples, weak optical contrast and invalid clock alignment. Save per-phase sample counts and source/host timestamp comparisons. LSL synchronization does not by itself correct arbitrary device buffering or incorrectly generated source timestamps; see [LSL timing guidance](https://labstreaminglayer.readthedocs.io/info/time_synchronization.html).

## Why Analysis Forge does not run QC

The required-QC snapshot reports `INPUT_ERROR: run_state_manifest is missing` and has an empty execution-receipt list. No required-QC subprocess launched.

Three compatibility defects are confirmed:

1. Atlas writes `*_run_state.json`; Forge discovery expects `*run_state_manifest.json`. The finalized session lock already records the correct Atlas artifact path and hash. Resolve and validate that typed evidence; do not rename the original file.
2. The analysis-window parser expects `PROTOCOL_SEQUENCE_START/END`; Atlas emits `ATLAS_PROTOCOL_START/END`. It therefore incorrectly classifies the completed XDF as a PRESTART_FRAGMENT. Resolve boundaries according to protocol/runner schema, matching run UUID and unique recorded events. For Zuna scoring, retain its observed calibration/evaluation boundaries.
3. Generic event QC does not recognize the Atlas event timestamp fields. Add schema-aware event-time interpretation without pretending a pre-LSL authority record has an LSL timestamp.

After those repairs, the current Zuna preparation function still refuses any interval over 2.5 sample periods (20 ms at 125 Hz) anywhere in the selected continuous span. This run's early calibration gaps trigger it. Introduce a reviewed gap-aware approach that independently processes valid contiguous intervals, excludes unsuitable windows/edges and preserves coverage/missingness. Do not interpolate through unknown gaps or present a changed analysis policy as the original frozen benchmark.

The existing BENCH_TEST and participant-ineligible records must remain preserved. Technical/descriptive analysis should be available without falsely promoting the session to a validated participant study.

## Mixed OpenBCI and experimental Cerelog

There is no blanket backend prohibition on combining carried and experimental routes. Two separate issues affect the requested combination:

- Experimental Cerelog currently has a no-participant evaluation restriction, applied through profile/session-wide admission rules. Prior successful use of OpenBCI does not remove Cerelog's separate restrictions.
- Both OpenBCI+ALS and Cerelog+ALS declare a primary ALS source. The backend supports primary/supplemental assignments, but the UI does not expose or submit the required choice. This is a concrete composition defect.

**Recommendation:** permit composition with per-device evidence/status and an explicit primary timing-source selector. Keep OpenBCI as primary EEG and its ALS as primary timing when selected; retain Cerelog EMG/EOG/ALS as separately identified supplemental streams. Preserve which analyses used each stream and their limitations. Do not silently grant participant-use clearance to experimental hardware.

The shipped Cerelog route requires off-body evaluation; a successful stream or barcode test is not an electrical-safety assessment. A later review must establish the exact firmware, wiring, power/isolation configuration, calibration and intended participant use before its authorization changes. Do not bypass that boundary by calling an on-body experimental recording 'bench'.

## Two ALS-PT19 sensors

Use separate per-sensor test rows and receipts:

- OpenBCI ALS: its exact run-bound ALS outlet.
- Cerelog ALS: `CerelogV1ALS`, the single-channel outlet derived from physical ADC channel 5 in the current exact-firmware route.

Each receipt must bind the device/module, connector configuration, run, source/outlet instance, channel and profile. Test each sensor independently, retaining both results. Invalid channel selection must fail explicitly rather than falling back to another channel.

Add a different **paired timing** test in which both sensors observe a common screen sequence simultaneously. Analyze matching physical transitions, offset, jitter, missed edges and drift over repeated measurements. Use colocated sensors or controlled display geometry to avoid conflating screen scanout position with device delay. A placement/brightness pass must not be labeled cross-device synchronization.

## Other issue identified

The recorded Vernier outlet declares 20 Hz but supplies approximately 10 Hz. Today's generic preflights saw approximately 10 Hz and did not fail for that reason. Reconcile the saved profile, publisher metadata and actual rate; do not treat this as an EEG-quality failure or invent missing respiration samples solely from the inconsistent nominal metadata.

## Recommended next patch order

1. Fix Atlas-to-Forge run-state, boundary and timestamp compatibility; add this completed bench run's formats to regression coverage.
2. Repair bridge clock discipline and ALS clock diagnostics; prove behavior under packet anomalies and long-running streams.
3. Unify and validate electrode-map ownership; add a reviewed Zuna profile for the actual PRAYCG wiring.
4. Redesign the preflight hard/advisory distinction and shared quality display; retain integrity/safety checks.
5. Add reviewed gap-aware analysis, preserving this run and all original exclusions/bench status.
6. Expose mixed-profile primary/supplemental selection, separate device statuses, and independently bound dual-ALS receipts plus a paired timing test.
7. Reconcile Vernier rate metadata and improve clear partial-run/diagnostic reporting.

Then reanalyze this existing recording under an explicitly revised diagnostic recipe and run a fresh end-to-end validation against the corrected frozen setup. There is no basis to discard the current recording or declare the cap unusable from these failures alone; there is also no completed model-validation result yet.

## Principal evidence locations

- Run artifacts: `[LOCAL_PATH_REMOVED]`.
- Saved QC failure: `[LOCAL_PATH_REMOVED]`.
- Incorrect composite classification: same workspace `analysis_inputs\[PRIVATE_ID_REMOVED]\composite_run_manifest_RUN_1.json`.
- Installed application reviewed: `[LOCAL_PATH_REMOVED]`.
- Preflight algorithm: `control_center/scripts/praycg_acquisition_preflight_v1_0.py`, channel metrics and classification.
- Bridge clock algorithm: `tools/Acquisition/praycg_acquisition_diagnostics_v1_0.py`, `reconstruct_lsl_timestamps`.
- Forge integration: `control_center/scripts/praycg_active_context_v1_0.py`, `praycg_analysis_window_v1_0.py`, main Control Center analysis artifact binding, and the run-integrity QC timestamp parser.
- Hardware composition: `platform_core/praycg_platform_core_v1_0_alpha_4.py`, `tools/Hardware_Workflow_v0_1/praycg_hardware_workflow_v0_1.py`, and the main Control Center's profile builder/ALS launcher.
