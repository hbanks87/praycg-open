> Public report-only derivative. Local identifiers, paths, exact machine timestamps and unavailable private links have been removed. Historical statements describe their original stage, not the final combined outcome.

> Context: Post-hoc proxy analysis; no independently verified blink labels. Private events, masks and waveform figures are withheld.

# Saved retained-input engineering diagnostics

No model inference or source changes. Only saved retained inputs, timestamps, masks and provenance were read.

```json
{
  "schema": "PRAYCG_PrivateZunaSavedRetainedInputAudit_v1_0",
  "status": "COMPLETED_NO_MODEL_INFERENCE",
  "elapsed_seconds": 0.125,
  "original_run_unchanged": true,
  "input_hashes_before": {
    "[LOCAL_PATH_REMOVED]": "44be66d1e9f5b2b7395d74c7fd1f5ce546afaca20942dc8f3bd7f33ea0c8190d",
    "[LOCAL_PATH_REMOVED]": "c31772af3612ec73bec81e4d64e4cefc72cc1f6873276db1c722496af1aac5aa"
  },
  "input_hashes_after": {
    "[LOCAL_PATH_REMOVED]": "44be66d1e9f5b2b7395d74c7fd1f5ce546afaca20942dc8f3bd7f33ea0c8190d",
    "[LOCAL_PATH_REMOVED]": "c31772af3612ec73bec81e4d64e4cefc72cc1f6873276db1c722496af1aac5aa"
  },
  "retained_names": [
    "Fz",
    "Cz",
    "Pz",
    "C3",
    "C4",
    "P7",
    "P8",
    "O1",
    "O2",
    "T7",
    "T8",
    "Fp1"
  ],
  "original_evaluation_samples": 102456,
  "original_mask_unchanged": true,
  "source_functions": [
    "Installed zuna_adapter.prepare_segment",
    "pinned transformer.py sample() zero-sum rule"
  ],
  "model_weights_loaded": false,
  "model_inference_executed": false,
  "target_measurements_used": false,
  "original_xdf_read": false,
  "source_modified": false,
  "network_access": false,
  "recreated_window_stats_match_saved_exactly": false,
  "recreated_window_stats_match_saved_within_tolerance": true,
  "statistic_comparison_tolerance": {
    "rtol": 2e-14,
    "atol_uv": 1e-10
  },
  "statistic_roundoff_differences_count": 143,
  "statistic_max_abs_difference_uv": 1.4551915228366852e-11,
  "window_count": 104,
  "short_contexts": [
    {
      "window": 13,
      "segment_index": 0,
      "node_id": "zuna_validation_eyes_open_1",
      "condition": "eyes_open",
      "start_after_block_onset_seconds": 59.99827295576688,
      "stop_after_block_onset_seconds": 60.02177783002844,
      "original_samples": 7,
      "padded_samples": 128,
      "evaluated_samples": 0,
      "shared_scale_uv": 50973.95808772858,
      "retained_mean_uv": -1.7756801320328598e-12,
      "retained_std_uv": 5097.395808772858,
      "retained_token_minimum": -0.1691250056028366,
      "retained_token_maximum": 0.18853172659873962,
      "retained_token_elements": 1536,
      "retained_token_elements_abs_gt_1": 0,
      "retained_zero_sum_tokens": 0,
      "expected_target_zero_sum_tokens": 16
    },
    {
      "window": 26,
      "segment_index": 1,
      "node_id": "zuna_validation_eyes_closed_1",
      "condition": "eyes_closed",
      "start_after_block_onset_seconds": 60.00221608392894,
      "stop_after_block_onset_seconds": 60.02527854120126,
      "original_samples": 7,
      "padded_samples": 128,
      "evaluated_samples": 0,
      "shared_scale_uv": 50294.346312587906,
      "retained_mean_uv": -3.0316490059097606e-13,
      "retained_std_uv": 5029.43463125879,
      "retained_token_minimum": -0.15224584937095642,
      "retained_token_maximum": 0.19568844139575958,
      "retained_token_elements": 1536,
      "retained_token_elements_abs_gt_1": 0,
      "retained_zero_sum_tokens": 0,
      "expected_target_zero_sum_tokens": 16
    },
    {
      "window": 39,
      "segment_index": 2,
      "node_id": "zuna_validation_eyes_closed_2",
      "condition": "eyes_closed",
      "start_after_block_onset_seconds": 59.99867623357568,
      "stop_after_block_onset_seconds": 60.00631703902036,
      "original_samples": 3,
      "padded_samples": 128,
      "evaluated_samples": 0,
      "shared_scale_uv": 55044.99318901895,
      "retained_mean_uv": 1.2126596023639042e-12,
      "retained_std_uv": 5504.499318901895,
      "retained_token_minimum": -0.12939974665641785,
      "retained_token_maximum": 0.18687455356121063,
      "retained_token_elements": 1536,
      "retained_token_elements_abs_gt_1": 0,
      "retained_zero_sum_tokens": 0,
      "expected_target_zero_sum_tokens": 16
    },
    {
      "window": 52,
      "segment_index": 3,
      "node_id": "zuna_validation_eyes_open_2",
      "condition": "eyes_open",
      "start_after_block_onset_seconds": 60.00234130886383,
      "stop_after_block_onset_seconds": 60.01809602713911,
      "original_samples": 5,
      "padded_samples": 128,
      "evaluated_samples": 0,
      "shared_scale_uv": 52189.255392305626,
      "retained_mean_uv": -5.456968210637569e-13,
      "retained_std_uv": 5218.925539230562,
      "retained_token_minimum": -0.13650384545326233,
      "retained_token_maximum": 0.1936887800693512,
      "retained_token_elements": 1536,
      "retained_token_elements_abs_gt_1": 0,
      "retained_zero_sum_tokens": 0,
      "expected_target_zero_sum_tokens": 16
    },
    {
      "window": 65,
      "segment_index": 4,
      "node_id": "zuna_validation_eyes_closed_3",
      "condition": "eyes_closed",
      "start_after_block_onset_seconds": 59.99702723126393,
      "stop_after_block_onset_seconds": 60.021092722949106,
      "original_samples": 7,
      "padded_samples": 128,
      "evaluated_samples": 0,
      "shared_scale_uv": 49293.754766801314,
      "retained_mean_uv": 2.7284841053187847e-12,
      "retained_std_uv": 4929.375476680131,
      "retained_token_minimum": -0.15161928534507751,
      "retained_token_maximum": 0.1968638151884079,
      "retained_token_elements": 1536,
      "retained_token_elements_abs_gt_1": 0,
      "retained_zero_sum_tokens": 0,
      "expected_target_zero_sum_tokens": 16
    },
    {
      "window": 78,
      "segment_index": 5,
      "node_id": "zuna_validation_eyes_open_3",
      "condition": "eyes_open",
      "start_after_block_onset_seconds": 59.994824249413796,
      "stop_after_block_onset_seconds": 60.018231699825265,
      "original_samples": 7,
      "padded_samples": 128,
      "evaluated_samples": 0,
      "shared_scale_uv": 49913.866695924284,
      "retained_mean_uv": 2.165463575649829e-13,
      "retained_std_uv": 4991.386669592428,
      "retained_token_minimum": -0.15705573558807373,
      "retained_token_maximum": 0.1960197240114212,
      "retained_token_elements": 1536,
      "retained_token_elements_abs_gt_1": 0,
      "retained_zero_sum_tokens": 0,
      "expected_target_zero_sum_tokens": 16
    },
    {
      "window": 91,
      "segment_index": 6,
      "node_id": "zuna_validation_eyes_open_4",
      "condition": "eyes_open",
      "start_after_block_onset_seconds": 59.99795558437472,
      "stop_after_block_onset_seconds": 60.0136073626345,
      "original_samples": 5,
      "padded_samples": 128,
      "evaluated_samples": 0,
      "shared_scale_uv": 53360.516276995324,
      "retained_mean_uv": 1.8189894035458566e-13,
      "retained_std_uv": 5336.051627699532,
      "retained_token_minimum": -0.15582521259784698,
      "retained_token_maximum": 0.1776042878627777,
      "retained_token_elements": 1536,
      "retained_token_elements_abs_gt_1": 0,
      "retained_zero_sum_tokens": 0,
      "expected_target_zero_sum_tokens": 16
    },
    {
      "window": 104,
      "segment_index": 7,
      "node_id": "zuna_validation_eyes_closed_4",
      "condition": "eyes_closed",
      "start_after_block_onset_seconds": 60.000115757167805,
      "stop_after_block_onset_seconds": 60.015512744139414,
      "original_samples": 5,
      "padded_samples": 128,
      "evaluated_samples": 0,
      "shared_scale_uv": 54854.72319953126,
      "retained_mean_uv": -4.0624096679190796e-12,
      "retained_std_uv": 5485.472319953126,
      "retained_token_minimum": -0.15714937448501587,
      "retained_token_maximum": 0.16804614663124084,
      "retained_token_elements": 1536,
      "retained_token_elements_abs_gt_1": 0,
      "retained_zero_sum_tokens": 0,
      "expected_target_zero_sum_tokens": 16
    }
  ],
  "normalized_retained_input_minimum": -2.1953201293945312,
  "normalized_retained_input_maximum": 1.3545794486999512,
  "retained_token_elements": 1486848,
  "retained_token_elements_abs_gt_1": 682,
  "retained_abs_gt_1_fraction": 0.000458688446969697,
  "retained_zero_sum_tokens_misidentified_by_heuristic": 0,
  "expected_hidden_target_zero_sum_tokens": 15488,
  "shared_window_scale_uv": {
    "count": 104,
    "minimum": 46.32738536995685,
    "maximum": 55044.99318901895,
    "median": 79.60353901784444,
    "p95": 50237.27437008836,
    "mean": 4579.076131800072
  },
  "fp1_last_two_seconds_pairwise_correlations": {
    "count": 28,
    "minimum": 0.9997183890791626,
    "maximum": 0.9999852277846637,
    "median": 0.9999707873990769,
    "p95": 0.999982603079093,
    "mean": 0.999916815928765
  },
  "blocks": [
    {
      "segment_index": 0,
      "node_id": "zuna_validation_eyes_open_1",
      "condition": "eyes_open",
      "total_samples": 15367,
      "evaluated_samples": 12807,
      "excluded_samples": 2560,
      "fp1_periods": {
        "first_2s": {
          "samples": 512,
          "rms_uv": 136.19140962850094,
          "max_abs_uv": 246.80231288214367,
          "mean_uv": 12.442952042986299
        },
        "interior_5_to_55s": {
          "samples": 12801,
          "rms_uv": 27.238102560655395,
          "max_abs_uv": 352.4402818449125,
          "mean_uv": -0.040594667493404374
        },
        "middle_25_to_30s": {
          "samples": 1279,
          "rms_uv": 5.400547697934481,
          "max_abs_uv": 16.205861524411922,
          "mean_uv": -0.25331898211689047
        },
        "pre_end_50_to_55s": {
          "samples": 1280,
          "rms_uv": 6.87953421291744,
          "max_abs_uv": 24.526156974561594,
          "mean_uv": -0.31360780014154377
        },
        "end_58_to_60s": {
          "samples": 512,
          "rms_uv": 1160.7996528879348,
          "max_abs_uv": 5241.807055758345,
          "mean_uv": -113.44360357876903
        }
      },
      "fp1_max_abs_evaluated_uv": 352.4402818449125,
      "evaluated_first_relative_seconds": 5.001702930370811,
      "evaluated_last_relative_seconds": 55.02145230845781,
      "evaluated_samples_at_or_after_nominal_55s": 6
    },
    {
      "segment_index": 1,
      "node_id": "zuna_validation_eyes_closed_1",
      "condition": "eyes_closed",
      "total_samples": 15367,
      "evaluated_samples": 12808,
      "excluded_samples": 2559,
      "fp1_periods": {
        "first_2s": {
          "samples": 511,
          "rms_uv": 94.10508090951605,
          "max_abs_uv": 208.09137924606839,
          "mean_uv": 6.286227749289952
        },
        "interior_5_to_55s": {
          "samples": 12801,
          "rms_uv": 21.377863212930503,
          "max_abs_uv": 174.79648295683512,
          "mean_uv": -0.058544987330358
        },
        "middle_25_to_30s": {
          "samples": 1280,
          "rms_uv": 6.220682533691381,
          "max_abs_uv": 17.860632063989986,
          "mean_uv": 0.2221438106431187
        },
        "pre_end_50_to_55s": {
          "samples": 1280,
          "rms_uv": 6.782306065062963,
          "max_abs_uv": 19.32945166603059,
          "mean_uv": -0.46047186028292975
        },
        "end_58_to_60s": {
          "samples": 512,
          "rms_uv": 1220.8519905146525,
          "max_abs_uv": 5612.050845852435,
          "mean_uv": -110.57900912797115
        }
      },
      "fp1_max_abs_evaluated_uv": 174.79648295683512,
      "evaluated_first_relative_seconds": 5.002585104492027,
      "evaluated_last_relative_seconds": 55.027202792989556,
      "evaluated_samples_at_or_after_nominal_55s": 7
    },
    {
      "segment_index": 2,
      "node_id": "zuna_validation_eyes_closed_2",
      "condition": "eyes_closed",
      "total_samples": 15363,
      "evaluated_samples": 12804,
      "excluded_samples": 2559,
      "fp1_periods": {
        "first_2s": {
          "samples": 512,
          "rms_uv": 93.99407712615013,
          "max_abs_uv": 156.7997946857038,
          "mean_uv": -13.195283282664713
        },
        "interior_5_to_55s": {
          "samples": 12801,
          "rms_uv": 7.653011937963363,
          "max_abs_uv": 37.3011812078939,
          "mean_uv": -0.057323903442951935
        },
        "middle_25_to_30s": {
          "samples": 1279,
          "rms_uv": 9.546581640832903,
          "max_abs_uv": 37.3011812078939,
          "mean_uv": 0.06263273337833102
        },
        "pre_end_50_to_55s": {
          "samples": 1280,
          "rms_uv": 6.848540893112572,
          "max_abs_uv": 28.29333171140933,
          "mean_uv": -0.14497858875193143
        },
        "end_58_to_60s": {
          "samples": 512,
          "rms_uv": 1354.621327500589,
          "max_abs_uv": 6986.366767211628,
          "mean_uv": -171.48993225478878
        }
      },
      "fp1_max_abs_evaluated_uv": 37.3011812078939,
      "evaluated_first_relative_seconds": 5.00141290697502,
      "evaluated_last_relative_seconds": 55.00946012738859,
      "evaluated_samples_at_or_after_nominal_55s": 3
    },
    {
      "segment_index": 3,
      "node_id": "zuna_validation_eyes_open_2",
      "condition": "eyes_open",
      "total_samples": 15365,
      "evaluated_samples": 12807,
      "excluded_samples": 2558,
      "fp1_periods": {
        "first_2s": {
          "samples": 511,
          "rms_uv": 64.38878274935456,
          "max_abs_uv": 141.91656964729435,
          "mean_uv": -7.193564730118838
        },
        "interior_5_to_55s": {
          "samples": 12801,
          "rms_uv": 35.85224977822579,
          "max_abs_uv": 290.88472315883723,
          "mean_uv": -0.20853716168968445
        },
        "middle_25_to_30s": {
          "samples": 1280,
          "rms_uv": 39.91086649019471,
          "max_abs_uv": 242.73353946261128,
          "mean_uv": -0.24069522862565246
        },
        "pre_end_50_to_55s": {
          "samples": 1280,
          "rms_uv": 12.193369638144086,
          "max_abs_uv": 82.87000682891393,
          "mean_uv": -0.7315622862968848
        },
        "end_58_to_60s": {
          "samples": 512,
          "rms_uv": 1222.8210163881997,
          "max_abs_uv": 5452.810811546962,
          "mean_uv": -126.46794451447953
        }
      },
      "fp1_max_abs_evaluated_uv": 290.88472315883723,
      "evaluated_first_relative_seconds": 5.003839757933747,
      "evaluated_last_relative_seconds": 55.02289583161473,
      "evaluated_samples_at_or_after_nominal_55s": 6
    },
    {
      "segment_index": 4,
      "node_id": "zuna_validation_eyes_closed_3",
      "condition": "eyes_closed",
      "total_samples": 15367,
      "evaluated_samples": 12808,
      "excluded_samples": 2559,
      "fp1_periods": {
        "first_2s": {
          "samples": 512,
          "rms_uv": 89.68646526000245,
          "max_abs_uv": 190.54644945222282,
          "mean_uv": 4.167499626602526
        },
        "interior_5_to_55s": {
          "samples": 12801,
          "rms_uv": 7.5139542908910135,
          "max_abs_uv": 45.76754460747946,
          "mean_uv": -0.07321833926529718
        },
        "middle_25_to_30s": {
          "samples": 1280,
          "rms_uv": 7.370813150485251,
          "max_abs_uv": 22.153438951446066,
          "mean_uv": 0.019090284832593694
        },
        "pre_end_50_to_55s": {
          "samples": 1280,
          "rms_uv": 7.778969764933989,
          "max_abs_uv": 23.313480249714456,
          "mean_uv": -0.6127391621722681
        },
        "end_58_to_60s": {
          "samples": 512,
          "rms_uv": 1222.834273288451,
          "max_abs_uv": 5527.508280891034,
          "mean_uv": -120.25866442581304
        }
      },
      "fp1_max_abs_evaluated_uv": 45.76754460747946,
      "evaluated_first_relative_seconds": 5.003272829926573,
      "evaluated_last_relative_seconds": 55.02556958713103,
      "evaluated_samples_at_or_after_nominal_55s": 7
    },
    {
      "segment_index": 5,
      "node_id": "zuna_validation_eyes_open_3",
      "condition": "eyes_open",
      "total_samples": 15367,
      "evaluated_samples": 12807,
      "excluded_samples": 2560,
      "fp1_periods": {
        "first_2s": {
          "samples": 512,
          "rms_uv": 63.179405787765305,
          "max_abs_uv": 143.64450521645395,
          "mean_uv": -4.797208647833184
        },
        "interior_5_to_55s": {
          "samples": 12802,
          "rms_uv": 41.31641075400843,
          "max_abs_uv": 342.117680504143,
          "mean_uv": 0.04010909015063822
        },
        "middle_25_to_30s": {
          "samples": 1281,
          "rms_uv": 49.84984299313968,
          "max_abs_uv": 218.68785377561915,
          "mean_uv": -0.709786650336463
        },
        "pre_end_50_to_55s": {
          "samples": 1281,
          "rms_uv": 5.289645945467233,
          "max_abs_uv": 15.292472889120813,
          "mean_uv": -0.4949146980991699
        },
        "end_58_to_60s": {
          "samples": 512,
          "rms_uv": 1226.1729971517657,
          "max_abs_uv": 5473.02740150645,
          "mean_uv": -129.3960735443292
        }
      },
      "fp1_max_abs_evaluated_uv": 342.117680504143,
      "evaluated_first_relative_seconds": 5.003562034165952,
      "evaluated_last_relative_seconds": 55.01902916934341,
      "evaluated_samples_at_or_after_nominal_55s": 5
    },
    {
      "segment_index": 6,
      "node_id": "zuna_validation_eyes_open_4",
      "condition": "eyes_open",
      "total_samples": 15365,
      "evaluated_samples": 12807,
      "excluded_samples": 2558,
      "fp1_periods": {
        "first_2s": {
          "samples": 511,
          "rms_uv": 138.13857827165617,
          "max_abs_uv": 267.5472002139249,
          "mean_uv": 18.268755625872718
        },
        "interior_5_to_55s": {
          "samples": 12802,
          "rms_uv": 28.395831900580323,
          "max_abs_uv": 304.3588603118328,
          "mean_uv": -0.09518911324489825
        },
        "middle_25_to_30s": {
          "samples": 1281,
          "rms_uv": 5.468383325157938,
          "max_abs_uv": 15.776907499046398,
          "mean_uv": -0.36363594823787376
        },
        "pre_end_50_to_55s": {
          "samples": 1280,
          "rms_uv": 52.67786831726075,
          "max_abs_uv": 161.14886561452457,
          "mean_uv": -1.1984203192569112
        },
        "end_58_to_60s": {
          "samples": 512,
          "rms_uv": 1298.2561205482257,
          "max_abs_uv": 5936.728896810699,
          "mean_uv": -145.02923732008028
        }
      },
      "fp1_max_abs_evaluated_uv": 304.3588603118328,
      "evaluated_first_relative_seconds": 5.002212429593783,
      "evaluated_last_relative_seconds": 55.018328488687985,
      "evaluated_samples_at_or_after_nominal_55s": 5
    },
    {
      "segment_index": 7,
      "node_id": "zuna_validation_eyes_closed_4",
      "condition": "eyes_closed",
      "total_samples": 15365,
      "evaluated_samples": 12808,
      "excluded_samples": 2557,
      "fp1_periods": {
        "first_2s": {
          "samples": 511,
          "rms_uv": 84.37771409850131,
          "max_abs_uv": 185.54246284293873,
          "mean_uv": 4.441233740364317
        },
        "interior_5_to_55s": {
          "samples": 12801,
          "rms_uv": 8.229550067269889,
          "max_abs_uv": 53.13204213114016,
          "mean_uv": -0.05281020298880666
        },
        "middle_25_to_30s": {
          "samples": 1281,
          "rms_uv": 6.156384117881081,
          "max_abs_uv": 19.444400246529334,
          "mean_uv": 0.12415558831600516
        },
        "pre_end_50_to_55s": {
          "samples": 1280,
          "rms_uv": 11.370942967541849,
          "max_abs_uv": 53.13204213114016,
          "mean_uv": -0.12277286782017979
        },
        "end_58_to_60s": {
          "samples": 512,
          "rms_uv": 1345.1485191277666,
          "max_abs_uv": 5991.565018557525,
          "mean_uv": -140.76399093554457
        }
      },
      "fp1_max_abs_evaluated_uv": 53.13204213114016,
      "evaluated_first_relative_seconds": 5.003759178798646,
      "evaluated_last_relative_seconds": 55.02322863577865,
      "evaluated_samples_at_or_after_nominal_55s": 7
    }
  ],
  "limitations": [
    "Absolute normalized values above 1 are descriptive; this audit does not assign an unsupported universal acceptable range.",
    "Recreated normalization statistics agree within recorded floating-point tolerance, not bit for bit; array reduction layout can alter near-zero means or final mantissa bits.",
    "Saved-input recreation and no false zero-sum token flags are engineering evidence, not model effectiveness.",
    "Fp1 is retained-average-referenced prepared EEG, not independent EOG and not raw acquisition voltages.",
    "Large repeatable endpoint transients can arise from preprocessing; saved traces alone do not prove their cause.",
    "The original five-second evaluation edge guard does not prove absence of filter or model-context propagation into scored intervals.",
    "Per-window scales include tiny final contexts reflected to 128 samples; these are disclosed separately, not treated as separate physiological epochs.",
    "This audit does not alter evaluation masks, original comparison scores, recipe, model settings or artifacts."
  ]
}
```

Full per-window diagnostics are preserved in additional_saved_input_checks.json.
