# PRAYCG Workbench / Control Center

**Current release: Alpha 10.2.1**

PRAYCG is an open, local-first neuroscience workbench for moving a study from an initial question to a reviewable research package. It connects protocol selection, stimulus preparation, hardware configuration, synchronized acquisition, protocol execution, analysis, visualization, interpretation and research exchange while preserving the identity and provenance of each step.

PRAYCG does not make an experiment scientifically valid merely by running it. Its purpose is to make assumptions, methods, timing, software, data lineage, limitations and results visible enough to inspect, reproduce and challenge.

> **Research-use warning:** PRAYCG is alpha research software. It is not a medical device, diagnostic system, clinical tool or safety-critical acquisition controller. Human research still requires appropriate scientific, ethical, consent, privacy and equipment review.

## Documentation

- [Installation guide](docs/INSTALLATION_ALPHA_10_2_1.md)
- [Detailed workflow guide](docs/WORKFLOW_ALPHA_10_2_1.md)
- [Master citations and attribution](CITATIONS_AND_ATTRIBUTION.md)

The packaged release also contains `CHANGELOG.md`, `LICENSE.md`, detailed hardware-route and AI-authoring notes under `app/docs/`, and machine-readable evidence under `app/deployment/validation/`.

## What PRAYCG connects

```text
Workspace and question
        ↓
Protocol and materials
        ↓
Reviewed hardware profile and synchronized streams
        ↓
Session confirmation, immutable lock and protocol runner
        ↓
Required QC and dependency-aware analysis plan
        ↓
Per-module reports, figures and offline interpretation
        ↓
Privacy-reviewed bundle, reanalysis and local DATA catalog
```

The Workbench is the general-purpose software and provenance workflow. The PRAYCG neuroscience research program contains particular hypotheses, protocols and exploratory constructs. Using the Workbench does not require accepting any particular research theory, and inclusion in the Protocol Atlas does not validate a hypothesis.

## Major capabilities

### Study and protocol workflow

- Create or reopen a persistent study workspace.
- Select native, Atlas or locally installed protocols while preserving exact versions and aliases.
- Prepare and fingerprint required media, manifests, channel maps and other study inputs.
- Use protocol-dependent pre-start settings rather than a single generic runner form.
- Confirm, hardware-lock and arm a run through explicit state transitions.
- Preserve interruptions, incomplete runs and historical receipts instead of silently rewriting them.

### Hardware and synchronized acquisition

- Build reviewed hardware profiles from separate EEG, ECG, gaze, pupil, motion, optical, autonomic and marker roles.
- Start a new equipment session with a unique run identity and dedicated evidence folder.
- Inspect LSL delivery, run identity, channel structure, sample rate, gaps and basic signal-health findings.
- Record synchronized streams with LabRecorder while preserving runner markers and acquisition evidence.
- Use an existing LSL publisher through an exact reviewed-outlet workflow without granting PRAYCG authority over the external application.

### Analysis Forge

- Begin with the required QC gateway: run integrity, event timing and applicable EEG/line-noise checks.
- Build a dependency-aware plan that can include downstream modules before their prerequisites finish.
- Lock and run an immutable analysis revision, pause after the active module or resume unfinished work.
- Keep persistent per-module results with scientific reports, figures, receipts, output folders and plain-English summaries.
- Preserve `NOT_ESTIMABLE` when a recording cannot support an endpoint instead of converting missing evidence into zero or a false success.

### Reproducible exchange

- Create local results packages and optional private full-study or AI-review bundles.
- Export Research Bundle 1.0 packages with explicit privacy/consent/rights classifications.
- Verify and import bundles without executing archived code or overwriting original studies.
- Prepare current-build reanalysis as separately identified derived work.
- Compare supported outputs under a frozen numerical policy and retain unmatched or unsupported artifacts honestly.
- Register and inspect bundles in the local PRAYCG DATA catalog.

### AI-assisted protocol and recipe authoring

- Export a local protocol-design document pack for an AI collaborator.
- Review a schema-bound returned protocol, run a bounded fake-I/O rehearsal and explicitly install it under **My Protocols**.
- Create supported local protocols from templates without an AI service.
- Export, review and load parent-bound EEG recipe proposals before ordinary validation and locking.
- Package private study context for external AI review without automatically uploading anything or executing returned code.

The casual protocol importer intentionally accepts bounded, data-only task components. New acquisition engines, device commands, adaptive controllers or numerical estimators remain separately reviewed development work.

## Alpha 10.2.1 hardware integration

Alpha 10.2.1 connects the exact routes introduced in 10.2.0 to the main Hardware Library, hardware-profile builder and locked route actions.

| Status | Routes | Meaning |
| --- | --- | --- |
| Managed connector available | Neurosity Crown OSC through BrainFlow; Muse S Athena through BrainFlow; Polar H10 ECG; GazePoint GP3; GazePoint GP3 HD | PRAYCG supplies a route-specific launcher and publisher. Software tests passed, but the new routes remain experimental pending physical-device and timing validation. |
| External publisher required | OpenMuse Athena EEG, motion, optics and battery; Pupil Core scene gaze and pupillometry; Pupil Neon gaze; OpenViBE external LSL | Start and manage the publisher separately, review the actual live outlet and freeze its exact metadata before attaching it. PRAYCG does not install, control or stop the external publisher. |
| Existing reviewed paths retained | OpenBCI with or without ALS, Polar RR, Vernier and existing generic LSL paths | Existing route-specific evidence and readiness requirements remain applicable. |
| Withheld | Cerelog 16 | Source evidence is cataloged, but the exact 16-channel transport, scaling, timing and physical contract are not sufficiently established for a runnable profile. |

All newly integrated 10.2.1 routes require an `EXPERIMENTAL_EVALUATION` profile and an explicitly labeled **Bench Test Mode (no participant)** session. A software pass or matching stream description is not physical validation, participant approval, electrode-placement proof or synchronization certification.

Important boundaries:

- Crown publishes the reviewed BrainFlow OSC route; it is not presented as the Neurosity SDK `rawUnfiltered` signal.
- Muse S Athena publishes its reviewed presets as separate modalities. It supplies no ALS. Raw optical values are not validated fNIRS or hemoglobin measurements.
- An OpenMuse p1041 EEG outlet can contain four named electrode channels plus four AUX channels. They are preserved but are not described as eight verified EEG electrodes.
- Polar H10 ECG is separate from its irregular RR stream. Opening multiple BLE clients can be unsupported by the device or operating system.
- GazePoint requires GazePoint Control and appropriate calibration. GP3 and GP3 HD are separate routes.
- Restarting a managed or external publisher creates a new segment/outlet identity; a stale reviewed outlet cannot silently replace it.

Before evaluating these paths, read `app/docs/HARDWARE_ROUTES_ALPHA_10_2_1.md` in the installed release.

## Quick start on Windows

1. Download the Alpha 10.2.1 ZIP and its SHA-256 file from the repository release.
2. Verify the checksum, then extract the entire ZIP into a new writable folder. Do not run from inside the archive or merge it over an older version.
3. Install native Windows Python 3.11 with Tcl/Tk support.
4. Double-click `INSTALL.bat`. The default full mode installs/checks Core, Live Monitor and Hardware Connectors.
5. Install and configure external PsychoPy and LabRecorder separately.
6. Double-click `START_PRAYCG.bat`.
7. In Settings, select bundled tool paths and verify the external PsychoPy and LabRecorder paths.

For component-specific installation or repair:

```text
INSTALL.bat -Mode minimal
INSTALL.bat -Mode monitor
INSTALL.bat -Mode hardware
INSTALL.bat -CheckOnly
```

Read the [installation guide](docs/INSTALLATION_ALPHA_10_2_1.md) before upgrading or troubleshooting.

## Typical study workflow

1. Create or open a **Study Workspace**.
2. Select a protocol with **Choose Protocol → Use This Protocol**.
3. Supply and fingerprint required materials.
4. Select or build the matching reviewed hardware profile.
5. Start a new equipment session and launch the required streams.
6. Complete the applicable equipment checks and inspect their actual findings.
7. Review the protocol-dependent pre-start configuration.
8. Confirm the session, hardware-lock and arm.
9. Start LabRecorder, launch the locked runner and complete the task.
10. Stop and save LabRecorder promptly; then finalize the run.
11. In Analysis Forge, review the input inventory and run required QC.
12. Add desired eligible modules to the plan, lock the revision and run or resume it.
13. Review per-module reports and the master index.
14. Build the appropriate local/private/public-oriented bundle and perform human privacy review before sharing.

The [workflow guide](docs/WORKFLOW_ALPHA_10_2_1.md) covers participant acquisition, bench demonstrations, replay, analysis, recovery, exchange and AI-assisted extensions in detail.

## Installation architecture

The full installer uses three environments:

| Component | Environment |
| --- | --- |
| Core | The selected native Python 3.11 interpreter. This is not isolated by the installer. |
| Live Monitor | `app/.live-monitor-env/` |
| Hardware Connectors | `app/.hardware-connectors-env/`, with BrainFlow 5.23.0 and its pinned connector dependencies |

The ZIP does not contain Python, dependency wheels, PsychoPy, LabRecorder, proprietary device software or third-party external publishers. Installation normally needs internet access to retrieve Python packages. Once the required software is installed, ordinary local workflows do not require an online AI service.

## Data, privacy and security boundaries

- PRAYCG does not automatically upload studies, contact an AI provider or publish to a remote catalog.
- Private full-study bundles may include XDF recordings, exact stream metadata, device identifiers, host details, media and other sensitive context.
- Public/privacy-restricted projections omit recognized private stream metadata, but this is not general anonymization.
- Human review of consent, sharing authority, media rights, identifiers and recipient terms remains mandatory.
- Imported bundles are inert: import does not install protocols, execute archived scripts, install dependencies or grant acquisition/publication authority.
- Hashes establish byte identity and change detection. They do not establish authorship, authenticity of an external publisher, scientific validity or legal permission.

## Validation status

The Alpha 10.2.1 release gate passed **69 declared suites and 2,098 reported checks**. The extracted ZIP was also checked for:

- clean installation layout and checksum consistency;
- application discovery and hidden-interface startup;
- all five managed and eight external Hardware Library workflows;
- 57 built-in protocol/material workflows;
- synthetic XDF analysis and bundle reimport;
- locally installed protocol workflows;
- AI document export, bound simulated return and safe local installation;
- historical PRAYCG3 reanalysis and bundle/recovery regression without changing the source archive.

These are software and same-machine checks. The release does **not** claim physical validation of the newly integrated devices, participant safety, absolute sensor/stimulus timing, clinical validity, complete protocol × hardware × analysis coverage or independent second-machine reproduction.

Executed evidence is preserved under `app/deployment/validation/`. File ledgers and distribution mappings are under `app/deployment/`.

## Repository and distribution layout

```text
INSTALL.bat             Full/component installer
START_PRAYCG.bat        Application launcher
README.md               Project overview and quick start
CHANGELOG.md             Consolidated release history
LICENSE.md              Mixed-license notice
app/
  control_center/        Desktop Control Center
  tools/                 Acquisition, analysis, replay and bundle tools
  config/                Protocol, hardware and analysis registries
  docs/                  Scientific, hardware and attribution references
  deployment/            Installer resources, validation evidence and ledgers
  examples/              Governed demo resources
```

Study workspaces and locally installed protocol extensions are not meant to be stored inside the immutable application package. Keep study data, private bundles and backups separate from the extracted release.

## Reporting problems

When reporting a problem, include:

- the exact PRAYCG release;
- the action and UI label used;
- whether the session was participant or bench mode;
- the selected protocol and hardware-profile identity;
- the exact error text;
- the relevant run-local log/evidence folder;
- whether acquisition, LabRecorder or a connector was still running.

Do not publish participant data, XDF files, device identifiers, private paths, credentials or copyrighted stimuli in a public issue. Use a minimal synthetic reproduction when possible.

## License and attribution

Original PRAYCG-owned code is MIT-licensed unless a file states otherwise. Repository documentation is generally CC BY 4.0, and the bundled synthetic demo media is CC0 1.0. Third-party source, dependencies, data and media retain their own terms. Read `LICENSE.md` and the [Master Citations and Attribution](CITATIONS_AND_ATTRIBUTION.md) for author credits, software references, protocol sources and license boundaries.

Copyright © 2026 Hoyt Banks.
