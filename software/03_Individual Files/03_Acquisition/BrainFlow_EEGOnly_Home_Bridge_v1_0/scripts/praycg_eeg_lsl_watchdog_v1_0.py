#!/usr/bin/env python3
"""Simple LSL EEG stream watchdog for the EEG-only bridge."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from pylsl import StreamInlet, resolve_byprop


def main() -> int:
    p = argparse.ArgumentParser(description="Verify an LSL EEG stream is present and publishing at expected rate.")
    p.add_argument("--stream-name", default="obci_eeg1")
    p.add_argument("--duration", type=float, default=120.0)
    p.add_argument("--expected-rate", type=float, default=125.0)
    p.add_argument("--min-rate-frac", type=float, default=0.85)
    p.add_argument("--max-gap-sec", type=float, default=0.25)
    p.add_argument("--resolve-timeout", type=float, default=10.0)
    p.add_argument("--pull-timeout", type=float, default=1.0)
    p.add_argument("--out-dir", default="lsl_watchdog_logs")
    args = p.parse_args()

    streams = resolve_byprop("name", args.stream_name, timeout=args.resolve_timeout)
    if not streams:
        print(f"No stream named {args.stream_name!r} found.")
        return 1
    inlet = StreamInlet(streams[0], max_buflen=60)
    timestamps = []
    samples = []
    t0 = None
    while True:
        chunk, ts = inlet.pull_chunk(timeout=args.pull_timeout, max_samples=512)
        if ts:
            if t0 is None:
                t0 = ts[0]
            timestamps.extend(ts)
            samples.extend(chunk)
        if t0 is not None and timestamps and (timestamps[-1] - t0) >= args.duration:
            break

    ts_arr = np.asarray(timestamps, dtype=float)
    n = int(len(ts_arr))
    duration_observed = float(ts_arr[-1] - ts_arr[0]) if n > 1 else 0.0
    eff_rate = n / duration_observed if duration_observed > 0 else 0.0
    gaps = np.diff(ts_arr) if n > 1 else np.array([])
    max_gap = float(np.max(gaps)) if gaps.size else 0.0
    p99_gap = float(np.quantile(gaps, 0.99)) if gaps.size else 0.0

    result = {
        "schema": "PRAYCG_LSL_EEG_Watchdog_EEGOnly_v1_0_summary",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "stream_name": args.stream_name,
        "stream_type": streams[0].type(),
        "source_id": streams[0].source_id(),
        "channel_count": streams[0].channel_count(),
        "nominal_srate": streams[0].nominal_srate(),
        "duration_requested_sec": args.duration,
        "samples_total": n,
        "effective_rate_hz": eff_rate,
        "max_gap_sec": max_gap,
        "p99_gap_sec": p99_gap,
        "pass_rate": eff_rate >= args.expected_rate * args.min_rate_frac,
        "pass_gap": max_gap <= args.max_gap_sec,
    }
    result["status"] = "PASS" if result["pass_rate"] and result["pass_gap"] else "WARN_OR_FAIL"

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"eegonly_watchdog_{args.stream_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"Wrote: {out_path}")
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
