#!/usr/bin/env python3
"""ALS-PT19 LSL watchdog: confirms the light timing pulse is visible."""
from __future__ import annotations
import argparse, csv, json, time
from pathlib import Path
import numpy as np
try:
    from pylsl import StreamInlet, resolve_byprop, local_clock
except Exception as exc:
    raise SystemExit("pylsl not installed. Run: python -m pip install pylsl\n" + str(exc))

def robust_edges(t, x, threshold):
    above = x >= threshold
    edges=[]
    for i in range(1,len(x)):
        if bool(above[i]) and not bool(above[i-1]):
            edges.append(float(t[i]))
    return edges

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--stream-name", default="ALS_PT19_Timing")
    ap.add_argument("--duration", type=float, default=30.0)
    ap.add_argument("--resolve-timeout", type=float, default=10.0)
    ap.add_argument("--out-dir", default="als_pt19_watchdog_logs")
    ap.add_argument("--min-amplitude", type=float, default=20.0, help="minimum max-min amplitude in raw stream units; adjust if needed")
    ap.add_argument("--expected-pulses", type=int, default=1)
    ap.add_argument("--threshold-frac", type=float, default=0.5, help="threshold = min + frac*(max-min)")
    args=ap.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    streams=resolve_byprop("name", args.stream_name, timeout=args.resolve_timeout)
    if not streams:
        raise SystemExit(f"Could not find LSL stream named {args.stream_name!r}. Start the BrainFlow bridge first.")
    inlet=StreamInlet(streams[0], max_buflen=120)
    samples=[]; times=[]
    t0=local_clock(); last_print=0
    print(f"Recording {args.stream_name} for {args.duration:.1f} seconds. Move sensor / play timing-pulse video now if needed.")
    while local_clock()-t0 < args.duration:
        chunk, stamps = inlet.pull_chunk(timeout=0.25, max_samples=256)
        if stamps:
            for row,ts in zip(chunk,stamps):
                samples.append(float(row[0])); times.append(float(ts))
        if time.time()-last_print > 2:
            last_print=time.time(); print(f"samples={len(samples)}", flush=True)
    if not samples:
        raise SystemExit("No ALS samples received.")
    t=np.asarray(times); x=np.asarray(samples)
    xmin=float(np.nanmin(x)); xmax=float(np.nanmax(x)); xmean=float(np.nanmean(x)); amp=xmax-xmin
    thresh=xmin+args.threshold_frac*amp
    edges=robust_edges(t,x,thresh) if amp > 0 else []
    pass_amp=amp >= args.min_amplitude
    pass_pulses=len(edges) >= args.expected_pulses
    status="PASS" if pass_amp and pass_pulses else "CHECK"
    stamp=time.strftime("%Y%m%d_%H%M%S")
    summary={
        "schema":"PRAYCG_ALS_PT19_Watchdog_v1_4",
        "status":status,
        "stream_name":args.stream_name,
        "duration_sec":args.duration,
        "samples":int(len(samples)),
        "min":xmin,
        "max":xmax,
        "mean":xmean,
        "amplitude":float(amp),
        "threshold":float(thresh),
        "rising_edges_detected":int(len(edges)),
        "rising_edge_lsl_times":edges[:20],
        "pass_amplitude":bool(pass_amp),
        "pass_expected_pulses":bool(pass_pulses),
        "args":vars(args),
    }
    (out/f"als_pt19_watchdog_summary_{stamp}.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    with (out/f"als_pt19_samples_{stamp}.csv").open("w", newline="", encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["lsl_time","als_value"]); w.writerows(zip(t.tolist(),x.tolist()))
    print(json.dumps(summary, indent=2))
    return 0 if status == "PASS" else 1
if __name__ == "__main__":
    raise SystemExit(main())
