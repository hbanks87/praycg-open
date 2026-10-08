# Install and use PRAYCG Workbench Alpha 10.5.1

1. Extract the complete ZIP into a new local writable folder, keeping `app/` beside the public launchers. Do not run it from inside the ZIP; keep studies in their existing separate data folders.
2. Run INSTALL.bat. Native Windows Python 3.11 with Tk support and internet access for dependency downloads are required.
3. Run START_PRAYCG.bat. INSTALL_ZUNA.bat installs or imports the optional pinned model separately.
4. For an upgrade, use **Settings → Use Bundled Paths** to select this release's tools. Retain external PsychoPy choices and existing data roots; select the bundled LabRecorder for Workbench integration.
5. Select a protocol and prepare its materials. Choose **Connect Muse S Athena…**, select the discovered headset and **Connect**. Close other software owning its Bluetooth connection. Workbench selects the EEG stream and opens live EEG automatically; an address option remains under Advanced.
6. The connector performs its real startup timing calibration. The brief recording-readiness check then samples incoming data. OpenBCI launches also request the brief check automatically, and **Check Recording Readiness** is available for other selected routes.
7. Use the red/yellow/green signal map for adjustments. **Optional 30-Second Signal Check** provides longer guidance; all-green is not required. **Record with cautions** confirms setup while retaining findings. Enter operator/participant details and choose **Mark Ready to Run**.
8. Open LabRecorder, select the intended EEG and task markers plus desired auxiliary streams, choose its destination and start recording before launching the protocol. Include Athena's separate **Optical** stream for optical review.
9. When finished, press **Stop** in LabRecorder and wait for the XDF to close, then disconnect. Protocol completion does not close an externally operated recorder.
10. In Forge open the completed recording: **Recording → Check signal**, **Analyze →** choose the desired card, **Results →** open its report. The recording stays selected. Add optional condition/activity notes on Recording.
11. In Live Monitor select **Recording**, use **Choose XDF** or **Replay Loaded Run**, choose **Sensor stream:** and open **Time–Frequency / Optical trends**. Playback speed changes presentation only; gaps and original timestamps remain visible. Live monitoring uses the same optional viewer.
12. Optical trends work immediately; optical spectra need longer continuous history. Forge provides raw optical QC/trends/spectra. Relative HbO/HbR requires separately verified source-bound optical metadata; Athena concentrations are not guessed.

Missing required data, unresolved identity/units, unusable timestamp progression and an unwritable Workbench run folder still require correction. LabRecorder independently checks its selected XDF destination. Quality cautions travel with the recording; Forge retains separate integrity, quality and coverage descriptions, including exploratory full-recording and accepted-window results where supported.

Core only: INSTALL.bat -Mode minimal. Live Monitor repair: INSTALL.bat -Mode monitor. Connector repair: INSTALL.bat -Mode hardware. Read-only verification: INSTALL.bat -CheckOnly.

See the [recording/Athena guide](RECORDING_WITH_CAUTIONS_ALPHA_10_5_1.md), [Forge guide](ANALYSIS_FORGE_ALPHA_10_5_1.md), [live/replay/optical guide](LIVE_REPLAY_OPTICAL_ALPHA_10_5_1.md), [release notes](RELEASE_NOTES_v1_0_0_alpha_10_5_1.md), and [changelog](CHANGELOG.md).
