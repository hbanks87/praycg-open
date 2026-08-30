#!/usr/bin/env python3
"""PRAYCG v1.4.9 / PRAYCG2.0 consolidated self-report parser.

This script extracts PRAYCG2.0 branch core reports, Override task reports, gated confound
reports, and final master reports from either the runner's JSON sidecar files or StasisMarkers
event JSON/CSV logs. It produces analysis-suite-compatible tables.
"""
import argparse, csv, json, re
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_events(path: Path) -> List[Dict[str, Any]]:
    if path.suffix.lower() == '.json':
        data = json.loads(path.read_text(encoding='utf-8'))
        if isinstance(data, list): return data
        if isinstance(data, dict) and isinstance(data.get('events'), list): return data['events']
        return []
    rows = []
    with path.open('r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for r in reader: rows.append(dict(r))
    return rows


def try_json(s: Any) -> Optional[Any]:
    if not isinstance(s, str) or not s.strip(): return None
    try: return json.loads(s)
    except Exception: return None


def flat_rating_row(prefix: str, phase_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    row = {'record_type': prefix, 'phase_name': phase_name, 'schema': payload.get('schema','')}
    if 'branch_label' in payload: row['branch_label'] = payload.get('branch_label')
    if 'branch_type' in payload: row['branch_type'] = payload.get('branch_type')
    for k,v in (payload.get('ratings') or {}).items(): row[k] = v
    for k,v in (payload.get('choices') or {}).items(): row[k] = v
    if 'scene_note' in payload: row['scene_note'] = payload.get('scene_note')
    if 'note' in payload: row['note'] = payload.get('note')
    if 'final_scene_note' in payload: row['final_scene_note'] = payload.get('final_scene_note')
    if 'confound_detail_recommended' in payload: row['confound_detail_recommended'] = payload.get('confound_detail_recommended')
    return row


def extract_from_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for ev in events:
        marker = str(ev.get('marker',''))
        note = ev.get('note','')
        payload = try_json(note)
        if payload is None: continue
        phase = str(ev.get('phase',''))
        if marker.startswith('BRANCH_CORE_REPORT_') and marker.endswith('_END'):
            out.append(flat_rating_row('branch_core', payload.get('phase_name', phase), payload))
        elif marker.startswith('OVERRIDE_TASK_REPORT_') and marker.endswith('_END'):
            out.append(flat_rating_row('override_task', payload.get('phase_name', phase), payload))
        elif marker.startswith('CONFOUND_REPORT_') and marker.endswith('_END'):
            out.append(flat_rating_row('confound_detail', payload.get('phase_name', phase), payload))
        elif marker == 'FINAL_MASTER_REPORT_END':
            out.append(flat_rating_row('final_master', 'FINAL_MASTER_REPORT', payload))
        elif marker == 'PRERUN_DISPLAY_AUDIO_CALIBRATION_END':
            out.append(flat_rating_row('prerun_calibration', 'PRERUN_DISPLAY_AUDIO_CALIBRATION', payload))
    return out


def extract_sidecars(folder: Path) -> List[Dict[str, Any]]:
    out = []
    for p in folder.glob('*.json'):
        name = p.name.lower()
        if any(key in name for key in ['core_report','override_task_report','confound_report','final_master_report','prerun_display_audio_calibration']):
            try: payload = json.loads(p.read_text(encoding='utf-8'))
            except Exception: continue
            if 'core_report' in name: typ='branch_core'
            elif 'override_task_report' in name: typ='override_task'
            elif 'confound_report' in name: typ='confound_detail'
            elif 'final_master_report' in name: typ='final_master'
            else: typ='prerun_calibration'
            out.append(flat_rating_row(typ, payload.get('phase_name', typ), payload))
    return out


def write_csv(rows: List[Dict[str, Any]], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = []
    for r in rows:
        for k in r.keys():
            if k not in keys: keys.append(k)
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader(); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--event-log', type=Path, default=None)
    ap.add_argument('--sidecar-folder', type=Path, default=None)
    ap.add_argument('--out-dir', type=Path, required=True)
    args = ap.parse_args()
    rows = []
    if args.event_log:
        rows.extend(extract_from_events(load_events(args.event_log)))
    if args.sidecar_folder:
        rows.extend(extract_sidecars(args.sidecar_folder))
    write_csv(rows, args.out_dir/'praycg2_0_selfreport_all_records.csv')
    for typ in sorted({r.get('record_type') for r in rows}):
        write_csv([r for r in rows if r.get('record_type') == typ], args.out_dir/f'praycg2_0_{typ}.csv')
    summary = {'schema':'PRAYCG2_0_selfreport_parser_summary_v1','n_records':len(rows),'record_types':sorted({r.get('record_type') for r in rows})}
    (args.out_dir/'praycg2_0_selfreport_interpretation.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
