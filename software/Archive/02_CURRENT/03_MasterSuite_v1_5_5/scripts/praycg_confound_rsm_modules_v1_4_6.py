#!/usr/bin/env python3
"""
PRAYCG Master Comprehensive Suite v1.4.6
Confound-aware presentation, cue-legibility, running-sum, and audio/noise modules.

Modules formalized here:
  - RSM_v0.1: Running Sum Microstate Model
  - CVB_v0.1: Cue Visibility / Legibility Burden
  - SquintProxy_v0.1: forehead/Fp1-derived visual-strain proxy, if available
  - AVSyncConfound_v0.1: subjective and/or measured audio-video desynchrony covariate
  - ExternalAcousticIntrusion_v0.1: train/noise/speaker masking covariate

Boundary: these modules do not certify meaning, OSM, hidden-Y biology, or squinting.
They generate covariates, veto flags, and exploratory overlays for PR-AYC-G analysis.
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
except Exception:  # pragma: no cover
    np = None
try:
    import pandas as pd
except Exception as exc:  # pragma: no cover
    raise RuntimeError("pandas is required for v1.4.6 confound/RSM modules") from exc

VERSION = "1.4.6"


def robust_z(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    med = s.median(skipna=True)
    mad = (s - med).abs().median(skipna=True)
    denom = 1.4826 * mad
    if not math.isfinite(float(denom)) or denom <= 1e-12:
        std = s.std(skipna=True)
        denom = std if math.isfinite(float(std)) and std > 1e-12 else 1.0
    return (s - med) / denom


def sigmoid(x: pd.Series) -> pd.Series:
    x = pd.to_numeric(x, errors="coerce").fillna(0.0).clip(-12, 12)
    return 1.0 / (1.0 + (-x).map(math.exp))


def load_json_or_csv_events(path: str) -> List[Dict[str, Any]]:
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        return []
    if p.suffix.lower() == ".json":
        obj = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(obj, list):
            return [dict(x) for x in obj if isinstance(x, dict)]
        if isinstance(obj, dict) and isinstance(obj.get("events"), list):
            return [dict(x) for x in obj["events"] if isinstance(x, dict)]
        return []
    rows: List[Dict[str, Any]] = []
    with p.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


def parse_json_note(note: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(note, str):
        return None
    s = note.strip()
    if not s.startswith("{"):
        return None
    try:
        obj = json.loads(s)
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None


def extract_praycg19_confound_reports(events: List[Dict[str, Any]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    branch_rows: List[Dict[str, Any]] = []
    calibration_rows: List[Dict[str, Any]] = []
    for ev in events:
        marker = str(ev.get("marker", ""))
        note = ev.get("note", "")
        obj = parse_json_note(note)
        if not obj:
            continue
        schema = str(obj.get("schema", ""))
        if schema == "PRAYCG1_9_branch_confound_report_v1" or ("CONFOUND_REPORT" in marker and "ratings" in obj):
            base = {
                "event_marker": marker,
                "event_phase": ev.get("phase", obj.get("phase_name", "")),
                "lsl_time": ev.get("lsl_time", ""),
                "phase_name": obj.get("phase_name", ""),
                "branch_label": obj.get("branch_label", ""),
                "is_override": obj.get("is_override", False),
            }
            ratings = obj.get("ratings", {}) if isinstance(obj.get("ratings"), dict) else {}
            notes = obj.get("notes", {}) if isinstance(obj.get("notes"), dict) else {}
            for k, v in ratings.items():
                base[k] = v
            for k, v in notes.items():
                base[f"note_{k}"] = v
            branch_rows.append(base)
        elif schema == "PRAYCG1_9_prerun_display_audio_calibration_v1" or "PRERUN_DISPLAY_AUDIO_CALIBRATION_END" in marker:
            base = {"event_marker": marker, "event_phase": ev.get("phase", ""), "lsl_time": ev.get("lsl_time", "")}
            ratings = obj.get("ratings", {}) if isinstance(obj.get("ratings"), dict) else {}
            for k, v in ratings.items():
                base[k] = v
            base["notes"] = obj.get("notes", "")
            calibration_rows.append(base)
    return pd.DataFrame(branch_rows), pd.DataFrame(calibration_rows)


def load_cue_schedule(path: str) -> pd.DataFrame:
    if not path:
        return pd.DataFrame()
    p = Path(path)
    if not p.exists():
        return pd.DataFrame()
    if p.suffix.lower() == ".json":
        obj = json.loads(p.read_text(encoding="utf-8"))
        cues = obj.get("cue_events", []) if isinstance(obj, dict) else []
        rows = []
        running = 0
        for c in cues:
            if not isinstance(c, dict):
                continue
            val = int(c.get("value", c.get("cue_value", 0)))
            prev = running
            running += val
            row = dict(c)
            row.setdefault("cue_index", c.get("index", len(rows) + 1))
            row.setdefault("cue_value", val)
            row["value"] = val
            row["running_sum_prev"] = prev
            row["running_sum_after"] = running
            rows.append(row)
        return pd.DataFrame(rows)
    df = pd.read_csv(p)
    if "value" not in df.columns and "cue_value" in df.columns:
        df["value"] = df["cue_value"]
    if "cue_value" not in df.columns and "value" in df.columns:
        df["cue_value"] = df["value"]
    if "cue_index" not in df.columns:
        df["cue_index"] = range(1, len(df) + 1)
    running = []
    prevs = []
    cur = 0
    for v in pd.to_numeric(df["cue_value"], errors="coerce").fillna(0).astype(int):
        prevs.append(cur)
        cur += int(v)
        running.append(cur)
    df["running_sum_prev"] = prevs
    df["running_sum_after"] = running
    return df


def load_optional_csv(path: str) -> pd.DataFrame:
    if path and Path(path).exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def find_first_existing(roots: Iterable[Path], names: Iterable[str], patterns: Iterable[str]) -> str:
    for root in roots:
        if not root or not root.exists():
            continue
        for name in names:
            p = root / name
            if p.exists() and p.is_file():
                return str(p)
        for pat in patterns:
            hits = sorted(root.glob(pat))
            if hits:
                return str(hits[0])
    return ""


def build_rsm_cvb_table(cues: pd.DataFrame, ocm: pd.DataFrame) -> pd.DataFrame:
    if cues.empty and ocm.empty:
        return pd.DataFrame()
    if cues.empty:
        df = ocm.copy()
        if "cue_value" not in df.columns and "value" in df.columns:
            df["cue_value"] = df["value"]
    elif ocm.empty:
        df = cues.copy()
    else:
        left = ocm.copy()
        right = cues.copy()
        if "cue_value" not in right.columns and "value" in right.columns:
            right["cue_value"] = right["value"]
        join_cols = ["cue_index"]
        if "phase" in left.columns and "phase" in right.columns:
            join_cols = ["phase", "cue_index"]
        keep_cols = [c for c in right.columns if c not in left.columns or c in join_cols]
        df = left.merge(right[keep_cols], on=join_cols, how="left")
    if "cue_value" not in df.columns and "value" in df.columns:
        df["cue_value"] = df["value"]
    df["cue_value"] = pd.to_numeric(df.get("cue_value", 0), errors="coerce").fillna(0).astype(int)
    if "running_sum_prev" not in df.columns:
        # compute within phase when possible; otherwise global cue order
        df = df.sort_values([c for c in ["phase", "cue_index"] if c in df.columns])
        prevs = []
        afters = []
        for _phase, g in df.groupby("phase") if "phase" in df.columns else [(None, df)]:
            running = 0
            for idx, row in g.iterrows():
                prevs.append((idx, running))
                running += int(row["cue_value"])
                afters.append((idx, running))
        prev_series = pd.Series({i: v for i, v in prevs})
        after_series = pd.Series({i: v for i, v in afters})
        df["running_sum_prev"] = df.index.map(prev_series).fillna(0)
        df["running_sum_after"] = df.index.map(after_series).fillna(df["cue_value"])
    df["running_sum_prev"] = pd.to_numeric(df["running_sum_prev"], errors="coerce").fillna(0)
    df["running_sum_after"] = pd.to_numeric(df.get("running_sum_after", df["running_sum_prev"] + df["cue_value"]), errors="coerce").fillna(df["running_sum_prev"] + df["cue_value"])
    df["prior_units_digit"] = (df["running_sum_prev"].astype(int) % 10).astype(int)
    df["carry_required"] = ((df["prior_units_digit"] + df["cue_value"]) >= 10).astype(int)
    df["high_carry_load"] = (df["prior_units_digit"] + df["cue_value"] - 9).clip(lower=0)
    df["hard9_personal_pattern"] = ((df["cue_value"] == 9) & (df["prior_units_digit"].isin([7, 8, 9]))).astype(int)
    # Objective arithmetic load from running sum magnitude, carry, high carry, hard9.
    df["log_running_sum_prev"] = (df["running_sum_prev"].clip(lower=0) + 1).map(math.log)
    df["arithmetic_compute_load_raw"] = (
        robust_z(df["log_running_sum_prev"]).fillna(0) +
        0.75 * df["carry_required"].fillna(0) +
        0.10 * df["high_carry_load"].fillna(0) +
        0.75 * df["hard9_personal_pattern"].fillna(0)
    )
    df["arithmetic_compute_load_z"] = robust_z(df["arithmetic_compute_load_raw"])

    # Normalize common OCM fields across previous table versions.
    if "WMU_frontaltheta_4_8" not in df.columns and "WMU_tasktheta_4_8" in df.columns:
        df["WMU_frontaltheta_4_8"] = df["WMU_tasktheta_4_8"]
    if "MAINT_tasktheta_4_8" not in df.columns and "MAINT_tasktheta_4_8_z" in df.columns:
        df["MAINT_tasktheta_4_8"] = df["MAINT_tasktheta_4_8_z"]
    for col in ["DR_taskgamma_35_40", "WMU_frontaltheta_4_8", "MAINT_tasktheta_4_8", "DR_visualgamma_30_45", "mean_artifact_score", "OCM_score"]:
        if col not in df.columns:
            df[col] = 0.0
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[f"{col}_z_v146"] = robust_z(df[col]).fillna(0)

    df["hold_burden_v146"] = (
        0.45 * df["WMU_frontaltheta_4_8_z_v146"] +
        0.35 * df["MAINT_tasktheta_4_8_z_v146"] +
        0.20 * df["OCM_score_z_v146"] -
        0.20 * df["mean_artifact_score_z_v146"].clip(lower=0)
    )
    df["cue_visibility_burden_v146"] = (
        0.50 * robust_z(df["hold_burden_v146"]).fillna(0) -
        0.25 * df["DR_taskgamma_35_40_z_v146"] +
        0.15 * df["DR_visualgamma_30_45_z_v146"] -
        0.20 * df["mean_artifact_score_z_v146"].clip(lower=0)
    )
    df["compute_stall_score_v146"] = (
        0.45 * df["WMU_frontaltheta_4_8_z_v146"] +
        0.30 * df["MAINT_tasktheta_4_8_z_v146"] +
        0.35 * df["arithmetic_compute_load_z"] +
        0.15 * df["DR_taskgamma_35_40_z_v146"] -
        0.20 * df["cue_visibility_burden_v146"].clip(lower=0) -
        0.20 * df["mean_artifact_score_z_v146"].clip(lower=0)
    )
    df["latent_guess_risk_v146"] = sigmoid(
        0.65 * robust_z(df["compute_stall_score_v146"]).fillna(0) +
        0.40 * df["arithmetic_compute_load_z"].fillna(0) +
        0.35 * df["cue_visibility_burden_v146"].fillna(0) +
        0.30 * df["high_carry_load"].fillna(0) -
        0.20 * df["DR_taskgamma_35_40_z_v146"].fillna(0)
    )

    # Fp1/squint proxy if columns are present.
    squint_cols = [c for c in [
        "squint_fp1_hf20_45_rec_delta", "squint_fp1_hf20_45_upd_delta",
        "squint_fp1_hf45_55_rec_delta", "squint_fp1_p2p_rec_delta",
        "squint_fp1_p2p_upd_delta", "frontal_strain_hf_delta",
    ] if c in df.columns]
    if squint_cols:
        zsum = pd.Series(0.0, index=df.index)
        for c in squint_cols:
            zsum += robust_z(df[c]).fillna(0)
        df["squint_proxy_score_v146"] = zsum / max(1, len(squint_cols))
    else:
        df["squint_proxy_score_v146"] = pd.NA
    df["possible_squint_candidate_v146"] = False
    if df["squint_proxy_score_v146"].notna().any():
        df["possible_squint_candidate_v146"] = df["squint_proxy_score_v146"] > df["squint_proxy_score_v146"].quantile(0.95)

    def cat(row):
        if pd.notna(row.get("squint_proxy_score_v146")) and bool(row.get("possible_squint_candidate_v146")):
            return "SQUINT_OR_VISUAL_STRAIN_CANDIDATE"
        if row.get("cue_visibility_burden_v146", 0) > 1.25 and row.get("DR_taskgamma_35_40_z_v146", 0) < 0.25:
            return "HARD_TO_RESOLVE_CUE_CANDIDATE"
        if row.get("compute_stall_score_v146", 0) > 1.25 and row.get("arithmetic_compute_load_z", 0) > 0.5:
            return "ARITHMETIC_STALL_CANDIDATE"
        if row.get("latent_guess_risk_v146", 0) > 0.80:
            return "APPROXIMATE_UPDATE_PRESSURE_CANDIDATE"
        return "ORDINARY_OR_LOW_BURDEN"
    df["rsm_cvb_squint_category_v146"] = df.apply(cat, axis=1)
    return df


def build_confound_registry(branch_reports: pd.DataFrame, calibration: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    if not branch_reports.empty:
        for _, r in branch_reports.iterrows():
            phase = r.get("phase_name", r.get("event_phase", ""))
            label = r.get("branch_label", "")
            av = float(pd.to_numeric(pd.Series([r.get("AudioVideoSyncProblem", 0)]), errors="coerce").fillna(0).iloc[0])
            noise = float(pd.to_numeric(pd.Series([r.get("ExternalNoiseIntrusion", 0)]), errors="coerce").fillna(0).iloc[0])
            aud = float(pd.to_numeric(pd.Series([r.get("AudioComprehensionDifficulty", 0)]), errors="coerce").fillna(0).iloc[0])
            cue = float(pd.to_numeric(pd.Series([r.get("CueLegibilityProblem", 0)]), errors="coerce").fillna(0).iloc[0])
            rows.append({
                "phase_name": phase,
                "branch_label": label,
                "avsync_problem_rating": av,
                "external_noise_intrusion_rating": noise,
                "audio_comprehension_difficulty_rating": aud,
                "cue_legibility_problem_rating": cue,
                "analysis_flag": "CONFOUND_CAUTION" if max(av, noise, aud, cue) >= 5 else "LOW_OR_REPORTED_NO_CONFOUND",
                "note_audio_video_sync": r.get("note_audio_video_sync", ""),
                "note_external_noise": r.get("note_external_noise", ""),
                "note_cue_legibility": r.get("note_cue_legibility", ""),
                "note_running_sum": r.get("note_running_sum", ""),
            })
    if calibration.empty:
        return pd.DataFrame(rows)
    for _, r in calibration.iterrows():
        rows.append({
            "phase_name": "PRERUN_DISPLAY_AUDIO_CALIBRATION",
            "branch_label": "pre-run",
            "avsync_problem_rating": "",
            "external_noise_intrusion_rating": "",
            "audio_comprehension_difficulty_rating": "",
            "cue_legibility_problem_rating": "",
            "analysis_flag": "PRERUN_CALIBRATION_REVIEW",
            "note_audio_video_sync": r.get("notes", ""),
            "note_external_noise": "",
            "note_cue_legibility": "",
            "note_running_sum": "",
        })
    return pd.DataFrame(rows)


def build_visual_overlays(rsm: pd.DataFrame, registry: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    rsm_rows = []
    if not rsm.empty:
        # Only include higher burden events, ideally only override cues.
        r = rsm.copy()
        if "phase" in r.columns:
            r = r[r["phase"].astype(str).str.contains("OVERRIDE", case=False, na=False)]
        if "cue_relative_time_sec" in r.columns:
            tcol = "cue_relative_time_sec"
        elif "start_sec" in r.columns:
            tcol = "start_sec"
        else:
            tcol = "cue_index"
        for _, row in r.iterrows():
            cat = str(row.get("rsm_cvb_squint_category_v146", ""))
            risk = float(row.get("latent_guess_risk_v146", 0) or 0)
            if cat == "ORDINARY_OR_LOW_BURDEN" and risk < 0.80:
                continue
            try:
                t = float(row.get(tcol, 0))
            except Exception:
                continue
            label = f"RSM cue {row.get('cue_index','')} {cat} risk={risk:.2f}"
            rsm_rows.append({"start_sec": t, "end_sec": t + 1.5, "label": label, "category": "rsm", "source": "RSM_v0.1"})
    conf_rows = []
    if not registry.empty:
        # Branch-level confounds are qualitative; put them at 0 sec of selected branch for visual reminder.
        for _, row in registry.iterrows():
            if row.get("analysis_flag") == "LOW_OR_REPORTED_NO_CONFOUND":
                continue
            label = f"Confound {row.get('branch_label','')}: {row.get('analysis_flag','')}"
            conf_rows.append({"start_sec": 0.0, "end_sec": 5.0, "label": label, "category": "confound", "source": "confound_registry"})
    return pd.DataFrame(rsm_rows), pd.DataFrame(conf_rows)


def load_manual_confound_json(path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load manual retrospective confound addendum.

    Format:
    {
      "branch_reports": [ {"phase_name": ..., "branch_label": ..., "ratings": {...}, "notes": {...}} ],
      "prerun_calibration": [ {...} ]
    }
    """
    if not path or not Path(path).exists():
        return pd.DataFrame(), pd.DataFrame()
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        return pd.DataFrame(), pd.DataFrame()
    rows = []
    for br in obj.get("branch_reports", []):
        if not isinstance(br, dict):
            continue
        base = {
            "event_marker": "MANUAL_RETROSPECTIVE_CONFOUND",
            "event_phase": br.get("phase_name", ""),
            "lsl_time": "",
            "phase_name": br.get("phase_name", ""),
            "branch_label": br.get("branch_label", ""),
            "is_override": br.get("is_override", False),
            "manual_retrospective": True,
            "claim_level": br.get("claim_level", "manual_caution"),
        }
        ratings = br.get("ratings", {}) if isinstance(br.get("ratings"), dict) else {}
        notes = br.get("notes", {}) if isinstance(br.get("notes"), dict) else {}
        for k, v in ratings.items():
            base[k] = v
        for k, v in notes.items():
            base[f"note_{k}"] = v
        rows.append(base)
    cal_rows = []
    for cr in obj.get("prerun_calibration", []):
        if isinstance(cr, dict):
            cal_rows.append(cr)
    return pd.DataFrame(rows), pd.DataFrame(cal_rows)


def run_modules(args: argparse.Namespace) -> Dict[str, Any]:
    analysis_folder = Path(args.analysis_folder).expanduser() if args.analysis_folder else Path(args.out_dir).expanduser()
    tables = Path(args.out_dir).expanduser() if args.out_dir else analysis_folder / "tables"
    tables.mkdir(parents=True, exist_ok=True)
    roots = [tables, analysis_folder / "tables", analysis_folder]

    event_log = args.event_log
    cue_path = args.cue_schedule_json or args.cue_schedule_csv
    ocm_path = args.ocm_cue_epoch_csv or find_first_existing(
        roots,
        names=[
            "combined_ocm_025_cue_epoch_table.csv", "her_ocm025_cue_epoch_table.csv", "ocm_025_cue_epoch_table.csv",
            "combined_ocm_cue_epoch_table.csv",
        ],
        patterns=["*ocm*025*cue_epoch*.csv", "*ocm*cue_epoch*.csv", "*rsm*cue_table*.csv"],
    )

    events = load_json_or_csv_events(event_log)
    branch_reports, calibration = extract_praycg19_confound_reports(events)
    manual_branch, manual_cal = load_manual_confound_json(getattr(args, "manual_confound_json", ""))
    if not manual_branch.empty:
        branch_reports = pd.concat([branch_reports, manual_branch], ignore_index=True, sort=False)
    if not manual_cal.empty:
        calibration = pd.concat([calibration, manual_cal], ignore_index=True, sort=False)
    cues = load_cue_schedule(cue_path)
    ocm = load_optional_csv(ocm_path)
    rsm = build_rsm_cvb_table(cues, ocm)
    registry = build_confound_registry(branch_reports, calibration)
    rsm_overlay, confound_overlay = build_visual_overlays(rsm, registry)

    outputs: Dict[str, str] = {}
    def write_df(df: pd.DataFrame, name: str):
        path = tables / name
        df.to_csv(path, index=False)
        outputs[name] = str(path)

    write_df(branch_reports, "branch_confound_reports.csv")
    write_df(calibration, "prerun_display_audio_calibration_table.csv")
    write_df(registry, "confound_registry.csv")
    write_df(rsm, "rsm_cvb_squint_cue_table.csv")
    write_df(rsm_overlay, "rsm_visual_overlay.csv")
    write_df(confound_overlay, "confound_visual_overlay.csv")

    summary = {
        "schema": "PRAYCG_MasterSuite_v1_4_6_Confound_RSM_summary",
        "version": VERSION,
        "analysis_folder": str(analysis_folder),
        "event_log": event_log,
        "cue_schedule": cue_path,
        "ocm_cue_epoch_csv": ocm_path,
        "n_branch_confound_reports": int(len(branch_reports)),
        "n_prerun_calibration_reports": int(len(calibration)),
        "n_rsm_rows": int(len(rsm)),
        "n_rsm_overlay_events": int(len(rsm_overlay)),
        "n_confound_overlay_events": int(len(confound_overlay)),
        "boundary": "Confound/RSM outputs are covariates and exploratory flags, not proof of mechanism, squinting, or hidden-Y biology.",
        "outputs": outputs,
    }
    if not rsm.empty:
        subset = rsm.copy()
        if "phase" in subset.columns:
            subset = subset[subset["phase"].astype(str).str.contains("OVERRIDE", case=False, na=False)]
        summary.update({
            "override_rows": int(len(subset)),
            "override_high_guess_risk_count": int((pd.to_numeric(subset.get("latent_guess_risk_v146", pd.Series(dtype=float)), errors="coerce") > 0.80).sum()) if not subset.empty else 0,
            "override_arithmetic_stall_candidate_count": int((subset.get("rsm_cvb_squint_category_v146", pd.Series(dtype=str)).astype(str) == "ARITHMETIC_STALL_CANDIDATE").sum()) if not subset.empty else 0,
            "override_hard_to_resolve_cue_candidate_count": int((subset.get("rsm_cvb_squint_category_v146", pd.Series(dtype=str)).astype(str) == "HARD_TO_RESOLVE_CUE_CANDIDATE").sum()) if not subset.empty else 0,
            "override_squint_candidate_count": int((subset.get("possible_squint_candidate_v146", pd.Series(dtype=bool)).astype(str).str.lower().isin(["true", "1", "yes"])).sum()) if not subset.empty else 0,
        })
    summary_path = tables / "confound_rsm_interpretation.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    outputs["confound_rsm_interpretation.json"] = str(summary_path)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="PRAYCG v1.4.6 confound/RSM/CVB/Squint modules")
    p.add_argument("--analysis-folder", default="", help="Root Master Comprehensive output folder.")
    p.add_argument("--event-log", default="", help="PRAYCG event log JSON/CSV. PRAYCG1.9 confound reports are parsed when present.")
    p.add_argument("--cue-schedule-json", default="")
    p.add_argument("--cue-schedule-csv", default="")
    p.add_argument("--ocm-cue-epoch-csv", default="", help="OCM025 cue-epoch table. If blank, script searches analysis folder/tables.")
    p.add_argument("--manual-confound-json", default="", help="Optional manual retrospective confound addendum JSON for runs collected before PRAYCG1.9.")
    p.add_argument("--out-dir", default="", help="Output tables folder. Defaults to <analysis-folder>/tables.")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    run_modules(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
