# A-MRED v1.5.3 — Anchor-Locked MRED Primary Endpoint

A-MRED compresses the current PR-AYC-G analysis workbench into a cleaner primary endpoint.

## Endpoint definition

For a predeclared media anchor `j`, A-MRED asks whether Target shows both:

```text
MR  = meaning-recognition / semantic-affective recognition
ENC = delayed theta/topological integration or carryover
```

and whether those values exceed both Control and Override after QC and confound gates.

## Strict gate

```text
A-MRED_j = 1 only if:
  1. Anchor was locked before acquisition.
  2. Target MR_j exceeds threshold.
  3. Target ENC_j exceeds threshold in a predeclared delayed window.
  4. Target MR_j exceeds Control and Override by margin.
  5. Target ENC_j exceeds Control and Override by margin.
  6. Artifact/confound gate passes.
  7. CET-R/stimulus-regressor correction does not explain the event when available.
  8. Self-report does not contradict the intended state.
```

Formula:

```text
A-MRED_j =
  1[MR_T,j > theta_MR]
  * 1[ENC_T,j > theta_ENC]
  * 1[MR_T,j > MR_C,j + delta]
  * 1[MR_T,j > MR_O,j + delta]
  * 1[ENC_T,j > ENC_C,j + delta]
  * 1[ENC_T,j > ENC_O,j + delta]
  * 1[QC_j = PASS]
```

## Continuous backup score

```text
MREDScore_j = MR_j * ENC_j * QC_j
DeltaMRED_j = MREDScore_T,j - max(MREDScore_C,j, MREDScore_O,j)
```

## Interpretation boundary

A-MRED is a human-scale psychophysiology endpoint. It does not prove OSM biology, microtubules, biophotons, hidden cellular Y, consciousness, or memory formation. Failure to pass A-MRED does not prove that the event was meaningless; it means the event did not pass the operational recognition-plus-integration gate.
