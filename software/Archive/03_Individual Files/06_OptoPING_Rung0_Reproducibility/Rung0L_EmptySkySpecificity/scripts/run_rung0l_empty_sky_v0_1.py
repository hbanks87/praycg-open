from __future__ import annotations
import json, math, hashlib, shutil, zipfile, textwrap
from pathlib import Path
from dataclasses import dataclass
import numpy as np
import pandas as pd

SPEC = {
    "schema": "OSM_OptoPING_Rung0L_EmptySkySpecificity_v0_1",
    "purpose": "Empty-sky specificity: reciprocal Opto-PING must stay quiet on loop-absent Standard-PING/null synthetic data.",
    "seed_policy": {"seed_start": 920001, "n_trials_per_generator": 60},
    "generators": ["full_reciprocal_positive_control", "standard_ping_null", "replay_only_null", "sensory_drive_only_null", "generic_hidden_oscillator_null", "colored_noise_null"],
    "perturbation_conditions": ["doublet_EY", "orthogonal_trap", "counterphase", "lagged_E_to_Y", "recovery_probe", "lagged_Y_to_E"],
    "samples_per_condition": 32,
    "models": ["full_reciprocal", "eta_only", "zeta_only", "null_no_coupling", "replay_only_basis", "standard_ping", "generic_hidden_oscillator", "sensory_drive_only"],
    "pass_criteria": {
        "positive_control_full_model_cv_win_rate_min": 0.80,
        "positive_control_K_within_15_rate_min": 0.80,
        "null_full_model_cv_win_rate_max": 0.20,
        "null_false_K_lock_rate_max": 0.10,
        "null_non_full_cv_win_rate_min": 0.80,
        "null_median_K_hat_max": 0.30
    },
    "boundary": "Synthetic specificity only; no biological, PR-AYC-G, human EEG, or OSM mechanism claim."
}
SPEC_SHA256=hashlib.sha256(json.dumps(SPEC,sort_keys=True,indent=2).encode()).hexdigest()
CONDITIONS=SPEC["perturbation_conditions"]; MODELS=SPEC["models"]; N_PER=SPEC["samples_per_condition"]
COND_PARAMS={
    "doublet_EY": dict(u=1.00, phase=0.0, rec=0.85, ydrive=0.85, lag=0.20, ping=0.80),
    "orthogonal_trap": dict(u=0.65, phase=1.1, rec=-0.75, ydrive=0.95, lag=-0.50, ping=0.55),
    "counterphase": dict(u=0.85, phase=2.4, rec=-0.95, ydrive=-0.90, lag=0.40, ping=0.75),
    "lagged_E_to_Y": dict(u=0.75, phase=0.7, rec=0.35, ydrive=1.15, lag=0.95, ping=0.60),
    "recovery_probe": dict(u=0.45, phase=1.7, rec=0.15, ydrive=0.35, lag=0.10, ping=0.30),
    "lagged_Y_to_E": dict(u=0.80, phase=2.9, rec=1.05, ydrive=0.55, lag=-0.95, ping=0.65),
}

def z(x):
    x=np.asarray(x,float); s=x.std()
    return (x-x.mean())/(s if s>1e-9 else 1.0)

def ar1(rng,n,rho=0.9,scale=1):
    e=rng.normal(0,scale,n); x=np.zeros(n)
    for i in range(1,n): x[i]=rho*x[i-1]+e[i]
    return z(x)

def lag(x,k=1):
    return np.r_[np.repeat(x[0],k), x[:-k]]

def basis(cond,n,rng):
    p=COND_PARAMS[cond]; t=np.linspace(0,1,n,endpoint=False)
    u=p['u']*(np.sin(2*np.pi*(1.0+0.18*p['ping'])*t+p['phase'])+0.35*np.sin(2*np.pi*3*t+0.5*p['phase']))
    ping=p['ping']*(np.sin(2*np.pi*6*t+p['phase'])-0.45*np.sin(2*np.pi*6*t+p['phase']+np.pi/4))
    replay=p['rec']*np.exp(-2.2*t)*np.cos(2*np.pi*2*t+p['phase'])
    ydrive=p['ydrive']*(np.sin(2*np.pi*1.5*t+p['phase']+0.8)+0.2*np.cos(2*np.pi*4*t))
    generic=np.sin(2*np.pi*2.5*t+p['phase']*0.7)+0.4*np.cos(2*np.pi*5*t+0.3)
    orth=p['lag']*np.sin(2*np.pi*(0.7+0.05*p['u'])*t+p['phase']+np.pi/2)
    return {"condition": np.array([cond]*n), "u":z(u), "u_lag":z(lag(u,2)), "ping":z(ping), "ping_lag":z(lag(ping,1)), "replay":z(replay), "ydrive":z(ydrive), "generic":z(generic), "orth":z(orth)}

def generate(generator,seed):
    rng=np.random.default_rng(seed); rows=[]
    for cond in CONDITIONS:
        b=basis(cond,N_PER,rng); n=N_PER
        ne=rng.normal(0,0.28,n); ny=rng.normal(0,0.28,n); nv=rng.normal(0,0.28,n)
        u=b['u']; ping=b['ping']; replay=b['replay']; ydrive=b['ydrive']; generic=b['generic']; orth=b['orth']
        if generator=="full_reciprocal_positive_control":
            Y_lat=0.70*ydrive+0.25*b['u_lag']+0.25*orth+rng.normal(0,0.18,n)
            E=0.55*u+0.35*ping+0.90*lag(Y_lat,1)+0.18*replay+ne
            Y=0.45*ydrive+0.85*lag(E,1)+0.20*generic+ny
            V=np.gradient(Y)+0.50*lag(E,2)-0.15*replay+nv; kt=1.0
        elif generator=="standard_ping_null":
            E=0.90*u+0.80*ping-0.35*b['ping_lag']+0.15*replay+ne
            Y=0.15*u+0.08*generic+rng.normal(0,0.55,n)
            V=np.gradient(Y)+rng.normal(0,0.55,n); kt=0.0
        elif generator=="replay_only_null":
            E=0.35*u+1.05*replay+0.25*lag(replay,1)+ne
            common=0.25*replay+0.20*u
            Y=common+rng.normal(0,0.50,n); V=np.gradient(common)+rng.normal(0,0.50,n); kt=0.0
        elif generator=="sensory_drive_only_null":
            E=1.05*u+0.25*ping+ne
            Y=0.85*u+0.20*orth+ny
            V=0.60*np.gradient(u)+0.10*orth+nv; kt=0.0
        elif generator=="generic_hidden_oscillator_null":
            h=generic
            E=0.55*u+0.85*h+0.25*ping+ne
            Y=0.15*u+0.90*h+ny
            V=0.65*np.gradient(h)+0.15*u+nv; kt=0.0
        elif generator=="colored_noise_null":
            drift=np.linspace(-0.5,0.5,n)
            E=0.35*u+0.70*ar1(rng,n,0.93,0.35)+0.20*drift+ne
            Y=0.20*u+0.70*ar1(rng,n,0.91,0.35)-0.10*drift+ny
            V=np.gradient(Y)+0.45*ar1(rng,n,0.88,0.35)+nv; kt=0.0
        else: raise ValueError(generator)
        for i in range(n):
            rows.append({"condition":cond,"u":u[i],"u_lag":b['u_lag'][i],"ping":ping[i],"ping_lag":b['ping_lag'][i],"replay":replay[i],"ydrive":ydrive[i],"generic":generic[i],"orth":orth[i],"E":z(E)[i],"Yproxy":z(Y)[i],"Vproxy":z(V)[i],"K_true_scaled":kt})
    df=pd.DataFrame(rows)
    # lags within condition
    for col in ['E','Yproxy','Vproxy']:
        df[col+'_l1']=0.0
        for cond in CONDITIONS:
            m=df['condition']==cond; df.loc[m,col+'_l1']=lag(df.loc[m,col].values,1)
    return df

def X_for(df,model):
    def cols(names): return [df[c].values for c in names]
    base=[np.ones(len(df))]
    if model=="full_reciprocal":
        arr=cols(['u','u_lag','ping','replay','ydrive','orth','generic','E_l1','Yproxy_l1','Vproxy_l1']); base+=arr+[df['Yproxy_l1'].values*df['ydrive'].values, df['E_l1'].values*df['u_lag'].values, df['E_l1'].values*df['Yproxy_l1'].values]
    elif model=="eta_only": base+=cols(['u','ping','replay','ydrive','Yproxy_l1','Vproxy_l1'])+[df['Yproxy_l1'].values*df['ydrive'].values]
    elif model=="zeta_only": base+=cols(['u','u_lag','ping','replay','ydrive','E_l1'])+[df['E_l1'].values*df['u_lag'].values]
    elif model=="null_no_coupling": base+=cols(['u'])
    elif model=="replay_only_basis": base+=cols(['u','replay','E_l1'])+[df['replay'].values*df['u'].values]
    elif model=="standard_ping": base+=cols(['u','u_lag','ping','ping_lag','E_l1'])
    elif model=="generic_hidden_oscillator": base+=cols(['u','generic','orth','E_l1'])+[df['generic'].values*df['orth'].values]
    elif model=="sensory_drive_only": base+=cols(['u','u_lag','orth','ping'])+[np.gradient(df['u'].values)]
    else: raise ValueError(model)
    return np.column_stack(base)

def fit_loss(X,Y,train_mask,test_mask,alpha=0.2):
    Xtr=X[train_mask]; Ytr=Y[train_mask]; Xte=X[test_mask]; Yte=Y[test_mask]
    mu=Xtr.mean(0); sd=Xtr.std(0); mu[0]=0; sd[0]=1; sd[sd<1e-9]=1
    Xt=(Xtr-mu)/sd; Xe=(Xte-mu)/sd
    P=Xt.shape[1]; pen=np.eye(P)*alpha; pen[0,0]=0
    B=np.linalg.solve(Xt.T@Xt+pen, Xt.T@Ytr)
    pred=Xe@B
    return float(np.mean((pred-Yte)**2)+0.0005*(P-1))

def k_est(df):
    controls=np.column_stack([np.ones(len(df)), df[['u','u_lag','ping','replay','generic','orth']].values])
    Xeta=np.column_stack([controls, df['Yproxy_l1'].values, df['Vproxy_l1'].values])
    beta=np.linalg.lstsq(Xeta,df['E'].values,rcond=None)[0]; eta=float(beta[-2])
    Xz=np.column_stack([controls, df['E_l1'].values])
    beta=np.linalg.lstsq(Xz,df['Yproxy'].values,rcond=None)[0]; zeta=float(beta[-1])
    prod=eta*zeta; k=math.sqrt(abs(prod))/0.70 if prod!=0 else 0.0
    return eta,zeta,prod,k

def run(out_dir):
    out_dir=Path(out_dir); tables=out_dir/'tables'; report=out_dir/'report'; lock=out_dir/'locked_protocol'
    for d in [tables,report,lock]: d.mkdir(parents=True,exist_ok=True)
    (lock/'RUNG0L_SPEC_v0_1.json').write_text(json.dumps({**SPEC,'spec_sha256':SPEC_SHA256},indent=2),encoding='utf-8')
    (lock/'RUNG0L_SPEC_SHA256.txt').write_text(SPEC_SHA256+'\n')
    trial_rows=[]; loss_rows=[]; winner_rows=[]
    n=SPEC['seed_policy']['n_trials_per_generator']; start=SPEC['seed_policy']['seed_start']
    for gi,g in enumerate(SPEC['generators']):
        for j in range(n):
            seed=start+gi*10000+j; df=generate(g,seed); Y=df[['E','Yproxy','Vproxy']].values
            Xm={m:X_for(df,m) for m in MODELS}
            fold_winners=[]
            for hold in CONDITIONS:
                test=(df['condition'].values==hold); train=~test
                losses=[]
                for m in MODELS:
                    loss=fit_loss(Xm[m],Y,train,test,alpha=0.5 if m=='full_reciprocal' else 0.2)
                    losses.append((m,loss))
                    loss_rows.append({'generator':g,'trial':j+1,'seed':seed,'fold_condition':hold,'model':m,'loss':loss})
                winner=min(losses,key=lambda x:x[1])
                fold_winners.append(winner[0])
                winner_rows.append({'generator':g,'trial':j+1,'seed':seed,'fold_condition':hold,'winning_model':winner[0],'loss':winner[1]})
            eta,zeta,prod,k=k_est(df)
            full_wins=sum(w=='full_reciprocal' for w in fold_winners)
            row={'generator':g,'trial':j+1,'seed':seed,'K_true_scaled':float(df['K_true_scaled'].iloc[0]),'eta_hat':eta,'zeta_hat':zeta,'eta_zeta_product':prod,'K_hat_scaled':k,'false_K_lock_null':bool(g!='full_reciprocal_positive_control' and k>=0.30),'K_within_15_positive':bool(g=='full_reciprocal_positive_control' and abs(k-1)<=0.15),'K_within_10_positive':bool(g=='full_reciprocal_positive_control' and abs(k-1)<=0.10),'full_cv_wins':full_wins,'full_cv_win_rate':full_wins/len(CONDITIONS),'non_full_cv_win_rate':1-full_wins/len(CONDITIONS),'trial_full_dominates':bool(full_wins>len(CONDITIONS)/2),'trial_non_full_dominates':bool((len(CONDITIONS)-full_wins)>=math.ceil(0.8*len(CONDITIONS))),'cv_winner_counts_json':json.dumps(pd.Series(fold_winners).value_counts().to_dict(),sort_keys=True)}
            trial_rows.append(row)
    trial_df=pd.DataFrame(trial_rows); loss_df=pd.DataFrame(loss_rows); winners_df=pd.DataFrame(winner_rows)
    trial_df.to_csv(tables/'rung0l_trial_results.csv',index=False); loss_df.to_csv(tables/'rung0l_cv_model_losses.csv',index=False); winners_df.to_csv(tables/'rung0l_cv_fold_winners.csv',index=False)
    gen_summary=trial_df.groupby('generator').agg(n_trials=('trial','count'),K_true_scaled=('K_true_scaled','first'),median_K_hat_scaled=('K_hat_scaled','median'),mean_K_hat_scaled=('K_hat_scaled','mean'),K_within_15_positive_rate=('K_within_15_positive','mean'),K_within_10_positive_rate=('K_within_10_positive','mean'),false_K_lock_rate=('false_K_lock_null','mean'),full_cv_win_rate_mean=('full_cv_win_rate','mean'),full_cv_dominance_rate=('trial_full_dominates','mean'),non_full_cv_win_rate_mean=('non_full_cv_win_rate','mean'),non_full_dominance_rate=('trial_non_full_dominates','mean')).reset_index()
    gen_summary.to_csv(tables/'rung0l_generator_summary.csv',index=False)
    win_summary=winners_df.groupby(['generator','winning_model']).size().reset_index(name='wins')
    totals=winners_df.groupby('generator').size().reset_index(name='total_folds')
    win_summary=win_summary.merge(totals,on='generator'); win_summary['win_rate']=win_summary['wins']/win_summary['total_folds']
    win_summary.to_csv(tables/'rung0l_cv_win_summary.csv',index=False)
    null=trial_df[trial_df.generator!='full_reciprocal_positive_control']; pos=trial_df[trial_df.generator=='full_reciprocal_positive_control']; c=SPEC['pass_criteria']
    ps={'schema':'OSM_OptoPING_Rung0L_EmptySkySpecificity_results_v0_1','spec_sha256':SPEC_SHA256,'n_trials_total':int(len(trial_df)),'n_positive_trials':int(len(pos)),'n_null_trials':int(len(null)),'positive_control':{'K_within_15_rate':float(pos.K_within_15_positive.mean()),'K_within_10_rate':float(pos.K_within_10_positive.mean()),'median_K_hat_scaled':float(pos.K_hat_scaled.median()),'full_model_cv_win_rate_mean':float(pos.full_cv_win_rate.mean()),'pass_full_model_cv':bool(pos.full_cv_win_rate.mean()>=c['positive_control_full_model_cv_win_rate_min']),'pass_K_15':bool(pos.K_within_15_positive.mean()>=c['positive_control_K_within_15_rate_min'])},'empty_sky_nulls':{'null_full_model_cv_win_rate_mean':float(null.full_cv_win_rate.mean()),'null_false_K_lock_rate':float(null.false_K_lock_null.mean()),'null_non_full_cv_win_rate_mean':float(null.non_full_cv_win_rate.mean()),'null_median_K_hat_scaled':float(null.K_hat_scaled.median()),'pass_full_model_stays_quiet':bool(null.full_cv_win_rate.mean()<=c['null_full_model_cv_win_rate_max']),'pass_false_K_lock_rate':bool(null.false_K_lock_null.mean()<=c['null_false_K_lock_rate_max']),'pass_non_full_wins':bool(null.non_full_cv_win_rate.mean()>=c['null_non_full_cv_win_rate_min']),'pass_median_K_near_zero':bool(null.K_hat_scaled.median()<=c['null_median_K_hat_max'])},'boundary':SPEC['boundary']}
    ps['overall_status']='PASS_EMPTY_SKY_SPECIFICITY' if all([ps['positive_control']['pass_full_model_cv'],ps['positive_control']['pass_K_15'],ps['empty_sky_nulls']['pass_full_model_stays_quiet'],ps['empty_sky_nulls']['pass_false_K_lock_rate'],ps['empty_sky_nulls']['pass_non_full_wins'],ps['empty_sky_nulls']['pass_median_K_near_zero']]) else 'PARTIAL_OR_FAILED_SPECIFICITY'
    (tables/'rung0l_pass_summary.json').write_text(json.dumps(ps,indent=2),encoding='utf-8')
    decisions=[]
    def dec(group,crit,val,thr,p): decisions.append({'group':group,'criterion':crit,'observed':val,'threshold':thr,'pass':p})
    pc=ps['positive_control']; nl=ps['empty_sky_nulls']
    dec('positive_control','full_model_cv_win_rate',pc['full_model_cv_win_rate_mean'],f">= {c['positive_control_full_model_cv_win_rate_min']}",pc['pass_full_model_cv'])
    dec('positive_control','K_within_15_rate',pc['K_within_15_rate'],f">= {c['positive_control_K_within_15_rate_min']}",pc['pass_K_15'])
    dec('empty_sky_nulls','full_model_cv_win_rate',nl['null_full_model_cv_win_rate_mean'],f"<= {c['null_full_model_cv_win_rate_max']}",nl['pass_full_model_stays_quiet'])
    dec('empty_sky_nulls','false_K_lock_rate',nl['null_false_K_lock_rate'],f"<= {c['null_false_K_lock_rate_max']}",nl['pass_false_K_lock_rate'])
    dec('empty_sky_nulls','non_full_cv_win_rate',nl['null_non_full_cv_win_rate_mean'],f">= {c['null_non_full_cv_win_rate_min']}",nl['pass_non_full_wins'])
    dec('empty_sky_nulls','median_K_hat_scaled',nl['null_median_K_hat_scaled'],f"<= {c['null_median_K_hat_max']}",nl['pass_median_K_near_zero'])
    pd.DataFrame(decisions).to_csv(tables/'rung0l_lock_decision_table.csv',index=False)
    md=f"""# OSM / Opto-PING Rung 0L - Standard-PING Null and Empty-Sky Specificity Gate v0.1

## Executive verdict

**Overall status:** `{ps['overall_status']}`

Rung 0L is the explicit empty-sky test. It asks whether the Opto-PING reciprocal model hallucinates a hidden loop when the generator contains no reciprocal Y-loop.

## Locked specification

- Rung 0L spec SHA-256: `{SPEC_SHA256}`
- Total trials: {len(trial_df)} ({len(pos)} positive-control; {len(null)} null / empty-sky)
- Trials per generator: {n}
- Conditions per trial: {len(CONDITIONS)}
- Models compared: {', '.join(MODELS)}

## Main result

### Positive-control loop-present generator

- Full reciprocal CV win rate mean: {pc['full_model_cv_win_rate_mean']:.3f}
- K within 15% rate: {pc['K_within_15_rate']:.3f}
- K within 10% rate: {pc['K_within_10_rate']:.3f}
- Median K_hat_scaled: {pc['median_K_hat_scaled']:.3f}

### Empty-sky loop-absent generators

- Null full-model CV win rate mean: {nl['null_full_model_cv_win_rate_mean']:.3f}
- Null false K-lock rate: {nl['null_false_K_lock_rate']:.3f}
- Null non-full model CV win rate mean: {nl['null_non_full_cv_win_rate_mean']:.3f}
- Null median K_hat_scaled: {nl['null_median_K_hat_scaled']:.3f}

## Generator summary

{gen_summary.to_markdown(index=False)}

## Interpretation

Rung 0L complements Rung 0J/K. Rung 0J/K demonstrated positive synthetic recovery when the reciprocal loop was present. Rung 0L tests specificity: under Standard-PING, replay-only, sensory-drive-only, generic-hidden, and colored-noise generators, the full reciprocal model should lose and K should not lock.

## Boundary

{SPEC['boundary']}
"""
    (report/'OSM_OptoPING_Rung0L_EmptySky_Report_v0_1.md').write_text(md,encoding='utf-8')
    return ps

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--out-dir',default='/mnt/data/OSM_OptoPING_Rung0L_EmptySkySpecificity_v0_1')
    args=p.parse_args(); run(args.out_dir)
