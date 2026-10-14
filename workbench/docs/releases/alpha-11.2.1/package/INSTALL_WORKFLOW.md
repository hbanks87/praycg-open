# Installation and workflow — PRAYCG Workbench - Public - Alpha 11.2.1

## Use the reporting fixes

For an existing Athena analysis, open its session in Analysis Forge Results and use **Explain existing results** to create a new explanatory derivative. This does not rerun analysis or unlock the plan. Historical reports remain intact. A newly generated local summary or optional AI explanation uses the improved evidence handoff; an already saved AI narrative is not silently rewritten. Creating another AI explanation still requires your confirmation and allowance.

New Athena executions also save **eeg_athena_scoped_summary_v1_3.csv**. Read its view and channel scope before comparing values. Accepted AF7/AF8 windows, all candidate windows and the full interval are different summaries, not independent confirmation. The all-four endpoint can remain unavailable while narrower descriptive results exist.

For a completed Synthetic Epiphany recording, select its recording and matched runner evidence, then **Run recommended analyses**. After Required QC, **Synthetic Epiphany — Recorded rating analysis** is recommended for that exact protocol. It can also be selected under Choose modules. It needs the matching canonical protocol manifest and JSON events, not usable EEG. If an old plan lacks the module, add it through a new analysis revision; keep the previous lock and outputs. Read the rating report and CSVs under Results.

The rating worker scores the last valid key in each completed observed rating window and preserves the earlier keys and rejection reasons. Unanswered or incomplete windows remain missing. All three comparisons are exploratory ordinal-category differences; no confirmatory primary outcome is chosen. The new rule is labeled post-hoc for existing protocol records. Fixed order, media differences and framing confounds remain limitations. This release does not alter the protocol or make it scientifically validated.

## Preserve the existing installation

1. Finish any recording and close the old Workbench before switching editions.
2. Keep the old installation and study folders intact. Extract this ZIP into its own new folder, not over the old folder.
3. Use **INSTALL.bat** in that outer release folder for setup, then **START.bat** to launch. Core setup includes NeuroKit2 0.2.13, mne-denoise 0.0.3 and PyWavelets 1.9.0 for the signal comparisons. They are not a separate optional add-on. Do not choose an optional Zuna reinstall or stimulus installation for this release.
4. Reopen your existing Study Workspace and confirm the selected recording. This build keeps existing settings/history locations; it does not copy studies into the release or rewrite old analysis locks.
5. If an existing plan was created with older code, retain its reports as historical evidence. A new execution uses a newly reviewed plan and current code fingerprints. Do not change old hashes to force compatibility.

This edition uses the independent public AI Assistant. It does not load or discover AUL. Provider configuration and request allowance are optional for local analysis.

## Select equipment and run an Athena task

1. Create or choose a reviewed equipment setup. The Atlas uses that active setup, not a device merely highlighted in the equipment tray.
2. Read **Recording** and **Intended result** in the Atlas. They refresh when equipment changes. Select the protocol and press **Use this protocol**.
3. Prepare its required materials and connect equipment. The motor-imagery task can record an exploratory Athena session without C3/Cz/C4; its central-electrode endpoint remains unavailable.
4. Run readiness, then **Confirm Session Setup → Mark Ready to Run → launch the runner**. Signal findings are stored automatically; no separate “Record with cautions” acceptance is needed for Athena.
5. Missing streams, ambiguous identities, unwritable destinations, active-run conflicts or unavailable task-critical inputs still need resolution. This policy does not enable an unreviewed feedback controller or bypass stimulation safeguards.

New sessions freeze the exploratory policy and hardware assessment alongside original preflight evidence. Prior runs are not relabeled. If a previous release's equipment setup is stale, review and rebuild it against this release's bundled definitions; do not manually edit hashes.

## Analyze a saved recording

1. **Open recording** and select the exact saved XDF. Check the displayed recording and run identity.
2. **Run recommended analyses**. Review the proposed work once. Required QC runs first when needed, followed by eligible registered analyses. No AI request is included. To select a custom set, use **Choose modules** after Required QC; **Advanced details → Check recording only** can run QC without the recommended analyses.
3. **View results**. The factual local summary is saved and displayed when the guided run finishes. Individual module reports remain in Forge Results. Completed-with-limitations, unavailable, blocked and failed outcomes remain distinguishable.
4. Optionally choose **Generate AI explanation**. Confirm the provider request. Saved derived measurements and context are sent, not the raw XDF. Numerical analyses are not rerun. Elapsed time and completion/failure remain visible. A failed AI request leaves numerical results and earlier reports intact and is never retried automatically.
5. Select a dated **Local summary** or **AI explanation** and press **Open report** for a readable HTML document. Historical reports can be opened without authorizing new execution. Their current-evidence status and source checks remain explicit.

Proposals, exact action previews, corrections and review decisions are under Advanced. Viewing or accepting a narrative does not validate an experiment or start a runner. Opening a saved report does not spend a provider request.

## Signal Quality & Cleaning Review (retained)

Use this review when you want to see what a recording contains, inspect a rejected interval, or compare cleaning methods before deciding what to use in a later analysis. It is a local review workflow, not a new recording or an AI request.

1. Open **Analysis Forge Results → Signal Quality & Cleaning Review…**. Confirm the selected recording, or use **Select recording** to choose the intended XDF.
2. Choose the **Stream** and **Channels**. Use Ctrl/Shift to select more than one channel. Check the channel labels, units, reference, time coverage and any missing-metadata messages before interpreting numerical results.
3. For an EEG comparison, choose the **Current recipe** explicitly: `athena_v1_2` or `standard_v0_1`. These identify the current processing transform to preview; they do not load or reproduce a previously locked derivative. Do not choose a recipe solely because its name resembles an earlier report.
4. For EEG cleaning, choose the displayed candidate, **Line Hz** and **Harmonics**. Both cleaning candidates are calculated for comparison. Use **Compare full recording**, or turn it off and enter an **explicit interval (s)** relative to the recording start. The selected support is recorded. The in-memory limit still applies to the loaded recording even with an interval selected. If it is exceeded, use a separately exported, source-documented bounded recording; nothing is silently truncated.
5. Press **Run comparison**. Compare original, current-transform preview, candidate and removed-signal views. Use **Play**, **Stop**, **−10 s**, **+10 s** and the display-window controls to inspect the same time span. **Common scale across views** helps compare amplitude; **Separate scale per view** can reveal small features but must not be mistaken for equal amplitude.
6. Inspect the ECG/respiration evidence and available tables. An unavailable result should explain which signal, units, duration or timing evidence is missing. A completed review does not mean every estimator produced a valid result.
7. To mark an operator exclusion, use **Operator exclusions**, set its start/end with the playhead controls, add it to the draft, then **Apply as new version**. This saves a new quality-review attempt. Earlier physiology and cleaning comparisons are marked not yet recomputed; press **Run comparison** to calculate them with the new exclusions. It does not delete XDF samples, alter a historical report or silently revise a locked analysis plan.
8. Use **Open saved report** to read the saved report for this review. Retain the source recording and the whole review output folder so source checks, evidence and derivative links remain usable.

The same capabilities are also registered as four managed analysis modules:

- **Signal quality and temporal-support review**
- **ECG, heartbeat and HRV review**
- **Respiration and measured-respiration RSA review**
- **Line-noise processing comparison**

These modules report evidence and limitations. They do not automatically authorize a downstream endpoint, adopt a cleaning method or modify acquisition.

### What the comparisons mean

ECG review compares the actual NeuroKit2 `neurokit` and `pantompkins1985` detectors, waveform quality and separately recorded correction candidates. Beat and interval/pair ledgers preserve original positions and rejection reasons. Mean interval, heart rate, SDNN and RMSSD comparisons state their measurement support. RMSSD uses only eligible original adjacent interval pairs: excluding an interval must not turn its former neighbors into a new pair. Sampled heart rate alone is displayed as a trend and is never converted into beat-to-beat HRV.

Respiration review compares the existing filtering/phase approach with NeuroKit2 breath, rate and phase estimates. Different phase conventions are identified. Relative amplitude is not measured tidal volume; movement flags are review aids, not diagnoses. Measured-respiration RSA is exploratory and requires eligible cardiac intervals plus compatible overlapping time support. Missing clock-uncertainty evidence is not replaced with an invented precision estimate. A belt-free ECG-derived surrogate is not treated as measured respiration.

Line-noise review runs the pinned mne-denoise spectrum-interpolation or fixed ZapLine candidate. Lower line-frequency power does not establish that a method preserved the signal of interest. Inspect the removed component and the same supported intervals, and retain the settings used. No candidate becomes the default simply because it looks cleaner.

Filters and estimators operate within eligible continuous segments; gaps and exclusions do not create new physiological adjacency. Window/support displays and synthetic calibration distinguish centered-window look-ahead and estimator persistence from a genuine physiological delay. These checks do not establish causality or validate an experimental construct.

## Live observer snapshots

Start the selected sources in Live Monitor, then open the signal observer. Inspect the named readiness reasons. Select supported sources explicitly; excluded sources remain identified.

Use **Save snapshot locally** to retain a derived quality window without an AI request. This is not a substitute for LabRecorder/XDF recording. Saved snapshots and explanations remain available in history. A saved historical snapshot can be explained explicitly, but a historical or late answer is never presented as current live status. Current-live freshness and identity requirements remain enforced. No explanation arms equipment or changes a protocol.

## Interpreting limited results

A failed four-channel endpoint does not imply all individual channels contain no information. Read the channel/pair-specific coverage and its limitations. Descriptive acceptance is an engineering screen, not proof of neural origin. A usable pair cannot stand in for an unavailable full-montage endpoint. The corrected interval/adjacency handling can change new HRV results; it does not rewrite historical results or declare them valid.

Adding modules preserves eligible prior terminal outcomes separately from successful prerequisites. An unavailable derivative still cannot satisfy a downstream requirement. Explicit retries remain explicit. New preprocessing attempts have separate output folders; older overwritten files are not silently reconstructed or accepted.

## Reports and privacy

Full-resolution physiological traces and other telemetry evidence are stored separately from the summary report for local inspection. The local review may therefore contain sensitive sample-level data even when the opening report looks concise. Default AI and results-review bundles exclude that full-telemetry evidence. Including it requires an explicit **private full-telemetry** export and a separate privacy/consent review; opening a review or generating an explanation is not permission to upload the raw recording. Derived summaries and channel/timing metadata can also be sensitive.

New review outputs are versioned derivatives. Source recordings, existing settings, historical reports and Zuna assets are not replaced by this workflow. Building and extracting the release have not installed it over an existing setup. Consult **BUILD_REPORT.md** for the actual software checks; neither a successful review nor those checks certify all features, hardware performance, AI explanations or neuroscience endpoints.

Each module retains its underlying technical report. Summaries explain the question, findings, meaning, supported conclusions, uncertainty and next steps where the implementation supplies evidence. Missing definitions or estimates remain missing. Reused measurements are not independent confirmation.

Large AI evidence accounts keep every module represented with explicit detail omissions. If even minimal metadata cannot fit, the request stops rather than silently dropping modules. Report source links are local, hash-checked document references. Public release archives contain no operator studies, API credentials, private history or real-recording QA artifacts.

