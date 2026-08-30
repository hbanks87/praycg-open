#!/usr/bin/env python3
"""PRAYCG NIP/BIT/CII/IAQ + CET/EET Module v1.5.1.

Implements:
- NIP_v0.1: Narrative Immersion Proxy
- BIT_v0.1: Bivariate Immersion Threshold
- CII_v0.1: Continuous Immersion Index
- IAQ_v0.1: Immersion Attenuation Quotient
- CET_EET_v0.1: Cinematic Entrainment Tracking, residualization, and Endogenous Echo Tracking

Boundary: macroscopic PRAYCG analysis proxies only. This script does not measure dopamine,
oxytocin, OSM biology, microtubules, biophotons, consciousness, or hidden cellular Y.
"""
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import welch
try:
    import cv2
except Exception:
    cv2=None
VERSION="1.5.1"

def robust_z(x, eps=1e-9):
    x=np.asarray(x,dtype=float); x[~np.isfinite(x)]=np.nan
    if not np.any(np.isfinite(x)): return np.full_like(x,np.nan)
    med=np.nanmedian(x); mad=np.nanmedian(np.abs(x-med)); scale=1.4826*mad if mad>eps else np.nanstd(x)
    if not np.isfinite(scale) or scale<eps: scale=1.0
    return (x-med)/(scale+eps)
def pos(x): return np.maximum(np.asarray(x,dtype=float),0)
def safe_mean(x):
    x=np.asarray(x,dtype=float); return float(np.nanmean(x)) if np.any(np.isfinite(x)) else np.nan
def cosine(a,b):
    a=np.asarray(a,dtype=float); b=np.asarray(b,dtype=float); ok=np.isfinite(a)&np.isfinite(b)
    if ok.sum()<2: return np.nan
    a=a[ok]; b=b[ok]; na=np.linalg.norm(a); nb=np.linalg.norm(b)
    return float(np.dot(a,b)/(na*nb)) if na and nb else np.nan
def corr_lag(x,y,maxlag=10):
    x=np.asarray(x,dtype=float); y=np.asarray(y,dtype=float); best=(np.nan,0)
    for lag in range(-maxlag,maxlag+1):
        xs=x[-lag:] if lag<0 else x[:-lag] if lag>0 else x
        ys=y[:len(y)+lag] if lag<0 else y[lag:] if lag>0 else y
        ok=np.isfinite(xs)&np.isfinite(ys)
        if ok.sum()<5 or np.nanstd(xs[ok])==0 or np.nanstd(ys[ok])==0: continue
        r=float(np.corrcoef(xs[ok],ys[ok])[0,1])
        if not np.isfinite(best[0]) or abs(r)>abs(best[0]): best=(r,lag)
    return best
def dominant_freq(x,fs=1.0,fmin=.02,fmax=.5):
    x=np.asarray(x,dtype=float); ok=np.isfinite(x)
    if ok.sum()<16 or np.nanstd(x[ok])==0: return np.nan,np.nan
    x=np.interp(np.arange(len(x)),np.where(ok)[0],x[ok]); x=x-np.nanmean(x)
    f,p=welch(x,fs=fs,nperseg=min(128,len(x))); mask=(f>=fmin)&(f<=fmax)
    if not np.any(mask): return np.nan,np.nan
    i=np.argmax(p[mask]); return float(f[mask][i]),float(p[mask][i])

def add_cue_cols(df,cues,cue_design=None,sensor_design=None):
    df=df.copy(); off=df['condition_offset_sec'].to_numpy(dtype=float)
    cue_on=np.zeros(len(df)); cue_edge=np.zeros(len(df)); cue_value=np.full(len(df),np.nan); cue_idx=np.full(len(df),np.nan)
    for ce in cues:
        s=float(ce.get('start_sec',np.nan)); e=float(ce.get('end_sec',np.nan))
        if not np.isfinite(s): continue
        on=(off>=s)&(off<=e); edge=(off>=s)&(off<s+1.0)
        cue_on[on]=1; cue_edge[edge]=1; cue_value[on]=ce.get('value',np.nan); cue_idx[on]=ce.get('cue_index',np.nan)
    df['cue_on']=cue_on; df['cue_edge']=cue_edge; df['cue_value_active']=cue_value; df['cue_index_active']=cue_idx
    interval=float((cue_design or {}).get('interval_sec',3.0)); start=float((cue_design or {}).get('start_delay_sec',3.0))+float((sensor_design or {}).get('content_start_offset_sec',0.0))
    phase=((off-start)%interval)/interval*2*np.pi; df['cue_phase_sin']=np.sin(phase); df['cue_phase_cos']=np.cos(phase)
    return df

def extract_visualizer_proxy(video_path, out_csv, crop_height=540, max_sec=None):
    if not video_path or cv2 is None or not Path(video_path).exists(): return None
    cap=cv2.VideoCapture(str(video_path)); fps=cap.get(cv2.CAP_PROP_FPS) or 24.0; frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0); dur=frames/fps if fps else 0
    limit=min(dur, max_sec or dur); vals=[]; prev=None
    for sec in np.arange(0,limit,1.0):
        cap.set(cv2.CAP_PROP_POS_MSEC, sec*1000); ok,frame=cap.read()
        if not ok: continue
        crop=frame[:int(crop_height),:,:]
        gray=cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY); lum=float(gray.mean())
        change=float(np.mean(np.abs(gray.astype(float)-prev.astype(float)))) if prev is not None else np.nan
        prev=gray; vals.append({'condition':'TARGET_1','condition_offset_sec':float(sec),'video_luminance_proxy':lum,'video_change_proxy':change})
    cap.release(); v=pd.DataFrame(vals)
    if len(v):
        v['video_luminance_z']=robust_z(v['video_luminance_proxy']); v['video_change_z']=robust_z(v['video_change_proxy']); v.to_csv(out_csv,index=False)
        return v
    return None

def run(args):
    out=Path(args.out_dir); (out/'tables').mkdir(parents=True,exist_ok=True); (out/'figures').mkdir(exist_ok=True)
    feat=pd.read_csv(args.feature_csv); events=pd.read_csv(args.event_csv) if args.event_csv else pd.DataFrame(); ann=pd.read_csv(args.annotation_csv) if args.annotation_csv else pd.DataFrame()
    cue={}
    if args.cue_schedule_json:
        with open(args.cue_schedule_json,encoding='utf-8') as f: cue=json.load(f)
    f=feat.copy();
    for req in ['meaninggamma_score','tsp_z','nas_score','alpha_drop_proxy_z','gamma_visual_30_45_z','artifact_score','theta_integration_z','condition','condition_offset_sec','time_lsl']:
        if req not in f.columns: raise ValueError(f'Missing required feature column: {req}')
    f['artifact_z']=robust_z(f['artifact_score']); f['theta_future_10_30_z']=[safe_mean(f.loc[(f.time_lsl>=t+10)&(f.time_lsl<=t+30),'theta_integration_z']) for t in f.time_lsl]
    f['A_sem_raw']=0.35*pos(f.meaninggamma_score)+0.35*pos(f.tsp_z)+0.15*pos(f.nas_score)+0.15*pos(f.alpha_drop_proxy_z)-0.12*pos(f.gamma_visual_30_45_z)-0.15*pos(f.artifact_z)
    f['A_sem']=pos(f.A_sem_raw)
    f['R_int_raw']=0.70*pos(f.theta_future_10_30_z)+0.20*pos(f.theta_integration_z)+0.10*pos(f.nas_score)-0.15*pos(f.artifact_z)
    f['R_int']=pos(f.R_int_raw); f['artifact_penalty']=np.exp(-0.15*pos(f.artifact_z)); f['visual_penalty']=np.exp(-0.05*pos(f.gamma_visual_30_45_z))
    f['NIP_density']=f.A_sem*f.R_int*f.artifact_penalty*f.visual_penalty; f['NIP_density_z']=robust_z(f.NIP_density)
    f=add_cue_cols(f,cue.get('cue_events',[]),cue.get('cue_design',{}),cue.get('sensor_timing_design',{})); f.to_csv(out/'tables/nip_component_timeseries.csv',index=False)
    conds=[c for c in ['CONTROL_1','TARGET_1','CONTEXTUAL_OVERRIDE_1'] if c in set(f.condition)]
    # BIT
    if len(events):
        e=events.copy(); near=[]
        for _,r in e.iterrows():
            sub=f[f.condition==r['condition']];
            if len(sub):
                idx=(sub.condition_offset_sec-float(r.condition_offset_sec)).abs().idxmin(); row=f.loc[idx]
                near.append({'artifact_z_nearest':row.artifact_z,'artifact_score_nearest':row.artifact_score,'NIP_density_nearest':row.NIP_density,'A_sem_nearest':row.A_sem,'R_int_nearest':row.R_int})
            else: near.append({})
        e=pd.concat([e,pd.DataFrame(near)],axis=1)
        e['BIT_attention_gate']=(e.MR_score>0)&(e.A_sem_nearest>0); e['BIT_resonance_gate']=(e.ENC_score>0)&(e.theta_delta_10_30>0)&(e.R_int_nearest>0)
        e['BIT_k_gate']=(e.K_percentile_by_condition>=90)&(e.K_HT_topo_local>0); e['BIT_artifact_gate']=e.artifact_z_nearest.fillna(0)<2.5
        e['BIT_mred_gate']=e.mred_quadrant.astype(str).str.contains('MR_HIGH_ENC_HIGH'); e['BIT_eventlock_gate']=e.event_lock_candidate.astype(bool) if 'event_lock_candidate' in e.columns else False
        e['BIT_pass_event_only']=e.BIT_attention_gate&e.BIT_resonance_gate&e.BIT_k_gate&e.BIT_artifact_gate&e.BIT_mred_gate; e['BIT_pass_praycg_strict']=e.BIT_pass_event_only&e.BIT_eventlock_gate&(e.condition=='TARGET_1')
        e.to_csv(out/'tables/bit_event_table.csv',index=False)
    # CII / IAQ
    if len(ann):
        branch_starts={c:float(f.loc[f.condition==c,'time_lsl'].min()) for c in conds}; rows=[]
        for _,a in ann.iterrows():
            start=float(a.get('peak_search_start_sec',a.get('rendered_time_sec_estimate',0))); end=float(a.get('theta_end_sec',start+30))
            for cond in conds:
                t0=branch_starts[cond]+start; t1=branch_starts[cond]+end; sub=f[(f.time_lsl>=t0)&(f.time_lsl<=t1)]
                rows.append({'anchor_id':a.get('anchor_id','anchor'),'scene_label':a.get('scene_label',''),'condition':cond,'window_start_sec':start,'window_end_sec':end,'n_rows':len(sub),'A_sem_mean':safe_mean(sub.A_sem),'R_int_mean':safe_mean(sub.R_int),'NIP_density_mean_CII':safe_mean(sub.NIP_density),'MeaningGamma_mean':safe_mean(sub.meaninggamma_score),'TSP_mean':safe_mean(sub.tsp_z),'theta_future_mean':safe_mean(sub.theta_future_10_30_z),'artifact_mean':safe_mean(sub.artifact_score),'visual_drive_mean':safe_mean(sub.gamma_visual_30_45_z)})
        cii=pd.DataFrame(rows); cii.to_csv(out/'tables/cii_anchor_integrals.csv',index=False)
        iaq=[]
        for anchor,g in cii.groupby('anchor_id'):
            vals={r.condition:r for _,r in g.iterrows()};
            if 'TARGET_1' in vals:
                T=vals['TARGET_1'].NIP_density_mean_CII; O=vals.get('CONTEXTUAL_OVERRIDE_1',pd.Series()).get('NIP_density_mean_CII',np.nan); C=vals.get('CONTROL_1',pd.Series()).get('NIP_density_mean_CII',np.nan); eps=1e-6
                iaq.append({'anchor_id':anchor,'scene_label':vals['TARGET_1'].scene_label,'CII_Target':T,'CII_Control':C,'CII_Override':O,'Target_minus_Control_CII':T-C if np.isfinite(C) else np.nan,'Target_minus_Override_CII':T-O if np.isfinite(O) else np.nan,'IAQ_Target_vs_Override':1-((O+eps)/(T+eps)) if np.isfinite(T) and np.isfinite(O) and abs(T)>eps else np.nan,'Target_greater_Control':bool(np.isfinite(C) and T>C),'Target_greater_Override':bool(np.isfinite(O) and T>O)})
        pd.DataFrame(iaq).to_csv(out/'tables/iaq_target_override_table.csv',index=False)
    # CET tracking
    cet=[]
    for cond in conds:
        sub=f[f.condition==cond].sort_values('condition_offset_sec'); cuev=sub.cue_on.to_numpy(float)
        for sig in ['meaninggamma_score','tsp_z','taskgamma_score','theta_integration_z','gamma_visual_30_45_z','gamma_front_35_40_z','nas_score','NIP_density']:
            r,lag=corr_lag(cuev,sub[sig].to_numpy(float),args.max_lag_sec); df,pow=dominant_freq(sub[sig].to_numpy(float))
            cet.append({'condition':cond,'stimulus_regressor':'cue_on_3s','signal':sig,'max_abs_corr':r,'lag_sec_signal_after_regressor':lag,'signal_dominant_freq_hz':df,'signal_dominant_power':pow,'cue_frequency_hz':1/3})
    pd.DataFrame(cet).to_csv(out/'tables/cet_cue_tracking_summary.csv',index=False)
    visual=None
    if args.stimulus_video_proxy:
        visual=extract_visualizer_proxy(args.stimulus_video_proxy,out/'tables/cet_visualizer_target_video_proxy_timeseries.csv',args.video_crop_height,args.max_video_proxy_sec)
        if visual is not None:
            tgt=f[f.condition=='TARGET_1'].copy(); tgt['sec_round']=tgt.condition_offset_sec.round().astype(int); visual['sec_round']=visual.condition_offset_sec.round().astype(int); m=tgt.merge(visual[['sec_round','video_luminance_z','video_change_z']],on='sec_round',how='left')
            rows=[]
            for reg in ['video_luminance_z','video_change_z']:
                for sig in ['meaninggamma_score','tsp_z','theta_integration_z','gamma_visual_30_45_z','NIP_density']:
                    r,lag=corr_lag(m[reg].to_numpy(float),m[sig].to_numpy(float),args.max_lag_sec); rows.append({'condition':'TARGET_1','stimulus_regressor':reg,'signal':sig,'max_abs_corr':r,'lag_sec_signal_after_regressor':lag})
            pd.DataFrame(rows).to_csv(out/'tables/cet_visualizer_target_video_proxy_tracking.csv',index=False)
    # Residualization
    resrows=[]; resdfs=[]
    for cond in conds:
        sub=f[f.condition==cond].copy().sort_values('condition_offset_sec'); Xcols=['cue_on','cue_phase_sin','cue_phase_cos']
        if cond=='TARGET_1' and visual is not None:
            sub['sec_round']=sub.condition_offset_sec.round().astype(int); visual['sec_round']=visual.condition_offset_sec.round().astype(int); sub=sub.merge(visual[['sec_round','video_luminance_z','video_change_z']],on='sec_round',how='left');
            for col in ['video_luminance_z','video_change_z']: sub[col]=sub[col].fillna(0); Xcols.append(col)
        y=sub.NIP_density.to_numpy(float); X=np.column_stack([np.ones(len(sub))]+[sub[c].fillna(0).to_numpy(float) for c in Xcols]); ok=np.isfinite(y)&np.all(np.isfinite(X),axis=1)
        if ok.sum()>5:
            beta=np.linalg.lstsq(X[ok],y[ok],rcond=None)[0]; yhat=X@beta; ss_res=np.nansum((y[ok]-yhat[ok])**2); ss_tot=np.nansum((y[ok]-np.nanmean(y[ok]))**2); r2=1-ss_res/ss_tot if ss_tot>0 else np.nan; sub['NIP_density_residualized_CET']=y-yhat+np.nanmean(y[ok])
        else: beta=[]; r2=np.nan; sub['NIP_density_residualized_CET']=np.nan
        resrows.append({'condition':cond,'dependent':'NIP_density','regressors':'+'.join(Xcols),'n_rows':int(ok.sum()),'r2_exogenous_tracking':r2,'beta_json':json.dumps([float(x) for x in beta]) if len(beta) else '[]'}); resdfs.append(sub)
    resdf=pd.concat(resdfs,ignore_index=True); resdf.to_csv(out/'tables/nip_residualized_by_cet_timeseries.csv',index=False); pd.DataFrame(resrows).to_csv(out/'tables/cet_residualization_model_summary.csv',index=False)
    if len(ann):
        rr=[]
        for _,a in ann.iterrows():
            start=float(a.get('peak_search_start_sec',a.get('rendered_time_sec_estimate',0))); end=float(a.get('theta_end_sec',start+30))
            for cond in conds:
                sub=resdf[(resdf.condition==cond)&(resdf.condition_offset_sec>=start)&(resdf.condition_offset_sec<=min(end,resdf[resdf.condition==cond].condition_offset_sec.max()))]
                rr.append({'anchor_id':a.get('anchor_id','anchor'),'scene_label':a.get('scene_label',''),'condition':cond,'window_start_sec':start,'window_end_sec':end,'NIP_density_residualized_CET_mean':safe_mean(sub.NIP_density_residualized_CET),'n_rows':len(sub)})
        pd.DataFrame(rr).to_csv(out/'tables/cet_residualized_cii_anchor_integrals.csv',index=False)
    # EET
    echo_features=[c for c in ['meaninggamma_score','tsp_z','theta_integration_z','nas_score','alpha_drop_proxy_z','NIP_density','gamma_pt_30_45_z','gamma_front_35_40_z'] if c in f.columns]
    def vec(cond,start,end):
        sub=f[(f.condition==cond)&(f.condition_offset_sec>=start)&(f.condition_offset_sec<=end)]; return np.array([safe_mean(sub[c]) for c in echo_features]),len(sub)
    refs=[]
    for name,cond,start,end in [('WASHOUT_2_first30','WASHOUT_2',0,30),('WASHOUT_2_first45','WASHOUT_2',0,45),('WASHOUT_2_first60','WASHOUT_2',0,60),('BASELINE_2_first30','BASELINE_2_REFLECTION',0,30),('BASELINE_2_all','BASELINE_2_REFLECTION',0,999)]:
        if cond in set(f.condition): refs.append((name,*vec(cond,start,end)))
    if len(ann):
        er=[]
        for _,a in ann.iterrows():
            start=float(a.get('peak_search_start_sec',a.get('rendered_time_sec_estimate',0))); end=float(a.get('peak_search_end_sec',start+10)); av,an=vec('TARGET_1',start,end)
            for name,rv,rn in refs: er.append({'anchor_id':a.get('anchor_id','anchor'),'scene_label':a.get('scene_label',''),'target_window_start':start,'target_window_end':end,'reference_window':name,'target_rows':an,'reference_rows':rn,'cosine_similarity':cosine(av,rv),'euclidean_distance':float(np.linalg.norm(np.nan_to_num(av)-np.nan_to_num(rv)))})
        pd.DataFrame(er).to_csv(out/'tables/eet_endogenous_echo_tracking.csv',index=False)
    # Overlay and interpretation
    overlay=[]
    bitfile=out/'tables/bit_event_table.csv'
    if bitfile.exists():
        be=pd.read_csv(bitfile)
        for _,r in be[be.get('BIT_pass_praycg_strict',False)==True].iterrows(): overlay.append({'start_sec':r.condition_offset_sec,'end_sec':r.condition_offset_sec+2,'label':f"BIT_PASS {r.anchor_metric} K={r.K_HT_topo_local:.2f}",'category':'bit','source':'NIP_BIT_v0.1'})
    iaqfile=out/'tables/iaq_target_override_table.csv'
    if iaqfile.exists():
        iaq=pd.read_csv(iaqfile)
        for _,r in iaq.iterrows():
            if bool(r.Target_greater_Override):
                ar=ann[ann.anchor_id==r.anchor_id] if len(ann) else pd.DataFrame()
                t=float(ar.iloc[0].rendered_time_sec_estimate) if len(ar) else 0
                overlay.append({'start_sec':max(0,t-3),'end_sec':t+3,'label':f"IAQ+ {r.anchor_id} IAQ={r.IAQ_Target_vs_Override:.2f}",'category':'iaq','source':'NIP_IAQ_v0.1'})
    pd.DataFrame(overlay).to_csv(out/'tables/nip_cet_eet_visual_overlay.csv',index=False)
    summary={'schema':'PRAYCG_NIP_CET_EET_v1_5_1','feature_csv':str(args.feature_csv),'event_csv':str(args.event_csv),'annotation_csv':str(args.annotation_csv),'cue_schedule_json':str(args.cue_schedule_json),'mean_NIP_density_by_condition':f.groupby('condition').NIP_density.mean().to_dict(),'boundary':'Macroscopic PRAYCG proxy layer only; no dopamine, oxytocin, OSM biology, microtubule, biophoton, consciousness, or hidden-Y claim.'}
    with open(out/'tables/nip_cet_eet_interpretation.json','w',encoding='utf-8') as fp: json.dump(summary,fp,indent=2)
    print(json.dumps(summary,indent=2))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--feature-csv',required=True)
    ap.add_argument('--event-csv',default='')
    ap.add_argument('--annotation-csv',default='')
    ap.add_argument('--cue-schedule-json',default='')
    ap.add_argument('--stimulus-video-proxy',default='',help='Optional MP4 proxy. For visualizer MP4, top video region can be cropped.')
    ap.add_argument('--video-crop-height',type=int,default=540)
    ap.add_argument('--max-video-proxy-sec',type=float,default=301)
    ap.add_argument('--out-dir',required=True)
    ap.add_argument('--max-lag-sec',type=int,default=10)
    run(ap.parse_args())
if __name__=='__main__': main()
