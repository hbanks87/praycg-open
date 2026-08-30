#!/usr/bin/env python3
"""
PRAYCG TTI Module v1.4.8
========================

Thermodynamic Theft Index (TTI) / Reception-Extraction Tradeoff module.

This module is an exploratory analysis tool. It estimates whether the Target
condition preserved more receptive meaning/integration than Contextual Override,
while Override diverted more capacity into task/extractive load.

Boundary: TTI is not a moral score, clinical metric, proof of consciousness,
or proof of OSM biology. It is a transparent composite index for PR-AYC-G
human-scale psychophysiology.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

VERSION = "1.4.8"

FEATURE_PRIORITY = [
    "contact_time_resolved_feature_frame.csv",
    "human_translation_kht_feature_frame.csv",
    "her_time_resolved_feature_frame.csv",
    "time_resolved_feature_frame.csv",
    "feature_frame.csv",
]
FEATURE_GLOBS = [
    "*_time_resolved_feature_frame.csv",
    "*time_resolved*feature*.csv",
    "*human_translation*kht*feature*.csv",
    "*feature_frame*.csv",
]

EVENT_PRIORITY = [
    "candidate_local_kht_topo_mred_event_table.csv",
    "candidate_local_kht_analysis.csv",
    "mred_event_table.csv",
]

OCM_PRIORITY = [
    "ocm025_rsm_cvb_squint_cue_epoch_table.csv",
    "combined_ocm_025_cue_epoch_table.csv",
    "ocm_cue_epoch_table.csv",
]

CONF_PRIORITY = [
    "branch_confound_reports.csv",
    "confound_registry.csv",
]


def eprint(*args):
    print(*args, file=sys.stderr)


def safe_read_csv(path: Path) -> Optional[pd.DataFrame]:
    try:
        if path and path.exists() and path.is_file():
            return pd.read_csv(path)
    except Exception as exc:
        eprint(f"WARNING: failed to read {path}: {exc}")
    return None


def find_file(analysis_folder: Path, explicit: str, priority: Sequence[str], globs: Sequence[str]) -> Optional[Path]:
    if explicit:
        p = Path(explicit)
        if p.exists():
            return p
    roots = []
    if (analysis_folder / "tables").exists():
        roots.append(analysis_folder / "tables")
    roots.append(analysis_folder)
    for root in roots:
        for name in priority:
            p = root / name
            if p.exists():
                return p
    for root in roots:
        for pat in globs:
            matches = sorted(root.glob(pat))
            if matches:
                return matches[0]
    return None


def norm_col_map(df: pd.DataFrame) -> Dict[str, str]:
    return {re.sub(r"[^a-z0-9]+", "", str(c).lower()): c for c in df.columns}


def pick_col(df: pd.DataFrame, candidates: Sequence[str]) -> Optional[str]:
    cmap = norm_col_map(df)
    for cand in candidates:
        key = re.sub(r"[^a-z0-9]+", "", cand.lower())
        if key in cmap:
            return cmap[key]
    # fuzzy contains
    for cand in candidates:
        key = re.sub(r"[^a-z0-9]+", "", cand.lower())
        for k, c in cmap.items():
            if key and (key in k or k in key):
                return c
    return None


def first_existing_cols(df: pd.DataFrame, groups: Sequence[Sequence[str]]) -> List[str]:
    cols = []
    for group in groups:
        c = pick_col(df, group)
        if c and c not in cols:
            cols.append(c)
    return cols


def as_numeric(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def robust_z(x: pd.Series) -> pd.Series:
    vals = as_numeric(x)
    med = np.nanmedian(vals)
    mad = np.nanmedian(np.abs(vals - med))
    scale = 1.4826 * mad
    if not np.isfinite(scale) or scale < 1e-9:
        scale = np.nanstd(vals)
    if not np.isfinite(scale) or scale < 1e-9:
        return vals * 0.0
    return (vals - med) / scale


def positive_z(x: pd.Series) -> pd.Series:
    return robust_z(x).clip(lower=0)


def condition_series(df: pd.DataFrame) -> pd.Series:
    c = pick_col(df, ["condition", "phase", "branch", "condition_label", "phase_label"])
    if c:
        return df[c].astype(str)
    return pd.Series([""] * len(df), index=df.index)


def is_target(s: pd.Series) -> pd.Series:
    return s.str.upper().str.contains("TARGET") & ~s.str.upper().str.contains("OVERRIDE")


def is_override(s: pd.Series) -> pd.Series:
    u = s.str.upper()
    return u.str.contains("OVERRIDE") | u.str.contains("CONTEXTUAL_OVERRIDE")


def time_col(df: pd.DataFrame) -> Optional[str]:
    return pick_col(df, ["condition_offset_sec", "phase_time_sec", "time_sec", "t_sec", "timestamp_sec", "relative_time_sec", "video_time_sec"])


def build_composite_feature_scores(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, List[str]]]:
    out = df.copy()
    mr_cols = first_existing_cols(df, [
        ["meaninggamma", "meaninggamma_z", "meaninggamma_score", "meaning_gamma_z", "meaning_gamma_score", "gamma_z"],
        ["tsp", "tsp_z", "temporal_semantic_proxy", "temporal_semantic_proxy_score", "tsp_score"],
        ["k_local", "k_ht_topo_local", "kht_topo", "local_k", "candidate_k"],
    ])
    enc_cols = first_existing_cols(df, [
        ["theta_integration", "theta_integration_z", "theta_delta_10_30", "theta_delta", "theta_handoff", "theta_global_z", "theta_midline_z", "theta_z"],
        ["mred_enc", "enc_score", "encoding_score", "integration_score"],
    ])
    api_cols = first_existing_cols(df, [
        ["api_a", "api_a_v1", "apia", "autonomic_availability", "availability_proxy"],
        ["rmssd_z", "hrv_rmssd_z", "sdnn_z"],
    ])
    x_cols = first_existing_cols(df, [
        ["taskgamma", "taskgamma_z", "task_gamma_z", "ptask", "ptask_z", "task_gamma_score"],
        ["ocm_score", "compute_stall_score", "rsm_compute_stall", "latent_guess_risk"],
        ["number_cue_distraction", "analytic_effort", "task_compliance"],
    ])
    artifact_cols = first_existing_cols(df, [
        ["artifact_score", "artifact", "artifact_z", "artifact_burden"],
        ["jaw_temporal_sentinel", "hf_proxy_45_55", "fp1_hf"],
    ])
    visual_cols = first_existing_cols(df, [
        ["visualgamma", "visual_gamma_z", "visual_control_gamma", "occipital_gamma", "visual_drive"],
    ])

    def comp(cols: List[str], name: str, penalty: bool = False):
        if not cols:
            out[name] = np.nan
            return
        zcols = []
        for c in cols:
            zcols.append(positive_z(out[c]) if penalty else robust_z(out[c]))
        out[name] = pd.concat(zcols, axis=1).mean(axis=1, skipna=True)

    comp(mr_cols, "TTI_MR_proxy")
    comp(enc_cols, "TTI_ENC_proxy")
    comp(api_cols, "TTI_API_proxy")
    comp(x_cols, "TTI_X_proxy")
    comp(artifact_cols, "TTI_Artifact_proxy", penalty=True)
    comp(visual_cols, "TTI_Visual_proxy")
    used = {
        "MR_cols": mr_cols,
        "ENC_cols": enc_cols,
        "API_cols": api_cols,
        "X_cols": x_cols,
        "Artifact_cols": artifact_cols,
        "Visual_cols": visual_cols,
    }
    return out, used


def mean_or_nan(df: pd.DataFrame, col: str) -> float:
    if col not in df.columns:
        return float("nan")
    v = pd.to_numeric(df[col], errors="coerce")
    if v.dropna().empty:
        return float("nan")
    return float(v.mean())


def delta_std(val: float, ref: pd.Series) -> float:
    # Standardize a between-condition delta by the robust scale of the underlying series.
    vals = pd.to_numeric(ref, errors="coerce")
    mad = np.nanmedian(np.abs(vals - np.nanmedian(vals)))
    scale = 1.4826 * mad
    if not np.isfinite(scale) or scale < 1e-9:
        scale = np.nanstd(vals)
    if not np.isfinite(scale) or scale < 1e-9:
        scale = 1.0
    return float(val / scale)


def compute_global_tti(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, float]]:
    cond = condition_series(df)
    tdf = df[is_target(cond)].copy()
    odf = df[is_override(cond)].copy()
    rows = []
    if tdf.empty or odf.empty:
        summary = {"status": "INSUFFICIENT_TARGET_OR_OVERRIDE_ROWS"}
        return pd.DataFrame(rows), summary

    components = {}
    for name, direction in [
        ("TTI_MR_proxy", "T_minus_O"),
        ("TTI_ENC_proxy", "T_minus_O"),
        ("TTI_API_proxy", "T_minus_O"),
        ("TTI_X_proxy", "O_minus_T"),
        ("TTI_Artifact_proxy", "penalty_abs_T_minus_O"),
        ("TTI_Visual_proxy", "penalty_abs_T_minus_O"),
    ]:
        mt = mean_or_nan(tdf, name)
        mo = mean_or_nan(odf, name)
        if direction == "T_minus_O":
            raw = mt - mo
            signed = delta_std(raw, df[name]) if name in df.columns else float("nan")
        elif direction == "O_minus_T":
            raw = mo - mt
            signed = delta_std(raw, df[name]) if name in df.columns else float("nan")
        else:
            raw = abs(mt - mo)
            signed = delta_std(raw, df[name]) if name in df.columns else float("nan")
        components[name] = signed
        rows.append({"component": name, "target_mean": mt, "override_mean": mo, "direction": direction, "raw_delta_for_tti": raw, "standardized_component": signed})

    weights = {
        "TTI_MR_proxy": 0.28,
        "TTI_ENC_proxy": 0.24,
        "TTI_API_proxy": 0.14,
        "TTI_X_proxy": 0.22,
        "TTI_Artifact_proxy": -0.08,
        "TTI_Visual_proxy": -0.04,
    }
    tti = 0.0
    wsum = 0.0
    for k, w in weights.items():
        val = components.get(k, float("nan"))
        if np.isfinite(val):
            tti += w * val
            wsum += abs(w)
    if wsum > 0:
        tti_norm = tti / wsum
    else:
        tti_norm = float("nan")
    summary = {
        "status": "OK",
        "TTI_raw_weighted_sum": float(tti),
        "TTI_weight_normalized": float(tti_norm),
        "interpretive_thresholds": "exploratory: >0.25 partial, >0.75 strong, <0 no Target advantage",
    }
    return pd.DataFrame(rows), summary


def compute_timewindow_tti(df: pd.DataFrame) -> pd.DataFrame:
    tcol = time_col(df)
    if not tcol:
        return pd.DataFrame()
    cond = condition_series(df)
    tdf = df[is_target(cond)].copy()
    odf = df[is_override(cond)].copy()
    if tdf.empty or odf.empty:
        return pd.DataFrame()
    # Pair by rounded condition offset / time bin.
    for d in [tdf, odf]:
        d["__timebin"] = (pd.to_numeric(d[tcol], errors="coerce") / 2.0).round() * 2.0
    cols = ["TTI_MR_proxy", "TTI_ENC_proxy", "TTI_API_proxy", "TTI_X_proxy", "TTI_Artifact_proxy", "TTI_Visual_proxy"]
    tg = tdf.groupby("__timebin")[cols].mean(numeric_only=True)
    og = odf.groupby("__timebin")[cols].mean(numeric_only=True)
    common = sorted(set(tg.index).intersection(set(og.index)))
    rows = []
    for b in common:
        row = {"time_sec": float(b)}
        for c in cols:
            row[f"target_{c}"] = float(tg.loc[b, c]) if c in tg.columns and pd.notna(tg.loc[b, c]) else np.nan
            row[f"override_{c}"] = float(og.loc[b, c]) if c in og.columns and pd.notna(og.loc[b, c]) else np.nan
        mr = row.get("target_TTI_MR_proxy", np.nan) - row.get("override_TTI_MR_proxy", np.nan)
        enc = row.get("target_TTI_ENC_proxy", np.nan) - row.get("override_TTI_ENC_proxy", np.nan)
        api = row.get("target_TTI_API_proxy", np.nan) - row.get("override_TTI_API_proxy", np.nan)
        x = row.get("override_TTI_X_proxy", np.nan) - row.get("target_TTI_X_proxy", np.nan)
        art = abs(row.get("target_TTI_Artifact_proxy", np.nan) - row.get("override_TTI_Artifact_proxy", np.nan))
        vis = abs(row.get("target_TTI_Visual_proxy", np.nan) - row.get("override_TTI_Visual_proxy", np.nan))
        vals = [(0.28, mr), (0.24, enc), (0.14, api), (0.22, x), (-0.08, art), (-0.04, vis)]
        tti = sum(w * v for w, v in vals if np.isfinite(v))
        denom = sum(abs(w) for w, v in vals if np.isfinite(v))
        row.update({
            "mr_delta_T_minus_O": mr,
            "enc_delta_T_minus_O": enc,
            "api_delta_T_minus_O": api,
            "extractive_delta_O_minus_T": x,
            "artifact_abs_delta_penalty": art,
            "visual_abs_delta_penalty": vis,
            "tti_timewindow": tti / denom if denom else np.nan,
        })
        rows.append(row)
    return pd.DataFrame(rows)


def compute_event_tti(event_df: Optional[pd.DataFrame]) -> pd.DataFrame:
    if event_df is None or event_df.empty:
        return pd.DataFrame()
    df = event_df.copy()
    cond = condition_series(df)
    df["__is_target"] = is_target(cond)
    df["__is_override"] = is_override(cond)
    # Build event-level proxy columns from existing event fields.
    df, used = build_composite_feature_scores(df)
    rows = []
    for label, mask in [("target", df["__is_target"]), ("override", df["__is_override"]), ("all", pd.Series([True]*len(df), index=df.index))]:
        part = df[mask]
        if part.empty:
            continue
        rows.append({
            "condition_group": label,
            "n_events": int(len(part)),
            "n_mr_high_enc_high": int(part.astype(str).apply(lambda r: "MR_HIGH_ENC_HIGH" in " ".join(r.values), axis=1).sum()),
            "mean_event_MR_proxy": mean_or_nan(part, "TTI_MR_proxy"),
            "mean_event_ENC_proxy": mean_or_nan(part, "TTI_ENC_proxy"),
            "max_event_K_or_MR": float(np.nanmax(pd.to_numeric(part.get("TTI_MR_proxy", pd.Series(dtype=float)), errors="coerce"))) if "TTI_MR_proxy" in part else np.nan,
        })
    return pd.DataFrame(rows)


def add_ocm_extraction(feature_df: pd.DataFrame, ocm_df: Optional[pd.DataFrame]) -> pd.DataFrame:
    # Feature-level TTI uses OCM only if present in feature columns. This optional summary is used for reporting.
    if ocm_df is None or ocm_df.empty:
        return pd.DataFrame()
    df = ocm_df.copy()
    cond = condition_series(df)
    df, used = build_composite_feature_scores(df)
    rows = []
    for label, mask in [("target", is_target(cond)), ("override", is_override(cond))]:
        part = df[mask]
        if part.empty:
            continue
        rows.append({
            "condition_group": label,
            "n_cues": int(len(part)),
            "mean_ocm_extraction_proxy": mean_or_nan(part, "TTI_X_proxy"),
            "mean_artifact_proxy": mean_or_nan(part, "TTI_Artifact_proxy"),
        })
    return pd.DataFrame(rows)


def overlay_from_timewindows(tw: pd.DataFrame, out_path: Path) -> None:
    if tw is None or tw.empty or "time_sec" not in tw.columns or "tti_timewindow" not in tw.columns:
        pd.DataFrame(columns=["start_sec", "end_sec", "category", "label", "source"]).to_csv(out_path, index=False)
        return
    # Top positive and negative windows for visual review.
    x = tw.dropna(subset=["tti_timewindow"]).copy()
    if x.empty:
        pd.DataFrame(columns=["start_sec", "end_sec", "category", "label", "source"]).to_csv(out_path, index=False)
        return
    top_pos = x.sort_values("tti_timewindow", ascending=False).head(10)
    top_neg = x.sort_values("tti_timewindow", ascending=True).head(5)
    rows = []
    for _, r in top_pos.iterrows():
        rows.append({"start_sec": float(r["time_sec"]), "end_sec": float(r["time_sec"])+2.0, "category": "tti_positive", "label": f"TTI +{r['tti_timewindow']:.2f}", "source": "tti_timewindow_paired_deltas.csv"})
    for _, r in top_neg.iterrows():
        rows.append({"start_sec": float(r["time_sec"]), "end_sec": float(r["time_sec"])+2.0, "category": "tti_negative", "label": f"TTI {r['tti_timewindow']:.2f}", "source": "tti_timewindow_paired_deltas.csv"})
    pd.DataFrame(rows).to_csv(out_path, index=False)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="PRAYCG TTI v1.4.8 - Reception/Extraction Tradeoff and Thermodynamic Theft Index")
    ap.add_argument("--analysis-folder", required=True, help="Master Comprehensive output folder")
    ap.add_argument("--feature-csv", default="", help="Optional feature CSV override")
    ap.add_argument("--event-table", default="", help="Optional CandidateLocal/MRED event table")
    ap.add_argument("--ocm-cue-epoch-csv", default="", help="Optional OCM/RSM cue epoch table")
    ap.add_argument("--confound-csv", default="", help="Optional branch confound report CSV")
    ap.add_argument("--out-dir", default="", help="Output directory; defaults to <analysis-folder>/tables")
    args = ap.parse_args(argv)

    analysis = Path(args.analysis_folder).resolve()
    out_dir = Path(args.out_dir).resolve() if args.out_dir else (analysis / "tables")
    out_dir.mkdir(parents=True, exist_ok=True)

    feature_path = find_file(analysis, args.feature_csv, FEATURE_PRIORITY, FEATURE_GLOBS)
    event_path = find_file(analysis, args.event_table, EVENT_PRIORITY, ["*candidate*local*kht*.csv", "*mred*event*.csv"])
    ocm_path = find_file(analysis, args.ocm_cue_epoch_csv, OCM_PRIORITY, ["*ocm*cue*epoch*.csv", "*rsm*cue*.csv"])
    conf_path = find_file(analysis, args.confound_csv, CONF_PRIORITY, ["*confound*.csv"])

    if not feature_path:
        raise SystemExit("No feature CSV found. Provide --feature-csv or run Master Suite first.")

    feature_df = safe_read_csv(feature_path)
    if feature_df is None or feature_df.empty:
        raise SystemExit(f"Feature CSV is empty or unreadable: {feature_path}")
    feature_scores, used_cols = build_composite_feature_scores(feature_df)

    component_table, global_summary = compute_global_tti(feature_scores)
    timewindow = compute_timewindow_tti(feature_scores)
    event_df = safe_read_csv(event_path) if event_path else None
    event_summary = compute_event_tti(event_df)
    ocm_df = safe_read_csv(ocm_path) if ocm_path else None
    ocm_summary = add_ocm_extraction(feature_scores, ocm_df)

    # Add optional confound summary.
    conf_df = safe_read_csv(conf_path) if conf_path else None
    conf_summary = pd.DataFrame()
    if conf_df is not None and not conf_df.empty:
        conf_summary = conf_df.copy()

    component_table.to_csv(out_dir / "tti_component_summary.csv", index=False)
    pd.DataFrame([global_summary]).to_csv(out_dir / "tti_global_summary.csv", index=False)
    timewindow.to_csv(out_dir / "tti_timewindow_paired_deltas.csv", index=False)
    event_summary.to_csv(out_dir / "tti_event_summary.csv", index=False)
    ocm_summary.to_csv(out_dir / "tti_ocm_extraction_summary.csv", index=False)
    if not conf_summary.empty:
        conf_summary.to_csv(out_dir / "tti_confound_context.csv", index=False)
    overlay_from_timewindows(timewindow, out_dir / "tti_visual_overlay.csv")

    interp = {
        "schema": "PRAYCG_TTI_v1_4_8_interpretation",
        "version": VERSION,
        "analysis_folder": str(analysis),
        "feature_csv": str(feature_path),
        "event_table": str(event_path) if event_path else "",
        "ocm_cue_epoch_csv": str(ocm_path) if ocm_path else "",
        "confound_csv": str(conf_path) if conf_path else "",
        "used_columns": used_cols,
        "global_summary": global_summary,
        "interpretation_boundary": "TTI estimates the Target-vs-Override reception/extraction tradeoff. It is not a moral score, clinical metric, proof of consciousness, or proof of OSM biology.",
        "claim_rules": [
            "Positive TTI suggests Target preserved more receptive meaning/integration than Override while Override carried greater extractive/task load.",
            "TTI does not imply total meaning erasure; Override may preserve semantic recognition while reducing integration/afterglow/carryover.",
            "Artifact, visual drive, audio-video sync, cue legibility, respiration, and self-report consistency must be reviewed before interpretive claims.",
            "Runner-registered anchors are required for strict confirmatory anchor language. Conceptual predeclaration is weaker than machine-registered predeclaration.",
        ],
    }
    (out_dir / "tti_interpretation.json").write_text(json.dumps(interp, indent=2), encoding="utf-8")
    print(json.dumps(interp, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
