# Internal Clean-Room Replay Result

This was a fresh-directory replay of the locked Rung 0J script, performed as a handoff dry run.

## Status

```text
PASS - internal clean-room replay
```

## Locked spec

```text
d93f6146e4e77ffeffbdd5c133250fd6d474317d8af6c34c3354dd6b28756282
```

## Metrics

| Metric | Clean-room replay |
|---|---:|
| n_trials | 60 |
| K within 15% rate | 1.000 |
| K within 10% rate | 1.000 |
| Median K percent error | 0.028175 |
| Directional eta/zeta <=20% rate | 1.000 |
| Full model CV fold win rate | 0.872222 |

## CV winners

```json
{
  "full_reciprocal": 314,
  "replay_only_basis": 20,
  "zeta_only": 14,
  "eta_only": 9,
  "generic_hidden_oscillator": 3
}
```

## Interpretation

The clean-room replay reproduces the pass/fail metrics of the Rung 0J lock-in. It does not constitute external reproduction because it was not performed by an independent person or on a separate physical machine.
