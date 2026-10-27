# Hardware routes in Alpha 10.2.1

Alpha 10.2.1 connects the exact 10.2.0 acquisition routes to the main Hardware Library, profile builder and locked launch actions. Their status is **experimental software validation**: no new physical devices were available for this build. Matching metadata does not establish calibration, timing accuracy or participant safety.

## Operator workflow

1. In Hardware Selection, set **Profile intended use** to **EXPERIMENTAL_EVALUATION**, explicitly confirm **Bench Test Mode (no participant)** and enter a reason. All newly integrated routes remain physically unverified.
2. Select the exact product/publisher in the Hardware Library and press **Validate and Add**. For an external route, start its publisher, select its live outlet and supply requested version, firmware, calibration and timing facts. Record unavailable firmware honestly. Managed routes provide a packaged connector; external routes provide publisher instructions and a reviewed attachment, not a bundled third-party application.
3. Review validation findings, create the hardware profile, then review and lock its draft. Missing labels/units, changed channel order, source-version changes, wrong presets and different products block the applicable contract. Required profile streams are distinct from optional generic observed attachments.
4. Start a fresh equipment session. In **Connect & Launch**, open the selected locked route's action. Managed routes open a restricted device panel; external routes recheck the selected live outlet. A restarted outlet requires re-review rather than silent substitution.
5. Inspect each modality, confirm the session, and select the required outlets and PRAYCG markers in LabRecorder. Record/reopen an evaluation XDF and check gaps, channel semantics and alignment.
6. Stop recording and stop PRAYCG-owned publishers through **Manage running connectors…**. Close external publishers yourself only when they are no longer used by any recording.

Library labels distinguish **connector implemented**, **external publisher required**, **physical testing pending**, and **withheld/catalog only**. Creating and locking an experimental profile does not promote it to participant acquisition. The existing reviewed hardware path and its readiness checks remain separate.

Binding evidence preserves original full XML, authoritative parsed identity, separately operator-asserted facts, source-derived units where applicable, and source references. It can contain device/network identifiers and must remain private telemetry under existing bundle exclusions.

## Included routes

| Product | Route | Boundary |
| --- | --- | --- |
| Crown | Shared BrainFlow connector | The programmatix repository is an LSL consumer. |
| Muse S Athena | BrainFlow plus optional external OpenMuse | Preset/version-specific; no ALS assumed. |
| Polar H10 ECG | Separate PRAYCG PMD ECG bridge | 130 Hz ECG waveform, not the existing irregular RR stream; absolute BLE delay remains unmeasured. |
| Pupil Core | Capture LSL Relay 2.3 scene gaze or pupillometry | Separate schema from Neon. |
| Pupil Neon | Companion built-in gaze/eye-state LSL | Freeze actual app version and observed XML. |
| GazePoint GP3 | PRAYCG Open Gaze API 2.0 bridge, selected 60 Hz | GazePoint Control must already run. |
| GazePoint GP3 HD | Same bridge, selected 150 Hz | API product identity must match. |
| OpenViBE | External LSL template | Exact driver/scenario/version/mapping evidence required. |
| Cerelog 16 | Withheld candidate and source evidence | Firmware route identified; physical contract unresolved. |

## GazePoint

The bridge is independently authored from the [Open Gaze API 2.0 specification](https://www.gazept.com/dl/Gazepoint_API_v2.0.pdf). It requests data fields but never changes calibration. Start GazePoint Control and perform appropriate calibration there.

The recommended entry point is **Hardware Library → the exact GP3 or GP3 HD route → Validate and Add → Create Hardware Profile → Review, Approve, and Lock Draft**, followed by the locked route's action in **Connect & Launch**. For manual bench diagnostics, open a terminal in the distribution's `app` directory and use its isolated hardware environment:

    .hardware-connectors-env\Scripts\python.exe tools/Acquisition/GazePoint_to_LSL_v1_0/gazepoint_to_lsl.py --model GP3 --sampling-rate 60 --run-uuid YOUR-SESSION-UUID --duration 30 --status-file PATH-TO-SESSION/gazepoint_segment1_status.json --stop-file PATH-TO-SESSION/gazepoint_segment1.stop

Replace the UUID with the actual valid session UUID and choose new segment paths. GP3 HD uses model GP3_HD and sampling-rate 150. The server defaults to 127.0.0.1:4242; host/port options permit explicit alternatives. Creating the chosen stop file stops the publisher. Existing status evidence is never overwritten on startup.

The 16 channels are CNT, TIME, TIME_TICK, LPOGX, LPOGY, LPOGV, RPOGX, RPOGY, RPOGV, BPOGX, BPOGY, BPOGV, LPD, RPD, LPV and RPV. Fields are selected by key independently of XML attribute order. Validity stays explicit. Missing invalid-eye coordinates remain NaN; missing valid data stops the segment. Coordinates are not clipped.

All channels use double64. Integers outside its exact range stop with an error. TIME_TICK remains ticks, with the API-reported frequency preserved in XML. LSL timestamps mark TCP record receipt; source TIME/TIME_TICK stay separate sample channels. No uniform replacement time or hardware synchronization is invented.

Status reports sample count, counter gaps, source-time span and observed samples per source second. Configured rate is labeled configured, not measured. Disconnects, stalled TCP reads, malformed data, product mismatch, counter reset and backward source clocks stop the bridge. Each new process gets a separate segment UUID/source ID. An OS endpoint lock prevents duplicate PRAYCG owners and is released on crash.

The reviewed [hynchl script](https://github.com/hynchl/lsl-gp3/blob/9bd790d98fc0d9e6256a58cd4d326bd5ebc926d9/gp3-to-lsl.py) was not adopted: XML attribute order controls samples, cursor/blink metadata order can disagree, and float32 can lose timing-counter precision. No source from that script is redistributed.

## Optional OpenMuse

[OpenMuse 0.1.8, pinned commit a9be252](https://github.com/DominiqueMakowski/OpenMuse/tree/a9be252188321e269537eabf609bc207be293f8c) requires Python 3.12+ in a separately managed environment. This release does not install or redistribute it: the inspected tree has an MIT classifier but no inspected license grant file.

Four profiles attach separately: EEG 4/8 channels at 256 Hz, ACCGYRO 6 at 52 Hz, optics 4/8/16 at 64 Hz and battery 1 with published nominal 0.2 Hz. Presets determine EEG/optics shape. Actual names follow Muse-EEG (device-id) and analogous sensor names. Extra AUX labels are not automatically scalp EEG electrodes.

For Athena preset **p1041**, the OpenMuse EEG outlet may contain four named electrode channels plus four AUX channels. PRAYCG preserves those eight published channels and their labels; it does not treat them as eight verified EEG electrodes. Review which channels belong in each analysis before locking its channel selection or recipe.

The publisher omits XML units. Original XML remains unchanged; separate metadata attributes microvolts, g/degrees-per-second, percent and scaled ADC units to pinned-source interpretation. Optical values are not calibrated hemoglobin concentrations. Preset and clock model are required facts. The default windowed clock and 200 ms reorder buffer still need physical timing characterization.

## Pupil products

[Pupil Core Relay 2.3, pinned commit 37dedd64](https://github.com/labstreaminglayer/App-PupilLabs/tree/37dedd64c6a7691f9d8d3900f46d9b89f8e35e7e/pupil_capture) remains an external LGPL-3.0 plugin. Scene gaze has 22 double64 channels, pupillometry 7, both irregular. Channel order, units and relay version are checked. Upstream gaze-normal entries declare mm; this is preserved with an interpretation limitation.

[Neon Companion](https://docs.pupil-labs.com/neon/data-collection/lab-streaming-layer/) directly provides LSL. Enable Stream over LSL and select the outlet ending in _Neon Gaze. Freeze Companion version, eye-state mode and channel metadata. Eye-state requires explicit left/right pupil identity. Neon Events requires active Companion recording. No universal sample rate or open-source Companion commit is invented.

## Cerelog 16

The [ESP-EEG source](https://github.com/Cerelog-ESP-EEG/ESP-EEG/tree/af1a56e0127e71606afdc7e7ddf0ca831715e09c) includes a candidate 16CH_EMUL_FW. It uses paired 33-byte OpenBCI-style frames, averaging two 250 Hz conversions into 125 Hz samples; channels 9–16 precede 1–8 and auxiliary bytes are zero. This preprocessing must be recorded.

The [linked USB LSL script](https://github.com/Cerelog-ESP-EEG/Lab-Stream-Layer-LSL-Compatability/blob/e70fcf9a7fa16a7b7847b51116680b17dd34079b/cerelog_lsl.py) reads only 8 channels, applies GUI amplitude correction, filters DC and creates scheduled timestamps. The [custom fork](https://github.com/shakimiansky/Shared_brainflow-cerelog/tree/932b3944bfe6c0f4e29a46b4a34afdeba39edd85) still exposes an 8-channel Cerelog_X8 driver; its 16ch example uses Cyton+Daisy. Firmware README guidance also references the 8-channel V2 sketch for 16-channel hardware.

Support remains withheld until exact firmware/build, packet fixtures, channel pairing, voltage scaling, references/gain, averaging/filter response, counters/gaps and physical capture are verified. The manufacturer warns that this non-isolated device requires battery-only laptop operation. This release neither flashes firmware nor grants participant-use approval. No ALS is assumed.

## OpenViBE and audit evidence

The [canonical SDK](https://gitlab.inria.fr/openvibe/sdk) and [extras](https://gitlab.inria.fr/openvibe/extras) servers denied automated access during review. No source/binaries were imported and no current driver-license certification is asserted. The external LSL template freezes actual driver, scenario SHA-256, driver-build SHA-256, versions, channel mapping and timing.

The machine-readable audit is config/hardware_upstream_evidence_alpha_10_2_1.json. GitHub facts are pinned to inspected commits. Missing licensing grants, inaccessible source and physical-test limits remain explicit.

## Software verification

The development source includes the following test entry point; development tests are not shipped in the clean end-user ZIP. Executed release evidence is preserved under `app/deployment/validation`.

    python tools/Hardware_Forge_v1_0/tests/test_device_routes_alpha_10_2_1.py

Tests cover XML/outer-descriptor disagreement, wrong products/presets, channel order/units, missing metadata, changed source versions, deterministic evidence, withheld routes, reordered/fragmented TCP, validity, integer precision, gaps/reset, ACK/NACK and explicit model/rate selection. These are software fixtures, not physical-device verification.
