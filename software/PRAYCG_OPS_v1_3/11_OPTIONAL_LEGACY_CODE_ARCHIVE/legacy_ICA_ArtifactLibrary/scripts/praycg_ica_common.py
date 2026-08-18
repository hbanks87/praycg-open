#!/usr/bin/env python3
"""
Shared utilities for PR-AYC-G ICA Artifact Library tools.

These utilities deliberately keep claims narrow:
- XDF loading and marker parsing.
- MNE Raw construction from EEG-like streams.
- Basic QC and ICA feature extraction.
- No automatic claim that any component is artifact unless inspected.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import signal, stats


@dataclass
class XDFStream:
    name: str
    stream_type: str
    time_series: np.ndarray
    time_stamps: np.ndarray
    info: dict


def load_xdf_streams(xdf_path: str | Path) -> List[XDFStream]:
    """Load XDF streams using pyxdf and return normalized stream objects."""
    try:
        import pyxdf
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("pyxdf is required. Install with: pip install pyxdf") from exc

    streams_raw, _header = pyxdf.load_xdf(str(xdf_path), synchronize_clocks=True, dejitter_timestamps=True)
    streams: List[XDFStream] = []
    for s in streams_raw:
        info = s.get("info", {})
        name = _first(info.get("name"), default="")
        typ = _first(info.get("type"), default="")
        ts = np.asarray(s.get("time_series", []))
        t = np.asarray(s.get("time_stamps", []), dtype=float)
        streams.append(XDFStream(name=name, stream_type=typ, time_series=ts, time_stamps=t, info=info))
    return streams


def _first(x, default=""):
    if isinstance(x, (list, tuple)) and len(x) > 0:
        return x[0]
    return default if x is None else x


def find_stream(
    streams: Sequence[XDFStream],
    name: Optional[str] = None,
    stream_type: Optional[str] = None,
    must_have: bool = True,
) -> Optional[XDFStream]:
    """Find an XDF stream by exact or case-insensitive name/type substring."""
    if name:
        for s in streams:
            if s.name == name:
                return s
        lname = name.lower()
        for s in streams:
            if lname in s.name.lower():
                return s
    if stream_type:
        ltyp = stream_type.lower()
        for s in streams:
            if s.stream_type.lower() == ltyp or ltyp in s.stream_type.lower():
                return s
    if must_have:
        available = ", ".join([f"{s.name}/{s.stream_type}" for s in streams])
        raise ValueError(f"Could not find stream name={name!r} type={stream_type!r}. Available: {available}")
    return None


def stream_inventory(streams: Sequence[XDFStream]) -> pd.DataFrame:
    rows = []
    for s in streams:
        arr = np.asarray(s.time_series)
        rows.append(
            dict(
                name=s.name,
                type=s.stream_type,
                samples=int(arr.shape[0]) if arr.ndim > 0 else 0,
                channels=int(arr.shape[1]) if arr.ndim > 1 else 1,
                t_min=float(np.nanmin(s.time_stamps)) if len(s.time_stamps) else np.nan,
                t_max=float(np.nanmax(s.time_stamps)) if len(s.time_stamps) else np.nan,
                duration_sec=float(np.nanmax(s.time_stamps) - np.nanmin(s.time_stamps)) if len(s.time_stamps) > 1 else np.nan,
                nominal_srate=_first(s.info.get("nominal_srate"), default=""),
            )
        )
    return pd.DataFrame(rows)


def estimate_sfreq(timestamps: np.ndarray) -> float:
    timestamps = np.asarray(timestamps, dtype=float)
    if len(timestamps) < 3:
        return float("nan")
    dt = np.diff(timestamps)
    dt = dt[np.isfinite(dt) & (dt > 0)]
    if len(dt) == 0:
        return float("nan")
    return float(1.0 / np.median(dt))


def extract_channel_names(eeg_stream: XDFStream, n_channels: int) -> List[str]:
    """Try to extract labels from XDF metadata; fall back to Ch1..ChN."""
    try:
        desc = eeg_stream.info.get("desc", [])
        # XDF metadata structure varies; this handles common nested dict/list patterns.
        labels: List[str] = []
        if desc:
            channels = desc[0].get("channels", []) if isinstance(desc[0], dict) else []
            if channels:
                ch_list = channels[0].get("channel", []) if isinstance(channels[0], dict) else []
                for ch in ch_list:
                    if isinstance(ch, dict) and "label" in ch:
                        labels.append(_first(ch["label"], default=""))
        labels = [x for x in labels if x]
        if len(labels) >= n_channels:
            return labels[:n_channels]
    except Exception:
        pass
    return [f"Ch{i+1}" for i in range(n_channels)]


def apply_channel_map(channel_names: List[str], channel_map_csv: Optional[str | Path]) -> List[str]:
    if not channel_map_csv:
        return channel_names
    df = pd.read_csv(channel_map_csv)
    if "raw_name" not in df.columns or "montage_name" not in df.columns:
        raise ValueError("channel map CSV must contain raw_name and montage_name columns")
    mapping = dict(zip(df["raw_name"].astype(str), df["montage_name"].astype(str)))
    # If raw names don't match, use channel_index order if available.
    if not any(ch in mapping for ch in channel_names) and "channel_index" in df.columns:
        ordered = df.sort_values("channel_index")["montage_name"].astype(str).tolist()
        if len(ordered) >= len(channel_names):
            return ordered[: len(channel_names)]
    return [mapping.get(ch, ch) for ch in channel_names]


def make_mne_raw_from_xdf(
    eeg_stream: XDFStream,
    channel_map_csv: Optional[str | Path] = None,
    eeg_units: str = "microvolts",
    montage_name: str = "standard_1020",
):
    """Construct MNE RawArray from an EEG stream."""
    try:
        import mne
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("mne is required. Install with: pip install mne") from exc

    data = np.asarray(eeg_stream.time_series, dtype=float)
    if data.ndim == 1:
        data = data[:, None]
    # Drop all-NaN columns.
    n_ch = data.shape[1]
    ch_names = extract_channel_names(eeg_stream, n_ch)
    ch_names = apply_channel_map(ch_names, channel_map_csv)

    # MNE expects channels x samples in volts for EEG.
    data_t = data.T.copy()
    unit = eeg_units.lower().strip()
    if unit in ["microvolts", "microvolt", "uv", "µv"]:
        data_t *= 1e-6
    elif unit in ["millivolts", "mv"]:
        data_t *= 1e-3
    elif unit in ["volts", "v"]:
        pass
    else:
        raise ValueError("eeg_units must be microvolts, millivolts, or volts")

    sfreq = estimate_sfreq(eeg_stream.time_stamps)
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=["eeg"] * len(ch_names))
    raw = mne.io.RawArray(data_t, info, verbose="ERROR")
    raw.info["description"] = f"Created from XDF stream {eeg_stream.name}"

    try:
        montage = mne.channels.make_standard_montage(montage_name)
        raw.set_montage(montage, on_missing="ignore", verbose="ERROR")
    except Exception:
        pass
    return raw


def parse_marker_stream(marker_stream: XDFStream) -> pd.DataFrame:
    ts = np.asarray(marker_stream.time_stamps, dtype=float)
    series = np.asarray(marker_stream.time_series)
    markers = []
    for i in range(len(ts)):
        val = series[i]
        if isinstance(val, np.ndarray):
            val = val.tolist()
        if isinstance(val, (list, tuple)):
            val = val[0] if val else ""
        if isinstance(val, bytes):
            val = val.decode("utf-8", errors="replace")
        markers.append(str(val))
    df = pd.DataFrame({"time": ts, "marker": markers})
    # Add parsed fields for control-run marker format.
    parsed = [parse_artifact_marker(m) for m in markers]
    return pd.concat([df, pd.DataFrame(parsed)], axis=1)


ART_RE = re.compile(r"ARTIFACT_(?P<label>[A-Z0-9_]+)_REP_(?P<rep>\d+)_(?P<phase>PREP_START|ACTION_START|ACTION_END|RECOVERY_END|BLOCK_END)")


def parse_artifact_marker(marker: str) -> Dict[str, object]:
    m = ART_RE.match(marker)
    if not m:
        return {"artifact_label": "", "artifact_rep": np.nan, "artifact_phase": ""}
    return {
        "artifact_label": m.group("label"),
        "artifact_rep": int(m.group("rep")),
        "artifact_phase": m.group("phase"),
    }


def build_artifact_events(markers_df: pd.DataFrame) -> pd.DataFrame:
    """Return action intervals from paired ACTION_START/ACTION_END markers."""
    starts = markers_df[markers_df["artifact_phase"] == "ACTION_START"].copy()
    ends = markers_df[markers_df["artifact_phase"] == "ACTION_END"].copy()
    rows = []
    for _, srow in starts.iterrows():
        label = srow["artifact_label"]
        rep = int(srow["artifact_rep"])
        match = ends[(ends["artifact_label"] == label) & (ends["artifact_rep"] == rep)]
        if len(match):
            end_time = float(match.iloc[0]["time"])
        else:
            end_time = float(srow["time"] + 2.0)
        rows.append(
            dict(
                artifact_label=label,
                artifact_rep=rep,
                start_time=float(srow["time"]),
                end_time=end_time,
                duration_sec=max(0.0, end_time - float(srow["time"])),
                marker_start=srow["marker"],
            )
        )
    return pd.DataFrame(rows)


def add_mne_annotations(raw, markers_df: pd.DataFrame, xdf_t0: float):
    import mne

    onsets = markers_df["time"].to_numpy(dtype=float) - xdf_t0
    durations = np.zeros_like(onsets)
    desc = markers_df["marker"].astype(str).tolist()
    ann = mne.Annotations(onset=onsets, duration=durations, description=desc)
    raw.set_annotations(ann)
    return raw


def basic_channel_qc(raw) -> pd.DataFrame:
    data = raw.get_data()  # volts
    rows = []
    for idx, ch in enumerate(raw.ch_names):
        x = data[idx]
        x_uv = x * 1e6
        rows.append(
            dict(
                channel=ch,
                idx=idx,
                mean_uv=float(np.nanmean(x_uv)),
                sd_uv=float(np.nanstd(x_uv)),
                ptp_uv=float(np.nanmax(x_uv) - np.nanmin(x_uv)),
                nan_fraction=float(np.mean(~np.isfinite(x_uv))),
                flat_fraction=float(np.mean(np.abs(np.diff(x_uv)) < 1e-12)) if len(x_uv) > 1 else np.nan,
                robust_sd_uv=float(1.4826 * np.nanmedian(np.abs(x_uv - np.nanmedian(x_uv)))),
            )
        )
    return pd.DataFrame(rows)


def suggest_bad_channels(qc: pd.DataFrame, robust_sd_min_uv: float = 0.05, robust_sd_max_uv: float = 500.0) -> List[str]:
    bad = qc[
        (qc["nan_fraction"] > 0.01)
        | (qc["flat_fraction"] > 0.50)
        | (qc["robust_sd_uv"] < robust_sd_min_uv)
        | (qc["robust_sd_uv"] > robust_sd_max_uv)
    ]["channel"].tolist()
    return bad


def compute_sources(ica, raw):
    src = ica.get_sources(raw).get_data()
    return np.asarray(src, dtype=float)


def welch_bandpower(x: np.ndarray, sfreq: float, band: Tuple[float, float]) -> float:
    x = np.asarray(x, dtype=float)
    if len(x) < max(8, int(sfreq)):
        return np.nan
    nperseg = min(len(x), max(64, int(round(2.0 * sfreq))))
    freqs, psd = signal.welch(x, fs=sfreq, nperseg=nperseg)
    lo, hi = band
    mask = (freqs >= lo) & (freqs <= hi)
    if not np.any(mask):
        return np.nan
    return float(np.trapz(psd[mask], freqs[mask]))


def compute_component_feature_table(ica, raw) -> pd.DataFrame:
    sf = float(raw.info["sfreq"])
    sources = compute_sources(ica, raw)
    rows = []
    for c in range(sources.shape[0]):
        x = sources[c]
        total = welch_bandpower(x, sf, (1, min(55, sf / 2 - 1)))
        def rel(bp):
            return float(bp / total) if np.isfinite(bp) and np.isfinite(total) and total > 0 else np.nan
        delta = welch_bandpower(x, sf, (1, 4))
        theta = welch_bandpower(x, sf, (4, 8))
        alpha = welch_bandpower(x, sf, (8, 12))
        beta = welch_bandpower(x, sf, (13, 30))
        lg = welch_bandpower(x, sf, (30, min(45, sf / 2 - 1)))
        edge = welch_bandpower(x, sf, (45, min(55, sf / 2 - 1))) if sf / 2 > 55 else np.nan
        hf = welch_bandpower(x, sf, (70, min(110, sf / 2 - 1))) if sf / 2 > 110 else np.nan
        rows.append(
            dict(
                component=int(c),
                variance=float(np.nanvar(x)),
                robust_sd=float(1.4826 * np.nanmedian(np.abs(x - np.nanmedian(x)))),
                kurtosis=float(stats.kurtosis(x, nan_policy="omit")),
                skew=float(stats.skew(x, nan_policy="omit")),
                bp_delta=delta,
                bp_theta=theta,
                bp_alpha=alpha,
                bp_beta=beta,
                bp_low_gamma_30_45=lg,
                bp_edge_45_55=edge,
                bp_hf_70_110=hf,
                rel_delta=rel(delta),
                rel_theta=rel(theta),
                rel_alpha=rel(alpha),
                rel_beta=rel(beta),
                rel_low_gamma_30_45=rel(lg),
                rel_edge_45_55=rel(edge),
                rel_hf_70_110=rel(hf),
            )
        )
    return pd.DataFrame(rows)


def event_locked_scores(
    ica,
    raw,
    events_df: pd.DataFrame,
    baseline_pre_sec: float = 1.0,
    action_pad_sec: float = 0.0,
) -> pd.DataFrame:
    """Score each ICA component by artifact-label event RMS vs pre-event baseline."""
    sources = compute_sources(ica, raw)
    sf = float(raw.info["sfreq"])
    raw_start = 0.0  # MNE raw time begins at zero after conversion
    # The input events are in XDF time; convert before calling using xdf_t0 externally? We allow both by checking.
    # build_ica script will add rel_start/rel_end columns.
    if "rel_start" not in events_df.columns:
        raise ValueError("events_df must include rel_start and rel_end columns relative to raw first sample")
    rows = []
    for label, g in events_df.groupby("artifact_label"):
        if not label:
            continue
        for c in range(sources.shape[0]):
            action_vals = []
            base_vals = []
            for _, ev in g.iterrows():
                s0 = int(max(0, math.floor((float(ev["rel_start"]) + action_pad_sec - raw_start) * sf)))
                s1 = int(min(sources.shape[1], math.ceil((float(ev["rel_end"]) - action_pad_sec - raw_start) * sf)))
                b0 = int(max(0, math.floor((float(ev["rel_start"]) - baseline_pre_sec - raw_start) * sf)))
                b1 = int(max(0, math.floor((float(ev["rel_start"]) - 0.1 - raw_start) * sf)))
                if s1 > s0:
                    action_vals.append(float(np.sqrt(np.nanmean(sources[c, s0:s1] ** 2))))
                if b1 > b0:
                    base_vals.append(float(np.sqrt(np.nanmean(sources[c, b0:b1] ** 2))))
            if action_vals:
                action_med = float(np.nanmedian(action_vals))
                base_med = float(np.nanmedian(base_vals)) if base_vals else np.nan
                ratio = float(action_med / base_med) if np.isfinite(base_med) and base_med > 0 else np.nan
                diff = float(action_med - base_med) if np.isfinite(base_med) else np.nan
                rows.append(
                    dict(
                        artifact_label=label,
                        component=int(c),
                        action_rms_median=action_med,
                        baseline_rms_median=base_med,
                        action_minus_baseline=diff,
                        action_over_baseline=ratio,
                        n_events=int(len(action_vals)),
                    )
                )
    df = pd.DataFrame(rows)
    if len(df):
        # z-score within label across components.
        df["score_z_within_label"] = df.groupby("artifact_label")["action_minus_baseline"].transform(_zscore_series)
        df["ratio_z_within_label"] = df.groupby("artifact_label")["action_over_baseline"].transform(_zscore_series)
        df["artifact_score"] = df[["score_z_within_label", "ratio_z_within_label"]].mean(axis=1, skipna=True)
    return df


def _zscore_series(s: pd.Series) -> pd.Series:
    arr = s.to_numpy(dtype=float)
    mu = np.nanmean(arr)
    sd = np.nanstd(arr)
    if not np.isfinite(sd) or sd == 0:
        return pd.Series(np.zeros(len(s)), index=s.index)
    return pd.Series((arr - mu) / sd, index=s.index)


def ica_topographies(ica) -> np.ndarray:
    """Return components x channels topographies from ICA mixing matrix when available."""
    # mne.preprocessing.ICA has get_components(): channels x components
    comps = ica.get_components()
    return np.asarray(comps.T, dtype=float)


def make_artifact_templates(
    ica,
    feature_df: pd.DataFrame,
    scores_df: pd.DataFrame,
    top_n: int = 2,
    min_score: float = 1.0,
) -> Tuple[pd.DataFrame, Dict[str, np.ndarray], Dict[str, np.ndarray], List[str]]:
    """Build simple templates from the highest event-locked components per artifact label."""
    topo = ica_topographies(ica)
    feature_cols = [
        "kurtosis",
        "rel_delta",
        "rel_theta",
        "rel_alpha",
        "rel_beta",
        "rel_low_gamma_30_45",
        "rel_edge_45_55",
        "rel_hf_70_110",
    ]
    feature_mat = feature_df.set_index("component")[feature_cols]
    # Fill NaNs with column medians.
    feature_mat = feature_mat.apply(lambda col: col.fillna(col.median()), axis=0).fillna(0.0)
    rows = []
    topo_templates: Dict[str, np.ndarray] = {}
    feature_templates: Dict[str, np.ndarray] = {}
    labels = []
    for label, g in scores_df.groupby("artifact_label"):
        gg = g.sort_values("artifact_score", ascending=False).head(top_n)
        gg = gg[gg["artifact_score"] >= min_score]
        if len(gg) == 0:
            continue
        comps = gg["component"].astype(int).tolist()
        # Sign-align topographies to the first comp by absolute correlation.
        base = topo[comps[0]].copy()
        aligned = []
        for c in comps:
            v = topo[c].copy()
            if np.dot(base, v) < 0:
                v *= -1
            aligned.append(v)
        topo_templates[label] = np.nanmean(np.vstack(aligned), axis=0)
        feature_templates[label] = feature_mat.loc[comps].mean(axis=0).to_numpy(dtype=float)
        labels.append(label)
        rows.append(
            dict(
                artifact_label=label,
                template_components=",".join(map(str, comps)),
                template_n_components=len(comps),
                template_mean_score=float(gg["artifact_score"].mean()),
            )
        )
    return pd.DataFrame(rows), topo_templates, feature_templates, feature_cols


def save_templates_npz(
    out_path: str | Path,
    labels: Sequence[str],
    topo_templates: Dict[str, np.ndarray],
    feature_templates: Dict[str, np.ndarray],
    feature_cols: Sequence[str],
    channel_names: Sequence[str],
) -> None:
    labels = list(labels)
    topo = np.vstack([topo_templates[l] for l in labels]) if labels else np.empty((0, len(channel_names)))
    feats = np.vstack([feature_templates[l] for l in labels]) if labels else np.empty((0, len(feature_cols)))
    np.savez_compressed(
        out_path,
        labels=np.array(labels, dtype=object),
        topo_templates=topo,
        feature_templates=feats,
        feature_cols=np.array(list(feature_cols), dtype=object),
        channel_names=np.array(list(channel_names), dtype=object),
    )


def safe_json_dump(obj, path: str | Path) -> None:
    def default(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        return str(o)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=default)
