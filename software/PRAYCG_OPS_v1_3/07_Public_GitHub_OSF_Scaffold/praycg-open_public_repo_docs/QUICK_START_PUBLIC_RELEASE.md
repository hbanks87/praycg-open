# Quick start for public release

1. Replace placeholder URLs in `README.md` and `CITATION.cff`.
2. Add current release ZIPs to GitHub Releases, not directly into the repo.
3. Upload stable release ZIPs and PDF handouts to OSF.
4. Confirm no copyrighted media or raw private participant data are committed.
5. Run a repository audit:

```bash
git status
git ls-files | grep -E "\.(mp4|mov|wav|mp3|xdf|zip|pdf|docx)$"
```

6. If any forbidden files are listed, remove them before public release.
7. Make GitHub public only after the boundary docs are visible at the root.
