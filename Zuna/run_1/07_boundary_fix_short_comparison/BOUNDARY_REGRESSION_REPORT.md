> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Four fixed five-second contexts, not an independent recording or a full endpoint. See subsequent priority-status correction in prestart history.

# Boundary-safe preparation regression report

Status: **PASS — 198 synthetic engineering regression tests** in the installed Zuna numerical environment (NumPy 2.3.3, SciPy 1.16.2). No model inference, original recording changes, hardware access, or dependency installation.

## Numerical checks

- 38 new tests cover independent DC shifts through ±10,000,000 µV at 125/250/256/500 Hz, flat-constant rejection, 10/20 Hz amplitude and phase, discontinuities/nonfinite values, hidden-target isolation through token preparation, memory-layout independence, unchanged time grids, independent block processing, input nonmutation, overflow rejection, and explicit offline policy.
- Largest observed DC-translation difference: 1.74336634e-09 µV; fixed tolerance: 0.000002 µV.
- Largest 10/20 Hz interior gain deviation: 0.165763907%; fixed tolerance: 1%.
- Largest phase error: 6.29178289e-08 radians; fixed tolerance: 0.005 radians.
- 160 existing worker, adapter, Forge/workflow, integrity, and protocol tests passed; none skipped.
- Same five-second masks, sample counts, fractional source mapping, and interblock gaps were preserved in the tested synthetic fixtures.

## Failure addressed without relaxing tests

The first general-runtime suite run had 159 passes and one exact target-isolation assertion failure (maximum difference 2.51e-12 µV). It exposed reduction-order differences between C- and Fortran-contiguous input arrays. The candidate now normalizes memory layout before channel means; the exact assertion was retained and a dedicated layout regression added. All final pinned-runtime tests passed. The earlier failure is retained in existing_zuna_regressions.junit.xml.

## Scope and reproducibility

These checks establish stated numerical/integrity behavior, not scientific validity or a Zuna benefit. Full-block centering and zero-phase filtering are offline/noncausal. Linear endpoint padding does not eliminate every transient or the model's independent-window seams. Existing recorded QC and BENCH labels are unaffected.

`regression_gate.json` records tested source fingerprints and JUnit hashes. `boundary_regression_evidence_pinned.json` contains numerical measurements and dependency versions. Any candidate source change requires a fresh gate. The optional environment lacks pytest; pytest 8.4.2 was loaded read-only from the existing general environment after pinned Zuna dependencies, with plugin autoload disabled and numerical threads limited to two.
