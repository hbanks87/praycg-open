> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Synthetic/runtime engineering comparison, not biological replication.

# Zuna CPU-thread benchmark — 26 September 2026

Eight threads was fastest on the synthetic five-second test. Two fresh calls
were made at each setting with the same input, model, seed and 16 sampling steps.

| CPU threads | First sampling time | Second sampling time |
| --- | ---: | ---: |
| 2 | 53.3 s | 53.0 s |
| 4 | 36.0 s | 35.8 s |
| 8 | 31.5 s | 22.0 s |

Model loading is excluded from these figures and recorded separately. The
original two-thread analysis continued during the benchmark, so these are
concurrent-workload measurements, not a guarantee of sustained speed.

Repeated predictions were bitwise identical within each thread setting.
Across settings they were not bitwise identical. For eight versus two threads,
the largest synthetic prediction difference was approximately 0.000058 microvolts;
relative RMS difference was approximately 0.0000027. These passed the engineering
consistency thresholds, not a scientific-equivalence test.

## Final action: keep the existing run

The first estimate favored an eight-thread restart. A new attempt was prepared,
but immediately before stopping the old worker the required fresh progress check
found that the restart no longer met the predeclared minimum savings threshold.
The stop was refused, and the subsequent duplicate-run guard also refused launch.
The original worker was never interrupted.

At the follow-up check, 21 windows had completed and recent full windows were
taking about 40 seconds. The conservative fresh eight-thread estimate was about
56 minutes. Keeping the ongoing run avoids discarding its progress under this
timing uncertainty. No two-thread and eight-thread prediction caches were mixed.

The active comparison remains `alpha1031_zuna_comparison_20260926_attempt1`.
The separately prepared eight-thread attempt is explicitly marked **NOT_LAUNCHED**.
Completion monitoring remains attached to the original run. Raw recordings,
installed software and the released Alpha 10.3.1 source were not modified.

Exact evidence: [benchmark results](benchmark_result.json),
[predeclared policy](benchmark_acceptance_policy_v1_0.json),
[initial estimate](switch_decision_v1_0.json), and
[final execution decision](final_execution_decision_v1_0.json).
