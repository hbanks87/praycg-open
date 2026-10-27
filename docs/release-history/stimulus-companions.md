# Carry the public stimuli with each Workbench release

The public release workflow is installed and its [first verified run](https://github.com/hbanks87/praycg-open/actions/runs/40434259585) attached all six companions to [Public Alpha 11.9.2](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.9.2). The existing application assets and tag retain their identities. Review the [workflow](../../.github/workflows/public-release-stimuli.yml), [helper](../../scripts/attach_public_stimuli.py) and [offline tests](../../scripts/tests/test_attach_public_stimuli.py).

On each published `PRAYCG_Workbench_Public_A<major>.<minor>.<patch>` release, the workflow copies the two existing public packs and their matching manifest/checksum companions from Public Alpha 11.2.2. The fixed six-file allowlist contains the reviewed seven-film archive and original Lantern installer archive. The full eleven-master collection remains outside this distribution. The archives are copied without re-encoding or changing their rights records.

The helper validates the repository, published release, asset names, byte counts and SHA-256 values. It checks every existing target asset and downloads/verifies every missing source before uploading anything. Identical assets are skipped. Conflicts stop the run; existing assets are never deleted or replaced. An upload interrupted after validation can leave a partial set; rerunning resumes missing files and skips complete identical assets. If GitHub retains an incomplete named asset, the helper stops for operator review rather than deleting or replacing it automatically.

The workflow uses the maintained helper from `main`, a full-commit pin for `actions/checkout` v7.0.1, and `contents: write` only for the attachment job. The token is passed to GitHub CLI and is not persisted by checkout. Inputs pass through an environment variable and are validated before CLI calls.

## Existing release or recovery

To fill a later existing release or retry a stopped run, open **Actions → Attach verified public stimuli → Run workflow** with that release's exact public tag. The initial 11.9.2 attachment has already completed. This does not create or move a tag or change the Workbench ZIP/signature.

For a local operator with Python 3.11+ and authenticated GitHub CLI:

```sh
python scripts/attach_public_stimuli.py --tag PRAYCG_Workbench_Public_A11.9.2
python scripts/attach_public_stimuli.py --tag PRAYCG_Workbench_Public_A11.9.2 --apply
```

The first command downloads and verifies missing assets without uploading. The second performs the authorized attachment. The initial transfer is approximately 798 MB. Existing assets with GitHub SHA-256 metadata need no repeat download; older assets without that digest are verified from their bytes.

The installed 11.9.2 manifest remains pinned to the original 11.2.2 URLs, which continue to work. These added attachments provide the same bytes on every later release. The matching companion manifests intentionally preserve their original pinned URLs; this helper does not rewrite historical package identities. A future installer can use its explicitly supported `--archive-directory` or `--url` options with these identical assets.

## Verification and future publishing

```sh
python -m unittest discover -s scripts/tests -p 'test_attach_public_stimuli.py' -v
```

The offline tests cover corrupt downloads, conflicting assets, source mismatch, duplicate runs, interrupted upload recovery and public/private tag boundaries. Publication itself still needs the separate Workbench build, attribution, signed-update and release checks.

The [`release: published` event](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#release) covers stable releases and prereleases. Releases created by another workflow using `GITHUB_TOKEN` do not normally trigger a second workflow; that publisher must explicitly dispatch this workflow or call the same helper in its publishing job. The manual dispatch also supports existing tags predating this workflow. See [workflow-trigger authentication](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-when-your-workflow-runs/triggering-a-workflow), [token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token) and the [GitHub CLI upload reference](https://cli.github.com/manual/gh_release_upload).

The checkout pin was verified against the official [actions/checkout v7.0.1 release](https://github.com/actions/checkout/releases/tag/v7.0.1): `3d3c42e5aac5ba805825da76410c181273ba90b1`.
