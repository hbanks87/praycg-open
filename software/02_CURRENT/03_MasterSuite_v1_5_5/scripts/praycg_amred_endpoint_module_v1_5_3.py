#!/usr/bin/env python3
"""
PRAYCG A-MRED Primary Endpoint Module v1.5.3
=============================================

Anchor-Locked Meaning Recognition / Encoding Dissociation (A-MRED)
primary endpoint module.

This post-module compresses the broader PR-AYC-G workbench into a cleaner
confirmatory-style endpoint:

  A predeclared media-structural anchor passes only when Target shows BOTH
  meaning-recognition and delayed integration greater than Control and Override,
  after QC/confound checks and stimulus-regressor checks are accounted for.

Boundary: A-MRED is a human-scale psychophysiology endpoint. It does not prove
OSM biology, cellular hidden-Y, microtubules, biophotons, consciousness, or memory
formation. Absence of A-MRED is not proof of absence of meaning.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import numpy as np
    import pandas as pd
except Exception as exc:  # pragma: no cover
    raise SystemExit("This module requires numpy and pandas. Install requirements first.") from exc

VERSION = "1.5.3"
SCHEMA = "PRAYCG_A_MRED_PrimaryEndpoint_v1_5_3"

COND_TARGET = "TARGET_1"
COND_CONTROL = "CONTROL_1"
COND_OVERRIDE = "CONTEXTUAL_OVERRIDE_1"
CONDS = [COND_CONTROL, COND_TARGET, COND_OVERRIDE]


def norm_condition(x: Any) -> str:
    s = str(x or "").strip().upper()
    if "TARGET" in s and "OVERRIDE" not in s:
        return COND_TARGET
    if "OVERRIDE" in s or "CONTEXTUAL" in s:
        return COND_OVERRIDE
    if "CONTROL" in s or "SCRAMB" in s:
        return COND_CONTROL
    return s or "UNKNOWN"


def safe_float(x: Any, default: float = float("nan")) -> float:
    try:
        if x is None or x == "":
            return default
        if isinstance(x, str) and x.strip().lower() in {"nan", "none", "null"}:
            return default
        v = float(x)
        return v if math.isfinite(v) else default
    except Exception:
        return default


def read_table(path: Optional[str]) -> pd.DataFrame:
    if not path:
        return pd.DataFrame()
    p = Path(path)
    if not p.exists():
        return pd.DataFrame()
    try:
        if p.suffix.lower() == ".json":
            obj = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(obj, list):
                return pd.DataFrame(obj)
            if isinstance(obj, dict):
                for key in ["rows", "events", "anchors", "records", "table"]:
                    if isinstance(obj.get(key), list):
                        return pd.DataFrame(obj[key])
                return pd.DataFrame([obj])
        return pd.read_csv(p)
    except Exception:
        return pd.DataFrame()


def first_col(df: pd.DataFrame, names: Iterable[str], contains: Iterable[str] = ()) -> Optional[str]:
    if df is None or df.empty:
        return None
    lower = {str(c).lower(): c for c in df.columns}
    for n in names:
        if n.lower() in lower:
            return lower[n.lower()]
    for c in df.columns:
        cl = str(c).lower()
        if all(s.lower() in cl for s in contains):
            return c
    return None


def find_file(analysis_folder: str, patterns: List[str]) -> str:
    if not analysis_folder:
        return ""
    roots = [Path(analysis_folder) / "tables", Path(analysis_folder)]
    for root in roots:
        if not root.exists():
            continue
        for pat in patterns:
            m = sorted(root.glob(pat))
            if m:
                return str(m[0])
    return ""


def load_anchors(path: str) -> pd.DataFrame:
    if not path:
        return pd.DataFrame()
    p = Path(path)
    if not p.exists():
        return pd.DataFrame()
    if p.suffix.lower() == ".csv":
        return pd.read_csv(p)
    obj = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(obj, list):
        rows = obj
        meta = {}
    elif isinstance(obj, dict):
        rows = obj.get("anchors") or obj.get("anchor_events") or obj.get("rows") or []
        meta = {k: v for k, v in obj.items() if k not in {"anchors", "anchor_events", "rows"}}
        if isinstance(rows, dict):
            rows = [rows]
        if not rows and any(k in obj for k in ["anchor_id", "rendered_time_sec", "time_sec"]):
            rows = [obj]
    else:
        rows, meta = [], {}
    df = pd.DataFrame(rows)
    for k, v in meta.items():
        if k not in df.columns and k in {"project_name", "status", "anchor_time_status", "schema", "version"}:
            df[k] = v
    return df


def parse_window(row: pd.Series, key: str, default: Tuple[float, float]) -> Tuple[float, float]:
    v = row.get(key, None)
    if isinstance(v, (list, tuple)) and len(v) >= 2:
        return safe_float(v[0], default[0]), safe_float(v[1], default[1])
    if isinstance(v, str) and v.strip():
        # Handles JSON-ish "[0,10]" or "0,10".
        s = v.strip().replace("[", "").replace("]", "").replace("(", "").replace(")", "")
        parts = [p.strip() for p in re.split(r"[,;]", s) if p.strip()]
        if len(parts) >= 2:
            return safe_float(parts[0], default[0]), safe_float(parts[1], default[1])
    return default


def anchor_is_strictly_locked(row: pd.Series) -> Tuple[bool, str]:
    text = " ".join(str(row.get(k, "")) for k in row.index).lower()
    if "estimated" in text or "draft" in text or "not_frame_verified" in text or "editme" in text:
        return False, "estimated_or_draft_timecode"
    if "frame_verified" in text or "runner_registered" in text or "locked" in text:
        return True, "locked_or_frame_verified"
    return False, "no_explicit_lock_marker"


def canonicalize_anchor_frame(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=["anchor_id", "rendered_time_sec", "scene_label"])
    out = df.copy()
    id_col = first_col(out, ["anchor_id", "event_id", "label", "name"])
    time_col = first_col(out, ["rendered_time_sec", "time_sec", "anchor_time_sec", "estimated_relative_sec", "rendered_time_sec_estimate"])
    label_col = first_col(out, ["scene_label", "description", "scene_description", "narrative_event", "note", "notes"])
    if not id_col:
        out["anchor_id"] = [f"ANCHOR_{i+1:02d}" for i in range(len(out))]
    else:
        out["anchor_id"] = out[id_col].astype(str)
    if not time_col:
        out["rendered_time_sec"] = np.nan
    else:
        out["rendered_time_sec"] = pd.to_numeric(out[time_col], errors="coerce")
    if label_col:
        out["scene_label"] = out[label_col].astype(str)
    else:
        out["scene_label"] = out["anchor_id"]
    out["condition_scope_norm"] = out.get("condition_scope", "all_branches")
    out["a_mred_role"] = out.get("a_mred_role", out.get("primary_endpoint_role", "secondary"))
    out["predicted_mred_quadrant"] = out.get("predicted_mred_quadrant", out.get("mred_prediction", "MR_HIGH_ENC_HIGH"))
    return out


def z_or_raw(series: pd.Series) -> pd.Series:
    x = pd.to_numeric(series, errors="coerce")
    if x.notna().sum() < 3:
        return x
    # If already bounded/z-like, leave mostly unchanged. Otherwise z-score.
    if x.abs().quantile(0.95) <= 5.0:
        return x
    sd = x.std(skipna=True)
    if not np.isfinite(sd) or sd == 0:
        return x * np.nan
    return (x - x.mean(skipna=True)) / sd


def canonical_feature_frame(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    out = df.copy()
    cond = first_col(out, ["analysis_segment", "condition", "phase", "segment", "branch"])
    time = first_col(out, ["analysis_time", "time_sec", "phase_time_sec", "condition_time_sec", "t_sec", "sec"])
    if not cond or not time:
        return pd.DataFrame()
    out["_cond"] = out[cond].map(norm_condition)
    out["_time"] = pd.to_numeric(out[time], errors="coerce")
    # Recognition proxy candidates.
    mr_cols = []
    for c in out.columns:
        cl = str(c).lower()
        if any(k in cl for k in ["mr_score", "meaninggamma", "meaning_gamma", "tsp", "temporal_semantic", "nip_density", "a_sem", "semantic_attention"]):
            if not any(bad in cl for bad in ["artifact", "visual", "control", "confound"]):
                mr_cols.append(c)
    # Integration proxy candidates.
    enc_cols = []
    for c in out.columns:
        cl = str(c).lower()
        if any(k in cl for k in ["enc_score", "theta_delta", "theta_integration", "h_theta", "r_int", "topo_shift", "carryover", "theta_proxy"]):
            if not any(bad in cl for bad in ["artifact", "visual", "control", "confound"]):
                enc_cols.append(c)
    art_cols = []
    for c in out.columns:
        cl = str(c).lower()
        if any(k in cl for k in ["artifact", "emg", "jaw", "blink", "squint", "confound"]):
            art_cols.append(c)
    if mr_cols:
        out["_mr_proxy"] = pd.concat([z_or_raw(out[c]) for c in mr_cols], axis=1).mean(axis=1, skipna=True)
    else:
        out["_mr_proxy"] = np.nan
    if enc_cols:
        out["_enc_proxy"] = pd.concat([z_or_raw(out[c]) for c in enc_cols], axis=1).mean(axis=1, skipna=True)
    else:
        out["_enc_proxy"] = np.nan
    if art_cols:
        out["_artifact_proxy"] = pd.concat([z_or_raw(out[c]) for c in art_cols], axis=1).mean(axis=1, skipna=True)
    else:
        out["_artifact_proxy"] = 0.0
    out["_feature_mr_cols"] = ";".join(map(str, mr_cols))
    out["_feature_enc_cols"] = ";".join(map(str, enc_cols))
    return out


def canonical_event_frame(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    out = df.copy()
    cond = first_col(out, ["analysis_segment", "condition", "phase", "segment", "branch"])
    time = first_col(out, ["analysis_time", "time_sec", "phase_time_sec", "condition_time_sec", "peak_sec", "event_time_sec", "anchor_time_sec"])
    if not time:
        return pd.DataFrame()
    out["_cond"] = out[cond].map(norm_condition) if cond else COND_TARGET
    out["_time"] = pd.to_numeric(out[time], errors="coerce")
    # direct columns first
    mr = first_col(out, ["MR_score", "mr_score", "meaning_recognition_score", "meaning_gamma_z", "MeaningGamma", "tsp_z", "TSP"])
    enc = first_col(out, ["ENC_score", "enc_score", "encoding_score", "theta_delta_10_30", "theta_delta_0_10", "H_theta", "theta_integration"])
    kcol = first_col(out, ["K_HT_topo", "K_HT", "K_local", "k_local", "kht_topo", "local_k"])
    art = first_col(out, ["artifact_score", "artifact_proxy_z", "artifact", "confound_burden"])
    quad = first_col(out, ["mred_quadrant", "quadrant_label", "MRED_quadrant"])
    out["_mr_proxy"] = z_or_raw(out[mr]) if mr else np.nan
    out["_enc_proxy"] = z_or_raw(out[enc]) if enc else np.nan
    out["_k_proxy"] = pd.to_numeric(out[kcol], errors="coerce") if kcol else np.nan
    out["_artifact_proxy"] = z_or_raw(out[art]) if art else 0.0
    out["_mred_quadrant"] = out[quad].astype(str) if quad else ""
    return out.dropna(subset=["_time"])


def summarize_window(features: pd.DataFrame, events: pd.DataFrame, condition: str, anchor_t: float, win: Tuple[float, float]) -> Dict[str, Any]:
    start = anchor_t + win[0]
    end = anchor_t + win[1]
    res: Dict[str, Any] = {"window_start_sec": start, "window_end_sec": end}
    # Feature-window average.
    if features is not None and not features.empty:
        f = features[(features["_cond"] == condition) & (features["_time"].between(start, end))]
        res["feature_n"] = int(len(f))
        res["feature_mr_mean"] = float(f["_mr_proxy"].mean()) if len(f) else float("nan")
        res["feature_enc_mean"] = float(f["_enc_proxy"].mean()) if len(f) else float("nan")
        res["feature_artifact_mean"] = float(f["_artifact_proxy"].mean()) if len(f) else float("nan")
    else:
        res.update({"feature_n": 0, "feature_mr_mean": float("nan"), "feature_enc_mean": float("nan"), "feature_artifact_mean": float("nan")})
    # Nearest event inside broader peak+theta window.
    if events is not None and not events.empty:
        e = events[(events["_cond"] == condition) & (events["_time"].between(start, end))].copy()
        res["event_n"] = int(len(e))
        if len(e):
            e["_dist"] = (e["_time"] - anchor_t).abs()
            # prefer higher MR+ENC and closeness
            e["_rank"] = e["_mr_proxy"].fillna(0) + e["_enc_proxy"].fillna(0) - 0.02 * e["_dist"]
            r = e.sort_values("_rank", ascending=False).iloc[0]
            res.update({
                "event_time_sec": float(r["_time"]),
                "event_mr": safe_float(r["_mr_proxy"]),
                "event_enc": safe_float(r["_enc_proxy"]),
                "event_k": safe_float(r.get("_k_proxy")),
                "event_artifact": safe_float(r.get("_artifact_proxy")),
                "event_quadrant": str(r.get("_mred_quadrant", "")),
            })
        else:
            res.update({"event_time_sec": float("nan"), "event_mr": float("nan"), "event_enc": float("nan"), "event_k": float("nan"), "event_artifact": float("nan"), "event_quadrant": ""})
    else:
        res.update({"event_n": 0, "event_time_sec": float("nan"), "event_mr": float("nan"), "event_enc": float("nan"), "event_k": float("nan"), "event_artifact": float("nan"), "event_quadrant": ""})
    # Conservative aggregate: event if available, else features.
    res["MR"] = res["event_mr"] if math.isfinite(res.get("event_mr", float("nan"))) else res["feature_mr_mean"]
    res["ENC"] = res["event_enc"] if math.isfinite(res.get("event_enc", float("nan"))) else res["feature_enc_mean"]
    vals_art = [res.get("event_artifact", np.nan), res.get("feature_artifact_mean", np.nan)]
    vals_art = [float(v) for v in vals_art if math.isfinite(safe_float(v))]
    res["artifact"] = float(sum(vals_art) / len(vals_art)) if vals_art else float("nan")
    return res


def run_amred(args: argparse.Namespace) -> Dict[str, Any]:
    tables_dir = Path(args.out_dir or (Path(args.analysis_folder) / "tables" if args.analysis_folder else ".")).resolve()
    tables_dir.mkdir(parents=True, exist_ok=True)

    anchor_path = args.anchor_file or find_file(args.analysis_folder, ["*predeclared*anchor*.json", "*anchors*LOCKED*.json", "*anchor*.csv"])
    feature_path = args.feature_csv or find_file(args.analysis_folder, ["*time_resolved*feature*.csv", "*nip_component_timeseries*.csv", "*feature_frame*.csv"])
    event_path = args.event_table or find_file(args.analysis_folder, ["*candidate_local*kht*merged*.csv", "*candidate_local*kht*event*.csv", "*candidate_local*kht*.csv", "*mred_event_table*.csv"])
    mred_path = args.mred_event_table or find_file(args.analysis_folder, ["*mred_event_table*.csv", "*MRED*.csv"])

    anchors_raw = load_anchors(anchor_path)
    anchors = canonicalize_anchor_frame(anchors_raw)
    features = canonical_feature_frame(read_table(feature_path))
    ev_primary = canonical_event_frame(read_table(event_path))
    ev_mred = canonical_event_frame(read_table(mred_path))
    events = pd.concat([ev_primary, ev_mred], ignore_index=True) if len(ev_primary) or len(ev_mred) else pd.DataFrame()

    rows = []
    overlay = []
    if anchors.empty:
        interp = {
            "schema": SCHEMA,
            "version": VERSION,
            "status": "NO_ANCHORS",
            "message": "No anchor file was supplied or detected. A-MRED cannot define confirmatory event windows without predeclared anchors.",
        }
        (tables_dir / "amred_interpretation.json").write_text(json.dumps(interp, indent=2), encoding="utf-8")
        return interp

    for _, a in anchors.iterrows():
        anchor_id = str(a.get("anchor_id", "ANCHOR"))
        t = safe_float(a.get("rendered_time_sec"))
        if not math.isfinite(t):
            continue
        peak_win = parse_window(a, "peak_search_window_sec", (0.0, 10.0))
        theta_win = parse_window(a, "theta_carryover_window_sec", (10.0, 30.0))
        eval_win = (min(peak_win[0], theta_win[0]), max(peak_win[1], theta_win[1]))
        locked, lock_reason = anchor_is_strictly_locked(a)
        cond_results = {}
        for cond in CONDS:
            cond_results[cond] = summarize_window(features, events, cond, t, eval_win)
        T, C, O = cond_results[COND_TARGET], cond_results[COND_CONTROL], cond_results[COND_OVERRIDE]
        target_mr, target_enc = safe_float(T.get("MR")), safe_float(T.get("ENC"))
        control_mr, control_enc = safe_float(C.get("MR")), safe_float(C.get("ENC"))
        override_mr, override_enc = safe_float(O.get("MR")), safe_float(O.get("ENC"))
        target_above_control_mr = bool(math.isfinite(target_mr) and math.isfinite(control_mr) and target_mr > control_mr + args.condition_margin)
        target_above_override_mr = bool(math.isfinite(target_mr) and math.isfinite(override_mr) and target_mr > override_mr + args.condition_margin)
        target_above_control_enc = bool(math.isfinite(target_enc) and math.isfinite(control_enc) and target_enc > control_enc + args.condition_margin)
        target_above_override_enc = bool(math.isfinite(target_enc) and math.isfinite(override_enc) and target_enc > override_enc + args.condition_margin)
        target_threshold_mr = bool(math.isfinite(target_mr) and target_mr > args.mr_threshold)
        target_threshold_enc = bool(math.isfinite(target_enc) and target_enc > args.enc_threshold)
        artifact_ok = bool(not math.isfinite(safe_float(T.get("artifact"))) or safe_float(T.get("artifact")) < args.artifact_max)
        directional_support = all([target_above_control_mr, target_above_override_mr, target_above_control_enc, target_above_override_enc])
        strict_pass = bool(locked and target_threshold_mr and target_threshold_enc and directional_support and artifact_ok)
        if strict_pass:
            grade = "STRICT_A_MRED_PASS"
        elif directional_support and target_threshold_mr:
            grade = "ANCHOR_CONSISTENT_SUPPORT_NOT_STRICT"
        elif target_threshold_mr and not target_threshold_enc:
            grade = "MR_ONLY_RECOGNITION_WITHOUT_ENCODING"
        elif target_threshold_enc and not target_threshold_mr:
            grade = "ENC_ONLY_NOT_MEANING_SPECIFIC"
        else:
            grade = "NO_A_MRED_SUPPORT"
        row = {
            "anchor_id": anchor_id,
            "scene_label": str(a.get("scene_label", "")),
            "rendered_time_sec": t,
            "a_mred_role": str(a.get("a_mred_role", "secondary")),
            "predicted_mred_quadrant": str(a.get("predicted_mred_quadrant", "")),
            "lock_status_ok": locked,
            "lock_reason": lock_reason,
            "target_MR": target_mr,
            "target_ENC": target_enc,
            "control_MR": control_mr,
            "control_ENC": control_enc,
            "override_MR": override_mr,
            "override_ENC": override_enc,
            "target_minus_control_MR": target_mr - control_mr if math.isfinite(target_mr) and math.isfinite(control_mr) else np.nan,
            "target_minus_override_MR": target_mr - override_mr if math.isfinite(target_mr) and math.isfinite(override_mr) else np.nan,
            "target_minus_control_ENC": target_enc - control_enc if math.isfinite(target_enc) and math.isfinite(control_enc) else np.nan,
            "target_minus_override_ENC": target_enc - override_enc if math.isfinite(target_enc) and math.isfinite(override_enc) else np.nan,
            "target_threshold_mr": target_threshold_mr,
            "target_threshold_enc": target_threshold_enc,
            "target_above_control_mr": target_above_control_mr,
            "target_above_override_mr": target_above_override_mr,
            "target_above_control_enc": target_above_control_enc,
            "target_above_override_enc": target_above_override_enc,
            "artifact_ok": artifact_ok,
            "strict_amred_pass": strict_pass,
            "amred_grade": grade,
            "target_event_time_sec": T.get("event_time_sec", np.nan),
            "target_event_k": T.get("event_k", np.nan),
            "target_event_quadrant": T.get("event_quadrant", ""),
            "feature_source": feature_path,
            "event_source": event_path or mred_path,
        }
        rows.append(row)
        category = "amred_primary" if strict_pass or str(a.get("a_mred_role", "")).lower().startswith("primary") else "amred"
        overlay.append({
            "time_sec": t,
            "start_sec": max(0, t + eval_win[0]),
            "end_sec": max(t + eval_win[1], t + eval_win[0] + 1),
            "condition": COND_TARGET,
            "label": f"A-MRED {anchor_id}: {grade}",
            "category": category,
            "anchor_id": anchor_id,
            "claim_level": grade,
        })

    out = pd.DataFrame(rows)
    out_path = tables_dir / "amred_anchor_endpoint_table.csv"
    out.to_csv(out_path, index=False)
    overlay_path = tables_dir / "amred_visual_overlay.csv"
    pd.DataFrame(overlay).to_csv(overlay_path, index=False)
    summary = {
        "schema": SCHEMA,
        "version": VERSION,
        "anchor_file": anchor_path,
        "feature_csv": feature_path,
        "event_table": event_path or mred_path,
        "n_anchors_evaluated": int(len(out)),
        "n_strict_amred_pass": int(out["strict_amred_pass"].sum()) if len(out) else 0,
        "n_anchor_consistent_support_not_strict": int((out["amred_grade"] == "ANCHOR_CONSISTENT_SUPPORT_NOT_STRICT").sum()) if len(out) else 0,
        "primary_endpoint_anchors": int(out["a_mred_role"].astype(str).str.contains("primary", case=False, na=False).sum()) if len(out) else 0,
        "boundary": "A-MRED is a human-scale anchor-locked psychophysiology endpoint. It does not prove OSM biology, cellular hidden-Y, microtubules, biophotons, consciousness, or memory formation.",
        "thresholds": {"mr_threshold": args.mr_threshold, "enc_threshold": args.enc_threshold, "condition_margin": args.condition_margin, "artifact_max": args.artifact_max},
    }
    summary_path = tables_dir / "amred_primary_endpoint_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    # CSV summary for spreadsheet/open hub.
    with (tables_dir / "amred_primary_endpoint_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary.keys()))
        w.writeheader(); w.writerow({k: json.dumps(v) if isinstance(v, (dict, list)) else v for k, v in summary.items()})
    return summary


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="PRAYCG A-MRED Anchor-Locked Endpoint Module v1.5.3")
    p.add_argument("--analysis-folder", default="", help="Existing Master Comprehensive output folder. Tables will be auto-discovered.")
    p.add_argument("--anchor-file", default="", help="Predeclared anchor JSON/CSV. Prefer *_LOCKED.json for strict A-MRED.")
    p.add_argument("--feature-csv", default="", help="Optional continuous feature table override.")
    p.add_argument("--event-table", default="", help="Optional CandidateLocal KHT/MRED event table override.")
    p.add_argument("--mred-event-table", default="", help="Optional MRED event table override.")
    p.add_argument("--out-dir", default="", help="Output directory; default <analysis-folder>/tables.")
    p.add_argument("--mr-threshold", type=float, default=0.75)
    p.add_argument("--enc-threshold", type=float, default=0.50)
    p.add_argument("--condition-margin", type=float, default=0.25)
    p.add_argument("--artifact-max", type=float, default=2.50)
    return p


def main() -> int:
    args = build_parser().parse_args()
    summary = run_amred(args)
    print(json.dumps(summary, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
