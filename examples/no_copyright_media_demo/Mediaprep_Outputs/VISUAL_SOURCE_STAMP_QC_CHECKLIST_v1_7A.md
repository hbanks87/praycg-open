# PRAYCG v1.7A Visual Source-Stamp / Watermark QC Checklist

Project: `stimulus_master_Demo_Lantern_Bridge_CC0`

## Required manual checks

Watch Target, Contextual Override, and Control.

Pass criteria:
- No readable source watermark, source stamp, platform logo, or subtitle artifact remains in Target or Override unless intentionally documented.
- If a mask/cleanup was applied, it was applied before all branches were generated.
- Target and Override remain bit-identical after cue rendering.
- Control was generated from the cleaned cue-embedded Target.

Record:
- Upper-left stamp removed or neutralized? yes / no / not applicable
- Other readable logo/stamp present? yes / no
- Visual QC verdict: PASS / FAIL / PILOT ONLY

Boundary: source-stamp cleanup is allowed only as a documented preprocessing step applied before branch generation.
