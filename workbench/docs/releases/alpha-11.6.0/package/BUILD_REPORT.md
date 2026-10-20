# Public Alpha 11.6.0 / AUL Alpha 1.5.0 — Revision 1: build verification

## Revision 1 and evidence lineage

The initial signed candidates passed the analysis tests below but failed a subsequent real updater check. A deeply nested QA path first exceeded Windows path limits; a shorter isolated path then exposed a genuine launcher bug. Windows PowerShell stripped embedded quotes from the Python startup probe. Revision 1 supplies the same probe through standard input, preserving its checks and failure exits.

The analysis, UI and private-extension Python files are byte-identical to the initially tested candidates. Their 1,500 passed / 15 skipped selected checks and four recording walkthroughs are explicitly inherited evidence, not newly rerun Revision 1 workflows. Only the shared launcher, enumerated release metadata and these existing release documents change. The altered launcher receives separate real-shell and failure-path tests, and final delivery requires new signed updater checks. The revision lineage and affected-test references are recorded in the release validation record.

The initial candidate ZIPs are withheld and retained as failure evidence. Use only the separately named Revision 1 archives. No operator installation, study data or original release archive is replaced by this correction.

## Scope

This release implements processing-input and reporting corrections, a separately versioned paired CAI/SID adapter, measured Gamma Scalpel reference/timing evidence, current-versus-historical Results continuity, and the optical-credit correction. The matching private AUL edition shares the Public engine and retains its existing persistence contract.

Final accepted counts and gates are recorded in `app/deployment/validation/ALPHA_11_6_0_BUILD.json`. Earlier failed development attempts are retained in private QA, not counted as passes. This document does not claim that every Workbench function or physical device is validated.

## Verification performed

Four native analysis walkthroughs passed: each edition against isolated copies of the two latest available recordings. They used actual preparation, QC, plan execution, analysis workers, report saving/opening and the saved TFR viewer. AI handoff used an explicitly labeled offline fixture, not a provider. The application ran its native event loop with a hidden main window; this was functional testing, not a pixel-level visual audit.

Each walkthrough reached a terminal result for its 13-entry plan without failed nodes. Completed, not-estimable and dependency-skipped outcomes remained distinguishable. Missing physiological inputs were not fabricated. Source inventories matched the accepted candidate, and original recording/evidence files remained read-only. Both fresh application-constructor checks and the isolated 25-test Muse suite also passed.

Separate processing checks exercise both recordings, versioned annotations, current-recipe and reviewed candidates, paired endpoint comparisons, persisted per-module explanations, and actual bundle build/verify/import/reopen. The recordings are not assumed clean controls or held-out scientific validation data.

Synthetic canonical-montage tests exercise the new CAI/SID adapter, fixed original references, baseline/condition support, gap boundaries, future-window requirements, result serialization and source tampering. Sparse Athena recordings cannot establish missing full-montage endpoints.

## Bugs found and corrected during this build

- Saved candidate reanalysis incorrectly required the exclusive interval endpoint to exist as a retained sample. The check now verifies requested original sample indices. The same half-open interval works; genuinely wider requests still fail.
- Added evidence metadata displaced one Gamma electrode's useful measurements from a bounded report. Individual measured rows now take priority over redundant aggregate rows; limits and atomic rows remain intact.
- Pilot stop handling could confuse a handled request with successful delivery. The panel now reports pending delivery, retry or I/O failure until the stop signal is actually written.
- Processing-results receipts now require matching input identity, and changing sessions invalidates the prior comparison list.
- Zero-valued measurements remain measurements rather than being narrated as unavailable.

## Installation, update and preservation

A real fresh-directory installation on the current Windows host completed the Core, Live Monitor and Hardware Connectors components. This was not installation over the operator's application and is not an independent-machine test. Installer and dependency inputs are checked against the release.

Updater regressions cover signed manifests, archive and edition matching, downgrade/tamper rejection, settings snapshots and failure recovery. A separate post-packaging QA may additionally exercise signed offline installation and guarded activation/rollback; that supplemental evidence is not a claim that a complete production restart handoff or independent-machine installation was tested.

A read-only compatibility check verified the existing independent Zuna runtime and shared model binding, without installation, weight download or inference. Preservation acceptance checks every original protected settings, recording/evidence and private-history binding, plus pinned Zuna assets and the shared-file inventory. Two append-only discovery registrations from a separately authorized approved-report recovery task were identified and retained; they did not replace prior history. This concurrent activity is recorded separately, not hidden by replacing the original baseline. The scope is selected protected state, not a byte audit of every installed dependency.

The separately developed AUL 1.3.1 approved-account recovery feature is not merged into these builds. Its new history registrations remain preserved, but this release does not claim that feature's new controls or tests.

Neither edition is installed over an existing application, activated for the operator or published by this build. No real AI requests or physical hardware sessions are performed. Public/private file boundaries are allowlisted and checked; archives are re-extracted and compared byte-for-byte. Study recordings, private histories, credentials and signing secrets are not distributed.

## Scientific and operational limits

The paired adapter records explicit new feature-source mappings and stricter temporal support. It does not claim bit-equivalence to every legacy heuristic export. Existing numerical workers and old outputs are unchanged. CAI/SID remain exploratory implemented measures, not established measures of consciousness or meaning.

Measured reference coverage is not proof of neural origin. Dual-ALS uncertainty is an engineering envelope, not a statistical confidence interval. The separate Cerelog participant-pilot software route does not certify electrical safety or physical acquisition quality. Fresh physical off-body integration and separately authorized participant testing remain necessary.

MATLAB port equivalence, independently reviewed artifact controls, held-out neural-preservation validation and universal propagation through every legacy analysis route remain unfinished. No cleaner is selected automatically. Public AI and private AUL explanations still require human content review.

See [WORKFLOW_COMPLETION_11_6.md](WORKFLOW_COMPLETION_11_6.md) for the operator workflow.
