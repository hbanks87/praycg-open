# PRAYCG Workbench - Public - Alpha 11.2.1

## Athena reporting, AI handoff and recorded ratings

- Separates completed calculation, available descriptive measurements and strict all-four-electrode coverage. Unavailable strict endpoints still do not authorize downstream prerequisites.
- Adds a scope-aware Athena CSV with channel/pair/all-four, accepted/all-candidate/full-interval views, units, sample support and source references. Legacy exports explicitly identify their all-four scope.
- Includes saved partial-channel measurements in plain-English explanations and AI evidence, with exact source fields. Bounded packet omissions remain visible; summaries do not replace complete native reports.
- Rebuilds explanatory derivatives from existing results without changing source outputs or unlocking an old plan. Fixes verified-reuse receipt attribution and misleading incomplete-workflow wording for terminal unavailable outcomes.
- Adds Synthetic Epiphany rating analysis for resonance, absorption and perceived authenticity. It uses the last valid key within each completed rating window, preserves every response and exclusion, and reports missing values rather than zeros.
- Saves individual ratings, three ordinal category comparisons, source fingerprints, a response ledger and readable reports. No EEG-quality prerequisite, inferred emotion, automatic p-value or causal claim is added.
- Labels the newly specified historical rating rule post-hoc. Original protocol text, order, media and installed extension are unchanged.

Public retains the PRAYCG AI Assistant without AUL. No new runtime dependency or provider request is required for these local analyses. See BUILD_REPORT.md for verification and INSTALL_WORKFLOW.md for the existing-result workflow.

## Retained from Public Alpha 11.2.0

## Signal-review and physiological-evidence cycle

- Adds **Signal Quality & Cleaning Review…** to Analysis Forge Results, with selectable streams/channels, aligned waveform views, playback controls, explicit time support and saved review reopening.
- Adds four managed modules: **Signal quality and temporal-support review**; **ECG, heartbeat and HRV review**; **Respiration and measured-respiration RSA review**; and **Line-noise processing comparison**.
- Records source identity, channel types/units, reference, timing and continuous segments. Unknown or unsupported metadata produces an actionable unavailable result rather than a guessed measurement.
- Removes sampled-HR-to-RR fallback for HRV. HR-only streams retain descriptive heart-rate trends. Beat/interval and adjacent-pair ledgers preserve original adjacency, rejected values and reasons; deleting a bad beat does not create a new successive pair.
- Processes eligible continuous segments independently so filtering, peak detection, phase estimation and interpolation do not bridge missing-data gaps. Applies corresponding continuous-segment handling to the existing autonomic and master-suite paths.
- Runs actual NeuroKit2 ECG comparisons with two explicit detectors, waveform-quality estimates and separate correction provenance. Time-domain HRV comparisons identify the same accepted intervals and original adjacent pairs. This is not a frequency-domain or nonlinear HRV validation.
- Compares respiration processing with NeuroKit2 breath/rate/phase outputs. Relative amplitude and movement flags are not calibrated tidal volume. Measured-respiration RSA requires eligible cardiac evidence and overlapping compatible clocks; unknown clock uncertainty remains unknown. ECG-derived respiration is not substituted for a measured belt.
- Adds explicit temporal-support review and synthetic estimator-window calibration. Centered-window look-ahead and estimator persistence are identified as processing effects, not physiological onset or recovery.
- Separates available channel/pair descriptions from missing full-montage endpoints. A local descriptive result does not grant a protocol's intended scientific endpoint.
- Compares actual mne-denoise spectrum interpolation and fixed ZapLine candidates against original signals and an explicitly named current processing-transform preview. The preview does not replay a previously governed derivative. Removed components remain inspectable; reduced line power alone is not evidence that neural information was preserved.
- Saves operator exclusions as a new review version and new output attempt without modifying the XDF or earlier results. No candidate, annotation or narrative automatically replaces a locked analysis recipe.
- Separates full-resolution telemetry evidence from summary reports. Default AI and results-review exports exclude that evidence; full-telemetry sharing requires explicit private export and privacy review.
- Installs NeuroKit2 0.2.13, mne-denoise 0.0.3 and PyWavelets 1.9.0 through normal core setup. No separate optional comparison-library installation is required.
- Includes a read-only historical HR-fallback audit tool. It flags matching provenance for review and does not rewrite or retroactively clear historical analyses.

The public edition retains the independent PRAYCG AI Assistant and does not include AUL. See BUILD_REPORT.md for the completed verification scope and limitations. No installation over an existing Workbench, live hardware recording or provider request is implied by this release.

## Changes retained from Alpha 11.1.3

- The Atlas previews actual selected hardware before preflight, with separate Recording and Intended result columns, early missing-equipment notices and scrolling.
- Athena recordings are exploratory by default. Missing scientific endpoint electrodes/count/rate requirements do not prevent recording the task.
- The motor-imagery protocol can record Athena EEG without measured C3/Cz/C4; its central-electrode result remains unavailable.
- Nonblocking signal observations are saved without a repeated quality-acceptance prompt. New locks freeze a versioned policy, hardware assessment and original preflight evidence without inventing an operator override.
- Operational recording requirements, task-critical roles, source identities, participant binding, stimulation safeguards, ownership and output destination checks remain enforced.
- Compatibility previews distinguish missing measurements from evidence not yet collected and refresh when equipment changes.

See BUILD_REPORT.md for verification scope. No installation, real provider request or new physical-device validation was performed.

## Changes retained from Alpha 11.1.2

- Consolidated recommended/custom analysis routing through the shared native workflow.
- Automatic local summary after guided analysis, with optional explicitly confirmed AI explanation.
- Dated Local/AI history, automatic recovery, readable HTML opening and source links.
- Persistent terminal outcomes separated from successful prerequisite authorization.
- Channel/pair-specific descriptive availability without relaxing full-montage endpoints.
- Fair bounded AI evidence projection retaining every module, with explicit omissions.
- Six-question explanations, technical detail underneath, and truthful failed/unavailable states.
- Independent local quality-snapshot saving and explicit historical explanation.
- Named live-source readiness, explicit source subset, scrollbars and persistent review disposition.
- Separate output locations for new preprocessing attempts to prevent cross-recording overwrites.
- Targeted regression, isolated real-recording checks and public/private packaging verification; see BUILD_REPORT.md.

No installed settings, data or Zuna setup are changed by building these archives. Historical evidence is not rewritten. This release does not claim device validation, a scientific endpoint validation, or a fresh-machine installation test.

