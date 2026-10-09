# Visual Analysis in Alpha 10.5.4

Visual Analysis links recording review, spectra, state landscape and timescale inspection through one source identity and recording cursor. It displays supplied measurements and supported derived values. The landscape metaphor is not evidence of a physical force or semantic state.

## Navigation and source selection

In Analysis Forge the **Visual Analysis** tab follows **Analyze**. In Live Monitor its button sits next to **Time–Frequency**. **Visual sources** opens the source-selection dialog even while a recording is loading, then updates when recorded streams arrive. Use it to declare actual channels, units and the calibration interval; setup failures stay visible in the dialog.

## Three connected capabilities

| Capability | What it does | Boundary |
| --- | --- | --- |
| Completed review | Attaches a supported saved JSON to the selected recording and offers four native views. | Full-recording estimates stay retrospective. Recording and payload identity are checked. |
| Recorded prefix replay | Feeds recorded EEG and optional RR through the same incremental engine used live. | Only source data already available can affect the result. Seeking rebuilds history. |
| Passive live viewing | Consumes explicitly selected streams with fixed source mapping and calibration. | Issues no hardware commands and supplies no missing semantic measurements. |

The views are **PRAYCG 3 Review**, **Time–Frequency**, **State landscape** and **Timescale inspector**. **Open original video / PRAYCG 3 review** retains the existing review layout. **Open full TFR explorer** retains the spectral tool. A cursor link requires compatible recording identity and an explicit clock relation; unsupported CSV/media mapping is not silently treated as aligned. Paired panels use the same selection and represented time.

Recording playback uses one transport. Live **Pause** holds the displayed observation time while the passive observer continues; older TFR features remain selectable within that held snapshot. **Play** returns the linked views to the newest state. Original video-review scrubbing sends a verified shared selection; incoming shared selections do not echo requests.

## What the surface represents

**CAI · completed model** and **NIP · historical alternative** display authentic fields from compatible completed results. Definitions and qualifications remain those of the producing analysis. These fields are not interchangeable with raw EEG power or heart rate. A retrospective source cannot be made causal simply by hiding later rows.

**Autonomic state · experimental** uses eligible RR data after calibration. Its signed input is an exploratory API-A: one half of baseline-normalized log RMSSD minus baseline-normalized heart rate. Larger API-A produces a larger inward state displacement. Display depth is max(0, tanh(API-A / 2)), with the same fixed mapping throughout the session. This is not the frozen CAI model or a validated absorption measure. Descriptive autonomic residence measures eligible time above its declared threshold; it is not CAI-SID.

Surface and marker use the same represented time. Missing measurements do not receive zero-valued replacements. Media landmarks are annotations, not evidence of gamma events or instructions to manufacture physiological loads. The display does not infer a semantic anchor from its own geometry.

## Timescales and availability

| Quantity | Default incremental recipe | Availability |
| --- | --- | --- |
| Gamma | Mean power over declared P7/P8, 30–45 Hz; trailing Hann periodogram, linear detrending. | Complete window and calibration required. |
| Theta | Mean power over declared Pz/P3/P4, 4–8 Hz; same estimator. | Broad support limits short-lag interpretation. |
| Spectral support | Nominal 504 ms window, 24 ms hop; exact samples depend on rate. At 125 Hz: 63 and 3 samples. | A 24 ms refresh is not 24 ms independent resolution. |
| Gamma event | Upward crossing of gamma z = 2.5; 1 second refractory interval. | A threshold event, not a gamma cycle or meaning label. |
| Fast theta response | Mean +0.5 to +1.0 seconds minus −1.0 to −0.5 seconds relative to event. | Pending until response data are available; missing if support fails. |
| Slower theta response | Mean +8 to +30 seconds minus −5 to −1 seconds. | Separately pending until +30 seconds and required support. |
| Cardiac features | Trailing 30 seconds; at least 20 eligible RR beats and 90% coverage. | No instantaneous HRV or forward-filled cardiac values. |

Gamma and theta z scores use an explicitly selected fixed calibration interval, defaulting to the first 60 seconds of the shared recording clock. At least 30 seconds of valid EEG feature support is required. Center is the median; scale is 1.4826 times median absolute deviation, with a 0.1 log-power floor. Cardiac calibration requires at least 15 eligible one-second windows in the fixed interval; HR scale has a 1 bpm floor and log RMSSD a 0.1 floor. Missing calibration is not replaced by a fit to later data. Saved source and recipe settings identify departures from defaults.

The setting `config.calibration_start_seconds` is a nonnegative offset from the unchanged shared recording origin; its default is 0. The dialog can deliberately use the selected EEG stream’s recorded start as the baseline start. This changes the requested calibration interval, not the recording clock or alignment of EEG, RR, media and markers. Start, duration, valid support and availability remain explicit. A later start still must pass the same support and gap checks; it is not an automatic rescue after a failed calibration.

The revised method labels are `experimental_streaming_visual_state_v1_1` and `experimental_streaming_api_a_v1_1`. They remain experimental and distinct from frozen completed CAI/SID methods.

Local recording checks illustrate this limit. The Contact EEG starts about 344.1025 seconds after the shared origin, but the tested raw timing produced zero valid baseline support under strict gap checks. The October 8 Muse recording lasts 38.57 seconds; a deliberately selected 31-second baseline supplied only 21.73 valid seconds, below the required 30. Neither check established successful raw metric calibration. These recordings are not included in the public package.

Rows distinguish window start, center, end and availability. Represented spectral time is the trailing window end. Reception and clock mapping can add delay. Event time, response availability and cursor time are separate. There is no general one-second end-to-end latency promise.

## Quality and interpretation

Processing requires declared rate, units and electrode names. It preserves the received reference and does not silently re-reference or resample. Required channels, finite values, accepted masks, gaps, amplitude and step guards determine support. These guards do not replace measured EOG/EMG, contact assessment or artifact-reviewed analysis. Gamma remains vulnerable to muscle and eye artifacts. Shared envelopes, spectral windows and nonsinusoidal waveforms can also produce apparent cross-band relationships.

Raw EEG and RR do not provide complete MeaningGamma, TSP, task or semantic inputs. **CAI, NIP and CAI-SID are withheld in the incremental raw feed.** No substitute is filled into those fields. Reconstructions and spline signals in supported completed payloads retain their source labels and appear separately from measured EEG.

**Physiology event**, **Media landmark** and **Inspection only** are separate menus. Inspection bookmarks remain useful when a study has no qualifying events; they do not enter the event count. An empty event set can make response estimation unavailable. It does not falsify the proposed biology.

## Records and limits

**Source & methods** exposes identity, clock, calibration, fixed scales, support and recipe. **Save view record** preserves the review context, not all raw data or a replacement analysis bundle. The default display retains about two minutes; older seeks reset and rebuild rather than reusing expired live state.

Engineering checks cover future-suffix independence, rechunking, missing-data propagation and delayed availability. They do not validate narrative, consciousness or causal gamma-to-theta interpretations. See the [implementation and validation boundaries](UPDATE_TRACEABILITY_ALPHA_10_5_4.md).
