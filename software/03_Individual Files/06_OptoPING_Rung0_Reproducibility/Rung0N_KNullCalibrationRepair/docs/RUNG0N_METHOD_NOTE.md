# Rung 0N Method Note

Rung 0N implements the null-calibration repair recommended after Rung 0M.

## Required repairs

1. Higher-resolution null distributions.
2. Generator-specific K thresholds.
3. K significance interpreted only when full reciprocal prediction wins.
4. Penalty tuning to recover positive-control sensitivity.
5. Strong colored-noise and generic-hidden alternatives retained.

## Final lock rule

```text
Final lock = full reciprocal predictive win AND K significant against the appropriate null threshold.
```

This means K is not allowed to become a standalone positive claim.

## Primary interpretation

Rung 0N is a synthetic calibration gate. It tests whether the model-selection logic can distinguish loop-present synthetic data from empty-sky synthetic nulls. It is not a biological test.
