#!/usr/bin/env python3
"""
PRAYCG Offline Interpretive Report Generator v1.5.6

A rule-based, offline text interpreter for PRAYCG Master Comprehensive Suite output folders.
It reads CSV/JSON module outputs and writes Markdown/TXT/JSON summaries in plain language.

This is not an AI model. It does not infer private experience, diagnose physiology, prove
consciousness, or certify PRAYCG endpoint validity. It is a deterministic ruleset that helps
users understand the analysis tables without internet access.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import numpy as np
import pandas as pd

VERSION = "1.5.6"
SCHEMA = "PRAYCG_Offline_Interpretive_Report_v1_5_6"

BOUNDARY = (
    "This offline report is a rule-based interpretation aid. It summarizes available module outputs. "
    "It does not prove consciousness, memory formation, OSM biology, hidden-Y mechanisms, clinical effects, "
    "or literal thermodynamic entropy. Self-report is treated as a contextual evidence stream, not proof of internal state."
)


def nrm(s: str) -> str:
    return "".join(ch.lower() for ch in str(s) if ch.isalnum())


def find_table(root: Path, terms: Iterable[str]) -> Optional[Path]:
    terms = [t.lower() for t in terms]
    cands = []
    for p in root.rglob("*.csv"):
        name = p.name.lower()
        if all(t in name for t in terms):
            cands.append(p)
    if not cands:
        return None
    return sorted(cands, key=lambda p: ("tables" not in [q.name for q in p.parents], len(str(p))))[0]


def read_csv(path: Optional[Path]) -> pd.DataFrame:
    if not path or not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def read_json(path: Optional[Path]) -> Dict[str, Any]:
    if not path or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def col(df: pd.DataFrame, *names: str) -> Optional[str]:
    if df.empty:
        return None
    cmap = {nrm(c): c for c in df.columns}
    for name in names:
        k = nrm(name)
        if k in cmap:
            return cmap[k]
    for name in names:
        k = nrm(name)
        for kk, cc in cmap.items():
            if k and (k in kk or kk in k):
                return cc
    return None


def fnum(x: Any, default: float = np.nan) -> float:
    try:
        v = float(x)
        return v if math.isfinite(v) else default
    except Exception:
        return default


def bval(x: Any) -> bool:
    if isinstance(x, bool):
        return x
    return str(x).strip().lower() in {"true", "1", "yes", "pass", "passed", "y"}


def get_first(df: pd.DataFrame, name: str, default: Any = "") -> Any:
    if df.empty:
        return default
    c = col(df, name)
    if c is None or not len(df):
        return default
    return df.iloc[0].get(c, default)


def table_paths(root: Path) -> Dict[str, Optional[Path]]:
    return {
        "module_registry": find_table(root, ["module", "registry"]),
        "module_tier": find_table(root, ["tier", "map"]),
        "als_qc": find_table(root, ["als", "qc"]),
        "stream_inventory": find_table(root, ["stream", "inventory"]),
        "phase_summary": find_table(root, ["phase", "feature", "summary"]),
        "amred_anchor": find_table(root, ["amred", "anchor", "endpoint"]),
        "amred_summary": find_table(root, ["amred", "primary", "summary"]),
        "mred_peak_res_anchor": find_table(root, ["mred", "peak", "resolution", "anchor"]),
        "mred_peak_res_summary": find_table(root, ["mred", "peak", "resolution", "run", "summary"]),
        "mred_event": find_table(root, ["mred", "event"]),
        "candidate_kht": find_table(root, ["candidate", "kht"]),
        "nupi_summary": find_table(root, ["nupi", "run", "summary"]),
        "tti_global": find_table(root, ["tti", "global"]),
        "cii_anchor": find_table(root, ["cii", "anchor"]),
        "cet_model": find_table(root, ["cet", "model", "summary"]),
        "eet": find_table(root, ["eet", "echo"]),
        "mred_itp": find_table(root, ["mred", "itp", "anchor"]),
        "ocm_rsm": find_table(root, ["rsm", "cue"]),
        "rsm_corr": find_table(root, ["rsm", "correlation"]),
        "baseline2": find_table(root, ["baseline1", "baseline2"]),
        "dga_branch": find_table(root, ["dga", "branch", "gate"]),
        "dga_summary": find_table(root, ["dga", "gate", "dissociation"]),
        "dga_anchor": find_table(root, ["dga", "gate", "adjusted"]),
        "selfreport_all": find_table(root, ["selfreport", "all"]),
        "branch_core": find_table(root, ["branch", "core"]),
        "final_master": find_table(root, ["final", "master"]),
        "confound": find_table(root, ["confound"]),
    }


def ensure_mred_peak_resolution(root: Path, out_dir: Optional[Path] = None) -> None:
    if find_table(root, ["mred", "peak", "resolution", "anchor"]):
        return
    script = Path(__file__).with_name("praycg_mred_peak_resolution_module_v1_5_5.py")
    if not script.exists():
        return
    cmd = [sys.executable, str(script), "--analysis-folder", str(root)]
    if out_dir:
        cmd += ["--out-dir", str(out_dir)]
    try:
        subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=90)
    except Exception:
        pass


def summarize_qc(d: Dict[str, pd.DataFrame], paths: Dict[str, Optional[Path]]) -> List[str]:
    lines = ["## 1. Data and QC status", ""]
    if not d["module_registry"].empty:
        lines.append(f"The module registry was found: `{Path(paths['module_registry']).name}`.")
    else:
        lines.append("No module registry was found. The report will summarize whatever tables are available.")
    if not d["als_qc"].empty:
        df = d["als_qc"]
        text = []
        for _, r in df.head(5).iterrows():
            branch = r.get(col(df, "branch", "phase", "condition") or "", "branch")
            status_col = col(df, "result", "status", "pass", "detected")
            text.append(f"{branch}: {r.get(status_col, '') if status_col else 'recorded'}")
        lines.append("ALS/timing QC table found. Summary: " + "; ".join(text) + ".")
    else:
        lines.append("No ALS start-pulse QC table was found. Timing-grade claims should be kept cautious unless another timing report exists.")
    if not d["stream_inventory"].empty:
        lines.append("Stream inventory found. Use it to check whether EEG/autonomic/ALS streams were actually available before overinterpreting missing panels.")
    if not d["phase_summary"].empty:
        lines.append("Phase-level feature summary found. This supports branch-level comparisons across Control, Target, Override, washouts, and baselines.")
    lines.append("")
    return lines


def summarize_amred(d: Dict[str, pd.DataFrame]) -> List[str]:
    lines = ["## 2. Boxed primary endpoint path: A-MRED", ""]
    df = d["amred_anchor"]
    if df.empty:
        lines.append("A-MRED anchor endpoint table was not found. The primary endpoint cannot be summarized from this folder.")
        lines.append("")
        return lines
    pass_col = col(df, "A_MRED_pass")
    aid_col = col(df, "anchor_id")
    claim_col = col(df, "claim_level")
    n = len(df)
    passes = int(df[pass_col].apply(bval).sum()) if pass_col else 0
    lines.append(f"A-MRED evaluated **{n}** anchor rows and found **{passes}** A-MRED pass rows.")
    if passes:
        sub = df[df[pass_col].apply(bval)] if pass_col else pd.DataFrame()
        ids = [str(x) for x in sub[aid_col].head(5).tolist()] if aid_col else []
        lines.append("Passing/candidate anchors: " + ", ".join(f"`{x}`" for x in ids) + ".")
        if claim_col:
            claims = sorted(set(str(x) for x in sub[claim_col].dropna().tolist()))
            lines.append("Claim-level labels on passing rows: " + ", ".join(f"`{x}`" for x in claims) + ".")
            if any("estimated" in x.lower() or "caution" in x.lower() for x in claims):
                lines.append("Caution: at least one pass is timing- or claim-level-cautioned. Treat it as pilot-positive unless frame-verified timing and timing QC are clean.")
    else:
        lines.append("No strict A-MRED pass is available in this folder. Secondary and exploratory modules can still be useful, but they should not be treated as confirmatory endpoints.")
    lines.append("")
    return lines


def summarize_peak_resolution(d: Dict[str, pd.DataFrame]) -> List[str]:
    lines = ["## 3. MRED-Peak vs MRED-Resolution", ""]
    s = d["mred_peak_res_summary"]
    a = d["mred_peak_res_anchor"]
    if s.empty or a.empty:
        lines.append("MRED-Peak / MRED-Resolution outputs were not found or could not be generated. This endpoint-compression section is unavailable.")
        lines.append("")
        return lines
    row = s.iloc[0]
    lines.append(f"Anchors evaluated: **{int(fnum(row.get(col(s,'anchor_count') or ''),0))}**.")
    lines.append(f"Strict or strict-cautioned MRED-Peak passes: **{int(fnum(row.get(col(s,'strict_peak_pass_count') or ''),0))}**.")
    lines.append(f"Soft MRED-Peak candidates: **{int(fnum(row.get(col(s,'soft_peak_candidate_count') or ''),0))}**.")
    lines.append(f"MRED-Resolution candidates: **{int(fnum(row.get(col(s,'resolution_candidate_count') or ''),0))}**.")
    interp_col = col(s, "overall_interpretation")
    if interp_col:
        lines.append("")
        lines.append(str(row.get(interp_col, "")))
    if not a.empty:
        peak_col = col(a, "mred_peak_score")
        res_col = col(a, "mred_resolution_score")
        aid_col = col(a, "anchor_id")
        pg_col = col(a, "mred_peak_gate")
        rg_col = col(a, "mred_resolution_gate")
        if peak_col and aid_col:
            top = a.sort_values(peak_col, ascending=False).iloc[0]
            lines.append("")
            lines.append(f"Top peak candidate: `{top.get(aid_col)}` with score `{fnum(top.get(peak_col),0):.3f}` and gate `{top.get(pg_col,'') if pg_col else ''}`.")
        if res_col and aid_col:
            top = a.sort_values(res_col, ascending=False).iloc[0]
            lines.append(f"Top resolution candidate: `{top.get(aid_col)}` with score `{fnum(top.get(res_col),0):.3f}` and gate `{top.get(rg_col,'') if rg_col else ''}`.")
    lines.append("")
    return lines


def summarize_secondary(d: Dict[str, pd.DataFrame]) -> List[str]:
    lines = ["## 4. Secondary summary modules", ""]
    if not d["tti_global"].empty:
        df = d["tti_global"]
        tcol = col(df, "TTI", "TTI_global", "thermodynamictheftindex")
        if tcol:
            val = fnum(df.iloc[0].get(tcol))
            if math.isfinite(val):
                direction = "Target-favoring reception/extraction contrast" if val > 0 else "Override/control-favoring or ambiguous reception/extraction contrast"
                lines.append(f"TTI: `{val:.3f}` — {direction}.")
        else:
            lines.append("TTI global table found, but no recognizable TTI column was detected.")
    else:
        lines.append("TTI global summary was not found.")
    if not d["nupi_summary"].empty:
        df = d["nupi_summary"]
        ncol = col(df, "NUPI")
        ccol = col(df, "classification")
        rcol = col(df, "RDI")
        acol = col(df, "ALI")
        parts = []
        if acol: parts.append(f"ALI `{fnum(df.iloc[0].get(acol),np.nan):.3f}`")
        if rcol: parts.append(f"RDI `{fnum(df.iloc[0].get(rcol),np.nan):.3f}`")
        if ncol: parts.append(f"NUPI `{fnum(df.iloc[0].get(ncol),np.nan):.3f}`")
        if ccol: parts.append(f"classification `{df.iloc[0].get(ccol)}`")
        lines.append("NUPI: " + ", ".join(parts) + ".")
    if not d["cii_anchor"].empty:
        df = d["cii_anchor"]
        cii = col(df, "CII")
        cond = col(df, "condition")
        if cii and cond:
            means = df.groupby(df[cond].astype(str).str.lower())[cii].mean(numeric_only=True).to_dict()
            lines.append("CII mean by condition: " + ", ".join(f"{k} `{v:.3f}`" for k, v in means.items()) + ".")
        else:
            lines.append("CII anchor table found, but condition/CII columns were not recognized.")
    if not d["cet_model"].empty:
        df = d["cet_model"]
        cv_cols = [c for c in df.columns if "cv" in c.lower() or "r2" in c.lower() or "R²" in c]
        if cv_cols:
            lines.append("CET/CET-R model table found. Review R² / blocked-CV columns to judge whether stimulus regressors explain the physiological proxy. Negative blocked-CV generally means poor generalization.")
        else:
            lines.append("CET/CET-R table found, but no recognizable R²/CV columns were detected.")
    lines.append("")
    return lines


def summarize_exploratory(d: Dict[str, pd.DataFrame]) -> List[str]:
    lines = ["## 5. Exploratory / convergence modules", ""]
    if not d["candidate_kht"].empty:
        lines.append("CandidateLocal KHT-topo/MRED event table found. Treat this as exploratory coupling/convergence unless promoted through A-MRED or BIT-style gates.")
    if not d["eet"].empty:
        sim = col(d["eet"], "cosine_similarity_state_vector", "similarity")
        if sim:
            best = pd.to_numeric(d["eet"][sim], errors="coerce").max()
            lines.append(f"EET echo table found. Maximum state-vector similarity observed: `{best:.3f}`. This is after-state resemblance, not proof of replay or memory.")
    if not d["mred_itp"].empty:
        lines.append("MRED-ITP table found. ACG/OCU complexity/blink markers are convergence aids, not proof of thermodynamic entropy reduction or memory encoding.")
    if not d["ocm_rsm"].empty or not d["rsm_corr"].empty:
        lines.append("OCM/RSM/CVB outputs found. These are Override-task diagnostics: cue recognition, working-memory load, arithmetic stall, cue legibility, and possible visual strain. They should not be read as narrative meaning endpoints.")
    if not any(not d[k].empty for k in ["candidate_kht", "eet", "mred_itp", "ocm_rsm", "rsm_corr"]):
        lines.append("No exploratory/convergence module tables were detected.")
    lines.append("")
    return lines



def summarize_dga(d: Dict[str, pd.DataFrame]) -> List[str]:
    lines = ["## 4b. DGA - Decoder Gate Availability", ""]
    s = d.get("dga_summary", pd.DataFrame())
    b = d.get("dga_branch", pd.DataFrame())
    if s.empty:
        lines.append("DGA tables were not found. Decoder-gate availability and gate-dissociation interpretation is unavailable for this folder.")
        lines.append("")
        return lines
    row = s.iloc[0]
    cls_col = col(s, "classification")
    gdi_col = col(s, "gate_dissociation_index")
    tg_col = col(s, "target_gate")
    og_col = col(s, "override_gate")
    if cls_col:
        lines.append(f"DGA classification: `{row.get(cls_col)}`.")
    if gdi_col:
        lines.append(f"Gate Dissociation Index: `{fnum(row.get(gdi_col),np.nan):.3f}`.")
    if tg_col and og_col:
        lines.append(f"Target gate `{fnum(row.get(tg_col),np.nan):.3f}`; Override gate `{fnum(row.get(og_col),np.nan):.3f}`.")
    if not b.empty:
        branch_col = col(b, "branch")
        gate_col = col(b, "decoder_gate_availability")
        sa_col = col(b, "semantic_access")
        ei_col = col(b, "emotional_integration")
        if branch_col and gate_col:
            parts=[]
            for _,r in b.iterrows():
                parts.append(f"{r.get(branch_col)} gate `{fnum(r.get(gate_col),np.nan):.3f}`" + (f", SA `{fnum(r.get(sa_col),np.nan):.3f}`" if sa_col else "") + (f", EI `{fnum(r.get(ei_col),np.nan):.3f}`" if ei_col else ""))
            lines.append("Branch gate summary: " + "; ".join(parts[:6]) + ".")
    lines.append("DGA is an interpretation layer: it estimates whether semantic access, decoder availability, emotional integration, task extraction, and confound burden made the gate available. It is not proof of mechanism.")
    lines.append("")
    return lines

def summarize_selfreport(d: Dict[str, pd.DataFrame]) -> List[str]:
    lines = ["## 6. Self-report and confound context", ""]
    if not d["final_master"].empty:
        df = d["final_master"]
        lines.append("Final master self-report table found. Use it as context, not proof.")
    if not d["branch_core"].empty:
        df = d["branch_core"]
        bcol = col(df, "branch_label", "branch", "condition")
        mcol = col(df, "Meaning")
        acol = col(df, "Absorption")
        if bcol and mcol:
            vals = []
            for _, r in df.iterrows():
                vals.append(f"{r.get(bcol)} meaning `{r.get(mcol)}`" + (f", absorption `{r.get(acol)}`" if acol else ""))
            lines.append("Branch self-report: " + "; ".join(vals[:6]) + ".")
    if not d["confound"].empty:
        lines.append("Confound report table(s) found. High confound burden should lower claim strength or trigger veto, depending on the endpoint.")
    lines.append("Interpretive boundary: self-report can constrain or contextualize physiology, but it does not prove internal state or mechanism.")
    lines.append("")
    return lines


def make_report(root: Path, run_label: str, d: Dict[str, pd.DataFrame], paths: Dict[str, Optional[Path]]) -> str:
    lines = []
    lines.append("# PRAYCG Offline Interpretive Report")
    lines.append("")
    lines.append(f"Schema: `{SCHEMA}`  ")
    lines.append(f"Version: `{VERSION}`  ")
    lines.append(f"Run label: `{run_label or root.name}`  ")
    lines.append(f"Analysis folder: `{root}`")
    lines.append("")
    lines.append("## Boundary")
    lines.append(BOUNDARY)
    lines.append("")
    lines.append("## Recommended interpretation hierarchy")
    lines.append("")
    lines.append("**BOXED PRIMARY PATH:** Timing/QC + StimulusFingerprint/CET-R + artifact/confound gates → A-MRED / MRED-Peak-Resolution endpoint compression.")
    lines.append("")
    lines.append("**SECONDARY:** NIP/BIT/CII/IAQ, TTI, NUPI.")
    lines.append("")
    lines.append("**EXPLORATORY / CONVERGENCE:** KHT-topo, NAST, EET, MRED-ITP/ACG/OCU, OCM/RSM/CVB/Squint, LSO where applicable.")
    lines.append("")
    lines.extend(summarize_qc(d, paths))
    lines.extend(summarize_amred(d))
    lines.extend(summarize_peak_resolution(d))
    lines.extend(summarize_secondary(d))
    lines.extend(summarize_dga(d))
    lines.extend(summarize_exploratory(d))
    lines.extend(summarize_selfreport(d))
    lines.append("## 7. Next-step guidance")
    lines.append("")
    lines.append("- Treat strict A-MRED/MRED-Peak passes as strongest only when anchors were locked before acquisition and timing QC passed.")
    lines.append("- Treat MRED-Resolution as strongest when Baseline2, EET/NUPI, autonomic recovery, and self-report echo converge.")
    lines.append("- If gamma artifacts, missing ALS, missing EOG/EMG, or unverified anchor timing are present, lower the claim grade.")
    lines.append("- Use this report as a map of the output folder, not as a substitute for visual inspection and replication.")
    lines.append("")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Offline PRAYCG Master Suite interpretation report generator v1.5.5")
    ap.add_argument("--analysis-folder", required=True, help="Master Comprehensive output folder.")
    ap.add_argument("--out-dir", default="", help="Output directory. Defaults to <analysis-folder>/reports/offline_interpretation.")
    ap.add_argument("--run-label", default="")
    ap.add_argument("--auto-run-mred-peak-resolution", action="store_true", help="Generate MRED-Peak/Resolution tables if absent.")
    ap.add_argument("--write-json", action="store_true", default=True)
    args = ap.parse_args(argv)

    root = Path(args.analysis_folder).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else root / "reports" / "offline_interpretation"
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.auto_run_mred_peak_resolution:
        ensure_mred_peak_resolution(root, root / "tables")

    paths = table_paths(root)
    d = {k: read_csv(v) for k, v in paths.items()}
    report = make_report(root, args.run_label, d, paths)

    md = out_dir / "offline_interpretive_report.md"
    txt = out_dir / "offline_interpretive_report.txt"
    js = out_dir / "offline_interpretive_report_summary.json"
    md.write_text(report, encoding="utf-8")
    txt.write_text(report, encoding="utf-8")

    summary = {
        "schema": SCHEMA,
        "version": VERSION,
        "analysis_folder": str(root),
        "run_label": args.run_label or root.name,
        "boundary": BOUNDARY,
        "tables_detected": {k: str(v) if v else "" for k, v in paths.items()},
        "outputs": {"markdown": str(md), "text": str(txt), "json": str(js)},
    }
    js.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"status": "ok", "outputs": summary["outputs"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
