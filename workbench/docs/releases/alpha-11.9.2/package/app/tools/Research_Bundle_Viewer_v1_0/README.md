# Research Bundle Viewer 1.0

Export one explicitly selected Research Exchange 1.0 ZIP as a standalone HTML page. The recipient opens that page in a modern browser without installing PRAYCG, Python, a server, or dependencies. This is an inspection view, not a replay or executable report.

## Workbench integration

Load `research_bundle_viewer.py` and call `export_viewer(bundle_path, destination_html)`. The result includes `path`, `archive_sha256`, `verified_file_count`, `preview_count`, and `omitted_count`. The function never opens the browser or uploads anything and refuses to overwrite an existing destination. Choose an existing destination folder on a local filesystem supporting hard links. Failures raise exceptions; the GUI should report them and leave the source bundle unchanged.

Command line: `python research_bundle_viewer.py --bundle selected.zip --output review.html`.

The viewer contains byte-preserved content from that bundle only, plus its own interface. Private paths already present in the selected manifest/reports/provenance are retained as text, never followed. The local ZIP filename/path is not embedded. The page displays the original privacy tier and raw/private selections. Export does not anonymize, approve sharing, or certify consent. Nothing is automatically published.

## Integrity boundary

The native exporter uses the existing Research Exchange verifier to check the complete archive, ledger and metadata bindings. It rehashes the same open ZIP after reading previews and checks the file identity for changes. The browser independently hashes the exact embedded manifest and complete previews. It clearly identifies omitted members and does not claim to recheck the original ZIP. Neither the manifest nor exporter record is a digital signature: a person who rewrites the page can rewrite both the data and hashes. Compare the original ZIP digest with a separately trusted receipt when that matters.

No bundle payload is imported, extracted or executed. HTML/XML reports are literal source text, not rendered pages. Report titles, links and local paths are never turned into links. A restrictive Content Security Policy permits only the viewer's hashed script and local styles, with no network, images, frames, media, objects or forms. The UI uses text nodes; no HTML interpretation, fetch, sockets, external assets, storage or dynamic code execution is used. Browser SHA-256 failure withholds all previews.

## Limits and traces

Input and expanded ZIP limits: 256 MiB; 5,000 members; central directory 4 MiB; root manifest 2 MiB; compression ratio 100 for members over 1 MiB. Research Exchange rejects traversal, absolute/drive paths, special/link/reparse entries, duplicate/case/Unicode collisions, directory/file collisions, encrypted members, nested archives, undeclared/missing members and hash mismatches. ZIP64 member headers used by Research Exchange are supported; split archives, ZIP64 archive directories, ZIP prefixes/trailing data and unsupported methods are rejected. Large bundles should be inspected with the native research tools or exported with a smaller deliberate selection; limits are not bypassed.

Complete UTF-8 TXT, MD, JSON, CSV, TSV, HTML, HTM, XML and LOG members up to 1 MiB are eligible. Total embedded preview bytes are limited to 8 MiB, with provenance first. All omitted members remain listed in the hash ledger with an explanation. Previews are never truncated and called verified.

CSV/TSV plotting accepts a user-selected X and Y column. The header checkbox controls whether the first row supplies labels. Row index is explicitly not time. No units are invented or converted. The first 20,000 data rows and at most 128 columns are supported, with an explicit prefix notice when bounded. Missing/nonfinite/nonnumeric pairs break lines. Values remain in original order; there is no filtering, gap filling, time synchronization, resampling or scientific interpretation. Binary recordings and containers are not decoded here.

## Verification and demo

Run `python -m unittest discover -s tests -p "test_*.py"` and `node tests/test_viewer.js` from this folder. Tests use synthetic bundles, hostile HTML, path attacks, duplicate entries/JSON, links, hash tampering, expansion limits, change detection, CSV gaps and unavailable browser cryptography.

`python tests/make_demo.py` creates `examples/synthetic_research_viewer.html` from synthetic data only. The included example has an intentional trace gap and inert HTML with an external image that must never be requested. It is an artifact for browser QA, not evidence of participant data or a numerical replay.
