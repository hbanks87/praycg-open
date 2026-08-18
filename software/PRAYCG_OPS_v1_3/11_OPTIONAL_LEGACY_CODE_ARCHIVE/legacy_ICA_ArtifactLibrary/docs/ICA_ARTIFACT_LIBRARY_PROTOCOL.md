# PR-AYC-G ICA Artifact Library Protocol

## Objective

Create a subject- and montage-specific artifact reference library for PR-AYC-G analysis.

The library intentionally records known artifacts under LSL markers so later ICA components from PR-AYC-G runs can be compared against these artifact fingerprints.

## Why this exists

Blinks, jaw activity, neck tension, shoulder movement, swallowing, and electrode contact shifts can mimic or contaminate EEG endpoints. This is especially important for PR-AYC-G because the current low-gamma endpoint lives in the 30-45 Hz range, which is vulnerable to myogenic contamination.

## Required streams

```text
OpenBCI EEG stream, usually obci_eeg1
ICAArtifactMarkers from praycg_ica_control_run.py
```

Recommended additional streams:

```text
VernierRespirationBelt
PolarHRV or PolarECG
video/audio marker stream if paired with a stimulus test
```

## Hardware posture

Use the same cap, montage, reference, ground, sampling rate, environment, and body posture planned for PR-AYC-G. The artifact library should match the actual run geometry.

## Run structure

The control script prompts the participant through:

```text
clean stillness
single blinks
triple blinks
long blink/squeeze
eye movements
brow raise
jaw clench
jaw left/right
simulated teeth tension
tongue press
swallow
neck tension
neck turn
shoulder shrug
asymmetric shoulder movement
posture shift
deep breath
sigh
silent counting
mental arithmetic
```

Each action is marked with:

```text
ARTIFACT_<LABEL>_REP_<N>_ACTION_START
ARTIFACT_<LABEL>_REP_<N>_ACTION_END
```

The build script scores ICA components by action-window RMS relative to pre-action baseline.

## Interpretation ladder

| Output | Allowed interpretation | Not allowed |
|---|---|---|
| Event-locked blink component | Candidate blink-related component | Proof that all blinks are removed |
| Event-locked jaw component | Candidate myogenic component | Proof low-gamma is cortical |
| Template match in PR-AYC-G run | Component resembles known artifact library pattern | Component is definitely artifact |
| Cleaned file after manual exclusion | Cleaner working dataset | Confirmatory proof of PR-AYC-G |

## Recommended decision rule

For PR-AYC-G analysis:

1. Inspect raw QC and retained channels.
2. Build artifact component rankings from the control run.
3. Fit ICA to the PR-AYC-G run.
4. Score components against the artifact library.
5. Inspect topographies, source time series, PSD, and marker-locked behavior.
6. Exclude only components with converging evidence.
7. Re-run low-gamma payload, PLV, API, and PNCC analyses with and without exclusions.
8. Report sensitivity.

## Reporting language

Use:

> ICA artifact-library matching identified candidate ocular/myogenic/motion components. Analyses were repeated with these components excluded and compared against the artifact-matched non-ICA pipeline.

Do not use:

> ICA proved the signal is artifact-free.

## Minimal output to archive

```text
artifact_control_run.xdf
marker_log.csv
raw_channel_qc.csv
component_features.csv
component_artifact_scores.csv
artifact_component_rankings.csv
artifact_templates.npz
figures/
manual_component_decision_log.csv
```
