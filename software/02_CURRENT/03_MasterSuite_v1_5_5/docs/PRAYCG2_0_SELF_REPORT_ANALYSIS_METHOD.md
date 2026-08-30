# PRAYCG2.0 Consolidated Self-Report Schema

## Branch core report JSON

```json
{
  "schema": "PRAYCG2_0_branch_core_report_v1",
  "phase_name": "TARGET_1_AFTER_WASHOUT_2",
  "branch_label": "Target",
  "branch_type": "target",
  "ratings": {
    "Meaning": 0,
    "Absorption": 0,
    "EmotionalAfterglow": 0,
    "StoryActiveWashout": 0,
    "TaskExtractionLoad": 0,
    "ConfoundBurden": 0
  },
  "scene_note": "typed scene-level note",
  "confound_detail_recommended": false
}
```

## Override task report JSON

```json
{
  "schema": "PRAYCG2_0_override_task_report_v1",
  "ratings": {
    "FinalSumConfidence": 0,
    "TaskCompliance": 0,
    "CueLegibilityProblem": 0,
    "RunningSumStall": 0,
    "ApproximateGuessCount": 0,
    "HardNumberCombinationDifficulty": 0
  },
  "note": "typed running-sum / cue-burden note"
}
```

## Final master report JSON

```json
{
  "schema": "PRAYCG2_0_final_master_report_v1",
  "choices": {
    "MostMeaningfulBranch": "Target",
    "MostAbsorbingBranch": "Target",
    "StrongestAfterglowBranch": "Target"
  },
  "ratings": {
    "OverrideReducedReception": 0,
    "StoryBrokeThroughOverride": 0,
    "TargetEchoedDuringBaseline2": 0,
    "Familiarity": 0,
    "NewMeaningToday": 0,
    "CurrentLifeResonance": 0
  },
  "final_scene_note": "typed final scene-level note"
}
```


## Analysis interpretation

The six-item branch report supplies compact covariates for MRED/NAST/TTI. Override task reports feed OCM/RSM/CVB. Gated confound details feed veto/caution flags. The final master report is comparative and should be interpreted after Baseline 2 rather than as a pre-Baseline cognitive task.
