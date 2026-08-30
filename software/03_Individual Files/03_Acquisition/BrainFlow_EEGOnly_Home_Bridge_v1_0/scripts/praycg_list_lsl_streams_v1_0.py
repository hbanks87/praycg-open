#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pylsl import resolve_streams


def main() -> int:
    p = argparse.ArgumentParser(description="List visible LSL streams.")
    p.add_argument("--wait", type=float, default=5.0, help="Seconds to wait for streams")
    args = p.parse_args()
    streams = resolve_streams(wait_time=args.wait)
    if not streams:
        print("No LSL streams found.")
        return 1
    print(f"Found {len(streams)} LSL stream(s):")
    for s in streams:
        print(
            f"  name={s.name()} | type={s.type()} | channels={s.channel_count()} | "
            f"srate={s.nominal_srate()} | source_id={s.source_id()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
