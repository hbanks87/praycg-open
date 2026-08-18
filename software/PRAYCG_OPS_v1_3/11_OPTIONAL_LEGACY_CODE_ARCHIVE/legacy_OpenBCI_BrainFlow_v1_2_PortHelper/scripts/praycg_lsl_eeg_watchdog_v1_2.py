#!/usr/bin/env python3
"""
PRAYCG LSL EEG Watchdog v1.2

Monitors an active LSL EEG stream and grades sample-flow timing. Use this before
real PR-AYC-G runs and during full-stack video stress tests.
"""
from __future__ import annotations
import argparse, csv, json, time
from pathlib import Path
from typing import List, Tuple
import numpy as np
from pylsl import StreamInlet, resolve_byprop, local_clock


def grade(rate_pct: float, max_gap: float, gaps_gt_250ms: int, dropout: bool) -> str:
    if dropout or rate_pct < 84.0 or max_gap >= 3.0: return 'F'
    if 99.0 <= rate_pct <= 101.0 and max_gap < 0.05 and gaps_gt_250ms == 0: return 'A'
    if 96.0 <= rate_pct <= 102.0 and max_gap < 0.25 and gaps_gt_250ms == 0: return 'B'
    if 84.0 <= rate_pct and max_gap < 3.0: return 'C'
    return 'F'


def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('--stream-name', default='obci_eeg1')
    p.add_argument('--duration', type=float, default=120.0)
    p.add_argument('--expected-rate', type=float, default=125.0)
    p.add_argument('--resolve-timeout', type=float, default=10.0)
    p.add_argument('--pull-timeout', type=float, default=1.0)
    p.add_argument('--max-gap-sec', type=float, default=0.25)
    p.add_argument('--min-rate-frac', type=float, default=0.85)
    p.add_argument('--out-dir', default='lsl_watchdog_logs')
    p.add_argument('--max-samples-per-pull', type=int, default=512)
    args=p.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    stamp=time.strftime('%Y%m%d_%H%M%S')
    chunks_path=out/f'watchdog_{args.stream_name}_{stamp}_chunks.csv'
    summary_path=out/f'watchdog_{args.stream_name}_{stamp}_summary.json'
    streams=resolve_byprop('name', args.stream_name, timeout=args.resolve_timeout)
    if not streams:
        summary={'schema':'PRAYCG_LSL_EEG_Watchdog_v1_2_summary','status':'FAIL_NO_STREAM','stream_name':args.stream_name}
        summary_path.write_text(json.dumps(summary,indent=2),encoding='utf-8')
        print(json.dumps(summary,indent=2)); return 2
    inlet=StreamInlet(streams[0], max_chunklen=args.max_samples_per_pull)
    info=streams[0]
    start=local_clock(); end=start+args.duration
    all_ts: List[float]=[]; chunks=[]; last_sample=None; dropout=False
    with chunks_path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=['unix_time','lsl_time','chunk_samples','first_ts','last_ts','gap_from_prev_sec','elapsed_sec'])
        w.writeheader()
        while local_clock() < end:
            samples, ts = inlet.pull_chunk(timeout=args.pull_timeout, max_samples=args.max_samples_per_pull)
            now=local_clock()
            if ts:
                gap=(ts[0]-last_sample) if last_sample is not None else 0.0
                if gap > 3.0: dropout=True
                all_ts.extend(ts); last_sample=ts[-1]
                row={'unix_time':time.time(),'lsl_time':now,'chunk_samples':len(ts),'first_ts':ts[0],'last_ts':ts[-1],'gap_from_prev_sec':gap,'elapsed_sec':now-start}
                w.writerow(row); f.flush(); chunks.append(row)
            else:
                if last_sample is not None and (now-last_sample)>3.0: dropout=True
    ts_arr=np.array(all_ts,dtype=float)
    if len(ts_arr)>1:
        diffs=np.diff(ts_arr); dur=ts_arr[-1]-ts_arr[0]; eff=(len(ts_arr)-1)/dur if dur>0 else 0
        max_gap=float(np.max(diffs)); p99=float(np.percentile(diffs,99)); gaps250=int(np.sum(diffs>0.25)); gaps050=int(np.sum(diffs>0.05))
    else:
        eff=0.0; max_gap=999.0; p99=999.0; gaps250=0; gaps050=0; dur=0.0
    min_samples=int(args.duration*args.expected_rate*args.min_rate_frac)
    rate_pct=100.0*eff/args.expected_rate if args.expected_rate else 0.0
    g=grade(rate_pct,max_gap,gaps250,dropout)
    summary={
        'schema':'PRAYCG_LSL_EEG_Watchdog_v1_2_summary','status':'PASS' if g in ['A','B'] else 'PASS_CAUTION' if g=='C' else 'FAIL',
        'timing_grade':g,'stream_name':args.stream_name,'stream_type':info.type(),'source_id':info.source_id(),
        'channel_count':info.channel_count(),'nominal_srate':info.nominal_srate(),'duration_requested_sec':args.duration,
        'samples_total':len(all_ts),'expected_min_samples':min_samples,'effective_rate_hz':eff,'effective_rate_percent_nominal':rate_pct,
        'max_gap_sec':max_gap,'p99_gap_sec':p99,'gaps_gt_250ms':gaps250,'gaps_gt_50ms':gaps050,
        'gap_threshold_sec':args.max_gap_sec,'pass_rate':len(all_ts)>=min_samples and eff>=args.expected_rate*args.min_rate_frac,
        'pass_samples':len(all_ts)>=min_samples,'pass_gap':max_gap<=args.max_gap_sec,'dropout_detected':dropout,
        'chunks_csv':str(chunks_path),'args':vars(args)
    }
    summary_path.write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
    return 0 if summary['status'].startswith('PASS') else 1

if __name__=='__main__':
    raise SystemExit(main())
