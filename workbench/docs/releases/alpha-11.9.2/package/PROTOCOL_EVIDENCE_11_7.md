# Protocol evidence workflow for Public Alpha 11.7.0 and AUL Alpha 1.6.0

This release adds eight research task packages, a shared analysis route, event descriptions, independent numerical checks and clearer processing history. The Public edition keeps the PRAYCG AI Assistant without the private AUL implementation. The private edition retains AUL integration and its existing history location.

## Install beside your current version

Extract the appropriate ZIP into a new folder. Run its outer **INSTALL.bat**, then **START.bat**. Do not merge it into an older installation, delete the older folder or reinstall Zuna to apply this update. Keep your external study folders and existing settings. Public and private editions are separate packages; the private package must not be published as the Public release.

The optional **INSTALL_EVENT_DESCRIPTIONS.bat** installs the official HED validator in a separate environment. It downloads HEDTools 1.2.0 and a checksum-pinned HED 8.4.0 schema. It does not upgrade NumPy in acquisition or Zuna. Basic event-description export works without this optional installation and explicitly reports that official validation was not run.

## The eight task packages

| Task | Recorded evidence | Important interpretation |
| --- | --- | --- |
| Eye and jaw artifact calibration | Voluntary gentle movement cues, actual sensor windows and optional independently reviewed labels | A cue is not proof that an artifact occurred. Quiet is not clean neural ground truth. |
| Narrative carryover | One original short story, free-association responses and a frozen lexical rubric | Word use is a behavioral observation, not a direct measurement of personal meaning. |
| Context-guided interpretation | Matched framing, interpretation choices and separate factual comprehension | Framing and comprehension are different outcomes. Repetition and item identity remain relevant. |
| Event boundaries and memory | Independently specified boundaries and subsequent memory responses | Boundaries are not selected from favorable EEG events. |
| Comfortable breathing and recovery | Voluntary continuous breathing periods, measured respiration and actual beat intervals when available | No breath holding or forced breathing. Sampled heart rate is not beat-based HRV. |
| ERP qualification | An original visual oddball task plus a source-fidelity inventory of existing ERP adaptations | Existing adaptations keep their identities. The new task is not an exact ERP CORE replication. |
| Perceptual decisions and confidence | Objective dot comparisons and stated probabilities of being correct | Calibration scores describe these trials; no meta-d′ or diagnostic trait is inferred. |
| Response stopping | Go/stop trials, delay adjustment, omissions, reaction times and assumption checks | A stopping estimate is reported only when its stated requirements are met. |

The tasks use original packaged material and deterministic preparation. They are inspectable research implementations, not normative or clinically validated tests. Existing Atlas protocols and historical marker identities are retained.

Previously imported custom protocols remain in their external store, but their saved admission records may refer to an older runner fingerprint. If compatibility review is requested, keep that historical version and review a new version through the existing protocol intake workflow. Do not edit an old admission receipt or its hashes to bypass the check. This build does not silently reapprove user-authored experiments.

## Run a new task

1. Choose its protocol in the Atlas and prepare its materials through the normal workflow.
2. Review the task, original materials, response instructions and analysis contract. The Materials lock binds the selected protocol; Atlas compilation freezes the participant-specific order and stimulus identities. Compile, review and lock that participant-specific plan before acquisition.
3. Select the actual hardware profile. Optional physiology is useful only when its channel identities, units and timing are supported. Exploratory Athena acquisition is not excluded for lacking a full-cap endpoint.
4. Use the normal recording and authorized runner flow. Escape stops the task. Saved evidence distinguishes completed trials from interruptions and missing responses.
5. Save the recording, select it in Analysis Forge and complete the required checks.
6. Add **Protocol evidence** to the analysis plan and run it. The report retains available behavioral outcomes alongside unavailable or failed signal endpoints.

The event log and separate compiled stimulus plan belong with the recording. Keep those files when moving a study or preparing a private full-data bundle. The compiled plan, not an editable answer field alone, supplies the expected scoring identity.

## Optional signal inputs

In **Analysis Forge → Analyze → Other analyses and comparisons**, use **Choose protocol signal inputs**. The selectors show actual recorded channel labels, types and units. Choose only channels appropriate to the endpoint; leave unsupported selections blank.

The new ERP task's EEG endpoint requires an actually recorded **Pz** channel and at least 20 accepted trials per condition. Its frozen comparison uses a −200–0 ms baseline and a 300–600 ms measurement window. Athena can run the behavioral task, but its electrodes cannot be renamed or interpolated into Pz to enable this endpoint. The pilot voltage contrast is not automatically a validated P3b measure.

Cardiac–respiration coupling additionally needs an explicit participant/source pairing, reviewer, reason and documented timing uncertainty within a prospectively selected tolerance. Sharing an LSL clock label does not establish that two sensors belong to the same person or that their timing is sufficiently accurate. Do not invent a timing bound to enable an endpoint.

Selections are saved as recording-bound versions. Existing locked plans are not silently changed. If a selection changes a locked input, create a new plan revision through the existing workflow. **Import reviewed signal settings** accepts an explicitly versioned, hash-bound settings file, including independently reviewed artifact labels where available.

## Independent numerical checks

Use **Independent numerical check** in the same Analyze section. Choose one actual EEG channel and a window of at most 60 seconds. The check compares the current Workbench spectral and complexity calculations with separate calculations on the same finite continuous samples. It saves a separate report; it neither chooses a cleaner nor replaces the original analysis.

Agreement establishes numerical consistency for the tested samples and settings, not clean EEG or validity of an experimental interpretation. A shared library backend is distinguished from an independently written calculation. Gaps, constant signals, short windows and unsupported values must remain explicit.

The protocol analysis also includes bounded nuisance controls where the design supports them. Order-only prediction and permutation checks can reveal a shortcut in a task schedule; they do not establish that an EEG effect is neural, causal or free of all confounds. Calibration, training and test groups remain separate.

## Event descriptions and processing history

In **Analysis Forge → Results**, use **Review processing history** to see the selected session's saved plan, executed attempts, outcomes and separately registered processing comparisons. Failed and unavailable attempts stay visible. Receipt verification is distinguished from rehashing every source and output. Reprocessing one recording is not independent confirmation.

**Export event descriptions (HED)** creates a new derivative containing the exact original event file, a description table, provenance and a file ledger. Original markers and timestamps are untouched. Unknown event names remain unmapped. With the optional validator installed, mapped descriptions are checked offline against the pinned schema. This validates annotation syntax, not what happened on the physical screen or the correctness of event timing.

Event exports may contain typed participant responses and are private until reviewed. Keep ordinary results bundles separate from explicitly chosen full-telemetry exports.

The automatic public-oriented selection excludes these new task-response reports, event derivatives and detailed history snapshots. An explicitly selected private bundle can preserve them; the original event copy and full trial ledger additionally require the raw-data option. This avoids treating a text response as anonymous merely because no hardware identifier appears in it.

## AI explanations and study bundles

Each new protocol-evidence report includes a plain-English account and underlying numerical evidence. Public AI or private AUL may explain those saved results through the existing explicit-request workflow. A report can describe successful behavior even when a physiological endpoint is unavailable. AI must not turn a missing estimate into a null effect, infer a participant's thoughts, or treat multiple transformations of one recording as independent evidence.

Use the existing bundle review and verification controls. Include event/compiled-plan evidence when the chosen bundle policy permits it. No new protocol, report, bundle or optional setup grants permission to upload private participant text automatically.

## Immediate research milestones

1. Validate the exact Cerelog build in use. The newer compact 3-EMG/2-EOG/1-ALS route has a different identity from the older 5-EMG profile. Offline packet tests do not replace electrical, placement, contact or human-recording validation.
2. Validate Cerelog and Cyton/Daisy together, preserving separate ALS observations, actual clock support, channel pairing and disconnect recovery.
3. Run the frozen PRAYCG4 preparation in the basement and then in the shielded setup. Treat them as separate recorded environments, not interchangeable clean/dirty labels.
4. Tune Gamma Scalpel using designated calibration data and independently reviewed artifacts. Keep separate sessions or material for the evaluation of desired-signal preservation.
5. Review the real findings before expanding the protocol battery or adding adaptive intervention. Neither the public assistant nor AUL gains permission to change a participant protocol autonomously in this release.

See **BUILD_REPORT.md** for this build's actual test scope and remaining checks.
