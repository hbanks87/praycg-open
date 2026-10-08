# Install and use Alpha 10.5.2

1. Extract the complete release into a new writable folder.
2. Run **INSTALL.bat**. The normal installation includes Core, Live Monitor and Hardware Connectors. Keep the installer output if any component fails.
3. Run **START_PRAYCG.bat**.
4. Connect Athena through the normal Muse connection action. Use the red/yellow/green map to adjust contact. The optional thirty-second signal check is guidance; recording readiness checks actual incoming data briefly.
5. Confirm the recording setup. Use **Record with cautions** when quality findings are present. Start LabRecorder, run the protocol, and **Stop LabRecorder** when finished.
6. Open the recording in **Analysis Forge**. Choose **Gamma Scalpel** or **Explore optical signals** under **Analyze**, then open the report in **Results**.

The optical stream must be selected for recording to support later optical analysis. Cerelog EOG/EMG must also be saved in the same recording for automatic reference discovery. The Workbench reports missing or ambiguous sources explicitly.

Optional Zuna installation uses **INSTALL_ZUNA.bat**. Read the [Forge guide](ANALYSIS_FORGE_ALPHA_10_5_2.md), [release notes](RELEASE_NOTES_v1_0_0_alpha_10_5_2.md), and [Athena optical information review](ATHENA_OPTICAL_SOURCE_REVIEW_ALPHA_10_5_2.md).

The complete package contains no hotfix installer. Existing studies and earlier releases remain available in their original locations.
