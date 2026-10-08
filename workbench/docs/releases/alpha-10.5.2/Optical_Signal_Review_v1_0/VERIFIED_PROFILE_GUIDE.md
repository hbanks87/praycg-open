# Verified optical profile guide

This guide describes `PRAYCG_OpticalFnirsProfile_v1_0`. It is an advanced research configuration for relative hemoglobin conversion. A valid file structure and matching hashes establish reproducibility; the person declaring the profile verified must also establish that its optical assumptions match the physical instrument and recording.

**No verified Muse S Athena mapping is bundled.** Sixteen raw optical channels do not establish sixteen anatomical measurement sites, wavelength pairing, or hemoglobin concentrations.

## Required top-level fields

| Field | Required meaning |
|---|---|
| `schema` | Exactly `PRAYCG_OpticalFnirsProfile_v1_0`. |
| `status` | Exactly `VERIFIED` only after the supporting evidence has been reviewed. A draft does not enable conversion. |
| `xdf_sha256` | SHA-256 of the exact completed XDF bytes. |
| `run_uuid` | UUID of the same acquisition identified by its analysis-window manifest. |
| `stream_source_id` | Exact recorded optical stream `source_id`; never substitute a nearby live device. |
| `constant_gain_verified` | Boolean `true` after establishing stable, comparable light-intensity scaling throughout this recording. |
| `baseline_seconds` | Positive finite duration from the selected scope start. Default: 10 seconds. |
| `evidence` | Nonempty list of evidence files, each with `relative_path` and exact `sha256`. Files must remain inside the profile directory. |
| `mapping` | Nonempty list of independently supported wavelength pairs described below. |
| `analysis_blocks` | Optional list of explicit `{label, start_lsl, end_lsl}` intervals for descriptive response review. Labels must be unique, times finite and advancing, blocks disjoint, and all bounds inside the recording's verified analysis window. |
| `canonical_sha256` | Canonical content hash of the complete JSON object with this field omitted. |

Evidence should establish wavelength identity, source and detector positions, pathlength assumptions, extinction conventions, and instrument intensity behavior. Add reviewer identity, review date, device/firmware identity, and limitations as documentary fields. Hashes do not replace that review.

The intensity input must represent positive light intensity proportional to the measured optical signal, with constant multiplicative gain. Establish and document any additive dark offset, gain changes, automatic exposure, clipping, and device preprocessing. This module does not subtract unknown offsets or reverse unknown instrument processing. If those assumptions cannot be established, use raw optical review.

## Fields for each wavelength pair

| Field | Definition and units |
|---|---|
| `name` | Nonempty unique pair name; it is a measurement identity rather than a brain-region assertion. |
| `channel_labels` | Two distinct exact measured channel labels, in the same order as wavelengths and extinction matrix rows. Each measured channel may appear in only one pair. |
| `wavelengths_nm` | Two distinct positive finite wavelengths, in nanometres. |
| `source_position_m` | Three finite coordinates for the verified physical source, in metres. |
| `detector_position_m` | Three finite coordinates for the verified physical detector, in the same coordinate frame. |
| `distance_m` | Positive source–detector distance in metres. Source and detector must differ; the distance must agree with their coordinates within 1%. |
| `partial_pathlength_factors` | Two positive finite dimensionless factors, one for each wavelength. Document their provenance and applicability. |
| `extinction_natural_log_m_inverse_per_molar` | A 2×2 nonnegative finite matrix. Rows follow wavelength order; columns are HbO then HbR. Coefficients use natural-log attenuation per metre per molar. The resulting inversion must be sufficiently well conditioned. |

Do not paste coefficients with base-ten absorbance or centimetre units into a field requiring natural-log attenuation per metre. Convert and document the source convention first. An ambiguous convention should leave conversion unavailable.

## Baseline and inversion

The baseline begins at the selected analysis scope start. For each pair, both channels must be finite, positive, and accepted by the engineering screen. At least 80% of the configured duration must have supported positive samples, and accepted baseline samples may not bridge an unsupported timing or acceptance gap. The reference intensity is the per-wavelength median of that baseline.

The calculation is:

`optical_density = -ln(intensity / baseline_intensity)`

`A = diag(distance_m × partial_pathlength_factors) × extinction_matrix`

`relative_concentration_µM = solve(A, optical_density) × 1,000,000`

This yields relative HbO/HbR changes. Invalid intensity remains missing. A separate mask retains engineering screening rather than turning generated concentrations into raw measurements. Singular or numerically unusable conversion is reported as unavailable.

With verified analysis blocks, the report summarizes each pair and component by full and jointly screened sample counts, observed sample exposure in seconds, mean, and median relative µM. Exposure uses the observed native sampling rate; it does not imply an uninterrupted block or independent observations. The baseline method stays visible. No block effect size, significance, cortical origin, or cognitive interpretation is asserted. Without explicit block metadata, block response review is unavailable.

## Canonical hash and evidence binding

Create the final profile object, omit `canonical_sha256`, and use the Workbench EEG module's `sha256_json` function. It hashes UTF-8 JSON with sorted keys and compact separators. Add the resulting digest as `canonical_sha256`. Every evidence file must also have its own byte SHA-256.

Changing the XDF, run UUID, stream identity, evidence bytes, mapping, baseline, or documentary fields changes the profile binding. Save a new profile and analysis attempt. The worker verifies evidence before conversion and again before completing the result; it never modifies the original recording.

## Safe preparation sequence

1. Review instrument documentation and calibration evidence. Establish the measured channel order, wavelengths, physical geometry, intensity behavior, and coefficient conventions.
2. Keep the working file a draft until those assumptions are supported.
3. Bind the final profile to the exact XDF hash, run UUID, and recorded optical source identity.
4. Place supporting files inside the profile directory and record their hashes.
5. Review all pair fields, baseline applicability, and limitations. Compute the final canonical hash.
6. Run a new optical review attempt with the profile. Inspect raw signals and coverage alongside relative estimates.

The bundled analytic tests use artificial signals to check the inversion formula. Those fixtures are not Athena calibration profiles and must not be used to certify a real recording.
