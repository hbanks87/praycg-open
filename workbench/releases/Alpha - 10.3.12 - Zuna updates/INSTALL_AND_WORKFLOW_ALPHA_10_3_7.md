# PRAYCG Workbench Alpha 10.3.7 — Installation and workflow

## Safe upgrade

1. Finish or stop recording and analysis before closing the old Control Center. Back up study folders separately.
2. Extract the entire new ZIP into a new writable local folder. Do not merge `app/` with an earlier version or run from inside the ZIP. Keep all six top-level files beside `app/`.
3. Use native Windows Python 3.11 with Tcl/Tk and run **INSTALL.bat**. The normal installation prepares Core, Live Monitor and Hardware Connectors. It does not include PsychoPy, LabRecorder, vendor programs or Zuna.
4. Start **START_PRAYCG.bat**. Confirm Alpha 10.3.7 in the application, choose **Use Bundled Paths**, and review external PsychoPy/LabRecorder, workspace and hardware paths.
5. To use the optional model, run **INSTALL_ZUNA.bat**. It uses this release's isolated environment/model directories and explicitly downloads large dependencies/model files. Do not manually mix an old environment with new application files. **INSTALL_ZUNA.bat -CheckOnly** checks without installing.

The software ZIP is self-contained application source/assets, not an offline bundle of Python, all external software or model weights. Installing a new release does not migrate, rerun or improve old recordings automatically.

## Ordinary study workflow

1. Open a workspace, select the protocol and prepare its required materials.
2. Review stimulus identity, protocol-dependent runner configuration and hardware selections.
3. Connect sources and inspect metadata, channels, units and timing. Software PASS is not electrical or participant-safety approval.
4. Run equipment checks, review permitted warnings, confirm and arm. Experimental hardware retains its restrictions; Bench Test Mode does not authorize participant use of an experimental route.
5. Record with LabRecorder and run the locked protocol. Preserve events, hardware information and run evidence with the XDF. PRAYCG does not start or stop LabRecorder for you.
6. Select/prepare the correct run for analysis, verify the XDF identity and run Required QC.
7. Select modules/recipe, lock the plan and execute it. Dependencies run before consumers; this patch introduces no new QC or planning gateway.
8. Review **Analysis Forge → Results**, per-module reports and **Study Explanation**. Failed, skipped and not-estimable modules remain visible.

The [recording and analysis policy](RECORDING_ANALYSIS_POLICY_ALPHA_10_3_5.md) and [detailed acquisition reference](INSTALL_AND_WORKFLOW_ALPHA_10_3_5.md) remain applicable except that this guide supersedes their Zuna preparation behavior.

## Optional corrected Zuna comparison

1. Open the intended recorded run and finish Required QC. Optional Zuna is not needed for ordinary QC or other analysis.
2. In **Optional Zuna — review → prepare → run → compare**, check installation, then review inputs. Confirm the actual physical electrode map and reference; do not substitute protocol assumptions for wiring evidence.
3. For an existing recording needing post-hoc review, use **Review existing recording** and save/select its explicitly reviewed recipe. Do not edit an original acquisition contract. Timing assumptions and inherited BENCH/QC labels remain visible.
4. Choose CPU threads and press **Prepare comparison**. Preparation checks inputs and freezes current source/preparation identity without model inference.
5. Only if you want another numerical comparison, press **Run prepared comparison**. This is explicit new computation and can take substantially longer than the recording. An upgrade alone does not require rerunning a completed historical comparison.
6. **Cancel safely** requests a stop after the current context. Resume only an interrupted attempt whose inputs, preparation, source, model and resource bindings still match. An older incompatible attempt is preserved; prepare a new comparison rather than modifying its identity files.
7. Open the saved report. Read preparation identity, execution state, comparison outcome and evidence class separately. Compare overall, eyes-open and eyes-closed errors, the mandatory companion endpoint and spectral/alpha differences. Insufficient support means no estimate, not no effect.
8. Open private comparison traces only when needed. They contain EEG-derived telemetry. Generated values are not measured electrodes and are not automatically substituted into another analysis.

The corrected pipeline remains offline/noncausal and experimental. Lower error in one condition does not establish general cleaning or live-decoder benefit. See [integration decisions and limitations](ZUNA_INTEGRATION_ALPHA_10_3_7.md).

## Plain-English and historical explanations

Use **Open ▾ → Plain-English findings** on a Results card. The six questions explain recorded findings and limitations; technical detail supplies literal values and source references. **View individual report** opens the original numerical report. **Study Explanation** consolidates available results without treating shared-data calculations as independent confirmation.

For an older session, choose it in the Results selector and press **Explain existing results**. This creates a separate versioned explanation, not a new numerical analysis or an unlocked plan. Missing old fields remain missing. Explaining an older Zuna result does not apply corrected preparation or create uncomputed eye-condition/spectral summaries. Reporting failures remain separate from numerical execution outcomes.

## AI-ready export and reviewed return

1. Select the matching study/run and finish or pause changing analysis outputs.
2. Choose **AI-ready study package → Explain existing results**. A locked plan supplies the module/attempt/evidence snapshot; a general archive without such a plan is not a module-bound explanation snapshot.
3. Review contents and privacy/consent before manually sharing a package. Full telemetry can include identifying data. No automatic upload or external API call is added.
4. Ask the receiving agent to follow the supplied explanation instructions and structured return template; recorded measurements must not be invented or silently recomputed.
5. Choose **Review AI Return…** and select the returned ZIP plus the exact original export. Content is initially staged as untrusted external work.
6. Read the six-section explanations, model details and evidence. Enter a reviewer name, then explicitly accept only what you have reviewed. Closing leaves the return unaccepted.
7. Open **Reviewed AI explanation** beside numerical results. Changed attempts/evidence invalidate stale explanations. Identity/value checks do not prove scientific correctness.

See the retained [AI-return detail](EXPLANATIONS_AND_AI_RETURN_ALPHA_10_3_6.md). AI protocol and EEG recipe/module authoring retain their separate [review and intake boundaries](AI_AUTHORING_WORKFLOW_REVIEW.md); an explanation return cannot install a runner, approve a module or unlock a plan.

## Bundle and verification boundaries

Module summaries/provenance use the existing research-bundle workflow. Private full-study bundles may include full telemetry only with explicit selection; public-oriented bundles retain exclusions and still require human review. Imports remain inert. No automated publication authority, clinical validity or participant eligibility is conferred.

Read the shipped Alpha 10.3.7 build-validation record for exactly which tests ran. Synthetic/stub tests, syntax checks and archive verification are not actual device validation, new human/model inference, fresh full installation or independent second-machine testing.
