#!/usr/bin/env python3
from __future__ import annotations

import importlib
import platform
import sys

mods = ["brainflow", "pylsl", "serial", "numpy"]
print("Python:", sys.version)
print("Platform:", platform.platform())
failed = False
for m in mods:
    try:
        mod = importlib.import_module(m)
        version = getattr(mod, "__version__", "unknown")
        print(f"OK: {m} version={version}")
    except Exception as exc:
        failed = True
        print(f"FAIL: {m}: {exc}")
raise SystemExit(1 if failed else 0)
