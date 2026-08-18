import os, json, math, shutil, zipfile, textwrap, subprocess
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path('/mnt/data/PRAYCG_NUPI_Arrival_Contact_Field_Analysis_v1_0')
(OUT/'tables').mkdir(parents=True, exist_ok=True)
(OUT/'report').mkdir(parents=True, exist_ok=True)
(OUT/'scripts').mkdir(parents=True, exist_ok=True)

def clip01(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return np.nan
    return max(0.0, min(1.0, float(x)))

def safe_mean(vals):
    vals=[v for v in vals if v is not None and not pd.isna(v)]
    return float(np.mean(vals)) if vals else np.nan

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f: return json.load(f)

# Paths
P = {
    'arrival_tables': Path('/mnt/data/PRAYCG_Arrival_Run1_LatestModules_Rerun_v1_0/tables'),
    'arrival_self': Path('/mnt/data/ArrivalEndScene_Run1_Master_Comprehensive_Synthesis_v1_1_0/tables/arrival_self_report_ratings.csv'),
    'contact_nip': Path('/mnt/data/PRAYCG_Contact_Run1_NIP_CET_EET_Analysis_v1_0/tables'),
    'contact_b2': Path('/mnt/data/PRAYCG_Contact_Run1_Baseline2_ThermoTheft_DeepDive_v1_0/tables'),
    'contact_itp': Path('/mnt/data/PRAYCG_Contact_Run1_MRED_ITP_Analysis_v1_0/tables'),
    'contact_self': Path('/mnt/data/PRAYCG_Contact_Run1_Analysis_v1_0/tables/final_master_subjective_report.csv'),
    'field_full': Path('/mnt/data/PRAYCG_FieldOfDreams_Run1_MasterComprehensive_FULL_v1_1/tables'),
    'field_b2': Path('/mnt/data/PRAYCG_FieldOfDreams_Run1_MasterSuite_v1_0/tables/field_baseline1_vs_baseline2_summary.csv'),
    'field_final': Path('/mnt/data/PRAYCG_v2_0_hoyt_banks_s0007_field_of_dreams2_20260818_060321_events_final_master_report(1).json'),
    'field_target': Path('/mnt/data/PRAYCG_v2_0_hoyt_banks_s0007_field_of_dreams2_20260818_060321_events_TARGET_1_AFTER_WASHOUT_2_core_report(1).json'),
}

def summarize_cii(run):
    if run == 'Arrival':
        df = pd.read_csv(P['arrival_tables']/ 'arrival_cii_anchor_integrals.csv')
        res = []
        for _,r in df.iterrows():
            res.append(dict(run=run, anchor_id=r.anchor_id, label=r.label, condition='TARGET', target_time_sec=r.center_sec,
                            target_CII=r.target_CII, control_CII=r.control_CII, override_CII=r.override_CII,
                            target_MR=r.target_MR, target_ENC=r.target_ENC, target_artifact=r.target_artifact,
                            target_taskgamma=r.target_task_gamma, target_specific_CII=r.target_CII-max(r.control_CII, r.override_CII)))
        return pd.DataFrame(res)
    if run == 'Contact':
        df = pd.read_csv(P['contact_nip']/ 'cii_anchor_integrals.csv')
        rows=[]
        for aid,g in df.groupby('anchor_id'):
            def one(cond, col):
                s = g.loc[g.condition.eq(cond), col]
                return float(s.iloc[0]) if len(s) else np.nan
            label = g['scene_label'].iloc[0]
            tc = one('TARGET_1','NIP_density_mean_CII'); cc=one('CONTROL_1','NIP_density_mean_CII'); oc=one('CONTEXTUAL_OVERRIDE_1','NIP_density_mean_CII')
            rows.append(dict(run=run,anchor_id=aid,label=label,condition='TARGET',target_time_sec=float(g.loc[g.condition.eq('TARGET_1'),'window_start_sec'].iloc[0]) if any(g.condition.eq('TARGET_1')) else np.nan,
                             target_CII=tc,control_CII=cc,override_CII=oc,target_MR=one('TARGET_1','A_sem_mean'),target_ENC=one('TARGET_1','R_int_mean'),target_artifact=one('TARGET_1','artifact_mean'),target_taskgamma=np.nan,target_specific_CII=tc-max(cc,oc)))
        return pd.DataFrame(rows)
    if run == 'Field':
        df = pd.read_csv(P['field_full']/ 'field_cii_anchor_integrals.csv')
        rows=[]
        for aid,g in df.groupby('anchor_id'):
            def one(cond, col):
                s = g.loc[g.condition.eq(cond), col]
                return float(s.iloc[0]) if len(s) else np.nan
            tc=one('TARGET','CII'); cc=one('CONTROL','CII'); oc=one('OVERRIDE','CII')
            rows.append(dict(run=run,anchor_id=aid,label=aid,condition='TARGET',target_time_sec=one('TARGET','anchor_time_sec'),
                             target_CII=tc,control_CII=cc,override_CII=oc,target_MR=one('TARGET','MR'),target_ENC=one('TARGET','ENC'),target_artifact=one('TARGET','artifact'),target_taskgamma=np.nan,target_specific_CII=tc-max(cc,oc)))
        return pd.DataFrame(rows)

def summarize_itp(run):
    if run == 'Arrival':
        d = pd.read_csv(P['arrival_tables']/ 'arrival_mred_itp_anchor_summary.csv')
        return d.rename(columns={'C_strike':'complexity_strike','C_settle':'complexity_settle','complexity_settlement_index':'CSI'})[['anchor_id','complexity_strike','complexity_settle','CSI','ACG_feature_proxy_flag','OCU_proxy_flag']]
    if run == 'Contact':
        d = pd.read_csv(P['contact_itp']/ 'mred_itp_anchor_summary.csv')
        d = d[d.condition.eq('TARGET_1')].copy()
        d = d.rename(columns={'delta_C_strike_peak_minus_pre':'complexity_strike','delta_C_settle_post_minus_peak':'complexity_settle','CSI_complexity_settlement_index':'CSI','ACG_candidate':'ACG_feature_proxy_flag','OCU_candidate':'OCU_proxy_flag'})
        return d[['anchor_id','complexity_strike','complexity_settle','CSI','ACG_feature_proxy_flag','OCU_proxy_flag']]
    if run == 'Field':
        d = pd.read_csv(P['field_full']/ 'field_mred_itp_anchor_summary.csv')
        d = d[d.condition.eq('TARGET_1')].copy()
        d = d.rename(columns={'C_strike':'complexity_strike','C_settle':'complexity_settle','ACG_candidate':'ACG_feature_proxy_flag','OCU_candidate':'OCU_proxy_flag'})
        d['CSI']=np.nan
        return d[['anchor_id','complexity_strike','complexity_settle','CSI','ACG_feature_proxy_flag','OCU_proxy_flag']]

def summarize_eet_anchor(run):
    if run == 'Arrival':
        d = pd.read_csv(P['arrival_tables']/ 'arrival_eet_endogenous_echo_tracking.csv')
        rows=[]
        for aid,g in d.groupby('anchor_id'):
            after = g[g.comparison_window.astype(str).str.contains('WASHOUT_2|WASHOUT_3', case=False, regex=True)]
            rows.append(dict(anchor_id=aid, afterstate_echo_max=after.cosine_similarity.max() if len(after) else np.nan, baseline2_echo_max=np.nan))
        return pd.DataFrame(rows)
    if run == 'Contact':
        d = pd.read_csv(P['contact_nip']/ 'eet_endogenous_echo_tracking.csv')
        rows=[]
        for aid,g in d.groupby('anchor_id'):
            after=g[g.reference_window.astype(str).str.contains('WASHOUT_2', case=False)]
            b2=g[g.reference_window.astype(str).str.contains('BASELINE_2', case=False)]
            rows.append(dict(anchor_id=aid, afterstate_echo_max=after.cosine_similarity.max() if len(after) else np.nan, baseline2_echo_max=b2.cosine_similarity.max() if len(b2) else np.nan))
        return pd.DataFrame(rows)
    if run == 'Field':
        d = pd.read_csv(P['field_full']/ 'field_eet_endogenous_echo_tracking.csv')
        rows=[]
        for aid,g in d.groupby('anchor_id'):
            after=g[g.comparison.astype(str).str.contains('WASHOUT_2', case=False)]
            b2=g[g.comparison.astype(str).str.contains('BASELINE2', case=False)]
            rows.append(dict(anchor_id=aid, afterstate_echo_max=after.cosine_similarity_state_vector.max() if len(after) else np.nan, baseline2_echo_max=b2.cosine_similarity_state_vector.max() if len(b2) else np.nan))
        return pd.DataFrame(rows)

def b2_scores(run):
    vals = {}
    if run == 'Arrival':
        return dict(b2_available=False,b2_regulation_score=np.nan,b2_semantic_echo_score=np.nan,b2_strain_score=np.nan,b2_raw={})
    if run == 'Contact':
        feat=pd.read_csv(P['contact_b2']/ 'baseline1_vs_baseline2_feature_summary.csv')
        polar=pd.read_csv(P['contact_b2']/ 'baseline1_vs_baseline2_polar_respiration_summary.csv')
        for _,r in feat.iterrows(): vals[str(r.metric)]=float(r.delta_B2_minus_B1)
        for _,r in polar.iterrows(): vals[str(r.metric)]=float(r.delta_B2_minus_B1)
    if run == 'Field':
        df=pd.read_csv(P['field_b2'])
        for _,r in df.iterrows(): vals[str(r.metric)]=float(r.delta_b2_minus_b1)
    def v(*names):
        for n in names:
            if n in vals: return vals[n]
        return np.nan
    hr=v('hr_mean_bpm'); rm=v('rmssd_ms'); sd=v('sdnn_ms'); pnn=v('pNN50','pnn50')
    respstd=v('Resp std','resp_std'); task=v('TaskGamma','taskgamma_z'); art=v('ArtifactScore','artifact_score')
    alpha=v('PosteriorAlpha','alpha_posterior_z'); tsp=v('TSP','tsp_z'); nip=v('NIP_density'); nast=v('NAST_NAS','nast_nas_z')
    reg=[]; sem=[]; strain=[]
    if not pd.isna(hr): reg.append(clip01(-hr/10)); strain.append(clip01(hr/10))
    if not pd.isna(rm): reg.append(clip01(rm/50)); strain.append(clip01(-rm/50))
    if not pd.isna(sd): reg.append(clip01(sd/50))
    if not pd.isna(pnn): reg.append(clip01(pnn/0.15))
    if not pd.isna(respstd): reg.append(clip01(-respstd/1.5)); strain.append(clip01(respstd/1.5))
    if not pd.isna(task): reg.append(clip01(-task/1.5)); strain.append(clip01(task/1.5))
    if not pd.isna(art): reg.append(clip01(-art/1.5)); strain.append(clip01(art/1.5))
    # semantic echo is not automatically recovery; it is post-state semantic persistence.
    if not pd.isna(tsp): sem.append(clip01(tsp/1.0))
    if not pd.isna(nip): sem.append(clip01(nip/0.15))
    if not pd.isna(nast): sem.append(clip01(nast/1.5))
    if not pd.isna(alpha): sem.append(clip01(alpha/0.7))
    return dict(b2_available=True,b2_regulation_score=safe_mean(reg),b2_semantic_echo_score=safe_mean(sem),b2_strain_score=safe_mean(strain),b2_raw=vals)

def subjective_scores(run):
    if run == 'Arrival':
        df=pd.read_csv(P['arrival_self'])
        t=df[df.phase.eq('TARGET_1_AFTER_WASHOUT_2')].iloc[0]
        return dict(self_target_meaning=t.Meaning/9,self_target_absorption=t.Absorption/9,self_target_afterglow=t.EmotionalAfterglow/9,self_target_washout=t.StoryActiveWashout/9,self_override_reduced=np.nan,self_story_breakthrough=np.nan,self_familiarity=np.nan,self_new_meaning=np.nan)
    if run == 'Contact':
        df=pd.read_csv(P['contact_self'])
        t=df[df.branch.eq('TARGET')].iloc[0]; o=df[df.branch.eq('OVERRIDE')].iloc[0]
        return dict(self_target_meaning=t.Meaning/9,self_target_absorption=t.Absorption/9,self_target_afterglow=t.EmotionalAfterglow/9,self_target_washout=t.StoryActiveWashout/9,self_override_reduced=(t.Absorption-o.Absorption)/9,self_story_breakthrough=o.Meaning/9,self_familiarity=np.nan,self_new_meaning=np.nan)
    if run == 'Field':
        final=load_json(P['field_final']); target=load_json(P['field_target'])
        return dict(self_target_meaning=target['ratings']['Meaning']/9,self_target_absorption=target['ratings']['Absorption']/9,self_target_afterglow=target['ratings']['EmotionalAfterglow']/9,self_target_washout=target['ratings']['StoryActiveWashout']/9,self_override_reduced=final['ratings']['OverrideReducedReception']/9,self_story_breakthrough=final['ratings']['StoryBrokeThroughOverride']/9,self_familiarity=final['ratings']['Familiarity']/9,self_new_meaning=final['ratings']['NewMeaningToday']/9)

def tti(run):
    if run == 'Arrival':
        df=pd.read_csv(P['arrival_tables']/ 'arrival_tti_global_summary.csv')
        return float(df.TTI.iloc[0])
    if run == 'Contact':
        df=pd.read_csv(P['contact_b2']/ 'thermodynamic_theft_composite_index.csv')
        s=df.loc[df.component.eq('thermodynamic_theft_index_exploratory'),'value']
        return float(s.iloc[0]) if len(s) else np.nan
    if run == 'Field':
        df=pd.read_csv(P['field_full']/ 'field_tti_global_summary.csv')
        return float(df.TTI_global.iloc[0])

def strict_pass_count(run):
    if run == 'Arrival':
        df=pd.read_csv(P['arrival_tables']/ 'arrival_bit_event_table.csv')
        col='BIT_strict_pass' if 'BIT_strict_pass' in df.columns else None
        return int(df[col].sum()) if col else 0, len(df)
    if run == 'Contact':
        df=pd.read_csv(P['contact_nip']/ 'bit_event_table.csv')
        col='BIT_pass_praycg_strict' if 'BIT_pass_praycg_strict' in df.columns else ('BIT_pass_event_only' if 'BIT_pass_event_only' in df.columns else None)
        return int(df[col].sum()) if col else 0, len(df)
    if run == 'Field':
        dt=pd.read_csv(P['field_full']/ 'field_amred_anchor_endpoint_table.csv')
        if 'sensitivity' in dt.columns:
            dt=dt[dt['sensitivity'].astype(str).eq('runner_registered_time')]
        col='A_MRED_pass' if 'A_MRED_pass' in dt.columns else ('AMRED_pass' if 'AMRED_pass' in dt.columns else 'amred_pass')
        return int(dt[col].sum()) if col in dt.columns else 0, len(dt)

# Build anchors and run rows
anchor_rows=[]; raw_rows=[]; comp_rows=[]
for run in ['Arrival','Contact','Field']:
    cii=summarize_cii(run)
    itp=summarize_itp(run)
    eet=summarize_eet_anchor(run)
    anchors=cii.merge(itp,on='anchor_id',how='left').merge(eet,on='anchor_id',how='left')
    # anchor-level rough scores
    anchors['load_proxy'] = anchors.apply(lambda r: safe_mean([
        clip01(max(r.target_CII,0)/1.0), clip01(max(r.target_MR,0)/1.2), clip01(max(r.target_ENC,0)/1.5), clip01(max(r.complexity_strike if not pd.isna(r.complexity_strike) else 0,0)/0.08)
    ]), axis=1)
    anchors['recovery_proxy'] = anchors.apply(lambda r: safe_mean([
        clip01((r.baseline2_echo_max+1)/2) if not pd.isna(r.baseline2_echo_max) else np.nan,
        clip01((r.afterstate_echo_max+1)/2) if not pd.isna(r.afterstate_echo_max) else np.nan,
        clip01(max(-(r.complexity_settle if not pd.isna(r.complexity_settle) else 0),0)/0.05),
    ]), axis=1)
    anchors['anchor_NUPI_proxy'] = anchors['recovery_proxy'] - anchors['load_proxy']
    anchors['anchor_polarity_label'] = pd.cut(anchors['anchor_NUPI_proxy'], bins=[-np.inf,-0.25,0.25,np.inf], labels=['ACCOMMODATIVE_LOAD_TILT','MIXED_NEUTRAL_TILT','RESOLUTIVE_RECOVERY_TILT'])
    anchor_rows.append(anchors)
    # run raw aggregation
    b2=b2_scores(run); subj=subjective_scores(run)
    pass_count,total_count = strict_pass_count(run)
    raw={
        'run': run,
        'n_anchors': len(anchors),
        'strict_primary_pass_count': pass_count,
        'strict_primary_anchor_count': total_count,
        'target_CII_mean': anchors.target_CII.mean(),
        'target_CII_max': anchors.target_CII.max(),
        'target_specific_CII_mean': anchors.target_specific_CII.mean(),
        'target_MR_mean': anchors.target_MR.mean(),
        'target_ENC_mean': anchors.target_ENC.mean(),
        'target_artifact_mean': anchors.target_artifact.mean(),
        'complexity_strike_pos_mean': np.maximum(anchors.complexity_strike.fillna(0),0).mean(),
        'complexity_settle_mean': anchors.complexity_settle.mean(),
        'complexity_CSI_max': anchors.CSI.max(),
        'ACG_rate': anchors.ACG_feature_proxy_flag.fillna(False).mean(),
        'OCU_rate': anchors.OCU_proxy_flag.fillna(False).mean(),
        'eet_afterstate_max': anchors.afterstate_echo_max.max(),
        'eet_afterstate_mean': anchors.afterstate_echo_max.mean(),
        'eet_baseline2_max': anchors.baseline2_echo_max.max(),
        'eet_baseline2_mean': anchors.baseline2_echo_max.mean(),
        'tti_global': tti(run),
        **{k:v for k,v in b2.items() if k!='b2_raw'},
        **subj
    }
    raw['b2_raw_json']=json.dumps(b2.get('b2_raw',{}))
    raw_rows.append(raw)

raw=pd.DataFrame(raw_rows)
anchor_df=pd.concat(anchor_rows, ignore_index=True)
# Compute components and NUPI
score_rows=[]
for _,r in raw.iterrows():
    semantic_intensity=safe_mean([clip01(r.target_CII_mean/0.9),clip01(r.target_CII_max/1.6),clip01(max(r.target_MR_mean,0)/1.2),clip01(max(r.target_ENC_mean,0)/1.5)])
    target_specificity=clip01(max(r.target_specific_CII_mean,0)/0.8)
    complexity_perturb=safe_mean([clip01(max(r.complexity_strike_pos_mean,0)/0.08),clip01(max(-r.complexity_settle_mean,0)/0.05),clip01(max(r.complexity_CSI_max if not pd.isna(r.complexity_CSI_max) else 0,0)/1.5)])
    tti_score=clip01(max(r.tti_global,0)/0.75)
    # A strict pass count makes load more credible, not mechanically positive alone
    primary_pass_score=clip01(r.strict_primary_pass_count/max(r.strict_primary_anchor_count,1)*3)
    ALI=safe_mean([semantic_intensity,target_specificity,complexity_perturb,tti_score,primary_pass_score])
    echo=safe_mean([clip01((r.eet_baseline2_max+1)/2) if not pd.isna(r.eet_baseline2_max) else np.nan, clip01((r.eet_afterstate_max+1)/2) if not pd.isna(r.eet_afterstate_max) else np.nan])
    self_echo=safe_mean([r.self_target_afterglow,r.self_target_washout,r.self_new_meaning if not pd.isna(r.self_new_meaning) else np.nan])
    # RDI requires a final/baseline2 physiology layer. If unavailable, calculate proxy but mark ungraded.
    RDI=safe_mean([r.b2_regulation_score,r.b2_semantic_echo_score,echo,self_echo]) if bool(r.b2_available) else np.nan
    RDI_proxy=safe_mean([echo,self_echo])
    NUPI=RDI-ALI if not pd.isna(RDI) else np.nan
    # Classification
    if not bool(r.b2_available):
        polarity='POLARITY_UNRESOLVED_NO_BASELINE2'
    elif ALI>=0.58 and RDI>=0.60:
        polarity='HIGH_LOAD_WITH_RECOVERY'
    elif RDI>=0.60 and ALI<0.58:
        polarity='RESOLUTIVE_RECOVERY'
    elif ALI>=0.58 and RDI<0.45:
        polarity='ACCOMMODATIVE_LOAD'
    elif semantic_intensity>=0.4 and RDI<0.45:
        polarity='RECOGNITION_WITH_WEAK_RECOVERY'
    else:
        polarity='MIXED_OR_UNCERTAIN'
    score_rows.append(dict(run=r.run, semantic_intensity=semantic_intensity, target_specificity=target_specificity, complexity_perturbation=complexity_perturb, tti_score=tti_score, primary_pass_score=primary_pass_score, ALI_accommodative_load=ALI, b2_regulation=r.b2_regulation_score, b2_semantic_echo=r.b2_semantic_echo_score, eet_echo=echo, self_report_echo=self_echo, RDI_resolutive_recovery=RDI, RDI_afterstate_proxy=RDI_proxy, NUPI=NUPI, polarity_class=polarity))
score=pd.DataFrame(score_rows)
# Merge raw+score for summary
summary=raw.merge(score,on='run')
# write
raw.to_csv(OUT/'tables/nupi_raw_component_inputs.csv', index=False)
score.to_csv(OUT/'tables/nupi_run_summary.csv', index=False)
summary.to_csv(OUT/'tables/nupi_run_summary_with_inputs.csv', index=False)
anchor_df.to_csv(OUT/'tables/nupi_anchor_polarity_table.csv', index=False)
# Visual overlay
vis=[]
for _,r in anchor_df.iterrows():
    vis.append(dict(run=r.run, time_sec=r.target_time_sec, end_sec=(r.target_time_sec+30 if not pd.isna(r.target_time_sec) else np.nan), label=f"NUPI {r.anchor_polarity_label}", category='nupi', anchor_id=r.anchor_id, score=r.anchor_NUPI_proxy, detail=f"load={r.load_proxy:.3f}; recovery={r.recovery_proxy:.3f}"))
pd.DataFrame(vis).to_csv(OUT/'tables/nupi_visual_overlay.csv', index=False)
# interpretation json
interpret={
 'module':'NUPI_v0.1 Narrative Update Polarity Index',
 'claim_boundary':'Proxy-level classification of narrative-update polarity. Does not measure literal heat, ATP, glucose, or thermodynamic energy. Requires replication and stronger autonomic/EOG controls.',
 'formula_summary':{
   'ALI':'Accommodative Load Index = mean(semantic intensity, Target specificity, complexity perturbation, TTI, primary endpoint pass score).',
   'RDI':'Resolutive Recovery Index = mean(Baseline2 regulation, Baseline2 semantic echo, EET afterstate echo, self-report echo), only graded when Baseline2/final reflection is available.',
   'NUPI':'RDI - ALI. Positive values imply recovery tilt; negative values imply load tilt. If no Baseline2/final reflection exists, NUPI is not graded.'},
 'classification': score.to_dict(orient='records')
}
with open(OUT/'tables/nupi_interpretation.json','w',encoding='utf-8') as f: json.dump(interpret,f,indent=2)
print(score.to_string(index=False))
