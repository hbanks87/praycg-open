> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Stopped before any model context because priority verification failed; later attempt completed separately.

# Full corrected comparison: boundary preflight

Status: **PASS**.

Read-only engineering audit; no model inference, source/recording changes, or dependency installation.

- Prior 198-test regression gate, frozen candidate sources, original recording/report/recipe/derivatives, and corrected prepared arrays verified unchanged.
- Historical whole-block comparison filtering and all eight-block metrics reproduced within predeclared tolerances. Original 102,456 scored samples, timestamps and masks are unchanged.
- Independent-block and branch filter isolation, finite outputs, deterministic repeat, and nonfinite rejection passed.
- Terminal context lengths: [7, 7, 3, 5, 7, 7, 5, 5] real samples, each reflected to 128 model samples. No tail itself is directly scored.
- Replacing only cached historical terminal predictions with the preceding value changed scored filtered signals by at most 12.193367 µV. A fixed +1 µV tail shift propagated at most 0.00104733031 µV into scoring.

## Interpretation

The existing zero-phase comparison filter permits backward effects from excluded terminal samples. In the historical output these effects can be material: the tiny-tail replacement sensitivity reached 12.19 µV in scored samples, despite the five-second guard. The audit quantifies this rather than claiming the guard guarantees zero influence. Tail interventions are diagnostic copies, not model reruns or modified full-run endpoints. Retain the original endpoint for the corrected comparison and disclose padding, seams, filtering and post-hoc BENCH limitations. Repeat this diagnostic on the corrected model output before interpreting its result; the corrected output does not yet exist at this preflight stage.

Engineering PASS is permission to evaluate the frozen corrected candidate, not evidence of a scientific benefit.
