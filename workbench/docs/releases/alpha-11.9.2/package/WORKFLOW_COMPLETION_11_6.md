# Processing and reporting workflow: Public 11.6.0 / AUL 1.5.0

This release improves the route from a recording to an inspectable analysis. It does not make every recording support every endpoint. Public retains the PRAYCG AI Assistant without AUL. The separate private edition retains AUL integration and history support.

## Ordinary analysis

1. Open the recording in the existing AI Assistant or Analysis Forge workflow.
2. Run recommended analyses. Required QC runs first when needed. Run pending analyses when offered.
3. Open the latest report. The coverage section shows what was included, omitted or unavailable. Zero is a measurement, not a missing value.
4. An AI explanation is a separate, authorized request. Saving or opening a local report does not contact a provider. Exact result references do not by themselves establish that the explanation is scientifically correct.
5. If the current plan is empty but earlier results exist, explicitly select previous results. The program must not silently relabel them as results of the current plan.

## Compare processing choices

Open **Signal Quality & Cleaning Review** from the Forge, load the recording and select the actual EEG stream, electrodes, time interval and annotation version. Choose original input, the current-recipe preview or an explicitly saved reviewed candidate. A recipe preview is not automatically the complete governed preprocessing derivative.

Run the compatible comparison suite. Each output retains its source, method settings, supported intervals, annotations and candidate identity. Results appear in a separate **Processing comparisons** area. They are not inserted into the original locked plan or presented as independent confirmation. Original samples and previous reports remain unchanged.

Open each module's report for the question, findings, ordinary-language meaning, supported conclusions, limitations and next step. These local explanations describe saved software outputs. They do not independently select the best cleaner. A report-rendering failure must remain separate from a numerical failure.

## Paired CAI/SID

The new adapter regenerates the implemented canonical features for each branch, then applies the original recording's frozen reference settings to both. It does not substitute a gamma/theta ratio for CAI or guess the meaning of SID. Outputs describe the actual operational definitions, including the existing theta-power feature mapping.

The adapter has a new, explicit feature-source policy. It uses positive primary-content alpha log-power rather than the legacy sign-flipped alpha-drop fallback, uses the preferred maximum peak-to-peak artifact feature, and names its NAST inputs instead of heuristically averaging similarly named columns. These differences are recorded; this comparison is not claimed bit-identical to every historical export route. Historical workers and outputs are unchanged.

This endpoint needs the complete supported canonical montage, sufficient bandwidth, genuine phase boundaries, adequate baseline rows, and the implemented NAST and future-window support. Four-channel Athena recordings can still run their supported analyses, but cannot supply missing canonical electrodes. An endpoint-specific `NOT_ESTIMABLE` result does not block acquisition.

In **Reviewed processing settings**, use **Load recorded condition events…** to select actual PRAYCG start/end events. Confirm the recording association and record its evidence. The importer checks acquisition IDs, explicit LSL times and complete boundaries. A filename is not proof of association. Unfinished phases are not assigned invented ends. Generic protocols require a separately reviewed condition mapping.

Feature-window, hop and filter-edge choices are explicit. Reducing a window changes the measurement; it is not a way to relabel unsupported data as supported. Long future windows also mean this offline CAI calculation is not an instantaneous live estimator.

## Measured artifact and timing evidence

Gamma Scalpel preserves its historical proxy and adds measured EMG/EOG coverage beside it. A missing, unusable or timing-unqualified reference does not mean there was no artifact. Recorded references cover their actual locations, not every possible muscle or eye movement.

The dual-ALS helper fits offset and drift only from explicitly matched measured optical events. It requires at least three pairs spanning ten seconds and does not extrapolate beyond their observed support. Reported uncertainty is an engineering envelope including sample brackets and residuals, not a statistical confidence interval. It never aligns by optimizing the neural result. These source-bound helper contracts do not certify an entire physical acquisition setup or provide an automatic pairing wizard.

## Cerelog experimental pilot

The exact 5 EMG / 2 EOG / 1 ALS hardware action offers separate off-body bench and experimental participant-pilot routes. The pilot requires fresh safety, privacy, recording, battery-only and trusted-network confirmations. It is bounded to 1–600 seconds, defaults to 60 seconds, and records raw transport/recovery evidence. It does not arm a protocol or establish hardware safety or physiological validation.

The pilot publishes EMG, EOG, ALS, timing and transport-event feeds. Use LabRecorder for a study XDF. Inspect the preserved evidence after stopping. Recoverable corruption is visible; missing packets are not assigned invented counts when the firmware provides no sequence counter. Do not treat software tests as permission to use an electrically unreviewed setup on a person.

## Optical credits and preserved history

The current optical method record includes Delpy and colleagues' modified Beer–Lambert reference and the MNE fNIRS guide, with a clear statement that the native profile inversion is not an MNE implementation call. This is an attribution correction only. Earlier report identities, numerical results, event namespaces and histories are not rewritten.

## Install or update without replacing studies

Use a new release folder. The outer installer prepares application dependencies; study data and private history stay in their existing external locations. Retain the previous installation until the new one has been checked. Do not merge release directories or delete a Zuna runtime that an existing setup still references.

For signed same-edition updates, keep the `.zip.update.json` sidecar beside its ZIP and import it through **Settings → Updates**. Preparation and restart are separate actions. Stop acquisition and finish analysis before restarting. A rollback changes the selected application, not study files or assistant history. No remote release publication or installation over an operator's existing setup is performed simply by delivering these archives.

See **BUILD_REPORT.md** for this build's actual tests and remaining limits. No claim is made that all functions, physical devices, MATLAB equivalence, neural preservation or AI interpretations have been validated.
