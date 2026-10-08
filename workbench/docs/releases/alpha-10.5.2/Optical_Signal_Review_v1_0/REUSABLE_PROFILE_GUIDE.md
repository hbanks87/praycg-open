# Reusable optical profiles

Alpha 10.5.2 separates fixed instrument information from recording-specific information. A supported profile can be reviewed once, versioned and reused. Each analysis automatically saves its own XDF/run/source binding, selected scope and baseline.

## Supplied Athena profile

`profiles/muse_s_athena_brainflow_raw_v1_0.json` identifies the Workbench's pinned BrainFlow 5.23.0 Athena optical route and exact sixteen-channel order. The profile includes manufacturer information and a local copy of the public source review with byte hashes. It is **DRAFT for hemoglobin conversion**. The published wavelength list does not establish which recorded columns form a wavelength pair. Geometry, offset/gain behavior and firmware mapping remain unresolved. Missing firmware is allowed only to identify this draft raw-review profile; it does not certify conversion.

## Reusable instrument schema

Use `PRAYCG_OpticalInstrumentProfile_v1_0` with:

- `profile_id`, `profile_version`, and `status` (`DRAFT` or `VERIFIED`).
- `match.model`, `match.decoder_id`, exact `match.decoder_versions`, exact `match.firmware_versions`, and ordered `match.channel_labels`. `match.board_id` is optional but checked when present. Empty recorded identity never matches a verified version list.
- `evidence`: local files under the profile directory, each with `relative_path` and byte `sha256`.
- `mapping`: the wavelength pairs, distances and extinction conventions described in the legacy guide. Source/detector three-dimensional coordinates are optional; a supported physical distance is sufficient for concentration conversion. If coordinates are supplied, both must be finite and their separation must match the declared distance.
- `intensity_model.positive_proportional_intensity_verified` and `additive_offset_accounted_for`, both true for conversion. `gain_behavior` must be `CONSTANT_BY_VERIFIED_DESIGN`, or `RECORDED_STATE` with the recorded `optical_gain_state` equal to `CONSTANT`. Unknown automatic gain is insufficient.
- `pathlength_assumptions.description` and `pathlength_assumptions.source`: explicit biological/model assumptions, separate from fixed instrument facts. Pair-specific numerical factors remain in `mapping`.
- `canonical_sha256`: the canonical content hash with this field omitted, using the Workbench's `sha256_json` convention.

Firmware-invariant behavior is not assumed. An exceptional `match.firmware_invariance` declaration must have `verified: true`, `scope: ALL_FIRMWARE_FOR_THIS_HARDWARE`, a nonempty rationale, and an `evidence_relative_path` naming one of the hashed evidence files. This declaration requires actual supporting instrument evidence. The supplied Athena profile makes no such declaration.

The worker searches packaged profiles automatically. It requires exactly one match, or an explicit advanced `--instrument-profile` selection. Multiple matches, mismatched firmware/decoder/channel identity, missing references or changed evidence leave hemoglobin conversion unavailable while raw exploration continues. A valid JSON shape or checksum does not by itself verify scientific assumptions.

## Recording binding

`optical_run_binding.json` uses `PRAYCG_OpticalRunBinding_v1_0` and records the instrument profile identity/version/content hash, XDF hash, run UUID, recorded source identity, scope, baseline and assumptions. It is an immutable analysis output; the original recording is untouched. Reports also include the instrument file hash, evidence hashes and the worker/profile-adapter source hashes.

Legacy `--optical-profile` files remain supported and take precedence for hemoglobin calculation when explicitly supplied. The report identifies the conversion route. No individual recording can recover absent channel mapping by having a longer baseline.

## Frozen exploratory settings

The optional `--review-settings` JSON uses `PRAYCG_OpticalReviewSettings_v1_0`, exact `xdf_sha256` and `run_uuid`, and a canonical hash. It can contain `scope` (`recording` or `protocol`), `spectral_window` (`auto`, `30`, `10`, `5`), `baseline_seconds`, `stream_uid` and `stream_source_id`. When both source identifiers are provided, they must select the same unique stream. Conflicting explicit command-line settings are refused.

Defaults are complete recording, automatic 30/10/5-second selection, and a ten-second positive-value baseline. Full and screened spectra share one resolution. Ratios of positive recorded numbers remain descriptive and do not enable hemoglobin conversion.
