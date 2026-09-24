#!/usr/bin/env python3
"""PRAYCG XDF EEG Timing Grade Verifier v1.2.

Loads an XDF and grades EEG stream timing. Works best on BrainFlow-to-LSL
recordings, but also supports OpenBCI GUI streams.
"""
from __future__ import annotations
import argparse, json, csv, math, sys
from pathlib import Path
from typing import Any, Dict, List
import numpy as np
try:
    import pyxdf
except Exception as exc:
    raise SystemExit('Install pyxdf first: pip install pyxdf\n'+str(exc))

def grade(rate_pct: float, max_gap: float, gaps_gt_250ms: int, sample_count: int, duration: float) -> str:
    if sample_count <= 0 or duration <= 0: return 'F'
    if rate_pct < 84.0 or max_gap >= 3.0: return 'F'
    if 99.0 <= rate_pct <= 101.0 and max_gap < 0.05 and gaps_gt_250ms == 0: return 'A'
    if 96.0 <= rate_pct <= 102.0 and max_gap < 0.25 and gaps_gt_250ms == 0: return 'B'
    return 'C'

def stream_name(s: Dict[str, Any]) -> str:
    return s.get('info',{}).get('name',[''])[0]

def stream_type(s: Dict[str, Any]) -> str:
    return s.get('info',{}).get('type',[''])[0]

def nominal_rate(s: Dict[str, Any]) -> float:
    try: return float(s.get('info',{}).get('nominal_srate',['0'])[0])
    except Exception: return 0.0

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('xdf')
    p.add_argument('--eeg-stream-name', default='obci_eeg1')
    p.add_argument('--expected-rate', type=float, default=125.0)
    p.add_argument('--out-dir', default='xdf_timing_qc')
    args=p.parse_args()
    xdf_path=Path(args.xdf)
    out=Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    streams, header = pyxdf.load_xdf(str(xdf_path))
    rows=[]
    for s in streams:
        name=stream_name(s); typ=stream_type(s); ts=np.asarray(s.get('time_stamps',[]),dtype=float); n=len(ts)
        sr=nominal_rate(s); duration=float(ts[-1]-ts[0]) if n>1 else 0.0
        eff=float((n-1)/duration) if n>1 and duration>0 else 0.0
        diffs=np.diff(ts) if n>1 else np.array([])
        max_gap=float(np.max(diffs)) if len(diffs) else 0.0
        p99=float(np.percentile(diffs,99)) if len(diffs) else 0.0
        gaps250=int(np.sum(diffs>0.25)) if len(diffs) else 0
        gaps050=int(np.sum(diffs>0.05)) if len(diffs) else 0
        rate_base=args.expected_rate if name==args.eeg_stream_name else sr
        rate_pct=100.0*eff/rate_base if rate_base else 0.0
        g=grade(rate_pct,max_gap,gaps250,n,duration) if name==args.eeg_stream_name else ''
        rows.append({'name':name,'type':typ,'nominal_srate':sr,'sample_count':n,'duration_sec':duration,'effective_rate_hz':eff,
                     'effective_rate_percent_expected':rate_pct,'max_gap_sec':max_gap,'p99_gap_sec':p99,
                     'gaps_gt_50ms':gaps050,'gaps_gt_250ms':gaps250,'timing_grade':g})
    csv_path=out/(xdf_path.stem+'_stream_timing_summary.csv')
    with csv_path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ['name'])
        w.writeheader(); w.writerows(rows)
    eeg=[r for r in rows if r['name']==args.eeg_stream_name]
    summary={'schema':'PRAYCG_XDF_EEG_TimingGrade_v1_2','xdf':str(xdf_path),'eeg_stream_name':args.eeg_stream_name,
             'eeg_found':bool(eeg),'eeg_summary':eeg[0] if eeg else None,'all_streams':rows,'csv':str(csv_path)}
    json_path=out/(xdf_path.stem+'_xdf_timing_grade_summary.json')
    json_path.write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
    if not eeg or eeg[0]['timing_grade']=='F': return 1
    return 0

if __name__=='__main__':
    raise SystemExit(main())
