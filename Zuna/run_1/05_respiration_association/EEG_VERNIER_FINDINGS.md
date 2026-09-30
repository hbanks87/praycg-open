> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Exploratory association, not proof that breathing caused drift or preflight failures.

# EEG–Vernier respiration comparison

Date: 26 September 2026. Run: `RUN_1`.

## Bottom line

The completed recording contains modest, channel-dependent EEG variation associated with the Vernier breathing signal. This supports breathing as a possible contributor to some of the observed variation. It does not establish that breathing caused all the slow drift, or caused the earlier preflight failures.

The strongest simultaneous linear associations were on channels 7 and 8 (Pearson r approximately 0.18 and 0.19). Channel 10 had the clearest frequency-specific association near the belt's dominant rhythm. Channel 16 had the largest breathing-band amplitude variation, but very little association with the belt under either linear or rank-based comparisons. This is a mixed result, not a blanket rejection or confirmation of the breathing explanation.

No PRAYCG application code, original recording, session status, or recorded timestamps were changed. Zuna inference was not run. This report is an exploratory recording comparison, not a Zuna validation result or clinical interpretation.

## What was compared

- The recorded 16-channel `obci_eeg1` EEG stream and `VernierRespirationBelt` force signal from the same XDF.
- The later eight evaluation blocks, avoiding the early interval with packet/timing anomalies. After filter-edge trimming, the analyzed interval was **420.4 seconds**, approximately seven minutes.
- The same **0.08–0.6 Hz** band on every EEG channel and on the belt. This tests breathing-range variation, not every form of slow drift or the full EEG spectrum.
- The belt's dominant spectral component was **0.20 Hz**, equivalent to about **12 cycles per minute**. This is a spectral estimate, not a manually verified count of every breath.
- Channel numbers are used because the saved EEG labels conflict with the Zuna protocol's electrode assumptions. Your report that you used your usual PRAYCG wiring was retained; an anatomical mapping was not silently substituted.

## Main measurements

Pearson r describes same-time linear association, from -1 to +1. Values near zero mean little linear tracking under this particular comparison. They do not prove absence of all physiological or mechanical relationships.

| Channel | Same-time Pearson r | Same-time Spearman rank correlation | Largest absolute Pearson r within ±3 seconds |
|---|---:|---:|---:|
| 1 | 0.060 | 0.104 | 0.098 |
| 2 | 0.003 | 0.012 | 0.064 |
| 3 | -0.035 | -0.040 | 0.091 |
| 4 | 0.032 | 0.032 | 0.104 |
| 5 | -0.046 | -0.075 | 0.106 |
| 6 | 0.042 | 0.044 | 0.079 |
| 7 | 0.180 | 0.21 | 0.206 |
| 8 | 0.186 | 0.18 | 0.185 |
| 9 | 0.004 | -0.01 | 0.071 |
| 10 | 0.140 | 0.132 | 0.239 |
| 11 | 0.051 | 0.047 | 0.157 |
| 12 | 0.066 | 0.063 | 0.157 |
| 13 | 0.067 | 0.055 | 0.143 |
| 14 | 0.031 | 0.047 | 0.113 |
| 15 | 0.131 | 0.090 | 0.160 |
| 16 | -0.015 | -0.017 | 0.067 |

The lag search uses a slightly shorter common interval than the same-time column; this explains the small difference for channel 8. Lag maxima are exploratory, selected on these same data, and are not validated predictive performance. Negative relationships count in the absolute maxima. Near-periodic signals can have several plausible lag peaks, so these lags are not physiological delay measurements.

The rank-based sensitivity analysis reduces the influence of a few very large excursions. It did not turn this into a strong, uniform association: the largest lag-searched rank association was approximately 0.27 on channel 7; channel 16 remained below 0.08.

### Consistency and frequency-specific findings

- Channels 7 and 8 retained positive same-time associations in both halves: channel 7, approximately 0.19/0.19; channel 8, approximately 0.20/0.17.
- Channel 10's same-time association varied substantially: approximately -0.07 in the first half and +0.29 in the second. Its magnitude-squared coherence at the belt's 0.20 Hz peak was approximately 0.41 overall, 0.39/0.52 by half. That is evidence of frequency-specific alignment in this sample, not a claim that 41% of all EEG or drift was caused by respiration.
- Channel 16's breathing-band standard deviation was approximately 51 microvolts, the largest of the 16 channels. Its same-time Pearson r was -0.015 and its largest lag-searched absolute r was 0.067. The large excursions on this channel were therefore not closely tracked by the belt in these tests. Nonlinear or time-varying respiratory effects are not excluded.

The figure shows three fixed channel examples and a block-by-block correlation overview. Blue is the belt; orange is EEG. Traces are standardized separately for shape comparison, so their plotted heights do not compare physical units. The heatmap's first and last blocks have less usable data because of filter-edge removal. The centered filter incorporates up to 30 seconds of neighboring data, so these are descriptive temporal windows, not independent or uncontaminated condition contrasts. EO means eyes open; EC means eyes closed. No formal EO-versus-EC contrast was tested here.

## Timing handling

The bridge diagnostics indicate that the published EEG timestamps ran approximately **1.315–1.365 seconds ahead** of the host-based endpoint estimate during the evaluation blocks; the median was **1.333 seconds**.

For this comparison only, a derived time axis was built from logged sample counts, missing-packet counts, and BrainFlow endpoint timestamps translated into host LSL time. This adjustment was derived independently of EEG–belt similarity: it was not chosen to maximize correlation.

Using host chunk-arrival times instead produced essentially the same associations. A ±250 ms timing sensitivity check retained the broad conclusion, although individual correlations changed. For example, channel 10 ranged from approximately 0.088 to 0.187, and channel 16 from -0.034 to +0.009. Uncorrected timestamps materially changed phase and correlation, which is why they were not treated as a reliable same-time comparison.

This is not a physical sensor-latency calibration. BrainFlow's host-derived timing and the Vernier sensor's unmeasured latency limit claims about exact delay or direction of influence.

## What this cannot answer

1. **Whether breathing caused each failed 30-second preflight.** Those attempts saved EEG samples but only aggregate Vernier statistics, not the paired raw breathing traces. The analyzed XDF interval occurred later.
2. **Whether all slower drift was respiratory.** This comparison does not cover drift below 0.08 Hz, and the later recording is not interchangeable with the earlier failed captures.
3. **Whether an association is neural or mechanical.** Shared timing can arise from different mechanisms; these comparisons do not identify the mechanism.
4. **Whether this run should automatically pass all quality gates.** Association with breathing does not by itself validate a recording, and an amplitude threshold alone does not identify the cause of a warning.
5. **A population-level effect or causal percentage.** This is one recording, with autocorrelated samples, exploratory choices, and channel/lag comparisons. No percentage of drift caused by respiration is claimed.

## Implications for the Workbench

The earlier recommendation still stands: separate transport integrity, flat/clipped/nonfinite signals, slow drift, and analysis-specific quality requirements. A slow-drift warning should explain the measured issue instead of presenting it as a diagnosis of poor electrode contact. It should not automatically erase respiratory-linked variation or grant an unconditional pass.

For future preflight diagnosis, save synchronized raw snippets from both EEG and the selected respiration stream, with explicit source identities and timestamp diagnostics. A respiration-association report could then supplement quality review without pretending to determine the cause conclusively.

## Reproducibility notes

Raw XDF timestamps were loaded without clock synchronization or de-jittering. EEG was low-pass filtered at 3 Hz before interpolation onto a common 10 Hz grid. The breathing-band filter was a 601-tap symmetric Hamming FIR; 30 seconds were discarded at each end to remove its finite-support boundary effects. Spectrum and coherence used 60-second Hann windows with 50% overlap, giving 13 windows for the full interval and six in each half. Correlation, rank correlation, and lag searches used the same declared band; no rereferencing or artifact rejection was applied.

Circular-shift diagnostics are preserved in the machine-readable result. They use a circular statistic, whereas the displayed lagged Pearson results use trimmed noncircular pairs. A value of 0.002 means none of 499 sampled shifted comparisons exceeded the observed circular statistic after the stated +1 correction; it is **not reported as a formal p-value**, because stationarity and exchangeability have not been established. Small exceedance fractions do not imply large effect sizes.

Input hashes were checked before and after execution and remained unchanged. Full hashes, software versions, timing sensitivities, block results, and all numerical measurements are recorded in `respiration_eeg_comparison.json` beside this report. The original XDF SHA-256 is:

`1937dad998f3cf265df32d3e235429a877b3f650f64c4ffde1b7e3d642b7c303`

Analysis used NumPy 2.4.6, SciPy 1.17.1, and pyxdf 1.17.5. The adjacent figure is `respiration_eeg_comparison.png`.
