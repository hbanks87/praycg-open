#!/usr/bin/env python3
"""
PRAYCG DGA_v0.1 - Decoder Gate Availability / Gate Dissociation module.
Version: Master Suite v1.5.6

This is a deterministic, rule-based analysis module. It estimates whether a run
shows: (a) a Target-open decoder gate, (b) a Target-resolution profile, (c) a
semantic/emotional gate dissociation, or (d) insufficient evidence.

It does not prove consciousness, memory formation, OSM biology, hidden-Y biology,
or literal thermodynamic energy transfer.
"""
from __future__ import annotations
import argparse, json, glob, math, os
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

def clip01(x):
    try:
        if pd.isna(x): return np.nan
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return np.nan

def sigmoid(x: float) -> float:
    return 1.0/(1.0+math.exp(-float(x)))

def mean_non_nan(vals):
    vals=[float(v) for v in vals if v is not None and not pd.isna(v)]
    return float(np.mean(vals)) if vals else np.nan

def load_json(path: str | Path):
    with open(path,'r',encoding='utf-8') as f:
        return json.load(f)

def detect_branch(label: str) -> str:
    s=str(label).lower()
    if 'target' in s: return 'TARGET'
    if 'override' in s or 'contextual' in s: return 'OVERRIDE'
    if 'control' in s: return 'CONTROL'
    return str(label).upper()

def branch_from_json(path: str | Path):
    j=load_json(path)
    branch=detect_branch(j.get('branch_label') or j.get('branch_type') or Path(path).name)
    return branch, j.get('ratings',{}), j

def proxy_from_feature_table(path: str | Path) -> Dict[str, Dict[str,float]]:
    path=Path(path)
    if not path.exists(): return {}
    df=pd.read_csv(path)
    cond_col=None
    for col in ['condition','phase']:
        if col in df.columns:
            cond_col=col; break
    if cond_col is None:
        return {}
    out={}
    for cond, sub in df.groupby(cond_col):
        branch=detect_branch(cond)
        if branch not in ['TARGET','OVERRIDE','CONTROL']:
            continue
        mr_cols=[x for x in ['MR_score','meaninggamma_score','meaninggamma_z','meaning_gamma_proxy','tsp_z','tsp_proxy'] if x in sub.columns]
        enc_cols=[x for x in ['ENC_score','theta_integration_z','theta_integration_proxy','R_int'] if x in sub.columns]
        nip_cols=[x for x in ['NIP_density','nip_density'] if x in sub.columns]
        mr=mean_non_nan([sub[col].mean() for col in mr_cols])
        enc=mean_non_nan([sub[col].mean() for col in enc_cols])
        nip=mean_non_nan([sub[col].mean() for col in nip_cols])
        def sig(v): return np.nan if pd.isna(v) else float(1/(1+np.exp(-float(v))))
        out[branch]={
            'phys_mr_proxy': sig(mr),
            'phys_enc_proxy': sig(enc),
            'phys_nip_proxy': clip01(nip) if not pd.isna(nip) and 0 <= nip <= 1 else sig(nip),
        }
    return out

def find_feature_table(analysis_folder: Path) -> Optional[Path]:
    pats=['*time_resolved_feature_frame*.csv','*nip_component_timeseries*.csv','*nip_mred_component_timeseries*.csv']
    for pat in pats:
        found=list(analysis_folder.glob(f'**/{pat}'))
        if found: return found[0]
    return None

def find_mred_anchor_table(analysis_folder: Path) -> Optional[Path]:
    pats=['*mred_peak_resolution_anchor_table*.csv','*amred_anchor_endpoint_table*.csv']
    for pat in pats:
        found=list(analysis_folder.glob(f'**/{pat}'))
        if found: return found[0]
    return None

def compute_branch(core=None, conf=None, override_task=None, phys=None, defaults=None):
    core=core or {}; conf=conf or {}; override_task=override_task or {}; phys=phys or {}; defaults=defaults or {}
    conf_items=[conf.get(k) for k in ['AudioComprehensionDifficulty','SpeakerVolumeDifficulty','ExternalNoiseIntrusion','AudioVideoSyncProblem']]
    conf_mean=mean_non_nan(conf_items)
    semantic_access=1-conf_mean/9 if not pd.isna(conf_mean) else defaults.get('semantic_access', np.nan)
    da_report=mean_non_nan([core.get('Meaning'), core.get('Absorption'), core.get('EmotionalAfterglow'), core.get('StoryActiveWashout')])
    decoder_availability=da_report/9 if not pd.isna(da_report) else defaults.get('decoder_availability', np.nan)
    ei_report=mean_non_nan([core.get('Absorption'), core.get('EmotionalAfterglow'), core.get('StoryActiveWashout')])
    emotional_integration=ei_report/9 if not pd.isna(ei_report) else defaults.get('emotional_integration', np.nan)
    x_core=core.get('TaskExtractionLoad', core.get('AnalyticEffort', np.nan))
    x_core=float(x_core)/9 if not pd.isna(x_core) else np.nan
    x_override=mean_non_nan([override_task.get(k) for k in ['TaskCompliance','RunningSumStall','ApproximateGuessCount','HardNumberCombinationDifficulty','CueLegibilityProblem']])
    x_override=x_override/9 if not pd.isna(x_override) else np.nan
    extraction_load=mean_non_nan([x_core, x_override]) if not pd.isna(x_override) else x_core
    if pd.isna(extraction_load): extraction_load=defaults.get('extraction_load', np.nan)
    c_core=core.get('ConfoundBurden', np.nan)
    c_core=float(c_core)/9 if not pd.isna(c_core) else np.nan
    c_detail=mean_non_nan([conf.get(k) for k in ['AudioComprehensionDifficulty','SpeakerVolumeDifficulty','ExternalNoiseIntrusion','AudioVideoSyncProblem','CueBlurOrSmallness','EyeStrainOrSquint']])
    c_detail=c_detail/9 if not pd.isna(c_detail) else np.nan
    confound_load=max([v for v in [c_core,c_detail] if not pd.isna(v)], default=np.nan)
    if pd.isna(confound_load): confound_load=defaults.get('confound_load', np.nan)
    phys_mr=phys.get('phys_mr_proxy', np.nan); phys_enc=phys.get('phys_enc_proxy', np.nan); phys_nip=phys.get('phys_nip_proxy', np.nan)
    if pd.isna(decoder_availability) and not pd.isna(phys_nip): decoder_availability=phys_nip
    if pd.isna(emotional_integration) and not pd.isna(phys_enc): emotional_integration=phys_enc
    comps=[semantic_access,decoder_availability,emotional_integration,extraction_load,confound_load]
    completeness=sum(not pd.isna(v) for v in comps)/len(comps)
    SA=0.5 if pd.isna(semantic_access) else semantic_access
    DA=0.5 if pd.isna(decoder_availability) else decoder_availability
    EI=0.5 if pd.isna(emotional_integration) else emotional_integration
    X=0.5 if pd.isna(extraction_load) else extraction_load
    C=0.5 if pd.isna(confound_load) else confound_load
    gate=sigmoid(2.0*SA + 1.4*DA + 1.1*EI - 1.2*X - 1.8*C - 0.75)
    return dict(semantic_access=clip01(semantic_access), decoder_availability=clip01(decoder_availability), emotional_integration=clip01(emotional_integration), extraction_load=clip01(extraction_load), confound_load=clip01(confound_load), physiologic_mr_proxy=phys_mr, physiologic_enc_proxy=phys_enc, physiologic_nip_proxy=phys_nip, decoder_gate_availability=gate, component_completeness=completeness)

def collect_reports(paths: List[Path]):
    core={}; conf={}; task={}; final={}; config={}
    files=[]
    for p in paths:
        if p.is_dir(): files.extend(p.glob('**/*.json'))
        elif p.exists(): files.append(p)
    for p in files:
        name=p.name.lower()
        try:
            if 'core_report' in name:
                b,r,j=branch_from_json(p); core[b]=r
            elif 'confound_report' in name:
                b,r,j=branch_from_json(p); conf[b]=r
            elif 'override_task_report' in name:
                j=load_json(p); task['OVERRIDE']=j.get('ratings',{})
            elif 'final_master_report' in name:
                final=load_json(p)
            elif 'run_config_media_selection' in name:
                config=load_json(p)
        except Exception:
            continue
    return core,conf,task,final,config

def analyze(analysis_folder: Path, sidecars: List[Path], run_label: str, out_dir: Path, data_grade: str='', defaults: Dict[str,float]|None=None):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir/'tables').mkdir(exist_ok=True)
    core,conf,task,final,config=collect_reports([analysis_folder]+sidecars)
    feature=find_feature_table(analysis_folder)
    phys=proxy_from_feature_table(feature) if feature else {}
    rows=[]; scores={}
    for branch in ['CONTROL','TARGET','OVERRIDE']:
        bs=compute_branch(core.get(branch), conf.get(branch), task.get(branch), phys.get(branch,{}), defaults or {})
        bs.update(run=run_label, branch=branch, data_grade=data_grade, feature_table=str(feature) if feature else '')
        rows.append(bs); scores[branch]=bs
    bdf=pd.DataFrame(rows)
    bdf.to_csv(out_dir/'tables/dga_branch_gate_table.csv', index=False)
    def v(branch,key):
        val=scores.get(branch,{}).get(key,np.nan)
        return np.nan if pd.isna(val) else float(val)
    diffs=[v('OVERRIDE','semantic_access')-v('TARGET','semantic_access'), v('TARGET','emotional_integration')-v('OVERRIDE','emotional_integration'), v('OVERRIDE','extraction_load')-v('TARGET','extraction_load'), v('TARGET','confound_load')-v('OVERRIDE','confound_load')]
    gdi=mean_non_nan(diffs)
    classification='UNRESOLVED'
    if diffs[0]>0.2 and diffs[1]>0.05 and diffs[3]>0.2:
        classification='DECODER_GATE_DISSOCIATION_AUDIO_ACCESS_SPLIT'
    elif v('TARGET','decoder_gate_availability') > v('OVERRIDE','decoder_gate_availability') and v('TARGET','emotional_integration') >= v('OVERRIDE','emotional_integration'):
        classification='TARGET_GATE_OPEN'
    sdf=pd.DataFrame([dict(run=run_label, data_grade=data_grade, semantic_access_O_minus_T=diffs[0], emotional_integration_T_minus_O=diffs[1], extraction_O_minus_T=diffs[2], confound_T_minus_O=diffs[3], gate_dissociation_index=gdi, target_gate=v('TARGET','decoder_gate_availability'), override_gate=v('OVERRIDE','decoder_gate_availability'), classification=classification)])
    sdf.to_csv(out_dir/'tables/dga_gate_dissociation_summary.csv', index=False)
    # Gate-adjust MRED anchor table if present.
    anchor=find_mred_anchor_table(analysis_folder)
    if anchor:
        adf=pd.read_csv(anchor)
        tg=v('TARGET','decoder_gate_availability')
        score_cols=[c for c in ['MRED_peak_score','mred_peak_score','MRED_resolution_score','resolution_score'] if c in adf.columns]
        for c in score_cols:
            adf['dga_bounded_'+c]=adf[c].apply(clip01)
            adf['dga_gate_adjusted_'+c]=adf['dga_bounded_'+c]*tg
        adf['target_gate']=tg
        adf.to_csv(out_dir/'tables/dga_gate_adjusted_mred_anchor_table.csv', index=False)
    with open(out_dir/'tables/dga_interpretation.json','w',encoding='utf-8') as f:
        json.dump(dict(schema='PRAYCG_DGA_v0_1', run=run_label, summary=sdf.to_dict(orient='records'), boundary='DGA estimates decoder/access conditions and is not proof of mechanism.'), f, indent=2)
    # Markdown report
    md=f"# DGA_v0.1 report - {run_label}\n\n"+sdf.to_markdown(index=False, floatfmt='.3f')+"\n\n## Branch table\n"+bdf.to_markdown(index=False, floatfmt='.3f')+"\n"
    (out_dir/'report').mkdir(exist_ok=True)
    with open(out_dir/'report/dga_report.md','w',encoding='utf-8') as f: f.write(md)
    return sdf,bdf

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--analysis-folder', required=True)
    ap.add_argument('--sidecar-folder', action='append', default=[])
    ap.add_argument('--run-label', default='PRAYCG_Run')
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--data-grade', default='')
    ap.add_argument('--default-semantic-access', type=float, default=None)
    ap.add_argument('--default-confound-load', type=float, default=None)
    args=ap.parse_args()
    defaults={}
    if args.default_semantic_access is not None: defaults['semantic_access']=args.default_semantic_access
    if args.default_confound_load is not None: defaults['confound_load']=args.default_confound_load
    analyze(Path(args.analysis_folder), [Path(x) for x in args.sidecar_folder], args.run_label, Path(args.out_dir), args.data_grade, defaults)
if __name__=='__main__': main()
