#!/usr/bin/env python3
"""
PRAYCG StimulusFingerprint Comparison v1.0

Compare two stimulus-fingerprint output folders to estimate physical match quality
between Target, phase-scrambled Control, or Contextual Override media.
"""

from __future__ import annotations
import argparse, csv, json, math
from pathlib import Path
from typing import Any, Dict, List, Tuple
import numpy as np


EPS = 1e-12


def load_summary(folder: Path) -> Dict[str, Any]:
    path = folder / "stimulus_fingerprint_summary.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def interp_series(rows: List[Dict[str, str]], key: str, n: int = 1000) -> np.ndarray:
    if not rows:
        return np.array([])
    t = np.array([float(r["time_sec"]) for r in rows if r.get("time_sec") not in (None, "")], dtype=float)
    y = np.array([float(r.get(key, "nan")) for r in rows if r.get("time_sec") not in (None, "")], dtype=float)
    mask = np.isfinite(t) & np.isfinite(y)
    if mask.sum() < 3:
        return np.array([])
    t = t[mask]; y = y[mask]
    order = np.argsort(t)
    t = t[order]; y = y[order]
    grid = np.linspace(t.min(), t.max(), n)
    return np.interp(grid, t, y)


def corr(a: np.ndarray, b: np.ndarray) -> float:
    if a.size < 3 or b.size < 3:
        return float("nan")
    n = min(a.size, b.size)
    a = a[:n]; b = b[:n]
    if np.std(a) < EPS or np.std(b) < EPS:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def similarity_from_corr(r: float) -> float:
    if not np.isfinite(r):
        return 0.0
    return max(0.0, min(1.0, (r + 1.0) / 2.0))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("folder_a")
    p.add_argument("folder_b")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    fa, fb, out = Path(args.folder_a), Path(args.folder_b), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    a = load_summary(fa)
    b = load_summary(fb)
    va, vb = a["visual"], b["visual"]
    aa, ab = a["audio"], b["audio"]

    vrows_a = load_csv(fa / "stimulus_visual_timeseries.csv")
    vrows_b = load_csv(fb / "stimulus_visual_timeseries.csv")
    arows_a = load_csv(fa / "stimulus_audio_timeseries.csv")
    arows_b = load_csv(fb / "stimulus_audio_timeseries.csv")

    lum_corr = corr(interp_series(vrows_a, "luminance_mean_0_255"), interp_series(vrows_b, "luminance_mean_0_255"))
    change_corr = corr(interp_series(vrows_a, "visual_change_mean_abs_0_255"), interp_series(vrows_b, "visual_change_mean_abs_0_255"))
    audio_corr = corr(interp_series(arows_a, "audio_dbfs"), interp_series(arows_b, "audio_dbfs"))

    duration_similarity = 1.0 - min(1.0, abs(va.get("duration_sec",0)-vb.get("duration_sec",0)) / max(1.0, max(va.get("duration_sec",0), vb.get("duration_sec",0))))
    fps_match = 1.0 if abs(va.get("fps",0)-vb.get("fps",0)) < 0.01 else 0.0
    resolution_match = 1.0 if (va.get("width")==vb.get("width") and va.get("height")==vb.get("height")) else 0.0

    lum_sim = similarity_from_corr(lum_corr)
    change_sim = similarity_from_corr(change_corr)
    audio_sim = similarity_from_corr(audio_corr) if aa.get("has_audio") and ab.get("has_audio") else (1.0 if not aa.get("has_audio") and not ab.get("has_audio") else 0.0)

    physical_match_score = 100.0 * (0.20*duration_similarity + 0.10*fps_match + 0.10*resolution_match + 0.25*lum_sim + 0.20*change_sim + 0.15*audio_sim)

    result = {
        "schema": "PRAYCG_stimulus_fingerprint_comparison_v1_0",
        "folder_a": str(fa),
        "folder_b": str(fb),
        "sha256_a": a.get("input_sha256"),
        "sha256_b": b.get("input_sha256"),
        "identical_file_hash": a.get("input_sha256") == b.get("input_sha256"),
        "duration_similarity_0_1": duration_similarity,
        "fps_match_0_1": fps_match,
        "resolution_match_0_1": resolution_match,
        "luminance_timeline_correlation": lum_corr,
        "visual_change_timeline_correlation": change_corr,
        "audio_dbfs_timeline_correlation": audio_corr,
        "physical_match_score_0_100": physical_match_score,
        "interpretation": (
            "High score means stronger low-level stimulus matching. It does not mean semantic equivalence. "
            "A phase-scrambled control should be high in low-level physical similarity while low in recognizable meaning."
        )
    }
    (out / "stimulus_physical_match_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    with (out / "stimulus_physical_match_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(result.keys()))
        w.writeheader()
        w.writerow(result)

    md = [
        "# PRAYCG StimulusFingerprint Comparison v1.0",
        "",
        f"Physical match score: **{physical_match_score:.2f}/100**",
        "",
        f"- Identical SHA-256: {result['identical_file_hash']}",
        f"- Duration similarity: {duration_similarity:.3f}",
        f"- FPS match: {fps_match:.3f}",
        f"- Resolution match: {resolution_match:.3f}",
        f"- Luminance timeline correlation: {lum_corr}",
        f"- Visual-change timeline correlation: {change_corr}",
        f"- Audio dBFS timeline correlation: {audio_corr}",
        "",
        "Boundary: this is a physical-delivery comparison, not a meaning comparison.",
    ]
    (out / "stimulus_physical_match_report.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
