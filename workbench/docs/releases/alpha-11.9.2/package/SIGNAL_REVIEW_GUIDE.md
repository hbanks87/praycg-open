# Signal Quality & Cleaning Review

This release adds offline comparison tools. It does not establish that any cleaner improves your recordings, and does not change the normal acquisition path.

## A short workflow

1. Open **Signal Quality & Cleaning Review** in the Analysis Forge. Select the recording or reopen a saved `signal_review.json`.
2. Select the EEG stream and channels. Original recordings always remain available. Review channel/pair support, gaps, units and exclusions before comparing anything.
3. Select a current recipe and a candidate. Use a bounded comparison interval for long recordings. Line-noise settings apply to the line-noise comparison, not to SPAR's artifact classification.
4. For ICA or ASR, open **Processing / pairing settings**. Enter a fit interval in seconds from the recording start. ICA defaults to removing nothing. Inspect its components before entering any zero-based component indexes for a new removal preview. ASR requires a deliberately reviewed clean calibration interval of at least 30 seconds, not an automatically selected segment.
5. Press **Run comparison**. Results and private full-resolution derivative arrays are saved as a new attempt. The original, current transform, selected candidate and removed signal remain distinct.
6. Open **Processing research → Inspect selected pass / ICA components**. SPAR shows pass output, heuristic detection weights and correction strength on separate scales. ICA shows channel loadings, source traces and spectra. No unmeasured scalp geometry is invented.
7. If a candidate warrants further study, press **Save reviewed candidate**, recording your name/pseudonym and reason. This produces an immutable receipt. It does not improve raw QC, unlock a plan, remove the original, or qualify connectivity.
8. Under **Processing research**, choose a comparison and run it. Select original-only input or explicitly select a reviewed-candidate receipt. Use **Open saved report** to inspect numerical evidence and available figures. Each saved review preserves links to these comparisons. These are additional exploratory derivatives, not silent amendments to a locked plan.

## Optional methods

Run `INSTALL_SIGNAL_EXTRAS.bat` from the outer release folder to install ASR, ICLabel and Pycrostates into this release's separate `.signal-review-env`. This is optional and requires downloading upstream packages. It does not modify Core or Zuna. ASRpy's tested NumPy 2 incompatibility is the reason for isolation. ICLabel's intended 1–100 Hz preprocessing is unavailable on a 125 Hz recording; unavailable results are not replaced with invented probabilities.

Core ICA, the native SPAR candidate, spectral/ERP/TFR/connectivity/complexity comparisons and the existing signal review remain separate from this optional installation. [Detailed method settings and file-based worker usage](app/tools/Signal_Review_v1_0/EEG_EXTENSIONS_USAGE.txt) include participant-level comparisons and group-separated decoding.

Microstates require separate fit and evaluation sample ranges. Use **Load advanced comparison settings JSON** in Processing settings. For example, a reviewed settings file can contain `research_settings` with `fit_range`, `evaluation_range` and a fixed `seed`. These indexes refer to original source samples unless a specifically selected candidate supplies a bounded input; consult its receipt. Do not overlap training and evaluation ranges.

Advanced settings also support `spar_settings`, `rsa_comparison`, `rsa_maximum_windows` and `advanced_hrv`. These are data-only JSON settings, not executable code. Method-specific validation rejects unsupported combinations.

## Pairing and events

Cardiac–respiration coupling and reference-assisted correction require explicit source/channel pairing, a participant pseudonym, reviewer, supporting reason and timing uncertainty/tolerance. A common clock alone is not evidence of a common participant. A pairing declaration cannot override a conflicting recorded identity or repair clocks. Reference regression currently requires aligned timestamps; it is PRAYCG linear regression, not iCanClean.

Event comparisons require a separately reviewed JSON file with `source_sha256` matching the recording and an `anchors` list. ERP/TFR entries require `timestamp`, `source` and `independently_identified: true`. Autonomic entries require `time`, `source` and `origin` of `independent_stimulus` or `operator_independent`. Do not convert a physiological peak into an independent stimulus anchor merely by labeling it that way. Baselines, epoch/window support and rejected events remain visible.

Saved exclusions can be retracted as a new version using **Retract saved exclusion**. To correct one, retract it and add its replacement in a later version; earlier decisions remain traceable. Changed annotations invalidate previous comparison branches in the current view without deleting their saved files.

## External recordings

EDF/BDF, EEGLAB and BrainVision imports preserve source/sidecar hashes, recorded events, units and discontinuities. Supply the actual external study, participant and session identity. No PRAYCG protocol is invented for imported data. Unknown channel types must be resolved through the documented import API; do not relabel a non-EEG channel merely to enable a cleaner.

## Evidence and privacy

Reports explain numerical changes, not just a generic caution. Every substantive value points to a saved result or array. These calculations are deterministic local software; neither the Public AI Assistant nor AUL chooses a cleaner or silently recomputes statistics. Their existing explanation workflows can review accepted result summaries with explicit request authority.

Full-resolution candidate/component/physiology arrays remain private telemetry. A report, source identity or pseudonym can still be sensitive. Review privacy and consent before exporting or sharing anything. Raw files, older reports and original locked plans remain untouched.

The SPAR synthetic benchmark found unwanted clean-signal changes. Its reference candidate is a native port with unestablished MATLAB equivalence; its preservation variant is a deliberate modification, not a uniformly superior method. Delayed replay tests are not qualification for live acquisition. See [the complete 37-item scope](RELEASE_SCOPE_37.md).
