# PRAYCG NUPI v0.1 Report - Arrival, Contact, Field of Dreams

## Executive conclusion
NUPI v0.1 treats narrative update polarity as a two-axis proxy: Accommodative Load Index (ALI) versus Resolutive Recovery Index (RDI). It does not measure literal heat, ATP, glucose, oxygen consumption, or thermodynamic energy. It tests whether a run is better described as model-expansion/load, closure/recovery, high-load-with-recovery, or unresolved recognition.

- **Arrival:** ALI=0.382; RDI=NA; NUPI=NA; classification=POLARITY_UNRESOLVED_NO_BASELINE2.
- **Contact:** ALI=0.658; RDI=0.820; NUPI=0.162; classification=HIGH_LOAD_WITH_RECOVERY.
- **Field:** ALI=0.335; RDI=0.711; NUPI=0.376; classification=RESOLUTIVE_RECOVERY.

## Formula
`ALI = mean(semantic intensity, Target specificity, complexity perturbation, TTI, primary endpoint pass score)`

`RDI = mean(Baseline2 regulation, Baseline2 semantic echo, EET afterstate echo, self-report echo)`

`NUPI = RDI - ALI`

RDI is only graded when a final reflective baseline or equivalent after-state physiology exists. Otherwise the run is marked polarity-unresolved even if afterstate proxies are suggestive.

## Interpretation by run
### Arrival
Arrival remains the recognition-dominant case. Its Target CII and Target-specific CII are positive, but the run lacks a PRAYCG2.0-style Baseline2/final reflective physiology layer and did not pass the strict gates. Therefore NUPI is not graded; the correct classification is polarity-unresolved / recognition-dominant rather than resolutive or accommodative.

### Contact
Contact has the highest semantic intensity and Target specificity. It also has strong Baseline2 regulatory recovery, so the data do not support a simple "metabolic crater" interpretation. NUPI classifies it as high-load-with-recovery: a strong accommodative/awe-style update with a substantial reflective-regulatory after-state.

### Field of Dreams
Field has lower semantic intensity and weaker A-MRED amplitude than Contact, but it has strong reflective/self-report echo and a regulated Baseline2 pattern. NUPI classifies it as resolutive recovery: meaning as closure/regulatory dividend rather than meaning as peak shock.

## Tables
| run     |   semantic_intensity |   target_specificity |   complexity_perturbation |   tti_score |   primary_pass_score |   ALI_accommodative_load |   b2_regulation |   b2_semantic_echo |   eet_echo |   self_report_echo |   RDI_resolutive_recovery |   RDI_afterstate_proxy |       NUPI | polarity_class                   |
|:--------|---------------------:|---------------------:|--------------------------:|------------:|---------------------:|-------------------------:|----------------:|-------------------:|-----------:|-------------------:|--------------------------:|-----------------------:|-----------:|:---------------------------------|
| Arrival |             0.301514 |            0.374368  |                  0.523193 |    0.710025 |            0         |                 0.38182  |       nan       |         nan        |   0.988071 |           0.833333 |                nan        |               0.910702 | nan        | POLARITY_UNRESOLVED_NO_BASELINE2 |
| Contact |             0.897127 |            1         |                  0.357865 |    0.993355 |            0.0428571 |                 0.658241 |         1       |           0.666667 |   0.946985 |           0.666667 |                  0.820079 |               0.806826 |   0.161839 | HIGH_LOAD_WITH_RECOVERY          |
| Field   |             0.163369 |            0.0666421 |                  0.259575 |    0.75704  |            0.428571  |                 0.33504  |         0.56531 |           0.609122 |   0.855905 |           0.814815 |                  0.711288 |               0.83536  |   0.376248 | RESOLUTIVE_RECOVERY              |

## Boundaries
NUPI is an exploratory cross-run interpretation layer. It should not be used as a clinical score, moral score, or literal thermodynamic measurement. It depends on prior modules, stimulus QC, artifact gating, and Baseline2 availability. Contact and Field are not equivalent confirmatory runs: Contact was conceptually predeclared but not runner-registered; Field was runner-registered but anchor timing was estimated and ALS start-pulse validation was weak. NUPI therefore compares profiles, not final truths.