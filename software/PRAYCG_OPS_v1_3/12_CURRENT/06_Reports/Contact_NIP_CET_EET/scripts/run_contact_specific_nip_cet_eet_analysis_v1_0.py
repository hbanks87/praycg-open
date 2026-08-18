import os, json, math, zipfile, shutil, textwrap, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import welch
from scipy.stats import spearmanr
try:
    import cv2
except Exception:
    cv2 = None

ROOT=Path('/mnt/data')
OUT=ROOT/'PRAYCG_Contact_Run1_NIP_CET_EET_Analysis_v1_0'
if OUT.exists(): shutil.rmtree(OUT)
(OUT/'tables').mkdir(parents=True)
(OUT/'figures').mkdir()
(OUT/'report').mkdir()
(OUT/'scripts').mkdir()

FEATURE=ROOT/'PRAYCG_Contact_Run1_Requested_Anchor_MRED_Files_v1_0'/'Contact_Run1_feature_table_contact_time_resolved_feature_frame_v1_0.csv'
EVENT=ROOT/'PRAYCG_Contact_Run1_Requested_Anchor_MRED_Files_v1_0'/'Contact_Run1_candidate_local_kht_topo_mred_event_table_v1_0.csv'
ANNOT=ROOT/'PRAYCG_Contact_Run1_Requested_Anchor_MRED_Files_v1_0'/'Contact_Run1_annotation_windows_v1_0.csv'
SCENE=ROOT/'PRAYCG_Contact_Run1_Requested_Anchor_MRED_Files_v1_0'/'Contact_Run1_MRED_scene_map_v1_0.csv'
FAM=ROOT/'PRAYCG_Contact_Run1_Requested_Anchor_MRED_Files_v1_0'/'Contact_Run1_MRED_familiarity_covariates_v1_0.csv'
CUE=ROOT/'contact_qc/qc/cue_schedule_Contact_final_scene_v1_6S.json'
MANIFEST=ROOT/'contact_qc/qc/media_prep_manifest_v1_6S.json'
VISVID=ROOT/'contact analysis vid.mp4'

feat=pd.read_csv(FEATURE)
events=pd.read_csv(EVENT)
ann=pd.read_csv(ANNOT)
scene=pd.read_csv(SCENE)
fam=pd.read_csv(FAM)
with open(CUE,encoding='utf-8') as f: cue=json.load(f)
with open(MANIFEST,encoding='utf-8') as f: manifest=json.load(f)

# ---------- utility ----------
def robust_z(x, eps=1e-9):
    x=np.asarray(x,dtype=float)
    x[~np.isfinite(x)]=np.nan
    med=np.nanmedian(x)
    mad=np.nanmedian(np.abs(x-med))
    scale=1.4826*mad if mad>eps else np.nanstd(x)
    if not np.isfinite(scale) or scale<eps: scale=1.0
    return (x-med)/(scale+eps)

def pos(x): return np.maximum(np.asarray(x,dtype=float),0)

def safe_mean(x):
    x=np.asarray(x,dtype=float)
    return float(np.nanmean(x)) if np.any(np.isfinite(x)) else np.nan

def safe_std(x):
    x=np.asarray(x,dtype=float)
    return float(np.nanstd(x)) if np.any(np.isfinite(x)) else np.nan

def clip01(x):
    return max(0,min(1,float(x))) if np.isfinite(x) else np.nan

def cosine(a,b):
    a=np.asarray(a,dtype=float); b=np.asarray(b,dtype=float)
    ok=np.isfinite(a)&np.isfinite(b)
    if ok.sum()<2: return np.nan
    a=a[ok]; b=b[ok]
    na=np.linalg.norm(a); nb=np.linalg.norm(b)
    if na==0 or nb==0: return np.nan
    return float(np.dot(a,b)/(na*nb))

def corr_lag(x,y,maxlag=10):
    x=np.asarray(x,dtype=float); y=np.asarray(y,dtype=float)
    best=(np.nan,0)
    for lag in range(-maxlag,maxlag+1):
        if lag<0:
            xs=x[-lag:]; ys=y[:len(y)+lag]
        elif lag>0:
            xs=x[:-lag]; ys=y[lag:]
        else:
            xs=x; ys=y
        ok=np.isfinite(xs)&np.isfinite(ys)
        if ok.sum()<5 or np.nanstd(xs[ok])==0 or np.nanstd(ys[ok])==0: continue
        r=float(np.corrcoef(xs[ok],ys[ok])[0,1])
        if not np.isfinite(best[0]) or abs(r)>abs(best[0]): best=(r,lag)
    return best

def dominant_freq(x, fs=1.0, fmin=0.02, fmax=0.5):
    x=np.asarray(x,dtype=float)
    ok=np.isfinite(x)
    if ok.sum()<16 or np.nanstd(x[ok])==0: return (np.nan,np.nan)
    x=np.interp(np.arange(len(x)), np.where(ok)[0], x[ok])
    x=x-np.nanmean(x)
    nper=min(128, len(x))
    f,p=welch(x, fs=fs, nperseg=nper)
    mask=(f>=fmin)&(f<=fmax)
    if not np.any(mask): return (np.nan,np.nan)
    idx=np.argmax(p[mask]); return (float(f[mask][idx]), float(p[mask][idx]))

# ---------- NIP timeseries ----------
f=feat.copy()
f['artifact_z']=robust_z(f['artifact_score'])
f['visual_drive_z']=f.get('gamma_visual_30_45_z',0.0)
# future theta integration using absolute time; for branch rows includes following washout due to absolute time slice
future=[]
for i,row in f.iterrows():
    t=row['time_lsl']; cond=row['condition']
    mask=(f['time_lsl']>=t+10)&(f['time_lsl']<=t+30)
    # future is physiologically subsequent; no condition restriction to allow branch->washout carryover
    future.append(safe_mean(f.loc[mask,'theta_integration_z']))
f['theta_future_10_30_z']=future
f['A_sem_raw']=0.35*pos(f['meaninggamma_score'])+0.35*pos(f['tsp_z'])+0.15*pos(f['nas_score'])+0.15*pos(f['alpha_drop_proxy_z'])-0.12*pos(f['gamma_visual_30_45_z'])-0.15*pos(f['artifact_z'])
f['A_sem']=pos(f['A_sem_raw'])
f['R_int_raw']=0.70*pos(f['theta_future_10_30_z'])+0.20*pos(f['theta_integration_z'])+0.10*pos(f['nas_score'])-0.15*pos(f['artifact_z'])
f['R_int']=pos(f['R_int_raw'])
f['artifact_penalty']=np.exp(-0.15*pos(f['artifact_z']))
f['visual_penalty']=np.exp(-0.05*pos(f['gamma_visual_30_45_z']))
f['NIP_density']=f['A_sem']*f['R_int']*f['artifact_penalty']*f['visual_penalty']
f['NIP_density_z']=robust_z(f['NIP_density'])
f['NIP_density_clip']=pos(f['NIP_density'])
f.to_csv(OUT/'tables/nip_component_timeseries.csv', index=False)

# ---------- cue train ----------
cues=cue.get('cue_events',[])
def make_cue_cols(df):
    off=df['condition_offset_sec'].to_numpy(dtype=float)
    cue_on=np.zeros(len(df)); cue_edge=np.zeros(len(df)); cue_value=np.full(len(df),np.nan); cue_idx=np.full(len(df),np.nan)
    for ce in cues:
        s=float(ce.get('start_sec', np.nan)); e=float(ce.get('end_sec', np.nan)); val=ce.get('value',np.nan); idx=ce.get('cue_index',np.nan)
        if not np.isfinite(s): continue
        on=(off>=s)&(off<=e)
        cue_on[on]=1; cue_value[on]=val; cue_idx[on]=idx
        edge=(off>=s)&(off<s+1.0)
        cue_edge[edge]=1
    df=df.copy(); df['cue_on']=cue_on; df['cue_edge']=cue_edge; df['cue_value_active']=cue_value; df['cue_index_active']=cue_idx
    if len(cues):
        interval=float(cue.get('cue_design',{}).get('interval_sec',3.0))
        start=float(cue.get('cue_design',{}).get('start_delay_sec',3.0))+float(cue.get('sensor_timing_design',{}).get('content_start_offset_sec',0.0))
        # phase relative to first cue at rendered time (approx)
        phase=((off-start)%interval)/interval*2*np.pi
        df['cue_phase_sin']=np.sin(phase); df['cue_phase_cos']=np.cos(phase)
    else:
        df['cue_phase_sin']=0; df['cue_phase_cos']=0
    return df
f=make_cue_cols(f)
f.to_csv(OUT/'tables/nip_component_timeseries_with_cue_regressors.csv',index=False)

# ---------- Event BIT ----------
e=events.copy()
# Add artifact/NIP nearest values
nearest=[]
for _,r in e.iterrows():
    cond=r['condition']; t=r['condition_offset_sec']
    sub=f[f['condition']==cond]
    if len(sub)==0: nearest.append({}); continue
    idx=(sub['condition_offset_sec']-t).abs().idxmin()
    row=f.loc[idx]
    nearest.append({'artifact_score_nearest':row['artifact_score'],'artifact_z_nearest':row['artifact_z'],'NIP_density_nearest':row['NIP_density'],'A_sem_nearest':row['A_sem'],'R_int_nearest':row['R_int']})
e=pd.concat([e, pd.DataFrame(nearest)], axis=1)
e['BIT_attention_gate']=(e['MR_score']>0)&(e['A_sem_nearest']>0)
e['BIT_resonance_gate']=(e['ENC_score']>0)&(e['theta_delta_10_30']>0)&(e['R_int_nearest']>0)
e['BIT_k_gate']=(e['K_percentile_by_condition']>=90)&(e['K_HT_topo_local']>0)
e['BIT_artifact_gate']=e['artifact_z_nearest'].fillna(0)<2.5
e['BIT_mred_gate']=e['mred_quadrant'].astype(str).str.contains('MR_HIGH_ENC_HIGH')
e['BIT_eventlock_gate']=e['event_lock_candidate'].astype(bool)
e['BIT_pass_event_only']=e['BIT_attention_gate']&e['BIT_resonance_gate']&e['BIT_k_gate']&e['BIT_artifact_gate']&e['BIT_mred_gate']
e['BIT_pass_praycg_strict']=e['BIT_pass_event_only']&e['BIT_eventlock_gate']&(e['condition']=='TARGET_1')
e.to_csv(OUT/'tables/bit_event_table.csv', index=False)

# ---------- CII/IAQ anchors ----------
# function to collect data window across phase+washout by absolute time. uses branch start abs time + relative window.
branch_starts={c:float(f.loc[f['condition']==c,'time_lsl'].min()) for c in ['CONTROL_1','TARGET_1','CONTEXTUAL_OVERRIDE_1']}
conds=['CONTROL_1','TARGET_1','CONTEXTUAL_OVERRIDE_1']
rows=[]
for _,a in ann.iterrows():
    anchor=a['anchor_id']; label=a.get('scene_label','')
    # CII window from peak_search_start to theta_end, plus clipped if too long; default use annotation windows.
    start=float(a['peak_search_start_sec']); end=float(a['theta_end_sec'])
    if not np.isfinite(start) or not np.isfinite(end): continue
    for cond in conds:
        bstart=branch_starts[cond]
        t0=bstart+start; t1=bstart+end
        sub=f[(f['time_lsl']>=t0)&(f['time_lsl']<=t1)].copy()
        # exclude reports; absolute slice likely includes branch and washout
        dur=max(1e-9, end-start)
        rows.append({
            'anchor_id':anchor,'scene_label':label,'condition':cond,'window_start_sec':start,'window_end_sec':end,'duration_sec':dur,
            'n_rows':len(sub),'A_sem_mean':safe_mean(sub['A_sem']),'R_int_mean':safe_mean(sub['R_int']),'NIP_density_mean_CII':safe_mean(sub['NIP_density']),
            'NIP_density_sum':float(np.nansum(sub['NIP_density'])),'MeaningGamma_mean':safe_mean(sub['meaninggamma_score']),'TSP_mean':safe_mean(sub['tsp_z']),
            'theta_future_mean':safe_mean(sub['theta_future_10_30_z']),'theta_integration_mean':safe_mean(sub['theta_integration_z']),
            'artifact_mean':safe_mean(sub['artifact_score']),'visual_drive_mean':safe_mean(sub['gamma_visual_30_45_z']),
        })
cii=pd.DataFrame(rows)
# IAQ table per anchor
iaq=[]
for anchor,g in cii.groupby('anchor_id'):
    vals={r['condition']:r for _,r in g.iterrows()}
    if 'TARGET_1' not in vals: continue
    T=vals['TARGET_1']['NIP_density_mean_CII']; C=vals.get('CONTROL_1',{}).get('NIP_density_mean_CII',np.nan); O=vals.get('CONTEXTUAL_OVERRIDE_1',{}).get('NIP_density_mean_CII',np.nan)
    eps=1e-6
    iaq.append({
        'anchor_id':anchor,'scene_label':vals['TARGET_1'].get('scene_label',''),
        'CII_Target':T,'CII_Control':C,'CII_Override':O,
        'Target_minus_Control_CII':T-C if np.isfinite(T) and np.isfinite(C) else np.nan,
        'Target_minus_Override_CII':T-O if np.isfinite(T) and np.isfinite(O) else np.nan,
        'IAQ_Target_vs_Override':1-((O+eps)/(T+eps)) if np.isfinite(T) and np.isfinite(O) and abs(T)>eps else np.nan,
        'Target_greater_Control':bool(np.isfinite(T) and np.isfinite(C) and T>C),
        'Target_greater_Override':bool(np.isfinite(T) and np.isfinite(O) and T>O),
    })
iaq=pd.DataFrame(iaq)
cii.to_csv(OUT/'tables/cii_anchor_integrals.csv',index=False)
iaq.to_csv(OUT/'tables/iaq_target_override_table.csv',index=False)

# ---------- CET cue tracking ----------
cet=[]
for cond in conds:
    sub=f[f['condition']==cond].sort_values('condition_offset_sec').copy()
    cue_tr=sub['cue_on'].to_numpy(dtype=float)
    for sig in ['meaninggamma_score','tsp_z','taskgamma_score','theta_integration_z','gamma_visual_30_45_z','gamma_front_35_40_z','nas_score','NIP_density']:
        x=sub[sig].to_numpy(dtype=float)
        r,lag=corr_lag(cue_tr,x,maxlag=10)
        dfreq,dpow=dominant_freq(x,fs=1.0)
        cet.append({'condition':cond,'stimulus_regressor':'cue_on_3s','signal':sig,'max_abs_corr':r,'lag_sec_signal_after_regressor':lag,'signal_dominant_freq_hz':dfreq,'signal_dominant_power':dpow,'cue_frequency_hz':1/3})
cet=pd.DataFrame(cet)
cet.to_csv(OUT/'tables/cet_cue_tracking_summary.csv',index=False)

# ---------- visualizer-derived target visual features ----------
visual_ts=None
if VISVID.exists() and cv2 is not None:
    cap=cv2.VideoCapture(str(VISVID)); fps=cap.get(cv2.CAP_PROP_FPS) or 24.0; frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0); duration=frames/fps if fps else 0
    # sample once per second; crop top video area 0:540 based on visualizer report
    vals=[]; prev=None
    for sec in np.arange(0, min(duration, 301), 1.0):
        cap.set(cv2.CAP_PROP_POS_MSEC, sec*1000.0)
        ok,frame=cap.read()
        if not ok: continue
        crop=frame[:540,:,:]
        gray=cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        lum=float(gray.mean())
        change=float(np.mean(np.abs(gray.astype(float)-prev.astype(float)))) if prev is not None else np.nan
        prev=gray
        vals.append({'condition':'TARGET_1','condition_offset_sec':float(sec),'video_luminance_proxy':lum,'video_change_proxy':change})
    cap.release()
    visual_ts=pd.DataFrame(vals)
    if len(visual_ts):
        visual_ts['video_luminance_z']=robust_z(visual_ts['video_luminance_proxy'])
        visual_ts['video_change_z']=robust_z(visual_ts['video_change_proxy'])
        visual_ts.to_csv(OUT/'tables/cet_visualizer_target_video_proxy_timeseries.csv',index=False)
        # merge target visual features to target f
        tgt=f[f.condition=='TARGET_1'].copy()
        tgt['sec_round']=tgt['condition_offset_sec'].round().astype(int)
        visual_ts['sec_round']=visual_ts['condition_offset_sec'].round().astype(int)
        m=tgt.merge(visual_ts[['sec_round','video_luminance_z','video_change_z']],on='sec_round',how='left')
        rows=[]
        for reg in ['video_luminance_z','video_change_z']:
            regv=m[reg].to_numpy(dtype=float)
            for sig in ['meaninggamma_score','tsp_z','theta_integration_z','gamma_visual_30_45_z','NIP_density']:
                r,lag=corr_lag(regv,m[sig].to_numpy(dtype=float),maxlag=10)
                rows.append({'condition':'TARGET_1','stimulus_regressor':reg,'signal':sig,'max_abs_corr':r,'lag_sec_signal_after_regressor':lag})
        pd.DataFrame(rows).to_csv(OUT/'tables/cet_visualizer_target_video_proxy_tracking.csv',index=False)

# ---------- CET-R residualization ----------
# Regression per condition: NIP_density ~ cue_on + cue_phase sin/cos (+ visual proxy for target if available)
resrows=[]; cii_res=[]
res_dfs=[]
for cond in conds:
    sub=f[f.condition==cond].copy().sort_values('condition_offset_sec')
    Xcols=['cue_on','cue_phase_sin','cue_phase_cos']
    # target-only add visualizer video proxies if available
    if cond=='TARGET_1' and visual_ts is not None and len(visual_ts):
        sub['sec_round']=sub['condition_offset_sec'].round().astype(int)
        v=visual_ts.copy(); v['sec_round']=v['condition_offset_sec'].round().astype(int)
        sub=sub.merge(v[['sec_round','video_luminance_z','video_change_z']],on='sec_round',how='left')
        for col in ['video_luminance_z','video_change_z']:
            sub[col]=sub[col].fillna(0)
            Xcols.append(col)
    y=sub['NIP_density'].to_numpy(dtype=float)
    X=np.column_stack([np.ones(len(sub))]+[sub[c].fillna(0).to_numpy(dtype=float) for c in Xcols])
    ok=np.isfinite(y)&np.all(np.isfinite(X),axis=1)
    if ok.sum()>5:
        beta=np.linalg.lstsq(X[ok],y[ok],rcond=None)[0]
        yhat=X@beta
        ss_res=np.nansum((y[ok]-yhat[ok])**2); ss_tot=np.nansum((y[ok]-np.nanmean(y[ok]))**2); r2=1-ss_res/ss_tot if ss_tot>0 else np.nan
        sub['NIP_density_residualized_CET']=y-yhat+np.nanmean(y[ok])
    else:
        beta=[]; r2=np.nan; sub['NIP_density_residualized_CET']=np.nan
    resrows.append({'condition':cond,'dependent':'NIP_density','regressors':'+'.join(Xcols),'n_rows':int(ok.sum()),'r2_exogenous_tracking':r2,'beta_json':json.dumps([float(x) for x in beta]) if len(beta) else '[]'})
    res_dfs.append(sub)
resdf=pd.concat(res_dfs,ignore_index=True)
resdf.to_csv(OUT/'tables/nip_residualized_by_cet_timeseries.csv',index=False)
pd.DataFrame(resrows).to_csv(OUT/'tables/cet_residualization_model_summary.csv',index=False)
# residualized cii anchor integrals
for _,a in ann.iterrows():
    anchor=a['anchor_id']; label=a.get('scene_label','')
    start=float(a['peak_search_start_sec']); end=float(a['theta_end_sec'])
    for cond in conds:
        sub=resdf[(resdf.condition==cond)&(resdf.condition_offset_sec>=start)&(resdf.condition_offset_sec<=min(end, resdf[resdf.condition==cond].condition_offset_sec.max()))]
        cii_res.append({'anchor_id':anchor,'scene_label':label,'condition':cond,'window_start_sec':start,'window_end_sec':end,'NIP_density_residualized_CET_mean':safe_mean(sub['NIP_density_residualized_CET']),'n_rows':len(sub)})
pd.DataFrame(cii_res).to_csv(OUT/'tables/cet_residualized_cii_anchor_integrals.csv',index=False)

# ---------- EET echo tracking ----------
echo_features=['meaninggamma_score','tsp_z','theta_integration_z','nas_score','alpha_drop_proxy_z','NIP_density','gamma_pt_30_45_z','gamma_front_35_40_z']
def vec_for(cond=None,start=None,end=None,abs_start=None,abs_end=None):
    sub=f.copy()
    if cond is not None: sub=sub[sub.condition==cond]
    if start is not None: sub=sub[sub.condition_offset_sec>=start]
    if end is not None: sub=sub[sub.condition_offset_sec<=end]
    if abs_start is not None: sub=sub[sub.time_lsl>=abs_start]
    if abs_end is not None: sub=sub[sub.time_lsl<=abs_end]
    return np.array([safe_mean(sub[c]) for c in echo_features],dtype=float),len(sub)
# target anchor windows compared to washout2 first windows + baseline2
refs=[]
for ref_name,cond,start,end in [('WASHOUT_2_first30','WASHOUT_2',0,30),('WASHOUT_2_first45','WASHOUT_2',0,45),('WASHOUT_2_first60','WASHOUT_2',0,60),('BASELINE_2_first30','BASELINE_2_REFLECTION',0,30),('BASELINE_2_all','BASELINE_2_REFLECTION',0,999)]:
    v,n=vec_for(cond,start,end); refs.append((ref_name,v,n))
echo=[]
for _,a in ann.iterrows():
    anchor=a['anchor_id']; label=a.get('scene_label','')
    start=float(a['peak_search_start_sec']); end=float(a['peak_search_end_sec'])
    av,an=vec_for('TARGET_1',start,end)
    for ref_name,rv,rn in refs:
        echo.append({'anchor_id':anchor,'scene_label':label,'target_window_start':start,'target_window_end':end,'reference_window':ref_name,'target_rows':an,'reference_rows':rn,'cosine_similarity':cosine(av,rv),'euclidean_distance':float(np.linalg.norm(np.nan_to_num(av)-np.nan_to_num(rv))),'target_vector_json':json.dumps([float(x) if np.isfinite(x) else None for x in av]),'reference_vector_json':json.dumps([float(x) if np.isfinite(x) else None for x in rv])})
echo=pd.DataFrame(echo)
echo.to_csv(OUT/'tables/eet_endogenous_echo_tracking.csv',index=False)

# ---------- overlays ----------
ov=[]
for _,r in e[e['BIT_pass_praycg_strict']].iterrows():
    ov.append({'start_sec':r.condition_offset_sec,'end_sec':r.condition_offset_sec+2,'label':f"BIT_PASS {r.anchor_metric} K={r.K_HT_topo_local:.2f}",'category':'bit','source':'NIP_BIT_v0.1'})
for _,r in iaq.iterrows():
    if bool(r.get('Target_greater_Override')):
        annr=ann[ann.anchor_id==r.anchor_id]
        if len(annr):
            t=float(annr.iloc[0].rendered_time_sec_estimate)
            ov.append({'start_sec':max(0,t-3),'end_sec':t+3,'label':f"IAQ+ {r.anchor_id} IAQ={r.IAQ_Target_vs_Override:.2f}",'category':'iaq','source':'NIP_IAQ_v0.1'})
# CET overlay for cue rhythm could be too many; only summary markers with best tracking in override
pd.DataFrame(ov).to_csv(OUT/'tables/nip_cet_eet_visual_overlay.csv', index=False)

# ---------- interpretation ----------
summary={
    'schema':'PRAYCG_Contact_Run1_NIP_CET_EET_v1_0',
    'nip':{
        'target_mean_NIP_density':safe_mean(f.loc[f.condition=='TARGET_1','NIP_density']),
        'control_mean_NIP_density':safe_mean(f.loc[f.condition=='CONTROL_1','NIP_density']),
        'override_mean_NIP_density':safe_mean(f.loc[f.condition=='CONTEXTUAL_OVERRIDE_1','NIP_density']),
    },
    'bit':{
        'strict_BIT_pass_count':int(e['BIT_pass_praycg_strict'].sum()),
        'event_only_BIT_pass_count':int(e['BIT_pass_event_only'].sum()),
        'target_strict_BIT_events':e[e['BIT_pass_praycg_strict']][['condition_offset_sec','anchor_metric','K_HT_topo_local','theta_delta_10_30','mred_quadrant']].to_dict('records')
    },
    'cii_iaq':{
        'anchors':iaq.to_dict('records'),
        'target_greater_control_count':int(iaq['Target_greater_Control'].sum()) if len(iaq) else 0,
        'target_greater_override_count':int(iaq['Target_greater_Override'].sum()) if len(iaq) else 0,
    },
    'cet':{
        'cue_tracking_summary_rows':len(cet),
        'cue_frequency_hz':1/3,
        'visualizer_video_proxy_used':bool(visual_ts is not None and len(visual_ts)>0),
        'limitations':'Raw source stimulus videos/audio were not available in container; CET uses cue-schedule regressors and, for Target visual rhythm only, the top stimulus region of the uploaded visualizer MP4 as a proxy.'
    },
    'eet':{
        'rows':len(echo),
        'interpretation':'State-vector echo only; not proof of replay or memory. Highest similarities indicate after-state resemblance to target anchor feature geometry.'
    },
    'boundary':'NIP/BIT/CII/IAQ/CET/EET are macroscopic PRAYCG proxies. They do not measure dopamine, oxytocin, microtubules, biophotons, OSM biology, or consciousness.'
}
with open(OUT/'tables/nip_cet_eet_interpretation.json','w',encoding='utf-8') as fp: json.dump(summary,fp,indent=2)

# ---------- create simple figures ----------
import matplotlib.pyplot as plt
plt.figure(figsize=(12,4))
for cond in conds:
    sub=f[f.condition==cond]
    plt.plot(sub['condition_offset_sec'], sub['NIP_density'].rolling(5,min_periods=1).mean(), label=cond)
plt.xlabel('Condition offset (s)'); plt.ylabel('NIP density (5s rolling)'); plt.title('Contact Run 1 - Narrative Immersion Proxy density')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'figures/nip_density_by_condition.png', dpi=160); plt.close()

plt.figure(figsize=(10,4))
plotdf=iaq.melt(id_vars=['anchor_id','scene_label'], value_vars=['CII_Target','CII_Control','CII_Override'], var_name='condition', value_name='CII')
# bar plot by anchor
anchors=iaq['anchor_id'].tolist(); x=np.arange(len(anchors)); width=0.25
for k,col in enumerate(['CII_Control','CII_Target','CII_Override']):
    plt.bar(x+(k-1)*width, iaq[col], width, label=col.replace('CII_',''))
plt.xticks(x, [a.replace('CONTACT_','').replace('_','\n')[:24] for a in anchors], fontsize=7)
plt.ylabel('CII mean NIP density'); plt.title('CII by conceptual Contact anchor'); plt.legend(); plt.tight_layout(); plt.savefig(OUT/'figures/cii_by_anchor.png',dpi=160); plt.close()

# Copy inputs summary references
for src in [FEATURE, EVENT, ANNOT, CUE, MANIFEST]:
    shutil.copy2(src, OUT/'tables'/('source_'+Path(src).name))

print(json.dumps(summary, indent=2)[:4000])
