#!/usr/bin/env python3
"""PRAYCG1.6K StasisMarkers LSL smoke test.

Use before a real run.
1. Run this script.
2. Open LabRecorder.
3. Click Update, confirm StasisMarkers appears, check it, and record 20-30 seconds.
4. Stop recording.
5. Run verify_xdf_stasis_markers.py on the saved XDF.
"""
from __future__ import annotations
import time, uuid
from pylsl import StreamInfo, StreamOutlet, local_clock

source_id = f"praycg_stasismarkers_smoke_{uuid.uuid4().hex[:10]}"
info = StreamInfo("StasisMarkers", "Markers", 1, 0, "string", source_id)
info.desc().append_child_value("protocol", "PRAYCG")
info.desc().append_child_value("test", "stasis_marker_smoke_test")
outlet = StreamOutlet(info, chunk_size=1, max_buffered=3600)
print("StasisMarkers smoke-test stream is online.")
print("Open LabRecorder -> Update -> check StasisMarkers -> Start recording.")
print("Sending one marker per second for 60 seconds. Press Ctrl+C to stop early.")
time.sleep(1.0)
try:
    for i in range(1, 61):
        marker = f"SMOKE_TEST_STASIS_MARKER_{i:03d}"
        ts = local_clock()
        try:
            outlet.push_sample([marker], timestamp=ts, pushthrough=True)
        except TypeError:
            outlet.push_sample([marker], timestamp=ts)
        print(f"{marker} @ {ts:.6f}")
        time.sleep(1.0)
finally:
    ts = local_clock()
    try:
        outlet.push_sample(["SMOKE_TEST_END"], timestamp=ts, pushthrough=True)
    except TypeError:
        outlet.push_sample(["SMOKE_TEST_END"], timestamp=ts)
    print("Smoke test ended.")
