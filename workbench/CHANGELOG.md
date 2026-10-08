# PRAYCG Workbench changelog

## Alpha 10.5.2 — Gamma Scalpel 2.0 and simpler optical exploration

- Adds one governed Gamma Scalpel action with measured EEG and optional Cerelog or compatible EOG/EMG references.
- Checks participant, source, units, continuity and timing; rejects ambiguous metadata and explains missing or unusable references.
- Uses measured references for the corresponding artifact assessment, retaining EEG integrity checks and the original legacy method comparison.
- Reports original and screened gamma, retained duration and supported condition comparisons using matched portions without reusing windows.
- Limits Athena gamma outcomes to its measured TP9, AF7, AF8 and TP10 electrodes.
- Makes optical review default to the whole recording, independently of EEG QC; saves source, scope and settings with each attempt.
- Adds automatic 30-, 10- or 5-second spectral windows with matching full/screened resolution, gap handling and explicit frequency support.
- Adds reusable versioned instrument profiles and automatic recording bindings/baselines; verified profiles can enable relative HbO/HbR. The bundled Athena profile remains raw-only because required conversion facts are unresolved.
- Keeps recording selection and progress visible, with optional optical settings under Details.
- Corrects migration of saved tools from prior public Workbench folders to the current release.
- Includes complete installers, public method/workflow guides, regression evidence and checksums; original recordings and prior releases stay intact.

## Alpha 10.5.1 — Recording with cautions, Forge organization and optical/replay review

- Adds source-bound scoped Athena EEG acquisition/recording admission, separately identifying transport verification and other unvalidated capabilities.
- Makes the thirty-second signal check optional, with brief actual-data recording readiness and retained connector startup timing calibration.
- Allows finite signal-quality cautions through one Record with cautions action; saves findings for analysis and removes repeated quality confirmation/freeform override.
- Separates slow electrical baseline movement from timing uncertainty and retains actual capture, identity, units and write-failure correction requirements.
- Keeps recording purpose independent of quality; historical bench labels and evidence are preserved.
- Reorganizes Forge into Recording / Analyze / Results with persistent recording context, analysis cards, result shortcuts and one current-operation area.
- Makes eligible dedicated Muse Zuna comparison visible; keeps generated signals and hardware QC distinct.
- Enables full-rate Time–Frequency XDF replay with history rebuilding, gaps and presentation-only playback speed.
- Adds raw optical trends and slower spectra to live, replay and Forge; relative HbO/HbR requires verified source-bound metadata.
- Ships complete installers and public installation, recording, Forge, replay/optical and release documentation. Current acceptance artifacts retain their observed scope.

## Alpha 10.5.0 — Live Time–Frequency and Forge Explorer

- Adds an optional Live Time–Frequency popup using the full-resolution EEG already received by the Live Monitor. A bounded rolling spectral history supports electrode heatmaps and a rotatable three-dimensional categorical-channel view.
- Adds a separate exploratory Time–Frequency Explorer module to the Analysis Forge, retaining the selected recording, original timeline, quality evidence and actual-condition notes.
- Shares viewer controls for live and recorded data, including fixed color scales, electrode labels, source selection, visual pause, inspection and export.
- Supports continuous measured-signal exploration and eligible saved event-related results with their original estimator, baseline and trial-support information.
- Shows per-electrode accepted support, gaps and recorded quality reasons. Compatible conventional and saved Zuna derivatives retain source labels and generated-sample provenance.
- Adds compatible recording comparisons and portable interactive HTML, static-image and numerical reports with source and processing information.
- Uses independently implemented Workbench code. The upstream eeg-tfr-volume project informed the requested visual concept; its code and example recording are not bundled.
- Provides the complete installers and current source-bound validation. Historical acquisition and reconstruction qualifications keep their original scope.

## Alpha 10.4.10 — Forge quality, comparisons and consistent Zuna processing

- Exploratory full-recording reporting remains available when accepted coverage is insufficient for an outcome.
- Per-electrode and per-analysis eligibility, paired-channel windows, and separate recording-integrity, signal-quality and coverage descriptions.
- Versioned Athena QC recipe, retained prior recipe, and local artifact guards in place of blanket neighboring-window exclusion; amplitude and clipping screens remain explicit engineering choices.
- Median, variability, large-burst influence and consistent full/accepted/equal-duration recording comparisons.
- Consistent preprocessing and baseline for optional Zuna comparisons, sample-aligned generation masks and audited joins.
- Optional Zuna comparison with actual generated coverage, processing duration, distortion metrics and checked supported-device metadata.
- Actual recording-condition notes, stable recording selection and progress for long operations.
- Complete installers and fresh release validation. No change to existing recordings or prior releases.

## Alpha 10.4.9 — Cerelog off-body bench controls and bundled timing-patched recorder

- Promotes the patched 10.4.8 Workbench into a separate complete release, retaining the normal installers, 91 protocol definitions, 20 Athena editions and existing Forge/Muse workflows. Earlier releases and user studies are not merged or rewritten.
- Adds the exact Cerelog V1 **5 EMG / 2 EOG / 1 ALS** off-body recording controls through **Hardware Selection → reviewed and locked Hardware Profile → Connect & Launch**. Eight physical channels publish three signal feeds plus Timing diagnostics. Generic Home connector management does not authorize a recording.
- Requires explicit Bench Test Mode, battery-only/off-body and trusted-network/local-recording consent, an unlocked equipment session and matching run/launch/firmware/stream identities. Each recording uses a new output path and remains non-participant equipment data without task markers.
- Gives owned bench recordings a graceful-stop lifecycle, independent file-closure check and raw timing audit. Connector stop, generic force-close and session replacement remain guarded while recording or evidence finalization is unfinished. Failure evidence is preserved without claiming successful closure or timing.
- Bundles the timing-patched LabRecorder GUI and CLI, required runtime, per-binary build identity and synthetic qualification summaries. Launch rejects an unverified selection; GUI configuration is hash-bound and explicit, with AutoStart and remote control disabled and online synchronization unset. GUI remote control remains **NOT QUALIFIED**.
- Fresh settings use the bundled recorder; nonblank saved recorder selections are preserved. **Use Bundled Paths** explicitly selects the current bundle. Protocol recording through the LabRecorder GUI remains an operator action, separate from the owned Cerelog equipment recorder.
- Retains twelve synthetic recorder trials from the unchanged 10.4.8 patch build, covering both shutdown orders three times per binary. CLI evidence does not qualify the GUI, and synthetic qualification does not establish physical synchronization, electrical safety, participant approval or scientific validity. Raw generated XDF fixtures are excluded from the public Workbench; the bundled distribution note identifies the full companion archive.
- Does not change Bench Test Mode's protocol/hardware compatibility boundary. A four-channel Muse profile still cannot satisfy a sixteen-measured-channel reconstruction protocol. No automatic firmware flash, reconnect, optical alignment or cross-board synchronization approval is added.
- New 10.4.9 acceptance is source-bound offline contract/regression checking only. Copied 10.4.8 full-install, saved-recording and model acceptance remain historical; no fresh full installation, model execution, physical acquisition, manual whole-workflow or second-machine validation is claimed. Consult the current build record for exact results.
- See the [10.4.9 installation and workflow guide](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.4.10).

Earlier release entries are preserved in the [complete packaged changelog](docs/releases/alpha-10.5.2/CHANGELOG.md) and the [GitHub release history](https://github.com/hbanks87/praycg-open/releases).
