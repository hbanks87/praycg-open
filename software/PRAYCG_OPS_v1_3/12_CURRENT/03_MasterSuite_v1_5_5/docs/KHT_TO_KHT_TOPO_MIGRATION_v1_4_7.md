# K_HT to K_HT-topo Migration Note

This package preserves legacy output names for compatibility, while updating interpretation.

## Legacy name

`K_HT` remains in some CSVs and figures because existing reports, scripts, and visualizer overlays depend on that column name.

## Updated interpretation

When produced from human PR-AYC-G data, interpret the value as:

\[
K_{HT-topo}=\sqrt{|\eta_{HT}\zeta_{HT}|}
\]

not as cellular OSM.

## Practical convention

- Column names may include both `K_local` and `K_HT_topo`.
- Report text should use `K_HT-topo`.
- `K_OSM` is reserved for future direct mechanism evidence.

## Event-lock rule

A topological event is not locked by K alone. It requires:

1. elevated local \(K_{HT-topo}\);
2. theta or topological carryover;
3. Target specificity over Control and Override;
4. artifact and timing pass;
5. confound registry pass or explicit caveat.
