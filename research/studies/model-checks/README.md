# Model checks: reproducibility and failed qualification

These two packages publish executable numerical methods, generated inputs, fixed seeds, protocols, expected behavior, historical qualification results and source provenance. Neither contains human data. Software execution and scientific qualification are reported separately.

| Package | Small executable check | Historical full-study result |
|---|---|---|
| [AIGP model recovery](aigp-model-recovery-20261107.zip) | Build the source-only Windows likelihood kernel; independently check densities/gradients/aliases; fit and predict reserved nonproduction fixtures. | All seven scenario screens failed. Shared gate/attention/memory remain observational aliases. |
| [GNT measurement qualification](gnt-measurement-qualification-20261107.zip) | Generate four bounded-process fixtures; reproduce signed-integral/smoothing counterexamples; run independent estimator and decision-rule checks. | Replacement qualification failed, 10/23 checks passed; no general coherence-lifetime instrument established. |

Check [SHA256SUMS.txt](SHA256SUMS.txt) before extraction. Each README supplies exact bounded and full-run commands, pinned NumPy/SciPy versions, failure criteria and PUBLIC_VERIFICATION.json. Full expensive operating-rate studies were not rerun for public packaging. Retained historical results are explicitly labeled and bound to their source hashes.

Original algorithm/configuration files are copied unchanged. Fresh full reproduction creates a new integrity binding, never a replacement historical preregistration. The AIGP aggregator correction remains a separate documented sibling; original failed code is retained. Generated records, shared aliases and repeated seeds must not be counted as independent human replications.
