# Installation and first launch

## Public Alpha 11.13.1

1. Finish recording and close Workbench. Download the [public ZIP](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.13.1/PRAYCG_Workbench_Public_Alpha_11_13_1.zip) and its [checksum](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.13.1/PRAYCG_Workbench_Public_Alpha_11_13_1.zip.sha256). On Windows, run `Get-FileHash .\PRAYCG_Workbench_Public_Alpha_11_13_1.zip -Algorithm SHA256` and compare the full digest with the checksum.
   Expected size: **47,010,179 bytes**. SHA-256: `be50bebd81e28df59674f127797260afb514c446bd2098ee48cdf5dd909b65af`.
2. Extract into a new writable folder. Keep your prior installation for rollback and keep study data outside the application folder.
3. Use native Windows Python 3.11 with Tcl/Tk. Run `INSTALL.bat`, then `START.bat`. Verify your selected workspace, recording destinations and external program paths.
4. For a first run, use `CREATE_SYNTHETIC_EXAMPLE.bat`. In Analysis Forge, select the generated run, complete the required checks and inspect Results.

**Updating an existing installation.** Settings → Updates discovers signed public releases. For a local import, place the [signed update file](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.13.1/PRAYCG_Workbench_Public_Alpha_11_13_1.zip.update.json) beside the matching ZIP. Preserve your current shared Zuna location.

**Optional stimuli.** `INSTALL_STIMULUS_PACKAGE.bat` uses the pinned sources for the seven-film pack and original Lantern Bridge. The [stimulus catalog](../../examples/stimulus-masters/README.md) gives the release downloads, editions and rights.

[Full release workflow](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.13.1/INSTALL_WORKFLOW.md) · [Hardware and recording](hardware-support.md) · [Troubleshooting](troubleshooting.md) · [Release history](../../docs/release-history/README.md)

## Earlier installation guides

- <a id="public-alpha-11130"></a>[Public Alpha 11.13.0](https://github.com/hbanks87/praycg-open/blob/4d6bbc7a305566d9eac0f5b314edbbb1d547d2c5/workbench/docs/installation.md#public-alpha-11130)
- <a id="preserved-public-alpha-11120-installation"></a>[Public Alpha 11.12.0](https://github.com/hbanks87/praycg-open/blob/4d6bbc7a305566d9eac0f5b314edbbb1d547d2c5/workbench/docs/installation.md#preserved-public-alpha-11120-installation)
- <a id="preserved-public-alpha-11101-installation"></a>[Public Alpha 11.10.1](https://github.com/hbanks87/praycg-open/blob/4d6bbc7a305566d9eac0f5b314edbbb1d547d2c5/workbench/docs/installation.md#preserved-public-alpha-11101-installation)
- <a id="preserved-public-alpha-1192-installation"></a>[Public Alpha 11.9.2](https://github.com/hbanks87/praycg-open/blob/4d6bbc7a305566d9eac0f5b314edbbb1d547d2c5/workbench/docs/installation.md#preserved-public-alpha-1192-installation)
- <a id="preserved-alpha-1054-installation"></a>[Alpha 10.5.4](https://github.com/hbanks87/praycg-open/blob/4d6bbc7a305566d9eac0f5b314edbbb1d547d2c5/workbench/docs/installation.md#preserved-alpha-1054-installation)
- <a id="before-you-begin"></a>[Before you begin](https://github.com/hbanks87/praycg-open/blob/4d6bbc7a305566d9eac0f5b314edbbb1d547d2c5/workbench/docs/installation.md#before-you-begin)
- <a id="install-the-components"></a>[Install the components](https://github.com/hbanks87/praycg-open/blob/4d6bbc7a305566d9eac0f5b314edbbb1d547d2c5/workbench/docs/installation.md#install-the-components)
- <a id="first-launch-and-upgrade"></a>[First launch and upgrade](https://github.com/hbanks87/praycg-open/blob/4d6bbc7a305566d9eac0f5b314edbbb1d547d2c5/workbench/docs/installation.md#first-launch-and-upgrade)
