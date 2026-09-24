# PRAYCG2.0 Patch Notes - Consolidated Self-Report

## Why this patch exists

The self-report layer had become too large. Long repeated reports risk turning reflection into a task, contaminating washout and Baseline 2. PRAYCG2.0 keeps self-report as an independent evidence stream but reduces it to the smallest set needed to interpret physiology.

## New branch core report

After Control, Target, and Override, the runner asks six ratings:

- Meaning
- Absorption
- EmotionalAfterglow
- StoryActiveWashout
- TaskExtractionLoad
- ConfoundBurden

Each branch then receives one short text prompt. Subjects are instructed not to estimate timestamps.

## Override-only report

Only after Contextual Override:

- FinalSumConfidence
- TaskCompliance
- CueLegibilityProblem
- RunningSumStall
- ApproximateGuessCount
- HardNumberCombinationDifficulty

## Gated confound detail

Detailed confound questions are asked only when `ConfoundBurden >= 3`.

## Final master report

After Baseline 2, the runner asks:

- MostMeaningfulBranch
- MostAbsorbingBranch
- StrongestAfterglowBranch
- OverrideReducedReception
- StoryBrokeThroughOverride
- TargetEchoedDuringBaseline2
- Familiarity
- NewMeaningToday
- CurrentLifeResonance
- final scene note

## Claim boundary

Self-report contextualizes and constrains physiology. It does not prove consciousness, mechanism, or internal state.
