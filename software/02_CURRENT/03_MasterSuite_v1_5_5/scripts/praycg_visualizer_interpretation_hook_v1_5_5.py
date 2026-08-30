#!/usr/bin/env python3
"""
PRAYCG Visualizer Interpretation Hook v1.5.5

Small helper intended to be called after the MasterSync Visualizer renders an MP4.
It writes the offline deterministic interpretation report next to the video or inside
<analysis-folder>/report. This lets the visualizer workflow produce both:

1. a synchronized MP4 review artifact, and
2. a human-readable text/Markdown/JSON interpretation artifact.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

# Import sibling reporter without requiring package installation.
THIS = Path(__file__).resolve().parent
if str(THIS) not in sys.path:
    sys.path.insert(0, str(THIS))

from praycg_offline_interpretation_reporter_v1_5_5 import generate_report


def main() -> None:
    ap = argparse.ArgumentParser(description='Run offline interpretation report after a visualizer render.')
    ap.add_argument('--analysis-folder', required=True, help='Master Suite output folder')
    ap.add_argument('--render-report-json', default='', help='Optional visualizer render_report.json for provenance')
    ap.add_argument('--out-dir', default='', help='Output directory. Default: <analysis-folder>/report')
    ap.add_argument('--project-name', default='', help='Optional project/run label')
    args = ap.parse_args()

    analysis_folder = Path(args.analysis_folder).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else analysis_folder / 'report'
    payload = generate_report(analysis_folder, out_dir)

    if args.render_report_json:
        rr = Path(args.render_report_json).expanduser().resolve()
        provenance_path = out_dir / 'offline_interpretation_visualizer_provenance.json'
        prov = {'render_report_json': str(rr), 'offline_report_json': payload['json']}
        if rr.exists():
            try:
                prov['render_report'] = json.loads(rr.read_text(encoding='utf-8'))
            except Exception as e:
                prov['render_report_parse_error'] = str(e)
        provenance_path.write_text(json.dumps(prov, indent=2), encoding='utf-8')
        print(f"Wrote visualizer provenance: {provenance_path}")

    print(f"Wrote offline interpretation report to: {out_dir}")


if __name__ == '__main__':
    main()
