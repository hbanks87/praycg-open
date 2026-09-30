> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Four fixed five-second contexts, not an independent recording or a full endpoint. See subsequent priority-status correction in prestart history.

# Boundary-safe offline preparation candidate

Policy: `PRAYCG_ZUNA_OFFLINE_BLOCK_CENTER_LINE_RESAMPLE_V1_0`.

Only the isolated `candidate_app` Zuna worker and exploratory wrapper were changed. The installed Workbench, published 10.3.5 source/archive, original recording, frozen recipes and previous comparisons are unchanged.

Each independently governed preparation interval now has its per-channel arithmetic mean removed **before** polyphase resampling. Resampling explicitly uses `padtype='line'` (linear endpoint extension), rather than the implicit zero-padded boundary. Each channel's mean is calculated separately; held-out channels cannot influence retained-channel centering, reference or model normalization. Finite-value checks reject numerical failures after centering, resampling or filtering.

The existing 256-Hz grid, fourth-order 0.5–40-Hz zero-phase filter, retained-only reference, source-fractional-index/timestamp mapping, caller-selected intervals and exclusions, common post-prediction comparison filter, model parameters and five-second model contexts/reflected tails remain unchanged. Source offsets are not restored after band-pass preparation.

Returned preparation and both prospective/exploratory artifact paths expose the new policy, worker fingerprint, per-interval removed channel means, padding/filter/reference details and explicit noncausal/offline limitation. Frozen acquisition contracts and recipes are not rewritten; these are versioned derivatives, not reproductions of the old execution. New output folders are required because preparation identities change.

This change addresses DC-offset interaction with resampling boundaries. It does not promise elimination of all filter transients, model-context seams, blink contamination, or physiological artifact. Full-interval centering and zero-phase filtering use future samples and must not be presented as live/causal processing.

Regression results and the separately declared short model comparison are recorded alongside this note; this note alone does not claim test success or model benefit.
