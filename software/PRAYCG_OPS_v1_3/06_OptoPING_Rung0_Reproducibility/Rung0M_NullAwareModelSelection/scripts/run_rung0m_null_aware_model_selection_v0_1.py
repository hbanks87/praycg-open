from __future__ import annotations
import json, math, hashlib, argparse, zipfile, shutil, textwrap
from pathlib import Path
import numpy as np
import pandas as pd

SPEC = {
    "schema": "OSM_OptoPING_Rung0M_NullAwareModelSelection_v0_1",
    "purpose": "Conservative null-aware model selection after Rung 0L empty-sky specificity failure.",
    "seed_policy": {"seed_start": 930001, "n_trials_per_generator": 20, "n_null_calibration_per_trial": 9},
    "generators": [
        "full_reciprocal_positive_control",
        "standard_ping_null",
        "replay_only_null",
        "sensory_drive_only_null",
        "generic_hidden_oscillator_null",
        "colored_noise_null",
    ],
    "perturbation_conditions": ["doublet_EY", "orthogonal_trap", "counterphase", "lagged_E_to_Y", "recovery_probe", "lagged_Y_to_E"],
    "samples_per_condition": 36,
    "models": [
        "full_reciprocal",
        "eta_only",
        "zeta_only",
        "null_no_coupling",
        "standard_ping",
        "replay_only_basis",
        "sensory_drive_only",
        "generic_hidden_tuned",
        "colored_noise_ar",
    ],
    "model_complexity_penalty": "BIC-like out-of-sample penalty: mse + penalty_scale * p * log(n_train) / n_test; full model gets additional guard penalty.",
    "k_null_calibration": "Trial-wise permutation/shuffled-label/time-reversed controls create an empirical K null. K locks only when p<=0.10, K_hat exceeds null 95th percentile, and full model wins prediction.",
    "generator_specific_pass_criteria": {
        "full_reciprocal_positive_control": {"full_and_K_lock_rate_min": 0.80, "K_significant_rate_min": 0.85, "full_cv_win_rate_min": 0.70, "K_within_15_rate_min": 0.80},
        "standard_ping_null": {"false_full_and_K_lock_rate_max": 0.05, "K_significant_rate_max": 0.10, "full_cv_win_rate_max": 0.35},
        "replay_only_null": {"false_full_and_K_lock_rate_max": 0.05, "K_significant_rate_max": 0.10, "full_cv_win_rate_max": 0.20},
        "sensory_drive_only_null": {"false_full_and_K_lock_rate_max": 0.05, "K_significant_rate_max": 0.10, "full_cv_win_rate_max": 0.20},
        "generic_hidden_oscillator_null": {"false_full_and_K_lock_rate_max": 0.05, "K_significant_rate_max": 0.10, "full_cv_win_rate_max": 0.25},
        "colored_noise_null": {"false_full_and_K_lock_rate_max": 0.05, "K_significant_rate_max": 0.10, "full_cv_win_rate_max": 0.25},
    },
    "global_pass_criteria": {
        "positive_full_and_K_lock_rate_min": 0.80,
        "overall_null_false_full_and_K_lock_rate_max": 0.05,
        "all_generator_thresholds_must_pass": True,
    },
    "boundary": "Synthetic sensitivity/specificity calibration only; no biological, PR-AYC-G, human EEG, microtubular memory, biophotonic, or OSM mechanism claim.",
}
SPEC_SHA256 = hashlib.sha256(json.dumps(SPEC, sort_keys=True, indent=2).encode()).hexdigest()
CONDITIONS = SPEC["perturbation_conditions"]
MODELS = SPEC["models"]
N_PER = SPEC["samples_per_condition"]
COND_PARAMS = {
    "doublet_EY": dict(u=1.00, phase=0.0, rec=0.90, ydrive=0.90, lag=0.20, ping=0.80),
    "orthogonal_trap": dict(u=0.65, phase=1.1, rec=-0.80, ydrive=0.95, lag=-0.55, ping=0.55),
    "counterphase": dict(u=0.85, phase=2.4, rec=-1.00, ydrive=-0.90, lag=0.45, ping=0.75),
    "lagged_E_to_Y": dict(u=0.75, phase=0.7, rec=0.35, ydrive=1.20, lag=0.95, ping=0.60),
    "recovery_probe": dict(u=0.45, phase=1.7, rec=0.15, ydrive=0.35, lag=0.10, ping=0.30),
    "lagged_Y_to_E": dict(u=0.80, phase=2.9, rec=1.05, ydrive=0.55, lag=-0.95, ping=0.65),
}

def z(x):
    x = np.asarray(x, float)
    s = x.std()
    return (x - x.mean()) / (s if s > 1e-9 else 1.0)

def lag(x, k=1):
    return np.r_[np.repeat(x[0], k), x[:-k]]

def ar1(rng, n, rho=0.9, scale=1.0):
    e = rng.normal(0, scale, n)
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = rho * x[i-1] + e[i]
    return z(x)

def basis(cond, n, rng):
    p = COND_PARAMS[cond]
    t = np.linspace(0, 1, n, endpoint=False)
    u = p['u'] * (np.sin(2*np.pi*(1.0 + 0.18*p['ping'])*t + p['phase']) + 0.35*np.sin(2*np.pi*3*t + 0.5*p['phase']))
    ping = p['ping'] * (np.sin(2*np.pi*6*t + p['phase']) - 0.45*np.sin(2*np.pi*6*t + p['phase'] + np.pi/4))
    replay = p['rec'] * np.exp(-2.2*t) * np.cos(2*np.pi*2*t + p['phase'])
    ydrive = p['ydrive'] * (np.sin(2*np.pi*1.5*t + p['phase'] + 0.8) + 0.2*np.cos(2*np.pi*4*t))
    generic = np.sin(2*np.pi*2.5*t + p['phase']*0.7) + 0.4*np.cos(2*np.pi*5*t + 0.3)
    orth = p['lag'] * np.sin(2*np.pi*(0.7 + 0.05*p['u'])*t + p['phase'] + np.pi/2)
    return {"condition": np.array([cond]*n), "u": z(u), "u_lag": z(lag(u, 2)), "ping": z(ping), "ping_lag": z(lag(ping, 1)), "replay": z(replay), "ydrive": z(ydrive), "generic": z(generic), "generic_lag": z(lag(generic, 1)), "orth": z(orth), "orth_lag": z(lag(orth, 1))}

def generate(generator: str, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for cond in CONDITIONS:
        b = basis(cond, N_PER, rng); n=N_PER
        ne = rng.normal(0, 0.24, n); ny = rng.normal(0, 0.24, n); nv = rng.normal(0, 0.24, n)
        u=b['u']; ping=b['ping']; replay=b['replay']; ydrive=b['ydrive']; generic=b['generic']; orth=b['orth']
        if generator == "full_reciprocal_positive_control":
            Y_lat = 0.88*ydrive + 0.32*b['u_lag'] + 0.38*orth + rng.normal(0, 0.14, n)
            E_base = 0.42*u + 0.26*ping + 0.16*replay + ne
            E_raw = E_base + 0.92*lag(Y_lat, 1) + 0.55*lag(Y_lat, 1)*ydrive + 0.38*lag(Y_lat, 1)*orth
            Y_raw = 0.30*ydrive + 0.78*lag(E_raw, 1) + 0.38*lag(E_raw, 1)*b['u_lag'] + 0.12*generic + ny
            V_raw = np.gradient(Y_raw) + 0.62*lag(E_raw, 2) + 0.42*lag(E_raw,1)*lag(Y_raw,1) - 0.15*replay + nv
            kt=1.0
        elif generator == "standard_ping_null":
            E_raw = 0.95*u + 0.90*ping - 0.42*b['ping_lag'] + 0.10*replay + ne
            Y_raw = 0.08*u + 0.05*generic + rng.normal(0, 0.58, n)
            V_raw = np.gradient(Y_raw) + rng.normal(0, 0.58, n); kt=0.0
        elif generator == "replay_only_null":
            E_raw = 0.32*u + 1.15*replay + 0.25*lag(replay, 1) + ne
            common = 0.18*replay + 0.14*u
            Y_raw = common + rng.normal(0, 0.55, n)
            V_raw = np.gradient(common) + rng.normal(0, 0.55, n); kt=0.0
        elif generator == "sensory_drive_only_null":
            E_raw = 1.10*u + 0.25*ping + ne
            Y_raw = 0.95*u + 0.22*orth + ny
            V_raw = 0.70*np.gradient(u) + 0.12*orth + nv; kt=0.0
        elif generator == "generic_hidden_oscillator_null":
            # Hidden oscillator drives E and Y independently, but without E<->Y reciprocal loop.
            h = 1.05*generic + 0.30*b['generic_lag'] + 0.15*orth
            E_raw = 0.50*u + 0.92*h + 0.20*ping + ne
            Y_raw = 0.16*u + 1.00*h + ny
            V_raw = 0.75*np.gradient(h) + 0.12*u + nv; kt=0.0
        elif generator == "colored_noise_null":
            drift = np.linspace(-0.55, 0.55, n)
            cn1 = ar1(rng, n, 0.95, 0.35)
            cn2 = ar1(rng, n, 0.93, 0.35)
            common = 0.55*cn1 + 0.25*cn2 + 0.20*drift
            E_raw = 0.34*u + 0.72*common + ne
            Y_raw = 0.22*u + 0.76*common - 0.10*drift + ny
            V_raw = np.gradient(Y_raw) + 0.35*ar1(rng,n,0.88,0.35) + nv; kt=0.0
        else:
            raise ValueError(generator)
        E=z(E_raw); Y=z(Y_raw); V=z(V_raw)
        for i in range(n):
            rows.append({"condition": cond, "u": u[i], "u_lag": b['u_lag'][i], "ping": ping[i], "ping_lag": b['ping_lag'][i], "replay": replay[i], "ydrive": ydrive[i], "generic": generic[i], "generic_lag": b['generic_lag'][i], "orth": orth[i], "orth_lag": b['orth_lag'][i], "E": E[i], "Yproxy": Y[i], "Vproxy": V[i], "K_true_scaled": kt})
    df = pd.DataFrame(rows)
    for col in ['E','Yproxy','Vproxy','u','ping','replay','generic','orth']:
        df[col+'_l1'] = 0.0
        for cond in CONDITIONS:
            m = df['condition'] == cond
            df.loc[m, col+'_l1'] = lag(df.loc[m, col].values, 1)
    return df

def X_for(df: pd.DataFrame, model: str) -> np.ndarray:
    def cols(names):
        return [df[c].values for c in names]
    base = [np.ones(len(df))]
    if model == "full_reciprocal":
        base += cols(['u','u_lag','ping','replay','ydrive','orth','generic','E_l1','Yproxy_l1','Vproxy_l1'])
        base += [df['Yproxy_l1'].values*df['ydrive'].values, df['E_l1'].values*df['u_lag'].values, df['E_l1'].values*df['Yproxy_l1'].values, df['Vproxy_l1'].values*df['orth'].values]
    elif model == "eta_only":
        base += cols(['u','ping','replay','ydrive','Yproxy_l1','Vproxy_l1']) + [df['Yproxy_l1'].values*df['ydrive'].values]
    elif model == "zeta_only":
        base += cols(['u','u_lag','ping','replay','ydrive','E_l1']) + [df['E_l1'].values*df['u_lag'].values]
    elif model == "null_no_coupling":
        base += cols(['u'])
    elif model == "standard_ping":
        base += cols(['u','u_lag','ping','ping_lag','E_l1'])
    elif model == "replay_only_basis":
        base += cols(['u','replay','replay_l1','E_l1']) + [df['replay'].values*df['u'].values]
    elif model == "sensory_drive_only":
        base += cols(['u','u_lag','orth','ping']) + [np.gradient(df['u'].values)]
    elif model == "generic_hidden_tuned":
        base += cols(['u','generic','generic_lag','orth','orth_lag','E_l1']) + [df['generic'].values*df['orth'].values, df['generic_lag'].values*df['u_lag'].values]
    elif model == "colored_noise_ar":
        # Flexible but penalized common-driver/AR weather model. It is allowed to explain structured noise without a reciprocal-loop interpretation.
        base += cols(['u','u_lag','E_l1','Yproxy_l1','Vproxy_l1','generic','orth']) + [df['E_l1'].values*df['u'].values, df['Yproxy_l1'].values*df['u'].values]
    else:
        raise ValueError(model)
    return np.column_stack(base)

def bic_penalized_cv_loss(X, Y, train_mask, test_mask, model, penalty_scale=0.012):
    # ridge solution with BIC-like complexity penalty on held-out loss
    Xtr=X[train_mask]; Ytr=Y[train_mask]; Xte=X[test_mask]; Yte=Y[test_mask]
    mu=Xtr.mean(0); sd=Xtr.std(0); mu[0]=0; sd[0]=1; sd[sd<1e-9]=1
    Xtr=(Xtr-mu)/sd; Xte=(Xte-mu)/sd
    p=Xtr.shape[1]; ntr=max(2,Xtr.shape[0]); nte=max(1,Xte.shape[0])
    ridge=0.35 if model=='full_reciprocal' else 0.22
    pen=np.eye(p)*ridge; pen[0,0]=0
    B=np.linalg.solve(Xtr.T@Xtr+pen, Xtr.T@Ytr)
    pred=Xte@B
    mse=float(np.mean((pred-Yte)**2))
    guard=0.0
    if model=='full_reciprocal': guard += 0.004
    # BIC-like held-out penalty; scale tuned/locked in spec for this gate
    return mse + penalty_scale*p*math.log(ntr)/nte + guard

def k_est(df: pd.DataFrame):
    # Partial out input/common-driver terms first; then assess reciprocal lagged cross-prediction.
    controls = np.column_stack([np.ones(len(df)), df[['u','u_lag','ping','replay','generic','generic_lag','orth','orth_lag']].values])
    Xeta = np.column_stack([controls, df['Yproxy_l1'].values, df['Vproxy_l1'].values])
    ridge_eta = np.eye(Xeta.shape[1]) * 1e-5; ridge_eta[0,0]=0
    beta_eta = np.linalg.solve(Xeta.T @ Xeta + ridge_eta, Xeta.T @ df['E'].values)
    eta = float(beta_eta[-2])
    Xzeta = np.column_stack([controls, df['E_l1'].values])
    ridge_zeta = np.eye(Xzeta.shape[1]) * 1e-5; ridge_zeta[0,0]=0
    beta_zeta = np.linalg.solve(Xzeta.T @ Xzeta + ridge_zeta, Xzeta.T @ df['Yproxy'].values)
    zeta = float(beta_zeta[-1])
    product=eta*zeta
    K=math.sqrt(abs(product))/0.70 if abs(product)>1e-12 else 0.0
    return eta,zeta,product,K

def permute_within_conditions(df: pd.DataFrame, rng, mode: str) -> pd.DataFrame:
    out=df.copy()
    # Break reciprocal alignment while preserving marginal distribution and inputs.
    for cond in CONDITIONS:
        m = out['condition']==cond
        idx = out.index[m].to_numpy()
        if mode=='shuffle_y':
            vals = out.loc[idx,'Yproxy'].values.copy(); rng.shuffle(vals); out.loc[idx,'Yproxy']=vals
            valsv = out.loc[idx,'Vproxy'].values.copy(); rng.shuffle(valsv); out.loc[idx,'Vproxy']=valsv
        elif mode=='time_reverse_y':
            out.loc[idx,'Yproxy']=out.loc[idx,'Yproxy'].values[::-1]
            out.loc[idx,'Vproxy']=out.loc[idx,'Vproxy'].values[::-1]
        elif mode=='condition_shift_y':
            # circularly shift Y/V by a nontrivial amount within condition
            shift=max(3, len(idx)//3)
            out.loc[idx,'Yproxy']=np.roll(out.loc[idx,'Yproxy'].values, shift)
            out.loc[idx,'Vproxy']=np.roll(out.loc[idx,'Vproxy'].values, -shift)
        else:
            raise ValueError(mode)
    for col in ['E','Yproxy','Vproxy','u','ping','replay','generic','orth']:
        out[col+'_l1']=0.0
        for cond in CONDITIONS:
            m=out['condition']==cond
            out.loc[m,col+'_l1']=lag(out.loc[m,col].values,1)
    return out

def k_null_calibration(df: pd.DataFrame, seed: int, n_null=36):
    rng=np.random.default_rng(seed+770000)
    modes=['shuffle_y','time_reverse_y','condition_shift_y']
    null_ks=[]
    for i in range(n_null):
        dnull=permute_within_conditions(df, rng, modes[i%len(modes)])
        null_ks.append(k_est(dnull)[3])
    null_ks=np.array(null_ks,float)
    obs=k_est(df)[3]
    # p-value: upper-tail with +1 correction
    p=(1.0+np.sum(null_ks>=obs))/(len(null_ks)+1.0)
    q95=float(np.quantile(null_ks,0.95))
    sig=bool((p<=0.10) and (obs>q95))
    return obs,p,q95,float(np.median(null_ks)),sig

def fit_all_models(df):
    Y=df[['E','Yproxy','Vproxy']].values
    Xs={m:X_for(df,m) for m in MODELS}
    loss_rows=[]; winners=[]
    for hold in CONDITIONS:
        test=(df['condition'].values==hold); train=~test
        losses=[]
        for m in MODELS:
            loss=bic_penalized_cv_loss(Xs[m],Y,train,test,m)
            losses.append((m,loss))
            loss_rows.append({'fold_condition':hold,'model':m,'loss':loss})
        winner=min(losses,key=lambda x:x[1])
        winners.append(winner[0])
    return loss_rows,winners

def run(out_dir):
    out_dir=Path(out_dir); tables=out_dir/'tables'; report=out_dir/'report'; lock=out_dir/'locked_protocol'; scripts=out_dir/'scripts'
    for d in [tables, report, lock, scripts]: d.mkdir(parents=True, exist_ok=True)
    (lock/'RUNG0M_SPEC_v0_1.json').write_text(json.dumps({**SPEC,'spec_sha256':SPEC_SHA256}, indent=2), encoding='utf-8')
    (lock/'RUNG0M_SPEC_SHA256.txt').write_text(SPEC_SHA256+'\n')
    n=SPEC['seed_policy']['n_trials_per_generator']; start=SPEC['seed_policy']['seed_start']; ncal=SPEC['seed_policy']['n_null_calibration_per_trial']
    trial_rows=[]; all_losses=[]; all_winners=[]; k_null_rows=[]
    for gi,g in enumerate(SPEC['generators']):
        for j in range(n):
            seed=start+gi*10000+j
            df=generate(g, seed)
            loss_rows,winners=fit_all_models(df)
            eta,zeta,prod,K=k_est(df)
            K_obs, p_K, q95, med_null, K_sig = k_null_calibration(df, seed, ncal)
            assert abs(K-K_obs) < 1e-9
            full_wins=sum(w=='full_reciprocal' for w in winners)
            full_cv_rate=full_wins/len(CONDITIONS)
            full_pred_win=full_cv_rate > 0.5
            full_and_K=bool(full_pred_win and K_sig)
            K_true=float(df['K_true_scaled'].iloc[0])
            row={'generator':g,'trial':j+1,'seed':seed,'K_true_scaled':K_true,'eta_hat':eta,'zeta_hat':zeta,'eta_zeta_product':prod,'K_hat_scaled':K,'K_null_p_upper':p_K,'K_null_q95':q95,'K_null_median':med_null,'K_significant_null_calibrated':K_sig,'K_within_15_positive':bool(g=='full_reciprocal_positive_control' and abs(K-1.0)<=0.15),'K_within_10_positive':bool(g=='full_reciprocal_positive_control' and abs(K-1.0)<=0.10),'full_cv_wins':full_wins,'full_cv_win_rate':full_cv_rate,'full_prediction_win':full_pred_win,'full_and_K_lock':full_and_K,'non_full_cv_win_rate':1-full_cv_rate,'cv_winner_counts_json':json.dumps(pd.Series(winners).value_counts().to_dict(),sort_keys=True)}
            trial_rows.append(row)
            for lr in loss_rows:
                all_losses.append({'generator':g,'trial':j+1,'seed':seed,**lr})
            for fold,w in zip(CONDITIONS,winners):
                all_winners.append({'generator':g,'trial':j+1,'seed':seed,'fold_condition':fold,'winning_model':w})
            k_null_rows.append({'generator':g,'trial':j+1,'seed':seed,'K_hat_scaled':K,'K_null_p_upper':p_K,'K_null_q95':q95,'K_null_median':med_null,'K_significant_null_calibrated':K_sig})
    trial_df=pd.DataFrame(trial_rows); loss_df=pd.DataFrame(all_losses); winners_df=pd.DataFrame(all_winners); knull_df=pd.DataFrame(k_null_rows)
    trial_df.to_csv(tables/'rung0m_trial_results.csv',index=False)
    loss_df.to_csv(tables/'rung0m_cv_model_losses.csv',index=False)
    winners_df.to_csv(tables/'rung0m_cv_fold_winners.csv',index=False)
    knull_df.to_csv(tables/'rung0m_k_null_calibration.csv',index=False)
    gen_summary=trial_df.groupby('generator').agg(
        n_trials=('trial','count'),
        K_true_scaled=('K_true_scaled','first'),
        median_K_hat_scaled=('K_hat_scaled','median'),
        mean_K_hat_scaled=('K_hat_scaled','mean'),
        K_within_15_positive_rate=('K_within_15_positive','mean'),
        K_within_10_positive_rate=('K_within_10_positive','mean'),
        K_significant_rate=('K_significant_null_calibrated','mean'),
        full_cv_win_rate_mean=('full_cv_win_rate','mean'),
        full_prediction_win_rate=('full_prediction_win','mean'),
        full_and_K_lock_rate=('full_and_K_lock','mean'),
        non_full_cv_win_rate_mean=('non_full_cv_win_rate','mean'),
        median_K_null_p=('K_null_p_upper','median')
    ).reset_index()
    gen_summary.to_csv(tables/'rung0m_generator_summary.csv',index=False)
    win_summary=winners_df.groupby(['generator','winning_model']).size().reset_index(name='wins')
    totals=winners_df.groupby('generator').size().reset_index(name='total_folds')
    win_summary=win_summary.merge(totals,on='generator')
    win_summary['win_rate']=win_summary['wins']/win_summary['total_folds']
    win_summary.to_csv(tables/'rung0m_cv_win_summary.csv',index=False)
    # generator-specific decisions
    decisions=[]
    criteria=SPEC['generator_specific_pass_criteria']
    gen_s=gen_summary.set_index('generator')
    for g,c in criteria.items():
        obs=gen_s.loc[g]
        if g=='full_reciprocal_positive_control':
            tests=[('full_and_K_lock_rate',obs.full_and_K_lock_rate, f">= {c['full_and_K_lock_rate_min']}", obs.full_and_K_lock_rate>=c['full_and_K_lock_rate_min']),('K_significant_rate',obs.K_significant_rate,f">= {c['K_significant_rate_min']}", obs.K_significant_rate>=c['K_significant_rate_min']),('full_cv_win_rate_mean',obs.full_cv_win_rate_mean,f">= {c['full_cv_win_rate_min']}", obs.full_cv_win_rate_mean>=c['full_cv_win_rate_min']),('K_within_15_positive_rate',obs.K_within_15_positive_rate,f">= {c['K_within_15_rate_min']}", obs.K_within_15_positive_rate>=c['K_within_15_rate_min'])]
        else:
            tests=[('false_full_and_K_lock_rate',obs.full_and_K_lock_rate, f"<= {c['false_full_and_K_lock_rate_max']}", obs.full_and_K_lock_rate<=c['false_full_and_K_lock_rate_max']),('K_significant_rate',obs.K_significant_rate, f"<= {c['K_significant_rate_max']}", obs.K_significant_rate<=c['K_significant_rate_max']),('full_cv_win_rate_mean',obs.full_cv_win_rate_mean, f"<= {c['full_cv_win_rate_max']}", obs.full_cv_win_rate_mean<=c['full_cv_win_rate_max'])]
        for name,val,thr,p in tests:
            decisions.append({'generator':g,'criterion':name,'observed':float(val),'threshold':thr,'pass':bool(p)})
    decisions_df=pd.DataFrame(decisions)
    decisions_df.to_csv(tables/'rung0m_generator_specific_decision_table.csv',index=False)
    pos=trial_df[trial_df.generator=='full_reciprocal_positive_control']
    null=trial_df[trial_df.generator!='full_reciprocal_positive_control']
    global_decisions={
        'positive_full_and_K_lock_rate': float(pos.full_and_K_lock.mean()),
        'overall_null_false_full_and_K_lock_rate': float(null.full_and_K_lock.mean()),
        'all_generator_thresholds_pass': bool(decisions_df['pass'].all()),
    }
    global_pass=bool(global_decisions['positive_full_and_K_lock_rate']>=SPEC['global_pass_criteria']['positive_full_and_K_lock_rate_min'] and global_decisions['overall_null_false_full_and_K_lock_rate']<=SPEC['global_pass_criteria']['overall_null_false_full_and_K_lock_rate_max'] and global_decisions['all_generator_thresholds_pass'])
    ps={
        'schema':'OSM_OptoPING_Rung0M_NullAwareModelSelection_results_v0_1',
        'spec_sha256':SPEC_SHA256,
        'n_trials_total':int(len(trial_df)),
        'n_positive_trials':int(len(pos)),
        'n_null_trials':int(len(null)),
        'positive_control':{
            'full_and_K_lock_rate':float(pos.full_and_K_lock.mean()),
            'K_significant_rate':float(pos.K_significant_null_calibrated.mean()),
            'K_within_15_rate':float(pos.K_within_15_positive.mean()),
            'K_within_10_rate':float(pos.K_within_10_positive.mean()),
            'full_model_cv_win_rate_mean':float(pos.full_cv_win_rate.mean()),
            'median_K_hat_scaled':float(pos.K_hat_scaled.median()),
        },
        'empty_sky_nulls':{
            'overall_false_full_and_K_lock_rate':float(null.full_and_K_lock.mean()),
            'overall_K_significant_rate':float(null.K_significant_null_calibrated.mean()),
            'overall_full_model_cv_win_rate_mean':float(null.full_cv_win_rate.mean()),
            'overall_non_full_cv_win_rate_mean':float(null.non_full_cv_win_rate.mean()),
            'overall_median_K_hat_scaled':float(null.K_hat_scaled.median()),
            'overall_median_K_null_p':float(null.K_null_p_upper.median()),
        },
        'global_decisions':global_decisions,
        'overall_status':'PASS_NULL_AWARE_SPECIFICITY' if global_pass else 'PARTIAL_OR_FAILED_NULL_AWARE_SPECIFICITY',
        'boundary':SPEC['boundary'],
    }
    (tables/'rung0m_pass_summary.json').write_text(json.dumps(ps,indent=2),encoding='utf-8')
    # concise markdown report
    def md_table(df):
        return df.to_markdown(index=False, floatfmt='.3f')
    md=f"""# OSM / Opto-PING Rung 0M - Conservative Null-Aware Model Selection and K-Significance Calibration v0.1

## Executive verdict

**Overall status:** `{ps['overall_status']}`

Rung 0M was designed because Rung 0L showed a split result: the scalar K endpoint mostly stayed quiet under null generators, but the full reciprocal model could still win too often under structured null skies. Rung 0M therefore required **two simultaneous gates**:

1. prediction gate: the full reciprocal model must win held-out prediction after stronger model penalties and better alternatives;
2. K gate: K must be significant against trial-wise permutation, shuffled-label, and time-reversed null controls.

A full Opto-PING lock requires both gates at the same time. Full-model prediction alone is not sufficient.

## Locked specification

- Rung 0M spec SHA-256: `{SPEC_SHA256}`
- Total trials: {len(trial_df)}
- Positive-control trials: {len(pos)}
- Empty-sky/null trials: {len(null)}
- Null-calibration controls per trial: {ncal}
- Boundary: {SPEC['boundary']}

## Main result

### Positive-control generator

- Full + K simultaneous lock rate: {ps['positive_control']['full_and_K_lock_rate']:.3f}
- K significant rate: {ps['positive_control']['K_significant_rate']:.3f}
- K within 15% rate: {ps['positive_control']['K_within_15_rate']:.3f}
- K within 10% rate: {ps['positive_control']['K_within_10_rate']:.3f}
- Full reciprocal mean CV win rate: {ps['positive_control']['full_model_cv_win_rate_mean']:.3f}
- Median K_hat_scaled: {ps['positive_control']['median_K_hat_scaled']:.3f}

### Empty-sky/null generators

- Overall false full + K lock rate: {ps['empty_sky_nulls']['overall_false_full_and_K_lock_rate']:.3f}
- Overall K significant rate: {ps['empty_sky_nulls']['overall_K_significant_rate']:.3f}
- Overall full reciprocal mean CV win rate: {ps['empty_sky_nulls']['overall_full_model_cv_win_rate_mean']:.3f}
- Overall non-full mean CV win rate: {ps['empty_sky_nulls']['overall_non_full_cv_win_rate_mean']:.3f}
- Overall median K_hat_scaled: {ps['empty_sky_nulls']['overall_median_K_hat_scaled']:.3f}

## Generator summary

{md_table(gen_summary)}

## Generator-specific decision table

{md_table(decisions_df)}

## Interpretation

Rung 0M is a stricter test than Rung 0L. It treats `full_reciprocal` prediction as insufficient unless it is accompanied by null-calibrated K significance. The pipeline is now testing specificity by asking whether the radar can both find the simulated target when it exists and stay quiet when the data are Standard-PING, replay-only, sensory-drive-only, generic-hidden, or colored-noise nulls.

## Boundary

This is synthetic sensitivity/specificity calibration only. It does not prove or disprove OSM, microtubular memory, biophotonic flickering, human EEG mechanism, or PR-AYC-G results.
"""
    (report/'OSM_OptoPING_Rung0M_NullAware_Report_v0_1.md').write_text(md,encoding='utf-8')
    return ps, gen_summary, decisions_df, win_summary

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--out-dir',default='/mnt/data/OSM_OptoPING_Rung0M_NullAwareModelSelection_v0_1')
    args=p.parse_args(); run(args.out_dir)
