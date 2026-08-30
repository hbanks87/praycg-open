# OCM_v0.2 - Raw-XDF Quarter-Second Override Cue Microstate Analysis

This patch adds a standalone raw-XDF re-extraction path for OCM. The older OCM_v0.1 layer could operate on two-second feature tables, but those tables are too coarse for the 0.85-second number cue used in PR-AYC-G.

## Purpose

OCM_v0.2 tests whether Contextual Override produces repeated cue-locked microstates:

- digit / cue recognition during the visible cue window;
- working-memory update after the cue disappears;
- running-sum maintenance before the next cue.

## Default windows

For cue onset `t_i`:

```text
Pre-cue baseline:       t_i - 0.75 to t_i
Digit recognition:      t_i + 0.10 to t_i + 0.85
Working-memory update:  t_i + 0.85 to t_i + 2.25
Maintenance:            t_i + 2.25 to t_i + 3.00
```

The microbin table is extracted in 0.25-second bins from -0.75 to +3.0 seconds relative to cue onset.

## Signals

The patch uses continuous bandpass envelope proxies from raw EEG rather than independent 0.25-second Fourier PSD estimates. This is important because 0.25 seconds is too short for a stable standalone theta FFT estimate. Theta is therefore interpreted only after aggregation across the update and maintenance windows.

Default proxies:

```text
task gamma:       35-40 Hz frontoparietal lower gamma
task theta:        4-8 Hz frontal/frontoparietal theta
visual gamma:     30-45 Hz visual-control gamma
artifact score:   jaw-temporal HF + global p2p proxy
```

## Claim boundary

OCM_v0.2 is an exploratory cue-task analysis. It does not prove narrative meaning, memory encoding, OSM, hidden-Y biology, or human EEG mechanism. It tests whether the Override branch fractures cognition into repeated cue recognition and working-memory update cycles.
