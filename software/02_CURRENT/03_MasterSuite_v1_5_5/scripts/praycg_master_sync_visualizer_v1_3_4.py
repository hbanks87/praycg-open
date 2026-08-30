#!/usr/bin/env python3
"""PRAYCG MasterSync Visualizer v1.3.1.

Adds two explicit render modes:
  public_tsc: clean explanatory render for showing at TSC / public demos.
  lab: dense diagnostic render for internal QC.

Patch features:
  - GUI radio selector for Public/TSC vs Lab.
  - feature availability diagnostics; missing signals are labeled or omitted.
  - robust graph scaling to avoid muted traces from outliers.
  - event timebase repair for mixed branch-relative vs raw-LSL seconds.
  - richer panel presets for MeaningGamma/TSP/theta, task/extraction, autonomics, ALS/artifact.
  - sidecar diagnostics for panels, features, events, and report.

Boundary: visualization/audit only; does not certify PR-AYC-G endpoint validity, meaning,
OSM, hidden-Y biology, or human EEG mechanism.
"""
from __future__ import annotations

import argparse, csv, json, math, re, sys, traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
try:
    import pandas as pd
except Exception:
    pd = None
try:
    import cv2
except Exception:
    cv2 = None
try:
    import praycg_master_sync_visualizer_v1_2 as legacy
except Exception:
    legacy = None

VERSION = "1.3.3"

BGR = {
    "theta": (255,255,0), "gamma": (255,0,255), "meaning": (80,230,255), "tsp": (255,190,80),
    "enc": (100,255,160), "task": (60,80,255), "alpha": (210,210,60), "hr": (40,80,255),
    "hrv": (0,180,255), "api": (0,220,255), "resp": (0,230,90), "als": (255,255,255),
    "artifact": (60,60,220), "visual": (180,160,255), "tti": (70,255,180), "default": (220,220,220)
}
EVENT_BGR = {
    "protocol": (130,130,130), "annotation": (80,210,80), "candidate_kht": (60,255,170),
    "kht_topo": (60,255,170), "mred": (120,255,120), "nast": (255,220,80),
    "tti": (70,255,180), "tti_positive": (70,255,180), "tti_negative": (60,100,255),
    "topo_osm": (180,255,120), "gamma_scalpel": (80,80,255), "tsp": (255,180,70),
    "g2theta": (255,120,255), "postpeak_pncc": (80,255,255), "ocm": (80,180,255),
    "rsm": (60,170,255), "cvb": (50,150,255), "squint": (80,80,220),
    "artifact": (50,50,180), "als": (255,255,255), "nip": (90,255,220), "bit": (40,255,210), "cii": (80,210,255), "iaq": (60,180,255), "cet": (220,220,80), "eet": (200,160,255), "cet_eet": (210,190,255), "immersion": (90,255,220), "mred_itp": (255,210,90), "mred_itp_candidate": (255,235,60), "acg_complexity": (180,255,60), "ocu_blink_release": (255,160,90), "itp": (255,210,90), "amred": (255,120,220), "amred_primary": (255,80,220), "primary_endpoint": (255,120,220), "other": (160,160,160)
}
PUBLIC_CATS = {"annotation","candidate_kht","kht_topo","mred","tti","tti_positive","topo_osm","g2theta","postpeak_pncc","nip","bit","cii","iaq","cet","eet","cet_eet","immersion","mred_itp","mred_itp_candidate","acg_complexity","ocu_blink_release","itp","amred","amred_primary","primary_endpoint","protocol"}

@dataclass
class VisualEvent:
    start_sec: float
    end_sec: float
    label: str
    category: str = "other"
    source: str = "unknown"
    raw_start_sec: Optional[float] = None
    raw_end_sec: Optional[float] = None
    timebase_repair: str = "none"

@dataclass
class Panel:
    title: str
    series: List[Tuple[str, str, Tuple[int,int,int]]]
    mode: str = "robust_z"
    y_range: Optional[Tuple[float,float]] = None
    missing_note: str = ""

# -------------------------- utilities --------------------------

def ensure_runtime():
    miss=[]
    if pd is None: miss.append("pandas")
    if cv2 is None: miss.append("opencv-python")
    if legacy is None: miss.append("praycg_master_sync_visualizer_v1_2.py")
    if miss: raise RuntimeError("Missing runtime dependency: "+", ".join(miss))

def eprint(*a): print(*a, file=sys.stderr)

def robust_z(x, eps=1e-9):
    y=np.asarray(x,dtype=float).copy(); y[~np.isfinite(y)]=np.nan
    if not np.any(np.isfinite(y)): return np.full_like(y,np.nan,dtype=float)
    med=np.nanmedian(y); mad=np.nanmedian(np.abs(y-med))
    scale=(1.4826*mad) if np.isfinite(mad) and mad>eps else (np.nanstd(y) if np.nanstd(y)>eps else 1.0)
    return (y-med)/(scale+eps)

def num(s):
    if pd is not None and hasattr(s,"to_numpy"): return pd.to_numeric(s,errors="coerce").to_numpy(dtype=float)
    out=[]
    for v in list(s):
        try: out.append(float(v))
        except Exception: out.append(np.nan)
    return np.asarray(out,dtype=float)

def read_json(p):
    with open(p,"r",encoding="utf-8") as f: return json.load(f)

def write_json(p,obj):
    with open(p,"w",encoding="utf-8") as f: json.dump(obj,f,indent=2,ensure_ascii=False)

def video_info(path):
    cap=cv2.VideoCapture(str(path))
    if not cap.isOpened(): raise RuntimeError(f"Could not open video: {path}")
    fps=cap.get(cv2.CAP_PROP_FPS) or 30.0; frames=cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0.0
    w=cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0.0; h=cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0.0
    cap.release(); return {"fps":float(fps),"frame_count":float(frames),"width":float(w),"height":float(h),"duration_sec":float(frames/fps) if fps and frames else 0.0}

def slug(s): return re.sub(r"[^A-Za-z0-9_.-]+","_",str(s)).strip("_") or "item"

# -------------------------- features --------------------------

TIME_CANDS=["time_sec","rel_time_sec","time","t_sec","seconds","t","condition_offset_sec","phase_time_sec"]

def detect_time_col(df):
    lower={c.lower():c for c in df.columns}
    for c in TIME_CANDS:
        if c in lower: return lower[c]
    for c in df.columns:
        cl=c.lower()
        if "time" in cl and "unix" not in cl and "lsl" not in cl: return c
    return None

def find_cols(df, include, exclude=()):
    out=[]
    for c in df.columns:
        cl=str(c).lower()
        if any(i.lower() in cl for i in include) and not any(e.lower() in cl for e in exclude):
            try:
                pd.to_numeric(df[c], errors="coerce")
                out.append(c)
            except Exception: pass
    return out

def feature_diag(df, time_col="time_sec"):
    rows=[]
    for c in df.columns:
        if c==time_col: continue
        x=pd.to_numeric(df[c], errors="coerce"); n=int(x.notna().sum()); uniq=int(x.dropna().nunique()) if n else 0
        sd=float(x.std()) if n>=2 else float("nan"); vals=x.to_numpy(dtype=float); vals=vals[np.isfinite(vals)]
        rows.append({"column":c,"non_null":n,"unique":uniq,"std":sd,"median":float(np.nanmedian(vals)) if vals.size else np.nan,"p05":float(np.nanpercentile(vals,5)) if vals.size else np.nan,"p95":float(np.nanpercentile(vals,95)) if vals.size else np.nan,"usable":bool(n>=3 and uniq>=3 and np.isfinite(sd) and sd>1e-9),"status":"usable" if n>=3 and uniq>=3 and np.isfinite(sd) and sd>1e-9 else ("missing_all_nan" if n==0 else "constant_or_nearly_constant")})
    return pd.DataFrame(rows)

def filter_for_condition(df, condition):
    try: return legacy.filter_feature_dataframe_for_condition(df, condition)
    except Exception: pass
    c=str(condition or "full").lower()
    if c in {"full","auto","all",""}: return df,"No condition filter applied."
    cond_cols=[col for col in df.columns if col.lower() in {"condition","phase","branch","arm","block"}]
    if not cond_cols: return df,"Feature CSV has no condition/phase/branch column; no filter applied."
    col=cond_cols[0]; aliases={"target":["target"],"control":["control","scrambled"],"override":["override","contextual","analytic"]}.get(c,[c])
    mask=df[col].astype(str).str.lower().str.contains("|".join(map(re.escape,aliases)), regex=True, na=False)
    if mask.sum()==0: return df,f"No rows matched {c}; no filter applied."
    return df.loc[mask].copy(), f"Filtered feature CSV by column '{col}' for condition '{c}': {int(mask.sum())} rows kept."

def resample_df(df, step, duration=None):
    tcol=detect_time_col(df)
    if tcol is None: src_t=np.arange(len(df))*step; note="No time column; using row index."
    else:
        src_t=num(df[tcol]);
        if np.any(np.isfinite(src_t)): src_t=src_t-float(np.nanmin(src_t))
        note=f"Using time column '{tcol}' reset to zero."
    if duration is None or duration<=0: duration=float(np.nanmax(src_t)) if np.any(np.isfinite(src_t)) else len(df)*step
    out_t=np.arange(0,max(step,float(duration))+1e-9,step); out=pd.DataFrame({"time_sec":out_t})
    mt=np.isfinite(src_t)
    for c in df.columns:
        if c==tcol: continue
        x=pd.to_numeric(df[c],errors="coerce").to_numpy(dtype=float); m=mt & np.isfinite(x)
        if m.sum()>=2:
            order=np.argsort(src_t[m]); tt=src_t[m][order]; xx=x[m][order]; ut,idx=np.unique(tt,return_index=True)
            if len(ut)>=2:
                yy=np.interp(out_t, ut, xx[idx]); yy[out_t<ut[0]]=np.nan; yy[out_t>ut[-1]]=np.nan
            else: yy=np.full_like(out_t,np.nan,dtype=float)
        else: yy=np.full_like(out_t,np.nan,dtype=float)
        out[c]=yy
    return out,note,tcol

def load_features(args):
    warnings=[]; duration=float(args.duration) if args.duration else None
    if args.video and (duration is None or duration<=0):
        try: duration=video_info(args.video)["duration_sec"]
        except Exception as exc: warnings.append(f"Could not infer video duration: {exc}")
    analysis_root=args.analysis_out; feature=args.features
    try:
        aroot,feat,iw=legacy.resolve_analysis_and_feature_inputs(args); warnings += list(iw or [])
        if aroot: analysis_root=args.analysis_out=aroot
        if feat and not feature: feature=args.features=feat
    except Exception as exc: warnings.append(f"Could not auto-resolve feature CSV: {exc}")
    phase={"condition":args.condition,"found":False,"warnings":[]}
    if args.xdf and args.condition not in {"full","auto",""}:
        try:
            phase=legacy.resolve_condition_phase_from_xdf(args.xdf,args.condition,args.condition_prepad,args.condition_postpad)
            if phase.get("found") and (duration is None or duration<=0): duration=float(phase["duration_sec"])
        except Exception as exc: warnings.append(f"Could not resolve branch markers: {exc}")
    if args.demo:
        ft,_=legacy.make_demo_features(duration_sec=duration or 30, step_sec=args.feature_step)
        df=pd.DataFrame({"time_sec":ft.time_sec,"theta":ft.theta,"gamma":ft.gamma,"hr":ft.hr,"hrv":ft.hrv,"api_a":ft.api_a,"resp":ft.resp,"als":ft.als})
        return df,{"mode":"demo","phase_window":phase,"feature_filter_note":"demo"},warnings
    if feature:
        raw=pd.read_csv(feature); filt,note=filter_for_condition(raw,args.condition); df,res_note,tcol=resample_df(filt,args.feature_step,duration)
        return df,{"mode":"feature_csv","feature_csv":feature,"raw_rows":len(raw),"filtered_rows":len(filt),"feature_filter_note":note,"resample_note":res_note,"source_time_col":tcol,"phase_window":phase},warnings
    if args.xdf:
        tb=legacy.parse_band(args.theta_band,(4,8)); gb=legacy.parse_band(args.gamma_band,(30,45)); anchor=args.anchor_marker
        if phase.get("found") and not anchor: anchor=str(phase.get("start_regex",""))
        ft,evs,xrep=legacy.features_from_xdf(args.xdf,duration_sec=duration,step_sec=args.feature_step,theta_band=tb,gamma_band=gb,eeg_stream_name=args.eeg_stream,aux_stream_name=args.aux_stream,cardiac_stream_name=args.cardiac_stream,resp_stream_name=args.resp_stream,anchor_marker_regex=anchor,als_aux_channel=args.als_aux_channel)
        df=pd.DataFrame({"time_sec":ft.time_sec,"theta":ft.theta,"gamma":ft.gamma,"hr":ft.hr,"hrv":ft.hrv,"api_a":ft.api_a,"resp":ft.resp,"als":ft.als})
        return df,{"mode":"xdf","xdf_report":xrep,"phase_window":phase},warnings
    raise RuntimeError("Choose an XDF, Feature CSV, or Analysis folder.")

# -------------------------- events --------------------------

def collect_event_paths(args):
    paths=[]
    if args.analysis_out:
        try: paths += legacy.collect_analysis_output_events(args.analysis_out)
        except Exception as exc: eprint(f"WARNING collect events: {exc}")
        # v1.3.1: add NIP/BIT/CII/IAQ/CET/EET overlay/event files when present
        try:
            tables = Path(args.analysis_out) / "tables"
            for name in [
                "nip_cet_eet_visual_overlay.csv", "nip_visual_overlay.csv", "bit_event_table.csv",
                "cii_anchor_integrals.csv", "iaq_target_override_table.csv", "cet_eet_visual_overlay.csv",
                "cet_tracking_summary.csv", "eet_endogenous_echo_tracking.csv", "mred_itp_visual_overlay.csv", "acg_event_table.csv", "ocu_event_table.csv", "mred_itp_anchor_summary.csv", "amred_visual_overlay.csv", "amred_anchor_endpoint_table.csv", "amred_primary_endpoint_summary.csv", "nupi_visual_overlay.csv", "nupi_anchor_polarity_table.csv", "nupi_run_summary.csv"
            ]:
                p = tables / name
                if p.exists(): paths.append(str(p))
        except Exception as exc:
            eprint(f"WARNING collect NIP/CET events: {exc}")
    if args.events:
        for item in str(args.events).split(","):
            item=item.strip().strip('"')
            if item: paths.append(item)
    out=[]; seen=set()
    for p in paths:
        if p not in seen: seen.add(p); out.append(p)
    return out

def infer_cat(row,label,source):
    text=(str(label)+" "+str(source)+" "+" ".join(map(str,row.keys()))).lower()
    if "nip" in text or "immersion" in text: return "nip"
    if "bit" in text: return "bit"
    if "cii" in text: return "cii"
    if "iaq" in text or "attenuation" in text: return "iaq"
    if "cet" in text or "entrainment" in text: return "cet"
    if "eet" in text or "echo" in text: return "eet"
    if "tti" in text or "theft" in text: return "tti_positive"
    if "mred" in text or "mr_score" in text or "enc_score" in text: return "mred"
    if "amred" in text or "a-mred" in text or "anchor_locked_mred" in text: return "amred_primary"
    if "mred_itp" in text or "itp" in text: return "mred_itp"
    if "acg" in text or "complexity" in text: return "acg_complexity"
    if "ocu" in text or "blink" in text or "ocular" in text: return "ocu_blink_release"
    if "k_ht" in text or "kht" in text or "candidate_local" in text: return "candidate_kht"
    if "topo" in text: return "topo_osm"
    if "nast" in text: return "nast"
    if "ocm" in text: return "ocm"
    if "rsm" in text: return "rsm"
    if "squint" in text: return "squint"
    if "artifact" in text: return "artifact"
    if "als" in text or "pulse" in text: return "als"
    if "anchor" in text or "annotation" in text: return "annotation"
    return "other"

def event_from_row(row, source):
    lower={str(k).lower():k for k in row.keys()}
    def val(names):
        for n in names:
            if n.lower() in lower: return row[lower[n.lower()]]
        return None
    start=val(["start_sec","onset_sec","time_sec","t_sec","sec","start","onset","peak_sec","taper_sec","event_time_sec","condition_offset_sec","phase_time_sec","anchor_time_sec","anchor_time_lsl","cue_time","cue_onset_sec"])
    end=val(["end_sec","stop_sec","offset_sec","end","stop","condition_end_sec"]); dur=val(["duration_sec","duration","dur_sec"])
    try: s=float(start)
    except Exception: return None
    if end not in [None,""]:
        try: e=float(end)
        except Exception: e=s+0.75
    elif dur not in [None,""]:
        try: e=s+float(dur)
        except Exception: e=s+0.75
    else: e=s+0.75
    if e<=s: e=s+0.75
    label=val(["label","event","event_label","marker","name","type","anchor_id","anchor","description","anchor_metric","mred_quadrant","condition"])
    parts=[]
    for k in ["condition","anchor_metric","mred_quadrant","K_HT_topo_local","K_local","MR_score","ENC_score","event_lock_candidate","tti_timewindow"]:
        v=val([k])
        if v not in [None,""] and str(v)!="nan": parts.append(f"{k}={v}")
    label=(str(label)+(" | " if parts else "")+" | ".join(parts)) if label not in [None,""] else (" | ".join(parts) if parts else source)
    cat=val(["category","event_category","class"]); cat=str(cat).lower() if cat not in [None,""] else infer_cat(row,label,source)
    return VisualEvent(s,e,label,cat,source,s,e)

def load_event_files(paths):
    out=[]
    for path in paths:
        p=Path(path)
        if not p.exists(): continue
        try:
            if p.suffix.lower()==".csv":
                df=pd.read_csv(p)
                for _,r in df.iterrows():
                    ev=event_from_row(r.to_dict(),p.name)
                    if ev: out.append(ev)
            elif p.suffix.lower() in {".json",".jsn"}:
                obj=read_json(p); rows=[]
                try: rows=legacy.flatten_json_events(obj,p.name)
                except Exception:
                    if isinstance(obj,list): rows=[x for x in obj if isinstance(x,dict)]
                    elif isinstance(obj,dict): rows=[obj]
                for row in rows:
                    ev=event_from_row(row,p.name)
                    if ev: out.append(ev)
        except Exception as exc: eprint(f"WARNING failed event load {path}: {exc}")
    return out

def event_filter_for_condition(events, condition):
    c=str(condition or "full").lower()
    if c in {"full","auto","all",""}: return events
    out=[]
    for ev in events:
        text=" ".join([ev.label,ev.category,ev.source]).lower()
        mc="control" in text or "scrambled" in text; mt="target" in text; mo="override" in text or "contextual" in text or "analytic" in text
        if c=="control" and (mt or mo): continue
        if c=="target" and (mc or mo): continue
        if c=="override" and (mc or (mt and not mo)): continue
        out.append(ev)
    return out

def load_events(args,duration):
    paths=collect_event_paths(args); events=load_event_files(paths); events=event_filter_for_condition(events,args.condition)
    cats=[c.strip().lower() for c in str(args.categories).split(",") if c.strip()]
    if cats and "all" not in cats: events=[e for e in events if e.category in cats]
    phase=getattr(args,"_phase_info",{}) or {}; start_lsl=None
    if isinstance(phase,dict) and phase.get("found"):
        try: start_lsl=float(phase.get("start_lsl_raw",phase.get("start_lsl")))
        except Exception: start_lsl=None
    rows=[]
    for ev in events:
        rs,re0=ev.start_sec,ev.end_sec; repair="none"
        if start_lsl is not None and ev.start_sec>duration+5:
            ns=ev.start_sec-start_lsl; ne=ev.end_sec-start_lsl
            if -5<=ns<=duration+10: ev.start_sec=ns; ev.end_sec=max(ns+0.1,ne); repair="raw_lsl_minus_branch_start"
        ev.timebase_repair=repair
        rows.append({"label":ev.label[:160],"category":ev.category,"source":ev.source,"raw_start_sec":rs,"raw_end_sec":re0,"render_start_sec":ev.start_sec,"render_end_sec":ev.end_sec,"timebase_repair":repair,"within_duration":bool(-.5<=ev.start_sec<=duration+.5)})
    events=sorted(events,key=lambda e:(e.start_sec,e.end_sec,e.label))
    return events, paths, pd.DataFrame(rows)

# -------------------------- panels --------------------------

def signal_map(df, diag):
    usable=set(diag.loc[diag.usable,"column"].tolist()) if len(diag) else set()
    def choose(incl, excl=()):
        cols=find_cols(df,incl,excl)
        for c in cols:
            if c in usable: return c
        return None
    return {
        "theta":choose(["theta"],["gamma","delta_theta"]), "gamma":choose(["gamma"],["meaninggamma","taskgamma","visualgamma","theta"]),
        "meaninggamma":choose(["meaninggamma","meaning_gamma","pmeaning"]), "tsp":choose(["tsp","temporal_semantic"]),
        "theta_integration":choose(["theta_integration","theta_delta","theta_handoff","theta_carryover"]),
        "taskgamma":choose(["taskgamma","task_gamma","ptask"]), "alpha":choose(["alpha"],["api"]),
        "hr":choose(["heart_rate","hr","bpm"],["hrv","rmssd","sdnn"]), "hrv":choose(["hrv","rmssd","sdnn"]),
        "api_a":choose(["api_a","apia","availability"]), "resp":choose(["resp","breath"]),
        "als":choose(["als","photodiode","pt19","light"]), "artifact":choose(["artifact","p2p","hf_proxy","jaw","blink","squint"]),
        "visual":choose(["visual","luminance","optical_flow","cut_rate"]), "tti":choose(["tti","theft"]),
        "mr":choose(["mr_score","meaning_recognition"]), "enc":choose(["enc_score","encoding"])
    }

def make_panels(mode, df, diag):
    m=signal_map(df,diag); notes=[]
    def s(items):
        out=[]
        for label,key,color in items:
            c=m.get(key)
            if c: out.append((label,c,color))
            else: notes.append(f"{label} unavailable")
        return out
    panels=[]
    if mode=="public_tsc":
        p=s([("MeaningGamma","meaninggamma",BGR["meaning"]),("TSP","tsp",BGR["tsp"]),("Theta/ENC","theta_integration",BGR["enc"])])
        if not p: p=s([("gamma","gamma",BGR["gamma"]),("theta","theta",BGR["theta"])])
        panels.append(Panel("Meaning-state review",p,"robust_z",(-3,3)))
        p=s([("TaskGamma","taskgamma",BGR["task"]),("Alpha/NAST","alpha",BGR["alpha"]),("Artifact","artifact",BGR["artifact"])])
        if p: panels.append(Panel("Extraction / absorption context",p,"robust_z",(-3,3)))
        p=s([("API-A","api_a",BGR["api"]),("HR","hr",BGR["hr"]),("HRV","hrv",BGR["hrv"]),("Resp","resp",BGR["resp"])])
        if p: panels.append(Panel("Body-state context",p,"robust_z",(-3,3)))
        p=s([("ALS","als",BGR["als"]),("Visual","visual",BGR["visual"])])
        if p: panels.append(Panel("Timing / sensory covariates",p,"robust_z",(-3,3)))
    else:
        panels.append(Panel("EEG bands: theta / gamma / alpha",s([("theta","theta",BGR["theta"]),("gamma","gamma",BGR["gamma"]),("alpha","alpha",BGR["alpha"])]),"robust_z_rolling"))
        panels.append(Panel("Meaning modules: MeaningGamma / TSP / MR / ENC",s([("MeaningGamma","meaninggamma",BGR["meaning"]),("TSP","tsp",BGR["tsp"]),("MR","mr",BGR["meaning"]),("ENC","enc",BGR["enc"])]),"robust_z_rolling"))
        panels.append(Panel("Task/extraction: TaskGamma / TTI / artifact",s([("TaskGamma","taskgamma",BGR["task"]),("TTI","tti",BGR["tti"]),("Artifact","artifact",BGR["artifact"])]),"robust_z_rolling"))
        panels.append(Panel("Autonomic: HR / HRV / API-A",s([("HR","hr",BGR["hr"]),("HRV","hrv",BGR["hrv"]),("API-A","api_a",BGR["api"])]),"robust_z_rolling"))
        panels.append(Panel("Respiration / ALS / visual drive",s([("Resp","resp",BGR["resp"]),("ALS","als",BGR["als"]),("Visual","visual",BGR["visual"])]),"robust_z_rolling"))
        for p in panels:
            if not p.series: p.missing_note="No usable signal columns for this diagnostic panel."
    if mode=="public_tsc": panels=[p for p in panels if p.series]
    if not panels: panels=[Panel("Fallback EEG",s([("theta","theta",BGR["theta"]),("gamma","gamma",BGR["gamma"])]),"robust_z",(-3,3),"No usable EEG columns.")]
    return panels,m,notes

def prep_arrays(df, panels):
    out={}
    for p in panels:
        for _,c,_ in p.series:
            if c not in out:
                arr=num(df[c]); out[c]=np.clip(robust_z(arr),-8,8) if p.mode.startswith("robust_z") else arr
    return out

# -------------------------- drawing --------------------------

def blend(img,x1,y1,x2,y2,color,alpha):
    h,w=img.shape[:2]; x1=max(0,min(w,int(x1))); x2=max(0,min(w,int(x2))); y1=max(0,min(h,int(y1))); y2=max(0,min(h,int(y2)))
    if x2<=x1 or y2<=y1: return
    ov=img[y1:y2,x1:x2].copy(); ov[:]=color; cv2.addWeighted(ov,alpha,img[y1:y2,x1:x2],1-alpha,0,dst=img[y1:y2,x1:x2])

def text_block(img,text,x,y,maxw,color=(230,230,230),scale=.42,lh=16):
    words=str(text).split(); line=""; yy=y
    for w in words:
        test=(line+" "+w).strip(); tw=cv2.getTextSize(test,cv2.FONT_HERSHEY_SIMPLEX,scale,1)[0][0]
        if tw>maxw and line:
            cv2.putText(img,line,(x,yy),cv2.FONT_HERSHEY_SIMPLEX,scale,color,1,cv2.LINE_AA); yy+=lh; line=w
        else: line=test
    if line: cv2.putText(img,line,(x,yy),cv2.FONT_HERSHEY_SIMPLEX,scale,color,1,cv2.LINE_AA); yy+=lh
    return yy

def rr(vals, default=(-3,3)):
    y=np.asarray(vals,dtype=float); y=y[np.isfinite(y)]
    if len(y)<3: return default
    lo,hi=np.nanpercentile(y,5),np.nanpercentile(y,95)
    if not np.isfinite(lo) or not np.isfinite(hi) or hi<=lo: return default
    pad=max(.2,.15*(hi-lo)); lo-=pad; hi+=pad
    lo=max(lo,-5); hi=min(hi,5)
    if hi-lo<1: mid=(hi+lo)/2; lo=mid-.5; hi=mid+.5
    return float(lo),float(hi)

def draw_panel(img, rect, panel, df, arrs, events, t, win, mode):
    x1,y1,x2,y2=rect; cv2.rectangle(img,(x1,y1),(x2,y2),(45,45,45),1)
    cv2.putText(img,panel.title[:100],(x1+8,y1+21),cv2.FONT_HERSHEY_SIMPLEX,.54 if mode=="public_tsc" else .48,(235,235,235),1,cv2.LINE_AA)
    pt,pb,pl,pr=y1+32,y2-22,x1+54,x2-12
    cv2.rectangle(img,(pl,pt),(pr,pb),(25,25,25),-1); cv2.rectangle(img,(pl,pt),(pr,pb),(80,80,80),1)
    t0=max(0,t-win); t1=max(win,t) if t<win else t
    for ev in events:
        if ev.end_sec<t0 or ev.start_sec>t1: continue
        ex1=pl+int((max(ev.start_sec,t0)-t0)/max(1e-9,t1-t0)*(pr-pl)); ex2=pl+int((min(ev.end_sec,t1)-t0)/max(1e-9,t1-t0)*(pr-pl))
        if ex2<=ex1: ex2=ex1+2
        blend(img,ex1,pt,ex2,pb,EVENT_BGR.get(ev.category,EVENT_BGR["other"]),.16 if mode=="public_tsc" else .22)
    cv2.line(img,(pr,pt),(pr,pb),(255,255,255),1)
    time=num(df["time_sec"]); mask=(time>=t0)&(time<=t1)
    if panel.y_range is not None and panel.mode!="robust_z_rolling": ymin,ymax=panel.y_range
    else:
        vals=[arrs[c][mask] for _,c,_ in panel.series if c in arrs]
        ymin,ymax=rr(np.concatenate(vals) if vals else np.array([]))
    if ymin<0<ymax:
        zy=pb-int((0-ymin)/max(1e-9,ymax-ymin)*(pb-pt)); cv2.line(img,(pl,zy),(pr,zy),(70,70,70),1)
    cv2.putText(img,f"{ymax:.2g}",(x1+8,pt+5),cv2.FONT_HERSHEY_SIMPLEX,.36,(150,150,150),1,cv2.LINE_AA)
    cv2.putText(img,f"{ymin:.2g}",(x1+8,pb),cv2.FONT_HERSHEY_SIMPLEX,.36,(150,150,150),1,cv2.LINE_AA)
    if not panel.series:
        text_block(img,panel.missing_note or "No usable signals in this panel.",pl+10,pt+35,pr-pl-20,(120,160,255),.48)
    for label,c,color in panel.series:
        yy=arrs.get(c); pts=[]
        if yy is None: continue
        for tt,vv in zip(time[mask],yy[mask]):
            if not np.isfinite(vv): continue
            px=pl+int((tt-t0)/max(1e-9,t1-t0)*(pr-pl)); py=pb-int((vv-ymin)/max(1e-9,ymax-ymin)*(pb-pt)); py=max(pt,min(pb,py)); pts.append((px,py))
        if len(pts)>=2: cv2.polylines(img,[np.asarray(pts,dtype=np.int32)],False,color,2,cv2.LINE_AA)
    lx,ly=pl+4,y2-5
    for label,c,color in panel.series:
        vstr=""; yy=arrs.get(c)
        if yy is not None and len(yy) and np.any(np.isfinite(time)):
            idx=int(np.nanargmin(np.abs(time-min(max(t,time[0]),time[-1]))))
            if np.isfinite(yy[idx]): vstr=f" {yy[idx]:+.2f}"
        txt=f"{label}{vstr}"; cv2.line(img,(lx,ly-6),(lx+14,ly-6),color,2); cv2.putText(img,txt[:24],(lx+18,ly),cv2.FONT_HERSHEY_SIMPLEX,.38,color,1,cv2.LINE_AA); lx+=min(180,70+len(txt)*8)
    cv2.putText(img,f"{t:7.2f}s",(pr-92,y1+21),cv2.FONT_HERSHEY_SIMPLEX,.48,(220,220,220),1,cv2.LINE_AA)
    return {"title":panel.title,"series":[s[0] for s in panel.series],"columns":[s[1] for s in panel.series],"y_min":ymin,"y_max":ymax,"mode":panel.mode,"has_series":bool(panel.series)}

def event_cards(img,events,t,width,y,mode):
    if mode=="public_tsc": evs=[e for e in events if e.category in PUBLIC_CATS and (e.start_sec<=t<=e.end_sec or abs(e.start_sec-t)<=1)]
    else: evs=[e for e in events if e.start_sec<=t<=e.end_sec or abs(e.start_sec-t)<=.75]
    evs=sorted(evs,key=lambda e:(abs(e.start_sec-t),e.start_sec))[:3]
    for ev in evs:
        h=42 if mode=="public_tsc" else 36; color=EVENT_BGR.get(ev.category,EVENT_BGR["other"])
        blend(img,12,y,width-12,y+h,color,.22); cv2.rectangle(img,(12,y),(width-12,y+h),color,1)
        text_block(img,f"{ev.start_sec:6.1f}s | {ev.category} | {ev.label}",20,y+18,width-48,(245,245,245),.45 if mode=="public_tsc" else .40,16)
        y+=h+5

def graph_frame(df,panels,arrs,events,t,width,height,win,mode):
    img=np.zeros((height,width,3),dtype=np.uint8); img[:]=(8,8,8)
    top=34 if mode=="public_tsc" else 28
    title="PRAYCG PUBLIC/TSC REVIEW" if mode=="public_tsc" else "PRAYCG LAB DIAGNOSTIC REVIEW"
    cv2.putText(img,f"{title} | t={t:7.2f}s | window={win:.0f}s",(12,23),cv2.FONT_HERSHEY_SIMPLEX,.62 if mode=="public_tsc" else .52,(240,240,240),1,cv2.LINE_AA)
    margin=12; gap=8; n=max(1,len(panels)); ph=max(72 if mode=="public_tsc" else 60,(height-top-2*margin-gap*(n-1))//n)
    reports=[]; y=top+margin
    for p in panels:
        reports.append(draw_panel(img,(margin,y,width-margin,min(height-margin,y+ph)),p,df,arrs,events,t,win,mode)); y+=ph+gap
    event_cards(img,events,t,width,top+2,mode)
    return img,reports

def compose(vf,gf,width,vh):
    if vf is None or vh<=0: return gf
    h,w=vf.shape[:2]; top=np.zeros((vh,width,3),dtype=np.uint8)
    if h>0 and w>0:
        scale=min(width/w,vh/h); nw,nh=max(1,int(w*scale)),max(1,int(h*scale)); r=cv2.resize(vf,(nw,nh),interpolation=cv2.INTER_AREA); x=(width-nw)//2; y=(vh-nh)//2; top[y:y+nh,x:x+nw]=r
    return np.vstack([top,gf])

def render_video(df,panels,events,args,duration):
    out=Path(args.out).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    fps=float(args.fps); width=int(args.width); mode=args.render_mode; gh=max(int(args.graph_height),700 if mode=="public_tsc" else 760); vh=int(args.video_height)
    cap=None; vinfo={}
    if args.video:
        vinfo=video_info(args.video); duration=min(duration if duration>0 else 1e9,vinfo.get("duration_sec",duration) or duration); cap=cv2.VideoCapture(str(args.video))
        if not cap.isOpened(): raise RuntimeError(f"Could not open video: {args.video}")
    else: vh=0
    total=int(math.ceil(max(.1,duration)*fps)); writer=cv2.VideoWriter(str(out),cv2.VideoWriter_fourcc(*"mp4v"),fps,(width,vh+gh))
    if not writer.isOpened(): raise RuntimeError(f"Could not open VideoWriter: {out}")
    arrs=prep_arrays(df,panels); sample=[]
    try:
        for i in range(total):
            t=i/fps; vf=None
            if cap is not None:
                cap.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,frame=cap.read(); vf=frame if ok else np.zeros((max(1,vh),width,3),dtype=np.uint8)
            gf,reps=graph_frame(df,panels,arrs,events,t,width,gh,float(args.rolling_window),mode)
            if i==min(10,total-1): sample=reps
            writer.write(compose(vf,gf,width,vh))
            if i % int(max(1,fps*10))==0: print(f"Rendered {i}/{total} frames ({100*i/max(1,total):.1f}%)")
    finally:
        writer.release();
        if cap is not None: cap.release()
    return {"out_mp4":str(out),"fps":fps,"duration_sec":duration,"total_frames":total,"out_width":width,"out_height":vh+gh,"stimulus_video":args.video,"stimulus_video_info":vinfo,"graph_height":gh,"video_height":vh,"rolling_window_sec":float(args.rolling_window),"render_mode":mode,"event_count_rendered":len(events)}, sample

# -------------------------- pipeline --------------------------

def write_events(path,events):
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["start_sec","end_sec","category","label","source","raw_start_sec","raw_end_sec","timebase_repair"]); w.writeheader()
        for e in events: w.writerow(e.__dict__)

def run_pipeline(args):
    ensure_runtime()
    if args.render_mode not in {"public_tsc","lab"}: args.render_mode="public_tsc"
    if args.render_mode=="public_tsc" and args.categories.lower()=="all": args.categories=",".join(sorted(PUBLIC_CATS))
    out=Path(args.out or "PRAYCG_MasterSync_v1_3_Render.mp4").resolve(); out_dir=Path(args.out_dir).resolve() if args.out_dir else out.parent; out_dir.mkdir(parents=True,exist_ok=True)
    df,frep,warn=load_features(args); args._phase_info=frep.get("phase_window",{})
    duration=float(args.duration) if args.duration else (float(np.nanmax(num(df["time_sec"]))) if len(df) else .1)
    if args.video:
        try: duration=min(duration if duration>0 else 1e9, video_info(args.video)["duration_sec"])
        except Exception: pass
    diag=feature_diag(df,"time_sec"); panels,colmap,notes=make_panels(args.render_mode,df,diag); events,paths,ediag=load_events(args,duration)
    rrep,psample=render_video(df,panels,events,args,max(.1,duration))
    stem=out.stem
    fcsv=out_dir/f"{stem}_features_used.csv"; ecsv=out_dir/f"{stem}_events_used.csv"; rjson=out_dir/f"{stem}_render_report.json"; dcsv=out_dir/f"{stem}_feature_diagnostics.csv"; tdcsv=out_dir/f"{stem}_event_time_diagnostics.csv"; pcsv=out_dir/f"{stem}_panel_definitions.csv"
    df.to_csv(fcsv,index=False); write_events(ecsv,events); diag.to_csv(dcsv,index=False); ediag.to_csv(tdcsv,index=False); pd.DataFrame([{"panel":p.title,"series_labels":";".join([x[0] for x in p.series]),"columns":";".join([x[1] for x in p.series]),"mode":p.mode,"missing_note":p.missing_note} for p in panels]).to_csv(pcsv,index=False)
    report={"schema":"PRAYCG_MasterSync_Visualizer_Report_v1_3_4","version":VERSION,"render_mode":args.render_mode,"condition_selected":args.condition,"detected_video_branch":legacy.detect_video_branch(args.video) if args.video else "none","phase_window":frep.get("phase_window",{}),"warnings":warn+notes,"render":rrep,"feature_report":frep,"feature_column_mapping":colmap,"panel_sample":psample,"inputs":{"xdf":args.xdf,"feature_csv":args.features,"stimulus_video":args.video,"event_files":paths,"analysis_output_folder":args.analysis_out},"sidecars":{"features_used_csv":str(fcsv),"events_used_csv":str(ecsv),"feature_diagnostics_csv":str(dcsv),"event_time_diagnostics_csv":str(tdcsv),"panel_definitions_csv":str(pcsv),"render_report_json":str(rjson)},"boundary":"Visualization/audit only. Public/TSC mode simplifies display for explanation; Lab mode exposes diagnostics. Neither mode certifies endpoint validity, meaning, OSM, hidden-Y biology, or human EEG mechanism."}
    write_json(rjson,report)
    return {**rrep,"features_csv":str(fcsv),"events_csv":str(ecsv),"report_json":str(rjson),"feature_diagnostics_csv":str(dcsv),"event_time_diagnostics_csv":str(tdcsv),"panel_definitions_csv":str(pcsv)}

def build_arg_parser():
    p=argparse.ArgumentParser(description="PRAYCG MasterSync Visualizer v1.3.1")
    p.add_argument("--gui",action="store_true"); p.add_argument("--demo",action="store_true")
    p.add_argument("--render-mode",choices=["public_tsc","lab"],default="public_tsc")
    p.add_argument("--xdf",default=""); p.add_argument("--features",default=""); p.add_argument("--video",default="")
    p.add_argument("--condition",default="full",choices=["control","target","override","full","auto"])
    p.add_argument("--condition-prepad",type=float,default=0.0); p.add_argument("--condition-postpad",type=float,default=0.0)
    p.add_argument("--events",default=""); p.add_argument("--analysis-out",default=""); p.add_argument("--out",default=""); p.add_argument("--out-dir",default="")
    p.add_argument("--fps",type=float,default=24.0); p.add_argument("--duration",type=float,default=0.0); p.add_argument("--width",type=int,default=1280)
    p.add_argument("--video-height",type=int,default=540); p.add_argument("--graph-height",type=int,default=720); p.add_argument("--rolling-window",type=float,default=30.0)
    p.add_argument("--categories",default="all"); p.add_argument("--anchor-marker",default=""); p.add_argument("--als-aux-channel",type=int,default=1); p.add_argument("--feature-step",type=float,default=.25)
    p.add_argument("--theta-band",default="4,8"); p.add_argument("--gamma-band",default="30,45"); p.add_argument("--eeg-stream",default=""); p.add_argument("--aux-stream",default=""); p.add_argument("--cardiac-stream",default=""); p.add_argument("--resp-stream",default="")
    return p

def launch_gui():
    ensure_runtime()
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    class App(tk.Tk):
        def __init__(self):
            super().__init__(); self.title("PRAYCG MasterSync Visualizer v1.3.1"); self.geometry("860x840")
            self.vars={k:tk.StringVar(value=v) for k,v in {"xdf":"","features":"","video":"","events":"","analysis_out":"","out":str(Path.cwd()/"PRAYCG_MasterSync_v1_3_public_tsc.mp4"),"condition":"target","render_mode":"public_tsc","fps":"24","width":"1280","video_height":"540","graph_height":"720","rolling":"30","als_ch":"1"}.items()}; self.build()
        def row(self,parent,label,key,folder=False,save=False,ftypes=None):
            fr=ttk.Frame(parent); fr.pack(fill="x",pady=4); ttk.Label(fr,text=label,width=22).pack(side="left"); ttk.Entry(fr,textvariable=self.vars[key]).pack(side="left",fill="x",expand=True)
            def b():
                p=filedialog.askdirectory(title=f"Select {label}") if folder else (filedialog.asksaveasfilename(title=f"Select {label}",defaultextension=".mp4",filetypes=ftypes or [("MP4","*.mp4"),("All","*.*")]) if save else filedialog.askopenfilename(title=f"Select {label}",filetypes=ftypes or [("All","*.*")]))
                if p: self.vars[key].set(p)
            ttk.Button(fr,text="Browse Folder" if folder else "Browse",command=b).pack(side="left",padx=3)
        def build(self):
            pad=ttk.Frame(self,padding=10); pad.pack(fill="both",expand=True); ttk.Label(pad,text="PRAYCG MasterSync Visualizer v1.3.1",font=("Arial",16,"bold")).pack(anchor="w")
            lf=ttk.LabelFrame(pad,text="Render mode"); lf.pack(fill="x",pady=8)
            ttk.Radiobutton(lf,text="Public/TSC version — fewer panels, larger labels, event cards",value="public_tsc",variable=self.vars["render_mode"]).pack(anchor="w",padx=8,pady=3)
            ttk.Radiobutton(lf,text="Lab/Diagnostic version — all panels, missing-data labels, rolling robust scale",value="lab",variable=self.vars["render_mode"]).pack(anchor="w",padx=8,pady=3)
            self.row(pad,"XDF","xdf",ftypes=[("XDF","*.xdf"),("All","*.*")]); self.row(pad,"Feature CSV","features",ftypes=[("CSV","*.csv"),("All","*.*")]); self.row(pad,"Stimulus MP4","video",ftypes=[("MP4","*.mp4"),("All","*.*")]); self.row(pad,"Events","events",ftypes=[("CSV/JSON","*.csv *.json"),("All","*.*")]); self.row(pad,"Analysis folder","analysis_out",folder=True)
            fr=ttk.Frame(pad); fr.pack(fill="x",pady=8); ttk.Label(fr,text="Branch / condition",width=22).pack(side="left")
            for val,txt in [("control","Control"),("target","Target"),("override","Contextual Override"),("full","Full")]: ttk.Radiobutton(fr,text=txt,value=val,variable=self.vars["condition"]).pack(side="left",padx=5)
            self.row(pad,"Output MP4","out",save=True,ftypes=[("MP4","*.mp4"),("All","*.*")])
            grid=ttk.Frame(pad); grid.pack(fill="x",pady=6)
            for i,(lab,key) in enumerate([("FPS","fps"),("Width","width"),("Video H","video_height"),("Graph H","graph_height"),("Window sec","rolling"),("ALS ch","als_ch")]): ttk.Label(grid,text=lab).grid(row=i//3,column=(i%3)*2,sticky="e",padx=4,pady=3); ttk.Entry(grid,textvariable=self.vars[key],width=10).grid(row=i//3,column=(i%3)*2+1,sticky="w",padx=4,pady=3)
            ttk.Button(pad,text="Render selected version",command=self.render).pack(pady=8); self.log=tk.Text(pad,height=15); self.log.pack(fill="both",expand=True)
        def ns(self,demo=False): return argparse.Namespace(gui=False,demo=demo,render_mode=self.vars["render_mode"].get(),xdf=self.vars["xdf"].get(),features=self.vars["features"].get(),video=self.vars["video"].get(),condition=self.vars["condition"].get(),condition_prepad=0.0,condition_postpad=0.0,events=self.vars["events"].get(),analysis_out=self.vars["analysis_out"].get(),out=self.vars["out"].get(),out_dir="",fps=float(self.vars["fps"].get()),duration=0.0,width=int(self.vars["width"].get()),video_height=int(self.vars["video_height"].get()),graph_height=int(self.vars["graph_height"].get()),rolling_window=float(self.vars["rolling"].get()),categories="all",anchor_marker="",als_aux_channel=int(self.vars["als_ch"].get()),feature_step=.25,theta_band="4,8",gamma_band="30,45",eeg_stream="",aux_stream="",cardiac_stream="",resp_stream="")
        def render(self):
            if not self.vars["xdf"].get() and not self.vars["features"].get() and not self.vars["analysis_out"].get(): messagebox.showwarning("Missing data","Choose XDF, Feature CSV, or Analysis folder."); return
            try:
                self.log.insert("end",f"Starting {self.vars['render_mode'].get()} render...\n"); self.update_idletasks(); res=run_pipeline(self.ns()); self.log.insert("end",json.dumps(res,indent=2)+"\n"); messagebox.showinfo("Done","Rendered:\n"+res.get("out_mp4",""))
            except Exception as exc: self.log.insert("end",traceback.format_exc()+"\n"); messagebox.showerror("Render failed",str(exc))
    app=App(); app.mainloop(); return 0

def main(argv=None):
    parser=build_arg_parser(); args=parser.parse_args(argv)
    if args.gui or (not args.demo and not args.xdf and not args.features and not args.analysis_out): return launch_gui()
    if not args.out: parser.error("--out is required in CLI mode")
    try: print(json.dumps(run_pipeline(args),indent=2)); return 0
    except Exception as exc: eprint("ERROR:",exc); traceback.print_exc(); return 1
if __name__=="__main__": raise SystemExit(main())
