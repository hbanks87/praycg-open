# Optical / fNIRS review

Alpha 10.5.2 provides recorded optical sensor review for every protocol that saved an Optical/fNIRS stream. It preserves the original recording and saves a new analysis attempt containing raw trends, per-sensor engineering screens, descriptive statistics, and optional time–frequency views. EEG quality does not determine optical eligibility.

For the current Muse S Athena connection, the supported starting point is **raw optical review**. Raw optical channel values are not already oxygenated or deoxygenated hemoglobin concentrations. This release supplies no verified Athena wavelength or source–detector mapping.

## Everyday workflow

1. Stop the recorder and select the completed recording in Forge's **Recording** page.
2. Check the recording, then open **Analyze** and choose **Explore optical signals**.
3. Open the completed report from **Results**. Review individual sensors, timing, full-data statistics, and screened-data statistics together.

The default covers the complete recorded optical stream. Details can limit it to the prepared protocol window, choose a spectral preset, or identify an exact optical source when several were recorded. Older recordings containing only EEG cannot supply optical data retrospectively. Source choices and settings are bound to the recording and saved with the analysis.

An engineering screen is a reproducible check of recorded sensor behavior. It does not establish cortical origin, contact quality, oxygenation, or cognitive state. Saturation remains unassessed when verified instrument limits are unavailable. No optical amplitude cutoff is guessed, and EEG acceptance masks or Zuna output are not used to certify optical observations.

## Automatic offline spectra

Forge first tries 30-second windows, then 10 seconds, then 5 seconds if no complete longer window is supported by any sensor's full data. It uses one preset for both full and screened results. It never joins across gaps or silently mixes spectral resolutions. The original live/replay viewer retains its 30-second default; saved Forge datasets open with their actual selected preset.

The approximate frequency-bin spacings are 0.033 Hz, 0.1 Hz and 0.2 Hz respectively. Shorter windows describe faster changes but provide less information about slow variation. A first bin represents one cycle, not a confidently established physiological rhythm. The report gives the selected window, frequency range, resolution and supported columns per sensor. Recordings under five continuous seconds retain trends and statistics even when spectra are unavailable. A fixed preset is available for comparisons between recordings.

Positive recorded values can also be expressed as a percentage of a per-sensor median baseline. These are descriptive changes in the recorded numbers. Unknown offsets, gain changes and preprocessing can affect them; they are not verified optical density or hemoglobin estimates. Baseline failures are reported separately for each sensor.

## Live viewing and recorded replay

In Live Monitor, use the **Source** switch: **Live** or **Recording**. Under Live, find streams, select the exact EEG and Optical stream instances you want to observe, and choose **Monitor Selected**. The observer supports up to six selected streams; the time–frequency popup displays one selected sensor stream at a time. Selecting EEG alone does not also select Optical.

Under Recording, use **Replay Loaded Run** or **Choose XDF**. Replay displays the recorded streams on their shared synchronized recording clock. It does not publish an LSL outlet or acquire hardware. Play, pause, stop, seek, and playback speed affect presentation; they do not change spectral frequencies.

Choose **Time–Frequency / Optical trends**, then select the desired **Sensor stream**. Optical starts in **Optical trends** and retains the recorded native units. Use the channel picker to inspect a sensor. Optional heatmap and 3D sensor views use categorical channels rather than an anatomical brain volume.

The live/replay optical default needs approximately 30 seconds of regular native data and displays 0.033–2 Hz with a one-second hop and up to 120 seconds of history. The 0.033–0.5 Hz region describes slower variation; 0.5–2 Hz may contain pulse-related variation. These ranges do not identify a particular physiological cause. EEG retains its separate four-second, 1–40 Hz default. During optical startup, raw trends remain available while spectral history accumulates.

Seeking rebuilds spectral history from original full-rate samples. Timestamp holes remain unavailable. The optical native sample rate is estimated from original intervals and displayed alongside the declared rate; raw timestamps are not rewritten or resampled. Live uses a frozen startup estimate, while recorded replay and Forge use the recorded stream. Comparisons require matching actual rate, input scope, and processing settings.

**Pause display** freezes the popup's drawing while the observer continues receiving data. Closing the popup leaves acquisition and the parent observer operating. Switching Live/Recording closes the existing passive observer and selects the new viewing source; it does not stop the separate device connector or recorder.

## Saved files

Each attempt includes:

- A readable HTML report and optical trend plot.
- Source-bound JSON with input hashes, scope, channel identities, recipe, timing, and unavailable outcomes.
- Full-precision native optical values, original timestamps, relative recorded-value percentages, and separate selected-scope and engineering acceptance masks in an NPZ derivative.
- Full-data and screened-data spectral exports when supported.
- An index for opening completed spectral datasets in the shared native viewer.
- A versioned reusable instrument-profile identity and automatic recording binding when a profile matches.

When recorded accelerometer or gyroscope streams exist, their native traces provide motion context on the same recorded clock. Event lines use actual in-scope recorded markers or explicitly named LSL timestamps from the supplied event file. They do not infer cue compliance or attribute a particular optical fluctuation to movement.

Original recordings remain intact. Full-data and screened-data results answer different questions; a screen pass alone does not validate the measured physiology.

## Relative hemoglobin estimates

Relative HbO/HbR estimates can use a reusable, verified instrument profile matched to the recorded model, firmware, decoder version and channel order. The Workbench creates the recording binding automatically; users do not re-enter fixed hardware facts for each recording. The profile establishes channel pairing, wavelengths, source–detector distances, intensity behavior and extinction coefficients with hash-bound evidence. Biological pathlength assumptions remain explicit. Positive screened baseline coverage must cover at least 80% of the configured baseline duration and contain no unsupported timing or acceptance gap. Legacy verified recording-bound profiles remain supported.

The conversion uses natural-log optical density and a modified Beer–Lambert inversion. Results are relative concentration changes in µM, with full estimates and a separate screened mask. They do not establish absolute oxygenation, scalp coupling, or cortical origin. A missing or invalid optional profile leaves raw review available and reports why hemoglobin conversion is unavailable.

Optional verified `analysis_blocks` provide descriptive per-block HbO/HbR means, medians, sample counts, and observed sample exposure for full and jointly screened wavelength pairs. Blocks must be explicit, disjoint, and inside the bound analysis window. Without them, relative trends remain available and block response review is explicitly unavailable. This review makes no statistical or cortical response claim.

The bundled Athena profile automatically identifies the pinned BrainFlow raw optical route. Its conversion status is DRAFT because public specifications do not yet establish the recorded-column mapping, distances, offsets/gain behavior or supported firmware range. Its missing facts are listed in the report/profile; recording and raw exploration remain available.

See [the reusable profile guide](REUSABLE_PROFILE_GUIDE.md) for the new workflow and [the verified profile guide](VERIFIED_PROFILE_GUIDE.md) for the legacy schema. Do not invent an Athena mapping from channel count or channel numbering.
