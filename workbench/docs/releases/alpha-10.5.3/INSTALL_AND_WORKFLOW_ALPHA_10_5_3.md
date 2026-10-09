# Install and use Alpha 10.5.3

1. Extract the complete release into a new writable folder. Keep the app folder beside the public launchers.
2. Run **INSTALL.bat**. Normal installation includes Core, Live Monitor and Hardware Connectors. Keep the installer output if any component fails.
3. Run **START.bat** or **START_PRAYCG.bat**.
4. Use the normal device connection and recording workflow. For Athena, adjust contact using the red/yellow/green map. The optional thirty-second signal check provides guidance; recording readiness checks actual incoming data briefly.
5. Confirm the recording setup. **Record with cautions** retains finite quality findings. Start LabRecorder, run the protocol, and **Stop LabRecorder** when finished so the XDF closes.
6. Open the recording in **Analysis Forge**. Existing **Analyze** and **Results** workflows remain available. The new **Visual Analysis** section opens linked views.

## Recorded Visual Analysis

Select the intended XDF in Forge, then open **State landscape**, **Timescale inspector** or **Paired well + TFR**. The monitor supplies playback and one recording clock. Choose **Visual sources** to select the exact EEG stream and optional RR stream, declare EEG units and electrode names, and select calibration. Generic channel numbers are not treated as electrode positions.

Allow playback to fill calibration and measurement windows. **As seen live** uses only the recording prefix available at the playhead; a backward seek rebuilds the engine. Playback speed changes presentation time, not the recipe. Unsupported, missing, warming-up and stale data remain explicit.

For a separately produced compatible result, use **Attach completed visual analysis…**, select its JSON, then **Open attached completed view**. The attachment must verify against the selected recording and is checked again when reopened. A saved view record documents the review; it does not replace the underlying analysis payload. Historical estimates requiring the full recording remain **Completed analysis** and are withheld from **As seen live**.

## Passive live views

Start the normal Live Monitor and use **Visual sources** to configure selected EEG and optional RR inputs. Open **Visual Analysis** after selecting sources. The visual feed consumes incoming samples and does not start acquisition, stimulation, a new outlet or recording. Missing identity, electrode mapping, units or required channels is reported instead of guessed. Source changes reset calibration and history.

Use **Source & methods** to inspect source, timing and recipe. **Save view record** records selection, source identity, calibration and display context. See the [Visual Analysis guide](VISUAL_ANALYSIS_ALPHA_10_5_3.md).

## Existing analysis and optional Zuna

The [retained Forge guide](../alpha-10.5.2/ANALYSIS_FORGE_ALPHA_10_5_2.md) describes Gamma Scalpel 2.0 and optical exploration. Save optical and optional measured EOG/EMG streams in the same recording when those analyses need them. Missing or ambiguous sources remain explicit. The bundled Athena optical profile supports raw exploration; relative HbO/HbR requires its missing conversion information.

Optional Zuna installation uses **INSTALL_ZUNA.bat**. Generated channels remain reconstructions and do not count as independent measured electrodes. The visualizer does not expand earlier reconstruction or hardware qualifications.

Read the [release notes](RELEASE_NOTES_v1_0_0_alpha_10_5_3.md) and [implementation and validation boundaries](UPDATE_TRACEABILITY_ALPHA_10_5_3.md). This is a complete release, not a hotfix installer. Keep earlier releases and studies in their original locations.