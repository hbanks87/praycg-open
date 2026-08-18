#!/usr/bin/env python3
"""Verify whether an XDF contains the PRAYCG StasisMarkers stream."""
from __future__ import annotations
import argparse, sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("xdf", help="Path to LabRecorder .xdf file")
    args = ap.parse_args()
    try:
        import pyxdf
    except Exception as e:
        print("ERROR: pyxdf is required. Install with: pip install pyxdf")
        print(e)
        return 2
    xdf_path = Path(args.xdf)
    if not xdf_path.exists():
        print(f"ERROR: file not found: {xdf_path}")
        return 2
    streams, header = pyxdf.load_xdf(str(xdf_path))
    found = []
    print("Streams in XDF:")
    for idx, s in enumerate(streams):
        info = s.get("info", {})
        name = info.get("name", [""])[0]
        typ = info.get("type", [""])[0]
        sid = info.get("source_id", [""])[0]
        n = len(s.get("time_stamps", []))
        print(f"  {idx:02d}: name={name!r} type={typ!r} source_id={sid!r} samples={n}")
        if name == "StasisMarkers" or typ == "Markers":
            found.append((idx, name, typ, sid, n, s))
    if not found:
        print("\nFAIL: No StasisMarkers/Markers stream found in this XDF.")
        print("This means LabRecorder did not record the marker stream, regardless of local JSON logs.")
        return 1
    print("\nMarker streams found:")
    for idx, name, typ, sid, n, s in found:
        print(f"  stream {idx}: name={name!r}, type={typ!r}, source_id={sid!r}, samples={n}")
        series = s.get("time_series", [])
        for j in range(min(10, len(series))):
            print(f"    sample[{j}] = {series[j]}")
    print("\nPASS: marker stream present in XDF.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
