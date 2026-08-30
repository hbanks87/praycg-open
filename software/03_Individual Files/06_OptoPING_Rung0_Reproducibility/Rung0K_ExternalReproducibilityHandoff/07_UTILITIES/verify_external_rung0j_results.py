#!/usr/bin/env python3
"""Verify an external Rung 0J reproduction output directory against the frozen lock-in criteria.
This does not require byte-identical CSV formatting; it verifies locked spec hash and preregistered pass/fail metrics.
"""
import argparse, json, sys
from pathlib import Path
EXPECTED_LOCKED_SPEC_SHA256 = "d93f6146e4e77ffeffbdd5c133250fd6d474317d8af6c34c3354dd6b28756282"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('output_dir', help='Directory containing rung0j_pass_summary.json from the reproduction script')
    args = ap.parse_args()
    p = Path(args.output_dir) / 'rung0j_pass_summary.json'
    if not p.exists():
        raise SystemExit(f'Missing {p}')
    data = json.loads(p.read_text())
    locked_hash = data.get('locked_spec_sha256') or data.get('metrics',{}).get('locked_spec_sha256')
    n_trials = data.get('n_trials') or data.get('metrics',{}).get('n_trials')
    k15 = data.get('K_within_15_rate') or data.get('metrics',{}).get('K_within_15_rate')
    k10 = data.get('K_within_10_rate') or data.get('metrics',{}).get('K_within_10_rate')
    kmed = data.get('K_median_pct_error') or data.get('metrics',{}).get('K_median_pct_error')
    d20 = data.get('directional_20_pass_rate') or data.get('metrics',{}).get('directional_20_pass_rate')
    cv = data.get('full_model_cv_fold_win_rate') or data.get('metrics',{}).get('full_model_cv_fold_win_rate')
    checks = {
        'locked_spec_hash_ok': locked_hash == EXPECTED_LOCKED_SPEC_SHA256,
        'n_trials_60': int(n_trials) == 60,
        'K_15_rate_ge_0_90': float(k15) >= 0.90,
        'K_median_error_le_0_10': float(kmed) <= 0.10,
        'K_10_rate_ge_0_80': float(k10) >= 0.80,
        'directional_20_rate_ge_0_80': float(d20) >= 0.80,
        'full_model_cv_ge_0_80': float(cv) >= 0.80,
    }
    out = {'status':'PASS' if all(checks.values()) else 'FAIL', 'checks':checks, 'metrics': {'locked_spec_sha256':locked_hash,'n_trials':n_trials,'K_within_15_rate':k15,'K_within_10_rate':k10,'K_median_pct_error':kmed,'directional_20_pass_rate':d20,'full_model_cv_fold_win_rate':cv}}
    print(json.dumps(out, indent=2))
    return 0 if all(checks.values()) else 2
if __name__ == '__main__':
    raise SystemExit(main())
