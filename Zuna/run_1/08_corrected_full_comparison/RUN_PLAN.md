> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Final corrected full Run 1 comparison. The two-sample eyes-closed/early/proxy-touched subgroup is insufficient for interpretation; historical numeric values are preserved with this warning.

# Full corrected Zuna comparison — private development study

The installed Workbench and integration patch are deliberately unchanged. This
comparison uses the isolated, regression-tested candidate on the existing real
hardware recording. Its historical BENCH/QC designation is retained; BENCH does
not mean that the EEG recording is synthetic.

## Scope committed before inference

- One fresh execution on all eight original evaluation blocks. Calibration is
  excluded as in the original recipe. The grid has 122,926 samples at 256 Hz;
  102,456 samples (400.21875 sample-equivalent seconds) remain in the original
  scoring mask. No blink-proxy flag adds an exclusion.
- Same 12 retained electrodes, four hidden electrodes, reviewed wiring,
  reference, template coordinates, pinned model weights, 16 steps and original
  context seeds. Two CPU threads at below-normal priority. Expected 104 contexts,
  including eight short reflected terminal contexts.
- Primary: mean per-electrode normalized squared error after the historical
  whole-block common comparison filter. Pooled RMSE and all per-channel/per-block
  metrics accompany it.
- Mandatory companion: the same metrics and mask on precomparison arrays,
  before the final common filter. Both scoring views are reported regardless of
  which favors Zuna. They are not competing candidates from which to select a
  preferred answer.
- Frozen descriptive groups: eye condition; [5,20) seconds versus second 20
  through the original eligible endpoint; historical retained-Fp1 proxy flags
  and unflagged windows. These are imperfect labels calculated on the previous
  preparation, not verified blinks or clean-signal labels.
- Spectral estimates use complete two-second Welch windows inside contiguous
  eligible spans, never artificial joins across excluded samples or blocks.
- Report waveform/amplitude agreement, frequency content, eye-condition
  differences, actual model seams, runtime and all failures/limitations.
- Repeat the fixed terminal-output sensitivity diagnostic on a copy: replace
  only the tiny generated terminal tail by its preceding generated value,
  reapply the declared comparison filter, and measure effects inside the
  original scoring mask. This diagnostic never replaces the primary result.

## Integrity and stopping rules

`full_comparison_plan.json` is the final machine-readable freeze record. It binds
the original data, recipes, prior results, corrected preparation, regression
evidence, source files, masks and execution/report scripts before inference.
Any binding mismatch stops completion. A fresh exclusive execution claim and
checkpoint identity prevent accidental duplicate launches or cache mixing.

Execution has a three-hour cooperative safety deadline, not a performance
promise. Cancellation finishes at a safe model boundary. Checkpoints and failure
records are preserved. There is no automatic retry, settings change, seed search
or deployment. A separately authorized resume would require matching identities.

Successful inference is not yet scientific verification: the completion record,
all 104 outputs, eight blocks, original input/source bindings and saved-array
metrics must be checked before accepting the interpretation report.

## Interpretation limits

This recording is development data, not a new prospective validation. Hidden
measured electrodes may contain artifact and are not clean neural ground truth.
The old and corrected pipelines have different prepared targets, so absolute
old/new error changes are not isolated changes in model accuracy. Compare Zuna
with interpolation within each pipeline. Eye-state timing is approximate,
template coordinate clipping remains disclosed, and processing is offline and
noncausal. A lower reconstruction error does not demonstrate blink removal,
clinical usefulness or live-decoder readiness. No favorable result is required
for the engineering correction to be worthwhile.

All outputs remain private. No original recording is edited or uploaded.
