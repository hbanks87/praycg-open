#!/usr/bin/env python3
"""Backward-compatible launcher alias. Runs the packaged v1.3 script."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('praycg_master_comprehensive_suite_gui_v1_3.py')), run_name='__main__')
