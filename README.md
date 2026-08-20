# PRAYCG Open

**PRAYCG** is an exploratory, open-source psychophysiology protocol and software pipeline for testing whether narrative meaning has measurable timing, shape, and physiological consequence.

This repository is **methods-first**. It contains software, documentation, templates, and public-safe example materials for stimulus preparation, PRAYCG2.0 protocol execution, physiological analysis, visualization, and offline interpretation.

## Current claim boundary

PRAYCG does **not** prove consciousness, memory biology, microtubules, biophotons, the soul, or love as a number. It tests whether an intact narrative target produces physiological state trajectories that differ from a phase-scrambled audiovisual control and from the same intact narrative under analytic contextual override.

## Recommended module hierarchy

```text
BOXED PRIMARY PATH:
  Timing/QC
  + StimulusFingerprint/CET-R
  + artifact/confound gates
  -> A-MRED / MRED-Peak-Resolution

SECONDARY:
  NIP/BIT/CII/IAQ
  TTI
  NUPI

EXPLORATORY / CONVERGENCE:
  KHT-topo
  NAST
  EET
  MRED-ITP / ACG / OCU
  OCM025 / RSM / CVB / SquintProxy
  LSO / Subtitle Override
```

## What is included

```text
software/mediaprep/                 MediaPrep + StimulusFingerprint v1.8
software/protocol_runner/           PRAYCG2.0 consolidated self-report runner
software/master_comprehensive_suite/ Master Suite v1.5.5 with offline interpreter
examples/gold_plated_contact_pilot_public/ derived Contact pilot files, no copyrighted media
examples/no_copyright_media_demo/   self-contained CC0 synthetic demo media + QC outputs
examples/open_movie_sintel_recipe/  CC-BY Sintel excerpt recipe/downloader for local generation
```

## Contact example status

The Contact pilot is included as a **gold-plated but not gold-record** example. It is useful for showing the file layout and analysis-output structure. It is not presented as confirmatory evidence.

## Citation

See `CITATION.cff`. If you reuse the synthetic demo media, cite this repository. If you generate a Sintel excerpt using the included recipe, follow the Sintel CC-BY 3.0 attribution requirements.

Generated: 2026-08-18T20:39:25.127752+00:00
