# MRED-Peak and MRED-Resolution Method v1.5.5

## Status

This is an endpoint-compression layer for PRAYCG. It does not replace A-MRED, MRED, NIP, TTI, NUPI, CET-R, or the visualizer. It organizes them into a simpler interpretive distinction.

## Core distinction

**MRED-Peak** asks whether a predeclared anchor produced an acute Target-specific meaning event:

- meaning recognition / semantic strike,
- delayed theta/topological integration,
- Target greater than Control,
- Target greater than Override,
- artifact/confound/timing gates passed.

**MRED-Resolution** asks whether a predeclared anchor produced a delayed reflective or regulatory after-state:

- Target echo into washout or Baseline 2,
- NUPI/RDI recovery profile,
- EET state-vector resemblance,
- self-report afterglow/echo support,
- autonomic/respiratory recovery where available.

## Intended use

Use this layer to simplify the Master Suite into a readable endpoint structure:

```text
BOXED PRIMARY PATH:
  Timing/QC + StimulusFingerprint/CET-R + artifact/confound gates
  -> A-MRED / MRED-Peak-Resolution

SECONDARY:
  NIP/BIT/CII/IAQ
  TTI
  NUPI

EXPLORATORY / CONVERGENCE:
  KHT-topo
  NAST
  EET
  MRED-ITP / ACG / OCU
  OCM025 / RSM / CVB / SquintProxy
  LSO / Subtitle Override when applicable
```

## Output files

The module writes:

```text
mred_peak_resolution_anchor_table.csv
mred_peak_resolution_run_summary.csv
top_mred_peak_candidates.csv
top_mred_resolution_candidates.csv
mred_peak_resolution_visual_overlay.csv
mred_peak_resolution_interpretation.json
mred_peak_resolution_report.md
```

## Claim boundary

A MRED-Peak pass is not proof of memory formation. A MRED-Resolution candidate is not proof of healing, replay, or OSM biology. This layer compresses existing proxy outputs into a clearer review table.
