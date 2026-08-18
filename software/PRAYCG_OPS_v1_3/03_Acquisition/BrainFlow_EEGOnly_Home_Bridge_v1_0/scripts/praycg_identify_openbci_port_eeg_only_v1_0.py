#!/usr/bin/env python3
"""Identify the likely OpenBCI USB dongle COM port by before/after comparison."""
from __future__ import annotations

import argparse
import sys
from typing import Dict, Set

try:
    import serial.tools.list_ports
except Exception as exc:
    print("pyserial is required. Install with: python -m pip install pyserial", file=sys.stderr)
    raise


def snapshot() -> Dict[str, str]:
    out = {}
    for p in serial.tools.list_ports.comports():
        out[p.device] = f"{p.description} | hwid={p.hwid}"
    return out


def print_ports(title: str, ports: Dict[str, str]) -> None:
    print(f"\n{title}")
    if not ports:
        print("  No serial ports detected.")
        return
    for dev, desc in sorted(ports.items()):
        print(f"  {dev:10s} | {desc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Find OpenBCI COM port by unplug/replug comparison.")
    parser.add_argument("--watch", action="store_true", help="Interactive unplug/replug workflow")
    args = parser.parse_args()

    if not args.watch:
        print_ports("Current serial ports:", snapshot())
        return 0

    input("Unplug the OpenBCI dongle, then press ENTER...")
    before = snapshot()
    print_ports("Ports while dongle is unplugged:", before)
    input("Plug the OpenBCI dongle back in, wait 3 seconds, then press ENTER...")
    after = snapshot()
    print_ports("Ports after replug:", after)
    new_ports: Set[str] = set(after) - set(before)
    if new_ports:
        print("\nLikely OpenBCI port(s):")
        for dev in sorted(new_ports):
            print(f"  {dev} | {after[dev]}")
        return 0
    print("\nNo new port detected. Try Device Manager > Ports (COM & LPT), another USB port, or reinstall drivers.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
