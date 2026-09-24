#!/usr/bin/env python3
"""Identify likely OpenBCI COM port on Windows/macOS/Linux."""
from __future__ import annotations
import argparse
import time
try:
    from serial.tools import list_ports
except Exception as exc:
    raise SystemExit("pyserial not installed. Run: python -m pip install pyserial\n" + str(exc))


def score_port(p) -> int:
    text = " ".join(str(x or "") for x in [p.device, p.description, p.manufacturer, p.hwid]).lower()
    score = 0
    for key, val in [
        ("openbci",90),("cyton",80),("daisy",50),("rfduino",50),("ftdi",55),("ft232",55),
        ("usb serial",35),("usb-serial",35),("silicon labs",35),("cp210",35),("bluetooth",-80),("modem",-30)
    ]:
        if key in text: score += val
    if getattr(p, "vid", None) == 0x0403: score += 40
    return score


def snapshot():
    rows=[]
    for p in list_ports.comports():
        rows.append({"device":str(p.device or ""), "description":str(p.description or ""), "manufacturer":str(p.manufacturer or ""), "hwid":str(p.hwid or ""), "score":score_port(p)})
    rows.sort(key=lambda r:(r["score"], r["device"]), reverse=True)
    return rows


def print_rows(rows):
    if not rows:
        print("No serial ports detected.")
        return
    for i,r in enumerate(rows,1):
        print(f"[{i}] {r['device']} score={r['score']} | {r['description']} | {r['manufacturer']} | {r['hwid']}")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--watch", action="store_true", help="unplug dongle, press Enter, plug dongle, press Enter; shows newly appeared ports")
    args=ap.parse_args()
    if not args.watch:
        print_rows(snapshot())
        return 0
    input("Unplug the OpenBCI dongle, wait 3 seconds, then press Enter...")
    before={r['device'] for r in snapshot()}
    print("Before:"); print_rows(snapshot())
    input("Now plug the OpenBCI dongle into the USB port you will use, wait 5 seconds, then press Enter...")
    time.sleep(1)
    after_rows=snapshot(); after={r['device'] for r in after_rows}
    new=after-before
    print("\nAfter:"); print_rows(after_rows)
    print("\nNew/appeared ports:")
    print_rows([r for r in after_rows if r['device'] in new])
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
