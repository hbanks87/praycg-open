# Public Workbench and optional private extension

PRAYCG Workbench Alpha 11.0.0 is a complete public research application. AUL is not included in the public archive and is not required to install or use the Workbench. This is an intentional product and source boundary, not a claim of legal clearance, novelty or model superiority.

## Intentionally public

- Hardware profiles and connectors, acquisition ownership and recording controls, LSL/XDF handling, Live Monitor and replay.
- Protocol catalogs, stimulus preparation and fingerprinting, protocol configuration, data-only extension validation and the existing protocol runners.
- Numerical analysis workers, Analysis Forge, deterministic recommendations and execution checks, local explanations, reports, visualizations and research-bundle verification.
- The PRAYCG AI Assistant: optional provider connections, bounded requests, source-grounded report drafts, reviewed protocol drafting and explicitly requested passive signal explanations.
- Ordinary request receipts, versioned drafts, source hashes, exact operator approvals, request allowances, credential protection, scientific limitations and failure reporting. Safety and reproducibility are public features.
- A small extension contract. An optional extension calls shared Workbench services rather than supplying a second copy of the research application.

Shared source entry points are `praycg_workbench_analysis_v1_0.py`, `praycg_protocol_assistance_v1_0.py`, `praycg_live_assistance_v1_0.py`, `praycg_ai_services_v1_0.py`, `praycg_ai_accounts_v1_0.py`, `praycg_ai_providers_v1_0.py` and `praycg_extension_api_v1_0.py` under `app/control_center/scripts`. The public UI is `praycg_ai_assistant_ui_v1_0.py`. Common native adapters and protective validation were deliberately extracted for public use. They were not made private merely because an earlier experimental interface used them.

## Separately packaged, private

AUL's private state implementation and private extension entry point belong to a separate package with its own terms, manifest and compatibility declaration. Private policies, prompts, research histories, evaluation fixtures, unpublished experiments and potential training collections do not belong in the public release. Existing private experiments elsewhere on a developer's computer are not release inputs.

The public assistant uses a newly implemented ordinary receipt store, not the private hash-linked AUL ledger. It neither discovers nor automatically imports private history. It does not claim to train a model, propagate a general evidence-dependency graph or establish an AUL reasoning advantage.

## Authority and privacy

The native Workbench performs calculations and validates supported actions. A model response is data, never executable authority. Consequential actions still require the existing review and acquisition gates. Neither assistant can silently arm equipment, start a participant protocol, install arbitrary returned code, change raw results or make a passive observer into a closed-loop controller.

Model requests are optional and explicit. Selected evidence and prompts may leave the computer when a remote provider is chosen. Review them for participant identifiers and sensitive content first. Request receipts stay local outside research exports by default. A local bundle is not an authorization to upload it.

## Compatibility and migration

The public extension API is version 1. The private launcher must verify its own manifest and the Workbench compatibility requirements before running trusted extension code. The public launcher does no extension discovery. Installing or reopening the public release must work when AUL is absent from disk and Python's import path.

Old releases, study identities, marker namespaces, results and private state remain unchanged. Alpha 11 uses a separate public assistant state directory. No private allowance or approval is silently transferred to it; new model use needs explicit allowance. Opening an old study does not require opening or migrating an old assistant history.

## Release-content gate

The release uses an explicit file allowlist, per-file checksums and an archive inspection. Unknown additions, private runtime imports and private state files are rejected. Installed environments, credentials, caches, raw participant recordings and nested archives are not public release inputs. Historical private assistant test fixtures and implementation guides are excluded even if their names look like ordinary release documentation.

The gate protects this declared boundary. It is not a repository-wide provenance or legal audit, and does not replace the retained third-party license notices. See `BUILD_REPORT_ALPHA_11_0_0.md` for the actual tests and remaining limitations.
