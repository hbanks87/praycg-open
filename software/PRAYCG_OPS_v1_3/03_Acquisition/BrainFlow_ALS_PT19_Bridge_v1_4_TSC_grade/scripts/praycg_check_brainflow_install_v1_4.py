#!/usr/bin/env python3
"""Installation sanity check for BrainFlow + pylsl + pyserial."""
from __future__ import annotations
import platform, sys
print("Python:", sys.version)
print("Executable:", sys.executable)
print("Platform:", platform.platform())
try:
    import numpy as np
    print("numpy:", np.__version__)
except Exception as e:
    print("numpy import FAILED:", repr(e))
try:
    import pylsl
    print("pylsl imported OK")
except Exception as e:
    print("pylsl import FAILED:", repr(e))
try:
    import serial
    print("pyserial:", serial.__version__)
except Exception as e:
    print("pyserial import FAILED:", repr(e))
try:
    import brainflow
    print("brainflow imported OK")
    from brainflow.board_shim import BoardShim, BoardIds
    for label,bid in [("cyton",BoardIds.CYTON_BOARD.value),("cyton-daisy",BoardIds.CYTON_DAISY_BOARD.value)]:
        print("\nBoard", label, bid)
        for name in ["get_sampling_rate","get_eeg_channels","get_accel_channels","get_analog_channels","get_package_num_channel","get_timestamp_channel"]:
            try:
                print(" ", name, getattr(BoardShim,name)(bid))
            except Exception as e:
                print(" ", name, "ERR", repr(e))
except Exception as e:
    print("brainflow import FAILED:", repr(e))
try:
    from serial.tools import list_ports
    print("\nSerial ports:")
    for p in list_ports.comports():
        print(f"  {p.device}: {p.description} | {p.manufacturer} | {p.hwid}")
except Exception as e:
    print("list ports FAILED:", repr(e))
