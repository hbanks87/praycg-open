# Carry the public stimuli with each Workbench release

## Current release procedure

For every public Workbench release, attach the two ZIPs from the [11.2.2 source release](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.2.2) with each matching `.manifest.json` and `.zip.sha256`.

| Source ZIP | Bytes | SHA-256 |
| --- | ---: | --- |
| `PRAYCG_OPTIONAL_MASTER_STIMULI_7_20261013.zip` | 691,949,836 | `e851f0a6bea03ea381efe4c96c9a93685e6afdbfc9ecf05bdfd29741e6ca0a4b` |
| `PRAYCG_ORIGINAL_LANTERN_INSTALLER_20261014.zip` | 106,117,274 | `52ce56874fac1e4320822e8d71e3668836e6744a434c9e96508466081ea84280` |

Compare all six source and destination asset names, sizes and SHA-256 digests. Keep any identical existing asset and stop for review on a mismatch. The Workbench continues to download from its pinned 11.2.2 URLs. The full eleven-master collection remains available for local review.

## Historical automated procedure for 11.9.2

The instructions below record the October 26, 2026 publication. The workflow and scripts were later removed from the default branch.

At that time the public release workflow was installed and its [first verified run](https://github.com/hbanks87/praycg-open/actions/runs/40434259585) attached all six companions to [Public Alpha 11.9.2](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.9.2). The existing application assets and tag retain their identities. Review the [workflow](https://github.com/hbanks87/praycg-open/blob/ecb6986651b3930d98fea9db1106069a7dbbd30b/.github/workflows/public-release-stimuli.yml), [helper](https://github.com/hbanks87/praycg-open/blob/ecb6986651b3930d98fea9db1106069a7dbbd30b/scripts/attach_public_stimuli.py) and [offline tests](https://github.com/hbanks87/praycg-open/blob/ecb6986651b3930d98fea9db1106069a7dbbd30b/scripts/tests/test_attach_public_stimuli.py).

On each published `PRAYCG_Workbench_Public_A<major>.<minor>.<patch>` release, the workflow copies the two existing public packs and their matching manifest/checksum companions from Public Alpha 11.2.2. The fixed six-file allowlist contains the reviewed seven-film archive and original Lantern installer archive. The full eleven-master collection remains outside this distribution. The archives are copied without re-encoding or changing their rights records.

The helper validates the repository, published release, asset names, byte counts and SHA-256 values. It checks every existing target asset and downloads/verifies every missing source before uploading anything. Identical assets are skipped. Conflicts stop the run; existing assets are never deleted or replaced. An upload interrupted after validation can leave a partial set; rerunning resumes missing files and skips complete identical assets. If GitHub retains an incomplete named asset, the helper stops for operator review rather than deleting or replacing it automatically.

The workflow uses the maintained helper from `main`, a full-commit pin for `actions/checkout` v7.0.1, and `contents: write` only for the attachment job. The token is passed to GitHub CLI and is not persisted by checkout. Inputs pass through an environment variable and are validated before CLI calls.

### Existing release or recovery in the historical workflow

To fill a later existing release or retry a stopped run, open **Actions → Attach verified public stimuli → Run workflow** with that release's exact public tag. The initial 11.9.2 attachment has already completed. This does not create or move a tag or change the Workbench ZIP/signature.

For a local operator with Python 3.11+ and authenticated GitHub CLI:

```sh
python scripts/attach_public_stimuli.py --tag PRAYCG_Workbench_Public_A11.9.2
python scripts/attach_public_stimuli.py --tag PRAYCG_Workbench_Public_A11.9.2 --apply
```

The first command downloads and verifies missing assets without uploading. The second performs the authorized attachment. The initial transfer is approximately 798 MB. Existing assets with GitHub SHA-256 metadata need no repeat download; older assets without that digest are verified from their bytes.

The installed 11.9.2 manifest remains pinned to the original 11.2.2 URLs, which continue to work. These added attachments provide the same bytes on every later release. The matching companion manifests intentionally preserve their original pinned URLs; this helper does not rewrite historical package identities. A future installer can use its explicitly supported `--archive-directory` or `--url` options with these identical assets.

### Verification in the historical workflow

```sh
python -m unittest discover -s scripts/tests -p 'test_attach_public_stimuli.py' -v
```

The offline tests cover corrupt downloads, conflicting assets, source mismatch, duplicate runs, interrupted upload recovery and public/private tag boundaries. Publication itself still needs the separate Workbench build, attribution, signed-update and release checks.

The [`release: published` event](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#release) covers stable releases and prereleases. Releases created by another workflow using `GITHUB_TOKEN` do not normally trigger a second workflow; that publisher must explicitly dispatch this workflow or call the same helper in its publishing job. The manual dispatch also supports existing tags predating this workflow. See [workflow-trigger authentication](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-when-your-workflow-runs/triggering-a-workflow), [token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token) and the [GitHub CLI upload reference](https://cli.github.com/manual/gh_release_upload).

The checkout pin was verified against the official [actions/checkout v7.0.1 release](https://github.com/actions/checkout/releases/tag/v7.0.1): `3d3c42e5aac5ba805825da76410c181273ba90b1`.
