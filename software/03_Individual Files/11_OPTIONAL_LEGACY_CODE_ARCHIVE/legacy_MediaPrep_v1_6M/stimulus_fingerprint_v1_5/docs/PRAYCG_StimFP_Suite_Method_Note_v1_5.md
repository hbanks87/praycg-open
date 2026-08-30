# PRAYCG StimulusFingerprint Suite v1.5 Method Note

## Purpose

StimulusFingerprint v1.5 is an offline media quality-control suite for PR-AYC-G. It standardizes stimulus QC before acquisition by analyzing the Control, Target, and Contextual Override MP4 files in one execution.

## What it measures

The suite estimates digital sensory-delivery properties:

- duration, FPS, resolution
- mean luminance and luminance dynamics
- frame-to-frame visual change
- estimated cut rate
- flash-risk proxy
- digital audio RMS / dBFS
- audio silence fraction and dynamic range
- audio envelope rhythm concentration
- cue visibility for number-cue schedules
- physical match across condition pairs

## What it does not measure

It does not measure literal photons, true sound pressure level, semantic meaning, empathy, consciousness, or stimulus beauty. It categorizes the physical vehicle, not the inner event.

## Why this matters for PR-AYC-G

PR-AYC-G requires separating sensory delivery from meaning and task stance. A useful stimulus suite should prevent the simplest objection: that any physiological or EEG pattern came from brightness, cuts, audio rhythm, cue visibility, or physical mismatch rather than the intended experimental state.

## Cue visibility

The suite uses the number-cue schedule JSON to estimate whether each cue was functionally visible. A cue can exist in the MP4 but be difficult to decode if local background contrast is poor. The suite writes `cue_visibility_qc.csv` for Target and Override when a cue schedule is supplied.

## Suggested interpretation thresholds

These thresholds are practical QC flags, not statistical laws:

- Target vs Override identical hash: ideal for cue-embedded override suites.
- Target vs Override physical match >= 90: excellent.
- Target vs Control physical match >= 80: useful; inspect individual channels.
- Target vs Control physical match 70-80: pilot-usable with caution.
- Target vs Control physical match < 70: major control-matching concern.
- Low-visibility cue fraction >= 5%: inspect cue windows.
- Low-visibility cue fraction >= 10%: regenerate cue overlay with stronger contrast.

## Recommended report language

"StimulusFingerprint v1.5 was used to quantify digital sensory-delivery proxies and physical matching across Control, Target, and Contextual Override media. These metrics do not measure meaning directly. They are used to evaluate exogenous entrainment and cue-decoding confounds before physiological interpretation."
