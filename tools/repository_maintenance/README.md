# Restore missing historical companions

The [reviewed restoration plan](RESTORATION_PLAN.json) identifies 320 exact public files and 12 labelled locator pages for missing historical link targets. Its public archive/commit sources, byte counts, hashes and member names make the recovery reproducible. The [repair record](../../docs/reorganization/link-repair-2026-10-26/README.md) explains preservation and link-check scope.

The helper checks every source and target before adding files. It creates missing targets, accepts already identical targets and refuses to change any existing content. Downloaded historical code is copied as evidence, never executed. Locator pages identify themselves as new navigation and link to preserved sources; they are not represented as recovered original text.

From the repository root, with Python 3.11 or later:

```sh
python -m unittest discover -s tools/repository_maintenance -p test_restore_historical_links.py -v
python tools/repository_maintenance/restore_historical_links.py
python tools/repository_maintenance/restore_historical_links.py --apply
```

The default command verifies without adding files. `--apply` adds only the reviewed missing targets. The [manual restoration workflow](../../.github/workflows/restore-historical-links.yml) runs the checks, rejects changes to existing tracked files, stages only plan entries and commits additions to `main`. It never force-pushes. If another commit arrives during restoration, inspect the rejected push and rerun against the new `main`.

The recovered files support historical reading and attribution. For an executable environment, obtain the complete matching software release rather than running a partial documentation mirror. The plan is a dated recovery record; expanding it requires a new source/identity review.
