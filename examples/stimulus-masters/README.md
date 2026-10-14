# Original eleven stimulus masters

**Public Alpha 11.2.2:** the [optional installer](../../workbench/docs/releases/alpha-11.2.2/STIMULUS_INSTALLATION.md) connects the exact seven-film archive to a separate original Lantern companion. The default offers eight master choices across two verified packages. This does not expand redistribution permission for the four excluded editions. Final remote publication verification is recorded with the [combined release update](../../docs/updates/2026-10-14-public-workflow-release.md).

The original eleven-film screening-master set is available locally and has been preserved in a complete **local-review companion archive**. A separate seven-film companion preserves the subset with recorded redistribution review. Neither archive has been uploaded by this update, and neither is inside the Public Alpha 11.2.1 application ZIP.

These are the existing standardized screening masters: 1920×1080 padded, 24 fps CFR, H.264/yuv420p and AAC 48 kHz stereo. They are distinct from the upstream source encodes, the Workbench's procedural demonstrations and the separate Lantern Bridge demo. Packaging preserves their bytes; it does not re-encode or retroactively repair them.

The [metadata catalog](catalog.json) records all eleven original filenames, sizes, full SHA-256 hashes, source URLs, recorded rights statements and companion identities. It contains no film payloads or personal filesystem paths.

## Prepared companions

| Companion | Contents | Current status |
| --- | --- | --- |
| `PRAYCG_Original_11_Stimulus_Masters_LOCAL_REVIEW_ONLY_2026-10-13.zip` | All 11 masters, 27 existing source/evidence files and two packaging documents | Complete local preservation; **not cleared for public redistribution** |
| `PRAYCG_OPTIONAL_MASTER_STIMULI_7_20261013.zip` | Seven exact masters plus attribution/edition notes and source catalog | Recorded redistribution-review subset; separate installer manifest prepared; no published URL |

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

## What is in Public Alpha 11.2.1?

The inspected application archive, SHA-256 `cb65ec3180a59a9181e4fecd9bb94a2b136ab158f0f275eaf49b01dc3386c42b`, contains **eight MP4 files and ten WAV files**, all under `app/examples/no_copyright_media_demo/`. Its four catalog packs are marked **DEMO_ONLY** and **CC0-1.0**. These procedural examples are not the eleven films above.

`INSTALL_STIMULUS_PACKAGE.bat`, its installer and a default `config/optional_stimulus_release_v1.json` are included. That default identifies the older `PRAYCG_OPTIONAL_MASTER_STIMULI_7_V1` archive: 691,953,162 bytes, SHA-256 `b35de8ace6ea5c241158119f3aa261c50cfb46827dd0eafb23f58f3c4effb6d8`, with `release_url: null`. It does not identify the newly prepared archive above. The film ZIP itself is not embedded, and the main installer does not install the optional films automatically.

The prepared seven-film companion has a separate `PRAYCG_OPTIONAL_MASTER_STIMULI_7_20261013.manifest.json`. Its new package ID prevents replacement of an existing package folder. The current public installer's exact manifest validator accepts it; its file inventory and every payload hash were checked. Its `release_url` remains `null` until a real HTTPS release asset exists.

The current installer's `main()` reads a supplied `--manifest` or the older bundled default. It then uses `--url` or asks the operator for an HTTPS ZIP URL; it does **not** read the manifest's `release_url` field. Using the newly prepared pack therefore requires both its new manifest and its eventual real URL. Supplying only the new URL while retaining the old default manifest would fail archive size/hash verification.

For an automatically connected release, publish the reviewed seven-film asset, bundle its matching manifest, and update the installer or launcher to use its published URL while retaining explicit overrides and integrity checks. Setting `release_url` alone is insufficient with the current code. No URL, installer change or application repack has been made by this documentation update.

The local-review eleven-film archive is intentionally not an installer-approved redistribution package. Its status should not be changed merely to make the optional installer accept it. After any permitted preparation or installation, importing a master into Prepare Materials still requires normal media and protocol review; installation does not create acquisition or scientific authority.

## Is the bridge video still present?

Yes. The repository retains [Demo Lantern Bridge](../synthetic-demo/README_Lantern.md), including the [cleaned master](../synthetic-demo/.mp4s/stimulus_master_cleaned_stimulus_master_Demo_Lantern_Bridge_CC0_v1_7A.mp4), target/override versions, controls, schedules and QC material. Its source notice states **CC0 1.0 Universal**.

It is separate from both film companions and is **not inside the Public Alpha 11.2.1 application ZIP**. A preserved companion is also prepared; see the [Bridge demo collection](../bridge-demo/README.md) for its exact package identity and files. No existing bridge media was replaced by the procedural examples in the application.

## Provenance of this catalog

This metadata review used the existing `candidate_screening_11/candidate_media_manifest.json`, eleven master sidecars and basic-validation reports, and the later Alpha 10.6.2 optional release manifest and build record. The candidate inventory describes the standardized source masters; the later record supplies the seven/four distribution distinction. Historical seven- and eleven-film archive hashes remain historical and are not substituted for the newly prepared companions' hashes above.

For the software proposal and its separate limits, read the [Public Alpha 11.2.1 update](../../workbench/docs/proposed-alpha-11.2.1.md). For other materials, use [Examples](../README.md), [Bridge demo](../bridge-demo/README.md) and [Sintel recipe](../stimulus-recipes/sintel/README.md).
