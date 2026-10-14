# Research concepts and mathematical definitions

PRAYCG introduces project-specific ways to ask whether a response is better described as recognition, delayed integration, immersion, task competition, or a reflective after-state. This guide explains what those quantities take as input, how the preserved methods combine them, and what an output can support. A named formula is an operational definition; its implementation and its scientific validity are separate questions.

[Bibliography and source credits](../bibliography/README.md) · [Research entrance](../README.md) · [Measures and original notes](../measures/README.md) · [Algorithms and implementations](../algorithms/README.md) · [Protocols](../protocols/README.md) · [Reproducibility](../reproducibility/README.md)

## Choose the question

| Research question | Concept guide | Main quantities |
| --- | --- | --- |
| Was an event associated with recognition-like features, and was there a distinct delayed integration-like response? | [Recognition and integration](recognition-integration.md) | MRED, A-MRED, MRED-Peak/Resolution, ACG/CSI, OCU/ORI |
| Did attention-like and delayed integration-like features coincide, and can stimulus rhythm explain them? | [Immersion, entrainment and echoes](immersion-entrainment.md) | NIP, BIT, CII, IAQ/ITQ, CET, CET-R, EET |
| Did the run show load, recovery, competing task demand, or limited availability to receive the material? | [Update polarity and availability](update-availability.md) | ALI/RDI/NUPI, TTI, DGA/GDI |
| Can fast and slow candidate features be summarized with explicit artifact, task and missing-data rules? | [Controlled Access-Integration and time density](cai-sid.md) | CAI v0.2, context sensitivity, SID |
| Can reciprocal state dynamics be estimated, and what changes when moving from simulation to human proxies? | [Coupling, topology and Opto-PING](coupling-topology.md) | K_math, K_HT, CandidateLocal KHT, K_HT-topo, Topo-OSM |

## Follow the evidence through the calculation

```text
Recording, markers, media identity, display timing and self-report
    -> synchronized, quality-checked signals and feature tables
    -> declared event windows and condition contrasts
    -> component scores, gates and composite summaries
    -> interpretation with missingness, provenance and alternatives retained
```

For example, a gamma-derived feature is an input to some recognition-like scores. The score's name does not convert gamma into a direct measurement of meaning. A delayed theta feature is an operational integration marker; its absence does not establish that no memory formed. A Baseline 2 difference describes a final after-state following the whole protocol and does not identify Target as its sole cause.

The [v1.5.5 tier map](../measures/originals/master-suite-v1-5-5/MODULE_TIER_MAP_v1_5_5.md) proposes timing/QC, stimulus-fingerprint/CET-R and artifact/confound gates leading to A-MRED as a primary path for future confirmatory work. It places NIP, TTI, NUPI and endpoint compression in secondary summaries, with KHT-topo, NAST, EET and MRED-ITP among exploratory/convergence layers. These are roles in the proposed research design, not claims that the primary construct has been validated.

Many modules share MeaningGamma, TSP, theta, artifact measures or earlier module outputs. Agreement among them can therefore be partly built into the formulas. It is useful convergence to inspect, but it is not equivalent to independent replication or independent biological measurement.

## Read the version with the formula

These pages are explanations of preserved, versioned sources. They do not silently replace an earlier formula with a later one. In particular:

- **MRED:** the explicit weighted v0.1 event recipe differs from the schematic v0.2 topological extension and later suite formulations.
- **NUPI:** the original v0.1 note, Formula Report v1.0 and proposed Public Alpha 11.2.1 runtime have different RDI component lists.
- **CAI/SID:** CAI v0.2 replaces the earlier v0.1 proposal. The methods supplement's general interval-density expression and the managed runtime's valid-time aggregation require different coverage interpretation.
- **K:** a synthetic hidden-state parameter, a human feature-model coefficient and a hypothesized cellular coupling are not interchangeable because they share a symbol.

Use [algorithms and implementations](../algorithms/README.md) to locate the actual code, declared method version, input schema, defaults and outputs in the proposed Public Alpha 11.2.1 package. A filename alone is insufficient evidence of the algorithm version. The research pages describe the preserved definitions; the implementation map records where current code agrees with or differs from them.

## Notation and prerequisites

`T`, `C` and `O` denote Target, Control and Contextual Override where that three-condition comparison is defined; `j` is an event/anchor and `t` is time. `1[condition]` is an indicator, `[x]+` and `clip_plus(x)` mean `max(x,0)`, and `sigmoid(x)=1/(1+exp(-x))`. A bounded score is not a calibrated probability.

Standardization is part of the method. The [Formula Report v1.0, section 2.3](../collections/public-docs/Formula_Module_Report_v1_0/PRAYCG_Formula_Module_Report_v1_0.md#23-robust-z-score) distinguishes `z` and robust `rz`, and requires the reference set to be declared. Event-level, pooled-condition, random-anchor and Baseline 1 reference distributions answer different questions. CAI's Baseline 1 transform is specified separately in its guide. Coefficients cannot be reproduced from a list of feature names without the reference distribution, windows, missing-data policy and preprocessing.

A useful methods record therefore identifies the source and algorithm version, channel/ROI and signal definitions, timing basis, stimulus hashes, anchor provenance, normalization reference, coefficients and thresholds, missingness and coverage, artifact/confound checks, and condition/order limitations. Report component values and failed gates with the composite rather than treating an attractive label as the result.

## Research status and next evidence

The [complete ladder index](../ladders/README.md) separates completed synthetic work, historical descriptions, exploratory human translation and proposed future stages. The [Opto-PING hub](../optoping/README.md) preserves both positive and unsuccessful specificity results. The [reproducibility guide](../reproducibility/README.md) distinguishes rerunning supplied synthetic programs from independently collecting human data.

The [protocol/theory methods supplement](../protocols/originals/docs/PRAYCG_v0_93_to_v0_95_Protocols_Theory_and_Analysis_Methods.md) states the central limit: software-valid does not mean construct-valid. Prospective anchor locking, valid manipulations, simpler alternative models, independent operators, additional participants and direct measurements appropriate to the claimed scale are distinct pieces of evidence. These guides organize the project's concepts without establishing priority over the wider literature or claiming that every named quantity is scientifically novel.
