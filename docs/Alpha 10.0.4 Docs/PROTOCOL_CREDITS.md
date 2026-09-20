# Protocol author credits and source citations

PRAYCG protocol development and adaptation byline: **Hoyt Banks**, confirmed by the author. This credit is separate from authorship of external papers, datasets, stimuli, or software used by a protocol. An approval reviewer or copyright-holder notice does not establish scientific authorship.

Every one of the 67 packaged protocol definitions carries `scholarly_attribution`. It contains the PRAYCG byline, original source author lists where verified, source references, retained document lineage, historical local-definition references, and separate rights and scientific boundaries. Public protocol names and operational settings are not changed by these credits.

The [protocol citation guide](PROTOCOL_CITATIONS.md) renders the same metadata for reading. Original publication, dataset, preprint, retained-document, and versioned local-definition records remain distinguishable. Sixteen reviewed primary-source records cover 23 externally sourced Atlas protocols. The other 44 definitions cite their local definition and retained lineage where available. These counts describe attribution coverage, not scientific validation or a complete review of prior literature.

## Historical definitions and study records

Local source citations identify the exact Alpha 10.0.3 definitions used to prepare the attribution update. Their release labels and SHA-256 values deliberately remain tied to those historical files. They are not hashes of the current Alpha 10.0.4 manifests, which now contain the added attribution. Prospective sequence variants cite both their own historical definition and their base protocol.

A current run's locked protocol definition and current file hash identify what actually ran. Preserve that evidence alongside these historical source citations. Previously saved study locks, recordings, reports, and manifests must not be rewritten to add a later byline or bibliography. If old evidence lacks attribution, report that absence and keep any later supplemental attribution separate from the original record.

## Citation is separate from copyright and licensing

Use the original authors, source title, publication or dataset version, and source identifiers recorded for the material actually used. Credit Hoyt Banks for the PRAYCG implementation or adaptation separately; do not substitute that credit for original source authors.

Retain original copyright and license text, NOTICE files, and modification notices when the actual source license requires them. Source code, data, media, questionnaires, and paper text can have different permissions. A citation does not replace those requirements or establish permission to redistribute a stimulus. The citation registry preserves source-specific license notes; it is not a license clearance record or a complete dependency inventory.

No affiliation, endorsement, review, sponsorship, or approval by the cited authors, institutions, or projects is implied. Bibliographic verification does not establish exact replication, scientific validity, safety, or clinical benefit.

## Maintaining attribution during generation

- `config/protocol_verified_source_records_v1_0.json` preserves the 16 reviewed primary-source records and protocol mappings.
- `config/protocol_scholarly_attribution_v1_0.json` stores the reviewed metadata for all 67 protocol identifiers.
- `control_center/scripts/praycg_protocol_attribution_v1_0.py` validates metadata, formats readable credits, checks historical artifacts when available, and applies registered attribution during generation.
- The Alpha 9.10 manifest builder and prospective counterbalance generator apply the registered metadata before serialization. Prospective variants receive their own references rather than inheriting only their base protocol's self citation.

New protocol identifiers need their own attribution review. Do not assign another protocol's verified status or source authors by resemblance. Changes to existing operational definitions may retain an explicitly historical source citation, but a newly claimed source artifact requires its own release/version, title, path, and verified hash. Update metadata through review, then refresh release fingerprints using the normal release process.
