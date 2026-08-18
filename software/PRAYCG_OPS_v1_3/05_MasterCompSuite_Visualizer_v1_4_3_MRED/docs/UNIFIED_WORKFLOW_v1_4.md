# Unified workflow v1.4

## Analysis-only mode

Use this when you want the Master Comprehensive Suite to process the run and write tables/reports, but you do not need a synchronized review MP4.

## Analysis-plus-visual mode

Use this when you want the Master Comprehensive Suite to run first, then automatically pass its output folder to the MasterSync Visualizer. The visualizer will overlay CandidateLocal_KHT events, state-locked windows, cue schedules, and other event files where available.

## Recommended branch visualizations

Render one MP4 per branch:

```text
control + condition=control
target + condition=target
override + condition=override
```

This prevents accidentally pairing the Target video with Override physiology or vice versa.
