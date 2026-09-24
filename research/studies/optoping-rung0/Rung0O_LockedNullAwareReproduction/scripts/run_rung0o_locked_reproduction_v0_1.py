#!/usr/bin/env python3
"""Rung 0O locked reproduction runner.
Run from package root after installing requirements. It uses the bundled Rung 0N source script and locked K thresholds.
"""
from __future__ import annotations
import argparse, importlib.util, json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd

RUNG0N_SHA = 'f11cc9662d5a666c10f29e11f70c88a04e377e6499e87ae0bb1f1632e884a6b8'
FRESH_SEED = 20260805
SELECTED_PENALTY = 0.04

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', default='reproduced_rung0o_outputs')
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True); (out/'tables').mkdir(exist_ok=True)
    mod_path = root/'scripts'/'source_run_rung0n_k_null_calibration_repair_v0_1.py'
    thresholds_path = root/'locked_protocol'/'LOCKED_RUNG0N_K_THRESHOLDS.csv'
    spec = importlib.util.spec_from_file_location('rung0n_source', str(mod_path))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    thresholds = pd.read_csv(thresholds_path)
    pooled_positive_threshold = float(thresholds['pooled_q975_K_null'].iloc[0])
    rng = np.random.default_rng(FRESH_SEED)
    trials, losses = mod.simulate_trial_losses(rng)
    T, penalized_losses, winners = mod.evaluate(trials, losses, thresholds, pooled_positive_threshold, SELECTED_PENALTY)
    pass_summary_n, gen_summary, cv_summary, decision = mod.summarize(T, winners)
    pos = T[T['generator_type']=='positive']; nul = T[T['generator_type']=='null']
    status = 'PASS_LOCKED_NULL_AWARE_REPRODUCTION' if bool(decision['pass'].all()) else 'FAILED_OR_PARTIAL_LOCKED_NULL_AWARE_REPRODUCTION'
    pass_summary = {
        'schema':'OSM_OptoPING_Rung0O_LockedNullAwareReproduction_results_v0_1',
        'status': status,
        'rung0n_locked_spec_sha256': RUNG0N_SHA,
        'rung0o_reproduction_seed': FRESH_SEED,
        'selected_penalty': SELECTED_PENALTY,
        'n_total_trials': int(T.shape[0]),
        'n_positive_trials': int(pos.shape[0]),
        'n_null_trials': int(nul.shape[0]),
        'positive_full_plus_K_lock_rate': float(pos['final_full_plus_K_lock'].mean()),
        'positive_K_significant_rate': float(pos['K_significant_raw'].mean()),
        'positive_K_within_15_rate': float(pos['K_within_15_positive'].mean()),
        'positive_K_within_10_rate': float(pos['K_within_10_positive'].mean()),
        'null_false_full_plus_K_lock_rate': float(nul['final_full_plus_K_lock'].mean()),
        'null_raw_K_significant_rate': float(nul['K_significant_raw'].mean()),
        'null_interpreted_K_rate': float(nul['K_interpreted_given_full_win'].mean()),
        'null_non_full_predictive_win_rate': float(1.0 - nul['full_predictive_win'].mean()),
        'decision_all_pass': bool(decision['pass'].all()),
        'boundary': 'Locked synthetic reproduction of null-aware specificity gate only; no biological, human EEG, microtubular, biophotonic, or OSM mechanism claim.'
    }
    with open(out/'tables'/'rung0o_pass_summary.json','w',encoding='utf-8') as f: json.dump(pass_summary,f,indent=2)
    T.to_csv(out/'tables'/'rung0o_trial_results.csv',index=False)
    penalized_losses.to_csv(out/'tables'/'rung0o_cv_model_losses.csv',index=False)
    winners.to_csv(out/'tables'/'rung0o_cv_winners_long.csv',index=False)
    gen_summary.to_csv(out/'tables'/'rung0o_generator_summary.csv',index=False)
    cv_summary.to_csv(out/'tables'/'rung0o_cv_win_summary.csv',index=False)
    decision.to_csv(out/'tables'/'rung0o_lock_decision_table.csv',index=False)
    print(json.dumps(pass_summary, indent=2))
if __name__ == '__main__': main()
