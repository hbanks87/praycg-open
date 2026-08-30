# PRAYCG2.0 Consolidated Self-Report Runner

PRAYCG2.0 keeps the anchor-registered PRAYCG1.9C/1.9D architecture and consolidates self-report so the report layer does not become its own cognitive extraction task.

## Core change

The old repeated long questionnaire is replaced by:

1. **Pre-run calibration** for cue legibility, blur, squint need, audio-video sync confidence, speaker audibility, and fatigue/discomfort.
2. **Six-item branch core report** after each branch/washout.
3. **Override-only task report** for running-sum/cue burden.
4. **Gated detailed confound report** only when `ConfoundBurden >= 3`.
5. **Final master report after Baseline 2**, not before.

## Run

```bat
python scriptsun_PRAYCG2_0_ConsolidatedSelfReport.py
```

## Important

Load a `*_LOCKED.json` predeclared anchor file. If no anchor file is loaded, the run is not runner-registered confirmatory even if the anchor existed in planning notes.
