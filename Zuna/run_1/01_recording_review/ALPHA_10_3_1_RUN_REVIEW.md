> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

# Your Zuna recording: Alpha 10.3.1 review

The recording is analyzable. The repaired Atlas hand-off completed both run-integrity QC and EEG signal QC, with **CAUTION**, rather than failing before analysis. This is not a declaration that the recording is artifact-free or that Zuna has been validated.

## What completed

- The original XDF was read without modification. Its SHA-256 remains `1937dad998f3cf265df32d3e235429a877b3f650f64c4ffde1b7e3d642b7c303`.
- The run is bound to UUID `RUN_1`. Atlas recorded completion; the original **BENCH / non-participant** designation remains unchanged.
- The recording contains 16 EEG channels and 84,886 EEG samples over about 679.64 seconds, plus ALS/AUX, Polar RR, Vernier respiration and markers.
- The overall marker-bounded Atlas interval is about 666.73 seconds, including instructions/confirmations. This is different from the ten minutes of scheduled calibration and eye-state content.
- Event QC found 79 timed rows in increasing recorded LSL order and one untimed pre-LSL authority row. It did not invent a timestamp for that row. A broad metadata scan also finds other identifiers; the governed run identity is recorded separately.
- EEG QC reported 10 gaps within its whole protocol-window scope under its frozen gap rule; the maximum interval was approximately 136 ms. Those findings are retained. A whole-run QC gap count is not the same as an endpoint-specific evaluation-block exclusion policy.
- The Vernier stream advertised 20 Hz but actually supplied approximately 10 Hz. The new bridge fixes buffered-sample handling and the default declaration for future recordings; it cannot recover samples discarded by the old bridge.

Latest local results:

- [Run-integrity report](alpha1031_trace_release_check/run_integrity_timing_qc_v0_1.json)
- [EEG QC, acquisition context and optional respiration findings](alpha1031_trace_release_check/eeg_signal_quality_v0_1.json)
- Private aligned EEG–belt plot (supporting file not included in this public copy)

The plot uses standardized one-second summaries, not raw EEG, a validated respiratory-band filter or cleaned data. Exclusions break the plotted traces. Its associations are descriptive and conditional on recorded-clock alignment; sensor/source latency is not established. It applies no inferred 1.33-second shift and must not be conflated with the earlier, separately documented clock-adjusted breathing investigation. Association cannot identify breathing as the cause of all drift or justify removing correlated activity.

## Zuna: prepared, awaiting confirmed physical wiring and reference

The software path is ready for an explicitly **post-hoc exploratory comparison**, separate from the original fixed-map endpoint. A private, hash-bound draft preserves the original contract, session classification, observed blocks and QC. Clock diagnostics were copied as an immutable historical snapshot because the old bridge was still running; it was not stopped or edited.

Private draft recipe (supporting file not included in this public copy) · Mapping review needing confirmation (supporting file not included in this public copy) · Snapshot ledger (supporting file not included in this public copy)

The draft deliberately has `confirmed: false`. The proposed channel-number order is:

`1 Fz; 2 Cz; 3 Pz; 4 F3; 5 F4; 6 C3; 7 C4; 8 P3; 9 P4; 10 T5; 11 T6; 12 O1; 13 O2; 14 T3; 15 T4; 16 Fp1.`

Please confirm that physical cap-to-board mapping, the reference connection used, and that no software all-channel common-average reference was applied before recording. “Usual PRAYCG wiring” and automatically generated labels do not by themselves resolve the conflicting original Zuna declaration. Do not edit the original files to make them agree.

After confirmation, the reviewed-copy route will:

1. Freeze the actual mapping/reference, retained-only reference rule, independent clock evidence and gap policy before looking at model errors.
2. Use all eight observed evaluation blocks, excluding calibration and the specified block-boundary intervals. A disallowed evaluation gap stops the recipe; no favorable blocks are silently selected.
3. Hide measured F3/F4/P3/P4 from both Zuna and the spherical-spline baseline. Held-out signals do not contribute to input referencing or normalization.
4. Compare both methods against the same measured targets with matched stated bandwidth, reporting RMSE/MAE/NMSE and secondary correlation. Targets may contain artifact; matching them does not establish clean neural reconstruction.
5. Preserve generated-channel labels, failures, timing, software/model identities, preprocessing, limitations and the comparison report for deliberate research-bundle inclusion.

## Software checks are not this recording's model result

The pinned real model completed short synthetic tests, including repeatability with the same seed on this machine and a generated-XDF-to-report smoke test. Those tests verify execution only. They are **not** a numerical assessment of your EEG, a full ten-minute model run, a fresh hardware acceptance test, or population-level scientific validation.

No actual-data Zuna-versus-spline accuracy result is claimed here. No current installation, original recording or saved session was changed by building Alpha 10.3.1. Install it into a separate folder after stopping acquisition safely and closing the old application.
