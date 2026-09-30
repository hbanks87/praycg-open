> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Final corrected full Run 1 comparison. The two-sample eyes-closed/early/proxy-touched subgroup is insufficient for interpretation; historical numeric values are preserved with this warning.

# Full corrected Zuna comparison — private development report

Post-hoc • one historical BENCH recording • all eight blocks • all 104 model contexts.

## Outcome

The primary production endpoint gave Zuna **higher mean electrode-normalized error** than interpolation: **1.176 versus 0.675**. Lower is better. This is a descriptive within-recording result, not validated denoising or generalizable model superiority.

Scored support: 102,456 original-mask samples (400.219 sample-equivalent seconds). All declared conditions, channels and strata remain visible; none was removed because it favored either method.

## Both frozen endpoints

| Endpoint | Spline NMSE | Zuna NMSE | Spline pooled RMSE µV | Zuna pooled RMSE µV |
| --- | --- | --- | --- | --- |
| Primary: production final filter | 0.675 | 1.176 | 5.583 | 7.366 |
| Companion: before comparison filter | 0.666 | 2.048 | 5.726 | 9.896 |

NMSE is MSE divided by each electrode’s population variance, then averaged across the four electrodes. Pooled RMSE weights all scored samples and electrodes equally. The pooled score is not the mean of block scores. A changing target variance can change NMSE independently of absolute error.

The final filter is applied independently within each block, never to stitched discontinuous samples. It applies the same operator to each branch but not the same total linear-filter history: measured and spline signals already underwent preparation filtering. Both endpoints are mandatory; we do not choose whichever favors Zuna.

## Every electrode

| Endpoint | Electrode | Spline NMSE | Zuna NMSE | Spline RMSE | Zuna RMSE | Spline r | Zuna r |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Primary | F3 | 0.301 | 0.897 | 4.695 | 8.109 | 0.871 | 0.551 |
| Primary | F4 | 0.902 | 0.819 | 7.002 | 6.673 | 0.713 | 0.591 |
| Primary | P3 | 0.724 | 1.493 | 4.951 | 7.109 | 0.631 | 0.460 |
| Primary | P4 | 0.773 | 1.493 | 5.395 | 7.495 | 0.655 | 0.462 |
| Companion | F3 | 0.295 | 1.450 | 4.817 | 10.683 | 0.874 | 0.449 |
| Companion | F4 | 0.877 | 0.981 | 7.151 | 7.566 | 0.717 | 0.548 |
| Companion | P3 | 0.720 | 2.501 | 5.094 | 9.493 | 0.631 | 0.362 |
| Companion | P4 | 0.772 | 3.260 | 5.553 | 11.412 | 0.650 | 0.322 |

## Every block

### Primary

| Block / condition | Scored seconds | Spline NMSE | Zuna NMSE | Spline RMSE | Zuna RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 / eyes_open | 50.027 | 0.819 | 1.161 | 6.099 | 7.300 |
| 2 / eyes_closed | 50.031 | 0.648 | 0.529 | 5.162 | 4.494 |
| 3 / eyes_closed | 50.016 | 0.577 | 0.470 | 4.843 | 4.371 |
| 4 / eyes_open | 50.027 | 0.429 | 2.255 | 5.098 | 11.316 |
| 5 / eyes_closed | 50.031 | 1.022 | 0.683 | 5.524 | 4.490 |
| 6 / eyes_open | 50.027 | 0.461 | 0.927 | 5.780 | 8.166 |
| 7 / eyes_open | 50.027 | 0.875 | 2.103 | 6.348 | 10.178 |
| 8 / eyes_closed | 50.031 | 1.188 | 0.863 | 5.644 | 4.788 |

### Companion

| Block / condition | Scored seconds | Spline NMSE | Zuna NMSE | Spline RMSE | Zuna RMSE |
| --- | --- | --- | --- | --- | --- |
| 1 / eyes_open | 50.027 | 0.782 | 4.212 | 6.224 | 13.246 |
| 2 / eyes_closed | 50.031 | 0.608 | 0.508 | 5.285 | 4.628 |
| 3 / eyes_closed | 50.016 | 0.585 | 0.481 | 4.927 | 4.473 |
| 4 / eyes_open | 50.027 | 0.431 | 3.283 | 5.258 | 13.840 |
| 5 / eyes_closed | 50.031 | 1.020 | 0.697 | 5.619 | 4.617 |
| 6 / eyes_open | 50.027 | 0.454 | 1.372 | 5.906 | 10.191 |
| 7 / eyes_open | 50.027 | 0.868 | 4.303 | 6.581 | 15.009 |
| 8 / eyes_closed | 50.031 | 1.205 | 0.884 | 5.822 | 4.961 |

*Figure omitted from this public report-only copy.*

## All predeclared descriptive strata

Every row is an intersection with the unchanged original scoring mask. Early means seconds 5–20; late means from second 20 to that mask’s end. Historical proxy flags are carried unchanged from the previous audit. Rows overlap and are not independent replications. “Untouched” does not mean clean. Small or absent strata are retained as such.

### Primary: all strata

| Stratum | Seconds | Spline NMSE | Zuna NMSE | Spline RMSE | Zuna RMSE |
| --- | --- | --- | --- | --- | --- |
| all / all / all | 400.219 | 0.675 | 1.176 | 5.583 | 7.366 |
| all / all / proxy_local | 43.672 | 0.225 | 0.780 | 6.490 | 12.328 |
| all / all / proxy_outside_local | 356.547 | 1.045 | 1.496 | 5.462 | 6.502 |
| all / all / proxy_context_touched | 160.219 | 0.490 | 1.528 | 5.798 | 10.199 |
| all / all / proxy_context_untouched | 240.000 | 1.006 | 0.723 | 5.435 | 4.585 |
| all / early_5_20 / all | 120.004 | 0.555 | 1.186 | 5.557 | 8.168 |
| all / early_5_20 / proxy_local | 15.832 | 0.167 | 0.720 | 6.477 | 13.799 |
| all / early_5_20 / proxy_outside_local | 104.172 | 1.048 | 1.740 | 5.404 | 6.922 |
| all / early_5_20 / proxy_context_touched | 50.012 | 0.356 | 1.453 | 5.699 | 11.496 |
| all / early_5_20 / proxy_context_untouched | 69.992 | 1.035 | 0.699 | 5.454 | 4.466 |
| all / late_from20_to_original_mask_end / all | 280.215 | 0.743 | 1.172 | 5.594 | 6.994 |
| all / late_from20_to_original_mask_end / proxy_local | 27.840 | 0.275 | 0.835 | 6.497 | 11.407 |
| all / late_from20_to_original_mask_end / proxy_outside_local | 252.375 | 1.044 | 1.401 | 5.485 | 6.321 |
| all / late_from20_to_original_mask_end / proxy_context_touched | 110.207 | 0.581 | 1.580 | 5.842 | 9.553 |
| all / late_from20_to_original_mask_end / proxy_context_untouched | 170.008 | 0.995 | 0.733 | 5.427 | 4.633 |
| eyes_open / all / all | 200.109 | 0.607 | 1.552 | 5.850 | 9.376 |
| eyes_open / all / proxy_local | 37.977 | 0.221 | 0.826 | 6.634 | 13.098 |
| eyes_open / all / proxy_outside_local | 162.133 | 1.323 | 2.822 | 5.651 | 8.265 |
| eyes_open / all / proxy_context_touched | 140.109 | 0.489 | 1.663 | 5.864 | 10.770 |
| eyes_open / all / proxy_context_untouched | 60.000 | 1.493 | 0.979 | 5.818 | 4.723 |
| eyes_open / early_5_20 / all | 60.000 | 0.406 | 1.434 | 5.639 | 10.645 |
| eyes_open / early_5_20 / proxy_local | 15.832 | 0.167 | 0.720 | 6.477 | 13.799 |
| eyes_open / early_5_20 / proxy_outside_local | 44.168 | 1.225 | 3.731 | 5.307 | 9.256 |
| eyes_open / early_5_20 / proxy_context_touched | 50.004 | 0.356 | 1.453 | 5.699 | 11.497 |
| eyes_open / early_5_20 / proxy_context_untouched | 9.996 | 1.897 | 1.196 | 5.329 | 4.344 |
| eyes_open / late_from20_to_original_mask_end / all | 140.109 | 0.746 | 1.637 | 5.938 | 8.776 |
| eyes_open / late_from20_to_original_mask_end / proxy_local | 22.145 | 0.275 | 0.937 | 6.744 | 12.573 |
| eyes_open / late_from20_to_original_mask_end / proxy_outside_local | 117.965 | 1.364 | 2.525 | 5.774 | 7.862 |
| eyes_open / late_from20_to_original_mask_end / proxy_context_touched | 90.105 | 0.599 | 1.838 | 5.953 | 10.345 |
| eyes_open / late_from20_to_original_mask_end / proxy_context_untouched | 50.004 | 1.443 | 0.953 | 5.911 | 4.795 |
| eyes_closed / all / all | 200.109 | 0.814 | 0.608 | 5.303 | 4.539 |
| eyes_closed / all / proxy_local | 5.695 | 0.279 | 0.217 | 5.430 | 4.632 |
| eyes_closed / all / proxy_outside_local | 194.414 | 0.876 | 0.651 | 5.299 | 4.536 |
| eyes_closed / all / proxy_context_touched | 20.109 | 0.500 | 0.379 | 5.315 | 4.541 |
| eyes_closed / all / proxy_context_untouched | 180.000 | 0.891 | 0.661 | 5.301 | 4.538 |
| eyes_closed / early_5_20 / all | 60.004 | 0.968 | 0.659 | 5.474 | 4.485 |
| eyes_closed / early_5_20 / proxy_local | 0.000 | not estimable | not estimable | not estimable | not estimable |
| eyes_closed / early_5_20 / proxy_outside_local | 60.004 | 0.968 | 0.659 | 5.474 | 4.485 |
| eyes_closed / early_5_20 / proxy_context_touched | 0.008 | 236.910 | 137.306 | 5.164 | 2.554 |
| eyes_closed / early_5_20 / proxy_context_untouched | 59.996 | 0.968 | 0.659 | 5.474 | 4.485 |
| eyes_closed / late_from20_to_original_mask_end / all | 140.105 | 0.759 | 0.591 | 5.227 | 4.561 |
| eyes_closed / late_from20_to_original_mask_end / proxy_local | 5.695 | 0.279 | 0.217 | 5.430 | 4.632 |
| eyes_closed / late_from20_to_original_mask_end / proxy_outside_local | 134.410 | 0.838 | 0.647 | 5.219 | 4.558 |
| eyes_closed / late_from20_to_original_mask_end / proxy_context_touched | 20.102 | 0.500 | 0.379 | 5.315 | 4.542 |
| eyes_closed / late_from20_to_original_mask_end / proxy_context_untouched | 120.004 | 0.855 | 0.662 | 5.212 | 4.564 |

### Companion: all strata

| Stratum | Seconds | Spline NMSE | Zuna NMSE | Spline RMSE | Zuna RMSE |
| --- | --- | --- | --- | --- | --- |
| all / all / all | 400.219 | 0.666 | 2.048 | 5.726 | 9.896 |
| all / all / proxy_local | 43.672 | 0.222 | 1.465 | 6.675 | 16.341 |
| all / all / proxy_outside_local | 356.547 | 1.036 | 2.580 | 5.598 | 8.788 |
| all / all / proxy_context_touched | 160.219 | 0.479 | 3.048 | 5.969 | 14.547 |
| all / all / proxy_context_untouched | 240.000 | 1.015 | 0.732 | 5.557 | 4.695 |
| all / early_5_20 / all | 120.004 | 0.546 | 1.618 | 5.685 | 9.729 |
| all / early_5_20 / proxy_local | 15.832 | 0.163 | 0.940 | 6.625 | 15.811 |
| all / early_5_20 / proxy_outside_local | 104.172 | 1.037 | 2.449 | 5.528 | 8.429 |
| all / early_5_20 / proxy_context_touched | 50.012 | 0.345 | 2.097 | 5.829 | 14.056 |
| all / early_5_20 / proxy_context_untouched | 69.992 | 1.050 | 0.717 | 5.580 | 4.594 |
| all / late_from20_to_original_mask_end / all | 280.215 | 0.733 | 2.288 | 5.743 | 9.967 |
| all / late_from20_to_original_mask_end / proxy_local | 27.840 | 0.273 | 1.924 | 6.704 | 16.635 |
| all / late_from20_to_original_mask_end / proxy_outside_local | 252.375 | 1.036 | 2.638 | 5.627 | 8.931 |
| all / late_from20_to_original_mask_end / proxy_context_touched | 110.207 | 0.569 | 3.679 | 6.032 | 14.764 |
| all / late_from20_to_original_mask_end / proxy_context_untouched | 170.008 | 1.002 | 0.738 | 5.547 | 4.736 |
| eyes_open / all / all | 200.109 | 0.598 | 3.017 | 6.012 | 13.192 |
| eyes_open / all / proxy_local | 37.977 | 0.219 | 1.573 | 6.813 | 17.418 |
| eyes_open / all / proxy_outside_local | 162.133 | 1.292 | 5.514 | 5.808 | 11.989 |
| eyes_open / all / proxy_context_touched | 140.109 | 0.482 | 3.386 | 6.038 | 15.451 |
| eyes_open / all / proxy_context_untouched | 60.000 | 1.484 | 0.954 | 5.951 | 4.787 |
| eyes_open / early_5_20 / all | 60.000 | 0.393 | 2.048 | 5.766 | 12.960 |
| eyes_open / early_5_20 / proxy_local | 15.832 | 0.163 | 0.940 | 6.625 | 15.811 |
| eyes_open / early_5_20 / proxy_outside_local | 44.168 | 1.162 | 5.559 | 5.425 | 11.771 |
| eyes_open / early_5_20 / proxy_context_touched | 50.004 | 0.345 | 2.097 | 5.829 | 14.057 |
| eyes_open / early_5_20 / proxy_context_untouched | 9.996 | 1.878 | 1.185 | 5.441 | 4.431 |
| eyes_open / late_from20_to_original_mask_end / all | 140.109 | 0.739 | 3.673 | 6.114 | 13.290 |
| eyes_open / late_from20_to_original_mask_end / proxy_local | 22.145 | 0.275 | 2.222 | 6.945 | 18.481 |
| eyes_open / late_from20_to_original_mask_end / proxy_outside_local | 117.965 | 1.349 | 5.540 | 5.945 | 12.069 |
| eyes_open / late_from20_to_original_mask_end / proxy_context_touched | 90.105 | 0.596 | 4.436 | 6.151 | 16.173 |
| eyes_open / late_from20_to_original_mask_end / proxy_context_untouched | 50.004 | 1.436 | 0.927 | 6.047 | 4.855 |
| eyes_closed / all / all | 200.109 | 0.804 | 0.610 | 5.424 | 4.673 |
| eyes_closed / all / proxy_local | 5.695 | 0.264 | 0.221 | 5.669 | 4.974 |
| eyes_closed / all / proxy_outside_local | 194.414 | 0.875 | 0.658 | 5.417 | 4.664 |
| eyes_closed / all / proxy_context_touched | 20.109 | 0.456 | 0.359 | 5.468 | 4.754 |
| eyes_closed / all / proxy_context_untouched | 180.000 | 0.903 | 0.676 | 5.419 | 4.664 |
| eyes_closed / early_5_20 / all | 60.004 | 0.984 | 0.678 | 5.603 | 4.620 |
| eyes_closed / early_5_20 / proxy_local | 0.000 | not estimable | not estimable | not estimable | not estimable |
| eyes_closed / early_5_20 / proxy_outside_local | 60.004 | 0.984 | 0.678 | 5.603 | 4.620 |
| eyes_closed / early_5_20 / proxy_context_touched | 0.008 | 11948.334 | 2927.619 | 5.358 | 2.453 |
| eyes_closed / early_5_20 / proxy_context_untouched | 59.996 | 0.984 | 0.678 | 5.603 | 4.620 |
| eyes_closed / late_from20_to_original_mask_end / all | 140.105 | 0.742 | 0.587 | 5.346 | 4.696 |
| eyes_closed / late_from20_to_original_mask_end / proxy_local | 5.695 | 0.264 | 0.221 | 5.669 | 4.974 |
| eyes_closed / late_from20_to_original_mask_end / proxy_outside_local | 134.410 | 0.831 | 0.650 | 5.332 | 4.683 |
| eyes_closed / late_from20_to_original_mask_end / proxy_context_touched | 20.102 | 0.456 | 0.359 | 5.468 | 4.755 |
| eyes_closed / late_from20_to_original_mask_end / proxy_context_untouched | 120.004 | 0.865 | 0.675 | 5.325 | 4.686 |

## Amplitude and spectral preservation

Welch spectra use fixed two-second Hann windows with 50% overlap, constant detrending and density scaling. Periodograms are averaged by the number of contributing Welch windows. Every run stays inside a single block and contiguous valid-mask interval; samples are never stitched across an exclusion or gap. Runs shorter than two seconds contribute no spectrum, and their omitted support is reported in JSON. Bands use trapezoidal integration: theta 4–8, alpha 8–13 and beta 13–30 Hz.

*Figure omitted from this public report-only copy.*

| Endpoint | Condition | Branch | Mean theta µV² | Mean alpha µV² | Mean beta µV² |
| --- | --- | --- | --- | --- | --- |
| Primary | eyes_open | measured | 5.523 | 3.807 | 1.856 |
| Primary | eyes_open | spherical_spline | 6.308 | 4.286 | 1.814 |
| Primary | eyes_open | zuna | 15.840 | 11.049 | 3.848 |
| Primary | eyes_closed | measured | 2.751 | 13.693 | 2.237 |
| Primary | eyes_closed | spherical_spline | 3.028 | 13.982 | 2.039 |
| Primary | eyes_closed | zuna | 2.946 | 17.354 | 2.280 |
| Companion | eyes_open | measured | 5.523 | 3.807 | 1.882 |
| Companion | eyes_open | spherical_spline | 6.308 | 4.286 | 1.837 |
| Companion | eyes_open | zuna | 15.840 | 11.049 | 3.884 |
| Companion | eyes_closed | measured | 2.751 | 13.693 | 2.259 |
| Companion | eyes_closed | spherical_spline | 3.028 | 13.982 | 2.056 |
| Companion | eyes_closed | zuna | 2.946 | 17.354 | 2.298 |

### Closed-minus-open alpha difference

| Endpoint | Branch | F3 | F4 | P3 | P4 | Electrode mean µV² |
| --- | --- | --- | --- | --- | --- | --- |
| Primary | measured | 10.890 | 11.344 | 7.262 | 10.048 | 9.886 |
| Primary | spherical_spline | 9.476 | 11.603 | 7.838 | 9.868 | 9.696 |
| Primary | zuna | 5.173 | 9.008 | 5.576 | 5.464 | 6.305 |
| Companion | measured | 10.890 | 11.344 | 7.262 | 10.048 | 9.886 |
| Companion | spherical_spline | 9.476 | 11.603 | 7.838 | 9.868 | 9.696 |
| Companion | zuna | 5.173 | 9.008 | 5.576 | 5.464 | 6.305 |

The signed difference describes the recorded condition contrast, not a verified neural response or compliance measure. A larger difference is not inherently more accurate; comparison is with the measured target’s difference. Waveform standard deviations/RMS for every electrode and stratum are preserved in JSON.

## Genuine model-context seams

Only 1,280-sample boundaries strictly inside each original block are considered, and both adjacent samples must pass the original scoring mask. Inter-block joins are excluded. Absolute adjacent-sample jumps are descriptive; ordinary pairs are all other scored within-block adjacent pairs, not matched causal controls.

| Endpoint | Branch | Electrode | Seams | Median seam jump µV | 95th percentile µV | Median ordinary jump µV |
| --- | --- | --- | --- | --- | --- | --- |
| Primary | measured | F3 | 84 | 0.851 | 2.362 | 0.711 |
| Primary | measured | F4 | 84 | 0.504 | 2.088 | 0.645 |
| Primary | measured | P3 | 84 | 0.593 | 2.533 | 0.608 |
| Primary | measured | P4 | 84 | 0.605 | 1.744 | 0.615 |
| Primary | spherical_spline | F3 | 84 | 0.705 | 2.554 | 0.644 |
| Primary | spherical_spline | F4 | 84 | 0.790 | 2.173 | 0.694 |
| Primary | spherical_spline | P3 | 84 | 0.546 | 2.430 | 0.568 |
| Primary | spherical_spline | P4 | 84 | 0.563 | 1.891 | 0.616 |
| Primary | zuna | F3 | 84 | 0.904 | 5.689 | 0.634 |
| Primary | zuna | F4 | 84 | 1.270 | 5.646 | 0.578 |
| Primary | zuna | P3 | 84 | 1.136 | 7.598 | 0.572 |
| Primary | zuna | P4 | 84 | 1.284 | 7.763 | 0.637 |
| Companion | measured | F3 | 84 | 0.984 | 2.635 | 0.765 |
| Companion | measured | F4 | 84 | 0.559 | 2.076 | 0.675 |
| Companion | measured | P3 | 84 | 0.603 | 2.572 | 0.639 |
| Companion | measured | P4 | 84 | 0.650 | 1.853 | 0.640 |
| Companion | spherical_spline | F3 | 84 | 0.727 | 2.639 | 0.677 |
| Companion | spherical_spline | F4 | 84 | 0.898 | 2.176 | 0.726 |
| Companion | spherical_spline | P3 | 84 | 0.549 | 2.444 | 0.602 |
| Companion | spherical_spline | P4 | 84 | 0.651 | 2.019 | 0.640 |
| Companion | zuna | F3 | 84 | 1.991 | 16.820 | 0.672 |
| Companion | zuna | F4 | 84 | 3.172 | 17.510 | 0.609 |
| Companion | zuna | P3 | 84 | 2.267 | 23.930 | 0.601 |
| Companion | zuna | P4 | 84 | 2.713 | 22.242 | 0.669 |

### Tiny terminal-context sensitivity

The eight last contexts contain only 3–7 recorded samples each and are reflected to 128 model samples, not a full 1,280-sample context. Padded samples are not assigned new timestamps or directly scored. Zero-phase final filtering can nevertheless propagate effects backward into scored samples. The following frozen interventions operate on private prediction copies only: hold the final tail at the preceding prediction value, or add exactly 1 µV to that tail. Neither replaces the primary or companion results.

| Pipeline | Block | Real tail samples | Tail-hold max change µV | Tail-hold RMS change µV | +1 µV tail max change µV |
| --- | --- | --- | --- | --- | --- |
| Current pipeline | 1 | 7 | 0.00398265 | 0.00033008 | 0.000999298 |
| Current pipeline | 2 | 7 | 0.0159126 | 0.000880907 | 0.000999298 |
| Current pipeline | 3 | 3 | 0.00434428 | 0.000339918 | 0.00102838 |
| Current pipeline | 4 | 5 | 0.0019001 | 0.000149788 | 0.00102138 |
| Current pipeline | 5 | 7 | 0.00803992 | 0.000625683 | 0.00101054 |
| Current pipeline | 6 | 7 | 0.00510265 | 0.000339357 | 0.000999298 |
| Current pipeline | 7 | 5 | 0.00444897 | 0.000337054 | 0.00102138 |
| Current pipeline | 8 | 5 | 0.00280927 | 0.000227857 | 0.00104733 |
| Historical pipeline | 1 | 7 | 8.76715 | 0.544235 | 0.000999298 |
| Historical pipeline | 2 | 7 | 5.23022 | 0.413831 | 0.000999298 |
| Historical pipeline | 3 | 3 | 12.1934 | 0.962536 | 0.00102838 |
| Historical pipeline | 4 | 5 | 10.6415 | 0.683081 | 0.00102138 |
| Historical pipeline | 5 | 7 | 5.72716 | 0.355624 | 0.00101054 |
| Historical pipeline | 6 | 7 | 7.32947 | 0.592321 | 0.000999298 |
| Historical pipeline | 7 | 5 | 11.0844 | 0.819011 | 0.00102138 |
| Historical pipeline | 8 | 5 | 6.91478 | 0.597588 | 0.00104733 |

These diagnostics quantify a residual filtering/tail limitation; the five-second edge exclusion is not claimed to provide perfect isolation. The historical tail-hold maximum was approximately 12.193 µV, so that historical propagation must not be dismissed as universally negligible.

## Fixed waveform examples

These are seconds 5–20 of the first chronological eyes-open and first eyes-closed blocks, declared independently of prediction errors. They are not selected best/worst examples.

*Figure omitted from this public report-only copy.*

## Historical comparison, not an unchanged-target improvement test

| Historical endpoint | Spline NMSE | Zuna NMSE | Spline pooled RMSE | Zuna pooled RMSE |
| --- | --- | --- | --- | --- |
| Original final filter | 0.659 | 1.224 | 5.734 | 7.753 |
| Original precomparison | 0.664 | 2.066 | 5.752 | 9.979 |

The original results remain intact. The new boundary preparation changes the measured targets as well as retained inputs; therefore absolute old/new error differences cannot isolate a model improvement. The useful comparison is Zuna against the baseline within each declared pipeline.

## Limitations and next decision

- Post-hoc, single-recording development comparison. Historical BENCH status is preserved. No participant-data promotion or prospective validation.
- Withheld measured EEG is not clean neural ground truth. Reproducing or disagreeing with ocular contamination is not proof of neural preservation or artifact removal.
- The original fixed frontal proxy was calculated before this corrected comparison, on the old preparation. It is a noisy historical stratifier, not verified blinks; untouched does not mean clean. No outcome-selected exclusion is made.
- Eyes-open/closed labels follow software observations, not independently measured compliance. Timing is approximate without independent ALS-barcode validation; template positions include disclosed Cz/Pz coordinate clipping.
- Full-block centering and zero-phase filtering use future samples; this is offline/noncausal, not live-ready processing. Independent five-second model contexts and reflected final padding can introduce seams.
- The primary production endpoint applies the same post-prediction filter to every branch, but measured/spline signals already had preparation filtering while model output did not. The mandatory precomparison companion is reported without choosing the favorable endpoint.
- Both prepared inputs and comparison targets changed after the boundary correction. Old/new absolute error differences are not an isolated measure of model improvement against an unchanged clean target.
- All blocks, channels and declared strata are retained regardless of winner. Repeated windows/channels are not independent participants; no significance or clinical-validity claim is made.
- Private EEG-derived outputs require separate privacy review before sharing. The installed Workbench, original XDF, recipe and historical results remain unchanged.

This result can determine whether a frozen reconstruction candidate merits testing in an untouched session. It cannot independently establish benefit, validate an artifact-removal claim, justify a hardware change, or authorize live adaptation. If an advantage depends on filtering, condition or proxy subset, that dependency remains part of the result rather than grounds to hide the unfavorable data.

## Audit files

- [Complete numerical report](FULL_COMPARISON_REPORT.json).
- Production module report (supporting file not included in this public copy).
- [Completion record](../execution_completion.json).
- [Frozen full comparison plan](../full_comparison_plan.json).
- [Predeclared strata](../strata_predeclared.json).
