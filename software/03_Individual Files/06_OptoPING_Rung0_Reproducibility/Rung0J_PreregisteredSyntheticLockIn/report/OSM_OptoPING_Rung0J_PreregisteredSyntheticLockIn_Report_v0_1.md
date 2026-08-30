# OSM / Opto-PING Rung 0J - Preregistered Synthetic Lock-In and External Reproducibility Pack v0.1

## Executive verdict

**Rung 0J is a synthetic lock-in pass for the primary composite endpoint K.**

This gate froze the model equations, parameter grids, perturbation order, K-lock criteria, failure thresholds, random-seed policy, alternative models, and reporting template before running a fresh seed set.

The locked specification SHA-256 was:

`d93f6146e4e77ffeffbdd5c133250fd6d474317d8af6c34c3354dd6b28756282`

## Locked design

Primary estimand:

```text
K = sqrt(eta_E * zeta_E)
K_loop = eta_E * zeta_E
```

True synthetic parameters:

```text
eta_E = 4.0
zeta_E = 180.0
K = 26.832816
```

Frozen perturbation order:

1. `doublet_EY`
2. `orthogonal_trap`
3. `counterphase`
4. `lagged_E_to_Y`
5. `recovery_probe`
6. `lagged_Y_to_E`


Fresh seed policy:

```text
seeds = 910001 through 910060
n = 60
```

## Primary lock-in results

| Metric | Result |
|---|---:|
| K within 15% rate | 1.000 |
| K within 10% rate | 1.000 |
| Median K percent error | 0.028 |
| Mean K percent error | 0.031 |
| Full reciprocal held-out CV fold win rate | 0.872 |
| Per-trial full-CV >=80% rate | 0.833 |
| Directional eta/zeta <=20% rate | 1.000 |
| Directional eta/zeta <=15% rate | 1.000 |

## Lock decision table

| criterion                     |   observed | threshold                                   | pass   | interpretation                                                                         |
|:------------------------------|-----------:|:--------------------------------------------|:-------|:---------------------------------------------------------------------------------------|
| Primary K-lock power          |  1         | >=0.90 trials K error <=15%                 | True   | Primary composite endpoint stability.                                                  |
| Median K precision            |  0.0281747 | <=0.10 median K error                       | True   | Composite endpoint precision.                                                          |
| Strict K-lock secondary       |  1         | >=0.80 trials K error <=10%                 | True   | Stricter composite endpoint check.                                                     |
| Held-out specificity          |  0.872222  | >=0.80 full reciprocal CV fold win rate     | True   | Tests against replay-only, eta-only, zeta-only, generic hidden, and null alternatives. |
| Directional secondary         |  1         | >=0.80 trials eta and zeta each <=20% error | True   | Directional decomposition may be reported after K-lock, with ridge caveat.             |
| Alternative dominance warning |  0.0555556 | <=0.20 for any single non-full alternative  | True   | No single alternative should dominate held-out folds.                                  |

## Held-out model comparison

| model                     |   wins |   total_folds |   win_rate |
|:--------------------------|-------:|--------------:|-----------:|
| full_reciprocal           |    314 |           360 | 0.872222   |
| replay_only_basis         |     20 |           360 | 0.0555556  |
| zeta_only                 |     14 |           360 | 0.0388889  |
| eta_only                  |      9 |           360 | 0.025      |
| generic_hidden_oscillator |      3 |           360 | 0.00833333 |

## Profile-likelihood ridge summary

|   representative_seed | criterion                                       |   min_loss |   near_cell_count |   eta_width |   zeta_width |   K_width |   best_eta |   best_zeta |   best_K |   true_eta |   true_zeta |   true_K | ridge_interpretation                                                                                                                    |
|----------------------:|:------------------------------------------------|-----------:|------------------:|------------:|-------------:|----------:|-----------:|------------:|---------:|-----------:|------------:|---------:|:----------------------------------------------------------------------------------------------------------------------------------------|
|                910008 | loss <= min_loss + max(1.0, 0.05*abs(min_loss)) |    2.41032 |                31 |        0.75 |           40 |   4.35818 |          4 |         170 |  26.0768 |          4 |         180 |  26.8328 | Profile surface is locally constrained enough for K-lock in this synthetic gate; eta/zeta separation remains secondary and conditional. |

## Interpretation

The fresh seed set replicated the central Rung 0I correction: the primary endpoint should be the composite reciprocal-coupling parameter `K`, not the immediate independent interpretation of `eta_E` and `zeta_E`.

The full reciprocal model also passed the held-out perturbation-family model-comparison criterion. No single non-full alternative exceeded the preregistered dominance warning threshold.

The directional parameters `eta_E` and `zeta_E` performed well in this locked toy setting, but the framework should still treat them as secondary conditional endpoints because prior Rung 0C-0F gates showed that directional decomposition can become ridge-confounded under hidden-Y, proxy-imperfect, or alternative-model stress.

## Boundary

This is synthetic identifiability work only. It does not prove OSM, microtubular memory, LTP, dendritic spine growth, quantum memory, or a human EEG mechanism.

## Reproducibility

Run:

```bash
pip install -r requirements.txt
python scripts/run_osm_opto_ping_rung0j_preregistered_lockin_v0_1.py --out-dir reproduced_rung0j
```

The script recomputes the locked specification hash and exits if the embedded locked specification has changed.
