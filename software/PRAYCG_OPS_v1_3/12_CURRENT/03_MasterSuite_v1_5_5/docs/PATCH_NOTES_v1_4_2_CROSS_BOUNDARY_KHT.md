# PRAYCG Unified Master Suite v1.4.2 - Cross-Boundary CandidateLocal_KHT Patch

## What changed

CandidateLocal_KHT now permits theta follow-up windows to continue into the paired formal washout when a gamma/TSP candidate occurs near the end of a stimulus branch.

The local K estimation window remains inside the originating branch. Only the outcome/integration window may cross, and only into the paired washout:

- CONTROL_1 -> WASHOUT_1
- TARGET_1 -> WASHOUT_2
- CONTEXTUAL_OVERRIDE_1 -> WASHOUT_3

No follow-up window is allowed to cross into subjective report screens, instruction screens, or a different stimulus branch.

## Why this is needed

The v0.1 strict boundary could return NaN for end-of-clip candidate events even though the EEG recording continued into washout. That was too conservative for PostPeakPNCC/Gamma-to-Theta handoff logic.

## Interpretive boundary

This patch rescues evaluability only. It does not lower the threshold for a positive K_HT claim. K alone is not enough. Theta handoff alone is not enough. Final human-event lock still requires local coupling, theta carryover, condition specificity, artifact/timing pass, and appropriate claim-level status.
