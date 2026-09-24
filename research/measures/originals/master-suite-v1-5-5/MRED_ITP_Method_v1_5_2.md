# MRED-ITP v1.5.2 - Information-Thermodynamic Proxy Layer

## Purpose
MRED-ITP adds two exploratory modules to the PR-AYC-G Master Comprehensive Suite:

- `ACG_v0.1` - Algorithmic Complexity Gate
- `OCU_v0.1` - Ocular-Cognitive Unloading

The layer tests whether MRED/NIP/TTI events show supportive information-structure and ocular-release patterns.

## Boundary
This is not a literal thermodynamic proof. Lempel-Ziv-style complexity is treated as an EEG compressibility/diversity proxy, not thermodynamic entropy or variational free energy. Fp1 blink timing is treated as an ocular event-boundary proxy, not proof of memory encoding. Without EOG or eye tracking, OCU is tentative.

## ACG_v0.1
For each predeclared or conceptually predeclared anchor, the module estimates an algorithmic complexity trajectory:

- `C_pre`: complexity before the anchor
- `C_peak`: complexity during the semantic-recognition window
- `C_post`: complexity during theta/integration follow-up

The core deltas are:

```text
delta_C_strike = C_peak - C_pre
delta_C_settle = C_post - C_peak
delta_C_post_pre = C_post - C_pre
```

The module computes a Complexity Settlement Index:

```text
CSI = 0.45*z(delta_C_strike) + 0.45*z(-delta_C_settle) - 0.20*z_positive(artifact_mean)
```

Interpretation:

- positive strike + negative settle can support a perturbation/settlement trajectory;
- persistent high complexity can indicate ongoing processing, artifact, or unresolved integration;
- low complexity can reflect drowsiness, flat signal, over-filtering, or true stabilization.

## OCU_v0.1
OCU estimates blink suppression and release around each anchor using Fp1 when EOG/eye tracking is not available.

```text
BR_pre     = blink rate from t_anchor -30s to -5s
BR_hold    = blink rate from t_anchor -5s to +5s
BR_release = blink rate from t_anchor +5s to +20s

BlinkSuppression = BR_pre - BR_hold
BlinkRelease     = BR_release - BR_hold
```

Ocular Release Index:

```text
ORI = 0.45*z(BlinkSuppression) + 0.45*z(BlinkRelease) - 0.25*z_positive(artifact_hold)
```

Interpretation:

- suppression during the anchor may index sustained visual/narrative attention;
- release after the anchor may index event-boundary transition or attentional release;
- Fp1 is not definitive; EOG or eye tracking should be used when available.

## Required inputs

```text
--xdf                  XDF file with EEG stream
--event-log            PRAYCG event log JSON/CSV
--feature-csv          Master Suite time-resolved feature frame
--annotation-csv       anchor/annotation window CSV
--mred-event-csv       CandidateLocal KHT-topo/MRED event table
--stream-inventory-csv optional corrected stream inventory for sample-index alignment
```

For Contact Run 1, the corrected inventory is important because raw XDF stream timestamps require sample-index alignment from the ALS pulse calibration.

## Outputs

```text
lz_complexity_timeseries.csv
acg_event_table.csv
blink_event_table.csv
ocu_event_table.csv
mred_itp_anchor_condition_windows.csv
mred_itp_anchor_summary.csv
mred_itp_condition_specificity.csv
mred_itp_visual_overlay.csv
mred_itp_phase_summary.csv
mred_itp_interpretation.json
```

## Visualizer
MasterSync Visualizer v1.3.2 recognizes:

```text
mred_itp_visual_overlay.csv
acg_event_table.csv
ocu_event_table.csv
mred_itp_anchor_summary.csv
```

Event categories:

```text
mred_itp
mred_itp_candidate
acg_complexity
ocu_blink_release
```
