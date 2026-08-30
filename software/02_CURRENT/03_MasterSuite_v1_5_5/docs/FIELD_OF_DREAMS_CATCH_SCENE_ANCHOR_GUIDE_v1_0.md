# Field of Dreams “Have a Catch?” PR-AYC-G Anchor Guide v1.0

**Status:** estimated anchor scaffold for tomorrow's run. These anchors must be checked against the final rendered MediaPrep Target MP4 before they can be treated as strict runner-registered timing hypotheses.

## Core endpoint plan

Use **A-MRED v1.5.3** as the primary endpoint. The primary anchors are:

1. `FOD_A2_DAD_WANT_TO_HAVE_A_CATCH_REQUEST`
2. `FOD_A3_FATHER_ACCEPTANCE_RESPONSE`
3. `FOD_A4_FIRST_THROW_FIRST_CATCH_EMBODIED_REPAIR`

The other anchors are useful, but should be treated as secondary / exploratory:

- `FOD_A1_FATHER_RECOGNITION_APPROACH`: early recognition / schema activation.
- `FOD_A5_SUSTAINED_CATCH_AFTERGLOW_CONTINUITY`: sustained CII / NIP / EET window.
- `FOD_A6_TERMINAL_RELEASE_AND_WASHOUT_ECHO`: washout / Baseline2 echo window, with clip-edge caution.

## Prediction

The clean PR-AYC-G prediction is not simply “gamma goes up.” A primary Field of Dreams result should show:

```text
Target:
  MR and ENC rise around primary anchors.

Control:
  low meaning-recognition / integration despite matched low-level sensory structure.

Override:
  increased extraction/task load and reduced receptive integration relative to Target.
```

A strict A-MRED pass requires Target to exceed both Control and Override on both MR and ENC after artifact, confound, and stimulus-regressor checks.

## Familiarity warning

This scene is culturally famous and may be familiar. Familiarity can produce high meaning recognition without new theta/topological integration. Record familiarity, line familiarity, father-schema resonance, novelty today, and current-life resonance.

## Timecode warning

The JSON file `FieldOfDreams_CatchScene_predeclared_anchors_ESTIMATED_EDITME_v1_0.json` is runner-loadable as a pilot scaffold, but it is **not strict confirmatory** unless the timecodes are edited after reviewing the final rendered Target MP4 and then locked.

Recommended workflow:

```text
MediaPrep v1.8
→ review final Target MP4
→ edit rendered_time_sec for each anchor
→ run anchor finalizer
→ load *_LOCKED.json into PRAYCG2.0
→ run acquisition
→ analyze with Master Suite v1.5.3+
```

## Boundary

Anchor files freeze hypotheses; they do not certify that physiology passed. A-MRED, MRED, NIP, TTI, CET/EET, and MRED-ITP remain human-scale psychophysiology analyses. They do not prove OSM biology, microtubules, biophotons, consciousness, soul, or literal memory formation.
