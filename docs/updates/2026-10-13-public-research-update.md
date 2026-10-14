# Suggested praycg-open update — 13 October 2026

**Prepared for review. No release or repository push is performed by this update.**

The suggested update pairs the newer **Public Alpha 11.2.1 Workbench** with a visible research entrance for **Opto-PING, the documented ladders/rungs and reproducibility programs**. The scientific originals already retained in the repository remain unchanged; new indexes make them accessible from the repository home.

## Suggested title and description

**Public Alpha 11.2.1 preparation and restored research navigation**

Prepare the cumulative Workbench update with the independent PRAYCG AI Assistant, guided analysis and report history, signal-quality and cleaning review, and scoped Athena reporting. Restore prominent access to Opto-PING, documented research ladders, locked synthetic reproduction packages and exploratory reanalysis programs. Preserve original research files and distinguish available artifacts, historical descriptions and planned validation.

## Review the prepared changes

| Area | Prepared material |
| --- | --- |
| Workbench additions | [Cumulative proposed changelog since 10.5.4](../../workbench/docs/proposed-alpha-11.2.1.md) |
| Current package source and evidence | [Seven verbatim documents/receipts and their source manifest](../../workbench/docs/releases/alpha-11.2.1/README.md) |
| Opto-PING | [Research overview and links to retained rung bundles](../../research/optoping/README.md) |
| Ladders and rungs | [Source-based stage index and artifact availability](../../research/ladders/README.md) |
| Reproducibility | [Programs, scripts, specifications, reference outputs and run constraints](../../research/reproducibility/README.md) |
| Attribution and bibliography | [Updated master record](../../CITATIONS_AND_ATTRIBUTION.md), [method bibliography](../../research/bibliography/README.md) and [exact retained notices](../attribution/alpha-11.2.1/README.md) |
| Detailed concepts | [Research questions, definitions, equations and interpretation](../../research/concepts/README.md) |
| Algorithm implementation | [Inputs, computation, outputs, versions and code locations](../../research/algorithms/README.md) |
| Original stimulus masters | [Eleven-master catalog and optional-package status](../../examples/stimulus-masters/README.md) |
| Bridge demonstration | [Original videos, companions and prepared CC0 archive](../../examples/bridge-demo/README.md) |
| Reader entry points | [Repository home](../../README.md), [research entrance](../../research/README.md), [studies](../../research/studies/README.md), [research roadmap](../../research/roadmap.md) and [Workbench](../../workbench/README.md) |

The research and protocol entrances now point to the general Workbench workflow instead of pinning readers to the old Alpha 10.2.1 guide. Original versioned guides remain available.

## Research coverage and gaps

**Opto-PING is restored to the main navigation.** The retained public archive contains 126 files across Rungs 0J–0O: 22 for J, 27 for K, 15 for L, 18 for M, 23 for N and 21 for O. The indexes link the expanded research tree and the original downloadable archive; no duplicate scientific payload is needed.

The rung sequence covers preregistered synthetic lock-in, an external reproduction handoff, empty-sky specificity, null-aware model selection, K-null calibration repair and locked null-aware reproduction. Links connect each stage to its own specifications, scripts, reports and outputs. The handoff includes Windows/Unix launchers, a verification script and an external reproducer reporting template.

The preserved 16-point handout also describes **0A–0I** in groups. Those stages are included as documented history. Their standalone source packages were not located in the retained public tree or the archived Opto-PING ZIP. This update cannot restore bytes that are not present; it records that gap instead of creating substitute experiments. The ladder index also links the source-defined broader research stages and keeps future stages separate from completed synthetic work.

The reproducibility catalog distinguishes runnable synthetic work from exploratory reanalysis and proposed participant studies. In particular, the preserved **NUPI Arrival/Contact/Field scripts** depend on a historical input layout and hard-coded `/mnt/data/` paths. They are retained programs with prerequisites, not a newly verified portable raw-data reproduction. The public Contact pilot excludes raw XDF and copyrighted stimulus media.

The source handout's multi-machine reproduction statement and the Rung K internal clean-room record retain their own wording and scope. This documentation update establishes neither an independently audited third-party replication nor a biological mechanism.

A separate local visual-narrative HMM audit candidate was found outside `praycg-open`. Its proposed GitHub repository was not publicly retrievable during this review. It is not linked as an available public program or copied into this update; publication status and its own source/redistribution record need to be resolved before adding it to the public catalog. Private AUL studies and participant materials are outside this public update.

## Release status and recommended next publication

### Stimulus companions and algorithm documentation

The original eleven screening masters were located and their stored checksums verified. Their combined media size is **1,269,126,015 bytes**. They belong in a separate optional stimulus distribution. The existing release records support a seven-film public subset; four entries remain marked for local review because source-edition or redistribution records are unresolved. The [stimulus catalog](../../examples/stimulus-masters/README.md) identifies the exact films, records and availability. A complete local eleven-master package is not automatically a public release asset.

The unchanged Public Alpha 11.2.1 installer bundles an **older seven-film manifest** and still prompts for an HTTPS URL unless `--url` is supplied. It does not use a manifest's `release_url` value automatically. Connecting the newly prepared public companion requires publishing that asset, replacing the bundled default with its matching manifest in a reviewed application revision, and wiring the real URL into the installer/launcher. Supplying only a new URL with the old manifest fails integrity verification. This connection remains release work; preparing the media ZIPs did not implement it.

The original **Demo Lantern Bridge** is preserved in the repository and now has a [dedicated entry page](../../examples/bridge-demo/README.md). A separate CC0 companion archive preserves all 23 original files, including prepared video variants, cues, draft anchors and QC evidence. It was built from canonical Git blobs and verified without re-encoding. This is distinct from the small demonstration catalogs already inside the Public Alpha 11.2.1 application ZIP.

The new [concept explanations](../../research/concepts/README.md) and [algorithm guide](../../research/algorithms/README.md) make the research more inspectable: each identifies the question, input requirements, calculation, output, interpretation and relevant source version. Historical formulas and current runtime implementations are identified separately. These sections explain project-specific methods without claiming that every component is novel, validated or implemented in every release.

### Workbench publication status

As checked on 13 October 2026, [Alpha 10.5.4](https://github.com/hbanks87/praycg-open/releases/tag/PRAYCG_Workbench_A10.5.4) remains the published latest GitHub release. The newer inspected local distribution is `PRAYCG_Workbench_Public_Alpha_11_2_1.zip`, **43,737,009 bytes**, with SHA-256:

```text
cb65ec3180a59a9181e4fecd9bb94a2b136ab158f0f275eaf49b01dc3386c42b
```

Its checksum matches the supplied sidecar. The [source manifest](../../workbench/docs/releases/alpha-11.2.1/SOURCE_MANIFEST.json) records each mirrored document's exact archive path, size and hash. Its recorded result is **535 unique targeted checks passed**, with zero final failures, errors or skips. These are supplied build receipts, not tests executed for this repository documentation update. No new installation, live acquisition, provider request, Zuna inference or independent replication is claimed.

The intended publication is a clearly labeled public alpha prerelease with the cumulative changelog linked above. The attribution review subsequently reproduced a [protocol-ratings credit-record defect](../attribution/alpha-11.2.1/proposed-fixes/README.md) that prevents that managed worker from starting. Apply and verify the proposed metadata fix before publishing an application update, then issue a newly identified package, checksum and corresponding evidence. The unchanged inspected archive is the review baseline. At publication, update the published installation/workflow/hardware entry pages together and replace the current-release link only after the new release exists. Preserve the 10.5.4 guide collection and its original validation scope.

The research navigation can be reviewed independently of that software release. Restoring its visibility does not change the scientific status of any study or promote a proposed rung to a completed result.

## Verification scope

Review this change as navigation, proposed release notes and a selected public-document snapshot. Relative links in changed/new Markdown are checked against the local checkout and full tracked Git tree. Mirrored documents are checked against their package bytes and source hashes. The change leaves preserved scientific originals, scripts and data unchanged; it does not rerun the research programs or modify the application archive.

The expanded [attribution review](../attribution/alpha-11.2.1/README.md) adds primary-source bibliography checks, ten exact package records, five separately observed upstream notices and a bounded observer-schema regression probe. Its proposed fix is separate from the immutable package evidence.

The [verification record](2026-10-13-verification.json) records these checks. All 126 archived Opto-PING payloads match their canonical Git blobs. Windows checkout line-ending conversion can change working-copy hashes; the Opto-PING guide therefore recommends the preserved ZIP or a checkout that preserves blob bytes for checksum verification.

[Original-file locator](../reorganization/original-file-index.md) · [Preservation record](../reorganization/README.md) · [Citations and attribution](../../CITATIONS_AND_ATTRIBUTION.md)
