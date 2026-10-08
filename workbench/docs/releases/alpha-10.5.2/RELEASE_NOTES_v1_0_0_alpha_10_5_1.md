# PRAYCG Workbench Alpha 10.5.1

This complete release simplifies recording with cautions, organizes the Analysis Forge, and extends spectral/optical exploration to XDF replay.

## Recording

- Adds scoped Athena **ACQUISITION_VERIFIED / TRANSPORT_RECORDING_VERIFIED** admission through current physical recording evidence and exact route identities. Ordinary EEG recording is independent of clean-contact screening. Physiological, precise timing, optical-conversion and reconstruction capabilities retain separate requirements.
- Uses a brief check of actual incoming data; the thirty-second signal check is optional guidance. Reaching all-green is not required.
- Keeps finite flatness/clipping, baseline/amplitude and other quality findings visible. One **Record with cautions** action preserves them for analysis without repeated quality confirmation or freeform override.
- Distinguishes slow baseline movement from timing uncertainty. Missing data, identity/units errors, unusable timestamp progression and an unwritable Workbench run folder retain correction requirements.
- Preserves actual session purpose and historical labels. Quality cautions do not turn human recordings into bench runs.

## Forge and visualization

- Provides **Recording / Analyze / Results**, a persistent recording header, clear analysis cards and one current-operation area. Technical controls remain under Details.
- Makes the eligible dedicated Muse Zuna reconstruction comparison visible alongside optional Zuna Signal Review; generated signals and measured hardware QC remain distinct.
- Retains separate integrity, signal quality and analysis coverage, with exploratory full-recording and accepted-window results where supported.
- Enables original-timeline Time–Frequency viewing during XDF replay, including seek-history rebuilding, gaps and presentation-only playback speed.
- Adds raw optical QC, trends and slower spectra in live, replay and Forge. Relative HbO/HbR requires verified source-bound metadata; Athena concentrations are not guessed.

## Installation and documentation

Run **INSTALL.bat**, then **START_PRAYCG.bat** from the fully extracted release. Full installation includes Core, Live Monitor and Hardware Connectors. Optional Zuna uses its separate installer.

Read the [installation guide](INSTALL_AND_WORKFLOW_ALPHA_10_5_1.md), [recording/Athena guide](RECORDING_WITH_CAUTIONS_ALPHA_10_5_1.md), [Forge guide](ANALYSIS_FORGE_ALPHA_10_5_1.md), and [live/replay/optical guide](LIVE_REPLAY_OPTICAL_ALPHA_10_5_1.md). Current acceptance artifacts state observed checks and their physical/software scope.

Existing recordings, studies, reports and earlier releases are preserved. Alpha status remains; acquisition sign-off does not grant clinical or scientific outcome validation.
