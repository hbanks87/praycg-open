# PRAYCG Alpha 10.3.12 — Installation and workflow

This patch makes optional Zuna model files reusable across releases. It does not change reconstruction methods, model weights, quality thresholds or the retained 10.3.11 timing policy. Downloading this release alone does not move an existing installation or start analysis.

## Upgrade without disturbing a study

1. Finish recording, stop LabRecorder and managed streams normally, then close the older Workbench. Keep your recordings, workspace, incomplete attempts and reports.
2. Extract the complete ZIP into a **new writable folder**. Do not merge releases, run inside the ZIP, copy an old Python environment into the new release, or edit historical hashes to force compatibility.
3. With native Windows Python 3.11 and Tcl/Tk available, run **INSTALL.bat**. Normal setup prepares separate Core, Live Monitor and Hardware Connectors environments. `INSTALL.bat -Mode minimal` prepares Core only. Normal setup does not install Zuna.
4. Run **START_PRAYCG.bat** and confirm **Alpha 10.3.12**. Choose **Use Bundled Paths**, then check your separate PsychoPy, LabRecorder and study paths. Existing workspace data remains separate.
5. If you want Zuna, follow the optional installation below. Ordinary Required QC does not require it. Review or regenerate analysis preparation when the saved source bindings differ; older results and incompatible checkpoints remain historical.

Python, PsychoPy, LabRecorder, model weights and installed environments are not included in this ZIP. Preserve previous releases until you have checked the new one.

## Optional Zuna: install once per release, share the large assets

Double-click **INSTALL_ZUNA.bat**, or run:

```text
INSTALL.bat -Mode zuna
```

The default shared root is `C:\PRAYCG\shared\Zuna`. The installer remembers a successful custom shared-root selection for later installations (or reports if it could not save that preference). If a compatible verified cache is available, its model files and pinned Zuna wheel are reused; otherwise the installer obtains the required assets. The model is approximately 1.53 GB. A separate shared pip-download cache can reduce repeated dependency downloads; it is not a copied environment or a complete transitive lock. Python packages can still require downloads even when the model is cached. The installer requires at least 8 GB free space at the release location and 2 GB at the shared location.

To choose another shared location, run from the extracted release folder:

```text
INSTALL_ZUNA.bat -SharedZunaRoot "D:\PRAYCG Shared\Zuna"
```

To explicitly offer a previous extracted release as a source of existing model files:

```text
INSTALL_ZUNA.bat -ImportZunaFrom "C:\PRAYCG\PRAYCG_ControlCenter_v1_0_0_alpha_10_3_11"
```

The two options may be combined. `INSTALL.bat -Mode zuna` accepts the same options. The installer can also inspect its own legacy local model folder and a bounded set of adjacent PRAYCG releases; it does not scan the whole computer. A reusable asset must match its pinned filename and cryptographic hash, plus the expected size where recorded in the lock. An import copies eligible model assets and the pinned wheel only: **not** the old Python environment, EEG, study reports or inference checkpoints. Original files remain in place. Do not delete an older model copy solely because this release was extracted; first complete and check the new installation.

Each shared model folder is keyed by its upstream revision and locked asset manifest. A different model revision uses a different folder. Each release retains:

- `app/.zuna-env`: its isolated Python environment;
- `app/.zuna-installation/`: its lock/requirements-bound installation receipt and notices;
- `app/.zuna-storage.json`: its local binding to the selected shared model and receipt.

These local installation records are not public release files. They are not substitutes for recorded analysis provenance. Legacy installations remain supported according to their original local receipt; they are not silently rewritten by merely opening the Workbench.

### Check without installing

```text
INSTALL_ZUNA.bat -CheckOnly
```

This inspects the release's current installation without downloading, installing or importing assets. A failure is a request to repair the installation, not permission to bypass model verification. Do not combine `-CheckOnly` with `-ImportZunaFrom`. Analysis itself does not install packages, download model files or upload EEG. Review the unresolved upstream notice/provenance limitation in the [Zuna methods guide](ZUNA_METHODS_ALPHA_10_3_0.md).

## Continue the selected Zuna run

1. Open the correct workspace/session and **Analysis Forge**. Confirm the XDF and bound run UUID. Do not rename the original reviewed v2 contract to look like a legacy v1 contract.
2. Run **Required QC** if the new analysis context requests it. Inspect the original validation contract, observed blocks and other automatically discovered inputs. Quality cautions remain part of the record.
3. For the supported host-receipt timing route, preserve the exact same-run, stopped bridge manifest and completed chunk diagnostics. Unsupported, active, conflicting or stale evidence cannot authorize the derived timing route.
4. If an older optional ALS declaration names the wrong source, use **Review ALS stream binding** after QC and before locking a new plan or preparing a comparison. A named review and reason create a separate hash-bound post-hoc artifact; the original contract remains untouched. A corrected source identity does not itself establish optical timing.
5. In the optional Zuna panel, check installation, review inputs and create a new preparation when required. Inspect its outcomes and provenance. Preparation alone does not execute the model.
6. Explicitly start the prepared comparison when ready. After completion, review Zuna versus interpolation, all declared blocks, cautions and timing provenance. A software pass is not evidence that Zuna performs better. Include actual results in a privacy-reviewed research bundle; full waveform telemetry remains opt-in.

The retained host-receipt policy is a narrow evidence-supported analysis time estimate, not measured per-sample hardware timing or a cross-device synchronization certificate. Original XDF samples/timestamps and QC remain unchanged. Read the [10.3.11 timing guide](INSTALL_AND_WORKFLOW_ALPHA_10_3_11.md) for its exact route, counter/chunk checks and limitations.

## Verification and limits

The current build record is `app/deployment/validation/BUILD_VALIDATION_v1_0_0_alpha_10_3_12.json`. It distinguishes behavioral tests with small synthetic assets, broader regressions, synthetic analysis acceptance and extracted-package integrity from a real download, clean installation, physical recording or model inference. This build does not perform those latter operations or migrate your installed files. Installation verification is not scientific validation.

After Core setup, a read-only software integrity check from the extracted release folder is:

```text
app\.core-env\Scripts\python.exe -B app\tools\Release_Validation_v0_1\praycg_public_release_check_v1_0.py --package app --output ..\praycg_10312_integrity.json
```

Keep the report outside the release. Mutable environments and local installation records are excluded from the immutable software ledger; the optional installer/runtime verify their own bindings separately. Add `--tests` to run supplied regression suites. No recording is uploaded by these checks.

Use this guide as the current entry point and root `CHANGELOG.md` for history. The [10.3.8 workflow](INSTALL_AND_WORKFLOW_ALPHA_10_3_8.md), [Zuna integration guide](ZUNA_INTEGRATION_ALPHA_10_3_7.md) and [bundle workflow](WORKFLOW_ALPHA_10_2_1.md) remain reference material. Generated EEG remains an estimate; measured targets are not clean neural ground truth, and windows within one recording are not independent replications.
