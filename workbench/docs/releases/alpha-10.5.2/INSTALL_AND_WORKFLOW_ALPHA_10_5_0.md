# Install and use PRAYCG Workbench Alpha 10.5.0

1. Extract the full ZIP into a new local writable folder, keeping app/ beside the six public files.
2. Run INSTALL.bat. Native Windows Python 3.11 with Tk support and internet access for dependency downloads are required.
3. Run START_PRAYCG.bat. INSTALL_ZUNA.bat installs or imports the optional pinned model separately.
4. Connect Athena through the existing Muse workflow, use the signal map to adjust contact, and start Live Monitor.
5. Choose Live Time–Frequency for the optional spectral popup. The first columns require several seconds of continuous samples. Visual pause freezes the display while the observer continues receiving data.
6. Finish and save LabRecorder before offline analysis. Select the recording in Analysis Forge and choose Check signal.
7. In Time–Frequency Explorer, choose Analyze / explore. Continuous views retain the recording timeline and identify accepted support per electrode. Available event-related results retain their declared baseline and trial support.
8. Use the source and view selectors to inspect compatible saved processing results. A processing difference quantifies changed spectral power; it does not prove restoration of clean neural activity.
9. Compare compatible explorer reports, keeping channel, reference, method, units and support selection consistent. Actual eye/activity notes accompany the recordings.
10. Export a report or image to retain the chosen view and its source information.

Core only: INSTALL.bat -Mode minimal. Live Monitor repair: INSTALL.bat -Mode monitor. Connector repair: INSTALL.bat -Mode hardware. Read-only verification: INSTALL.bat -CheckOnly.

Keep studies separately from software releases. Refer to the [feature guide](TIME_FREQUENCY_EXPLORER_ALPHA_10_5_0.md), [release notes](RELEASE_NOTES_v1_0_0_alpha_10_5_0.md), and [changelog](CHANGELOG.md).
