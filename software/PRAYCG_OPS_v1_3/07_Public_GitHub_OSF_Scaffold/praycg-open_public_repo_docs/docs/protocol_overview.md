# PR-AYC-G protocol overview

## Purpose

PR-AYC-G is designed to test whether narrative meaning produces measurable physiological and EEG-state changes beyond matched audiovisual stimulation and analytic task stance.

## Standard three-arm stimulus suite

| Arm | Stimulus | Subject stance | Primary question |
|---|---|---|---|
| Control | Phase-scrambled version of the cue-embedded Target | Watch normally | Is the response just light, sound, motion, cuts, or audio pacing? |
| Target | Intact meaningful narrative | Watch naturally and allow the story to land | What happens when meaning is accessible? |
| Contextual Override | Same intact narrative as Target | Perform analytic task, such as summing number cues | Does the same stimulus change when the viewer is measuring instead of receiving? |

## Critical media rule

Target and Contextual Override should be generated from the same cue-embedded video. Only instructions should differ. The phase-scrambled Control should be generated from the cue-embedded Target so cue timing and low-level cue energy are represented in the control branch.

## Current PRAYCG1.8B sequence

```text
SETUP / stream preflight
BASELINE_1
CONTROL_1
WASHOUT_1
CONTROL_1_AFTER_WASHOUT_1 subjective report
TARGET_1
WASHOUT_2
TARGET_1_AFTER_WASHOUT_2 subjective report
CONTEXTUAL_OVERRIDE_1
WASHOUT_3
OVERRIDE_1_AFTER_WASHOUT_3 subjective report
BASELINE_2_REFLECTION instruction
spacebar proceed
stillness settle
BASELINE_2_REFLECTION
FINAL_MASTER_REPORT
typed scene-level frozen notes
END
```

## Final reflection baseline

`BASELINE_2_REFLECTION` is not a neutral baseline. It is a post-exposure comparative reflection state. It should be analyzed as:

```text
post-protocol integration / comparison physiology
```

not as clean pre-exposure rest.

## Predeclared anchors

PRAYCG1.8B supports predeclared media-structural anchors. These replace retrospective human timestamp guessing.

The principle is:

```text
Freeze the scene. Do not ask the absorbed subject to be the stopwatch.
```

Anchor files may define:

```text
anchor_id
stimulus_id
source
condition_scope
rendered_time_sec
pre_window
expected_peak_search_window
theta_carryover_window
claim_level
description
```

## Self-report role

Self-report is an independent evidence stream. It should identify experience, scene, meaning, absorption, task effort, discomfort, and confidence. It should not be treated as proof of a physiological mechanism.

## Minimum run artifacts

A public-safe run should preserve:

```text
event log JSON/CSV
run config JSON
channel map CSV
cue schedule JSON/CSV
media manifest / hashes
QC checklists
XDF or deidentified feature outputs when permitted
analysis outputs
run notes
```
