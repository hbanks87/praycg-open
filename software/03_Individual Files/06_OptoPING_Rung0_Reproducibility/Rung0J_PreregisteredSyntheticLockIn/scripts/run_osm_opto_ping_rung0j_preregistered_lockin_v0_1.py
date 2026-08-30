#!/usr/bin/env python3
"""Reproduce OSM / Opto-PING Rung 0J preregistered synthetic lock-in v0.1."""
import argparse, json, math, hashlib
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd

LOCKED_SPEC = json.loads(r'''
{
  "K_lock_criteria": {
    "directional_secondary": "eta_E and zeta_E each within 20% in >=80% of trials; reported only after K-lock passes",
    "model_specificity": "full reciprocal model wins >=80% of leave-one-perturbation-family-out CV folds",
    "primary_pass": ">= 90% of trials recover K within 15% of K_true AND median K error <= 10%",
    "strict_secondary": ">= 80% of trials recover K within 10%"
  },
  "alternative_models": [
    {
      "description": "eta_E and zeta_E free; K primary.",
      "name": "full_reciprocal"
    },
    {
      "description": "Y-to-E direction only; zeta_E fixed to zero.",
      "name": "eta_only"
    },
    {
      "description": "E-to-Y direction only; eta_E fixed to zero.",
      "name": "zeta_only"
    },
    {
      "description": "eta_E=zeta_E=0.",
      "name": "null_no_coupling"
    },
    {
      "description": "independent non-directional stimulus-basis regression; no reciprocal loop.",
      "name": "replay_only_basis"
    },
    {
      "description": "single symmetric hidden oscillator parameter h; no eta/zeta decomposition.",
      "name": "generic_hidden_oscillator"
    }
  ],
  "boundary": "Synthetic Rung 0 only. This does not prove OSM, microtubular memory, LTP, dendritic spine growth, quantum memory, or human EEG mechanism.",
  "document_status": "synthetic_identifiability_lock_in; not biological proof",
  "failure_thresholds": {
    "K_lock_failure": "<90% trials within 15% K error OR median K error >10%",
    "alternative_warning": "any single non-full alternative wins >20% of held-out CV folds",
    "ridge_warning": "profile likelihood remains broad enough that eta/zeta separation is conditional even if K-lock passes",
    "specificity_failure": "full reciprocal held-out CV win rate <80%"
  },
  "fresh_seed_policy": {
    "n_trials": 60,
    "rule": "No tuning, no grid change, no perturbation change, and no threshold change after seed loop begins.",
    "seed_set_name": "fresh_lock_in_seed_set_A",
    "seed_start": 910001,
    "seed_stop_inclusive": 910060
  },
  "locked_before_seed_run": true,
  "model_equations": {
    "feature_model": [
      "z = zeta_E / 45",
      "K_scaled = 4 * sqrt(eta_E*zeta_E) / sqrt(4*180)",
      "E = 0.8*dE + 0.42*eta_E*dY + 0.20*K_scaled*mix + 0.12*z*lag*dE + 0.18*orth*(eta_E-z) + 0.12*rec*K_scaled",
      "Y_proxy = 0.8*dY + 0.39*z*dE + 0.17*K_scaled*mix - 0.12*eta_E*lag*dY - 0.16*orth*(eta_E-z) + 0.10*rec*K_scaled",
      "V_proxy = 0.62*(z*dE - eta_E*dY) + 0.42*lag*(z*dE + eta_E*dY) + 0.25*K_scaled*orth + 0.08*rec*(eta_E+z)"
    ],
    "loop_gain": "K_loop = eta_E * zeta_E",
    "noise_model": "Gaussian residual proxy noise at SNR=6 plus low-amplitude channel offset noise; fixed across all models.",
    "primary_estimand": "K = sqrt(eta_E * zeta_E)",
    "synthetic_observation_vector": "X_c = [E_c, Y_proxy_c, V_proxy_c] for each perturbation condition c"
  },
  "observation_family": "E_plus_Yproxy_plus_Vproxy",
  "parameter_grids": {
    "eta_E_grid": {
      "start": 2.0,
      "step": 0.25,
      "stop": 6.0
    },
    "generic_hidden_h_grid": {
      "start": 1.0,
      "step": 0.25,
      "stop": 8.0
    },
    "zeta_E_grid": {
      "start": 120.0,
      "step": 5.0,
      "stop": 240.0
    }
  },
  "primary_perturbation_order": [
    {
      "dE": 1.0,
      "dY": 1.0,
      "lag": 0.0,
      "mix": 1.0,
      "name": "doublet_EY",
      "orth": 0.0,
      "rec": 0.0
    },
    {
      "dE": 1.0,
      "dY": -1.0,
      "lag": 0.5,
      "mix": -1.0,
      "name": "orthogonal_trap",
      "orth": 1.0,
      "rec": 0.0
    },
    {
      "dE": 0.8,
      "dY": -0.8,
      "lag": 0.0,
      "mix": -0.8,
      "name": "counterphase",
      "orth": 0.0,
      "rec": 0.0
    },
    {
      "dE": 1.2,
      "dY": 0.15,
      "lag": 1.0,
      "mix": 0.3,
      "name": "lagged_E_to_Y",
      "orth": 0.0,
      "rec": 0.0
    },
    {
      "dE": 0.2,
      "dY": 0.2,
      "lag": 0.0,
      "mix": 0.1,
      "name": "recovery_probe",
      "orth": 0.0,
      "rec": 1.0
    },
    {
      "dE": 0.15,
      "dY": 1.2,
      "lag": -1.0,
      "mix": 0.3,
      "name": "lagged_Y_to_E",
      "orth": 0.0,
      "rec": 0.0
    }
  ],
  "reporting_template_files": [
    "LOCKED_PROTOCOL.md",
    "REPORTING_TEMPLATE.md",
    "run_summary.json",
    "trial_results.csv",
    "cv_model_losses.csv",
    "profile_likelihood_grid.csv"
  ],
  "schema": "OSM_OptoPING_Rung0J_PreregisteredSyntheticLockIn_v0_1",
  "true_parameters": {
    "K": 26.832815729997478,
    "K_loop": 720.0,
    "eta_E": 4.0,
    "fY_hz": 7.0,
    "zeta_E": 180.0
  }
}
''')
EXPECTED_SPEC_SHA256 = "d93f6146e4e77ffeffbdd5c133250fd6d474317d8af6c34c3354dd6b28756282"

def canonical_spec_hash():
    return hashlib.sha256(json.dumps(LOCKED_SPEC, sort_keys=True, indent=2).encode('utf-8')).hexdigest()

def frange(start, stop, step):
    vals=[]; x=start
    while x <= stop+1e-9:
        vals.append(round(x,10)); x += step
    return np.array(vals, dtype=float)

eta_true=LOCKED_SPEC['true_parameters']['eta_E']; zeta_true=LOCKED_SPEC['true_parameters']['zeta_E']; K_true=LOCKED_SPEC['true_parameters']['K']
conditions=LOCKED_SPEC['primary_perturbation_order']
eta_grid=frange(**LOCKED_SPEC['parameter_grids']['eta_E_grid'])
zeta_grid=frange(**LOCKED_SPEC['parameter_grids']['zeta_E_grid'])
h_grid=frange(**LOCKED_SPEC['parameter_grids']['generic_hidden_h_grid'])

def pred_full(eta,zeta,conds=conditions):
    z=zeta/45.0; K=math.sqrt(max(eta*zeta,0.0)); K_scaled=4.0*K/K_true if K_true>0 else 0.0; rows=[]
    for c in conds:
        dE,dY,lag,mix,orth,rec=c['dE'],c['dY'],c['lag'],c['mix'],c['orth'],c['rec']
        E=0.8*dE+0.42*eta*dY+0.20*K_scaled*mix+0.12*z*lag*dE+0.18*orth*(eta-z)+0.12*rec*K_scaled
        Y=0.8*dY+0.39*z*dE+0.17*K_scaled*mix-0.12*eta*lag*dY-0.16*orth*(eta-z)+0.10*rec*K_scaled
        V=0.62*(z*dE-eta*dY)+0.42*lag*(z*dE+eta*dY)+0.25*K_scaled*orth+0.08*rec*(eta+z)
        rows.append([E,Y,V])
    return np.array(rows,float)

def pred_generic(h,conds=conditions):
    rows=[]
    for c in conds:
        dE,dY,lag,mix,orth,rec=c['dE'],c['dY'],c['lag'],c['mix'],c['orth'],c['rec']; s=dE+dY; q=dE-dY
        E=0.8*dE+0.25*h*s+0.25*h*mix+0.08*h*rec
        Y=0.8*dY+0.25*h*s+0.25*h*mix+0.08*h*rec
        V=0.25*h*lag+0.15*h*orth+0.05*h*q
        rows.append([E,Y,V])
    return np.array(rows,float)

true_prediction=pred_full(eta_true,zeta_true)
full_params=[]; full_preds=[]
for eta in eta_grid:
    for zeta in zeta_grid:
        full_params.append((eta,zeta,math.sqrt(eta*zeta),eta*zeta)); full_preds.append(pred_full(eta,zeta))
full_params=np.array(full_params); full_preds=np.array(full_preds)
eta_preds=np.array([pred_full(e,0.0) for e in eta_grid])
zeta_preds=np.array([pred_full(0.0,z) for z in zeta_grid])
generic_preds=np.array([pred_generic(h) for h in h_grid])
null_pred=pred_full(0,0)

def loss_grid(arr,obs,mask): return ((arr[:,mask,:]-obs[mask])**2).sum(axis=(1,2))

def fit_grid(obs,mask,model):
    if model=='full_reciprocal':
        loss=loss_grid(full_preds,obs,mask); i=int(loss.argmin()); eta,zeta,K,Kloop=full_params[i]
        return {'model':model,'pred':full_preds[i],'loss':float(loss[i]),'eta_E':float(eta),'zeta_E':float(zeta),'K':float(K),'K_loop':float(Kloop)}
    if model=='eta_only':
        loss=loss_grid(eta_preds,obs,mask); i=int(loss.argmin()); return {'model':model,'pred':eta_preds[i],'loss':float(loss[i])}
    if model=='zeta_only':
        loss=loss_grid(zeta_preds,obs,mask); i=int(loss.argmin()); return {'model':model,'pred':zeta_preds[i],'loss':float(loss[i])}
    if model=='generic_hidden_oscillator':
        loss=loss_grid(generic_preds,obs,mask); i=int(loss.argmin()); return {'model':model,'pred':generic_preds[i],'loss':float(loss[i])}
    if model=='null_no_coupling': return {'model':model,'pred':null_pred,'loss':float(((null_pred[mask]-obs[mask])**2).sum())}
    raise ValueError(model)

def fit_replay(obs,train,ridge=2.0):
    X=np.array([[1.0,c['dE'],c['dY'],c['rec']] for c in conditions],float); Xt=X[train]; Y=obs[train]
    coef=np.linalg.solve(Xt.T@Xt+ridge*np.eye(X.shape[1]), Xt.T@Y); pred=X@coef
    return {'model':'replay_only_basis','pred':pred,'loss':float(((pred[train]-obs[train])**2).sum())}

def run_one(seed):
    rng=np.random.default_rng(seed); noise_sd=float(np.std(true_prediction))/6.0
    obs=true_prediction+rng.normal(0.0,noise_sd,true_prediction.shape)
    obs[:,1]+=rng.normal(0.0,noise_sd*0.20); obs[:,2]+=rng.normal(0.0,noise_sd*0.20)
    mask=np.ones(len(conditions),bool); f=fit_grid(obs,mask,'full_reciprocal')
    rows=[]; winners=[]
    for hold,c in enumerate(conditions):
        train=np.ones(len(conditions),bool); train[hold]=False; test=~train
        fits=[fit_grid(obs,train,m) for m in ['full_reciprocal','eta_only','zeta_only','generic_hidden_oscillator','null_no_coupling']]+[fit_replay(obs,train)]
        losses=[]
        for m in fits:
            tl=float(((m['pred'][test]-obs[test])**2).sum()); losses.append((m['model'],tl)); rows.append({'seed':seed,'heldout_condition':c['name'],'model':m['model'],'heldout_loss':tl,'train_loss':m['loss']})
        winners.append(min(losses,key=lambda x:x[1])[0])
    eta=f['eta_E']; zeta=f['zeta_E']; K=f['K']
    trial={'seed':seed,'eta_hat':eta,'zeta_hat':zeta,'K_hat':K,'K_loop_hat':eta*zeta,'eta_pct_error':abs(eta-eta_true)/eta_true,'zeta_pct_error':abs(zeta-zeta_true)/zeta_true,'K_pct_error':abs(K-K_true)/K_true,'K_lock_15_pass':abs(K-K_true)/K_true<=.15,'K_lock_10_pass':abs(K-K_true)/K_true<=.10,'directional_20_pass':abs(eta-eta_true)/eta_true<=.2 and abs(zeta-zeta_true)/zeta_true<=.2,'directional_15_pass':abs(eta-eta_true)/eta_true<=.15 and abs(zeta-zeta_true)/zeta_true<=.15,'full_cv_fold_wins':winners.count('full_reciprocal'),'full_cv_win_rate':winners.count('full_reciprocal')/len(winners),'cv_winners_pipe':'|'.join(winners)}
    return trial, rows

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out-dir',default='rung0j_reproduced'); args=ap.parse_args(); out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    got=canonical_spec_hash()
    if got != EXPECTED_SPEC_SHA256: raise SystemExit(f'LOCKED SPEC HASH MISMATCH: {got} != {EXPECTED_SPEC_SHA256}')
    seeds=range(LOCKED_SPEC['fresh_seed_policy']['seed_start'],LOCKED_SPEC['fresh_seed_policy']['seed_stop_inclusive']+1)
    trials=[]; cv=[]
    for seed in seeds:
        t,r=run_one(seed); trials.append(t); cv.extend(r)
    tdf=pd.DataFrame(trials); cdf=pd.DataFrame(cv)
    tdf.to_csv(out/'rung0j_trial_results.csv',index=False); cdf.to_csv(out/'rung0j_cv_model_losses.csv',index=False)
    winners=[]
    for (seed,cond),g in cdf.groupby(['seed','heldout_condition']): winners.append(g.sort_values('heldout_loss').iloc[0]['model'])
    summary={'locked_spec_sha256':got,'n_trials':len(tdf),'K_within_15_rate':float(tdf.K_lock_15_pass.mean()),'K_within_10_rate':float(tdf.K_lock_10_pass.mean()),'K_median_pct_error':float(tdf.K_pct_error.median()),'directional_20_pass_rate':float(tdf.directional_20_pass.mean()),'full_model_cv_fold_win_rate':float(pd.Series(winners).eq('full_reciprocal').mean()),'cv_wins':dict(Counter(winners))}
    (out/'rung0j_pass_summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
