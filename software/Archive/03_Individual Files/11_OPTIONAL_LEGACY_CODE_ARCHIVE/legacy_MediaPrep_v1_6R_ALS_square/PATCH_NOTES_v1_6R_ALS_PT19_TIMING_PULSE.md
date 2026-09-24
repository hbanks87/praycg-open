# Patch Notes — PRAYCG MediaPrep v1.6R ALS-PT19 Timing-Pulse Patch

## Purpose

v1.6R adds a small black/white hardware timing square for an ALS-PT19, photodiode, or photoresistor-style sensor. The square is intended to be taped over and recorded through OpenBCI analog AUX / Analog Read, giving a physical display-timing trace in the XDF.

## Why this patch exists

Software LSL markers tell the analysis when PsychoPy intended a video to start. The ALS-PT19 timing square tells the analysis when the monitor physically changed. This reduces ambiguity around video onset, cue timing, display lag, and dropped-frame concerns.

## Core implementation decision

The timing square is added after the Control branch is generated. This preserves the existing PR-AYC-G rule that Control is generated from the cue-embedded Target while also giving Target, Override, and Control identical readable timing pulses.

Pipeline:

```text
clean master, optional
-> number-cued Target working video
-> phase-scrambled Control working video from number-cued Target
-> render ALS timing square into Target
-> copy Target to Override
-> render ALS timing square into Control
```

## Default pulse mode

Default:

```text
video_start
```

This renders a 1-second white pulse at the start of each video and black otherwise. This is the recommended acquisition setting.

Optional:

```text
cue_start
both
```

These modes pulse at every number-cue onset and should be used mainly for hardware-validation runs.

## New manifest fields

```text
sensor_timing_design
sensor_timing_pulse_events
sensor_timing_render_summary
```

## New QC checklist

```text
ALS_PT19_SENSOR_TIMING_QC_CHECKLIST_v1_6R.md
```

## Boundary

The ALS timing square is not a biological measurement. It validates stimulus timing and belongs to the media/input-control layer.
