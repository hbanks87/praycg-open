# Recording and analysis policy — Alpha 10.3.5

Greater tolerance at recording level; precise checks at analysis-window level; transparent exclusions.

Recording permission, signal quality, sample continuity, physical event timing, computation and scientific interpretation are separate evidence layers. An acknowledged warning neither enables BENCH nor grants analytical validity. Original recordings, warnings, participant/BENCH designations and frozen endpoints are not rewritten.

## Acquisition

The shared quality engine preserves slow-drift, mains/variability, partial channel-integrity and timestamp findings. Localized faults, short nonempty captures, reduced observed rate and future-clock discrepancies can be warnings. No required EEG, wholly unusable required channels, no usable timestamp intervals, malformed mapping, wrong identity/units and essential requirements remain blocking. Explicitly reviewed optional/supplemental streams may be absent; required primary sources and markers cannot be relabeled optional by a report.

Daisy counters use their declared stride. Counter skips estimate missing delivered samples, not independently proven physical radio-packet loss. Timestamp gaps are separate observations. The publisher retains clock-domain/reset/order safeguards rather than fabricating corrected timestamps. No universal acceptable loss percentage is asserted.

Each new report exposes recording readiness, its policy version, blocking and warning codes, dimensions and evidence. Acknowledgment freezes report hashes and exact findings. Historical reports are interpreted under their recorded policy; old FAIL records do not become new PASS records.

## Segmented EEG analysis

Continuous regions are identified by the configured timestamp-gap rule. Each is independently filtered, with declared edge exclusions and original timestamps preserved. Outputs include segment IDs, observed retained/excluded samples, sample-equivalent seconds, boundary policy and reasons. Missing time is not counted as observed data. Segment arrays may be stored together, but temporal estimators cannot cross their boundaries.

Spectral, complexity, PAC, connectivity, microstate, event-related, RSA and motor-imagery consumers use qualifying windows/epochs. Microstate transitions never connect distinct segments. Train/test fitting remains separated; CSP uses training-only covariance-range whitening where common-average reference reduces rank. Frozen event/recipe requirements remain in force.

Current conservative limit: the general EEG source loader still refuses nonfinite EEG or invalid/nonmonotonic clocks globally rather than guessing how to repair them. The Zuna reviewed block route can reject affected evaluation blocks without calibration faults vetoing intact blocks. Five-second filter guards reduce edge effects but are not proof of artifact-free physiology.

## Zuna

Legacy v1 keeps its frozen method. An incompatible historical recording uses a new explicit post-hoc review. Native reviewed-montage and historical reviewed routes assess all eight declared evaluation blocks separately; calibration is not part of the scored endpoint. The all-eight-block endpoint still requires all eight. Any alternative reduced-block endpoint requires a separately declared method, not silent selection.

Preparation is not inference. Execution success is not improved reconstruction. Hidden measured electrodes are comparison targets, not clean neural ground truth. Template geometry, clipping, approximate historical clock mapping, filtering, normalization and context boundaries remain limitations. Old comparison results remain intact even if a new method later differs.

## Optical timing

The new optional optical variant emits fixed pre/post patterns outside scored content. Detection independently measures sampled light transitions, validates pattern and selected source/channel, checks missing/extra edges and continuity, and reports discrepancy from display-flip markers. Sampling brackets are not calibrated sensor-response confidence intervals.

Pre/post measurements do not certify every intervening transition or rule out temporary clock changes. ALS cannot recreate absent EEG, measure acoustic onset or prove eye-state compliance. OpenBCI ALS shares its acquisition route with OpenBCI EEG; a different device's ALS does not independently certify that EEG clock. The original timestamps remain unchanged; no optical estimate is silently applied as a universal correction.

## Reporting

Execution state, module quality assessment and inherited cautions remain separately visible. Every selected module has a persistent report or an explicit explanation of unavailability. A module that never ran has no new quality assessment. Research bundles preserve these distinctions, not just successful outputs.
