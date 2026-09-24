#!/usr/bin/env python3
"""
Apply / reference a PR-AYC-G ICA Artifact Library against a new PR-AYC-G XDF run.

This script fits ICA to the target PR-AYC-G run, then scores each component against artifact
library templates using:
  - absolute spatial/topography correlation, if channel sets match
  - spectral/statistical feature similarity

Default behavior is report-only. It does NOT remove components unless --auto-clean is set.
Manual review is strongly recommended.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from praycg_ica_common import (
    basic_channel_qc,
    compute_component_feature_table,
    find_stream,
    ica_topographies,
    load_xdf_streams,
    make_mne_raw_from_xdf,
    safe_json_dump,
    stream_inventory,
    suggest_bad_channels,
)


def parse_args():
    p = argparse.ArgumentParser(description="Score ICA components in a PR-AYC-G run against an artifact library.")
    p.add_argument("xdf", help="PR-AYC-G run .xdf")
    p.add_argument("--library", required=True, help="Path to artifact_templates.npz or a folder containing run subfolders")
    p.add_argument("--out", default="ica_artifact_apply_report", help="Output folder")
    p.add_argument("--eeg-stream", default="obci_eeg1")
    p.add_argument("--channel-map", default=None)
    p.add_argument("--eeg-units", default="microvolts", choices=["microvolts", "millivolts", "volts"])
    p.add_argument("--montage", default="standard_1020")
    p.add_argument("--l-freq", type=float, default=1.0)
    p.add_argument("--h-freq", type=float, default=55.0)
    p.add_argument("--notch", type=float, default=60.0)
    p.add_argument("--n-components", default="0.95")
    p.add_argument("--method", default="fastica", choices=["fastica", "infomax", "picard"])
    p.add_argument("--random-state", type=int, default=97)
    p.add_argument("--spatial-weight", type=float, default=0.65)
    p.add_argument("--feature-weight", type=float, default=0.35)
    p.add_argument("--candidate-threshold", type=float, default=0.70)
    p.add_argument("--auto-clean", action="store_true", help="Apply ICA excluding components above threshold and save cleaned FIF. Report-only by default.")
    p.add_argument("--make-figures", action="store_true")
    return p.parse_args()


def parse_n_components(value: str):
    if "." in value:
        return float(value)
    return int(value)


def load_template_files(library_path: Path) -> List[Path]:
    if library_path.is_file() and library_path.name.endswith(".npz"):
        return [library_path]
    if library_path.is_dir():
        files = sorted(library_path.rglob("artifact_templates.npz"))
        if files:
            return files
    raise FileNotFoundError(f"No artifact_templates.npz found at {library_path}")


def normalize(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    v = np.nan_to_num(v, nan=0.0, posinf=0.0, neginf=0.0)
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def abs_corr(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape:
        return np.nan
    if np.nanstd(a) == 0 or np.nanstd(b) == 0:
        return np.nan
    return float(abs(np.corrcoef(a, b)[0, 1]))


def feature_cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(normalize(a), normalize(b)))


def fit_ica_for_run(args, outdir: Path):
    import mne
    from mne.preprocessing import ICA

    streams = load_xdf_streams(args.xdf)
    stream_inventory(streams).to_csv(outdir / "stream_inventory.csv", index=False)
    eeg = find_stream(streams, name=args.eeg_stream, stream_type="EEG")
    raw = make_mne_raw_from_xdf(eeg, channel_map_csv=args.channel_map, eeg_units=args.eeg_units, montage_name=args.montage)
    qc = basic_channel_qc(raw)
    qc.to_csv(outdir / "raw_channel_qc.csv", index=False)
    bads = suggest_bad_channels(qc)
    raw.info["bads"] = bads
    with open(outdir / "suggested_bad_channels.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(bads) + ("\n" if bads else ""))

    raw_ica = raw.copy().pick("eeg")
    if args.notch and args.notch > 0 and raw_ica.info["sfreq"] / 2 > args.notch:
        raw_ica.notch_filter(freqs=[args.notch], verbose="ERROR")
    raw_ica.filter(l_freq=args.l_freq, h_freq=min(args.h_freq, raw_ica.info["sfreq"] / 2 - 1.0), verbose="ERROR")
    if bads:
        raw_ica.drop_channels([ch for ch in bads if ch in raw_ica.ch_names])

    ica = ICA(n_components=parse_n_components(args.n_components), method=args.method, random_state=args.random_state, max_iter="auto")
    ica.fit(raw_ica, verbose="ERROR")
    ica.save(outdir / "praycg_run_ica_solution.fif", overwrite=True)
    return raw, raw_ica, ica


def score_against_templates(args, outdir: Path, raw_ica, ica, feature_df: pd.DataFrame) -> pd.DataFrame:
    topo = ica_topographies(ica)
    feature_index = feature_df.set_index("component")
    rows = []
    template_files = load_template_files(Path(args.library).resolve())
    for tf in template_files:
        z = np.load(tf, allow_pickle=True)
        labels = [str(x) for x in z["labels"].tolist()]
        t_topo = z["topo_templates"]
        t_feat = z["feature_templates"]
        feat_cols = [str(x) for x in z["feature_cols"].tolist()]
        t_ch = [str(x) for x in z["channel_names"].tolist()]
        spatial_ok = list(raw_ica.ch_names) == t_ch and topo.shape[1] == t_topo.shape[1]

        for comp in range(topo.shape[0]):
            comp_feat = []
            for col in feat_cols:
                comp_feat.append(float(feature_index.loc[comp, col]) if col in feature_index.columns else 0.0)
            comp_feat = np.nan_to_num(np.asarray(comp_feat, dtype=float), nan=0.0)
            for j, label in enumerate(labels):
                spatial_score = abs_corr(topo[comp], t_topo[j]) if spatial_ok else np.nan
                feat_score = feature_cosine(comp_feat, np.nan_to_num(t_feat[j], nan=0.0))
                if np.isfinite(spatial_score):
                    score = args.spatial_weight * spatial_score + args.feature_weight * feat_score
                else:
                    score = feat_score
                rows.append(
                    dict(
                        template_file=str(tf),
                        artifact_label=label,
                        component=int(comp),
                        spatial_score=spatial_score,
                        feature_score=feat_score,
                        combined_score=float(score),
                        spatial_channels_matched=bool(spatial_ok),
                        candidate=bool(score >= args.candidate_threshold),
                    )
                )
    df = pd.DataFrame(rows)
    df.sort_values(["candidate", "combined_score"], ascending=[False, False], inplace=True)
    df.to_csv(outdir / "ica_artifact_library_match_scores.csv", index=False)
    return df


def make_figures(outdir: Path, ica, match_df: pd.DataFrame, feature_df: pd.DataFrame):
    import matplotlib.pyplot as plt

    figdir = outdir / "figures"
    figdir.mkdir(exist_ok=True)
    if len(match_df):
        top = match_df.sort_values("combined_score", ascending=False).head(25).copy()
        labels = [f"IC{r.component}:{r.artifact_label}" for r in top.itertuples()]
        fig, ax = plt.subplots(figsize=(12, max(5, 0.3 * len(top))))
        ax.barh(labels[::-1], top["combined_score"].to_numpy()[::-1])
        ax.axvline(0.70, linestyle="--")
        ax.set_xlabel("Template match score")
        ax.set_title("Top ICA artifact-template matches")
        fig.tight_layout()
        fig.savefig(figdir / "top_artifact_template_matches.png", dpi=160)
        plt.close(fig)
    try:
        figs = ica.plot_components(show=False)
        if not isinstance(figs, list):
            figs = [figs]
        for i, fig in enumerate(figs):
            fig.savefig(figdir / f"praycg_ica_components_topomap_page_{i+1}.png", dpi=160)
            plt.close(fig)
    except Exception as exc:
        with open(figdir / "topomap_plot_error.txt", "w", encoding="utf-8") as f:
            f.write(str(exc))


def main():
    args = parse_args()
    outdir = Path(args.out).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    raw, raw_ica, ica = fit_ica_for_run(args, outdir)
    features = compute_component_feature_table(ica, raw_ica)
    features.to_csv(outdir / "praycg_run_component_features.csv", index=False)
    match_df = score_against_templates(args, outdir, raw_ica, ica, features)

    candidates = sorted(match_df.loc[match_df["candidate"], "component"].astype(int).unique().tolist()) if len(match_df) else []
    safe_json_dump(
        dict(
            xdf=args.xdf,
            library=args.library,
            candidate_threshold=args.candidate_threshold,
            candidate_components=candidates,
            warning="Candidate components require visual/manual review before removal. Auto-clean is disabled unless --auto-clean is passed.",
        ),
        outdir / "ica_artifact_apply_summary.json",
    )

    if args.auto_clean and candidates:
        clean_raw = raw_ica.copy()
        ica.exclude = candidates
        ica.apply(clean_raw, verbose="ERROR")
        clean_raw.save(outdir / "praycg_run_cleaned_by_ica_candidates_raw.fif", overwrite=True)
        with open(outdir / "AUTO_CLEAN_WARNING.txt", "w", encoding="utf-8") as f:
            f.write(
                "Auto-clean was enabled. This file excluded components above the artifact-template threshold.\n"
                "Use only after manual inspection; do not treat this as claim-level artifact proof.\n"
            )

    if args.make_figures:
        make_figures(outdir, ica, match_df, features)

    print("\nICA library reference report complete.")
    print(f"Output: {outdir}")
    print(f"Candidate components above threshold: {candidates}")
    print("Manual inspection required before exclusion.")


if __name__ == "__main__":
    main()
