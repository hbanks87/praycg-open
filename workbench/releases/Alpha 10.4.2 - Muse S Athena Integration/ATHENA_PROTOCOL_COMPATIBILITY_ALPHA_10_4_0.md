# Athena protocol editions in Alpha 10.4.0

The compatibility registry covers all 71 original definitions and 20 separately identified Athena editions. The original definitions, stimulus orders and scientific endpoints remain intact. Their profiles distinguish task availability from the narrower endpoint requirements.

The managed Athena route supplies four real EEG channels, TP9, AF7, AF8 and TP10, at nominal 256 Hz. FPz remains the reference in preserved native data. AUX and raw optical streams do not supply other EEG sites, ALS, pulse intervals, respiration, EMG or EOG. Device admission and physical qualification remain independent gates.

Start with **IndividualRest — Athena EEG-only baseline**, the MIPDB eyes-closed rest adaptation, or meditation versus active thinking. IndividualRest provides observed awake eyes-closed acquisition and descriptive channel quality/spectra. The meditation comparison has an implemented, explicitly descriptive within-person spectral adapter. The thirteen existing behavioral protocols retain optional EEG; their behavioral analyses do not infer physiology.

The three native narrative protocols have new `PRAYCG3_ATHENA_V1`, `PRAYCG4_ATHENA_V1` and `SMG_ATHENA_V1` editions. They preserve the original branches, stimuli and questions while limiting results to behavior, recording/timing quality and four-site descriptive EEG. Their active analysis contract excludes CAI, SID, whole-cap ROI composites, unrecorded autonomic signals and physical optical-arrival measurements.

All ten prospective counterbalance sequences have a matching `_ATHENA_V1` edition. The Prospective Study Console has an explicit edition selector. Assignment uses the exact original sequence identity, verifies its base protocol and condition order, then resolves the exact selected-edition manifest and runner hashes. Two separate catalogs prevent a first matching base ID from choosing the wrong edition. The Athena study template and allocation file are distinct; freezing an edition that disagrees with the selected study configuration fails. Template freezing never declares collection readiness.

Six ERP tasks have separate `_ATHENA_EXPLORATORY_V1` editions. Task sequences remain unchanged. Active outputs are behavioral observations where the task collects them, trial retention and event-related averages at the four measured sites. The source N170, N2pc, N400, P3b, MMN, LRP and ERN component claims are excluded. The original component protocols retain their required scalp sites and fail the Athena hardware check. Software timestamps do not establish physical visual or acoustic onset.

The old three Zuna protocols require sixteen real measured channels and the declared F3/F4/P3/P4 sites. The separate Muse S Athena reconstruction protocol is preferred for this device. Generated or interpolated channels do not meet measured-channel requirements. Inner-speech controls, SSVEP photodiodes and autonomic sensors remain actual additional acquisition requirements. True dyadic hyperscanning requires independent, participant-bound EEG, RR and respiration sources for both people; caregiver or trust tasks do not inherit that demand.

## Shared API

`control_center/scripts/praycg_athena_compatibility_v1_0.py` exports:

- `load_profiles(base_root=None)` returns profiles keyed by protocol ID.
- `get_profile(protocol_id, base_root=None)` returns a copy or `None` for an unreviewed extension.
- `hardware_context(hardware_profile)` extracts declared measured EEG metadata and actual roles. It honors an explicit primary source and never concatenates people into one montage.
- `evaluate_protocol(protocol_id, *, hardware_profile=None, measured_sites=None, available_roles=None, sample_rate_hz=256, physical_channel_count=None, timing_evidence=None, participant_role_counts=None, protocol_parameters=None, base_root=None)` returns task/endpoint states, missing requirements and reasons.
- `protocol_compatibility_errors(protocol, hardware_profile, base_root=None)` supplies the measured-input launch blockers for packaged protocols. External extensions retain their own review/admission process.

Without a hardware profile, evaluation previews four-channel Athena plus task markers. With a profile, empty or ambiguous measured metadata does not fall back to that preview. `launch_blockers` and `can_run_task` cover the scientific edition's declared hardware requirements. `blockers` and `can_claim_endpoint` additionally check timing evidence and actual analysis availability. A passing result only permits the profile's stated descriptive scope; it is not evidence that data were acquired, clean, physically validated or scientifically validated.

Analysis states are `IMPLEMENTED`, `EVENT_ONLY` and `NOT_IMPLEMENTED`, with a separate scope and module list. A recorded event is not an implemented physiological analysis. Known defaults such as the motor protocol's fifteen trials per class remain explicitly insufficient for its twenty-retained-trial decoder. Optional NATVIEW checkerboard activation adds posterior-site requirements instead of inheriting the default video compatibility.

The versioned registry is `config/athena_protocol_compatibility_v1_0.json`; new identities and hashes are in `config/athena_protocol_editions_catalog_v1_0.json`. Each edition keeps parent provenance, a pre-attribution design snapshot and its own local citation. The builder only reads original manifests; rebuilding requires the preserved review directory. Tests cover inventory completeness, actual montage/sensor rejection, edition semantics, exact wrapper dispatch, attribution hashes, prospective assignments and edition-specific freezing. All reported checks are software tests; no physical acquisition is implied.
