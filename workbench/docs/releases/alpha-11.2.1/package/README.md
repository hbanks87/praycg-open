# PRAYCG Workbench - Public - Alpha 11.2.1

This patch repairs Athena reporting and the AI evidence handoff, and adds source-bound rating analysis for Synthetic Epiphany. A completed analysis can now show available channel-specific results without implying that its strict four-electrode endpoint succeeded. Existing saved Athena outputs can receive updated explanations without rerunning their numerical analysis.

Synthetic Epiphany's three rating comparisons are descriptive. The new response-selection rule remains explicitly post-hoc for existing protocol records. Its private protocol package, media and participant data are not distributed in this public build.

A local-first research workbench for protocol preparation, synchronized acquisition, analysis and reproducible research bundles. Alpha 11.2.0 adds a dedicated signal-quality and cleaning review inside Analysis Forge Results. It helps you inspect what was recorded, compare processing methods and understand which measurements the available signals can support.

Open **Signal Quality & Cleaning Review…** to compare source-aligned original, current-transform preview, candidate and removed-signal views. Choose the recording, channels, explicit processing recipe and time interval. Review ECG beat detections, accepted intervals, respiration and temporal support alongside EEG cleaning comparisons. Operator exclusions are saved as a new review version; the source recording and earlier results remain unchanged.

Four managed modules cover signal quality and temporal support, ECG/heartbeat/HRV, respiration/measured-respiration RSA, and line-noise comparison. NeuroKit2 and mne-denoise comparisons run the actual pinned libraries, not stand-in implementations. A current-transform preview is not a replay of a previously locked preprocessing derivative. No comparison automatically adopts a method or replaces a governed analysis recipe.

The Atlas separates **Recording** from **Intended result**. A motor task can record Athena EEG without pretending its missing central electrodes were measured. Signal observations are saved automatically; Athena no longer requires repeated quality-acceptance prompts. Missing streams, invalid identities, unavailable task-critical equipment and active-run conflicts still need resolution.

## Start here

Read **INSTALL_WORKFLOW.md**. Use **INSTALL.bat** for setup, then **START.bat** in this outer release folder to launch. Do not launch a historical script from inside app. See **CHANGELOG.md** for this release and **BUILD_REPORT.md** for the exact validation scope.

Setup includes the pinned comparison dependencies: NeuroKit2 0.2.13, mne-denoise 0.0.3 and PyWavelets 1.9.0. There is no separate optional signal-review installer.

The normal analysis path is **Select recording → Run recommended analyses → View results**. Choose modules is optional. Local summaries use saved numerical results; Generate AI explanation is a separate, explicit provider request. Reports remain dated, source-linked derivatives, not replacements for original results.

This public edition includes the independent PRAYCG AI Assistant and contains no private AUL implementation, history or evaluation data.

## Preservation and limitations

Building or extracting this package does not migrate or overwrite existing settings, recordings, analysis history, environments or Zuna assets. Extract into a new folder; never merge over a running installation. Installation is a separate operator action. No optional stimulus pack or Zuna reinstall is required by this patch.

Sampled heart rate supports heart-rate trends, not reconstructed beat-to-beat HRV. HRV uses eligible measured intervals and original adjacent interval pairs, with rejection reasons retained. Available single-channel or pair descriptions remain separate from an unavailable full-montage endpoint. Missing units, timing or required measurements are reported, not invented.

Full-resolution telemetry evidence is retained separately for local review. It is excluded from default AI and results-review bundles and requires an explicit private full-telemetry export. Derived summaries may also contain sensitive information and still require review before sharing.

This package has not been installed over your existing Workbench. Software checks do not certify every function, a physical device, an AI interpretation or a neuroscience endpoint. AI explanation does not rerun statistics or grant acquisition authority. Original attribution and license notices remain in the distribution.

