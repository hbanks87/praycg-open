# PRAYCG MediaPrep + Protocol Suite v1.6Q — GUI Button Hotfix

This is a hotfix build of the v1.6P control-validity media-prep pipeline.

It keeps the v1.6P scientific/media-prep logic:

- optional visual source-stamp / watermark cleanup applied to the master before all stimulus branches;
- contrast-protected number badge;
- cue-embedded Target and bit-identical cue-embedded Contextual Override;
- phase-scrambled Control generated from the cue-embedded Target;
- stronger control audio mode, defaulting to `speech_shaped_noise_envelope`.

The v1.6Q change is the GUI behavior. The Run button now gives immediate visible feedback, validates inputs, disables while running, writes errors to the log area, and writes a crash text file to the output root when possible.

## Run the GUI

```bash
python scripts\praycg_media_prep_gui_v1_6Q.py
```

or:

```bash
python scripts\run_PRAYCG_MediaPrep_v1_6Q.py
```

Use the new **Validate Inputs** button before running. When you click **Run Stimulus Media Suite v1.6Q**, the log should immediately show:

```text
RUN BUTTON CLICKED.
RUN BUTTON CLICK CONFIRMED. MediaPrep worker started.
```

If it does not, use the launcher BAT from `examples/` so the console stays open.

## Headless example

```bash
python scripts\praycg_media_prep_gui_v1_6Q.py --no-gui ^
  --project-name thePresent_SM ^
  --master "C:\PRAYCG\source\stimulus_master.mp4" ^
  --out-root "C:\PRAYCG\media_prepared" ^
  --clean-visual-mask ^
  --mask-preset upper_left ^
  --mask-method blur ^
  --control-audio-mode speech_shaped_noise_envelope ^
  --run-fingerprint ^
  --overwrite
```

The `^` characters are Windows line breaks only.

## If a run fails

v1.6Q writes a crash file such as:

```text
PRAYCG_MediaPrep_v1_6Q_CRASH_YYYYMMDD_HHMMSS.txt
```

inside the chosen output root. Send or inspect that file instead of guessing.

## Boundary

This package prepares media. It does not certify meaning, empathy, neural endpoints, task compliance, or audio unintelligibility. Manual media QC, StimulusFingerprint QC, protocol acquisition, and Master Comprehensive analysis remain required.
