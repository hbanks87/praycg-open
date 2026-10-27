# Seven-film collection and original Lantern

Run `INSTALL_STIMULUS_PACKAGE.bat` from the extracted Workbench release to install the optional seven-film collection and the original Lantern demo. They remain two separate verified packages and provide eight master choices. Review the destination and storage summary, then confirm. The installer does not install software environments or alter recordings and settings.

The seven films are Coffee Run, Poached, Glass Half, You Imagined, Wing It!, Hero and Charge. Original editions, credits and rights are recorded in each package. Four other catalog editions are not part of this public download because their redistribution records require further review.

The installer uses pinned manifest URLs by default. To use separately downloaded companion archives without network access:

```bat
INSTALL_STIMULUS_PACKAGE.bat --archive-directory "D:\Downloads\PRAYCG stimuli"
```

This folder must contain `PRAYCG_OPTIONAL_MASTER_STIMULI_7_20261013.zip` and `PRAYCG_ORIGINAL_LANTERN_INSTALLER_20261014.zip`. Use `--package seven` or `--package lantern` for one package, `--destination` for a dedicated folder, and `--preflight-only` to check local readiness without installation. `--archive` or `--url` requires one selected package or one explicit reviewed manifest. Overrides do not bypass identity checks.

Exact verified installations are reusable. Changed or conflicting files are never overwritten. If a later package fails, rerun the installer to reuse earlier verified packages and retry the missing package. Partial downloads restart. The installer rejects unexpected files, unsafe paths, links, executables, nested archives and hash mismatches.

After installation, return to Prepare Materials, refresh installed masters and select the one to use. It still needs normal local playback checks, protocol-specific preparation, fingerprints and review. Installation is not collection approval.

Lantern's original master SHA-256 is `4b8a96892d840070176307c9ac169910993ebdaece8cf41ade774bafc97a141f`. It is unchanged. The installer-ready companion preserves the master and safe historical prepared media/records, with nested archives flattened during packaging. Original archival files remain separately preserved. Historical anchors, cues and QC are examples, not newly qualified materials. No media was re-encoded.

If a release URL is unavailable, do not substitute a similarly named archive. Use the exact matching companion from the public release when available. A published URL, license record or hash does not establish experimental validity, participant suitability or permission to share a study.
