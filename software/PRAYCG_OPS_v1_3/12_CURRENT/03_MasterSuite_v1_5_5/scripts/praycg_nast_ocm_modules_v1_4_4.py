#!/usr/bin/env python3
from __future__ import annotations
import json, math, os, glob, zipfile, shutil, hashlib
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
try:
    from scipy import stats
except Exception:
    stats = None

EPS = 1e-9


def robust_z(x: pd.Series) -> pd.Series:
    x = pd.to_numeric(x, errors='coerce')
    med = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - med))
    if not np.isfinite(mad) or mad < EPS:
        sd = np.nanstd(x)
        if not np.isfinite(sd) or sd < EPS:
            return pd.Series(np.zeros(len(x)), index=x.index, dtype=float)
        return (x - np.nanmean(x)) / (sd + EPS)
    return (x - med) / (1.4826 * mad + EPS)


def first_existing(cols, candidates):
    for c in candidates:
        if c in cols:
            return c
    return None


def mean_existing(df, candidates, name=None):
    existing = [c for c in candidates if c in df.columns]
    if not existing:
        return pd.Series(np.nan, index=df.index, dtype=float)
    return df[existing].apply(pd.to_numeric, errors='coerce').mean(axis=1)


def cols_matching(cols, include_all=(), include_any=(), exclude=()):
    out=[]
    for c in cols:
        cl=c.lower()
        if all(s.lower() in cl for s in include_all) and (not include_any or any(s.lower() in cl for s in include_any)) and not any(s.lower() in cl for s in exclude):
            out.append(c)
    return out


def choose_col_by_patterns(cols, patterns, exclude=()):
    for pattern in patterns:
        matches=[]
        for c in cols:
            cl=c.lower()
            if all(p.lower() in cl for p in pattern) and not any(e.lower() in cl for e in exclude):
                matches.append(c)
        if matches:
            # prefer z columns if available
            z=[c for c in matches if c.lower().startswith('z_') or c.lower().endswith('_z')]
            return z[0] if z else matches[0]
    return None


def canonicalize(df: pd.DataFrame, run_name: str) -> pd.DataFrame:
    cols=list(df.columns)
    out=pd.DataFrame(index=df.index)
    out['run']=run_name
    # phase
    phase_col = 'phase' if 'phase' in df.columns else ('segment' if 'segment' in df.columns else None)
    if phase_col is None:
        raise ValueError(f'{run_name}: no phase/segment column')
    out['phase']=df[phase_col].astype(str)
    # time columns
    if {'start_lsl','end_lsl','mid_lsl'}.issubset(df.columns):
        out['start']=pd.to_numeric(df['start_lsl'], errors='coerce')
        out['end']=pd.to_numeric(df['end_lsl'], errors='coerce')
        out['time']=pd.to_numeric(df['mid_lsl'], errors='coerce')
    elif {'t0','t1'}.issubset(df.columns):
        out['start']=pd.to_numeric(df['t0'], errors='coerce')
        out['end']=pd.to_numeric(df['t1'], errors='coerce')
        out['time']=(out['start']+out['end'])/2
    elif {'window_start','window_end','window_mid'}.issubset(df.columns):
        out['start']=pd.to_numeric(df['window_start'], errors='coerce')
        out['end']=pd.to_numeric(df['window_end'], errors='coerce')
        out['time']=pd.to_numeric(df['window_mid'], errors='coerce')
    elif 'analysis_time' in df.columns:
        out['time']=pd.to_numeric(df['analysis_time'], errors='coerce')
        out['start']=out['time']-1
        out['end']=out['time']+1
    else:
        out['time']=np.arange(len(df), dtype=float)
        out['start']=out['time']-0.5
        out['end']=out['time']+0.5
    # relative time within phase
    out['phase_time']=np.nan
    for ph, idx in out.groupby('phase').groups.items():
        t0=np.nanmin(out.loc[idx,'start'])
        out.loc[idx,'phase_time']=out.loc[idx,'time']-t0
    if 'rel_t' in df.columns:
        rt=pd.to_numeric(df['rel_t'], errors='coerce')
        if rt.notna().sum()>0:
            out['phase_time']=rt
    # canonical feature candidates
    # alpha: posterior/parietal/primary, non-frontal, non-artifact. Prefer z-scored columns.
    alpha_candidates = [
        'alpha_8_12_primary_content_core_z','alpha_8_12_parietal_integration_z','alpha_8_12_posterior_temporal_proxy_z','alpha_8_12_non_sentinel_all_z',
        'pow_alpha_8_12_primary_content_core_z','pow_alpha_8_12_parietal_z','pow_alpha_8_12_posterior_temporal_proxy_z','pow_alpha_8_12_meaning_candidate_z',
        'z_pow_alpha_8_12_primary_content_core','z_pow_alpha_8_12_parietal','z_pow_alpha_8_12_posterior_temporal','z_pow_alpha_8_12_meaning_candidate',
        'z_logbp_primary_content_core_alpha_8_12','z_logbp_posterior_temporal_alpha_8_12','z_logbp_meaning_candidate_alpha_8_12','z_logbp_all16_alpha_8_12'
    ]
    out['alpha_proxy_z']=mean_existing(df, alpha_candidates)
    if out['alpha_proxy_z'].isna().all():
        found=cols_matching(cols, include_all=('alpha',), include_any=('primary','parietal','posterior','meaning','all16','non_sentinel'), exclude=('artifact','sentinel','jaw','blink','visual','task','frontal'))
        zfound=[c for c in found if c.lower().startswith('z_') or c.lower().endswith('_z')]
        out['alpha_proxy_z']=mean_existing(df, zfound or found)
        if not (zfound or [c for c in found if c in df.columns]): out['alpha_proxy_z']=np.nan
        elif not zfound: out['alpha_proxy_z']=robust_z(out['alpha_proxy_z'])
    # theta primary / integration
    theta_candidates = ['ThetaPLV_primary','ThetaPower_primary','theta_proxy_z','theta_z','theta_4_8_primary_content_core_z','theta_4_8_parietal_integration_z','pow_theta_4_8_primary_content_core_z','pow_theta_4_8_parietal_z','z_pow_theta_4_8_primary_content_core','z_logbp_primary_content_core_theta_4_8','z_logbp_all16_theta_4_8']
    out['theta_primary_z']=mean_existing(df, theta_candidates)
    if out['theta_primary_z'].isna().all():
        found=cols_matching(cols, include_all=('theta',), include_any=('primary','parietal','all16','non_sentinel'), exclude=('artifact','sentinel','jaw','blink','visual'))
        zfound=[c for c in found if c.lower().startswith('z_') or c.lower().endswith('_z')]
        out['theta_primary_z']=mean_existing(df, zfound or found)
        if not zfound: out['theta_primary_z']=robust_z(out['theta_primary_z'])
    # theta task/frontal for override working memory
    theta_task_candidates = ['theta_4_8_frontoparietal_task_z','theta_4_8_frontal_analytic_lock_z','pow_theta_4_8_frontoparietal_task_z','pow_theta_4_8_frontal_z','z_pow_theta_4_8_frontoparietal_task','z_logbp_frontoparietal_task_theta_4_8','z_plv_frontoparietal_task_theta_4_8','plv_theta_4_8_frontoparietal_task_z','z_plv_theta_4_8_frontoparietal_task']
    out['theta_task_z']=mean_existing(df, theta_task_candidates)
    if out['theta_task_z'].isna().all():
        found=cols_matching(cols, include_all=('theta',), include_any=('task','frontal'), exclude=('artifact','sentinel','jaw','blink'))
        zfound=[c for c in found if c.lower().startswith('z_') or c.lower().endswith('_z')]
        out['theta_task_z']=mean_existing(df, zfound or found)
        if not zfound: out['theta_task_z']=robust_z(out['theta_task_z'])
    # meaninggamma
    mg_candidates = ['MeaningGamma_phys','MeaningGamma','meaninggamma_lgamma_30_45','meaninggamma_lgamma_35_40','E_gamma_z']
    out['meaning_gamma_z']=mean_existing(df, mg_candidates)
    if out['meaning_gamma_z'].isna().all():
        found=cols_matching(cols, include_all=('gamma',), include_any=('meaning_candidate','temporal_semantic_candidate','posterior_temporal'), exclude=('artifact','sentinel','jaw','blink','visual','task'))
        zfound=[c for c in found if c.lower().startswith('z_') or c.lower().endswith('_z')]
        out['meaning_gamma_z']=mean_existing(df, zfound or found)
        if not zfound: out['meaning_gamma_z']=robust_z(out['meaning_gamma_z'])
    else:
        out['meaning_gamma_z']=robust_z(out['meaning_gamma_z']) if not any(c in df.columns for c in ['E_gamma_z']) else out['meaning_gamma_z']
    # TSP
    tsp_candidates = ['TSP_gamma','tsp_z','temporal_semantic_proxy_score','temporal_semantic_proxy_z']
    out['tsp_z']=mean_existing(df, tsp_candidates)
    if out['tsp_z'].isna().all():
        post=mean_existing(df, ['pow_lgamma_30_45_posterior_temporal_proxy_z','z_pow_lgamma_30_45_posterior_temporal','z_logbp_posterior_temporal_low_gamma_30_45','lgamma_30_45_posterior_temporal_proxy_z','pow_lgamma_30_45_meaning_candidate_z','z_pow_lgamma_30_45_meaning_candidate','z_logbp_meaning_candidate_low_gamma_30_45'])
        vis=mean_existing(df, ['pow_lgamma_30_45_visual_control_z','z_pow_lgamma_30_45_visual_control','z_logbp_visual_control_low_gamma_30_45','lgamma_30_45_visual_control_z'])
        art=mean_existing(df, ['artifact_score','artifact_composite','z_pow_hf_proxy_45_55_artifact_sentinel','z_logbp_artifact_sentinel_hf_proxy_45_55'])
        out['tsp_z']=robust_z(post.fillna(0)-0.5*vis.fillna(0)-0.25*art.fillna(0))
    else:
        out['tsp_z']=robust_z(out['tsp_z'])
    # task gamma
    task_candidates = ['TaskGamma','taskgamma_lgamma_30_45','taskgamma_lgamma_35_40','task_proxy_z']
    out['task_gamma_z']=mean_existing(df, task_candidates)
    if out['task_gamma_z'].isna().all():
        found=cols_matching(cols, include_all=('gamma',), include_any=('frontoparietal_task','frontal_analytic_lock'), exclude=('artifact','sentinel','jaw','blink'))
        zfound=[c for c in found if c.lower().startswith('z_') or c.lower().endswith('_z')]
        out['task_gamma_z']=mean_existing(df, zfound or found)
        if not zfound: out['task_gamma_z']=robust_z(out['task_gamma_z'])
    else:
        out['task_gamma_z']=robust_z(out['task_gamma_z']) if 'task_proxy_z' not in df.columns else out['task_gamma_z']
    # visual/sensory proxy
    vis_candidates=['z_logbp_visual_control_low_gamma_30_45','z_pow_lgamma_30_45_visual_control','lgamma_30_45_visual_control_z','pow_lgamma_30_45_visual_control_z','z_logbp_visual_control_gamma_35_40','z_pow_g35_40_visual_control']
    out['visual_gamma_z']=mean_existing(df, vis_candidates)
    if out['visual_gamma_z'].isna().all():
        found=cols_matching(cols, include_all=('visual',), include_any=('gamma','lgamma','low_gamma'), exclude=('artifact','sentinel','jaw','blink'))
        zfound=[c for c in found if c.lower().startswith('z_') or c.lower().endswith('_z')]
        out['visual_gamma_z']=mean_existing(df, zfound or found)
        if not zfound: out['visual_gamma_z']=robust_z(out['visual_gamma_z'])
    # artifact
    art_candidates=['artifact_score','artifact_proxy_z','artifact_composite','z_hf_proxy_45_55_artifact_sentinel_logp','hf_proxy_45_55_artifact_sentinel_z','z_logbp_artifact_sentinel_hf_proxy_45_55','z_pow_hf_proxy_45_55_artifact_sentinel','artifact_p2p_median','ptp_median','median_p2p']
    out['artifact_z']=mean_existing(df, art_candidates)
    if out['artifact_z'].isna().all():
        found=cols_matching(cols, include_all=('artifact',), include_any=('hf','gamma','p2p','peak','score','composite'), exclude=())
        zfound=[c for c in found if c.lower().startswith('z_') or c.lower().endswith('_z')]
        out['artifact_z']=mean_existing(df, zfound or found)
    out['artifact_z']=robust_z(out['artifact_z'].fillna(0))
    # API and resp optional
    api_candidates=['API_A','api_a','api_a_proxy','api_a_z','API_A_v1','API_A_z']
    out['api_a_z']=mean_existing(df, api_candidates)
    if out['api_a_z'].isna().all(): out['api_a_z']=0.0
    else: out['api_a_z']=robust_z(out['api_a_z'])
    resp_candidates=['resp_slope','resp_rate_bpm','resp_mean','resp_amp']
    out['resp_z']=mean_existing(df, resp_candidates)
    if out['resp_z'].isna().all(): out['resp_z']=0.0
    else: out['resp_z']=robust_z(out['resp_z'])
    # valid
    out['valid']=True
    if 'valid_eeg' in df.columns:
        out['valid']=df['valid_eeg'].astype(str).str.lower().isin(['true','1','yes'])
    # z canonical component normalization for score stability
    for c in ['alpha_proxy_z','theta_primary_z','theta_task_z','meaning_gamma_z','tsp_z','task_gamma_z','visual_gamma_z','api_a_z','resp_z']:
        if out[c].notna().sum()>2:
            out[c]=robust_z(out[c])
        else:
            out[c]=out[c].fillna(0.0)
    return out.sort_values('time').reset_index(drop=True)


def weighted_mean(df: pd.DataFrame, feature: str, a: float, b: float, phase: Optional[str]=None) -> float:
    if b <= a or feature not in df.columns:
        return np.nan
    sub=df
    if phase is not None:
        sub=sub[sub['phase']==phase]
    sub=sub[(sub['end']>a) & (sub['start']<b)]
    if sub.empty: return np.nan
    weights=np.minimum(sub['end'], b)-np.maximum(sub['start'], a)
    weights=np.maximum(weights,0)
    vals=pd.to_numeric(sub[feature], errors='coerce')
    good=vals.notna() & np.isfinite(weights) & (weights>0)
    if not good.any(): return np.nan
    return np.average(vals[good], weights=weights[good])


def compute_alpha_drop(df: pd.DataFrame, L=10.0):
    drops=[]
    for _, row in df.iterrows():
        t=row['time']
        pre=weighted_mean(df,'alpha_proxy_z',t-L,t)
        post=weighted_mean(df,'alpha_proxy_z',t,t+L)
        drops.append(pre-post if np.isfinite(pre) and np.isfinite(post) else np.nan)
    return pd.Series(drops,index=df.index)


def phase_delta(df: pd.DataFrame, pre_phase: str, post_phase: str, L=30.0) -> Dict[str,float]:
    res={'transition':f'{pre_phase}->{post_phase}'}
    if pre_phase not in set(df['phase']) or post_phase not in set(df['phase']):
        res['available']=False; return res
    pre_end=df.loc[df['phase']==pre_phase,'end'].max()
    post_start=df.loc[df['phase']==post_phase,'start'].min()
    res['available']=True
    for feat in ['alpha_proxy_z','meaning_gamma_z','tsp_z','task_gamma_z','theta_primary_z','theta_task_z','artifact_z','api_a_z']:
        pre=weighted_mean(df,feat,pre_end-L,pre_end,pre_phase)
        post=weighted_mean(df,feat,post_start,post_start+L,post_phase)
        res[f'pre_{feat}']=pre
        res[f'post_{feat}']=post
        res[f'delta_{feat}']=post-pre if np.isfinite(pre) and np.isfinite(post) else np.nan
    # qualitative phenotype
    res['interpretation']=''
    da=res.get('delta_alpha_proxy_z',np.nan)
    dm=res.get('delta_meaning_gamma_z',np.nan)
    dt=res.get('delta_tsp_z',np.nan)
    dtask=res.get('delta_task_gamma_z',np.nan)
    if np.isfinite(da):
        if da<0 and (dm>0 or dt>0): res['interpretation']='alpha suppression + meaning/TSP rise candidate'
        elif da<0 and dtask>0: res['interpretation']='alpha suppression + task-gamma candidate'
        elif da<0: res['interpretation']='alpha suppression / sensory capture candidate'
        else: res['interpretation']='no alpha-suppression transition'
    return res


def run_nast(df: pd.DataFrame, run_name: str) -> Tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame,Dict]:
    d=df.copy()
    d['alpha_drop_z']=robust_z(compute_alpha_drop(d, L=10.0).fillna(0))
    d['NAS_raw']=(0.30*d['alpha_drop_z'] + 0.25*d['meaning_gamma_z'] + 0.25*d['tsp_z'] + 0.10*d['api_a_z']
                  -0.20*d['task_gamma_z'] -0.20*d['artifact_z'] -0.10*d['visual_gamma_z'])
    d['NAS_z']=robust_z(d['NAS_raw'])
    null_mask=d['phase'].isin(['BASELINE_1','CONTROL_1'])
    q95=np.nanpercentile(d.loc[null_mask,'NAS_z'],95) if null_mask.any() else np.nanpercentile(d['NAS_z'],95)
    art_q90=np.nanpercentile(d['artifact_z'],90)
    d['nast_candidate']= (d['NAS_z']>q95) & (d['artifact_z']<art_q90) & d['valid']
    # sustained: at least two candidates in 8s neighborhood
    sustained=[]
    for _,row in d.iterrows():
        sub=d[(d['time']>=row['time']) & (d['time']<=row['time']+8) & (d['phase']==row['phase'])]
        sustained.append(bool(row['nast_candidate'] and sub['nast_candidate'].sum()>=2))
    d['nast_sustained_candidate']=sustained
    transitions=[('BASELINE_1','CONTROL_1'),('WASHOUT_1','TARGET_1'),('WASHOUT_2','CONTEXTUAL_OVERRIDE_1')]
    # some tables use CONTEXTUAL_OVERRIDE_1, ok
    rows=[phase_delta(d,a,b) for a,b in transitions]
    trans=pd.DataFrame(rows)
    # onset table for phases
    onset_rows=[]
    for ph in ['CONTROL_1','TARGET_1','CONTEXTUAL_OVERRIDE_1']:
        sub=d[d['phase']==ph].copy()
        if sub.empty:
            continue
        cand=sub[sub['nast_sustained_candidate']]
        top=sub.sort_values('NAS_z',ascending=False).head(1)
        if not cand.empty:
            row=cand.iloc[0]
            status='sustained_candidate'
        else:
            row=top.iloc[0]
            status='top_only_no_sustained_lock'
        onset_rows.append({
            'run':run_name,'phase':ph,'status':status,'time':row['time'],'phase_time_sec':row['phase_time'],
            'NAS_z':row['NAS_z'],'alpha_drop_z':row['alpha_drop_z'],'alpha_proxy_z':row['alpha_proxy_z'],
            'meaning_gamma_z':row['meaning_gamma_z'],'tsp_z':row['tsp_z'],'task_gamma_z':row['task_gamma_z'],
            'theta_primary_z':row['theta_primary_z'],'artifact_z':row['artifact_z'],
            'threshold_q95_null':q95,'artifact_q90':art_q90
        })
    onset=pd.DataFrame(onset_rows)
    d['overlay_label']=np.where(d['nast_sustained_candidate'],'NAST sustained absorption-proxy candidate',np.where(d['nast_candidate'],'NAST candidate',''))
    overlay=d[d['overlay_label']!=''][['run','phase','time','phase_time','NAS_z','alpha_drop_z','meaning_gamma_z','tsp_z','task_gamma_z','artifact_z','overlay_label']].copy()
    interp={
        'run':run_name,
        'q95_null_NAS_z':float(q95),
        'artifact_q90':float(art_q90),
        'n_nast_candidates':int(d['nast_candidate'].sum()),
        'n_sustained_candidates':int(d['nast_sustained_candidate'].sum()),
        'boundary':'NAST is an EEG-proxy narrative-absorption state-transition analysis, not direct DMN detection.'
    }
    return trans,onset,overlay,interp


def create_arrival_cue_table(cue_json_path: str, segments_path: str) -> pd.DataFrame:
    j=json.load(open(cue_json_path))
    seg=pd.read_csv(segments_path)
    rows=[]
    for phase in ['TARGET_1','CONTEXTUAL_OVERRIDE_1','CONTROL_1']:
        if phase not in set(seg['segment']): continue
        start=float(seg.loc[seg['segment']==phase,'start_lsl'].iloc[0])
        for e in j['cue_events']:
            rows.append({'phase':phase,'cue_index':e['cue_index'],'value':e['value'],'lsl_time':start+float(e['start_sec']),'cue_start_sec':float(e['start_sec']),'source':'cue_schedule_plus_segment_start'})
    return pd.DataFrame(rows)


def run_ocm(df: pd.DataFrame, cues: pd.DataFrame, run_name: str) -> Tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame,Dict]:
    # normalize phase names
    c=cues.copy()
    c['phase']=c['phase'].astype(str)
    # Keep Target and Override cues if available
    # For each override cue, compute real and corresponding target windows by matching cue_index.
    override_ph='CONTEXTUAL_OVERRIDE_1'
    if override_ph not in set(c['phase']) and 'OVERRIDE_1' in set(c['phase']): override_ph='OVERRIDE_1'
    target_ph='TARGET_1'
    rows=[]
    pseudo=[]
    oc=c[c['phase']==override_ph].sort_values('cue_index')
    tc=c[c['phase']==target_ph].sort_values('cue_index')
    target_times=dict(zip(tc['cue_index'],tc['lsl_time']))
    cue_times=list(oc['lsl_time'].values)
    for idx, row in oc.iterrows():
        ti=float(row['lsl_time']); ci=int(row['cue_index']); val=float(row['value']);
        next_t = cue_times[list(oc.index).index(idx)+1] if list(oc.index).index(idx)+1 < len(cue_times) else ti+3.0
        windows={
            'pre':(ti-0.75,ti),
            'recognition':(ti+0.10,ti+0.85),
            'update':(ti+0.85,ti+2.25),
            'maintenance':(ti+2.25,min(next_t,ti+3.0))
        }
        rec_task=weighted_mean(df,'task_gamma_z',*windows['recognition'],phase=override_ph)
        pre_task=weighted_mean(df,'task_gamma_z',*windows['pre'],phase=override_ph)
        upd_theta=weighted_mean(df,'theta_task_z',*windows['update'],phase=override_ph)
        pre_theta=weighted_mean(df,'theta_task_z',*windows['pre'],phase=override_ph)
        maint_theta=weighted_mean(df,'theta_task_z',*windows['maintenance'],phase=override_ph)
        art=np.nanmean([weighted_mean(df,'artifact_z',*w,phase=override_ph) for w in windows.values()])
        # target equivalent
        t_targ=target_times.get(ci,np.nan)
        if np.isfinite(t_targ):
            tw={
                'pre':(t_targ-0.75,t_targ),
                'recognition':(t_targ+0.10,t_targ+0.85),
                'update':(t_targ+0.85,t_targ+2.25),
                'maintenance':(t_targ+2.25,t_targ+3.0)
            }
            targ_DR=weighted_mean(df,'task_gamma_z',*tw['recognition'],phase=target_ph)-weighted_mean(df,'task_gamma_z',*tw['pre'],phase=target_ph)
            targ_WMU=weighted_mean(df,'theta_task_z',*tw['update'],phase=target_ph)-weighted_mean(df,'theta_task_z',*tw['pre'],phase=target_ph)
        else:
            targ_DR=np.nan; targ_WMU=np.nan
        DR=rec_task-pre_task if np.isfinite(rec_task) and np.isfinite(pre_task) else np.nan
        WMU=upd_theta-pre_theta if np.isfinite(upd_theta) and np.isfinite(pre_theta) else np.nan
        MAINT=maint_theta-pre_theta if np.isfinite(maint_theta) and np.isfinite(pre_theta) else np.nan
        rows.append({'run':run_name,'phase':override_ph,'cue_index':ci,'value':val,'running_sum':np.nan, 'cue_time':ti,
                     'digit_recognition_DR':DR,'working_memory_update_WMU':WMU,'maintenance_MAINT':MAINT,
                     'artifact_z_mean':art,'target_matched_DR':targ_DR,'target_matched_WMU':targ_WMU,
                     'override_minus_target_DR':DR-targ_DR if np.isfinite(DR) and np.isfinite(targ_DR) else np.nan,
                     'override_minus_target_WMU':WMU-targ_WMU if np.isfinite(WMU) and np.isfinite(targ_WMU) else np.nan})
        # pseudo cue halfway between real cues. This is deliberately phase-shifted from the visible cue;
        # it can overlap later processing in the 3-s cue stream, so it is a coarse negative-control, not a clean physiological null.
        pt=ti+1.5
        pre=(pt-0.75,pt); rec=(pt+0.10,pt+0.85); upd=(pt+0.85,pt+2.25)
        pDR=weighted_mean(df,'task_gamma_z',*rec,phase=override_ph)-weighted_mean(df,'task_gamma_z',*pre,phase=override_ph)
        pWMU=weighted_mean(df,'theta_task_z',*upd,phase=override_ph)-weighted_mean(df,'theta_task_z',*pre,phase=override_ph)
        pseudo.append({'run':run_name,'phase':override_ph,'cue_index':ci,'pseudo_time':pt,'pseudo_DR':pDR,'pseudo_WMU':pWMU})
    res=pd.DataFrame(rows)
    if not res.empty:
        res['running_sum']=res['value'].cumsum()
        art_q90=np.nanpercentile(df['artifact_z'],90)
        res['cue_update_event']=(res['digit_recognition_DR']>np.nanpercentile(res['digit_recognition_DR'],60)) & (res['working_memory_update_WMU']>np.nanpercentile(res['working_memory_update_WMU'],60)) & (res['artifact_z_mean']<art_q90)
    pseudo_df=pd.DataFrame(pseudo)
    # summary
    summ={'run':run_name,'n_override_cues':int(len(res)),'n_analyzable_cues_DR':int(res['digit_recognition_DR'].notna().sum()) if not res.empty else 0,
          'n_analyzable_cues_WMU':int(res['working_memory_update_WMU'].notna().sum()) if not res.empty else 0,
          'mean_DR_real':float(np.nanmean(res['digit_recognition_DR'])) if not res.empty else np.nan,
          'mean_WMU_real':float(np.nanmean(res['working_memory_update_WMU'])) if not res.empty else np.nan,
          'mean_MAINT_real':float(np.nanmean(res['maintenance_MAINT'])) if not res.empty else np.nan,
          'mean_override_minus_target_DR':float(np.nanmean(res['override_minus_target_DR'])) if not res.empty else np.nan,
          'mean_override_minus_target_WMU':float(np.nanmean(res['override_minus_target_WMU'])) if not res.empty else np.nan,
          'n_cue_update_events':int(res['cue_update_event'].sum()) if not res.empty and 'cue_update_event' in res else 0,
          'boundary':'OCM uses cue-locked EEG feature windows to test working-memory microstates. With existing 2s feature tables, sub-second recognition/update claims are coarse and exploratory.'}
    if not pseudo_df.empty:
        summ['mean_DR_pseudo']=float(np.nanmean(pseudo_df['pseudo_DR']))
        summ['mean_WMU_pseudo']=float(np.nanmean(pseudo_df['pseudo_WMU']))
        summ['real_minus_pseudo_DR']=summ['mean_DR_real']-summ['mean_DR_pseudo']
        summ['real_minus_pseudo_WMU']=summ['mean_WMU_real']-summ['mean_WMU_pseudo']
    else:
        summ.update({'mean_DR_pseudo':np.nan,'mean_WMU_pseudo':np.nan,'real_minus_pseudo_DR':np.nan,'real_minus_pseudo_WMU':np.nan})
    # correlations with load
    if not res.empty and stats is not None:
        for col in ['working_memory_update_WMU','digit_recognition_DR','maintenance_MAINT']:
            good=res[[col,'cue_index','running_sum','value','artifact_z_mean']].replace([np.inf,-np.inf],np.nan).dropna()
            if len(good)>4:
                rho_i,p_i=stats.spearmanr(good['cue_index'],good[col])
                rho_s,p_s=stats.spearmanr(good['running_sum'],good[col])
                summ[f'spearman_{col}_cue_index_rho']=float(rho_i); summ[f'spearman_{col}_cue_index_p']=float(p_i)
                summ[f'spearman_{col}_running_sum_rho']=float(rho_s); summ[f'spearman_{col}_running_sum_p']=float(p_s)
    overlay=res[res.get('cue_update_event',pd.Series(False,index=res.index))][['run','phase','cue_index','cue_time','digit_recognition_DR','working_memory_update_WMU','maintenance_MAINT','artifact_z_mean']].copy() if not res.empty else pd.DataFrame()
    if not overlay.empty:
        overlay['overlay_label']='OCM cue-update event'
    return res,pseudo_df,overlay,summ


def save_json(obj,path):
    with open(path,'w',encoding='utf-8') as f: json.dump(obj,f,indent=2,default=lambda x: None if (isinstance(x,float) and not np.isfinite(x)) else x)


def main():
    out=Path('/mnt/data/PRAYCG_NAST_OCM_Arrival_SnackAttack_AboutTime_v1_0')
    if out.exists(): shutil.rmtree(out)
    (out/'tables').mkdir(parents=True); (out/'report').mkdir(); (out/'figures').mkdir(); (out/'scripts').mkdir(); (out/'docs').mkdir()
    base=Path('/mnt/data/_analysis_work')
    datasets={
        'Arrival_Run1': {
            'features': base/'ArrivalEndScene_Run1_PostPeakPNCC_G2Theta_Handoff_Suite_v1_0/provenance/eeg_window_master_features.csv',
            'cue_json': base/'ArrivalEndScene_Run1_Master_Comprehensive_Suite_v1_0/logs/cue_schedule_Arrival_End_scene_v1_6Q.json',
            'segments': base/'ArrivalEndScene_Run1_Master_Comprehensive_Suite_v1_0/tables/segment_timing.csv',
            'notes':'Arrival run is ROI-metadata-cautioned: channel map confirmed true but confidence FALSE.'
        },
        'SnackAttack_Run1': {
            'features': base/'PRAYCG_SnackAttack_AboutTime_MRED_Rerun_v1_0/transformed_feature_tables/snack_attack_features_v1_4_compatible.csv',
            'cues': base/'PRAYCG_SnackAttack_AboutTime_MRED_Rerun_v1_0/source_outputs/SnackAttack_Run1_MRED_v1_4_3/tables/cue_marker_events.csv',
            'segments': base/'PRAYCG_SnackAttack_AboutTime_MRED_Rerun_v1_0/source_outputs/SnackAttack_Run1_MRED_v1_4_3/tables/segments_used.csv',
            'notes':'Snack Attack run has confirmed locked channel map in event metadata.'
        },
        'AboutTime_Run2': {
            'features': base/'PRAYCG_SnackAttack_AboutTime_MRED_Rerun_v1_0/transformed_feature_tables/about_time_run2_features_v1_4_compatible.csv',
            'cues': base/'PRAYCG_SnackAttack_AboutTime_MRED_Rerun_v1_0/source_outputs/AboutTime_Run2_MRED_v1_4_3/tables/cue_marker_events.csv',
            'segments': base/'PRAYCG_SnackAttack_AboutTime_MRED_Rerun_v1_0/source_outputs/AboutTime_Run2_MRED_v1_4_3/tables/segments_used.csv',
            'notes':'About Time Run 2 has confirmed locked channel map and same-source Target/Override.'
        }
    }
    all_trans=[]; all_onsets=[]; all_nast_overlays=[]; all_ocm=[]; all_pseudo=[]; all_ocm_overlays=[]; interpretations={}
    for run,meta in datasets.items():
        raw=pd.read_csv(meta['features'])
        can=canonicalize(raw,run)
        can.to_csv(out/'tables'/f'{run}_canonical_feature_frame_for_NAST_OCM.csv',index=False)
        trans,onset,nast_overlay,nast_interp=run_nast(can,run)
        trans.insert(0,'run',run); onset.insert(0,'run_name',run)
        trans.to_csv(out/'tables'/f'{run}_nast_phase_transition_table.csv',index=False)
        onset.to_csv(out/'tables'/f'{run}_nast_absorption_onset_candidates.csv',index=False)
        nast_overlay.to_csv(out/'tables'/f'{run}_nast_visual_overlay.csv',index=False)
        all_trans.append(trans); all_onsets.append(onset); all_nast_overlays.append(nast_overlay)
        if 'cues' in meta:
            cues=pd.read_csv(meta['cues'])
        else:
            cues=create_arrival_cue_table(str(meta['cue_json']), str(meta['segments']))
            cues.to_csv(out/'tables'/f'{run}_cue_table_constructed_from_schedule.csv',index=False)
        ocm,pseudo,ocm_overlay,ocm_interp=run_ocm(can,cues,run)
        ocm.to_csv(out/'tables'/f'{run}_ocm_cue_epoch_table.csv',index=False)
        pseudo.to_csv(out/'tables'/f'{run}_ocm_pseudo_cue_nulls.csv',index=False)
        ocm_overlay.to_csv(out/'tables'/f'{run}_ocm_visual_overlay.csv',index=False)
        all_ocm.append(ocm); all_pseudo.append(pseudo); all_ocm_overlays.append(ocm_overlay)
        interpretations[run]={'dataset_notes':meta['notes'],'nast':nast_interp,'ocm':ocm_interp}
    combined_trans=pd.concat(all_trans,ignore_index=True)
    combined_onsets=pd.concat(all_onsets,ignore_index=True)
    combined_ocm=pd.concat(all_ocm,ignore_index=True)
    combined_pseudo=pd.concat(all_pseudo,ignore_index=True)
    combined_nast_overlay=pd.concat(all_nast_overlays,ignore_index=True) if all_nast_overlays else pd.DataFrame()
    combined_ocm_overlay=pd.concat(all_ocm_overlays,ignore_index=True) if all_ocm_overlays else pd.DataFrame()
    combined_trans.to_csv(out/'tables'/'combined_nast_phase_transition_table.csv',index=False)
    combined_onsets.to_csv(out/'tables'/'combined_nast_absorption_onset_candidates.csv',index=False)
    combined_ocm.to_csv(out/'tables'/'combined_ocm_cue_epoch_table.csv',index=False)
    combined_pseudo.to_csv(out/'tables'/'combined_ocm_pseudo_cue_nulls.csv',index=False)
    combined_nast_overlay.to_csv(out/'tables'/'combined_nast_visual_overlay.csv',index=False)
    combined_ocm_overlay.to_csv(out/'tables'/'combined_ocm_visual_overlay.csv',index=False)
    # summaries
    ocm_summary=pd.DataFrame([interpretations[r]['ocm'] for r in interpretations])
    nast_summary=pd.DataFrame([interpretations[r]['nast'] for r in interpretations])
    ocm_summary.to_csv(out/'tables'/'combined_ocm_summary.csv',index=False)
    nast_summary.to_csv(out/'tables'/'combined_nast_summary.csv',index=False)
    save_json(interpretations,out/'tables'/'nast_ocm_interpretation.json')
    # figures
    import matplotlib.pyplot as plt
    # per-run NAS timeline
    for run in datasets:
        df=pd.read_csv(out/'tables'/f'{run}_canonical_feature_frame_for_NAST_OCM.csv')
        # recompute with overlay data by merging time if possible
        trans,onset,overlay,interp=run_nast(df,run)
        fig,ax=plt.subplots(figsize=(10,4))
        # need use internal d, recompute quickly
        d=df.copy(); d['alpha_drop_z']=robust_z(compute_alpha_drop(d,10).fillna(0)); d['NAS_raw']=(0.30*d['alpha_drop_z']+0.25*d['meaning_gamma_z']+0.25*d['tsp_z']+0.10*d['api_a_z']-0.20*d['task_gamma_z']-0.20*d['artifact_z']-0.10*d['visual_gamma_z']); d['NAS_z']=robust_z(d['NAS_raw'])
        for ph, sub in d.groupby('phase'):
            if ph in ['BASELINE_1','CONTROL_1','WASHOUT_1','TARGET_1','WASHOUT_2','CONTEXTUAL_OVERRIDE_1']:
                ax.plot(sub['time']-d['time'].min(), sub['NAS_z'], label=ph, linewidth=1)
        ax.axhline(np.nanpercentile(d.loc[d['phase'].isin(['BASELINE_1','CONTROL_1']),'NAS_z'],95), linestyle='--', linewidth=1, label='null q95')
        ax.set_title(f'{run}: NAST narrative-absorption proxy timeline')
        ax.set_xlabel('seconds from first analyzed window'); ax.set_ylabel('NAS z')
        ax.legend(fontsize=7, ncol=3)
        fig.tight_layout(); fig.savefig(out/'figures'/f'{run}_nast_timeline.png',dpi=180); plt.close(fig)
    # OCM summary figure
    if not combined_ocm.empty:
        fig,ax=plt.subplots(figsize=(8,4))
        plotdf=combined_ocm.groupby('run')[['digit_recognition_DR','working_memory_update_WMU','override_minus_target_WMU']].mean().reset_index()
        x=np.arange(len(plotdf)); width=0.25
        ax.bar(x-width, plotdf['digit_recognition_DR'], width, label='DR')
        ax.bar(x, plotdf['working_memory_update_WMU'], width, label='WMU')
        ax.bar(x+width, plotdf['override_minus_target_WMU'], width, label='Override-Target WMU')
        ax.set_xticks(x); ax.set_xticklabels(plotdf['run'], rotation=20, ha='right')
        ax.set_ylabel('mean z-delta'); ax.set_title('OCM cue-locked microstate summary')
        ax.legend(); fig.tight_layout(); fig.savefig(out/'figures'/'combined_ocm_summary.png',dpi=180); plt.close(fig)
    # write method notes md
    md=[]
    md.append('# NAST_v0.1 and OCM_v0.1 Analysis Rerun\n')
    md.append('This package formalizes and applies two additional PR-AYC-G modules: Narrative Absorption State Transition (NAST) and Override Cue Microstate Analysis (OCM).\n')
    md.append('NAST is a DMN-proxy / absorption-transition analysis, not direct DMN detection. OCM is a cue-locked working-memory analysis of the Override branch.\n')
    (out/'report'/'NAST_OCM_Rerun_Report_v1_0.md').write_text('\n'.join(md),encoding='utf-8')
    return out

if __name__=='__main__':
    main()
