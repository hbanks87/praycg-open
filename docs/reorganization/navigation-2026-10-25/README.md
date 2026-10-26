# Navigation update — 25 October 2026

This update gives the repository five clear entry paths: using the Workbench, understanding the research, inspecting or reproducing evidence, finding hardware and stimuli, and locating sources and history. Current guides state the applicable software version; original research and historical records retain their own identities.

## Preservation

The baseline is commit `45ec802b730c01b6cc8227a469656949158d0791`, containing 1,658 tracked files. The update replaces 13 navigation or maintained-guide files and adds four guides. All other **1,645 baseline files** retain their original paths and exact Git blob identities. No original scientific document, core specification, code file, release snapshot, binary or reproducibility package is removed or modified.

The exact previous bytes of all 13 edited pages are in [PREVIOUS_NAVIGATION.zip](PREVIOUS_NAVIGATION.zip), with their repository-relative paths intact. [PRESERVATION_MANIFEST.json](PRESERVATION_MANIFEST.json) records their hashes, the archive checksum and every baseline file identity. These preservation records are separate from the earlier [migration ledger](../FILE_MIGRATION_LEDGER.json), which remains unchanged.

The [original-file locator](../original-file-index.md) now resolves 16 relocated Cerelog paths and 15 historical Offline Master Interpreter entries. Those 15 entries link to the immutable original commit because the files were already absent from the current tree before this update. Their original identities were checked against the migration ledger, accounting for Windows checkout line endings for text files.

## Link checks and historical references

All Markdown documents in the public tree were scanned for repository paths and heading fragments, with the new navigation applied. External HTTP links were checked separately. The scope excludes links embedded inside PDF, Word, ZIP and other binary files; external page fragments and the meaning of a linked page are not certified by an HTTP response.

[Link audit](LINK_AUDIT.json) records the results and unresolved references. [Historical link recovery guide](HISTORICAL_LINKS.md) groups old references by source and provides available recovery routes. Current navigation is checked separately from frozen original documents: preserved snapshots can refer to files that exist only inside their complete software package or to a former repository layout.

This is a documentation organization update. Public Workbench **11.9.2**, its release assets and existing tags remain unchanged. The detailed algorithm inspection still identifies **11.2.1**; this update does not relabel that inspection as a later audit.

[Repository home](../../../README.md) · [Sources and history](../../README.md) · [Current Workbench guide](../../../workbench/README.md)
