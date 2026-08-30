# DGA_v0.1 - Decoder Gate Availability / Gate Dissociation

Version: PRAYCG Unified Master Suite v1.5.6

## Purpose

DGA formalizes a new PRAYCG interpretation layer: meaning is not treated as a simple payload transferred from stimulus to brain. A meaningful response is modeled as an interaction between external semantic access and an already-structured internal decoder state.

DGA asks whether the subject had enough sensory access, internal availability, emotional/integrative impact, and low enough extraction/confound burden for meaning to be received and integrated.

## Core formulas

```text
SA_b = 1 - mean(AudioComprehensionDifficulty, SpeakerVolumeDifficulty,
                ExternalNoiseIntrusion, AudioVideoSyncProblem)/9

DA_b = mean(Meaning, Absorption, EmotionalAfterglow,
            StoryActiveWashout)/9

EI_b = mean(Absorption, EmotionalAfterglow, StoryActiveWashout)/9

X_b = max(core TaskExtractionLoad, Override task burden)/9

C_b = max(core ConfoundBurden, detailed confound mean)/9

D_gate,b = sigmoid(2.0*SA_b + 1.4*DA_b + 1.1*EI_b
                   - 1.2*X_b - 1.8*C_b - 0.75)

GDI = mean(SA_Override - SA_Target,
           EI_Target - EI_Override,
           X_Override - X_Target,
           C_Target - C_Override)
```

## Interpretation

- High Target gate: the Target branch had sufficient semantic access, availability, and emotional integration with manageable confounds.
- High GDI: semantic access and emotional/integrative impact dissociated across branches, often because Override was clearer but more task-loaded, while Target was emotionally stronger but confounded.
- Feature-proxy only: older runs without PRAYCG2.0 self-report and Baseline2 should not be treated as strict DGA endpoint evidence.

## Inputs

DGA reads:

- PRAYCG2.0 branch core report JSONs;
- PRAYCG2.0 branch confound report JSONs;
- Override task report JSONs;
- Master Suite feature tables when available;
- A-MRED or MRED-Peak/Resolution anchor tables when available.

## Outputs

```text
dga_branch_gate_table.csv
dga_gate_dissociation_summary.csv
dga_gate_adjusted_mred_anchor_table.csv
dga_interpretation.json
dga_report.md
```

## Boundary

DGA is an interpretation and triage module. It does not prove consciousness, memory formation, hidden-Y biology, OSM biology, or literal thermodynamic energy transfer. It estimates the conditions under which meaning could be decoded, received, and integrated.
