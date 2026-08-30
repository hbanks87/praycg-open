#!/usr/bin/env python3
"""
PRAYCG Topo-OSM Network-State Module v1.4.7

Standalone post-analysis module. It does not infer microtubules, biophotons, or cellular OSM.
It aliases human K outputs as K_HT-topo and creates visual overlays for topological event review.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd


def zscore(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    med = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - med))
    den = 1.4826 * mad if mad and np.isfinite(mad) else np.nanstd(x)
    if not den or not np.isfinite(den): den = 1.0
    return (x - med) / (den + 1e-9)


def find_col(df: pd.DataFrame, candidates):
    lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand in df.columns: return cand
        if cand.lower() in lower: return lower[cand.lower()]
    # fuzzy
    for c in df.columns:
        lc=c.lower()
        if any(cand.lower() in lc for cand in candidates): return c
    return None


def load_feature_csv(analysis_folder: Path, explicit: str = "") -> Path|None:
    if explicit:
        p=Path(explicit)
        return p if p.exists() else None
    tables=analysis_folder/'tables'
    patterns=[
        'human_translation_kht_feature_frame.csv', '*_time_resolved_feature_frame.csv', '*feature_frame*.csv', '*window*features*.csv'
    ]
    for pat in patterns:
        hits=list(tables.glob(pat)) if tables.exists() else []
        if hits: return hits[0]
    return None


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--analysis-folder', required=True)
    ap.add_argument('--feature-csv', default='')
    ap.add_argument('--candidate-local-kht-csv', default='')
    ap.add_argument('--mred-event-csv', default='')
    ap.add_argument('--out-dir', default='')
    args=ap.parse_args()
    root=Path(args.analysis_folder)
    tables=Path(args.out_dir) if args.out_dir else root/'tables'
    tables.mkdir(parents=True, exist_ok=True)

    feature_path=load_feature_csv(root, args.feature_csv)
    topo_rows=[]
    interp={
        'schema':'PRAYCG_TopoOSM_NetworkState_Module_v1_4_7',
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'analysis_folder':str(root),
        'boundary':'Human-scale network-state topology only; no microtubule, biophoton, cytoskeletal, or molecular OSM inference.',
    }

    if feature_path and feature_path.exists():
        df=pd.read_csv(feature_path)
        time_col=find_col(df,['time_sec','condition_offset_sec','phase_time_sec','analysis_time','time'])
        cond_col=find_col(df,['condition','phase'])
        gamma_col=find_col(df,['MeaningGamma','meaninggamma_score','gamma_z','lgamma_posterior_temporal_z','lgamma_global_z'])
        tsp_col=find_col(df,['tsp_z','TSP','temporal_semantic_proxy_score','temporal_semantic_proxy_z'])
        theta_col=find_col(df,['theta_z','theta_global_z','theta_midline_z','theta_posterior_temporal_z'])
        alpha_col=find_col(df,['alpha_z','alpha_global_z','posterior_alpha_z','alpha_power_z'])
        api_col=find_col(df,['API_A','api_a','api_a_z','autonomic_availability'])
        art_col=find_col(df,['artifact_score','artifact_z','jaw_artifact','p2p_artifact'])
        used={k:v for k,v in dict(time_col=time_col,cond_col=cond_col,gamma_col=gamma_col,tsp_col=tsp_col,theta_col=theta_col,alpha_col=alpha_col,api_col=api_col,artifact_col=art_col).items()}
        interp['feature_csv']=str(feature_path)
        interp['feature_columns_used']=used
        work=pd.DataFrame()
        if time_col: work['time_sec']=pd.to_numeric(df[time_col], errors='coerce')
        else: work['time_sec']=np.arange(len(df), dtype=float)
        work['condition']=df[cond_col].astype(str) if cond_col else ''
        for name,col in [('gamma',gamma_col),('tsp',tsp_col),('theta',theta_col),('alpha',alpha_col),('api',api_col),('artifact',art_col)]:
            work[name]=zscore(df[col]) if col else 0.0
        # topological state proxy: meaning work + theta persistence + API - artifact - alpha-idle burden
        work['topo_state_proxy_z']=0.30*work['gamma']+0.30*work['tsp']+0.25*work['theta']+0.10*work['api']-0.15*work['artifact']-0.05*work['alpha']
        work['topo_delta_z']=work['topo_state_proxy_z'].diff().fillna(0.0)
        work['topo_persistence_z']=work['topo_state_proxy_z'].rolling(8, min_periods=1).mean()
        out= tables/'topo_osm_feature_proxy_frame.csv'
        work.to_csv(out,index=False)
        # candidate overlay events at local maxima > robust threshold
        score=work['topo_state_proxy_z']
        thr=np.nanpercentile(score, 95) if len(score) else np.nan
        for _,r in work[score>=thr].iterrows():
            topo_rows.append({
                'time_sec':float(r['time_sec']),
                'condition':r.get('condition',''),
                'topo_state_proxy_z':float(r['topo_state_proxy_z']),
                'topo_delta_z':float(r['topo_delta_z']),
                'topo_persistence_z':float(r['topo_persistence_z']),
                'interpretation':'high inferred network-state topology proxy; exploratory unless predeclared and condition-specific',
            })
    else:
        interp['feature_csv']='not_found'

    topo_event=pd.DataFrame(topo_rows)
    if not topo_event.empty:
        topo_event.to_csv(tables/'topo_osm_event_table.csv',index=False)
        overlay=[]
        for _,r in topo_event.iterrows():
            overlay.append({'start_sec':r['time_sec'],'end_sec':r['time_sec']+1.0,'label':f"TopoOSM proxy {r['topo_state_proxy_z']:.2f}", 'category':'topo_osm', 'source':'topo_osm_event_table.csv'})
        pd.DataFrame(overlay).to_csv(tables/'topo_osm_visual_overlay.csv',index=False)
    else:
        pd.DataFrame(columns=['time_sec','condition','topo_state_proxy_z','topo_delta_z','topo_persistence_z','interpretation']).to_csv(tables/'topo_osm_event_table.csv',index=False)
        pd.DataFrame(columns=['start_sec','end_sec','label','category','source']).to_csv(tables/'topo_osm_visual_overlay.csv',index=False)

    # KHT-topo alias table from candidate_local_kht
    cand_path=Path(args.candidate_local_kht_csv) if args.candidate_local_kht_csv else root/'tables'/'candidate_local_kht_analysis.csv'
    if cand_path.exists():
        try:
            cdf=pd.read_csv(cand_path)
            if 'K_local' in cdf.columns:
                cdf['K_HT_topo']=pd.to_numeric(cdf['K_local'], errors='coerce')
            elif 'K_HT' in cdf.columns:
                cdf['K_HT_topo']=pd.to_numeric(cdf['K_HT'], errors='coerce')
            else:
                cdf['K_HT_topo']=np.nan
            cdf['claim_boundary']='K_HT_topo is a human-scale network-state coupling proxy, not K_OSM or cellular OSM.'
            cdf.to_csv(tables/'kht_topo_event_table.csv',index=False)
            interp['kht_topo_alias_source']=str(cand_path)
        except Exception as e:
            interp['kht_topo_alias_error']=str(e)

    with open(tables/'topo_osm_interpretation.json','w',encoding='utf-8') as f:
        json.dump(interp,f,indent=2)
    print(json.dumps({'status':'ok','tables':str(tables),'boundary':interp['boundary']}, indent=2))

if __name__=='__main__':
    main()
