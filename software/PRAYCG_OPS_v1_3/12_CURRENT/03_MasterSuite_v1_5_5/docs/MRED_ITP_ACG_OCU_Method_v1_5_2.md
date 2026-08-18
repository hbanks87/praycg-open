# PRAYCG Master Suite v1.5.2 - MRED-ITP / ACG / OCU Method

## Purpose

`MRED-ITP_v0.1` adds an information-thermodynamic proxy layer to PR-AYC-G. It tests whether MRED/NIP/TTI events show structured changes in algorithmic complexity and blink/ocular-release timing.

This module does **not** prove literal thermodynamic entropy reduction, memory encoding, OSM biology, microtubules, biophotons, or hidden-Y biology.

## Submodules

### ACG_v0.1 - Algorithmic Complexity Gate

ACG estimates whether a predeclared or future-freeze event shows:

1. complexity perturbation around recognition / semantic strike;
2. complexity settlement after the event;
3. acceptable artifact burden.

Raw EEG form:

```text
C_LZ(t) = normalized Lempel-Ziv complexity of symbolic EEG state sequence
Delta_C_strike = C_LZ_peak - C_LZ_pre
Delta_C_settle = C_LZ_post - C_LZ_peak
ACG_gate = strike_gate AND settle_gate AND artifact_gate
```

The default raw path excludes the Fp1 blink sentinel and T3/T4 jaw sentinels from the complexity estimate when the PRAYCG16 channel map is available.

Feature-level fallback:

```text
FEATURE_LEVEL_PROXY_NOT_RAW_EEG_LZC
```

### CSI_v0.1 - Complexity Settlement Index

```text
CSI = z(Delta_C_strike) + z(-Delta_C_settle)
```

CSI is a proxy for perturbation-followed-by-settlement. It is not thermodynamic entropy.

### OCU_v0.1 - Ocular-Cognitive Unloading

OCU estimates whether blink/ocular proxy events show attention-hold and post-event release:

```text
BlinkSuppression_proxy = baseline_rate - hold_window_rate
BlinkRelease_proxy = release_window_rate - hold_window_rate
OCU_gate = suppression_gate AND release_gate AND artifact_gate
```

With true EOG or eye tracking, OCU can be a blink-timing module. With Fp1 only, it is a blink-proxy module:

```text
RAW_FP1_BLINK_PROXY_NOT_CONFIRMED_EOG
```

With only feature tables, it becomes a still weaker p2p/global artifact proxy.

### ORI_v0.1 - Ocular Release Index

```text
ORI = scaled(BlinkSuppression_proxy + BlinkRelease_proxy)
```

ORI is a candidate attention-release marker, not proof of memory encoding or buffer dumping.

## Required inputs

```text
--xdf              raw XDF, recommended
--event-log        PRAYCG event log with branch markers
--feature-csv      Master Suite time-resolved feature frame
--annotation-csv   anchor/annotation windows
--mred-event-csv   CandidateLocal KHT-topo/MRED event table
--out-dir          output analysis folder
```

## Outputs

```text
lz_complexity_timeseries.csv
blink_event_table.csv
acg_event_table.csv
ocu_event_table.csv
mred_itp_anchor_condition_windows.csv
mred_itp_anchor_summary.csv
mred_itp_condition_specificity.csv
mred_itp_phase_summary.csv
mred_itp_visual_overlay.csv
mred_itp_interpretation.json
```

## Interpretation boundary

A positive ACG or OCU result supports an information-structure or ocular-release **proxy**. It must be interpreted with MRED, NIP, TTI, artifact controls, condition specificity, ALS timing, and self-report. A negative result does not prove that no memory or meaning occurred; it only means the module did not detect its operational signature under the available measurement path.
