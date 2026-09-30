> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Four fixed five-second contexts, not an independent recording or a full endpoint. See subsequent priority-status correction in prestart history.

# Independent saved-result verification

**PASS — no blocking mismatch found.** This review performed no new inference and changed no application source or original data.

All four cases, their frozen selections/seeds, source and data bindings, committed prediction checkpoints, and model provenance verified. The generated arrays exactly match their checkpoint arrays; no context was reported as resumed. Each context contains 1,280 samples and every selected sample passes the original scoring mask.

An independent calculation checked **584 numeric values**, including per-case and pooled waveform metrics and per-context spectral powers. The largest observed waveform-metric difference from the report was **8.88 × 10⁻¹⁶**, within the stated numerical tolerance. Original and corrected targets/baselines were also matched exactly to the saved preparation arrays.

| Same fixed 20-second selection | Spline RMSE | Zuna RMSE |
|---|---:|---:|
| Historical preparation | 5.739697 µV | 5.073030 µV |
| Corrected preparation | 5.734792 µV | 5.058575 µV |

**The chosen intervals already favored Zuna before the correction.** The short comparison does not demonstrate that the correction created that advantage or reversed the earlier whole-recording result. The corrected and historical prepared targets differ, and four contexts from two blocks are not independent validation.

The Markdown/HTML report and scientific plot were inspected. They preserve the post-hoc BENCH designation, old negative result, changed-target caveat, imperfect proxy labels, different scoring/filter endpoint, and remaining timing/coordinate/context limitations. P3 is correctly disclosed as slightly worse for Zuna in the corrected sample.

One optional clarification: pooled NMSE uses each electrode's target variance across the pooled 20 seconds; it is not the arithmetic average of the four context-specific NMSE values. The ten-minute execution bound is a cooperative inference-phase soft deadline, not a hard limit on all earlier preparation.

Exact verified artifact hashes and check scope are preserved in `independent_result_verification.json`.
