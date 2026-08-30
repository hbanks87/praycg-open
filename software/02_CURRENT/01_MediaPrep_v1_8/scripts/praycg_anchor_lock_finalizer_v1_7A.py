#!/usr/bin/env python3
"""
PRAYCG Anchor Lock Finalizer v1.7A

Takes a MediaPrep-generated DRAFT anchor schedule and produces a LOCKED anchor
schedule that the PRAYCG1.9C runner can load and marker-register.

A LOCKED file means only this: the anchor definitions and rendered-video
seconds were written before acquisition or before physiological analysis. It is
not evidence that the physiological endpoint will pass.
"""
from __future__ import annotations
import argparse, csv, datetime as dt, hashlib, json, sys
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_TIME_FIELDS = ("rendered_time_sec", "anchor_time_sec", "time_sec", "content_time_sec")

def now_utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _has_time(row: Dict[str, Any]) -> bool:
    for k in REQUIRED_TIME_FIELDS:
        v = row.get(k)
        if v is None:
            continue
        if isinstance(v, str) and not v.strip():
            continue
        try:
            float(v)
            return True
        except Exception:
            continue
    return False

def _norm_anchor(row: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(row)
    if not _has_time(out):
        raise ValueError(f"Anchor {out.get('anchor_id') or out.get('id') or '<unnamed>'} has no valid rendered/content time.")
    out["claim_level"] = "confirmatory_if_loaded_before_run"
    out["lock_status"] = "LOCKED"
    out["locked_requires_runner_registration"] = True
    return out

def load_any(path: Path) -> Dict[str, Any]:
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return {"schema": "PRAYCG_predeclared_anchor_schedule_v1_7A", "anchors": payload}
        return payload
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        return {"schema": "PRAYCG_predeclared_anchor_schedule_v1_7A", "anchors": rows}
    raise ValueError("Use a .json or .csv draft anchor file")

def write_csv(path: Path, anchors: List[Dict[str, Any]]) -> None:
    fields: List[str] = []
    for row in anchors:
        for k in row.keys():
            if k not in fields:
                fields.append(k)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in anchors:
            clean = {}
            for k, v in row.items():
                if isinstance(v, (list, dict)):
                    clean[k] = json.dumps(v, ensure_ascii=False)
                else:
                    clean[k] = v
            w.writerow(clean)

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Finalize a DRAFT PRAYCG predeclared anchor schedule into a LOCKED runner-loadable anchor file.")
    ap.add_argument("--draft", required=True, help="DRAFT JSON or CSV from MediaPrep anchor-prep")
    ap.add_argument("--out-dir", default="", help="Optional output directory; default is draft parent")
    ap.add_argument("--suffix", default="LOCKED", help="Output suffix label")
    ap.add_argument("--allow-missing-times", action="store_true", help="Dangerous: write locked file even if some anchors lack time. They will be skipped by runner.")
    args = ap.parse_args(argv)
    src = Path(args.draft).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(src)
    payload = load_any(src)
    anchors_raw = payload.get("anchors", [])
    if not isinstance(anchors_raw, list) or not anchors_raw:
        raise ValueError("Draft has no anchors list")
    locked: List[Dict[str, Any]] = []
    missing: List[str] = []
    for row in anchors_raw:
        row = dict(row)
        if not _has_time(row):
            missing.append(str(row.get("anchor_id") or row.get("id") or "<unnamed>"))
            if args.allow_missing_times:
                row["lock_status"] = "INCOMPLETE_SKIPPED_BY_RUNNER"
                locked.append(row)
            continue
        locked.append(_norm_anchor(row))
    if missing and not args.allow_missing_times:
        raise SystemExit("Cannot LOCK anchor schedule. Missing rendered/content time for: " + ", ".join(missing))
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = src.stem
    for tag in ("_DRAFT", "_draft", "-DRAFT", "-draft"):
        stem = stem.replace(tag, "")
    out_json = out_dir / f"{stem}_{args.suffix}.json"
    out_csv = out_dir / f"{stem}_{args.suffix}.csv"
    payload_out = dict(payload)
    payload_out["status"] = "LOCKED"
    payload_out["locked_utc"] = now_utc_iso()
    payload_out["source_draft"] = str(src)
    payload_out["source_draft_sha256"] = sha256_file(src)
    payload_out["anchors"] = locked
    payload_out["runner_instruction"] = "Load this LOCKED file in PRAYCG1.9C Predeclared anchor JSON/CSV before acquisition."
    out_json.write_text(json.dumps(payload_out, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(out_csv, locked)
    manifest = {
        "locked_json": str(out_json),
        "locked_csv": str(out_csv),
        "locked_json_sha256": sha256_file(out_json),
        "locked_csv_sha256": sha256_file(out_csv),
        "n_anchors": len(locked),
        "missing_or_skipped": missing,
    }
    (out_dir / f"{stem}_{args.suffix}_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
