#!/usr/bin/env python3
"""
PRAYCG LSL Stream Checker v0.1
Lists visible Lab Streaming Layer streams and optionally repeats for a fixed duration.
"""
from __future__ import annotations
import argparse, csv, json, time, sys
from pathlib import Path
from datetime import datetime


def main() -> int:
    p = argparse.ArgumentParser(description="Check visible LSL streams for PRAYCG acquisition setup.")
    p.add_argument("--duration", type=float, default=5.0, help="Seconds to monitor")
    p.add_argument("--period", type=float, default=1.0, help="Polling interval")
    p.add_argument("--out-dir", default="lsl_stream_check_logs", help="Output directory")
    p.add_argument("--required", nargs="*", default=["obci_eeg1", "OpenBCIStatusMarkers", "PolarHRV", "VernierRespirationBelt"], help="Stream names expected")
    args = p.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = out_dir / f"lsl_stream_check_{stamp}.csv"
    json_path = out_dir / f"lsl_stream_check_{stamp}.json"

    try:
        from pylsl import resolve_streams
    except Exception as exc:
        msg = {
            "status": "PYLSL_NOT_AVAILABLE",
            "error": str(exc),
            "install": "pip install pylsl",
        }
        json_path.write_text(json.dumps(msg, indent=2), encoding="utf-8")
        print(json.dumps(msg, indent=2))
        return 2

    rows = []
    start = time.time()
    print("PRAYCG LSL Stream Checker v0.1")
    print(f"Monitoring for {args.duration:.1f} seconds...\n")
    while time.time() - start <= args.duration:
        t = time.time()
        try:
            streams = resolve_streams(wait_time=0.6)
        except Exception as exc:
            print(f"Resolve error: {exc}")
            streams = []
        if streams:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {len(streams)} stream(s) visible")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] no streams visible")
        seen_names = set()
        for s in streams:
            d = {
                "poll_unix_time": t,
                "name": s.name(),
                "type": s.type(),
                "source_id": s.source_id(),
                "channel_count": s.channel_count(),
                "nominal_srate": s.nominal_srate(),
                "hostname": s.hostname(),
            }
            rows.append(d)
            seen_names.add(s.name())
            print(f"  - {d['name']} | type={d['type']} | ch={d['channel_count']} | srate={d['nominal_srate']} | source={d['source_id']}")
        missing = [x for x in args.required if x not in seen_names]
        if missing:
            print("  missing required/expected:", ", ".join(missing))
        print()
        time.sleep(max(0.1, args.period))

    if rows:
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
    names = sorted({r["name"] for r in rows})
    summary = {
        "schema": "PRAYCG_LSL_Stream_Check_v0_1",
        "created_local": datetime.now().isoformat(timespec="seconds"),
        "duration_sec": args.duration,
        "streams_seen": names,
        "required": args.required,
        "missing_final": [x for x in args.required if x not in names],
        "csv_path": str(csv_path) if rows else None,
    }
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("Summary:")
    print(json.dumps(summary, indent=2))
    return 0 if not summary["missing_final"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
