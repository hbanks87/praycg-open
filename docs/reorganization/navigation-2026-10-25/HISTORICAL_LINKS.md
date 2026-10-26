# Historical link recovery

The navigation update keeps original documents and packaged release snapshots intact. Some relative links in those documents were already broken before this update because companion files were moved or only part of an application package was mirrored into GitHub. They remain recorded rather than silently rewritten.

The complete audit scans 467 Markdown documents and 4,466 links, including repository paths and heading anchors. It records **0 broken links in edited navigation**, **0 newly introduced broken links**, and **311 remaining historical missing-path references**. These historical links still do not resolve in place. [The machine-readable report](LINK_AUDIT.json) lists every source, line, target and available recovery route.

| Preserved source group | Missing references | Where to recover context |
| --- | ---: | --- |
| Alpha 11.4.1 third-party notice snapshots | 229 | [Root notice collection](https://github.com/hbanks87/praycg-open/tree/main/THIRD_PARTY_NOTICES) contains matching paths for some dependencies; use the application ZIP attached to [Alpha 11.4.1](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.4.1) for the versioned package context. |
| Alpha 11.2.2 / 11.4.1 attribution snapshots | 21 | [Maintained citations](https://github.com/hbanks87/praycg-open/blob/main/CITATIONS_AND_ATTRIBUTION.md), [attribution records](https://github.com/hbanks87/praycg-open/tree/main/docs/attribution), and the application ZIP for [Alpha 11.2.2](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.2.2) or [Alpha 11.4.1](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.4.1). |
| Original root README and citations snapshots | 13 | [Original installation/workflow guides](https://github.com/hbanks87/praycg-open/tree/main/workbench/docs/releases/alpha-10.2.1), [root notices](https://github.com/hbanks87/praycg-open/tree/main/THIRD_PARTY_NOTICES), and [maintained citations](https://github.com/hbanks87/praycg-open/blob/main/CITATIONS_AND_ATTRIBUTION.md). |
| Alpha 11.x packaged guides | 29 | Open the matching application ZIP in [Alpha 11.4.1](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.4.1), [Alpha 11.6.0](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.6.0) or [Alpha 11.9.2](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_Public_A11.9.2); the report supplies the package-relative lookup path. These links refer to application tools that were not mirrored beside the guide. |
| Older release installation and attribution guides | 19 | [Release history](https://github.com/hbanks87/praycg-open/blob/main/docs/release-history/README.md) and [preserved release guides](https://github.com/hbanks87/praycg-open/tree/main/workbench/docs/releases). Exact replacement paths are listed where found; several older sibling files have no confirmed standalone replacement. |

267 unresolved references have at least one existing repository-path recovery candidate. Candidates from another location or version are navigation aids; this audit does not assert that their bytes match the historical copy. Package lookup routes do not certify that each requested member exists inside every ZIP.

The original-file locator was also checked: 16 Cerelog files moved into the four-channel hardware folder; 15 Offline Master Interpreter files remain available at their original immutable Git commit. Those locator links are repaired separately, while the original migration ledger stays unchanged.

External checks reached 255 of 270 unique URLs. 15 could not be certified because servers rejected automated access or TLS verification failed. No external URL returned a confirmed 404 or 410 in this run. The JSON report lists each unverified URL. HTTP reachability does not certify external fragments, page contents or scientific claims.

This check covers Markdown links, images and HTML `href`/`src` references outside code. It does not parse links embedded inside PDFs, Word documents, binaries, ZIP archives or executable source files.
