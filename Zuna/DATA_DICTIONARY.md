# Reading and verifying this archive

- `README.md`: orientation and primary results.
- `summary_metrics.json`: four historical full-comparison stages across two recordings; not four independent studies.
- `run_1/`: original/guided/corrected reports, audits, and failure history.
- `run_2/`: final comparison, QC, and execution records.
- `engineering/`: runtime-only thread benchmark, separate from biological evidence.
- Public JSON envelope: `schema=PRAYCG_PublicAnalysisDerivative_v1_0`, `original_document_sha256`, transformation/context notes, and a `record` containing the redacted original data. Do not submit it as a production recipe or original acquisition record.
- `manifest.json`: original-document hashes and the hashes/lengths of their transformed public files. Original hashes cannot be recomputed from redacted copies; privately held originals are needed.
- Nested `canonical_sha256` and other `*_sha256` fields inside exported records remain historical original-source claims. They do **not** authenticate the transformed record objects. Use the public manifest and checksums for the exported bytes.
- `SHA256SUMS.txt`: hashes every other public file at packaging. The external ZIP checksum verifies transport.

Units remain those in each source: µV for amplitude/RMSE; µV² for squared amplitude; µV²/Hz for PSD; seconds/sample counts for coverage; dimensionless NMSE/correlation. Numeric aggregate values are preserved, with nonfinite values explicitly marked not estimable if encountered. Local identities and exact machine times are intentionally unavailable. Missing raw data, masks, code and environments mean this is **inspection/audit evidence, not a self-contained numerical replay package**.

Run 1's existing independent numerical verification covered its corrected full result; Run 2's completion verification covered execution, coverage, eight-thread settings and immutable hashes. This export checks copying/redaction/integrity, not a new independent reconstruction of either scientific result.
