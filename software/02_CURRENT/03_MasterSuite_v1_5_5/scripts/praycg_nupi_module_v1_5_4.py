#!/usr/bin/env python3
"""
PRAYCG NUPI v1.5.4 - Narrative Update Polarity Index

This module classifies narrative-update polarity as a proxy-level profile:
- ALI: Accommodative Load Index
- RDI: Resolutive Recovery Index
- NUPI = RDI - ALI

Boundary: NUPI does not measure literal heat, ATP, glucose metabolism, clinical restoration,
moral value, or consciousness. It is a secondary/exploratory PRAYCG interpretation layer.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
from typing import Optional, Dict, Any, List
import numpy as np
import pandas as pd


def clip01(x):
    if x is None:
        return np.nan
    try:
        if pd.isna(x):
            return np.nan
    except Exception:
        pass
    return max(0.0, min(1.0, float(x)))


def safe_mean(vals):
    vals = [v for v in vals if v is not None and not pd.isna(v)]
    return float(np.mean(vals)) if vals else np.nan


def find_one(folder: Path, patterns: List[str]) -> Optional[Path]:
    for pat in patterns:
        hits = sorted(folder.glob(pat))
        if hits:
            return hits[0]
    return None


def load_cii(profile: str, folder: Path) -> pd.DataFrame:
    f = find_one(folder, ["*cii_anchor_integrals.csv", "*CII*anchor*.csv"])
    if not f:
        raise FileNotFoundError("Could not find CII anchor integral table in analysis folder.")
    df = pd.read_csv(f)
    profile = profile.lower()
    rows = []
    if "arrival" in profile or {"target_CII", "control_CII", "override_CII"}.issubset(df.columns):
        for _, r in df.iterrows():
            rows.append(dict(
                anchor_id=r.get("anchor_id"),
                label=r.get("label", r.get("scene_label", r.get("anchor_id"))),
                target_time_sec=r.get("center_sec", r.get("anchor_time_sec", np.nan)),
                target_CII=r.get("target_CII", np.nan),
                control_CII=r.get("control_CII", np.nan),
                override_CII=r.get("override_CII", np.nan),
                target_MR=r.get("target_MR", np.nan),
                target_ENC=r.get("target_ENC", np.nan),
                target_artifact=r.get("target_artifact", np.nan),
                target_taskgamma=r.get("target_task_gamma", np.nan),
            ))
    elif "condition" in df.columns and "NIP_density_mean_CII" in df.columns:
        for aid, g in df.groupby("anchor_id"):
            def one(cond, col):
                s = g.loc[g.condition.eq(cond), col]
                return float(s.iloc[0]) if len(s) else np.nan
            tc, cc, oc = one("TARGET_1", "NIP_density_mean_CII"), one("CONTROL_1", "NIP_density_mean_CII"), one("CONTEXTUAL_OVERRIDE_1", "NIP_density_mean_CII")
            rows.append(dict(anchor_id=aid, label=g.get("scene_label", pd.Series([aid])).iloc[0], target_time_sec=one("TARGET_1", "window_start_sec"), target_CII=tc, control_CII=cc, override_CII=oc, target_MR=one("TARGET_1", "A_sem_mean"), target_ENC=one("TARGET_1", "R_int_mean"), target_artifact=one("TARGET_1", "artifact_mean"), target_taskgamma=np.nan))
    elif "condition" in df.columns and "CII" in df.columns:
        # Field-style compact table
        for aid, g in df.groupby("anchor_id"):
            def one(cond, col):
                s = g.loc[g.condition.eq(cond), col]
                return float(s.iloc[0]) if len(s) else np.nan
            tc, cc, oc = one("TARGET", "CII"), one("CONTROL", "CII"), one("OVERRIDE", "CII")
            rows.append(dict(anchor_id=aid, label=aid, target_time_sec=one("TARGET", "anchor_time_sec"), target_CII=tc, control_CII=cc, override_CII=oc, target_MR=one("TARGET", "MR"), target_ENC=one("TARGET", "ENC"), target_artifact=one("TARGET", "artifact"), target_taskgamma=np.nan))
    else:
        raise ValueError("CII table format not recognized.")
    out = pd.DataFrame(rows)
    out["target_specific_CII"] = out["target_CII"] - out[["control_CII", "override_CII"]].max(axis=1)
    return out


def load_tti(folder: Path) -> float:
    f = find_one(folder, ["*tti_global_summary.csv", "thermodynamic_theft_composite_index.csv", "*theft*composite*.csv"])
    if not f:
        return np.nan
    df = pd.read_csv(f)
    if "TTI_global" in df.columns:
        return float(df["TTI_global"].iloc[0])
    if "TTI" in df.columns:
        return float(df["TTI"].iloc[0])
    if "component" in df.columns and "value" in df.columns:
        s = df.loc[df["component"].astype(str).str.contains("thermodynamic_theft_index", case=False, regex=False), "value"]
        return float(s.iloc[0]) if len(s) else np.nan
    return np.nan


def load_itp(profile: str, folder: Path) -> pd.DataFrame:
    f = find_one(folder, ["*mred_itp_anchor_summary.csv", "*itp*anchor*.csv"])
    if not f:
        return pd.DataFrame(columns=["anchor_id", "complexity_strike", "complexity_settle", "CSI", "ACG_feature_proxy_flag", "OCU_proxy_flag"])
    d = pd.read_csv(f)
    if "condition" in d.columns:
        if "TARGET_1" in set(d["condition"].astype(str)):
            d = d[d["condition"].astype(str).eq("TARGET_1")].copy()
        elif "TARGET" in set(d["condition"].astype(str)):
            d = d[d["condition"].astype(str).eq("TARGET")].copy()
    rename = {
        "C_strike": "complexity_strike",
        "delta_C_strike_peak_minus_pre": "complexity_strike",
        "C_settle": "complexity_settle",
        "delta_C_settle_post_minus_peak": "complexity_settle",
        "complexity_settlement_index": "CSI",
        "CSI_complexity_settlement_index": "CSI",
        "ACG_candidate": "ACG_feature_proxy_flag",
        "OCU_candidate": "OCU_proxy_flag",
    }
    d = d.rename(columns=rename)
    for col in ["complexity_strike", "complexity_settle", "CSI", "ACG_feature_proxy_flag", "OCU_proxy_flag"]:
        if col not in d.columns:
            d[col] = np.nan if col not in ["ACG_feature_proxy_flag", "OCU_proxy_flag"] else False
    return d[["anchor_id", "complexity_strike", "complexity_settle", "CSI", "ACG_feature_proxy_flag", "OCU_proxy_flag"]]


def load_eet(folder: Path) -> pd.DataFrame:
    f = find_one(folder, ["*eet_endogenous_echo_tracking.csv", "*endogenous_echo*.csv"])
    if not f:
        return pd.DataFrame(columns=["anchor_id", "afterstate_echo_max", "baseline2_echo_max"])
    d = pd.read_csv(f)
    rows = []
    if "reference_window" in d.columns:
        for aid, g in d.groupby("anchor_id"):
            after = g[g.reference_window.astype(str).str.contains("WASHOUT", case=False, regex=True)]
            b2 = g[g.reference_window.astype(str).str.contains("BASELINE_2|BASELINE2", case=False, regex=True)]
            rows.append(dict(anchor_id=aid, afterstate_echo_max=after.cosine_similarity.max() if len(after) else np.nan, baseline2_echo_max=b2.cosine_similarity.max() if len(b2) else np.nan))
    elif "comparison" in d.columns:
        sim_col = "cosine_similarity_state_vector"
        for aid, g in d.groupby("anchor_id"):
            after = g[g.comparison.astype(str).str.contains("WASHOUT", case=False, regex=True)]
            b2 = g[g.comparison.astype(str).str.contains("BASELINE_2|BASELINE2", case=False, regex=True)]
            rows.append(dict(anchor_id=aid, afterstate_echo_max=after[sim_col].max() if len(after) else np.nan, baseline2_echo_max=b2[sim_col].max() if len(b2) else np.nan))
    elif "comparison_window" in d.columns:
        for aid, g in d.groupby("anchor_id"):
            after = g[g.comparison_window.astype(str).str.contains("WASHOUT", case=False, regex=True)]
            rows.append(dict(anchor_id=aid, afterstate_echo_max=after.cosine_similarity.max() if len(after) else np.nan, baseline2_echo_max=np.nan))
    return pd.DataFrame(rows)


def b2_scores(folder: Path) -> Dict[str, Any]:
    vals = {}
    f = find_one(folder, ["*baseline1_vs_baseline2_feature_summary.csv", "*baseline1_vs_baseline2_summary.csv"])
    if f:
        df = pd.read_csv(f)
        metric_col = "metric"
        delta_col = "delta_B2_minus_B1" if "delta_B2_minus_B1" in df.columns else "delta_b2_minus_b1" if "delta_b2_minus_b1" in df.columns else None
        if delta_col:
            for _, r in df.iterrows(): vals[str(r[metric_col])] = float(r[delta_col])
    f2 = find_one(folder, ["*baseline1_vs_baseline2_polar_respiration_summary.csv"])
    if f2:
        df = pd.read_csv(f2)
        for _, r in df.iterrows(): vals[str(r["metric"])] = float(r["delta_B2_minus_B1"])
    if not vals:
        return dict(b2_available=False, b2_regulation_score=np.nan, b2_semantic_echo_score=np.nan, b2_strain_score=np.nan, b2_raw={})
    def val(*names):
        for n in names:
            if n in vals: return vals[n]
        return np.nan
    hr, rm, sd, pnn = val("hr_mean_bpm"), val("rmssd_ms"), val("sdnn_ms"), val("pNN50", "pnn50")
    respstd, task, art = val("Resp std", "resp_std"), val("TaskGamma", "taskgamma_z"), val("ArtifactScore", "artifact_score")
    alpha, tsp, nip, nast = val("PosteriorAlpha", "alpha_posterior_z"), val("TSP", "tsp_z"), val("NIP_density"), val("NAST_NAS", "nast_nas_z")
    reg=[]; sem=[]; strain=[]
    if not pd.isna(hr): reg.append(clip01(-hr/10)); strain.append(clip01(hr/10))
    if not pd.isna(rm): reg.append(clip01(rm/50)); strain.append(clip01(-rm/50))
    if not pd.isna(sd): reg.append(clip01(sd/50))
    if not pd.isna(pnn): reg.append(clip01(pnn/0.15))
    if not pd.isna(respstd): reg.append(clip01(-respstd/1.5)); strain.append(clip01(respstd/1.5))
    if not pd.isna(task): reg.append(clip01(-task/1.5)); strain.append(clip01(task/1.5))
    if not pd.isna(art): reg.append(clip01(-art/1.5)); strain.append(clip01(art/1.5))
    if not pd.isna(tsp): sem.append(clip01(tsp/1.0))
    if not pd.isna(nip): sem.append(clip01(nip/0.15))
    if not pd.isna(nast): sem.append(clip01(nast/1.5))
    if not pd.isna(alpha): sem.append(clip01(alpha/0.7))
    return dict(b2_available=True, b2_regulation_score=safe_mean(reg), b2_semantic_echo_score=safe_mean(sem), b2_strain_score=safe_mean(strain), b2_raw=vals)


def primary_pass_count(folder: Path) -> tuple[int, int]:
    f = find_one(folder, ["*amred_anchor_endpoint_table.csv", "*bit_event_table.csv"])
    if not f:
        return 0, 0
    d = pd.read_csv(f)
    if "sensitivity" in d.columns:
        d = d[d["sensitivity"].astype(str).eq("runner_registered_time")]
    for col in ["A_MRED_pass", "BIT_pass_praycg_strict", "BIT_strict_pass", "BIT_pass_event_only"]:
        if col in d.columns:
            return int(d[col].astype(bool).sum()), len(d)
    return 0, len(d)


def run_module(args):
    folder = Path(args.analysis_folder)
    out = Path(args.out_dir) if args.out_dir else folder / "tables"
    out.mkdir(parents=True, exist_ok=True)
    cii = load_cii(args.profile, folder)
    itp = load_itp(args.profile, folder)
    eet = load_eet(folder)
    anchors = cii.merge(itp, on="anchor_id", how="left").merge(eet, on="anchor_id", how="left")
    anchors["load_proxy"] = anchors.apply(lambda r: safe_mean([clip01(max(r.target_CII,0)/1.0), clip01(max(r.target_MR,0)/1.2), clip01(max(r.target_ENC,0)/1.5), clip01(max(r.complexity_strike if not pd.isna(r.complexity_strike) else 0,0)/0.08)]), axis=1)
    anchors["recovery_proxy"] = anchors.apply(lambda r: safe_mean([clip01((r.baseline2_echo_max+1)/2) if not pd.isna(r.baseline2_echo_max) else np.nan, clip01((r.afterstate_echo_max+1)/2) if not pd.isna(r.afterstate_echo_max) else np.nan, clip01(max(-(r.complexity_settle if not pd.isna(r.complexity_settle) else 0),0)/0.05)]), axis=1)
    anchors["anchor_NUPI_proxy"] = anchors["recovery_proxy"] - anchors["load_proxy"]
    anchors["anchor_polarity_label"] = pd.cut(anchors["anchor_NUPI_proxy"], bins=[-np.inf,-0.25,0.25,np.inf], labels=["ACCOMMODATIVE_LOAD_TILT","MIXED_NEUTRAL_TILT","RESOLUTIVE_RECOVERY_TILT"])
    # run summary
    b2 = b2_scores(folder)
    pass_count,total = primary_pass_count(folder)
    tti = load_tti(folder)
    semantic_intensity = safe_mean([clip01(anchors.target_CII.mean()/0.9), clip01(anchors.target_CII.max()/1.6), clip01(max(anchors.target_MR.mean(),0)/1.2), clip01(max(anchors.target_ENC.mean(),0)/1.5)])
    target_specificity = clip01(max(anchors.target_specific_CII.mean(),0)/0.8)
    complexity_perturb = safe_mean([clip01(max(np.maximum(anchors.complexity_strike.fillna(0),0).mean(),0)/0.08), clip01(max(-anchors.complexity_settle.mean(),0)/0.05), clip01(max(anchors.CSI.max() if "CSI" in anchors else 0,0)/1.5)])
    tti_score = clip01(max(tti,0)/0.75)
    primary_pass_score = clip01(pass_count/max(total,1)*3) if total else 0
    ALI = safe_mean([semantic_intensity,target_specificity,complexity_perturb,tti_score,primary_pass_score])
    eet_echo = safe_mean([clip01((anchors.baseline2_echo_max.max()+1)/2) if "baseline2_echo_max" in anchors and not pd.isna(anchors.baseline2_echo_max.max()) else np.nan, clip01((anchors.afterstate_echo_max.max()+1)/2) if "afterstate_echo_max" in anchors and not pd.isna(anchors.afterstate_echo_max.max()) else np.nan])
    RDI = safe_mean([b2["b2_regulation_score"], b2["b2_semantic_echo_score"], eet_echo]) if b2["b2_available"] else np.nan
    RDI_proxy = safe_mean([eet_echo])
    NUPI = RDI - ALI if not pd.isna(RDI) else np.nan
    if not b2["b2_available"]:
        label="POLARITY_UNRESOLVED_NO_BASELINE2"
    elif ALI>=0.58 and RDI>=0.60:
        label="HIGH_LOAD_WITH_RECOVERY"
    elif RDI>=0.60 and ALI<0.58:
        label="RESOLUTIVE_RECOVERY"
    elif ALI>=0.58 and RDI<0.45:
        label="ACCOMMODATIVE_LOAD"
    elif semantic_intensity>=0.4 and RDI<0.45:
        label="RECOGNITION_WITH_WEAK_RECOVERY"
    else:
        label="MIXED_OR_UNCERTAIN"
    summary = pd.DataFrame([dict(run=args.run_name or args.profile, semantic_intensity=semantic_intensity, target_specificity=target_specificity, complexity_perturbation=complexity_perturb, tti_score=tti_score, primary_pass_score=primary_pass_score, ALI_accommodative_load=ALI, b2_regulation=b2["b2_regulation_score"], b2_semantic_echo=b2["b2_semantic_echo_score"], b2_strain=b2["b2_strain_score"], eet_echo=eet_echo, RDI_resolutive_recovery=RDI, RDI_afterstate_proxy=RDI_proxy, NUPI=NUPI, polarity_class=label)])
    anchors.to_csv(out/"nupi_anchor_polarity_table.csv", index=False)
    summary.to_csv(out/"nupi_run_summary.csv", index=False)
    overlay = anchors[["anchor_id","target_time_sec","anchor_NUPI_proxy","anchor_polarity_label","load_proxy","recovery_proxy"]].copy()
    overlay["time_sec"] = overlay["target_time_sec"]
    overlay["end_sec"] = overlay["target_time_sec"] + 30
    overlay["category"] = "nupi"
    overlay["label"] = overlay["anchor_polarity_label"].astype(str)
    overlay.to_csv(out/"nupi_visual_overlay.csv", index=False)
    with open(out/"nupi_interpretation.json", "w", encoding="utf-8") as f:
        json.dump({"module":"NUPI_v0.1", "version":"1.5.4", "boundary":"Proxy-level narrative update polarity. Not literal thermodynamics.", "summary":summary.to_dict(orient="records")}, f, indent=2)
    print(summary.to_string(index=False))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--analysis-folder", required=True)
    p.add_argument("--profile", required=True, help="arrival, contact, field, or custom")
    p.add_argument("--run-name", default="")
    p.add_argument("--out-dir", default="")
    args=p.parse_args()
    run_module(args)

if __name__ == "__main__":
    main()
