# Public-copy privacy review

## Included

Research summaries; aggregate reconstruction metrics and spectra; per-block/per-electrode tables; QC findings; methods and software/model identities; engineering checks; and unsuccessful-attempt history. Reports describe sensitive physiological measurements even without direct identifiers.

## Excluded or transformed

- Raw XDF recordings; NPZ/NPY/FIF/EDF data; measured/reconstructed waveform arrays; waveform images/SVGs; masks and model checkpoints; sample/event ledgers; hardware XML and stream inventories.
- Installed environments, models, wheels, executable code, raw logs and commands, process identifiers, local computer paths, reviewer/operator identifiers, source IDs and exact machine-clock timestamps.
- Original raw stream headers and device/host identity hashes are removed. Generic EEG/respiration stream labels, channel names and acquisition rates may remain where needed to explain the methods; these are not unique source identities.
- Detailed per-context/per-sample telemetry fields are removed while aggregate endpoints, spectra, durations and counts are retained. Known run identifiers are replaced by RUN_1/RUN_2; other UUIDs are removed. Dates mentioned in historical narrative may remain as research chronology.
- Original HTML is not copied. A new static overview is generated without embedded waveforms, scripts, remote assets or automatic requests. Private links in Markdown are removed or redirected to included public derivatives.

## Required human review

Before uploading, confirm permission to disclose the physiological findings, read the README and both final summaries, and inspect the file list. This is **privacy-reduced**, not certified anonymous or a legal/ethics clearance. Public account identity, research dates, values and retained source-file hashes can enable linkage. Hashes support audit but are not anonymization.

This export does not authorize publication on another participant's behalf, select a broad data license, or upload anything. Keep the untouched private originals separately. A future raw-data release requires its own privacy/consent and licensing decision.
