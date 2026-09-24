# Repository reorganization record

This replacement tree separates PRAYCG Workbench, the Neuro Research Program, hardware projects, reusable examples and historical software.

## Preservation

Every tracked file in the reviewed source checkout has a byte-identical destination in this tree. Duplicate files remain distinct occurrences. Theory documents, PDFs, archives, firmware, raw source and original notices were not resaved or reformatted.

The root README, contribution guide and master attribution navigation have revised public-facing copies. The Git ignore file's demo exception follows the new example location. Their exact previous versions are preserved under docs/project-history/original-root. The migration ledger distinguishes original preservation from newly authored pages.

- [Original-file locator](original-file-index.md)
- [Per-file migration ledger](FILE_MIGRATION_LEDGER.json)
- [Validation results](VALIDATION.json)
- [Replacement instructions](replacement-instructions.md)

## Reading historical documents

Original document text is unchanged. A historical Markdown file may therefore still mention its old location or link to a former relative path. Those references are not silently rewritten inside scientific originals. The locator maps each old file path to its actual preserved destination.

Some historical links were already incomplete in the source checkout. New navigation is checked separately; preserving an original does not certify all of its historical links or claims.

The application ZIP remains intact and retains its internal file layout. Older component collections are historical artifacts, not a promise that every component launches from its new archival location.

The root mixed-license notice is also preserved unchanged. Its historical `software/` paths now correspond to the current package under `workbench/releases/` and older material under `archive/software/`; its designated synthetic demo moved from `examples/no_copyright_media_demo/` to `examples/synthetic-demo/`. Use the per-file ledger for exact correspondences. Relocation does not change ownership, license terms or artifact-specific exceptions. Third-party notices remain with their relevant materials or in the root notices directory.

## Scope

The source checkout itself was not changed during preparation. Git metadata is not included in this tree. The validation covers file identity, destination collisions, new navigation links and editorial checks, not scientific validity, device safety, comprehensive licensing or a fresh privacy review.
