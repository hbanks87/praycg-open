# NUPI_v0.1 - Narrative Update Polarity Index

Document status: exploratory secondary module. NUPI estimates the polarity of a narrative update using available PR-AYC-G proxy outputs. It does not measure literal heat, ATP, glucose consumption, oxygen metabolism, clinical recovery, moral value, or consciousness.

## Purpose

NUPI asks whether a meaningful narrative event is better described as:

- `ACCOMMODATIVE_LOAD`: the story imposes model-expansion cost or destabilizing semantic work.
- `RESOLUTIVE_RECOVERY`: the story closes an unresolved predictive loop and is followed by regulatory recovery.
- `HIGH_LOAD_WITH_RECOVERY`: the story strongly perturbs the system and is followed by strong reflective/regulatory recovery.
- `RECOGNITION_WITH_WEAK_RECOVERY`: meaning recognition occurs without a convincing recovery/integration after-state.
- `POLARITY_UNRESOLVED_NO_BASELINE2`: after-state physiology is not available, so polarity is not graded.

## Core formulas

```text
ALI = mean(
  semantic_intensity,
  target_specificity,
  complexity_perturbation,
  TTI_score,
  primary_endpoint_pass_score
)
```

```text
RDI = mean(
  Baseline2_regulation,
  Baseline2_semantic_echo,
  EET_afterstate_echo,
  self_report_echo
)
```

```text
NUPI = RDI - ALI
```

A positive NUPI means recovery tilt. A negative NUPI means load tilt. If Baseline2 or an equivalent final reflective after-state is absent, NUPI is not graded and the run is marked polarity-unresolved.

## Module tier placement

```text
PRIMARY RECOMMENDED:
  Timing/QC + StimulusFingerprint/CET-R + artifact/confound gates -> A-MRED

SECONDARY SUMMARIES:
  NIP/BIT/CII/IAQ, TTI, NUPI

EXPLORATORY / CONVERGENCE:
  KHT-topo, NAST, EET, MRED-ITP/ACG/OCU, OCM/RSM/CVB/Squint, LSO/SPM
```

## Required inputs

At minimum:

- CII/NIP anchor integral table.
- TTI global table or thermodynamic theft composite table.
- MRED-ITP anchor summary if available.
- EET endogenous echo table if available.
- Baseline1 vs Baseline2 feature/autonomic summary for graded RDI.
- Optional final self-report parser outputs.

## Outputs

```text
nupi_run_summary.csv
nupi_anchor_polarity_table.csv
nupi_visual_overlay.csv
nupi_interpretation.json
```

## Command

```bat
py -3.11 scripts\praycg_nupi_module_v1_5_4.py ^
  --analysis-folder "C:\path\to\MasterComprehensiveOutput\tables" ^
  --profile field ^
  --run-name FieldOfDreams_Run1
```

## Claim boundary

NUPI can help distinguish different shapes of narrative response. It cannot prove that a story literally releases or absorbs thermodynamic heat. It should be reported as a proxy-level profile classifier and only after QC, artifact checks, stimulus-fingerprint controls, and self-report boundaries are preserved.
