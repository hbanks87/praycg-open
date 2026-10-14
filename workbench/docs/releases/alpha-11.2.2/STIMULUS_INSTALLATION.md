# Optional seven-film collection and original Lantern

The Workbench stays a small application download. Movies are optional separate release assets. The default installer selection is **seven films plus the original Lantern demo**, installed as two independently verified packages. This supplies eight master choices, not seven movies with a replacement Lantern.

The seven films are Coffee Run, Poached, Glass Half, You Imagined, Wing It!, Hero and Charge. Their exact editions, original credits and license records are preserved in the [eleven-master catalog](../../../../examples/stimulus-masters/README.md). Four other catalog editions remain outside the public installer because their redistribution records require further review.

## Simple installation

1. Extract the complete Public Alpha 11.2.2 application ZIP. Run the ordinary installation first if Python 3.11 is not available.
2. Run **INSTALL_STIMULUS_PACKAGE.bat**. Review the selected package names, destination, storage requirements and sources, then confirm. No movie download begins just by opening the Workbench.
3. Return to **Prepare Materials**. Refresh the installed masters and select the movie to use. The selected master enters normal local playback checking, protocol-specific preparation and fingerprinting.
4. Review the resulting materials and their requirements before locking the study. Installing a master does not qualify its historical derivatives for a new protocol or declare its anchors approved.

The installer uses each bundled manifest's pinned release URL by default. If publication is incomplete or the network is unavailable, it reports that problem rather than accepting a different archive. Download the exact companion ZIPs separately and use a local folder as below.

## Local files and advanced choices

From the extracted release directory:

```bat
INSTALL_STIMULUS_PACKAGE.bat --archive-directory "D:\Downloads\PRAYCG stimuli"
INSTALL_STIMULUS_PACKAGE.bat --package lantern
INSTALL_STIMULUS_PACKAGE.bat --package seven --preflight-only
```

The local folder must contain these exact filenames:

| Package | ZIP | Size | SHA-256 |
| --- | --- | ---: | --- |
| Seven films | `PRAYCG_OPTIONAL_MASTER_STIMULI_7_20261013.zip` | 691,949,836 bytes | `e851f0a6bea03ea381efe4c96c9a93685e6afdbfc9ecf05bdfd29741e6ca0a4b` |
| Original Lantern | `PRAYCG_ORIGINAL_LANTERN_INSTALLER_20261014.zip` | 106,117,274 bytes | `52ce56874fac1e4320822e8d71e3668836e6744a434c9e96508466081ea84280` |

`--destination` selects a dedicated optional-media folder. `--archive` selects one ZIP and therefore requires one package or an explicit reviewed `--manifest`. `--url` also applies to one selected package; an override cannot bypass its archive and per-file hashes. `--preflight-only` checks local readiness without installing or testing network availability. `--yes` accepts the displayed operation for deliberate unattended use.

Downloads total approximately 798 MB. The installer checks available storage for downloads and expanded files. It rejects unreviewed manifests, unexpected files, path traversal, linked entries, executables, nested archives and hash changes. An exact verified installation is reusable. Changed or conflicting folders are never overwritten. If a later package fails, earlier verified packages remain available, and rerunning safely resumes at the package level; an incomplete download itself is restarted.

## What is preserved

Lantern's master SHA-256 remains `4b8a96892d840070176307c9ac169910993ebdaece8cf41ade774bafc97a141f`. The installer-ready companion preserves its master, prepared variants and safe historical records without re-encoding. Its original archival ZIP remains separately preserved. Nested historical archives are flattened during packaging; the installed package does not contain executable code or nested ZIPs. Source mappings explain the layout and omitted empty log. Historical paths inside original records remain historical.

The seven-film and Lantern packages each carry their own rights, source and integrity records. Installing them changes neither recordings, study settings, previous results nor Python/Zuna environments. No installer grants consent, publication authority, scientific validity or current protocol approval.

[Lantern history](../../../../examples/bridge-demo/README.md) · [Film editions and sources](../../../../examples/stimulus-masters/README.md) · [Citations](../../../../CITATIONS_AND_ATTRIBUTION.md)
