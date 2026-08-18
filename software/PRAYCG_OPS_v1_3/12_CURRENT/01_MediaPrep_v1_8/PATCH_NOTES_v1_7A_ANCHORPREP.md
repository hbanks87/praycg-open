# Patch Notes — v1.7A AnchorPrep

## Added

- DRAFT anchor JSON/CSV generation next to the cue schedule.
- Contact and Eternal Sunshine/Montauk anchor presets.
- Anchor lock checklist generated per project.
- Anchor finalizer script that validates exact timecodes and writes *_LOCKED.json/csv.
- Manifest fields for anchor draft outputs.

## Operational rule

DRAFT anchors are not confirmatory. Only a LOCKED anchor file loaded into PRAYCG1.9C before acquisition can support a runner-registered predeclared anchor claim.

## Recommended folder state before running PRAYCG1.9C

```text
stimulus_target_cued_<project>.mp4
stimulus_override_cued_<project>.mp4
stimulus_control_cued_phase_scrambled_<project>.mp4
cue_schedule_<project>.json
predeclared_anchors_<project>_v1_7A_LOCKED.json
```
