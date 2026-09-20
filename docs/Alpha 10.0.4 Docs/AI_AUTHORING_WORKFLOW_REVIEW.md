# AI-assisted authoring: workflow review and next steps

Alpha 10.0.4. This review separates what the workbench can actually execute from design assistance and review staging. No files are automatically uploaded to an AI provider, and no returned code is automatically executed.

## The central finding

The previous workflow did not support a complete casual-user loop from an AI protocol document pack to installing a new runner. The document builder produced a design brief; the return reviewer staged a candidate. It did not admit the candidate to the runnable library. Similarly, the EEG recipe editor configured existing packaged analysis methods; it was not an analysis-module installer.

These are product gaps, not user mistakes. A successful structural check cannot truthfully be presented as a working new protocol or a scientifically validated analysis.

## Three distinct authoring paths

| Desired change | Correct artifact | Current boundary |
|---|---|---|
| Design a protocol using already implemented task primitives | Declarative protocol JSON plus references, materials contract, timing and limitations | Export instructions/examples, review the return and stage a candidate. New runnable-library admission remains developer work. |
| Change supported settings of an existing EEG analysis | Parent-bound, declarative recipe proposal | Review a diff, load permitted settings into the recipe editor, then use normal validation and an immutable recipe/plan revision. It does not add a new mathematical method. |
| Add a new stimulus engine, device behavior or analysis algorithm | Reviewed software extension with source, dependency/license records, numerical tests and capability contracts | Separate development/integration path. Not accepted as arbitrary executable code through either casual-user importer. |

An EEG event recipe is also not a universal numerical preprocessing recipe. Only settings that the actual worker consumes belong in its supported return contract. Installing a package or citing a method does not establish that PRAYCG executes that method.

## Changes made in this patch

Protocol AI handoff material now identifies supported return formats, existing engine capabilities, schema/examples and the exact review-only endpoint. The interface calls the action **Review AI Protocol Return**, not a compiler/installer. A timeline preview remains a preview; new protocols are not silently added to the runnable catalog.

The EEG recipe workflow preserves previously stored settings that the dialog does not expose, including the existing event-condition subset and RSA model matrix. Silent loss of those fields can change calculations. A changed condition order with an existing RSA model requires an explicit compatible revision, not guessing how to reinterpret matrix rows.

The shared behavioral runner now accepts the manifest handoff used by Control Center. The packaged-path checks and the acquisition lock/lease remain required. Dry-run checks cover all 14 protocols using that shared entry point; they do not demonstrate physical stimulus timing or participant safety.

Source citations and authorship are structured across all 67 protocol definitions. Hoyt Banks is credited for PRAYCG development/adaptation, separately from external study/dataset authors. Citations are not permissions or scientific approval.

## What a genuinely seamless extension system still needs

1. **One versioned extension contract.** An extension declares its type, supported PRAYCG versions, dependencies, inputs/outputs, events, units, timing, source citations, license, limits and tests. It must say whether it uses an existing engine or introduces code.
2. **A guided export wizard.** Choose a base task/method and intended change; export only reviewed context. Include exact schemas, valid examples and a bounded validator. Do not send raw data or personally identifying paths by default.
3. **An explicit return contract.** Ask the AI for named files, source references, assumptions, unimplemented requirements and test evidence. Reject invented approval, unsupported features and claims of tests it did not run. The AI model/version is provenance, not an eligibility badge.
4. **Local admission and failure recovery.** Verify package paths and integrity, check compatibility, show a plain-English diff, validate structure and inputs, and run bounded synthetic tests. Admission must register every required protocol/stimulus/configuration/runner/analysis relationship, not merely copy a JSON file into a directory.
5. **Separate permissions for new code.** A package hash verifies identity, not safety. Newly generated Python needs a reviewed extension host, suitable isolation, resource/network/file-access policy, dependency management and rollback. A subprocess alone is not a security sandbox.
6. **A final human decision with honest labels.** Distinguish structurally valid, software-tested, hardware-tested and scientifically supported. Require relevant participant safeguards; exploratory does not mean unrestricted or validated.
7. **Persistent provenance and an end-to-end acceptance test.** Export brief → simulated AI return → validation → authorized admission → runner/analysis → individual report → bundle → reimport. Also test malformed returns, stale parents, missing dependencies, failed runs and retries. Keep historical studies immutable.

For new analysis modules, synthetic tests should verify known numerical answers, null/degenerate cases, units, missingness and expected failure outcomes—not only a zero process exit. Machine-learning methods additionally need leakage controls and genuinely held-out evaluation appropriate to the claim.

## Practical release position

The workbench can be described as **AI-assisted study design and governed analysis configuration**. It should not yet be advertised as “upload any AI-generated runner or analysis and run it.” Full protocol and executable-module admission is a distinct next development milestone; this patch deliberately does not weaken existing runtime authority to imitate that capability.

No claim is made that an external GPT agent was invoked during local synthetic workflow tests. Handcrafted return fixtures test PRAYCG's contracts; model reliability and a user's cloud upload/download experience require separate acceptance testing and privacy review.
