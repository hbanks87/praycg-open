# Historical link repairs — 26 October 2026

This update repairs the repository's remaining internal Markdown references while preserving its original scientific documents, core specifications and versioned release evidence. It also refreshes maintained attribution guidance and makes the public stimulus packs available with the current release.

## What was recovered

The previous audit found **311 broken references to 298 missing paths**. The recovery adds **320 exact public files** and **12 clearly labelled locator pages**. The total includes 34 supporting files needed by links inside restored documents. All 229 missing license-notice targets are restored with their verified bytes. The remaining restored files include historical instructions, selected code/configuration companions and original attribution evidence.

The [restoration plan](../../../tools/repository_maintenance/RESTORATION_PLAN.json) identifies seven public ZIPs and ten files from immutable public commits, with source hashes, member names and destination hashes. The 11.6.0 source is the published Revision 1 archive; the recovered members were checked against the unrevised archive and match. One pytest notice omitted from the 11.4.1 ZIP was recovered from the public notice collection and matches that release's original notice-index hash.

Locator pages are new navigation at formerly missing paths. They identify themselves and point to the appropriate preserved source, complete release or index. This avoids copying unrelated documentation and entire notice trees simply to repair an index backlink. They do not replace an existing original or masquerade as its text.

## Preservation

The baseline is commit `88c535f52958c908e1b8b14e46b7398451b22129`, containing 1,667 files. **1,661 retain their exact paths and bytes.** Only six maintained guides change: the master attribution, research bibliography, stimulus-master and bridge indexes, source-library index and development guide. Their exact previous bytes are preserved in [PREVIOUS_GUIDES.zip](PREVIOUS_GUIDES.zip); [PRESERVATION.json](PRESERVATION.json) records their Git blob identities and SHA-256 values.

All existing original scientific papers, core specifications, license notices, versioned package snapshots, research programs and historical audits remain unchanged. The [25 October audit](../navigation-2026-10-25/README.md) remains the historical before-repair record. The additive [restoration helper](../../../tools/repository_maintenance/README.md) refuses any overwrite of differing existing content.

## Link checks

[LINK_AUDIT.json](LINK_AUDIT.json) records the final Markdown scan, repaired baseline references and any external reachability limitations. The check covers Markdown links, images, HTML references and repository heading anchors outside code. It does not parse links embedded inside PDFs, Word files, ZIP contents or executable source.

The earlier publisher HTTP 403 responses are not evidence that the cited DOIs are invalid. A separate [reference review](EXTERNAL_REFERENCE_REVIEW.json) verifies all 13 affected DOI identities through official Crossref metadata. The NITRC Naturalistic Viewing page was independently retrieved with the web reader, although the command-line checker encountered a TLS hostname problem. Publisher access restrictions and this network difference remain recorded rather than silently changing valid historical references.

## Attribution and stimulus distribution

The [current attribution guide](../../attribution/README.md) and [bibliography](../../../research/bibliography/README.md) identify the reviewed 11.9.2 scope, retained NeuroKit2/EEGLAB/optical references and the explicitly pending method-level protocol-evidence attribution review. These documentation updates do not claim a new algorithm or full scientific validation.

[Public Alpha 11.9.2](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.9.2) now includes the existing seven-film and original Lantern packs, each with its matching manifest and checksum. The six added assets match their 11.2.2 sources; all 17 original release assets and the application tag are unchanged. The [release companion workflow](../../release-history/stimulus-companions.md) repeats attachment for future published public releases. The eleven-film local-review archive remains excluded because four editions have unresolved redistribution records.

[Repository home](../../../README.md) · [Sources and history](../../README.md) · [Attribution guide](../../attribution/README.md)
