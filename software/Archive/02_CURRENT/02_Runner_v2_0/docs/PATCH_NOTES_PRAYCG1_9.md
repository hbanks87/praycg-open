# Patch Notes — PRAYCG1.9

## Retained from PRAYCG1.8B

- browse-file GUI for Control, Target, Override, cue schedule, and anchor file;
- predeclared media-structural anchors;
- final reflection baseline and final master subjective report;
- display safe-fit mode for high-DPI laptops;
- LSL hardening and local event-log capture.

## Added in PRAYCG1.9

### Pre-run display/audio calibration

A screen asks the subject/operator to rate cue legibility, cue blur, need to squint, audio-video sync confidence, and speaker audibility before the run.

### Per-branch confound reports

After each washout and subjective rating block, the runner collects ratings and short typed notes for:

- audio-video sync problems;
- audio comprehension problems;
- external noise / train / equipment intrusions;
- cue legibility and blur;
- eye strain / squint need;
- speaker-volume difficulty.

### Override running-sum report

The Override report additionally asks about:

- running-sum stalls;
- approximate or guessed updates;
- large-sum difficulty;
- carry difficulty;
- hard number combinations;
- final sum confidence.

## Why this patch exists

Her Run 1 revealed presentation-level confounds that were not fully captured by earlier protocols: delayed voice/lip-sync, train noise masking a monologue, and small/blurry number cues. PRAYCG1.9 formalizes those observations so the analysis suite can mark affected windows as confound-cautioned instead of silently overinterpreting them.
