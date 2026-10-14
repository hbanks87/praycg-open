# Proposed update: Public Alpha 11.2.1

**PROPOSED — for review; this page does not announce a published release.**

The latest published release is [Alpha 10.5.4](releases/alpha-10.5.4/README.md), published on 9 October 2026. The proposed update would bring its Workbench documentation and release materials forward to **PRAYCG Workbench — Public — Alpha 11.2.1**, covering the intervening additions as well as the latest patch. Existing release guides and evidence should remain available under their original versions.

This proposal is based on the public distribution inspected on **13 October 2026**. No full Workbench session, installation or scientific analysis was run for this documentation review. The test totals below are the package's recorded evidence. A later [isolated attribution-observer check](../../docs/attribution/alpha-11.2.1/proposed-fixes/README.md) found a protocol-ratings launch defect; the proposed metadata correction must be applied and the corrected package checked before release.

The repository now includes a [current software and method bibliography](../../research/bibliography/README.md) and [dated attribution review](../../docs/attribution/alpha-11.2.1/README.md), including NeuroKit2, PyWavelets, mne-denoise and EEGLAB's external-reference status. These supplement the unchanged package's own credits.

## Artifact and status

| Field | Inspected value |
| --- | --- |
| Archive | `PRAYCG_Workbench_Public_Alpha_11_2_1.zip` |
| Size | 43,737,009 bytes |
| Archive entries | 2,065 |
| SHA-256 | `cb65ec3180a59a9181e4fecd9bb94a2b136ab158f0f275eaf49b01dc3386c42b` |
| Checksum sidecar | `PRAYCG_Workbench_Public_Alpha_11_2_1.zip.sha256`; matches the inspected archive |
| Runtime version | `1.0.0-alpha.11.2.1` |
| Edition | `PUBLIC` |
| Manifest date | `2026-10-13` |
| Manifest release type | `ATHENA_REPORTING_AND_PROTOCOL_RATINGS_TARGETED_CHECKED` |
| Recorded verification status | `PASS_TARGETED_WORKFLOW_CHECKS` |

This identity applies to the exact archive above. If the package changes, its checksum, evidence and this proposal need to be reviewed together before publication. The public archive contains the independent **PRAYCG AI Assistant**. Its stated distribution boundary excludes private AUL implementation, histories and evaluation data.

## Draft release summary — PROPOSED

Public Alpha 11.2.1 would update the published 10.5.4 Workbench with Study / Prepare / Run / Analyze / Share navigation, improved recording playback and sensor displays, a simpler saved-recording analysis workflow, optional evidence-grounded AI explanations, a dedicated Signal Quality & Cleaning Review, and clearer separation between recording a task and supporting its intended scientific result.

The latest patch improves Athena channel- and pair-specific reporting and the evidence supplied to explanations. Existing saved analyses can receive new explanatory derivatives while their original numerical outputs remain intact. A new recorded-rating worker supports descriptive Synthetic Epiphany comparisons; the private protocol package, media and participant data are excluded from the public distribution.

The public build remains local-first alpha research software. Optional remote explanations require an explicit provider request. Recorded software checks do not establish physiological validity, physical timing, participant safety, AI explanation quality or complete workflow coverage.

## Proposed cumulative changelog since 10.5.4

The intervening 10.6.0–10.6.3 series introduced several ordinary workflow and display changes retained by this public package. Its historical AUL assistant, private state and review history are distinct from the independent public Assistant introduced in Alpha 11. The cumulative changes below include retained public capabilities; they do not propose distributing the older private implementation or importing its history.

### Navigate and inspect recordings

- **Study / Prepare / Run / Analyze / Share** navigation organizes the existing application pages. The context header distinguishes the prepared equipment session, historical analysis recording and independent live/replay viewer. A saved stage cannot by itself claim that equipment is currently armed or a runner is active.
- Scrollable navigation, keyboard access and a collapsed bounded log drawer keep controls accessible. Hardware utilities and Operator Confidence are organized through Tools and Settings.
- Replay provides **Close recording** and **Choose another XDF**, separately from **Reset playback**. Canceling a new selection preserves the current replay; a failed load permits another selection.
- Live waveform display no longer hides half of a sixteen-channel EEG behind the former eight-channel display cap. Its stream, channel and sample budgets remain bounded.
- Measured scalp-sensor band-power maps use declared standard electrode sites. Missing sites remain missing; these maps do not interpolate absent sensors, localize cortical activity or show fMRI/fNIRS measurements.
- A separate local delayed observer exposes supported descriptive features and unavailable reasons. Advanced regional gamma/theta or TSP/KHT proxies require their declared channels and usable support. They are not current brain-state estimates or replacements for the observer's basic Signal status.

### Prepare protocols and materials

- Public Alpha 11 introduces an independent PRAYCG AI Assistant for optional explanatory drafts, supported protocol proposals and explicitly requested passive snapshot explanations. Native validation, review and runner gates continue to govern actions.
- The detailed Protocol Designer shares the same design fields between the in-app Assistant and AI document export. Revision review, timeline changes and current installation blockers remain visible. Compiled material previews support preparation without treating a preview as a completed participant run.
- Historical recording preparation can associate uniquely matching runner evidence without relying on an old workspace's saved configuration. Conflicting evidence remains unresolved; association records are new derivatives.
- Required Atlas media contracts now check review records, native schedules, explicit frame-review declarations, fingerprints and measured-scale definitions where applicable. Passing a structural check does not establish stimulus suitability or an independently witnessed review.
- MediaPrep and ShotOrder repairs address final-frame loss, reordered-segment coverage and unsupported audio policies. Invalid inputs and unsupported dimensions are refused. Previously presented or fingerprinted media are not retroactively repaired; regeneration creates a new derivative requiring normal fingerprinting and review.

These changes are documented across the retained 11.0.0–11.0.2 records. Some intervening records describe candidate revisions; their historical status should remain visible.

### Select equipment and record

- Ownership recovery adds a read-only Windows process-absence check for eligible finalized historical runs. An active runner, uncertain ownership or unresolved acquisition still blocks a new session.
- The Atlas shows **Recording** and **Intended result** separately and refreshes compatibility against the selected equipment setup. An Athena motor task can be recorded exploratorily without claiming that missing C3/Cz/C4 electrodes were measured.
- Athena's nonblocking signal observations are retained automatically. The newer workflow no longer requires the repeated quality-acceptance action described in the 10.5.4 guide. Missing streams, invalid identities, task-critical equipment, active-run conflicts and operational requirements still need resolution.
- Replay and visual inspection give clearer reasons for unavailable timing, calibration and cardiac measures. A stream name alone does not establish units or an eligible RR source. Raw EEG/RR still cannot supply missing CAI, NIP or CAI-SID components.
- Verified acquisition context and recording disposition are available to explanations, with unknown or conflicting evidence preserved. Timing-specific findings remain distinguishable from unrelated quality cautions. Athena optical/EEG source selection checks the corresponding device run and segment.

These are software and workflow changes. Retained hardware admission evidence keeps its original scope; the proposed release adds no fresh physical-device or cross-device timing qualification.

### Open recordings and run analyses

- **Open recording** selects the exact XDF, with folder selection retained as an advanced route. The assistant's recording actions use the same native selection and QC workflow.
- The normal guided path becomes **Select recording → Run recommended analyses → View results**. Required QC runs when needed; **Choose modules** remains available for custom work.
- Guided execution saves a factual local summary. Dated **Local summary** and **AI explanation** history, readable HTML reports, recovery and source links keep earlier results accessible.
- Persistent terminal outcomes distinguish completed-with-limitations, unavailable, blocked and failed work. An unavailable result does not authorize a downstream prerequisite merely because its process completed.
- Empty optional event tables and ineligible cue-gamma inputs retain supported calculations or explicit not-estimable results. A versioned signed imaginary-coherency correction requires a new analysis output; historical matrices are preserved.
- New preprocessing attempts use separate output locations to prevent cross-recording overwrites.

The latest registry contains **40 module IDs**, compared with **35** in 10.5.4. All 35 earlier IDs remain. The additions are the four review modules below and `protocol_ratings_v0_1`; retaining an ID is not a claim that every implementation is byte-identical or scientifically validated.

### Inspect signal quality and cleaning

Public Alpha 11.2.0 adds **Signal Quality & Cleaning Review…** in Analysis Forge Results. It provides source-aligned original, explicitly selected current-transform preview, candidate and removed-signal views, with stream/channel selection, time support, playback and saved review reopening.

Four managed modules cover:

- **Signal quality and temporal-support review**
- **ECG, heartbeat and HRV review**
- **Respiration and measured-respiration RSA review**
- **Line-noise processing comparison**

Normal Core setup includes **NeuroKit2 0.2.13**, **mne-denoise 0.0.3** and **PyWavelets 1.9.0**. The comparison paths use the actual pinned libraries. There is no separate optional signal-review installer.

Eligible continuous segments are processed separately so filtering, peak detection and related estimators do not bridge missing-data gaps. HRV requires eligible measured intervals and original adjacent pairs. Sampled heart rate remains a trend and is not converted into beat-to-beat HRV. Respiration amplitude is not calibrated tidal volume; measured-respiration RSA needs eligible cardiac evidence and compatible overlapping time support.

Line-noise candidates include spectrum interpolation and fixed ZapLine comparisons. Reduced line power alone does not demonstrate preservation of neural information. The current-transform preview is not a replay of an earlier locked derivative. Operator exclusions create a new review version; no candidate or narrative automatically replaces a governed recipe, source XDF or earlier result.

### Explain results and share evidence

- Local summaries do not require a model request. **Generate AI explanation** is separate and explicit, with provider configuration and bounded request allowance.
- The public Assistant exposes **OpenAI API**, **ChatGPT account** and **Claude API** provider modes, with protected account storage and provider-specific configuration. The available modes are software routes, not evidence that an account, model or provider was validated during this build. Navigation alone makes no request.
- A local **Check AI report size** action and lossless packing of repeated evidence retain the request cap. Actual dispatch checks the current evidence again. Oversize requests stop rather than silently removing modules or increasing the cap.
- Bounded AI evidence keeps modules represented and makes omitted detail visible. Summaries remain linked derivatives rather than replacements for native reports.
- Live observer **Signal status** and local snapshot saving work without an AI account. An optional explanation describes the selected snapshot; a historical or late answer is not current live status.
- Full-resolution telemetry is retained separately for local review and excluded from default AI and results-review bundles. Full-telemetry sharing requires an explicit private export and separate privacy review. Derived summaries can also contain sensitive information.

Optional AI cannot arm equipment, alter raw measurements or silently adapt a participant protocol. Provider failures preserve numerical results and earlier reports.

### Latest patch: Athena reporting and recorded ratings

Public Alpha 11.2.1 separates completed calculation, available channel/pair descriptions and the strict all-four-electrode endpoint. A narrower available measurement cannot substitute for an unavailable full-montage prerequisite.

New Athena executions save `eeg_athena_scoped_summary_v1_3.csv`, identifying channel/pair/all-four scope, accepted/all-candidate/full-interval views, units, support and sources. **Explain existing results** can create a new explanation from saved numerical reports without rerunning analysis or unlocking an old plan. Existing saved AI narratives are not silently rewritten.

The new rating worker reports resonance, absorption and perceived-authenticity ratings, response ledgers, source fingerprints and three ordinal-category comparisons. It selects the last valid key within a completed rating window and preserves earlier responses and exclusions. Missing or interrupted windows stay missing. The newly specified rule is explicitly post-hoc for existing records; no automatic p-value, inferred emotion or causal conclusion is added.

The worker needs the matching canonical protocol and event evidence. The privately installed Synthetic Epiphany protocol, its media and participant data are not supplied by the public archive.

## Recorded evidence and publication gaps

The 11.2.1 build receipt reports **535 unique targeted checks passed**, with **0 failures, 0 errors and 0 skips**. Its build report describes:

- Existing saved Athena recording checks with exactly matching numerical results and sample exclusions; the reporting changed while recording, event, analysis-window and prior-report hashes remained unchanged.
- Historical-report explanation and bounded AI evidence checks with exact measurement references, without a provider request.
- Simulated rating workflows, malformed and mismatched evidence, missing/repeated responses, immutable attempts and managed Forge routing. Simulation is not participant evidence.
- Isolated public/private application constructor checks and the public distribution boundary.

The package explicitly records **no installation, physical hardware retest, real provider request, Zuna inference or fresh-machine installation test** for this patch. It does not certify every function. Earlier build receipts describe their own source versions and scopes. Their counts must not be summed or represented as a full regression run on 11.2.1.

Before a publication decision, the release preparation should:

1. Pin the exact public artifact and repeat its checksum comparison if any packaging change occurs.
2. Review the staged public contents, package ledgers and source bindings for that artifact. This documentation review did not independently execute its release checks or test suite.
3. Update installation, workflow, hardware and release navigation together, preserving the older guides and marking their evidence historical.
4. Publish the scope as an **alpha prerelease with targeted software evidence**, without implying a fresh installation, full functional certification or scientific validation.

Opto-ping, ladder/rung and reproducibility-program restoration should retain its own research documents, sources and evidence status. It should not be presented as a newly validated Workbench capability merely because the repository documentation is restored.

## Package documentation provenance

All paths below are inside the inspected public ZIP, under `PRAYCG_Workbench_Public_Alpha_11_2_1/`. They identify the source documents for this proposal; no private AUL source or study payload was used. Seven selected public documents are also preserved byte-for-byte in the proposed guide collection. Its [source manifest](releases/alpha-11.2.1/SOURCE_MANIFEST.json) records their relationship to the inspected archive.

| Source path | What it supports |
| --- | --- |
| [`README.md`](releases/alpha-11.2.1/package/README.md), [`CHANGELOG.md`](releases/alpha-11.2.1/package/CHANGELOG.md) | Current public workflow and the 11.1.2–11.2.1 additions |
| [`INSTALL_WORKFLOW.md`](releases/alpha-11.2.1/package/INSTALL_WORKFLOW.md) | Existing-result explanations, guided analysis, equipment policy, signal review and privacy workflow |
| [`BUILD_REPORT.md`](releases/alpha-11.2.1/package/BUILD_REPORT.md) | Current 535-check scope and explicit limitations |
| `app/config/release_identity_v1_0.json` | Runtime version identity |
| [`app/VERSION_MANIFEST_v1_0_0_alpha_11_2_1.json`](releases/alpha-11.2.1/package/app/VERSION_MANIFEST_v1_0_0_alpha_11_2_1.json) | Public edition, date, release type and current verification claims |
| [`app/deployment/validation/ALPHA_11_2_1_BUILD.json`](releases/alpha-11.2.1/package/app/deployment/validation/ALPHA_11_2_1_BUILD.json) | Current counts, parity checks, simulated-rating scope and unperformed actions |
| `app/config/analysis_orchestration_registry_v0_1.json` | Current 40-module registry |
| [`app/docs/PUBLIC_PRIVATE_BOUNDARY_ALPHA_11_0_0.md`](releases/alpha-11.2.1/package/app/docs/PUBLIC_PRIVATE_BOUNDARY_ALPHA_11_0_0.md) | Public Assistant and private AUL separation |
| `app/docs/WORKBENCH_ALPHA_11_0_0.md` | Initial public Alpha 11 workflow and assistant |
| `app/docs/WORKBENCH_ALPHA_11_0_1.md` | Ownership recovery and replay limitations |
| `app/docs/WORKBENCH_ALPHA_11_0_2.md` | Candidate revisions, analysis/media repairs and AI size checking |
| `app/docs/WORKBENCH_PUBLIC_ALPHA_11_1_0.md` | Launcher checks, installation and retained study workflow |
| `app/docs/WORKBENCH_PUBLIC_ALPHA_11_1_1.md` | Exact recording selection, observer recovery and optical display repairs |
| `app/control_center/scripts/praycg_navigation_ui_v1_0.py` | Retained stage navigation, separate session/recording/viewer context and keyboard access |
| `app/control_center/scripts/praycg_protocol_designer_v1_0.py`, `app/control_center/scripts/praycg_protocol_assistance_v1_0.py` | Shared design/export fields, revision review and installation blockers |
| `app/control_center/scripts/praycg_live_monitor_ui_v1_0.py`, `app/tools/Live_Monitor_v1_0/praycg_live_monitor_v1_0.py` | Retained replay controls, source selection and bounded multi-channel waveform display |
| `app/control_center/scripts/praycg_eeg_activity_map_v1_0.py`, `app/control_center/scripts/praycg_live_assistance_v1_0.py` | Sensor-level maps and separate local delayed features with support limitations |
| `app/control_center/scripts/praycg_ai_providers_v1_0.py`, `app/control_center/scripts/praycg_ai_assistant_ui_v1_0.py` | Public provider modes and explicit connection/request interface |
| `app/control_center/scripts/praycg_workbench_analysis_v1_0.py` | Verified acquisition context, disposition and reporting evidence |

The comparison baseline is the published 10.5.4 [Workbench changelog](../CHANGELOG.md), [guide collection](releases/alpha-10.5.4/README.md) and its public archive registry. Current repository pages still describe that baseline until a reviewed update is adopted.

[Workbench overview](../README.md) · [Installation](installation.md) · [Workflow](workflow.md)
