# Replacing the repository layout

This is a complete replacement tree, not a merge overlay. Pasting it on top of an existing checkout without retiring the old tracked paths leaves both layouts in place.

## Before changing the existing checkout

1. Keep the prepared replacement folder separate and review its README and original-file locator.
2. In GitHub Desktop, confirm the existing repository has no uncommitted work you need to preserve separately.
3. Make a separate backup of the existing checkout, including its hidden Git metadata. The migration ledger is an integrity record, not a backup.
4. Check that the source commit and original-file hashes recorded in the ledger still describe the checkout you intend to replace. If files have changed since preparation, stop and reconcile them first.
5. Prefer a dedicated branch for reviewing this reorganization.

## Apply the replacement

Preserve the existing checkout's hidden .git directory. It contains its history and remote connection. The prepared tree intentionally does not include .git.

Only after the backup and identity checks, retire the old tracked files and folders from the checkout and copy the contents of the prepared tree into the checkout root. Do not put the replacement folder itself one level down inside the checkout.

Do not use a broad delete or a force reset. A controlled, per-path replacement is preferable, especially if the checkout contains local ignored environments, private study folders or unrelated untracked work. Those items were not included in the tracked-file inventory and must be handled separately.

## Review before committing or pushing

- The root should contain the new README and the Workbench, Research, Hardware, Examples, Docs, Notices and Archive areas.
- The prior root software layout should not remain as a second active layout.
- Confirm all original destinations against the migration ledger and hashes.
- Open the theory index and confirm historical versions and duplicate occurrences remain available.
- Check the current application ZIP hash against its preserved original; no new application release was produced.
- Review the entire GitHub Desktop change list. File moves may be displayed as additions and deletions; that alone does not prove loss. Use the ledger to verify identity.
- Commit only the reviewed changes, then push the branch or submit it for review.

No commit, push, source-checkout cleanup or deletion was performed when this replacement folder was prepared.

If you want the existing checkout updated automatically, request that as a separate operation so it can be backed up, validated and applied against its current state.
