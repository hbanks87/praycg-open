# PR-AYC-G Open Science Hub

Open protocol, hardware documentation, software tools, synthetic reproducibility packages, and public-facing methods documents for exploratory psychophysiology of narrative meaning.

## One-sentence summary

PR-AYC-G tests whether narrative meaning has measurable timing, shape, and physiological consequence beyond matched audiovisual stimulation and analytic task stance.

## What this repository contains

```text
hardware/the_box/                  Public build documentation for the Box / Faraday-style chamber.
software/mediaprep/                Stimulus preparation and QC workflow.
software/protocol_runner/          PR-AYC-G protocol runner workflow.
software/acquisition_brainflow_als/ OpenBCI BrainFlow + ALS-PT19 LSL bridge workflow.
software/master_comprehensive_suite/ Analysis suite documentation and release slot.
software/master_sync_visualizer/    Synchronized data/stimulus visualization workflow.
software/optoping_rung0/            Synthetic Opto-PING reproducibility ladder.
examples/                           Synthetic and no-copyright demo examples only.
templates/                          Cue, anchor, self-report, and QC templates.
docs/                               Public orientation, ethics, safety, and TSC handouts.
```

## What this is not

This is not a medical device, diagnostic tool, treatment system, clinical protocol, or proof of consciousness. It does not prove Opto-Structural Memory, microtubular memory, biophotonic memory, hidden cellular variables, souls, love as a physical force, or human EEG access to molecular mechanisms.

Current human PR-AYC-G data should be treated as exploratory unless a future preregistered design, validated timing, artifact controls, appropriate sample size, and independent replication support stronger claims.

## Current public posture

Use this repository as an open engineering and hypothesis-testing workspace:

```text
Run it.
Break it.
Audit it.
Improve it.
Do not overclaim it.
```

## Core PR-AYC-G design

The clean PR-AYC-G stimulus suite uses three arms:

1. **Phase-scrambled Control** - same source stimulus with recognizable story, faces, and meaning disrupted while low-level audiovisual structure is preserved as much as practical.
2. **Target** - intact meaningful narrative watched naturally.
3. **Contextual Override** - same intact narrative, but watched under analytic task demand.

Target and Contextual Override should use the same cue-embedded stimulus file; only instructions should differ. The Control should be generated from the cue-embedded Target so cue timing and low-level cue energy are represented across branches.

## Public release rule

Do not upload copyrighted stimulus media, raw participant data, private emails, private file paths, location-identifying photographs, secrets, API keys, or unreviewed clinical claims.

Use lawful demo media or synthetic media only in public examples.

## Repository status

Initial public scaffold. Replace placeholders with current release ZIPs, installation docs, and public-safe examples before making the repository public.

## License summary

Suggested default:

```text
Code: Apache-2.0
Docs / protocols / hardware guides: CC BY 4.0 unless otherwise marked
Philosophical companion essays: choose CC BY 4.0 or a more restrictive Creative Commons license intentionally
```

See `LICENSE` and `docs/license_policy.md`.
