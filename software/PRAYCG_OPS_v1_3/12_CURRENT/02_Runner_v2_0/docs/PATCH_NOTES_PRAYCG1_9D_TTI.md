# PRAYCG1.9D - TTI Protocol Notes

This package extends PRAYCG1.9C anchor-registered operation with TTI documentation and report templates.

No change is required to MediaPrep for TTI itself. MediaPrep v1.7A already generates draft/locked anchor scaffolds. PRAYCG1.9C/1.9D should load the LOCKED anchor JSON before acquisition for strict runner-registered timing.

## Added report layer

After Target/Override, PRAYCG1.9D should capture reception/extraction ratings:

- target_reception_depth_0_9
- override_extraction_load_0_9
- override_meaning_breakthrough_0_9
- target_afterglow_0_9
- override_afterglow_0_9
- task_fragmentation_0_9

These are interpretive covariates, not proof.
