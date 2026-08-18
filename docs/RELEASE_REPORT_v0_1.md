# PRAYCG public release v0.1 report

This release pack is designed for a GitHub repository plus an OSF project.

## Packages

- `praycg-open/`: GitHub-facing repository tree.
- `PRAYCG_Open_Science_Hub_OSF_v0_1/`: OSF-facing upload tree.

## Status

This is a public predata/open-method release. It is suitable for technical critique and repository setup. It is not a confirmatory scientific release.

## Contact example

The Contact pilot is included as a public-safe derived-output example. It is gold-plated for folder layout and interpretation demos, but not a gold record. It does not include copyrighted stimulus media or raw XDF.

## Demo media

The package includes `Demo Lantern Bridge`, a synthetic CC0 3-minute PRAYCG demo with target/override/control videos and QC outputs.

The package also includes a `Sintel` recipe. Sintel is an online open movie source under Creative Commons Attribution 3.0, but the generated Sintel excerpt itself is not bundled here. Run the recipe locally if you want a CC-BY open-movie stimulus excerpt.

## Upload scripts

- GitHub recursive uploader: `software/upload_tools/github_recursive_upload_pygithub.py`
- OSF recursive uploader: `software/upload_tools/osf_recursive_upload_osfclient.py`

## Recommended upload split

- GitHub: code, docs, templates, small demo assets.
- OSF: frozen software ZIPs, reports, public-safe derived examples, larger media/data, release snapshots.
