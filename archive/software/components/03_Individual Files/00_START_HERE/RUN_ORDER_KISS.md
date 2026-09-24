# PRAYCG Run Order - KISS

## 0. Install Python
Use Python 3.11 or 3.12 on Windows. Create a separate virtual environment for each major tool folder if needed.

## 1. Prepare media
Use:

```text
01_StimulusPrep_MediaPrep_v1_6S/
```

Default recommendation: fullscreen ALS start pulse enabled.

Outputs needed for the protocol:

```text
stimulus_control_cued_phase_scrambled_<project>_v1_6S.mp4
stimulus_target_cued_<project>_v1_6S.mp4
stimulus_override_cued_<project>_v1_6S.mp4
cue_schedule_<project>_v1_6S.json
```

## 2. QC media
Use:

```text
04_StimulusFingerprint_QC_v1_5/
09_QC_Checklists/
```

Manual QC remains mandatory for control audio and visual source-stamp cleanup.

## 3. Start acquisition
For TSC-grade / timing-critical acquisition:

```text
03_Acquisition/BrainFlow_ALS_PT19_Bridge_v1_4_TSC_grade/
```

For home-user low-burden acquisition:

```text
03_Acquisition/BrainFlow_EEGOnly_Home_Bridge_v1_0/
```

## 4. Run protocol
Use:

```text
02_ProtocolRunner_PRAYCG1_8B/
```

Load the Control, Target, Override, cue schedule, and optional predeclared anchor JSON/CSV.

## 5. Analyze and visualize
Use:

```text
05_MasterComprehensiveSuite_Visualizer_v1_4_3_MRED/
```

The unified launcher can run analysis only or analysis plus visualizer.

## 6. Optional Opto-PING synthetic verification
Use:

```text
06_OptoPING_Rung0_Reproducibility/Rung0O_LockedNullAwareReproduction/
```

The current synthetic boundary remains: Rung 0 proves synthetic identifiability/specificity under locked assumptions, not biology.
