# Time–Frequency Explorer in Alpha 10.5.0

Live Monitor and Analysis Forge share an independently implemented viewer. The three-dimensional axes are time, frequency and a categorical list of electrodes. The viewer retains actual channel names and does not infer anatomical brain locations between sensors.

| Requested addition | Implementation and interpretation |
|---|---|
| Optional live popup | The current selected EEG outlet supplies full-resolution samples. The visualizer follows the observer's source identity and has an independent display lifecycle. |
| Separate Forge module | A managed exploratory worker produces immutable saved numerical and visualization artifacts from the selected finalized recording and its bound analysis inputs. |
| Two visual layouts | Electrode heatmaps and a rotatable three-dimensional volume share selection, scales, method and source information. |
| Bounded live defaults | Defaults use four-second trailing windows, half-second updates and approximately thirty seconds of history. Available frequency limits and voltage units come from actual stream metadata. |
| Recording independence | Visual pause and close affect the display; the passive monitor continues to follow the existing acquisition lifecycle. Source changes and stale or discontinuous samples are explicit. |
| Continuous and event-based offline views | Continuous exploration follows the actual recording timeline. Saved event-related results retain estimator, baseline, trial support and source identities; missing prerequisites remain explicit. |
| Quality overlays | Per-electrode accepted support and artifact reasons accompany full measured data. Missing values and timestamp gaps remain visible rather than being concatenated. |
| Processing comparisons | Measured, conventional and eligible saved Zuna branches carry their method, units, reference and generated-sample information. Matched differences describe model or processing alteration. |
| Recording comparisons | Compatible reports use consistent channel, method, units and reference information. Support-selection differences remain visible, including accepted and equal-duration comparisons. |
| Region inspection | Selected time/frequency regions link to underlying values, waveform samples, timestamps and available quality reasons. Descriptive statistics show large-burst influence. |
| Clear display semantics | Stable comparable color scales, true frequency coordinates, electrode labels, source flags and explicit estimator names accompany the images. Visual thresholds control visibility. |
| Reproducible exports | Interactive HTML, static figures and full numerical artifacts preserve source and processing information. Display compression does not replace the numerical analysis artifact. |
| Validation | Known signals, normalization, baseline and edge support, gaps, source changes, per-electrode quality and observer workload are software acceptance subjects. Their evidence is independent of physical or physiological validation. |
| Full packaging | Normal full installers and source-bound distribution checks cover the complete release. The earlier recording tools and protocols remain included. |

Live short-window spectra and saved event-related Morlet results are distinct methods. Their units and normalization must be read with the view. Wavelet resolution varies with frequency; edge support and baseline prerequisites are part of an event-related result.

Hardware quality continues to use measured signals. Generated estimates are visibly labelled. A stronger or smoother spectral pattern does not by itself establish denoising, attention, mental state or a regional physiological endpoint.

The reviewed upstream concept: [eeg-tfr-volume](https://github.com/kolascoco/eeg-tfr-volume), commit 93b970d7a085b9d9967c0184e0d688adab1cfd13. No upstream source is included. The current build validation records implementation tests and their exact scope.
