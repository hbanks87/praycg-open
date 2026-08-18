# OCM_v0.1 - Override Cue Microstate Analysis

OCM analyzes the repeated upper-right number cues during Contextual Override. It asks whether the override task creates cue-locked digit-recognition and working-memory update microstates.

## Cue windows

For cue onset `t_i`:

```text
W_pre   = [t_i - 0.75, t_i]
W_rec   = [t_i + 0.10, t_i + 0.85]
W_upd   = [t_i + 0.85, t_i + 2.25]
W_maint = [t_i + 2.25, t_{i+1}]
```

## Scores

```text
DR_i    = mean(TaskGamma, W_rec) - mean(TaskGamma, W_pre)
WMU_i   = mean(TaskTheta, W_upd) - mean(TaskTheta, W_pre)
MAINT_i = mean(TaskTheta, W_maint) - mean(TaskTheta, W_pre)
```

Where:

- `DR_i` is digit-recognition / cue-detection proxy.
- `WMU_i` is working-memory update proxy.
- `MAINT_i` is inter-cue maintenance proxy.

## Specificity checks

The module compares:

```text
Override cue response - Target matched cue response
Real cue response - pseudo-cue response
WMU_i ~ cue_index / running_sum / value / artifact
```

## Boundary

OCM is not interpreted as narrative meaning encoding. In existing 2-second feature tables, sub-second cue dynamics are coarse and exploratory. A stronger implementation should rerun from raw XDF with 0.25-0.5 second windows and EOG/EMG checks.
