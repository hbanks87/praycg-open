# Signal preservation and analysis workflow in Alpha 11.5.0

This release adds explicit processing-input selection and numerical original-versus-candidate comparisons. A cleaner is a research candidate, not a quality certificate. Original recordings, locked plans, previous results and assistant history remain separate from new derivatives.

## Use the processing comparison

1. Open the exact recording in **Analysis Forge → Signal Quality & Cleaning Review**. Inspect channel and interval support. A missing full-group endpoint does not invalidate an available channel or pair.
2. Select channels, an interval and the current recipe. Save any exclusions as a new annotation version. Changing annotations invalidates previous candidate selection; recompute before adopting that version.
3. Choose a candidate and run the comparison. `spar_preservation_v2` is a new conservative policy: the slow pass stays unchanged without reviewed, same-participant motion evidence. The older `spar_preservation` and `spar_reference` remain available under their original identities.
4. Inspect original, candidate, removed signal, component/pass evidence and available support. A smoother waveform or smaller amplitude does not establish accuracy. **Save reviewed candidate** records the reviewer and selection reason without replacing the recording.
5. Under processing research, select **Original recording**, **Current recipe preview** or **Saved reviewed candidate**. The current recipe is a named transform preview, not an automatic replay of a locked historical derivative. Choosing it saves a separate reviewed input.
6. Select `compatible_suite` and run the comparison. Numerical workers produce separate spectral, complexity, connectivity, continuous TFR and gamma–theta reports where supported. Event ERP/TFR additionally needs independently identified source-bound anchors. Partial, unavailable and cancelled results remain visible beside completed results.
7. Open the branch report or an individual module report. Continuous TFR recomputes both inputs on common windows. Gamma–theta uses the original input's frozen calibration for both branches, so independently refitting the candidate cannot conceal its amplitude change. Neither is independent confirmation.

The paired TFR and gamma–theta route is bounded to 600 seconds and two million sample-channel values per comparison. Select a shorter interval or fewer channels when prompted; the software does not silently truncate a longer request. Calibration remains on the original recording clock and is not moved into a selected interval to make it succeed.

TFR also needs uninterrupted support for its selected window length. A default four-second window may not fit inside a guarded SPAR block. In processing settings, explicitly choose a shorter window, such as one second, when appropriate. Shorter windows give coarser frequency resolution; they do not restore missing samples or relax exclusions. Both comparison inputs use the same selected window and hop.

## Explicit reference evidence

In **Processing / pairing settings**, select the actual EOG, EMG or motion stream and channel. Declare the participant pseudonym, reviewer, pairing evidence and clock uncertainty. A shared clock label does not establish a shared participant. Optional offline alignment interpolates a reference only within supported pieces, never across gaps or beyond its recorded support. It does not alter EEG timestamps or create higher-frequency information.

**Review artifact-reference interval** records a deliberately reviewed interval from that independent sensor. Sensor availability alone is not an artifact label. EOG supports the ocular pass, EMG supports the muscle pass and motion supports the conservative slow pass. Saved comparison playback marks these reviewed intervals in amber. Detection and a decision to transform EEG remain distinct.

**Gamma–theta channel and calibration selection** lets the reviewer select actual recorded electrodes. This is an explicit descriptive analysis choice, not a substitution for missing canonical electrodes. It does not make sparse wearable EEG equivalent to a full montage.

## Playback scales and reports

Saved processing playback starts at a fixed ±100 µV. Change that physical scale explicitly or enable visibly labeled autoscaling. Original, current, candidate and removed-signal panels share the EEG scale. Time navigation never silently changes the fixed scale. Outside-scale values can be clipped by the plot; stored values remain intact.

Local processing explanations report actual supported duration, original and candidate RMS amplitudes, RMS difference and change-to-original energy ratio. That ratio is not a fraction of brain activity removed. Reports link numerical evidence and retain missing endpoints. Generating an additional model explanation remains an authorized operation; opening a report makes no provider request.

## Timing and convergence

Polar notification/arrival timestamps are not measured beat endpoints. Received-order RR summaries can remain useful, but precise event windows and cardiac–respiration coupling require appropriate beat timing. Historical outputs are not silently rewritten.

ICA stopping evidence distinguishes confirmed convergence, nonconvergence and unknown. Unknown stopping evidence permits component inspection but does not authorize unsupported component removal. Source/version changes cannot inherit a convergence proof from a different implementation.

## The fourteen item delivery scope

| Item | Delivery and evidence boundary |
| --- | --- |
| 1 RR timing | Explicit transport/interval semantics carried into bridge, analysis and replay consumers; order summaries kept separate from beat-aligned endpoints. |
| 2 ICA | Explicit convergence evidence with an exact-implementation observation path and restoration tests. Unknown is not renamed success or failure. |
| 3 SPAR slow preservation | Separately versioned v2 policy, pass evidence and adverse synthetic cases; old algorithms/results preserved. |
| 4 MATLAB parity | Bounded fixture import/comparison and pinned-source checks. Authentic MATLAB output is still required; numerical equivalence is unestablished. |
| 5 Analysis input | Original, current preview and saved candidate selection create separate analysis branches without plan mutation. |
| 6 Downstream recomputation | Real paired TFR and gamma–theta calculations plus existing matched spectral/connectivity/complexity comparisons. Paired CAI/SID feature regeneration is not implemented or validated; its exact missing prerequisites are reported, not replaced by raw bandpower. |
| 7 Playback | Explicit fixed microvolt scale and optional visibly labeled autoscaling. |
| 8 References | Explicit source/channel/participant/timing pairing, gap-aware cross-rate reference alignment, reviewed interval masks and saved comparison markers. A universal reference-overlay adapter for every legacy visualizer remains incomplete. |
| 9 Annotations and support | Branches bind immutable annotation identities and current source support. Existing legacy workers are not all automatically converted to consume an arbitrary new candidate; they remain outside this branch unless explicitly supported. |
| 10 Explanations | Measured per-channel change summaries, source links, original/candidate endpoint reports, and visible unavailable states. Automatic structured model explanation of every new branch has not been established. |
| 11 Optional tools | Actual synthetic numerical and external-format round-trip checks, separately documented in the build report. These do not validate physiology in human recordings. |
| 12 Controls | Reviewed source-bound control enrollment and explicit development/regression corpus roles. Independent real-world clean/contaminated labels must still be supplied; shielded data and Zuna reconstruction are not declared ground truth. |
| 13 Replay | Bounded, instrumented replay and cancellation tests. Physical live cleaning remains disabled; accelerated software replay is not a hardware latency certification. |
| 14 Both editions | Shared-engine workflow, reporting, reopening, boundary, updater and preservation checks. Installation and publication require separate actions. |

This is an implementation and validation-infrastructure release, not a claim that all fourteen research objectives are scientifically completed. The build report states which acceptance tests actually ran. No recording is treated as a fresh holdout after its results have been inspected.

## Existing data and Zuna

Use a new release folder. Keep external settings, workspaces, recordings, historical reports and the current Zuna runtime/model binding. Do not copy a new application over an old installation or a study folder. A verified updater may reuse a compatible runtime; keep the referenced runtime until a separate independent installation is verified. This package does not restore a dependency on a retired application folder by guessing a path.
