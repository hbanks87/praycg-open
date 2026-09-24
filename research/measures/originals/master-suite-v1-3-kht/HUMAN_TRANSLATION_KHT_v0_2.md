# HumanTranslation_KHT_v0.2

This module operationalizes the PR-AYC-G Rung 1 human-translation bridge. It is downstream of the Opto-PING Rung 0J/K synthetic lock-in work, but it does not treat human EEG as a cellular or opto-structural measurement.

## Primary distinction

- `K_math`: synthetic Opto-PING endpoint.
- `K_HT`: human translation coupling estimate.
- `K_OSM`: reserved for direct opto-structural/cellular evidence.

The module estimates `K_HT` only.

## Inputs

- EEG feature table from the Master Suite.
- TemporalSemanticProxy or posterior-temporal proxy columns.
- Theta power or theta PLV outcome.
- Task, visual, artifact covariates where available.
- Optional annotation CSV, media manifest, and stimulus fingerprint folder.

## Outputs

- Requirements audit.
- State-space input table.
- Phase-wise eta/zeta/K_HT proxy table.
- Leave-segment-out model-comparison table.
- Gate decision table.

## Interpretation boundary

A positive K_HT result would be evidence of a human-level state-transition model. It would not prove Opto-Structural Memory, hidden cytoskeletal resonance, biophotonic flickering, microtubular memory, or any cellular mechanism.
