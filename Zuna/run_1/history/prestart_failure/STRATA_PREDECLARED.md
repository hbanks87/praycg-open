> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Stopped before any model context because priority verification failed; later attempt completed separately.

# Frozen descriptive categories for the full corrected comparison

Post-hoc development analysis, frozen before the new full model run. No model predictions or errors were inspected by this freeze script.

The primary comparison retains all **102,456 original evaluated samples** (400.218750 sample-equivalent seconds). Categories below are descriptions, never exclusions.

| Base category | Samples | Sample-equivalent seconds |
|---|---:|---:|
| all_original | 102456 | 400.218750 |
| eyes_open | 51228 | 200.109375 |
| eyes_closed | 51228 | 200.109375 |
| early_5_20 | 30721 | 120.003906 |
| late_from20_to_original_mask_end | 71735 | 280.214844 |
| proxy_local | 11180 | 43.671875 |
| proxy_outside_local | 91276 | 356.546875 |
| proxy_context_touched | 41016 | 160.218750 |
| proxy_context_untouched | 61440 | 240.000000 |

The saved mask archive additionally contains all 45 intersections of eye condition, timing interval and historical proxy category, with exact per-block counts and frozen-event counts in the JSON plan.

Early: [5,20) seconds after each observed block onset. Later: second20 through the original scoring-mask endpoint, not an invented exact55-second endpoint.

The local proxy mask and whole-context touched mask are reused unchanged from the earlier audit. Their detector parameters are preserved verbatim. They were calculated on the OLD preparation; no corrected-input detector is silently substituted. These labels are not verified blinks and untouched does not mean clean.

No new event detection or reconstruction scoring occurred. Previously frozen event indices are only counted within the declared intervals. This explicitly differs by a few samples from the older audit’s strict20–55-second timing interval.

Empty or too-short groups must remain visible as not estimable. Spectra must use contiguous within-block complete windows rather than concatenating masked fragments. Overlapping strata and repeated windows are not independent participants.

Frozen masks SHA-256: `7658f0257931484e3699bb3eeba803160baaaea89ace651b2cf8a3bce4e6420b`.

Validate all source and artifact bindings with `freeze_strata.py --validate`. The validator also checks mask nesting and partition identities. No output is overwritten by a repeated freeze.
