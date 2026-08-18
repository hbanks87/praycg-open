#!/usr/bin/env python3
"""
Build a PR-AYC-G ICA Artifact Library from one or more artifact-control XDF files.

Input:
  XDF(s) recorded during praycg_ica_control_run.py while OpenBCI EEG was streaming.

Output:
  - stream_inventory.csv
  - markers.csv
  - artifact_events.csv
  - raw_channel_qc.csv
  - suggested_bad_channels.txt
  - ica_solution.fif
  - component_features.csv
  - component_artifact_scores.csv
  - artifact_component_rankings.csv
  - artifact_templates.npz
  - artifact_templates.csv
  - figures/ if requested

This script builds an inspection library. It does not prove that any component is artifact.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd

from praycg_ica_common import (
    add_mne_annotations,
    basic_channel_qc,
    build_artifact_events,
    compute_component_feature_table,
    event_locked_scores,
    find_stream,
    ica_topographies,
    load_xdf_streams,
    make_artifact_templates,
    make_mne_raw_from_xdf,
    parse_marker_stream,
    safe_json_dump,
    save_templates_npz,
    stream_inventory,
    suggest_bad_channels,
)


def parse_args():
    p = argparse.ArgumentParser(description="Build a PR-AYC-G ICA artifact library from artifact-control XDF files.")
    p.add_argument("xdf", nargs="+", help="Artifact-control .xdf files")
    p.add_argument("--out", default="ica_artifact_library", help="Output folder")
    p.add_argument("--eeg-stream", default="obci_eeg1", help="EEG stream name or substring")
    p.add_argument("--marker-stream", default="ICAArtifactMarkers", help="Marker stream name or substring")
    p.add_argument("--channel-map", default=None, help="CSV mapping raw channel names to 10-20 montage names")
    p.add_argument("--eeg-units", default="microvolts", choices=["microvolts", "millivolts", "volts"], help="Units in XDF EEG stream")
    p.add_argument("--montage", default="standard_1020", help="MNE montage name")
    p.add_argument("--l-freq", type=float, default=1.0, help="High-pass cutoff for ICA preprocessing")
    p.add_argument("--h-freq", type=float, default=55.0, help="Low-pass cutoff for ICA preprocessing")
    p.add_argument("--notch", type=float, default=60.0, help="Notch frequency; set 0 to skip")
    p.add_argument("--n-components", default="0.95", help="ICA n_components: integer or float variance fraction")
    p.add_argument("--method", default="fastica", choices=["fastica", "infomax", "picard"], help="MNE ICA method")
    p.add_argument("--random-state", type=int, default=97)
    p.add_argument("--baseline-pre-sec", type=float, default=1.0, help="Pre-action baseline window for event-locked scoring")
    p.add_argument("--template-top-n", type=int, default=2)
    p.add_argument("--template-min-score", type=float, default=1.0)
    p.add_argument("--make-figures", action="store_true", help="Save diagnostic plots")
    p.add_argument("--overwrite", action="store_true")
    return p.parse_args()


def parse_n_components(value: str):
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("--n-components must be an int or float string, e.g. 8 or 0.95")


def process_one_xdf(args, xdf_path: Path, outdir: Path):
    import mne
    from mne.preprocessing import ICA

    run_name = xdf_path.stem
    run_out = outdir / run_name
    run_out.mkdir(parents=True, exist_ok=True)

    streams = load_xdf_streams(xdf_path)
    inv = stream_inventory(streams)
    inv.to_csv(run_out / "stream_inventory.csv", index=False)

    eeg = find_stream(streams, name=args.eeg_stream, stream_type="EEG")
    markers = find_stream(streams, name=args.marker_stream, stream_type="Markers")

    raw = make_mne_raw_from_xdf(eeg, channel_map_csv=args.channel_map, eeg_units=args.eeg_units, montage_name=args.montage)
    xdf_t0 = float(eeg.time_stamps[0])

    markers_df = parse_marker_stream(markers)
    markers_df.to_csv(run_out / "markers.csv", index=False)
    events_df = build_artifact_events(markers_df)
    if len(events_df) == 0:
        raise RuntimeError("No artifact ACTION_START/ACTION_END markers found. Was this XDF recorded with praycg_ica_control_run.py?")
    events_df["rel_start"] = events_df["start_time"] - xdf_t0
    events_df["rel_end"] = events_df["end_time"] - xdf_t0
    events_df.to_csv(run_out / "artifact_events.csv", index=False)

    add_mne_annotations(raw, markers_df, xdf_t0=xdf_t0)
    qc = basic_channel_qc(raw)
    qc.to_csv(run_out / "raw_channel_qc.csv", index=False)
    bads = suggest_bad_channels(qc)
    raw.info["bads"] = bads
    with open(run_out / "suggested_bad_channels.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(bads) + ("\n" if bads else ""))

    # Preprocessing copy for ICA. Keep original raw untouched except annotations/bads.
    raw_ica = raw.copy().pick("eeg")
    if args.notch and args.notch > 0 and raw_ica.info["sfreq"] / 2 > args.notch:
        raw_ica.notch_filter(freqs=[args.notch], verbose="ERROR")
    h_freq = min(args.h_freq, raw_ica.info["sfreq"] / 2 - 1.0)
    raw_ica.filter(l_freq=args.l_freq, h_freq=h_freq, verbose="ERROR")

    if bads:
        # Drop bad channels for ICA instead of interpolating to avoid inventing data.
        raw_ica.drop_channels([ch for ch in bads if ch in raw_ica.ch_names])

    if len(raw_ica.ch_names) < 4:
        raise RuntimeError(f"Too few usable channels after QC: {len(raw_ica.ch_names)}")

    n_components = parse_n_components(args.n_components)
    ica = ICA(n_components=n_components, method=args.method, random_state=args.random_state, max_iter="auto")
    ica.fit(raw_ica, verbose="ERROR")
    ica.save(run_out / "ica_solution.fif", overwrite=True)

    features = compute_component_feature_table(ica, raw_ica)
    features.to_csv(run_out / "component_features.csv", index=False)

    scores = event_locked_scores(ica, raw_ica, events_df, baseline_pre_sec=args.baseline_pre_sec)
    scores.to_csv(run_out / "component_artifact_scores.csv", index=False)
    if len(scores):
        rankings = scores.sort_values(["artifact_label", "artifact_score"], ascending=[True, False])
    else:
        rankings = pd.DataFrame()
    rankings.to_csv(run_out / "artifact_component_rankings.csv", index=False)

    template_df, topo_templates, feature_templates, feature_cols = make_artifact_templates(
        ica,
        features,
        scores,
        top_n=args.template_top_n,
        min_score=args.template_min_score,
    )
    template_df.to_csv(run_out / "artifact_templates.csv", index=False)
    labels = template_df["artifact_label"].tolist() if len(template_df) else []
    save_templates_npz(
        run_out / "artifact_templates.npz",
        labels=labels,
        topo_templates=topo_templates,
        feature_templates=feature_templates,
        feature_cols=feature_cols,
        channel_names=raw_ica.ch_names,
    )

    # Metadata.
    meta = dict(
        xdf=str(xdf_path),
        eeg_stream=eeg.name,
        marker_stream=markers.name,
        sfreq=float(raw_ica.info["sfreq"]),
        n_channels_original=len(raw.ch_names),
        n_channels_ica=len(raw_ica.ch_names),
        bad_channels=bads,
        n_ica_components=int(ica.n_components_),
        artifact_labels=sorted(events_df["artifact_label"].dropna().unique().tolist()),
        caveat="ICA library is an inspection aid. It is not a substitute for EOG/EMG/respiration/motion sensors or manual review.",
    )
    safe_json_dump(meta, run_out / "library_metadata.json")

    if args.make_figures:
        make_figures(run_out, ica, raw_ica, features, scores, events_df)

    return run_out


def make_figures(run_out: Path, ica, raw, features: pd.DataFrame, scores: pd.DataFrame, events_df: pd.DataFrame):
    import matplotlib.pyplot as plt

    figdir = run_out / "figures"
    figdir.mkdir(exist_ok=True)

    # Artifact score heatmap.
    if len(scores):
        pivot = scores.pivot_table(index="artifact_label", columns="component", values="artifact_score", aggfunc="mean")
        fig, ax = plt.subplots(figsize=(max(8, 0.5 * pivot.shape[1]), max(5, 0.35 * pivot.shape[0])))
        im = ax.imshow(pivot.to_numpy(), aspect="auto")
        ax.set_title("ICA component artifact scores by label")
        ax.set_xlabel("ICA component")
        ax.set_ylabel("Artifact label")
        ax.set_xticks(range(pivot.shape[1]))
        ax.set_xticklabels(pivot.columns.astype(str), rotation=90)
        ax.set_yticks(range(pivot.shape[0]))
        ax.set_yticklabels(pivot.index)
        fig.colorbar(im, ax=ax, label="event-locked score")
        fig.tight_layout()
        fig.savefig(figdir / "artifact_score_heatmap.png", dpi=160)
        plt.close(fig)

    # Feature summary.
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(features["component"].astype(str), features["rel_low_gamma_30_45"].fillna(0))
    ax.set_title("Relative low-gamma 30-45 Hz by ICA component")
    ax.set_xlabel("Component")
    ax.set_ylabel("Relative power")
    fig.tight_layout()
    fig.savefig(figdir / "component_low_gamma_relative_power.png", dpi=160)
    plt.close(fig)

    # MNE component topomaps if possible.
    try:
        picks = list(range(int(ica.n_components_)))
        figs = ica.plot_components(picks=picks, show=False)
        if not isinstance(figs, list):
            figs = [figs]
        for i, fig in enumerate(figs):
            fig.savefig(figdir / f"ica_components_topomap_page_{i+1}.png", dpi=160)
            plt.close(fig)
    except Exception as exc:
        with open(figdir / "topomap_plot_error.txt", "w", encoding="utf-8") as f:
            f.write(str(exc))


def merge_templates(run_dirs: List[Path], outdir: Path):
    """Create a simple top-level registry pointing to per-run libraries."""
    rows = []
    for rd in run_dirs:
        meta_path = rd / "library_metadata.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            labels = meta.get("artifact_labels", [])
            for label in labels:
                rows.append(dict(run=rd.name, artifact_label=label, run_dir=str(rd)))
    pd.DataFrame(rows).to_csv(outdir / "artifact_library_registry.csv", index=False)
    safe_json_dump(
        dict(
            run_libraries=[str(x) for x in run_dirs],
            note="Templates are stored per run because ICA solutions are montage/session-specific. Use apply script for per-run matching.",
        ),
        outdir / "artifact_library_registry.json",
    )


def main():
    args = parse_args()
    outdir = Path(args.out).resolve()
    if outdir.exists() and not args.overwrite:
        print(f"Output folder exists: {outdir}. Use --overwrite to continue writing into it.")
    outdir.mkdir(parents=True, exist_ok=True)

    run_dirs = []
    for xp in args.xdf:
        run_dirs.append(process_one_xdf(args, Path(xp).resolve(), outdir))
    merge_templates(run_dirs, outdir)
    print("\nICA artifact library build complete.")
    print(f"Output: {outdir}")
    print("Inspect artifact_component_rankings.csv and figures before excluding any components from PR-AYC-G runs.")


if __name__ == "__main__":
    main()
