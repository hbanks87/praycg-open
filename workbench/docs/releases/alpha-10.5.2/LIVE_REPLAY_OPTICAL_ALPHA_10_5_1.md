# Live, XDF replay and optical views

The optional viewer supports incoming EEG/optical streams and saved XDF replay. Its sensor axis names recorded channels; it is not an anatomical brain volume.

## Source and controls

- **Live**: choose **Find Live Streams**, select up to six exact stream instances, then **Monitor Selected**. Athena connection can open EEG automatically.
- **Recording**: choose **Replay Loaded Run** or **Choose XDF**. Use Play, Pause, Stop, timeline seeking, ±10 seconds and playback speed.

Choose a stream in **Sensor stream:**, then open **Time–Frequency / Optical trends**. Views include per-electrode heatmaps, 3D sensor volume, 3D surface, source comparison and optical trends.

Replay loads the recording's streams within its size limits. The popup displays one selected EEG or Optical source at a time.

Replay uses original timestamped samples. Seeking rebuilds history; gaps stay visible. Playback speed affects presentation, while frequencies use the recording's sampling rate. Replay does not publish an LSL outlet.

Replay Pause stops progression. The popup's **Pause display** freezes its plot while the observer continues receiving data. Closing the popup leaves acquisition/replay running.

## EEG and optical defaults

EEG defaults use four-second windows, half-second steps, 1–40 Hz and thirty seconds of history. Initial spectral columns need enough continuous samples.

Optical opens **Optical trends** by default. Trends use declared native units and work before spectral history is sufficient. Change the channel picker to inspect another sensor. Optical spectra use thirty-second windows, one-second steps, 0.033–2 Hz and two minutes of history. The slower 0.033–0.5 Hz and pulse-containing 0.5–2 Hz ranges are exploratory optical descriptions. Missing/unstable timing can make spectra unavailable while raw trends remain inspectable.

Live, replay and offline results agree when input timestamps, selected rate and settings match. Live rate estimation uses startup observations; replay/offline may use the whole recording. Their reported observation support and rate can differ.

## Athena raw optics and Forge

Include Athena's separate **Optical** stream in the XDF. It contains sixteen raw optical channels at a nominal 64 Hz. These are not sixteen independently validated brain measurements or already converted hemoglobin concentrations. [BrainFlow Athena documentation](https://brainflow.readthedocs.io/en/stable/SupportedBoards.html#muses-athena)

In Forge choose **Analyze optical recording**. The raw review reports channel names, units, timing/coverage, finite observations, flatness and variability, mean/median values, trends and full/engineering-screened spectra. Saturation remains unassessed when verified ADC limits are unavailable. Recorded acceleration/gyroscope context and explicit task markers appear where available. The original XDF is preserved.

Relative HbO/HbR requires an independently verified `optical_fnirs_profile_v1_0.json` attached to the run or governed analysis inputs. It binds the run/XDF/source and requires explicit wavelength pairing, measured source/detector positions, intensity scaling, pathlength factors and extinction coefficients with source references. The backend computes relative concentration changes using those declared assumptions; no standalone profile editor or automatic Athena mapping is provided.

Athena's current raw stream has no automatically verified conversion profile, so HbO/HbR remains **UNAVAILABLE** with missing metadata explained. The workflow does not infer concentrations from unnamed values or apply EEG frequency bands to optical data. See the [MNE fNIRS processing workflow](https://mne.tools/stable/auto_tutorials/preprocessing/70_fnirs_processing.html) for raw intensity, optical density and hemoglobin distinctions.

A verified profile with explicit valid analysis blocks can also report full-window and jointly screened relative concentration summaries for those blocks. Missing block definitions leave that outcome unavailable. These are descriptive observations; they do not establish a statistical or cortical response. The [verified optical profile guide](Optical_Signal_Review_v1_0/VERIFIED_PROFILE_GUIDE.md) documents the professional metadata requirements.

See the [Forge guide](ANALYSIS_FORGE_ALPHA_10_5_1.md) and [installation guide](INSTALL_AND_WORKFLOW_ALPHA_10_5_1.md).
