#!/usr/bin/env python3
"""
PRAYCG MRED-Peak / MRED-Resolution Endpoint Compression Module v1.5.5

Reads a PRAYCG Master Comprehensive analysis folder and produces a compact,
interpretable endpoint layer:

  - MRED-Peak: acute anchor-locked recognition + integration event.
  - MRED-Resolution: delayed reflective/regulatory recovery profile.

This script is deliberately conservative. It does not prove memory formation,
consciousness, OSM biology, or literal thermodynamic entropy. It compresses
existing module outputs into a reviewable endpoint table and text-safe JSON.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

VERSION = "1.5.5"
SCHEMA = "PRAYCG_MRED_Peak_Resolution_v1_5_5"

BOUNDARY = (
    "MRED-Peak/MRED-Resolution is an endpoint-compression layer. It does not prove "
    "memory formation, consciousness, OSM biology, cellular mechanism, or literal thermodynamic entropy. "
    "It summarizes existing PRAYCG outputs under explicit QC and claim boundaries."
)


def _norm(s: str) -> str:
    return "".join(ch.lower() for ch in str(s) if ch.isalnum())


def read_csv_safe(path: Optional[Path]) -> pd.DataFrame:
    if not path or not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        try:
            return pd.read_csv(path, encoding="utf-8-sig")
        except Exception:
            return pd.DataFrame()


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def find_table(root: Path, contains: Iterable[str], preferred_prefix: str = "") -> Optional[Path]:
    pats = [c.lower() for c in contains]
    candidates = []
    for p in root.rglob("*.csv"):
        name = p.name.lower()
        if all(x in name for x in pats):
            candidates.append(p)
    if not candidates:
        return None
    if preferred_prefix:
        pref = [p for p in candidates if p.name.lower().startswith(preferred_prefix.lower())]
        if pref:
            return sorted(pref, key=lambda p: len(str(p)))[0]
    # Prefer tables folder and shortest name.
    candidates = sorted(candidates, key=lambda p: ("tables" not in [q.name for q in p.parents], len(str(p))))
    return candidates[0]


def col(df: pd.DataFrame, *names: str) -> Optional[str]:
    if df.empty:
        return None
    cmap = {_norm(c): c for c in df.columns}
    for n in names:
        key = _norm(n)
        if key in cmap:
            return cmap[key]
    # flexible contains search
    for n in names:
        key = _norm(n)
        for k, c in cmap.items():
            if key and (key in k or k in key):
                return c
    return None


def to_num(s: Any, default: float = np.nan) -> float:
    try:
        v = float(s)
        if math.isfinite(v):
            return v
        return default
    except Exception:
        return default


def z01(values: List[float]) -> List[float]:
    arr = np.array([v if math.isfinite(v) else np.nan for v in values], dtype=float)
    if np.all(np.isnan(arr)):
        return [0.0 for _ in values]
    med = np.nanmedian(arr)
    q1, q3 = np.nanpercentile(arr, [25, 75])
    scale = (q3 - q1) / 1.349 if q3 > q1 else np.nanstd(arr)
    if not math.isfinite(scale) or scale < 1e-9:
        scale = 1.0
    z = (arr - med) / scale
    z = np.clip(z, -4, 4)
    out = (z + 4) / 8
    out = np.where(np.isnan(out), 0.5, out)
    return out.tolist()


def clip01(x: float) -> float:
    if not math.isfinite(x):
        return 0.0
    return float(max(0.0, min(1.0, x)))


def best_by_anchor(df: pd.DataFrame, anchor_col: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    if df.empty or anchor_col not in df:
        return out
    # Retain first row by default; callers should use pre-filtered tables.
    for _, r in df.iterrows():
        aid = str(r.get(anchor_col, "")).strip()
        if aid and aid not in out:
            out[aid] = r.to_dict()
    return out


def load_inputs(analysis_folder: Path) -> Dict[str, Any]:
    tables = analysis_folder / "tables"
    root = analysis_folder if analysis_folder.exists() else Path(".")
    preferred_prefix = ""
    # If exactly one run prefix dominates, this is unnecessary, but harmless.
    paths = {
        "amred": find_table(root, ["amred", "anchor", "endpoint"]),
        "cii": find_table(root, ["cii", "anchor"]),
        "mred_event": find_table(root, ["mred", "event"]),
        "nupi_run": find_table(root, ["nupi", "run", "summary"]),
        "nupi_anchor": find_table(root, ["nupi", "anchor", "polarity"]),
        "baseline": find_table(root, ["baseline1", "baseline2"]),
        "eet": find_table(root, ["eet", "echo"]),
        "mred_itp": find_table(root, ["mred", "itp", "anchor"]),
        "tti_global": find_table(root, ["tti", "global"]),
        "tti_anchor": find_table(root, ["tti", "anchor"]),
        "module_registry": find_table(root, ["module", "registry"]),
    }
    return {k: read_csv_safe(v) for k, v in paths.items()} | {"paths": {k: str(v) if v else "" for k, v in paths.items()}}


def amred_rows(amred: pd.DataFrame) -> pd.DataFrame:
    if amred.empty:
        return pd.DataFrame()
    sens_col = col(amred, "sensitivity")
    if sens_col:
        # Prefer runner time rows and avoid offset sensitivity duplicates when possible.
        runner = amred[amred[sens_col].astype(str).str.contains("runner|registered|default", case=False, na=False)].copy()
        if len(runner):
            return runner
    return amred.copy()


def build_anchor_table(inputs: Dict[str, Any]) -> pd.DataFrame:
    am = amred_rows(inputs.get("amred", pd.DataFrame()))
    cii = inputs.get("cii", pd.DataFrame())
    nupi_anchor = inputs.get("nupi_anchor", pd.DataFrame())
    eet = inputs.get("eet", pd.DataFrame())
    itp = inputs.get("mred_itp", pd.DataFrame())

    anchors: Dict[str, Dict[str, Any]] = {}

    if not am.empty:
        ac = col(am, "anchor_id")
        if ac:
            for _, r in am.iterrows():
                aid = str(r.get(ac, "")).strip()
                if not aid:
                    continue
                d = anchors.setdefault(aid, {"anchor_id": aid})
                for k in [
                    "anchor_time_sec_used", "original_anchor_time_sec", "A_MRED_pass", "base_gate_pass",
                    "specificity_gate_pass", "claim_level", "notes", "target_MR", "target_ENC", "target_CII",
                    "target_artifact", "target_minus_control_MR", "target_minus_override_MR",
                    "target_minus_control_ENC", "target_minus_override_ENC", "target_minus_control_CII",
                    "target_minus_override_CII", "IAQ_target_vs_override"
                ]:
                    ck = col(am, k)
                    if ck and ck in r:
                        d[k] = r.get(ck)

    # Add CII/MR/ENC if A-MRED table absent or sparse.
    if not cii.empty:
        ac = col(cii, "anchor_id")
        cond = col(cii, "condition")
        for _, r in cii.iterrows():
            aid = str(r.get(ac, "")).strip() if ac else ""
            if not aid:
                continue
            d = anchors.setdefault(aid, {"anchor_id": aid})
            c = str(r.get(cond, "")).lower() if cond else ""
            prefix = "target" if "target" in c else "control" if "control" in c else "override" if "override" in c else "condition"
            for k in ["CII", "MR", "ENC", "artifact", "anchor_time_sec"]:
                ck = col(cii, k)
                if ck:
                    name = f"{prefix}_{k}" if k != "anchor_time_sec" else "anchor_time_sec"
                    d.setdefault(name, r.get(ck))

    if not nupi_anchor.empty:
        ac = col(nupi_anchor, "anchor_id")
        for _, r in nupi_anchor.iterrows():
            aid = str(r.get(ac, "")).strip() if ac else ""
            if not aid:
                continue
            d = anchors.setdefault(aid, {"anchor_id": aid})
            for k in ["RDI", "ALI", "NUPI", "classification", "resolution_score", "recovery_score", "afterstate_echo", "baseline2_recovery"]:
                ck = col(nupi_anchor, k)
                if ck:
                    d[f"nupi_{k}"] = r.get(ck)

    if not eet.empty:
        ac = col(eet, "anchor_id")
        sim = col(eet, "cosine_similarity_state_vector", "cosine_similarity", "similarity")
        comp = col(eet, "comparison", "comparison_phase")
        if ac and sim:
            for aid, sub in eet.groupby(ac):
                vals = pd.to_numeric(sub[sim], errors="coerce")
                # Prefer Baseline2 if present, otherwise max available washout echo.
                b2 = sub[sub[comp].astype(str).str.contains("baseline", case=False, na=False)] if comp else pd.DataFrame()
                d = anchors.setdefault(str(aid), {"anchor_id": str(aid)})
                d["eet_max_echo"] = float(vals.max()) if vals.notna().any() else np.nan
                if len(b2):
                    bvals = pd.to_numeric(b2[sim], errors="coerce")
                    d["eet_baseline2_echo"] = float(bvals.max()) if bvals.notna().any() else np.nan

    if not itp.empty:
        ac = col(itp, "anchor_id")
        for _, r in itp.iterrows():
            aid = str(r.get(ac, "")).strip() if ac else ""
            if not aid:
                continue
            d = anchors.setdefault(aid, {"anchor_id": aid})
            for k in ["CSI", "ORI", "ITP", "ACG", "OCU", "strict_MRED_ITP_pass", "mred_lock"]:
                ck = col(itp, k)
                if ck:
                    d[f"itp_{k}"] = r.get(ck)

    if not anchors:
        return pd.DataFrame()
    df = pd.DataFrame(list(anchors.values()))
    return df


def boolish(x: Any) -> bool:
    if isinstance(x, bool):
        return x
    s = str(x).strip().lower()
    return s in {"1", "true", "yes", "y", "pass", "passed"}


def compute_scores(anchor_df: pd.DataFrame, nupi_run: pd.DataFrame, baseline_df: pd.DataFrame) -> pd.DataFrame:
    if anchor_df.empty:
        return anchor_df
    df = anchor_df.copy()
    # Numeric columns, with aliases.
    for c in df.columns:
        if c not in {"anchor_id", "claim_level", "notes", "nupi_classification"}:
            try:
                df[c] = pd.to_numeric(df[c], errors="coerce")
            except Exception:
                pass

    # Build peak score components.
    tmr = pd.to_numeric(df.get("target_MR", df.get("target_MR", np.nan)), errors="coerce")
    tenc = pd.to_numeric(df.get("target_ENC", np.nan), errors="coerce")
    tcii = pd.to_numeric(df.get("target_CII", df.get("target_CII", np.nan)), errors="coerce")
    mr_margin = pd.to_numeric(df.get("target_minus_override_MR", np.nan), errors="coerce")
    enc_margin = pd.to_numeric(df.get("target_minus_override_ENC", np.nan), errors="coerce")
    cii_margin = pd.to_numeric(df.get("target_minus_override_CII", np.nan), errors="coerce")
    artifact = pd.to_numeric(df.get("target_artifact", np.nan), errors="coerce")
    amred_pass = df.get("A_MRED_pass", pd.Series([False] * len(df))).apply(boolish)
    base_gate = df.get("base_gate_pass", pd.Series([False] * len(df))).apply(boolish)
    spec_gate = df.get("specificity_gate_pass", pd.Series([False] * len(df))).apply(boolish)

    # Robust score: positive recognition/integration + Target specificity + gate support - artifact.
    comp = pd.DataFrame({
        "MR": z01(tmr.tolist()),
        "ENC": z01(tenc.tolist()),
        "CII": z01(tcii.tolist()),
        "MR_margin": z01(mr_margin.fillna(0).tolist()),
        "ENC_margin": z01(enc_margin.fillna(0).tolist()),
        "CII_margin": z01(cii_margin.fillna(0).tolist()),
        "artifact_inv": [1 - clip01(abs(x) / 4) if math.isfinite(to_num(x)) else 0.5 for x in artifact.tolist()],
    })
    score = (
        0.20 * comp["MR"] +
        0.22 * comp["ENC"] +
        0.15 * comp["CII"] +
        0.13 * comp["MR_margin"] +
        0.13 * comp["ENC_margin"] +
        0.08 * comp["CII_margin"] +
        0.09 * comp["artifact_inv"]
    )
    score += amred_pass.astype(float) * 0.18 + base_gate.astype(float) * 0.06 + spec_gate.astype(float) * 0.05
    df["mred_peak_score"] = np.clip(score, 0, 1)

    # Resolution: recovery/echo/self-report-like afterstate, weighted by modest MR and low task/extraction when available.
    rdi_run = np.nan
    nupi_val = np.nan
    nupi_cls = ""
    if not nupi_run.empty:
        rcol = col(nupi_run, "RDI")
        ncol = col(nupi_run, "NUPI")
        ccol = col(nupi_run, "classification")
        if rcol:
            rdi_run = to_num(nupi_run.iloc[0].get(rcol))
        if ncol:
            nupi_val = to_num(nupi_run.iloc[0].get(ncol))
        if ccol:
            nupi_cls = str(nupi_run.iloc[0].get(ccol, ""))
    eet_echo = pd.to_numeric(df.get("eet_baseline2_echo", df.get("eet_max_echo", np.nan)), errors="coerce")
    nupi_src = df.get("nupi_RDI", pd.Series([np.nan] * len(df), index=df.index))
    if not isinstance(nupi_src, pd.Series):
        nupi_src = pd.Series([nupi_src] * len(df), index=df.index)
    nupi_rdi_anchor = pd.to_numeric(nupi_src, errors="coerce")
    # Fill from run RDI where anchor-level absent.
    rdi_vec = nupi_rdi_anchor.copy()
    if math.isfinite(rdi_run):
        rdi_vec = rdi_vec.fillna(rdi_run)
    echo_vec = eet_echo.fillna(0.5)
    # Resolution rewards post-state recovery and echo more than acute peak.
    res_comp = pd.DataFrame({
        "RDI": z01(rdi_vec.tolist()),
        "Echo": z01(echo_vec.tolist()),
        "MR": z01(tmr.tolist()),
        "CII": z01(tcii.tolist()),
        "Peak_not_too_high": [1 - min(1, max(0, to_num(x))) for x in df["mred_peak_score"].tolist()],
    })
    res_score = 0.38 * res_comp["RDI"] + 0.27 * res_comp["Echo"] + 0.14 * res_comp["MR"] + 0.11 * res_comp["CII"] + 0.10 * res_comp["Peak_not_too_high"]
    # Strong A-MRED can also be part of resolution if after-state is strong; don't penalize too much.
    res_score += amred_pass.astype(float) * 0.05
    df["mred_resolution_score"] = np.clip(res_score, 0, 1)
    df["run_level_RDI"] = rdi_run
    df["run_level_NUPI"] = nupi_val
    df["run_level_NUPI_classification"] = nupi_cls

    peak_gate = []
    res_gate = []
    for _, row in df.iterrows():
        if boolish(row.get("A_MRED_pass")):
            if "estimated" in str(row.get("claim_level", "")).lower() or "caution" in str(row.get("claim_level", "")).lower():
                peak_gate.append("STRICT_PEAK_PASS_TIMING_CAUTION")
            else:
                peak_gate.append("STRICT_PEAK_PASS")
        elif row.get("mred_peak_score", 0) >= 0.68 and (to_num(row.get("target_MR")) > 0 or to_num(row.get("target_CII")) > 0):
            peak_gate.append("PEAK_CANDIDATE_NO_STRICT_LOCK")
        else:
            peak_gate.append("NO_PEAK_PASS")

        if row.get("mred_resolution_score", 0) >= 0.68 and (math.isfinite(to_num(row.get("run_level_RDI"))) or math.isfinite(to_num(row.get("eet_baseline2_echo")))):
            res_gate.append("RESOLUTION_CANDIDATE")
        elif not math.isfinite(to_num(row.get("run_level_RDI"))) and not math.isfinite(to_num(row.get("eet_baseline2_echo"))):
            res_gate.append("NOT_GRADABLE_NO_BASELINE2_OR_ECHO")
        else:
            res_gate.append("NO_RESOLUTION_PASS")
    df["mred_peak_gate"] = peak_gate
    df["mred_resolution_gate"] = res_gate
    return df


def summarize_run(df: pd.DataFrame, inputs: Dict[str, Any], run_label: str = "") -> Dict[str, Any]:
    if df.empty:
        return {
            "schema": SCHEMA,
            "version": VERSION,
            "run_label": run_label,
            "status": "NO_ANCHOR_TABLE_AVAILABLE",
            "boundary": BOUNDARY,
        }
    top_peak = df.sort_values("mred_peak_score", ascending=False).iloc[0].to_dict()
    top_res = df.sort_values("mred_resolution_score", ascending=False).iloc[0].to_dict()
    strict_peak_count = int(df["mred_peak_gate"].astype(str).str.contains("STRICT_PEAK_PASS", na=False).sum())
    peak_candidate_count = int(df["mred_peak_gate"].astype(str).str.contains("PEAK_CANDIDATE", na=False).sum())
    resolution_count = int((df["mred_resolution_gate"] == "RESOLUTION_CANDIDATE").sum())
    summary = {
        "schema": SCHEMA,
        "version": VERSION,
        "run_label": run_label or "unspecified_run",
        "anchor_count": int(len(df)),
        "strict_peak_pass_count": strict_peak_count,
        "soft_peak_candidate_count": peak_candidate_count,
        "resolution_candidate_count": resolution_count,
        "top_peak_anchor_id": top_peak.get("anchor_id", ""),
        "top_peak_score": float(to_num(top_peak.get("mred_peak_score"), 0)),
        "top_peak_gate": str(top_peak.get("mred_peak_gate", "")),
        "top_resolution_anchor_id": top_res.get("anchor_id", ""),
        "top_resolution_score": float(to_num(top_res.get("mred_resolution_score"), 0)),
        "top_resolution_gate": str(top_res.get("mred_resolution_gate", "")),
        "overall_interpretation": "",
        "boundary": BOUNDARY,
        "input_tables": inputs.get("paths", {}),
    }
    if strict_peak_count and resolution_count:
        summary["overall_interpretation"] = "Mixed profile: at least one strict/strict-cautioned peak and at least one resolution candidate. Interpret peak and recovery as distinct endpoints."
    elif strict_peak_count:
        summary["overall_interpretation"] = "MRED-Peak dominant: acute Target-specific recognition/integration is stronger than delayed resolution."
    elif resolution_count:
        summary["overall_interpretation"] = "MRED-Resolution dominant: delayed reflective/regulatory recovery is stronger than acute peak evidence."
    elif peak_candidate_count:
        summary["overall_interpretation"] = "Soft peak candidate only: recognition/integration structure is present but does not meet strict endpoint criteria."
    else:
        summary["overall_interpretation"] = "No dedicated MRED-Peak or MRED-Resolution endpoint pass under available inputs."
    return summary


def make_visual_overlay(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if df.empty:
        return pd.DataFrame(columns=["time_sec", "start_sec", "end_sec", "category", "label", "anchor_id", "score", "claim_level"])
    time_col = "anchor_time_sec_used" if "anchor_time_sec_used" in df.columns else "anchor_time_sec" if "anchor_time_sec" in df.columns else "original_anchor_time_sec" if "original_anchor_time_sec" in df.columns else None
    for _, r in df.iterrows():
        t = to_num(r.get(time_col)) if time_col else np.nan
        if not math.isfinite(t):
            continue
        aid = str(r.get("anchor_id", "anchor"))
        pg = str(r.get("mred_peak_gate", ""))
        rg = str(r.get("mred_resolution_gate", ""))
        if "STRICT" in pg or "PEAK_CANDIDATE" in pg:
            rows.append({"time_sec": t, "start_sec": max(0, t-5), "end_sec": t+30, "category": "mred_peak", "label": f"{aid}: {pg}", "anchor_id": aid, "score": r.get("mred_peak_score", np.nan), "claim_level": r.get("claim_level", "")})
        if rg == "RESOLUTION_CANDIDATE":
            rows.append({"time_sec": t, "start_sec": max(0, t-5), "end_sec": t+60, "category": "mred_resolution", "label": f"{aid}: {rg}", "anchor_id": aid, "score": r.get("mred_resolution_score", np.nan), "claim_level": r.get("claim_level", "")})
    return pd.DataFrame(rows)


def text_report(summary: Dict[str, Any], df: pd.DataFrame) -> str:
    lines = []
    lines.append("# MRED-Peak / MRED-Resolution Endpoint Compression Report")
    lines.append("")
    lines.append(f"Schema: `{summary.get('schema')}`  ")
    lines.append(f"Version: `{summary.get('version')}`  ")
    lines.append(f"Run label: `{summary.get('run_label')}`")
    lines.append("")
    lines.append("## Boundary")
    lines.append(BOUNDARY)
    lines.append("")
    lines.append("## Executive interpretation")
    lines.append(summary.get("overall_interpretation", "No interpretation generated."))
    lines.append("")
    lines.append("## Counts")
    lines.append(f"- Anchors evaluated: **{summary.get('anchor_count', 0)}**")
    lines.append(f"- Strict or strict-cautioned MRED-Peak passes: **{summary.get('strict_peak_pass_count', 0)}**")
    lines.append(f"- Soft MRED-Peak candidates: **{summary.get('soft_peak_candidate_count', 0)}**")
    lines.append(f"- MRED-Resolution candidates: **{summary.get('resolution_candidate_count', 0)}**")
    lines.append("")
    if not df.empty:
        peak = df.sort_values("mred_peak_score", ascending=False).iloc[0]
        res = df.sort_values("mred_resolution_score", ascending=False).iloc[0]
        lines.append("## Top MRED-Peak candidate")
        lines.append(f"- Anchor: `{peak.get('anchor_id','')}`")
        lines.append(f"- Score: `{to_num(peak.get('mred_peak_score'),0):.3f}`")
        lines.append(f"- Gate: `{peak.get('mred_peak_gate','')}`")
        lines.append(f"- Target MR / ENC / CII: `{to_num(peak.get('target_MR'),np.nan):.3f}` / `{to_num(peak.get('target_ENC'),np.nan):.3f}` / `{to_num(peak.get('target_CII'),np.nan):.3f}`")
        lines.append("")
        lines.append("## Top MRED-Resolution candidate")
        lines.append(f"- Anchor: `{res.get('anchor_id','')}`")
        lines.append(f"- Score: `{to_num(res.get('mred_resolution_score'),0):.3f}`")
        lines.append(f"- Gate: `{res.get('mred_resolution_gate','')}`")
        lines.append(f"- Run-level RDI / NUPI: `{to_num(res.get('run_level_RDI'),np.nan):.3f}` / `{to_num(res.get('run_level_NUPI'),np.nan):.3f}`")
        lines.append("")
        lines.append("## Interpretation guide")
        lines.append("- MRED-Peak means acute anchor-locked recognition plus delayed integration. It is strongest when A-MRED/BIT and condition specificity agree.")
        lines.append("- MRED-Resolution means delayed reflective/regulatory recovery. It requires Baseline2/EET/NUPI-like evidence and should not be forced for older runs without that layer.")
        lines.append("- A run can be peak-dominant, resolution-dominant, mixed, or unresolved.")
    return "\n".join(lines) + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="PRAYCG MRED-Peak / MRED-Resolution endpoint compression module v1.5.5")
    ap.add_argument("--analysis-folder", required=True, help="Master Comprehensive output folder containing a tables/ subfolder.")
    ap.add_argument("--out-dir", default="", help="Output directory. Defaults to <analysis-folder>/tables.")
    ap.add_argument("--run-label", "--project-name", dest="run_label", default="", help="Optional human-readable run label/project name.")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args(argv)

    analysis_folder = Path(args.analysis_folder).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else analysis_folder / "tables"
    out_dir.mkdir(parents=True, exist_ok=True)

    inputs = load_inputs(analysis_folder)
    anchor = build_anchor_table(inputs)
    scored = compute_scores(anchor, inputs.get("nupi_run", pd.DataFrame()), inputs.get("baseline", pd.DataFrame()))
    summary = summarize_run(scored, inputs, args.run_label)
    overlay = make_visual_overlay(scored)

    anchor_path = out_dir / "mred_peak_resolution_anchor_table.csv"
    run_path = out_dir / "mred_peak_resolution_run_summary.csv"
    top_peak_path = out_dir / "top_mred_peak_candidates.csv"
    top_res_path = out_dir / "top_mred_resolution_candidates.csv"
    overlay_path = out_dir / "mred_peak_resolution_visual_overlay.csv"
    json_path = out_dir / "mred_peak_resolution_interpretation.json"
    md_path = out_dir / "mred_peak_resolution_report.md"

    scored.to_csv(anchor_path, index=False)
    pd.DataFrame([summary]).to_csv(run_path, index=False)
    if not scored.empty:
        scored.sort_values("mred_peak_score", ascending=False).head(10).to_csv(top_peak_path, index=False)
        scored.sort_values("mred_resolution_score", ascending=False).head(10).to_csv(top_res_path, index=False)
    else:
        pd.DataFrame().to_csv(top_peak_path, index=False)
        pd.DataFrame().to_csv(top_res_path, index=False)
    overlay.to_csv(overlay_path, index=False)
    write_json(json_path, summary)
    write_md(md_path, text_report(summary, scored))

    print(json.dumps({
        "status": "ok",
        "schema": SCHEMA,
        "analysis_folder": str(analysis_folder),
        "out_dir": str(out_dir),
        "outputs": {
            "anchor_table": str(anchor_path),
            "run_summary": str(run_path),
            "top_peak": str(top_peak_path),
            "top_resolution": str(top_res_path),
            "visual_overlay": str(overlay_path),
            "interpretation_json": str(json_path),
            "report_md": str(md_path),
        }
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
