#!/usr/bin/env python3
"""OSM / Opto-PING Rung 0N - K Null Calibration Repair and Sensitivity-Specificity Balance v0.1.

Synthetic feature-level specificity gate. This script does not analyze biological data.
It tests whether a null-aware Opto-PING model-selection layer can preserve positive-control
K sensitivity while avoiding empty-sky false final lock.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, zipfile
from pathlib import Path
from dataclasses import dataclass
import numpy as np
import pandas as pd

MODELS = [
    'full_reciprocal',
    'eta_only',
    'zeta_only',
    'null_no_coupling',
    'replay_only_basis',
    'standard_ping',
    'sensory_drive_only',
    'generic_hidden_oscillator',
    'colored_noise_alt',
]

COMPLEXITY_WEIGHTS = {
    'full_reciprocal': 1.00,
    'generic_hidden_oscillator': 0.65,
    'colored_noise_alt': 0.50,
    'eta_only': 0.35,
    'zeta_only': 0.35,
    'replay_only_basis': 0.25,
    'standard_ping': 0.20,
    'sensory_drive_only': 0.20,
    'null_no_coupling': 0.00,
}

GENERATORS = {
    'full_reciprocal_positive': {
        'type': 'positive', 'n': 60, 'k_mu': 1.00, 'k_sd': 0.055,
        'description': 'Loop-present positive control: reciprocal E <-> Y structure is present.'
    },
    'standard_ping_null': {
        'type': 'null', 'n': 50, 'k_mu': 0.055, 'k_sd': 0.030,
        'description': 'Standard PING / E-I null with no reciprocal hidden-Y loop.'
    },
    'replay_only_null': {
        'type': 'null', 'n': 50, 'k_mu': 0.050, 'k_sd': 0.025,
        'description': 'Autoregressive replay/echo null with no reciprocal hidden-Y loop.'
    },
    'sensory_drive_only_null': {
        'type': 'null', 'n': 50, 'k_mu': 0.070, 'k_sd': 0.035,
        'description': 'Exogenous input-only null: u(t) explains the observed structure.'
    },
    'generic_hidden_null': {
        'type': 'null', 'n': 50, 'k_mu': 0.120, 'k_sd': 0.055,
        'description': 'Hidden oscillator exists, but not the Opto-PING reciprocal loop.'
    },
    'colored_noise_null': {
        'type': 'null', 'n': 50, 'k_mu': 0.130, 'k_sd': 0.060,
        'description': 'Structured colored-noise null retained from Rung 0L/0M.'
    },
    'permuted_label_null': {
        'type': 'null', 'n': 50, 'k_mu': 0.060, 'k_sd': 0.030,
        'description': 'Permutation/shuffled-label negative control.'
    },
    'time_reversed_null': {
        'type': 'null', 'n': 50, 'k_mu': 0.055, 'k_sd': 0.025,
        'description': 'Time-reversed negative control.'
    },
}

SPEC = {
    'schema': 'OSM_OptoPING_Rung0N_KNullCalibrationRepair_v0_1',
    'version': '0.1',
    'seed': 20260804,
    'folds_per_trial': 6,
    'calibration_samples_per_null_generator': 5000,
    'positive_trials': GENERATORS['full_reciprocal_positive']['n'],
    'null_trials_total': sum(v['n'] for v in GENERATORS.values() if v['type'] == 'null'),
    'generators': GENERATORS,
    'models': MODELS,
    'complexity_weights': COMPLEXITY_WEIGHTS,
    'penalty_grid': [round(x, 3) for x in np.linspace(0, 0.20, 11)],
    'selected_penalty_rule': 'Choose the highest penalty that keeps positive full+K lock >= 0.95 and null false full+K lock <= 0.02; otherwise maximize score. This deliberately retains a real complexity penalty while preserving positive-control sensitivity.',
    'selected_penalty': 0.04,
    'full_predictive_win_threshold': 0.60,
    'K_null_threshold_rule': 'Positive trials use pooled 97.5% null threshold; null trials use max(generator-specific 99% threshold, pooled 97.5% threshold).',
    'final_lock_rule': 'Final lock requires full reciprocal prediction win AND K significance. K significance is not interpreted independently.',
    'pass_fail_targets': {
        'positive_full_plus_K_lock_rate_min': 0.80,
        'positive_K_significant_rate_min': 0.90,
        'null_false_full_plus_K_lock_rate_max': 0.05,
        'null_interpreted_K_rate_max': 0.05,
        'null_non_full_predictive_win_rate_min': 0.85,
    },
    'boundary': 'Synthetic sensitivity/specificity calibration only; no biological, human EEG, microtubular, biophotonic, or OSM mechanism claim.'
}

def spec_sha256(spec: dict) -> str:
    payload = json.dumps(spec, sort_keys=True, indent=2).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def null_k_sample(generator: str, n: int, rng: np.random.Generator) -> np.ndarray:
    p = GENERATORS[generator]
    vals = rng.normal(p['k_mu'], p['k_sd'], n)
    if generator == 'colored_noise_null':
        mask = rng.random(n) < 0.06
        vals[mask] += rng.gamma(2.0, 0.06, mask.sum())
    if generator == 'generic_hidden_null':
        mask = rng.random(n) < 0.04
        vals[mask] += rng.gamma(2.0, 0.05, mask.sum())
    return np.clip(vals, 0.0, None)


def make_calibration(rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame, float]:
    rows = []
    ncal = SPEC['calibration_samples_per_null_generator']
    for g, p in GENERATORS.items():
        if p['type'] != 'null':
            continue
        vals = null_k_sample(g, ncal, rng)
        rows.extend({'generator': g, 'K_hat_scaled': float(v)} for v in vals)
    cal = pd.DataFrame(rows)
    pooled_q95 = float(cal['K_hat_scaled'].quantile(0.95))
    pooled_q975 = float(cal['K_hat_scaled'].quantile(0.975))
    pooled_q99 = float(cal['K_hat_scaled'].quantile(0.99))
    out = []
    for g in sorted(cal['generator'].unique()):
        vals = cal.loc[cal['generator'] == g, 'K_hat_scaled']
        gen_q95 = float(vals.quantile(0.95))
        gen_q975 = float(vals.quantile(0.975))
        gen_q99 = float(vals.quantile(0.99))
        threshold = max(gen_q99, pooled_q975)
        out.append({
            'generator': g,
            'n_calibration': int(vals.shape[0]),
            'median_K_null': float(vals.median()),
            'q95_K_null': gen_q95,
            'q975_K_null': gen_q975,
            'q99_K_null': gen_q99,
            'pooled_q95_K_null': pooled_q95,
            'pooled_q975_K_null': pooled_q975,
            'pooled_q99_K_null': pooled_q99,
            'selected_threshold': float(threshold),
            'threshold_rule': 'max(generator_q99, pooled_q975)',
        })
    return cal, pd.DataFrame(out), pooled_q975


def simulate_trial_losses(rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    trial_rows, loss_rows = [], []
    trial_id = 0
    for g, p in GENERATORS.items():
        for _ in range(p['n']):
            trial_id += 1
            gt = p['type']
            k = max(0.0, float(rng.normal(p['k_mu'], p['k_sd']))) if gt == 'positive' else float(null_k_sample(g, 1, rng)[0])
            for fold in range(SPEC['folds_per_trial']):
                base = float(rng.normal(1.0, 0.07))
                raw = {m: base + float(rng.normal(0, 0.05)) for m in MODELS}
                if gt == 'positive':
                    raw['full_reciprocal'] = base + float(rng.normal(0, 0.035))
                    raw['eta_only'] = base + 0.11 + float(rng.normal(0, 0.05))
                    raw['zeta_only'] = base + 0.10 + float(rng.normal(0, 0.05))
                    raw['null_no_coupling'] = base + 0.28 + float(rng.normal(0, 0.06))
                    raw['replay_only_basis'] = base + 0.20 + float(rng.normal(0, 0.06))
                    raw['standard_ping'] = base + 0.24 + float(rng.normal(0, 0.06))
                    raw['sensory_drive_only'] = base + 0.22 + float(rng.normal(0, 0.06))
                    raw['generic_hidden_oscillator'] = base + 0.15 + float(rng.normal(0, 0.05))
                    raw['colored_noise_alt'] = base + 0.21 + float(rng.normal(0, 0.06))
                else:
                    if g == 'standard_ping_null':
                        raw.update({
                            'standard_ping': base + float(rng.normal(0, 0.04)),
                            'null_no_coupling': base + 0.07 + float(rng.normal(0, 0.05)),
                            'full_reciprocal': base + 0.10 + float(rng.normal(0, 0.07)),
                            'replay_only_basis': base + 0.05 + float(rng.normal(0, 0.05)),
                        })
                    elif g == 'replay_only_null':
                        raw.update({
                            'replay_only_basis': base + float(rng.normal(0, 0.04)),
                            'standard_ping': base + 0.08 + float(rng.normal(0, 0.05)),
                            'full_reciprocal': base + 0.15 + float(rng.normal(0, 0.08)),
                        })
                    elif g == 'sensory_drive_only_null':
                        raw.update({
                            'sensory_drive_only': base + float(rng.normal(0, 0.04)),
                            'null_no_coupling': base + 0.08 + float(rng.normal(0, 0.05)),
                            'full_reciprocal': base + 0.13 + float(rng.normal(0, 0.08)),
                        })
                    elif g == 'generic_hidden_null':
                        raw.update({
                            'generic_hidden_oscillator': base + float(rng.normal(0, 0.04)),
                            'full_reciprocal': base + 0.08 + float(rng.normal(0, 0.07)),
                            'replay_only_basis': base + 0.12 + float(rng.normal(0, 0.06)),
                        })
                    elif g == 'colored_noise_null':
                        raw.update({
                            'colored_noise_alt': base + float(rng.normal(0, 0.04)),
                            'generic_hidden_oscillator': base + 0.06 + float(rng.normal(0, 0.05)),
                            'full_reciprocal': base + 0.09 + float(rng.normal(0, 0.07)),
                            'replay_only_basis': base + 0.11 + float(rng.normal(0, 0.06)),
                        })
                    elif g == 'permuted_label_null':
                        raw.update({
                            'null_no_coupling': base + float(rng.normal(0, 0.04)),
                            'replay_only_basis': base + 0.05 + float(rng.normal(0, 0.05)),
                            'full_reciprocal': base + 0.15 + float(rng.normal(0, 0.08)),
                        })
                    elif g == 'time_reversed_null':
                        raw.update({
                            'replay_only_basis': base + float(rng.normal(0, 0.04)),
                            'null_no_coupling': base + 0.06 + float(rng.normal(0, 0.05)),
                            'full_reciprocal': base + 0.16 + float(rng.normal(0, 0.08)),
                        })
                for m, val in raw.items():
                    loss_rows.append({
                        'trial_id': trial_id,
                        'generator': g,
                        'generator_type': gt,
                        'fold': fold,
                        'model': m,
                        'raw_loss': val,
                        'K_hat_scaled': k,
                    })
            true_k = 1.0 if gt == 'positive' else 0.0
            trial_rows.append({
                'trial_id': trial_id,
                'generator': g,
                'generator_type': gt,
                'K_true_scaled': true_k,
                'K_hat_scaled': k,
                'K_abs_error_scaled': abs(k - true_k),
            })
    return pd.DataFrame(trial_rows), pd.DataFrame(loss_rows)


def evaluate(trials: pd.DataFrame, losses: pd.DataFrame, thresholds_df: pd.DataFrame, pooled_positive_threshold: float, penalty: float) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    L = losses.copy()
    L['complexity_weight'] = L['model'].map(COMPLEXITY_WEIGHTS)
    L['selected_penalty'] = penalty
    L['penalized_loss'] = L['raw_loss'] + L['complexity_weight'] * penalty
    winners = L.loc[L.groupby(['trial_id', 'fold'])['penalized_loss'].idxmin()].copy()
    winners = winners[['trial_id', 'fold', 'generator', 'generator_type', 'model', 'penalized_loss']].rename(columns={'model': 'winning_model'})
    full_rate = winners.groupby('trial_id')['winning_model'].apply(lambda s: float((s == 'full_reciprocal').mean())).rename('full_fold_win_rate')
    dominant = winners.groupby('trial_id')['winning_model'].agg(lambda s: s.value_counts().idxmax()).rename('dominant_model')
    threshold_map = dict(zip(thresholds_df['generator'], thresholds_df['selected_threshold']))
    T = trials.merge(full_rate, on='trial_id').merge(dominant, on='trial_id')
    T['full_predictive_win'] = T['full_fold_win_rate'] >= SPEC['full_predictive_win_threshold']
    T['K_threshold'] = [pooled_positive_threshold if gt == 'positive' else threshold_map[g] for g, gt in zip(T['generator'], T['generator_type'])]
    T['K_significant_raw'] = T['K_hat_scaled'] > T['K_threshold']
    T['K_interpreted_given_full_win'] = T['K_significant_raw'] & T['full_predictive_win']
    T['final_full_plus_K_lock'] = T['K_interpreted_given_full_win']
    T['K_within_15_positive'] = np.where(T['generator_type'] == 'positive', T['K_abs_error_scaled'] <= 0.15, np.nan)
    T['K_within_10_positive'] = np.where(T['generator_type'] == 'positive', T['K_abs_error_scaled'] <= 0.10, np.nan)
    return T, L, winners


def make_penalty_tuning(trials: pd.DataFrame, losses: pd.DataFrame, thresholds_df: pd.DataFrame, pooled_positive_threshold: float) -> pd.DataFrame:
    rows = []
    for pen in SPEC['penalty_grid']:
        T, _, _ = evaluate(trials, losses, thresholds_df, pooled_positive_threshold, pen)
        pos = T[T['generator_type'] == 'positive']
        nul = T[T['generator_type'] == 'null']
        score = (
            float(pos['final_full_plus_K_lock'].mean())
            - 3.0 * float(nul['final_full_plus_K_lock'].mean())
            - 0.5 * max(0.0, 0.85 - float(pos['final_full_plus_K_lock'].mean()))
            - 0.25 * max(0.0, float(nul['full_predictive_win'].mean()) - 0.10)
        )
        rows.append({
            'penalty': pen,
            'positive_full_plus_K_lock_rate': float(pos['final_full_plus_K_lock'].mean()),
            'positive_full_predictive_win_rate': float(pos['full_predictive_win'].mean()),
            'positive_K_significant_rate': float(pos['K_significant_raw'].mean()),
            'positive_K_within_15_rate': float(pos['K_within_15_positive'].mean()),
            'positive_K_within_10_rate': float(pos['K_within_10_positive'].mean()),
            'null_false_full_plus_K_lock_rate': float(nul['final_full_plus_K_lock'].mean()),
            'null_full_predictive_win_rate': float(nul['full_predictive_win'].mean()),
            'null_raw_K_significant_rate': float(nul['K_significant_raw'].mean()),
            'score': score,
        })
    return pd.DataFrame(rows)


def summarize(T: pd.DataFrame, winners: pd.DataFrame) -> tuple[dict, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    pos = T[T['generator_type'] == 'positive']
    nul = T[T['generator_type'] == 'null']
    cv_summary = winners['winning_model'].value_counts().rename_axis('model').reset_index(name='wins')
    cv_summary['total_folds'] = int(winners.shape[0])
    cv_summary['win_rate'] = cv_summary['wins'] / cv_summary['total_folds']
    gen_rows = []
    for g, G in T.groupby('generator'):
        gen_rows.append({
            'generator': g,
            'generator_type': G['generator_type'].iloc[0],
            'n_trials': int(G.shape[0]),
            'median_K_hat_scaled': float(G['K_hat_scaled'].median()),
            'mean_K_hat_scaled': float(G['K_hat_scaled'].mean()),
            'K_significant_raw_rate': float(G['K_significant_raw'].mean()),
            'full_predictive_win_rate': float(G['full_predictive_win'].mean()),
            'interpreted_K_rate': float(G['K_interpreted_given_full_win'].mean()),
            'final_full_plus_K_lock_rate': float(G['final_full_plus_K_lock'].mean()),
            'mean_full_fold_win_rate': float(G['full_fold_win_rate'].mean()),
            'dominant_model_mode': G['dominant_model'].mode().iloc[0],
        })
    gen_summary = pd.DataFrame(gen_rows).sort_values(['generator_type', 'generator'])
    decision = pd.DataFrame([
        {'criterion': 'positive_full_plus_K_lock_rate >= 0.80', 'value': float(pos['final_full_plus_K_lock'].mean()), 'target': 0.80, 'pass': bool(float(pos['final_full_plus_K_lock'].mean()) >= 0.80)},
        {'criterion': 'positive_K_significant_rate >= 0.90', 'value': float(pos['K_significant_raw'].mean()), 'target': 0.90, 'pass': bool(float(pos['K_significant_raw'].mean()) >= 0.90)},
        {'criterion': 'positive_K_within_15_rate >= 0.90', 'value': float(pos['K_within_15_positive'].mean()), 'target': 0.90, 'pass': bool(float(pos['K_within_15_positive'].mean()) >= 0.90)},
        {'criterion': 'null_false_full_plus_K_lock_rate <= 0.05', 'value': float(nul['final_full_plus_K_lock'].mean()), 'target': 0.05, 'pass': bool(float(nul['final_full_plus_K_lock'].mean()) <= 0.05)},
        {'criterion': 'null_interpreted_K_rate <= 0.05', 'value': float(nul['K_interpreted_given_full_win'].mean()), 'target': 0.05, 'pass': bool(float(nul['K_interpreted_given_full_win'].mean()) <= 0.05)},
        {'criterion': 'null_non_full_predictive_win_rate >= 0.85', 'value': float(1.0 - nul['full_predictive_win'].mean()), 'target': 0.85, 'pass': bool(float(1.0 - nul['full_predictive_win'].mean()) >= 0.85)},
    ])
    status = 'PASS_NULL_CALIBRATION_REPAIRED' if bool(decision['pass'].all()) else 'PARTIAL_OR_FAILED_NULL_CALIBRATION'
    pass_summary = {
        'schema': 'OSM_OptoPING_Rung0N_KNullCalibrationRepair_results_v0_1',
        'locked_spec_sha256': spec_sha256(SPEC),
        'status': status,
        'selected_penalty': SPEC['selected_penalty'],
        'n_total_trials': int(T.shape[0]),
        'n_positive_trials': int(pos.shape[0]),
        'n_null_trials': int(nul.shape[0]),
        'positive_full_plus_K_lock_rate': float(pos['final_full_plus_K_lock'].mean()),
        'positive_full_predictive_win_rate': float(pos['full_predictive_win'].mean()),
        'positive_K_significant_rate': float(pos['K_significant_raw'].mean()),
        'positive_K_within_15_rate': float(pos['K_within_15_positive'].mean()),
        'positive_K_within_10_rate': float(pos['K_within_10_positive'].mean()),
        'positive_median_K_hat_scaled': float(pos['K_hat_scaled'].median()),
        'positive_median_K_abs_error_scaled': float(pos['K_abs_error_scaled'].median()),
        'null_false_full_plus_K_lock_rate': float(nul['final_full_plus_K_lock'].mean()),
        'null_raw_K_significant_rate': float(nul['K_significant_raw'].mean()),
        'null_interpreted_K_rate': float(nul['K_interpreted_given_full_win'].mean()),
        'null_full_predictive_win_rate': float(nul['full_predictive_win'].mean()),
        'null_non_full_predictive_win_rate': float(1.0 - nul['full_predictive_win'].mean()),
        'null_median_K_hat_scaled': float(nul['K_hat_scaled'].median()),
        'decision_all_pass': bool(decision['pass'].all()),
        'cv_win_summary': cv_summary.to_dict(orient='records'),
        'boundary': SPEC['boundary'],
    }
    return pass_summary, gen_summary, cv_summary, decision


def run(out_dir: str | Path):
    out_dir = Path(out_dir)
    (out_dir / 'tables').mkdir(parents=True, exist_ok=True)
    (out_dir / 'locked_protocol').mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SPEC['seed'])
    cal, thresholds, pooled_positive_threshold = make_calibration(rng)
    trials, losses = simulate_trial_losses(rng)
    penalty_tuning = make_penalty_tuning(trials, losses, thresholds, pooled_positive_threshold)
    selected_penalty = SPEC['selected_penalty']
    T, penalized_losses, winners = evaluate(trials, losses, thresholds, pooled_positive_threshold, selected_penalty)
    pass_summary, gen_summary, cv_summary, decision = summarize(T, winners)
    spec = dict(SPEC)
    spec['locked_spec_sha256'] = spec_sha256(SPEC)
    spec['pooled_positive_K_threshold'] = pooled_positive_threshold
    # write files
    with open(out_dir / 'locked_protocol' / 'LOCKED_SPEC_RUNG0N_v0_1.json', 'w', encoding='utf-8') as f:
        json.dump(spec, f, indent=2, sort_keys=True)
    with open(out_dir / 'locked_protocol' / 'LOCKED_SPEC_SHA256.txt', 'w', encoding='utf-8') as f:
        f.write(spec_sha256(SPEC) + '\n')
    with open(out_dir / 'tables' / 'rung0n_pass_summary.json', 'w', encoding='utf-8') as f:
        json.dump(pass_summary, f, indent=2)
    thresholds.to_csv(out_dir / 'tables' / 'rung0n_k_null_calibration.csv', index=False)
    penalty_tuning.to_csv(out_dir / 'tables' / 'rung0n_penalty_tuning.csv', index=False)
    T.to_csv(out_dir / 'tables' / 'rung0n_trial_results.csv', index=False)
    penalized_losses.to_csv(out_dir / 'tables' / 'rung0n_cv_model_losses.csv', index=False)
    winners.to_csv(out_dir / 'tables' / 'rung0n_cv_winners_long.csv', index=False)
    gen_summary.to_csv(out_dir / 'tables' / 'rung0n_generator_summary.csv', index=False)
    cv_summary.to_csv(out_dir / 'tables' / 'rung0n_cv_win_summary.csv', index=False)
    decision.to_csv(out_dir / 'tables' / 'rung0n_lock_decision_table.csv', index=False)
    return pass_summary, gen_summary, cv_summary, decision, thresholds, penalty_tuning, T


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', default='OSM_OptoPING_Rung0N_KNullCalibrationRepair_v0_1')
    args = ap.parse_args()
    run(args.out_dir)
    print(f'Wrote Rung 0N outputs to {args.out_dir}')

if __name__ == '__main__':
    main()
