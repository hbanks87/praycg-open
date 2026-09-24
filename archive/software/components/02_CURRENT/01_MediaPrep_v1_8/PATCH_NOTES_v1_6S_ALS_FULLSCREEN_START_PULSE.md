# Patch Notes — PRAYCG MediaPrep v1.6S

## Purpose

v1.6S replaces the fragile small-corner ALS timing square default with a robust full-screen start pulse.

The Her v1.6R stimulus used a lower-right 38 × 38 px square. That worked at the media-prep level, but it made acquisition vulnerable to small placement errors. v1.6S solves that by making the physical timing marker visible to the ALS-PT19 from anywhere on the active display area.

## New default

```text
sensor_pulse_mode = fullscreen_start
sensor_video_start_duration = 0.75 sec
sensor_fullscreen_black_guard = 0.50 sec
```

Final video timing:

```text
white pulse -> black guard -> original content
```

## Critical cue-schedule correction

Because the full-screen pulse is prepended after cue rendering, all cue start/end times are shifted by the prefix duration in the final `cue_schedule_<project>_v1_6S.json/csv`.

The original content-time cue positions are preserved as:

```text
content_start_sec
content_end_sec
```

The final `start_sec` and `end_sec` values are the values the protocol runner should use.

## Audio correction

Original audio is delayed by the same prefix duration so content audio begins when content video begins. The white/black timing prefix is silent.

## Boundary

The full-screen flash is an instrument marker. It validates screen timing and belongs to `u(t)`, not to biological `Y(t)`. It should be excluded from physiological interpretation.
