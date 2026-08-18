# PRAYCG1.8 Patch Notes

## Reason for update

PRAYCG1.8 adds an explicit delayed comparison / reflection state after the standard PR-AYC-G sequence. This captures a post-run physiological window after the participant has completed all three branches and had a chance to compare them internally.

The update is methodologically useful because the post-video washout is not always where narrative integration appears. A delayed reflection baseline may capture residual integration, rebound, or comparative appraisal after the Target and Override have both been experienced.

## New phase markers

```text
BASELINE_2_REFLECTION_INSTRUCTION_START / END
BASELINE_2_REFLECTION_PRE_START_STILLNESS_START / END
BASELINE_2_REFLECTION_START / END
FINAL_MASTER_REPORT_START / END
FINAL_MASTER_REPORT_CONTROL_START / END
FINAL_MASTER_REPORT_TARGET_START / END
FINAL_MASTER_REPORT_OVERRIDE_START / END
FINAL_FROZEN_NOTE_CONTROL_START / END
FINAL_FROZEN_NOTE_TARGET_START / END
FINAL_FROZEN_NOTE_OVERRIDE_START / END
```

## New config fields

```text
enable_final_reflection_baseline: true/false
final_reflection_baseline_seconds: default 120
movie_display_mode: safe_fit/native/fit/custom
movie_safe_fit_fraction: default 0.92
movie_custom_width_px: 0 unless custom mode is used
movie_custom_height_px: 0 unless custom mode is used
```

## Display-safe cue handling

This update does not alter cue rendering inside the media files. It changes only the display size of the entire stimulus movie during playback. This is a presentation-layer fix for laptop scaling/cropping/edge-position issues.

For true cue-position changes, use MediaPrep settings, not the protocol runner.

## Epistemic status

The final reflection baseline is exploratory until enough runs establish its stability. It should be reported as a delayed reflection / comparative appraisal window, not a neutral physiological baseline.
