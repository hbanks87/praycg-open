# Proposed protocol-ratings attribution correction

**Status: reviewable fix; not applied to the preserved distribution.**

The unchanged `PRAYCG_Workbench_Public_Alpha_11_2_1.zip` has SHA-256 `cb65ec3180a59a9181e4fecd9bb94a2b136ab158f0f275eaf49b01dc3386c42b`. Its managed protocol-ratings route is blocked by an attribution-registry schema mismatch before the analysis worker starts. This is a packaged launch issue, separate from scientific validation or the availability of valid rating data.

## Affected record and proposed change

In `app/config/attribution_registry_v1.json`, method `protocol_rating_last_valid_v0_1` lacks `functions` and `definition`. The exact [preserved registry](../package/app/config/attribution_registry_v1.json) has SHA-256 `d9b7c57bd2fda58725945608a12e28cd91553186709c0e3a5dd1f272a64f3207`.

The current managed launcher wraps `protocol_ratings_v0_1` with `app/tools/Attribution_v1/run_with_credits.py`. At line 39, that observer indexes `method["functions"]` during setup, before invoking the worker. The missing key raises `KeyError: 'functions'`.

The [standalone patch](protocol-ratings-attribution.patch) adds only:

- `functions: ["analyze_events"]`, naming the existing function in `app/tools/Protocol_Ratings_Analysis_v0_1/protocol_ratings.py`.
- `definition`, copied verbatim from the record's existing `implementation` text, so an observed method has the field required by the credits aggregator.

The ratings source hash remains `9110809024fe73a45d760f959ca903de620d4819400fbde069c1a69638ab4069`. Source code, scientific calculations, existing registry fields and the preserved package snapshot are unchanged.

The existing rating policy selects the last admissible allowed key in a completed observed `[onset, offset)` rating window, ordered by recorded `response_time_seconds`, with original `event_index` breaking ties. Earlier valid keys remain in the ledger as superseded; missing or interrupted windows do not acquire an imputed rating. Condition-coded ordinal comparisons remain descriptive, with no equal-interval, causal or population inference. The patch changes none of these rules.

## Isolated verification on 13 October 2026

Exact ZIP copies of the observer, credits helper, registry and hash-bound ratings source were used with a harmless sentinel worker. No rating analysis, study, installation or release publication was run.

| Check | Original registry | Proposed registry |
| --- | --- | --- |
| Observer exit | 1; `KeyError: 'functions'` at line 39 | 0 |
| Sentinel worker entered | No | Yes |
| Credits file produced | No | Yes; valid content hash |
| Source-hash mismatches | Worker not reached | None |
| Observed analysis methods | No credits record | Empty, correctly reflecting that the stub ran no analysis |

`git apply --check` accepted the patch against the exact original registry. Static inspection confirmed that `analyze_events` exists, its source hash matches, and the added fields satisfy the observer/aggregator shape. The proposed registry bytes have SHA-256 `e8032fb8867bbbba8e0242e2a3f1fbf6fe99ea5b4f5e7bb499645bb478950fd9`; the patch has SHA-256 `33d8c22e22d61cc031dfb6c983371ee03c947e9a7c1e9ae02a95fb3ba1ee25f0`.

This verifies the narrow attribution setup repair. It does not establish successful analysis of real rating inputs or a complete release check. A future corrected application package needs its own version, archive hash and managed-route verification; this repository supplement does not replace or silently repair the unchanged ZIP.
