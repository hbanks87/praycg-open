#!/usr/bin/env python3
"""
PRAYCG LSO/SPM Subtitle Override Module v1.4.7

Parses subtitle schedules and estimates lexical extraction cost and subtitle phase mapping.
Does not prove comprehension or memory encoding.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd


def parse_srt(path: Path) -> pd.DataFrame:
    text=path.read_text(encoding='utf-8', errors='ignore')
    blocks=re.split(r'\n\s*\n', text.strip())
    rows=[]
    def to_sec(t):
        h,m,sms=t.strip().replace(',', '.').split(':')
        s=float(sms)
        return int(h)*3600+int(m)*60+s
    for b in blocks:
        lines=[l.strip() for l in b.splitlines() if l.strip()]
        if len(lines)>=2 and '-->' in lines[1]:
            idx=lines[0]
            a,btime=lines[1].split('-->')[:2]
            txt=' '.join(lines[2:])
            rows.append({'line_id':idx,'subtitle_onset_sec':to_sec(a),'subtitle_offset_sec':to_sec(btime),'text':txt})
    return pd.DataFrame(rows)


def z(x):
    x=pd.to_numeric(pd.Series(x), errors='coerce')
    med=np.nanmedian(x); mad=np.nanmedian(np.abs(x-med)); den=1.4826*mad if mad and np.isfinite(mad) else np.nanstd(x)
    if not den or not np.isfinite(den): den=1.0
    return (x-med)/(den+1e-9)


def load_subs(p: Path):
    if p.suffix.lower()=='.srt': return parse_srt(p)
    return pd.read_csv(p)


def find_col(df, names):
    low={c.lower():c for c in df.columns}
    for n in names:
        if n in df.columns: return n
        if n.lower() in low: return low[n.lower()]
    for c in df.columns:
        if any(n.lower() in c.lower() for n in names): return c
    return None


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--analysis-folder', required=True)
    ap.add_argument('--subtitle-file', required=True, help='SRT or CSV with subtitle_onset_sec, subtitle_offset_sec, text')
    ap.add_argument('--feature-csv', default='')
    ap.add_argument('--gaze-csv', default='')
    ap.add_argument('--audio-anchor-csv', default='')
    ap.add_argument('--out-dir', default='')
    args=ap.parse_args()
    root=Path(args.analysis_folder)
    tables=Path(args.out_dir) if args.out_dir else root/'tables'
    tables.mkdir(parents=True, exist_ok=True)
    subs=load_subs(Path(args.subtitle_file))
    if 'subtitle_onset_sec' not in subs.columns:
        raise SystemExit('subtitle file must include subtitle_onset_sec')
    if 'subtitle_offset_sec' not in subs.columns:
        raise SystemExit('subtitle file must include subtitle_offset_sec')
    if 'text' not in subs.columns:
        subs['text']=''
    subs['char_count']=subs['text'].astype(str).str.len()
    subs['word_count']=subs['text'].astype(str).str.split().map(len)
    dur=(pd.to_numeric(subs['subtitle_offset_sec'])-pd.to_numeric(subs['subtitle_onset_sec'])).clip(lower=0.01)
    subs['chars_per_sec']=subs['char_count']/dur
    subs['words_per_sec']=subs['word_count']/dur
    subs['line_count']=subs['text'].astype(str).str.count(r'\\n')+1
    subs['LEC']=0.45*z(subs['chars_per_sec'])+0.35*z(subs['words_per_sec'])+0.20*z(subs['line_count'])
    subs['semantic_anchor_estimate_sec']=(pd.to_numeric(subs['subtitle_onset_sec'])+pd.to_numeric(subs['subtitle_offset_sec']))/2.0
    subs['anchor_method']='subtitle_midpoint_fallback'

    # feature-based TSP/MeaningGamma argmax fallback if available
    fpath=Path(args.feature_csv) if args.feature_csv else None
    if not fpath or not fpath.exists():
        for pat in ['human_translation_kht_feature_frame.csv','*_time_resolved_feature_frame.csv','*feature_frame*.csv']:
            hits=list((root/'tables').glob(pat))
            if hits:
                fpath=hits[0]; break
    if fpath and fpath.exists():
        feat=pd.read_csv(fpath)
        tcol=find_col(feat,['time_sec','condition_offset_sec','phase_time_sec','time'])
        tsp=find_col(feat,['tsp_z','TSP','temporal_semantic_proxy'])
        gamma=find_col(feat,['MeaningGamma','meaninggamma','gamma_z','lgamma'])
        art=find_col(feat,['artifact_score','artifact'])
        if tcol and (tsp or gamma):
            times=pd.to_numeric(feat[tcol], errors='coerce')
            score=np.zeros(len(feat), dtype=float)
            if tsp: score+=pd.to_numeric(feat[tsp], errors='coerce').fillna(0).to_numpy()
            if gamma: score+=pd.to_numeric(feat[gamma], errors='coerce').fillna(0).to_numpy()
            if art: score-=pd.to_numeric(feat[art], errors='coerce').fillna(0).to_numpy()
            anchors=[]
            methods=[]
            for _,r in subs.iterrows():
                start=float(r['subtitle_onset_sec'])-2.0
                end=float(r['subtitle_offset_sec'])+1.0
                mask=(times>=start)&(times<=end)
                if mask.any():
                    idx=np.nanargmax(np.where(mask,score,np.nan))
                    anchors.append(float(times.iloc[idx])); methods.append('argmax_TSP_MeaningGamma_minus_artifact_in_predeclared_subtitle_window')
                else:
                    anchors.append(float(r['semantic_anchor_estimate_sec'])); methods.append('subtitle_midpoint_fallback_no_feature_window')
            subs['semantic_anchor_estimate_sec']=anchors
            subs['anchor_method']=methods

    subs['SubtitleChoke_candidate']=((subs['LEC']>np.nanpercentile(subs['LEC'],75))).astype(int)
    subs.to_csv(tables/'subtitle_line_event_table.csv',index=False)
    subs[['line_id','subtitle_onset_sec','subtitle_offset_sec','semantic_anchor_estimate_sec','anchor_method','LEC']].to_csv(tables/'subtitle_phase_shift_table.csv',index=False)
    overlays=[]
    for _,r in subs.iterrows():
        label=f"Subtitle line {r.get('line_id','')} LEC={float(r['LEC']):.2f}"
        overlays.append({'start_sec':r['semantic_anchor_estimate_sec'],'end_sec':r['semantic_anchor_estimate_sec']+1.0,'label':label,'category':'lso_subtitle','source':'subtitle_line_event_table.csv'})
    pd.DataFrame(overlays).to_csv(tables/'subtitle_visual_overlay.csv',index=False)
    interp={'schema':'PRAYCG_LSO_SPM_SubtitleOverride_v1_4_7','created_utc':datetime.now(timezone.utc).isoformat(),'boundary':'Subtitle gaze/argmax timing estimates text ingestion timing, not comprehension; LSO is optional protocol variant.'}
    with open(tables/'subtitle_override_interpretation.json','w') as f: json.dump(interp,f,indent=2)
    print(json.dumps({'status':'ok','n_lines':len(subs),'tables':str(tables)},indent=2))

if __name__=='__main__': main()
