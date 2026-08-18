# External Reproducer Checklist

Before running:

- [ ] I did not edit the locked spec JSON.
- [ ] I did not edit the runner script.
- [ ] I did not alter the seed policy.
- [ ] I did not alter the parameter grids.
- [ ] I did not alter the alternative model list.
- [ ] I did not alter pass/fail thresholds.
- [ ] I created a fresh output directory.

After running:

- [ ] `reproduced_outputs/rung0j_pass_summary.json` exists.
- [ ] `reproduced_outputs/rung0j_trial_results.csv` exists.
- [ ] `reproduced_outputs/rung0j_cv_model_losses.csv` exists.
- [ ] `verify_external_rung0j_results.py` reports PASS or FAIL without manual edits.
- [ ] I report all deviations, including Python version, OS, package versions, and any errors.

Required note in external report:

> This is a synthetic reproduction of the locked Rung 0J protocol. It is not biological evidence and does not validate OSM as a mechanism.
