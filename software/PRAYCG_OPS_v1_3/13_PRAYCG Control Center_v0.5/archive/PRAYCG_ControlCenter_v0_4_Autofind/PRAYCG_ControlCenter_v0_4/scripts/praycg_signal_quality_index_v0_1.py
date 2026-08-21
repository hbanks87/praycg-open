#!/usr/bin/env python3
"""
PRAYCG Signal Quality / Contact Index v0.1

This is a conservative 0-100 live quality proxy for LSL EEG streams.
It is NOT a true Cyton lead-off impedance measurement. True impedance requires
OpenBCI impedance/lead-off commands and should be run as a dedicated pre-run mode.
"""
from __future__ import annotations
import argparse, csv, json, math, time
from pathlib import Path
from datetime import datetime

import numpy as np


def robust_std(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if x.size < 2:
        return float("nan")
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    return float(1.4826 * mad) if mad > 0 else float(np.std(x))


def safe_score(value: float, good: float, bad: float, direction: str = "low_good") -> float:
    if not math.isfinite(value):
        return 0.0
    if direction == "low_good":
        if value <= good:
            return 100.0
        if value >= bad:
            return 0.0
        return 100.0 * (bad - value) / (bad - good)
    else:
        if value >= good:
            return 100.0
        if value <= bad:
            return 0.0
        return 100.0 * (value - bad) / (good - bad)


def compute_channel_scores(data: np.ndarray, times: np.ndarray, expected_rate: float) -> tuple[list[dict], dict]:
    if data.ndim != 2:
        raise ValueError("Expected data shape samples x channels")
    n, ch = data.shape
    finite_global = float(np.isfinite(data).mean()) if data.size else 0.0
    duration = float(times[-1] - times[0]) if len(times) > 1 else 0.0
    eff_rate = float((len(times) - 1) / duration) if duration > 0 else float("nan")
    gaps = np.diff(times) if len(times) > 1 else np.array([])
    p99_gap = float(np.nanpercentile(gaps, 99)) if gaps.size else float("nan")
    max_gap = float(np.nanmax(gaps)) if gaps.size else float("nan")

    rows = []
    for ci in range(ch):
        x = data[:, ci].astype(float)
        finite = np.isfinite(x)
        finite_frac = float(finite.mean()) if x.size else 0.0
        xf = x[finite]
        if xf.size == 0:
            std = p2p = rstd = hf_ratio = float("nan")
        else:
            std = float(np.std(xf))
            rstd = robust_std(xf)
            p2p = float(np.nanpercentile(xf, 99) - np.nanpercentile(xf, 1)) if xf.size > 5 else float(np.ptp(xf))
            dx = np.diff(xf)
            hf_ratio = float(robust_std(dx) / (rstd + 1e-12)) if dx.size and math.isfinite(rstd) else float("nan")
        flat_penalty = 60.0 if (not math.isfinite(std) or std < 1e-8 or p2p < 1e-7) else 0.0
        finite_penalty = max(0.0, (0.98 - finite_frac) * 200.0)
        p2p_penalty = 100.0 - safe_score(p2p, good=250.0, bad=5000.0, direction="low_good")
        hf_penalty = 100.0 - safe_score(hf_ratio, good=0.35, bad=2.0, direction="low_good")
        score = 100.0 - (0.30 * finite_penalty + 0.25 * p2p_penalty + 0.25 * hf_penalty + 0.20 * flat_penalty)
        score = max(0.0, min(100.0, score))
        status = "GOOD" if score >= 80 else "WATCH" if score >= 60 else "POOR"
        rows.append({
            "channel_index_1based": ci + 1,
            "quality_0_100": round(score, 2),
            "status": status,
            "finite_fraction": round(finite_frac, 4),
            "std": std,
            "robust_std": rstd,
            "p2p_1_99": p2p,
            "high_freq_diff_ratio": hf_ratio,
            "note": "Quality/contact proxy; not true lead-off impedance.",
        })
    summary = {
        "schema": "PRAYCG_Signal_Quality_Index_v0_1",
        "created_local": datetime.now().isoformat(timespec="seconds"),
        "sample_count": int(n),
        "channel_count": int(ch),
        "duration_sec": duration,
        "effective_rate_hz": eff_rate,
        "expected_rate_hz": expected_rate,
        "p99_gap_sec": p99_gap,
        "max_gap_sec": max_gap,
        "finite_global": finite_global,
        "overall_quality_0_100": round(float(np.mean([r["quality_0_100"] for r in rows])) if rows else 0.0, 2),
        "boundary": "This is a live signal quality/contact proxy, not true electrode impedance.",
    }
    return rows, summary


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--stream-name", default="obci_eeg1")
    p.add_argument("--duration", type=float, default=20.0)
    p.add_argument("--expected-rate", type=float, default=125.0)
    p.add_argument("--out-dir", default="signal_quality_logs")
    p.add_argument("--max-samples-per-pull", type=int, default=512)
    args = p.parse_args()
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = out_dir / f"signal_quality_channels_{stamp}.csv"
    json_path = out_dir / f"signal_quality_summary_{stamp}.json"
    try:
        from pylsl import resolve_byprop, StreamInlet
    except Exception as exc:
        msg = {"status":"PYLSL_NOT_AVAILABLE", "error":str(exc), "install":"pip install pylsl"}
        json_path.write_text(json.dumps(msg, indent=2), encoding="utf-8")
        print(json.dumps(msg, indent=2)); return 2
    print(f"Resolving LSL stream name={args.stream_name!r}...")
    streams = resolve_byprop("name", args.stream_name, timeout=10)
    if not streams:
        msg = {"status":"STREAM_NOT_FOUND", "stream_name":args.stream_name}
        json_path.write_text(json.dumps(msg, indent=2), encoding="utf-8")
        print(json.dumps(msg, indent=2)); return 3
    inlet = StreamInlet(streams[0], max_buflen=60)
    print(f"Recording {args.duration:.1f}s from {args.stream_name}...")
    samples, times = [], []
    start = time.time()
    while time.time() - start < args.duration:
        chunk, ts = inlet.pull_chunk(timeout=0.5, max_samples=args.max_samples_per_pull)
        if ts:
            samples.extend(chunk); times.extend(ts)
    if not samples:
        msg = {"status":"NO_SAMPLES", "stream_name":args.stream_name}
        json_path.write_text(json.dumps(msg, indent=2), encoding="utf-8")
        print(json.dumps(msg, indent=2)); return 4
    data = np.asarray(samples, dtype=float)
    t = np.asarray(times, dtype=float)
    rows, summary = compute_channel_scores(data, t, args.expected_rate)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    summary["channel_csv"] = str(csv_path)
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
