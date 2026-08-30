# OSM / Opto-PING Rung 0J Locked Synthetic Protocol v0.1

## Status
This is a preregistered synthetic lock-in gate. It is designed to test whether the Rung 0I ridge-reduction design replicates on a fresh seed set without modifying the model, grids, perturbation order, thresholds, alternatives, or reporting template.

## Locked specification hash

`d93f6146e4e77ffeffbdd5c133250fd6d474317d8af6c34c3354dd6b28756282`

## Primary endpoint

`K = sqrt(eta_E * zeta_E)`

The directional parameters `eta_E` and `zeta_E` are secondary. They are interpreted only after `K` passes.

## Frozen true synthetic parameters

- eta_E = 4.0
- zeta_E = 180.0
- K = 26.832816
- fY = 7 Hz

## Frozen perturbation order

1. doublet_EY
2. orthogonal_trap
3. counterphase
4. lagged_E_to_Y
5. recovery_probe
6. lagged_Y_to_E


## Frozen pass/fail criteria

1. Primary K-lock: at least 90% of trials recover K within 15% of true K.
2. Median K precision: median K error <=10%.
3. Strict K secondary: at least 80% of trials recover K within 10%.
4. Held-out specificity: full reciprocal model wins at least 80% of leave-one-perturbation-family-out CV folds.
5. Directional secondary: eta_E and zeta_E are each within 20% in at least 80% of trials.
6. Alternative warning: no single non-full alternative may win more than 20% of held-out folds.

## Boundary
Synthetic identifiability only. This gate does not prove OSM, microtubular memory, LTP, dendritic spine growth, quantum memory, or a human EEG mechanism.
