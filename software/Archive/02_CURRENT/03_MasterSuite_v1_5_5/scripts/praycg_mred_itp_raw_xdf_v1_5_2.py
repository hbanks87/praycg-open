#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math, importlib.util
from pathlib import Path
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from scipy import signal
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('itp', HERE/'praycg_mred_itp_modules_v1_5_2.py')
itp=importlib.util.module_from_spec(spec); spec.loader.exec_module(itp)
spec2=importlib.util.spec_from_file_location('ocm', HERE/'praycg_ocm_quartersecond_reextract_v1_4_5.py')
ocm=importlib.util.module_from_spec(spec2); spec2.loader.exec_module(ocm)
VERSION='1.5.2'

def branch_starts_from_feature(feat):
    out={}
    for cond,g in feat.groupby('condition'):
        if 'time_lsl' in g.columns and 'condition_offset_sec' in g.columns:
            starts=pd.to_numeric(g['time_lsl'],errors='coerce')-pd.to_numeric(g['condition_offset_sec'],errors='coerce')
            if starts.notna().any(): out[str(cond)] = float(starts.median())
    return out

def load_channel_map(path):
    return pd.read_csv(path) if path and Path(path).exists() else None

def channel_indices(cmap):
    idx={'neural_clean':list(range(13)),'fp1':[15],'jaw':[13,14]}
    if cmap is not None:
        fp=[]; jaw=[]; clean=[]
        for _,r in cmap.iterrows():
            try: ch=int(r.get('openbci_channel'))-1
            except Exception: continue
            elec=str(r.get('electrode_location','')).lower(); roi=str(r.get('roi','')).lower()
            if 'fp1' in elec or 'blink' in roi: fp.append(ch)
            elif elec in {'t3','t4'} or 'jaw' in roi: jaw.append(ch)
            else: clean.append(ch)
        if fp: idx['fp1']=fp
        if jaw: idx['jaw']=jaw
        if clean: idx['neural_clean']=clean
    return idx

def preprocess_raw(data,fs):
    x=np.asarray(data,dtype=float).copy()
    for c in range(x.shape[1]):
        col=x[:,c]; med=np.nanmedian(col[np.isfinite(col)]) if np.isfinite(col).any() else 0.0
        col[~np.isfinite(col)]=med; x[:,c]=col-med
    try:
        b,a=signal.iirnotch(60,Q=30,fs=fs); x=signal.filtfilt(b,a,x,axis=0)
    except Exception: pass
    try:
        sos=signal.butter(4,[1,min(45,fs/2-1)],btype='bandpass',fs=fs,output='sos'); x=signal.sosfiltfilt(sos,x,axis=0)
    except Exception: pass
    return x

def resample_segment(seg,fs,target_fs=25.0):
    if len(seg)<2: return seg
    try:
        import math
        up=int(target_fs); down=int(round(fs)); g=math.gcd(up,down); up//=g; down//=g
        return signal.resample_poly(seg,up,down,axis=0)
    except Exception:
        n=max(2,int(round(len(seg)*target_fs/fs))); return signal.resample(seg,n,axis=0)

def raw_lzc_for_window(ts,data,fs,start,end,chans):
    m=(ts>=start)&(ts<end)
    if m.sum()<int(3*fs): return (np.nan,int(m.sum()))
    seg=resample_segment(data[m][:,chans],fs,25.0)
    med=np.nanmedian(seg,axis=0); mad=np.nanmedian(np.abs(seg-med),axis=0); denom=1.4826*mad
    denom=np.where(np.isfinite(denom)&(denom>1e-9),denom,1.0)
    seg=np.clip((seg-med)/denom,-6,6)
    return (itp.normalized_lzc_symbol_matrix(seg),int(m.sum()))

def compute_raw_acg(feat,ann,xdf_path,cmap,out_dir):
    ts,data,h=ocm.load_eeg_from_xdf(xdf_path); fs=float(h.get('nominal_srate',125) or 125)
    data=preprocess_raw(data,fs); idx=channel_indices(cmap); starts=branch_starts_from_feature(feat)
    anchors=itp.build_anchor_rows(ann,[c for c in ['CONTROL_1','TARGET_1','CONTEXTUAL_OVERRIDE_1'] if c in starts])
    rows=[]
    for _,r in anchors.iterrows():
        base=starts.get(r['condition'],np.nan)
        pre,pre_n=raw_lzc_for_window(ts,data,fs,base+r.pre_start_sec,base+r.pre_end_sec,idx['neural_clean'])
        peak,peak_n=raw_lzc_for_window(ts,data,fs,base+r.peak_start_sec,base+r.peak_end_sec,idx['neural_clean'])
        post,post_n=raw_lzc_for_window(ts,data,fs,base+r.post_start_sec,base+r.post_end_sec,idx['neural_clean'])
        strike=peak-pre if np.isfinite(peak) and np.isfinite(pre) else np.nan
        settle=post-peak if np.isfinite(post) and np.isfinite(peak) else np.nan
        rows.append({**r.to_dict(),'raw_C_LZ_pre':pre,'raw_C_LZ_peak':peak,'raw_C_LZ_post':post,'raw_delta_C_strike':strike,'raw_delta_C_settle':settle,'raw_delta_C_post_vs_pre':post-pre if np.isfinite(post) and np.isfinite(pre) else np.nan,'pre_sample_count':pre_n,'peak_sample_count':peak_n,'post_sample_count':post_n,'raw_ACG_strike_gate':bool(np.isfinite(strike) and strike>0.002),'raw_ACG_settle_gate':bool(np.isfinite(settle) and settle<-0.002),'raw_ACG_gate':bool(np.isfinite(strike) and strike>0.002 and np.isfinite(settle) and settle<-0.002),'raw_complexity_settlement_index_CSI':(strike if np.isfinite(strike) else 0)+((-settle) if np.isfinite(settle) else 0),'method_status':'RAW_EEG_LZC_PROXY_EXCLUDING_FP1_JAW_CHANNELS'})
    res=pd.DataFrame(rows)
    if len(res): res['raw_CSI_z']=itp._zscore(res['raw_complexity_settlement_index_CSI'])
    res.to_csv(out_dir/'raw_acg_event_table.csv',index=False); return res

def detect_fp1_blink_proxy(ts,data,fs,fp_ch,jaw_chans):
    fp=data[:,fp_ch]; n=max(5,int(round(0.25*fs)))
    p2p=(pd.Series(fp).rolling(n,center=True,min_periods=max(2,n//3)).max()-pd.Series(fp).rolling(n,center=True,min_periods=max(2,n//3)).min()).bfill().ffill().values
    z=itp._zscore(pd.Series(p2p)).values
    jaw=np.zeros_like(z)
    if jaw_chans:
        try:
            sos=signal.butter(4,[45,min(55,fs/2-1)],btype='bandpass',fs=fs,output='sos'); j=signal.sosfiltfilt(sos,data[:,jaw_chans],axis=0); jaw=itp._zscore(pd.Series(np.mean(j*j,axis=1))).values
        except Exception: pass
    score=z-0.25*jaw; thr=max(3.0,float(np.nanpercentile(score,97)))
    peaks,_=signal.find_peaks(score,height=thr,distance=int(0.35*fs))
    return pd.DataFrame({'time_lsl':ts[peaks],'fp1_p2p_z':z[peaks],'jaw_hf_z':jaw[peaks],'blink_proxy_score':score[peaks],'method_status':'RAW_FP1_BLINK_PROXY_NOT_CONFIRMED_EOG'})

def compute_raw_ocu(feat,ann,xdf_path,cmap,out_dir):
    ts,data,h=ocm.load_eeg_from_xdf(xdf_path); fs=float(h.get('nominal_srate',125) or 125)
    data=preprocess_raw(data,fs); idx=channel_indices(cmap); events=detect_fp1_blink_proxy(ts,data,fs,idx['fp1'][0],idx['jaw']); events.to_csv(out_dir/'raw_fp1_blink_proxy_events.csv',index=False)
    starts=branch_starts_from_feature(feat); anchors=itp.build_anchor_rows(ann,[c for c in ['CONTROL_1','TARGET_1','CONTEXTUAL_OVERRIDE_1'] if c in starts])
    base_rates=[]
    for cond,base in starts.items():
        if 'BASELINE' in cond:
            g=feat[feat.condition==cond]
            if len(g):
                st=base+g.condition_offset_sec.min(); en=base+g.condition_offset_sec.max(); n=((events.time_lsl>=st)&(events.time_lsl<en)).sum(); base_rates.append(n/((en-st)/60))
    baseline_rate=float(np.nanmean(base_rates)) if base_rates else np.nan
    rows=[]
    for _,r in anchors.iterrows():
        base=starts.get(r['condition'],np.nan); t=base+r.anchor_time_sec
        windows={'pre':(t-30,t-5),'hold':(t-5,t+5),'release':(t+5,t+20)}; rates={}; counts={}
        for k,(st,en) in windows.items():
            cnt=int(((events.time_lsl>=st)&(events.time_lsl<en)).sum()); counts[k]=cnt; rates[k]=cnt/((en-st)/60)
        suppression=baseline_rate-rates['hold'] if np.isfinite(baseline_rate) else np.nan; release=rates['release']-rates['hold']
        rows.append({**r.to_dict(),'raw_baseline_fp1_blink_proxy_rate_per_min':baseline_rate,'raw_pre_event_rate_per_min':rates['pre'],'raw_hold_rate_per_min':rates['hold'],'raw_release_rate_per_min':rates['release'],'raw_pre_event_count':counts['pre'],'raw_hold_count':counts['hold'],'raw_release_count':counts['release'],'raw_blink_suppression_proxy':suppression,'raw_blink_release_proxy':release,'raw_OCU_suppression_gate':bool(np.isfinite(suppression) and suppression>0),'raw_OCU_release_gate':bool(np.isfinite(release) and release>0),'raw_OCU_gate':bool(np.isfinite(suppression) and suppression>0 and np.isfinite(release) and release>0),'raw_ocular_release_index_ORI':(suppression if np.isfinite(suppression) else 0)/10+release/10,'method_status':'RAW_FP1_BLINK_PROXY_NOT_CONFIRMED_EOG'})
    res=pd.DataFrame(rows)
    if len(res): res['raw_ORI_z']=itp._zscore(res['raw_ocular_release_index_ORI'])
    res.to_csv(out_dir/'raw_ocu_event_table.csv',index=False); return res

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--xdf',required=True); ap.add_argument('--feature-csv',required=True); ap.add_argument('--annotation-csv',required=True); ap.add_argument('--channel-map-csv',default=''); ap.add_argument('--out-dir',required=True)
    args=ap.parse_args(); out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True); feat=pd.read_csv(args.feature_csv); ann=pd.read_csv(args.annotation_csv); cmap=load_channel_map(args.channel_map_csv)
    acg=compute_raw_acg(feat,ann,Path(args.xdf),cmap,out); ocu=compute_raw_ocu(feat,ann,Path(args.xdf),cmap,out)
    summary={'module':'MRED_ITP_RAW_XDF_v0.1','version':VERSION,'raw_acg_gate_counts_by_condition': acg.groupby('condition')['raw_ACG_gate'].sum().to_dict() if len(acg) else {},'raw_ocu_gate_counts_by_condition': ocu.groupby('condition')['raw_OCU_gate'].sum().to_dict() if len(ocu) else {},'boundary':'Raw EEG/Fp1 proxy analysis only; not confirmed EOG/blink, not thermodynamic proof.'}
    (out/'mred_itp_raw_xdf_interpretation.json').write_text(json.dumps(summary,indent=2),encoding='utf-8'); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
