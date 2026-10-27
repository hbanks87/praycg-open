# Evidence-grounded explanations — Alpha 10.3.6

## Responsibilities

Workers calculate statistics. Local reporting describes recorded outputs and their limits. An external language model may explain, compare and propose hypotheses. The importer checks identity, exact evidence and explicit human acceptance; it does not certify prose scientifically.

Each module explanation answers: question; findings; ordinary-language meaning; supported conclusions; uncertainty/missingness/contamination; next steps. Technical detail remains underneath. Execution, output integrity, quality and endpoint estimability are separate.

## Local contract

The existing `PRAYCG_RecordedModuleInterpretation_v0_1` envelope has additive `PRAYCG_ModuleExplanation_v1_0` fields: `six_sections`, `evidence_ledger`, `measure_definition` and provenance. Claims carry kinds and evidence identifiers. Evidence identifies source SHA-256, JSON pointer or one-based table data row/column, literal value and unit metadata. Reporting does not rerun estimators.

`implemented_measure_definitions_v1.json` records reviewed implementation hashes and operational definitions. Managed SID is a valid-duration-weighted CAI mean; its contrasts do not inherit uncertainty from a separate bootstrap implementation. NIP/CET/CET-R/EET remain exploratory proxies with disclosed lag-search, residualization and missing-value policies. These descriptions alone do not prove an older run's exact implementation; execution provenance is authoritative.

`PRAYCG_StudyExplanation_v1_0` groups observations and unavailable endpoints, links evidence and exposes reused artifacts/prerequisites. Unlike endpoints are not automatically judged to agree or conflict. Unknown recorded conditions stay unknown.

## Export and return

The existing `AI_READY_STUDY`, `purpose=explain` package accepts an exact dashboard snapshot and generates `metadata/explanation_evidence_packet.json`, instructions and a template. It preserves dataset/input identity, study/session/plan scope, actual receipt/attempt bindings, execution states, method definitions and evidence. Chain-child context and missing/failed modules remain visible.

Return the usual `PRAYCG_ExternalAnalysisReturn_v0_1` ZIP with root `RETURN_MANIFEST.json` and complete file ledger. Optional prose goes in `reports/PRAYCG_EXPLANATIONS.json`, schema `PRAYCG_ExternalExplanations_v1_0`. Keep exact packet/module bindings; record provider/model/version or disclose absence. Use six sections and distinguish observations, interpretations, hypotheses, limitations, questions and next steps.

Numerical result values use `{{ev_identifier}}` placeholders; the importer substitutes exact verified values. Observation claims need evidence. Do not silently round, calculate ratios or claim unexecuted work. Placeholder checks are not a general semantic or mathematical proof; misleading units, prose or conclusions remain possible.

## Review and stale results

Staging is inert and compatible with older returns. Structured explanations receive readable review followed by explicit named acceptance. New derivatives under `accepted_explanations` preserve review notes, model metadata, original returned prose, evidence and report hashes. No original is overwritten and no returned code executes.

Accepted module prose appears only while its study/session/plan, receipt/attempt, status, definition/dependencies and evidence match. A new attempt invalidates old prose even with identical values. Study synthesis additionally requires matching represented results. Missing/changed derivatives are withheld, not silently replaced with another study's explanation.

The structured round trip expects original locally exported source evidence to remain accessible and unchanged on the reviewing machine. Arbitrary relocation is not silently remapped. Portable Research Bundle verification is a separate feature.

## Failure and privacy

Reporting failures cannot relabel a successful numerical worker as failed. Historical rebuilds create separate explanation revisions without unlocking plans or rerunning analysis.

Private packages may include full biosignals, responses, absolute local paths and identifiers. Neither an evidence packet nor prose is automatically anonymous. Review permission and consent before manual sharing. This workflow does not upload, call a provider or install a language model.
