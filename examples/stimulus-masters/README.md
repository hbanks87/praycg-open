# Original eleven stimulus masters

The public installer offers the seven cleared film editions and the original Lantern Bridge. Four additional editions are preserved in the local eleven-film collection and have unresolved redistribution rights. The [catalog](catalog.json) records the filenames, hashes, source URLs and edition-specific rights for all eleven original masters.

## Download the public packs

| Public Workbench 11.13.1 companion | Verify the exact edition |
| --- | --- |
| [Seven original film masters](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.13.1/PRAYCG_OPTIONAL_MASTER_STIMULI_7_20261013.zip) | [Manifest](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.13.1/PRAYCG_OPTIONAL_MASTER_STIMULI_7_20261013.manifest.json) · [SHA-256](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.13.1/PRAYCG_OPTIONAL_MASTER_STIMULI_7_20261013.zip.sha256) |
| [Original Lantern Bridge installer pack](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.13.1/PRAYCG_ORIGINAL_LANTERN_INSTALLER_20261014.zip) | [Manifest](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.13.1/PRAYCG_ORIGINAL_LANTERN_INSTALLER_20261014.manifest.json) · [SHA-256](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.13.1/PRAYCG_ORIGINAL_LANTERN_INSTALLER_20261014.zip.sha256) |

The [optional installer](../../workbench/docs/releases/alpha-11.2.2/STIMULUS_INSTALLATION.md) uses the original pinned 11.2.2 URLs for these same bytes. The standardized masters use padded 1920×1080 video at 24 fps with H.264/yuv420p and 48 kHz AAC stereo. The [release companion procedure](../../docs/release-history/stimulus-companions.md) covers attaching the packs and their verification files.

## Prepared companions

| Companion | Contents | Current status |
| --- | --- | --- |
| `PRAYCG_Original_11_Stimulus_Masters_LOCAL_REVIEW_ONLY_2026-10-13.zip` | All 11 masters, 27 existing source/evidence files and two packaging documents | Complete local preservation; **not cleared for public redistribution** |
| `PRAYCG_OPTIONAL_MASTER_STIMULI_7_20261013.zip` | Seven exact masters plus attribution/edition notes and source catalog | Published with the [11.2.2 media release](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.2.2); used by the current optional installer |

The full eleven-film archive is **1,269,289,300 bytes**, SHA-256:

```text
89dd81232c4e9b0fe17a06985e599a31c434a0cf89f429a6850978357c884c0c
```

The seven-film archive is **691,949,836 bytes**, SHA-256:

```text
e851f0a6bea03ea381efe4c96c9a93685e6afdbfc9ecf05bdfd29741e6ca0a4b
```

Both companions were prepared outside the Git source tree. Archive inventories, CRCs and preserved file hashes were checked. This is packaging verification, not a fresh playback, installation, scientific-validation or participant-study check.

## Which eleven files?

All eleven master payloads were found and hash-checked against their existing candidate inventory and installed-copy sidecars. Their combined media size is **1,269,126,015 bytes**. The seven-film subset contains **691,935,302 bytes** of media.

| ID | Film | Original master filename | Bytes | Prepared subset |
| --- | --- | --- | ---: | --- |
| 01 | Coffee Run | `01_Coffee_Run_screening_1080p24.mp4` | 84,405,537 | Seven-film recorded-review package |
| 02 | Poached | `02_Poached_screening_1080p24.mp4` | 79,559,239 | Seven-film recorded-review package |
| 03 | Glass Half | `03_Glass_Half_screening_1080p24.mp4` | 59,609,612 | Seven-film recorded-review package |
| 04 | You Imagined | `04_You_Imagined_screening_1080p24.mp4` | 114,519,779 | Seven-film recorded-review package |
| 05 | Joy & Heron | `05_Joy_Heron_screening_1080p24.mp4` | 106,786,533 | Local review only |
| 06 | WING IT | `06_WING_IT_screening_1080p24.mp4` | 152,902,610 | Seven-film recorded-review package |
| 07 | HERO | `07_HERO_screening_1080p24.mp4` | 75,293,702 | Seven-film recorded-review package |
| 08 | Charge | `08_Charge_screening_1080p24.mp4` | 125,644,823 | Seven-film recorded-review package |
| 09 | The Little Match Seller | `09_The_Little_Match_Seller_screening_1080p24.mp4` | 101,031,970 | Local review only |
| 10 | An Interesting Story | `10_An_Interesting_Story_screening_1080p24.mp4` | 150,160,194 | Local review only |
| 11 | Le Voyage de Gulliver | `11_Le_Voyage_de_Gulliver_screening_1080p24.mp4` | 219,212,016 | Local review only |

The complete companion preserves those original filenames. The optional seven-film installer package uses `<stimulus_id>/master/stimulus_master.mp4` paths and retains the original filename in its edition catalog. The underlying media hashes are identical.

## Recorded rights and edition boundaries

The later Alpha 10.6.2 records identify Coffee Run, Poached, Glass Half, You Imagined, WING IT, HERO and Charge as the reviewed seven-film subset, with per-file source, license, attribution and redistribution-evidence fields. Those records are preserved historical provenance; this packaging did not obtain new permissions. The Commons-reviewed Poached and You Imagined entries retain that limitation.

The same later build record keeps **Joy & Heron** and the exact editions of **The Little Match Seller**, **An Interesting Story** and **Le Voyage de Gulliver** unresolved for redistribution. A source film's public-domain description does not settle the soundtrack or exact edition used here. The initial candidate inventory also differs from the later review for Glass Half; the prepared seven-film manifest follows the later **CC BY 3.0** record and preserves the earlier label in the catalog.

The full eleven-film archive therefore remains **LOCAL_REVIEW_ONLY_NOT_REDISTRIBUTION_CLEARED**. Its presence on the developer's machine is not a public download or a clearance for study deployment. No missing rightsholder or edition record has been replaced with an assumption.

## Historical inspection: Public Alpha 11.2.1

The 11.2.1 installer expected an operator-supplied URL and used an older manifest. Version 11.2.2 connected the reviewed pack to the installer. The [original inspection](https://github.com/hbanks87/praycg-open/blob/4d6bbc7a305566d9eac0f5b314edbbb1d547d2c5/examples/stimulus-masters/README.md#historical-inspection-public-alpha-1121) records both manifest identities and the manual procedure.

## Is the bridge video still present?

Yes. Use the original Lantern Bridge pack above for the installed master. The [Bridge demo collection](../bridge-demo/README.md) records the companion’s provenance and supporting material.

## Provenance of this catalog

The eleven master sidecars, candidate media manifest, validation reports and the Alpha 10.6.2 distribution record establish the edition identities and the seven/four split. Use the checksum associated with the exact named ZIP. [Examples](../README.md) · [Sintel recipe](../stimulus-recipes/sintel/README.md)
