# Analysis Forge: Recording → Analyze → Results

The selected recording stays visible while you check, analyze and review it. The header identifies the recording, verified device/duration and operator condition notes. Technical settings remain available under **Details**.

## Recording

Choose **Open recording**, then **Check signal**. Review integrity, electrode findings and available duration separately. Open the quality report for full-recording and accepted-window support.

Use **Recording conditions (optional)** for eyes-open/closed and activity notes. A protocol name does not establish what actually happened. Added annotations preserve the original metadata.

**Choose analysis →** opens the analysis choices. **Details — inputs and recovery** contains less frequently needed input and recovery tools.

## Analyze

| Card | Main action | Result |
|---|---|---|
| Signal summary | **Analyze measured EEG** | Athena measured EEG, quality and coverage. Other supported EEG uses **Analyze measured EEG — spectral summary**. |
| Time–Frequency Explorer | **Analyze / explore** | Electrode spectral views with timeline, processing details and quality support |
| Compare recordings | **Compare EEG summaries…** / **Compare time–frequency views…** | Comparisons with compatible channels, units, references and settings |
| Zuna comparison — experimental | **Run optional Zuna signal review** | Optional processing comparison with measured/generated signals labeled separately |
| Dedicated Muse validation | **Run Zuna reconstruction comparison — experimental**, when eligible | Reviewed Muse reconstruction-versus-spline comparison |
| Optical / fNIRS | **Analyze optical recording** | Raw optical QC, trends and spectra; verified metadata is required for relative HbO/HbR |

Zuna requires its optional installation. Generated signals preserve their provenance and do not improve the measured hardware QC label. Dedicated Muse comparison appears for recordings with the required contract and inputs. Older sixteen-measured-channel reconstruction protocols retain their electrode requirements.

Optical review includes recorded motion context and task-marker overlays where available. A verified optical profile can support relative hemoglobin and explicitly defined block summaries. Athena currently provides raw optical review; its wavelength/geometry mapping is not guessed. See the [verified profile guide](Optical_Signal_Review_v1_0/VERIFIED_PROFILE_GUIDE.md).

Plan, catalog and advanced controls are in collapsed **Details**. Analyses retain the existing governed plan/dependency/worker workflow; unavailable inputs or outcomes remain visible.

## Results

Results shortcuts open measured EEG/quality, latest Time–Frequency, latest Zuna and Optical/fNIRS reports for this recording. Plan result cards show completion status and an **Open** menu. Export, explanation and sharing controls are under **Details**.

The bottom **Current operation** area shows status/progress and available cancel, resume or retry controls. Results appear without losing the recording selection.

Full-recording exploratory and accepted-window results use different support. Review electrode requirements, timing and coverage before interpreting a difference. An unfinalized XDF is a recording-integrity issue; finish or recover it first.

See [recording with cautions](RECORDING_WITH_CAUTIONS_ALPHA_10_5_1.md) and [live/replay/optical views](LIVE_REPLAY_OPTICAL_ALPHA_10_5_1.md).
