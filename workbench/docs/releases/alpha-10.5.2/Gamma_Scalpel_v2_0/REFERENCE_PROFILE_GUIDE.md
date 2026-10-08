# Gamma Scalpel reference profile

Use this optional profile when the recording lacks participant/source assignments or measured cross-device timing metadata, or when explicitly defined condition blocks/thresholds are available. Do not infer timing from coincident gamma and muscle activity: doing so would bias the very relationship being examined.

Save `gamma_reference_profile_v2_0.json` alongside the analysis context. This is a binding for one recording, not a reusable hardware calibration certificate. The Forge records the profile's file hash; the worker rechecks the source XDF hash, acquisition UUID and every evidence-file hash. The example below is a template containing placeholders and is not verified evidence.

```json
{
  "schema": "PRAYCG_GammaReferenceProfile_v2_0",
  "xdf_sha256": "EXACT_SOURCE_XDF_SHA256",
  "run_uuid": "RECORDED_ACQUISITION_UUID",
  "participant_id": "RECORDED_OR_REVIEWED_PARTICIPANT",
  "eeg_source_id": "EXACT_RECORDED_EEG_SOURCE_ID",
  "eeg_stream_uid": "OPTIONAL_EXACT_RECORDED_EEG_UID",
  "references": [
    {
      "source_id": "EXACT_RECORDED_EMG_SOURCE_ID",
      "participant_id": "RECORDED_OR_REVIEWED_PARTICIPANT",
      "type": "EMG",
      "alignment": {
        "status": "VERIFIED",
        "offset_seconds": 0.012,
        "drift_ppm": 4.0,
        "origin_lsl": 1000.0,
        "residual_seconds": 0.008,
        "evidence_path": "measured_timing_review.json",
        "evidence_sha256": "EXACT_EVIDENCE_SHA256"
      }
    }
  ],
  "blocks": [
    {"label": "eyes-open rest", "start_lsl": 1000.0, "end_lsl": 1060.0},
    {"label": "active task", "start_lsl": 1060.0, "end_lsl": 1120.0}
  ],
  "thresholds": {
    "EXACT_RECORDED_EMG_SOURCE_ID": {
      "Masseter_Left": {"metric": "rms_uv", "value": 15.0}
    }
  }
}
```

The numeric examples illustrate syntax only; they are not suggested device values or validated thresholds. Remove optional fields that are unavailable. A profile with only EMG assignment does not assess EOG. Include each intended source exactly once. Labels and source IDs must match the saved recording. `type` is exactly `EMG` or `EOG`; threshold metric is `rms_uv` for EMG and `p2p_uv` for EOG. Evidence paths may be absolute or relative to this profile.

The alignment transform applied only to the derived reference analysis timeline is:

`t_aligned = t_recorded + offset_seconds + (t_recorded - origin_lsl) * drift_ppm / 1e6`

The XDF loader first applies its recorded clock offsets without dejitter. Measure alignment evidence on that same common-clock convention. Preserve offset estimation, paired-event identities, observation duration, drift and maximum residual uncertainty in the cited evidence. A `VERIFIED` string does not independently validate a measurement; it declares the reviewed evidence used. The worker verifies its identity and numerics, not the physical experiment. Shared recorded sampling-clock IDs can qualify within-device references without an affine alignment profile.

Condition blocks must be nonoverlapping, within the selected recording scope and explicitly labeled by the actual condition. A window crossing a block boundary is excluded from condition matching, while its original recording summary remains. A protocol name never supplies a condition label. Outcomes requiring at least five reference windows remain unavailable when this support is absent.
