# Demo Lantern Bridge — preserved stimulus companion

**Public Alpha 11.2.2 installer companion:** [installation and integrity guide](../../workbench/docs/releases/alpha-11.2.2/STIMULUS_INSTALLATION.md). The new installer-ready ZIP supplies the unchanged original master and safe flattened historical companions. Its SHA-256 is `52ce56874fac1e4320822e8d71e3668836e6744a434c9e96508466081ea84280`; size 106,117,274 bytes. It is distinct from the immutable archival ZIP described below. The installer pack is published on the [11.2.2 source release](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.2.2) and is now attached unchanged to [11.9.2](https://github.com/hbanks87/praycg-open/releases/download/PRAYCG_Workbench_Public_A11.9.2/PRAYCG_ORIGINAL_LANTERN_INSTALLER_20261014.zip), with its matching manifest and checksum in Assets. The [release companion workflow](../../docs/release-history/stimulus-companions.md) carries this installer pack with future public releases.

The original **Demo Lantern Bridge** remains in this repository. It is a synthetic three-minute CC0 demonstration with prepared target, analytic-override, phase-scrambled and shot-order control materials. It is separate from the eleven-film stimulus collection.

[Examples and stimuli](../README.md) · [Preserved original README](../synthetic-demo/README_Lantern.md) · [Stimulus masters](../stimulus-masters/README.md) · [Workbench update proposal](../../workbench/docs/proposed-alpha-11.2.1.md)

## Find the video and its companions

| Material | Original file or collection |
| --- | --- |
| Clean bridge master | [Master MP4](../synthetic-demo/.mp4s/stimulus_master_cleaned_stimulus_master_Demo_Lantern_Bridge_CC0_v1_7A.mp4) |
| Cued target | [Target MP4](../synthetic-demo/.mp4s/stimulus_target_cued_stimulus_master_Demo_Lantern_Bridge_CC0_v1_7A.mp4) |
| Cued analytic override | [Override MP4](../synthetic-demo/.mp4s/stimulus_override_cued_stimulus_master_Demo_Lantern_Bridge_CC0_v1_7A.mp4) |
| Shot-order structural control | [Structural-control MP4](../synthetic-demo/.mp4s/stimulus_structural_control_clean_shot_order_scrambled_lantern_shot_scramble_v1_9.mp4) |
| Phase-scrambled control | [Original control ZIP](../synthetic-demo/.mp4s/stimulus_control_cued_phase_scrambled_Lantern_shotcramble_v1_7A.zip); extract its contents before media selection |
| Cues, draft anchors, preparation manifest and QC checklists | [MediaPrep outputs](../synthetic-demo/Mediaprep_Outputs/) |
| Structural-control construction and QC | [Shot-order records](../synthetic-demo/Shotscramble_QC/) |
| Fingerprint/QC report | [Original report archive](../synthetic-demo/Fingerprint_Stimulus_QC_report.zip) |
| Original media license | [CC0 notice](../synthetic-demo/Mediaprep_Outputs/CC0_DEMO_LICENSE.txt) |

The `.mp4s` directory can be hidden on systems that hide dot-prefixed folders. Keep the supporting files with the media. These records retain their original versions and include draft anchors; they are not newly qualified stimulus materials for every current protocol.

## Historical preservation archive (separate from the public installer pack)

The earlier local preservation archive below is distinct from the published installer pack linked above:

```text
PRAYCG_Demo_Lantern_Bridge_Preserved_CC0_2026-10-13.zip
```

Size: **106,074,791 bytes**. SHA-256:

```text
3344980589bf3fae282d0a5049f882e3b479f62a5c9c7eb4c4efb446ee1e640d
```

The package preserves all **23 original files** from `examples/synthetic-demo` at commit `bc17059f10d0756f811c4ec900be8d4a476f191f`, plus three packaging files: `START_HERE.md`, `PACKAGE_MANIFEST.json` and `SOURCE_REPOSITORY_LICENSE.md`. The [package manifest](PACKAGE_MANIFEST.json) records each original file's SHA-256. Originals are taken from canonical Git blobs to avoid checkout line-ending conversion. Archive integrity and all 23 original-file hashes were checked after packaging.

The companion is prepared locally and has no published release-asset URL yet. The original repository links above are available independently. The proposed Public Alpha 11.2.1 application ZIP does not contain this original bridge collection; it contains separate small demonstration catalogs. Current users should use the published installer pack linked at the top of this page; this older archival identity remains available for provenance.

No media was regenerated or re-encoded. No new stimulus QC, application compatibility test, participant run or scientific validation is claimed by packaging. Select or import the appropriate materials through the Workbench's normal media workflow, then check the chosen protocol's requirements. Preserve historical stimulus identities when preparing a new version.

[Repository license](../../LICENSE.md) · [Citations and attribution](../../CITATIONS_AND_ATTRIBUTION.md) · [Reproducibility programs](../../research/reproducibility/README.md)
