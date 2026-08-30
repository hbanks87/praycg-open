#!/usr/bin/env python3
"""List visible LSL streams."""
from __future__ import annotations
import argparse
try:
    from pylsl import resolve_streams
except Exception as exc:
    raise SystemExit("pylsl not installed. Run: python -m pip install pylsl\n" + str(exc))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--timeout", type=float, default=5.0)
    args=ap.parse_args()
    streams=resolve_streams(wait_time=args.timeout)
    print(f"Found {len(streams)} LSL stream(s).")
    for s in streams:
        print(f"name={s.name()} | type={s.type()} | channels={s.channel_count()} | srate={s.nominal_srate()} | source_id={s.source_id()}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
