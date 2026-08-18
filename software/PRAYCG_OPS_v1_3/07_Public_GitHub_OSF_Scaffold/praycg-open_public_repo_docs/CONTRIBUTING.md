# Contributing to PR-AYC-G Open

Thank you for helping make this project more testable, safer, cleaner, and easier to reproduce.

## Contribution priorities

High-value contributions include:

- bug fixes for MediaPrep, acquisition, protocol running, analysis, or visualization;
- tests that reduce false positives;
- clearer documentation;
- no-copyright demo stimuli;
- improved QC checklists;
- better artifact handling;
- independent reproduction of the Rung 0 packages;
- hardware safety improvements;
- issues that identify overclaiming or unclear boundaries.

## Non-negotiable boundaries

Do not contribute:

- copyrighted stimulus media;
- raw participant data without explicit permission and de-identification;
- private emails or identifiable personal information;
- medical, diagnostic, therapeutic, or clinical efficacy claims;
- claims that PR-AYC-G proves consciousness, OSM, hidden cellular variables, microtubular memory, souls, or biophotonic memory;
- code that requires secrets, private paths, or commercial assets to run;
- hardware instructions that involve unsafe mains wiring or unreviewed electrical modifications.

## How to contribute

1. Open an issue describing the proposed change.
2. Keep the claim boundary intact.
3. Submit a pull request against a development branch.
4. Include a short test or smoke-test note when practical.
5. Update documentation when behavior changes.
6. Avoid committing large media, raw XDF files, participant data, generated output folders, or local logs.

## Coding style

- Prefer clear, boring, auditable Python.
- Avoid hidden state and hard-coded local paths.
- Put user-editable settings in config files or command-line arguments.
- Write sidecar reports for generated outputs.
- Label exploratory outputs as exploratory.
- Fail safely and loudly when streams, markers, or required files are missing.

## Documentation style

Use this pattern:

```text
What it does.
What it does not do.
Inputs.
Outputs.
How to run it.
How to verify it.
Known failure modes.
Claim boundary.
```

## Reproducibility standard

For any synthetic reproducibility package, do not modify locked specifications, seeds, thresholds, alternatives, or reporting templates and still call the output a reproduction. Any modification creates a new version.

## Human-subjects caution

This repository is not an IRB approval. Human-subjects work requires appropriate consent, privacy protection, risk review, data handling, and debriefing procedures where applicable.
