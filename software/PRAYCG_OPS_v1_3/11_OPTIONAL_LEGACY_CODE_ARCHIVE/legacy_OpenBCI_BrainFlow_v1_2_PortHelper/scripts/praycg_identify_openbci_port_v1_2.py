#!/usr/bin/env python3
"""
PRAYCG OpenBCI Port Identifier v1.2

Lists available Windows COM ports and ranks the likely OpenBCI dongle port.
Use this first on a new laptop.

Examples:
    python praycg_identify_openbci_port_v1_2.py
    python praycg_identify_openbci_port_v1_2.py --watch
    python praycg_identify_openbci_port_v1_2.py --json-out ports.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from typing import List, Optional

try:
    from serial.tools import list_ports
except Exception as exc:
    raise SystemExit(
        "Could not import pyserial. Install with: pip install pyserial\n"
        f"Original import error: {exc}"
    )

@dataclass
class PortInfo:
    device: str
    description: str
    manufacturer: str
    hwid: str
    vid: Optional[int]
    pid: Optional[int]
    serial_number: str
    location: str
    score: int
    reasons: List[str]


def score_port(p) -> tuple[int, List[str]]:
    text = " ".join(str(x or "") for x in [p.device, p.description, p.manufacturer, p.hwid]).lower()
    score = 0
    reasons: List[str] = []
    positive = [
        ("openbci", 90), ("cyton", 80), ("daisy", 50), ("rfduino", 50),
        ("ftdi", 55), ("ft232", 55), ("usb serial", 35), ("usb-serial", 35),
        ("silicon labs", 35), ("cp210", 35), ("com", 5),
        ("wch", 15), ("ch340", 15), ("arduino", 10),
    ]
    negative = [("bluetooth", -80), ("standard serial over bluetooth", -100), ("modem", -30)]
    for key, val in positive:
        if key in text:
            score += val; reasons.append(f"+{val}:{key}")
    for key, val in negative:
        if key in text:
            score += val; reasons.append(f"{val}:{key}")
    # FTDI VID is common for OpenBCI dongles, but not unique.
    if getattr(p, "vid", None) == 0x0403:
        score += 40; reasons.append("+40:VID_0403_FTDI")
    return score, reasons


def get_ports() -> List[PortInfo]:
    out: List[PortInfo] = []
    for p in list_ports.comports():
        score, reasons = score_port(p)
        out.append(PortInfo(
            device=str(p.device or ""),
            description=str(p.description or ""),
            manufacturer=str(p.manufacturer or ""),
            hwid=str(p.hwid or ""),
            vid=getattr(p, "vid", None),
            pid=getattr(p, "pid", None),
            serial_number=str(getattr(p, "serial_number", "") or ""),
            location=str(getattr(p, "location", "") or ""),
            score=score,
            reasons=reasons,
        ))
    out.sort(key=lambda x: (x.score, x.device), reverse=True)
    return out


def print_ports(ports: List[PortInfo], title: str = "Detected serial ports") -> None:
    print("\n" + title)
    print("=" * len(title))
    if not ports:
        print("No serial ports detected.")
        return
    for i, p in enumerate(ports, 1):
        print(f"\n[{i}] {p.device}   score={p.score}")
        print(f"    description : {p.description}")
        print(f"    manufacturer: {p.manufacturer}")
        print(f"    hwid        : {p.hwid}")
        if p.vid is not None or p.pid is not None:
            print(f"    VID:PID     : {p.vid!s}:{p.pid!s}")
        if p.serial_number:
            print(f"    serial      : {p.serial_number}")
        if p.location:
            print(f"    location    : {p.location}")
        print(f"    reasons     : {', '.join(p.reasons) if p.reasons else '(none)'}")
    best = ports[0]
    print("\nMost likely OpenBCI port:", best.device if best.score > 0 else "not obvious")
    if best.score > 0:
        print("Example command:")
        print(f"  python praycg_openbci_brainflow_to_lsl_v1_2.py --board cyton-daisy --serial-port {best.device} --stream-name obci_eeg1 --timestamp-mode reconstructed --confirmed-channel-map")


def main() -> int:
    ap = argparse.ArgumentParser(description="Identify likely OpenBCI / Cyton COM port on Windows.")
    ap.add_argument("--watch", action="store_true", help="Before/after plug-in helper. Unplug dongle, run, press Enter, plug it in, press Enter.")
    ap.add_argument("--json-out", default="", help="Optional JSON output path.")
    ap.add_argument("--repeat", type=float, default=0.0, help="Continuously print ports every N seconds until Ctrl+C.")
    args = ap.parse_args()

    if args.watch:
        input("Unplug the OpenBCI dongle, then press ENTER...")
        before = {p.device for p in get_ports()}
        print_ports(get_ports(), "Ports BEFORE plugging OpenBCI dongle")
        input("Now plug the OpenBCI dongle into the USB port you plan to use, wait 3-5 seconds, then press ENTER...")
        after_ports = get_ports()
        after = {p.device for p in after_ports}
        new_devices = after - before
        print_ports(after_ports, "Ports AFTER plugging OpenBCI dongle")
        if new_devices:
            print("\nNew port(s) that appeared:", ", ".join(sorted(new_devices)))
        else:
            print("\nNo new COM port appeared. Try a different USB port, check dongle seating, or install the USB serial driver.")
    elif args.repeat > 0:
        try:
            while True:
                print_ports(get_ports(), f"Detected serial ports at {time.strftime('%H:%M:%S')}")
                time.sleep(args.repeat)
        except KeyboardInterrupt:
            return 0
    else:
        ports = get_ports()
        print_ports(ports)
        if args.json_out:
            with open(args.json_out, "w", encoding="utf-8") as f:
                json.dump([asdict(p) for p in ports], f, indent=2)
            print(f"\nWrote: {args.json_out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
