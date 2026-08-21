#!/usr/bin/env python3
"""
PRAYCG ALS Screen Pulse / Barcode Test v0.1
Displays a black-white-black-white-black timing barcode and optionally reads an LSL stream
so the ALS/PT19 signal can be checked before a protocol run.
"""
from __future__ import annotations
import argparse, json, threading, time
from pathlib import Path
from datetime import datetime

import numpy as np


def collector(stop_event, out, stream_name: str, max_samples_per_pull: int = 256):
    try:
        from pylsl import resolve_byprop, StreamInlet
    except Exception as exc:
        out["error"] = f"pylsl unavailable: {exc}"; return
    streams = resolve_byprop("name", stream_name, timeout=10)
    if not streams:
        out["error"] = f"stream not found: {stream_name}"; return
    inlet = StreamInlet(streams[0], max_buflen=30)
    out["stream_info"] = {
        "name": streams[0].name(), "type": streams[0].type(),
        "channel_count": streams[0].channel_count(), "nominal_srate": streams[0].nominal_srate(),
        "source_id": streams[0].source_id(),
    }
    samples, times = [], []
    while not stop_event.is_set():
        chunk, ts = inlet.pull_chunk(timeout=0.05, max_samples=max_samples_per_pull)
        if ts:
            samples.extend(chunk); times.extend(ts)
    # final flush
    for _ in range(5):
        chunk, ts = inlet.pull_chunk(timeout=0.05, max_samples=max_samples_per_pull)
        if ts:
            samples.extend(chunk); times.extend(ts)
    out["samples"] = samples; out["times"] = times


def run_display(pattern, fullscreen=True, screen_index=0, box_fraction=1.0, pulse_position="fullscreen"):
    import tkinter as tk
    root = tk.Tk()
    root.configure(bg="black")
    root.title("PRAYCG ALS Pulse Test")
    if fullscreen:
        root.attributes("-fullscreen", True)
    else:
        root.geometry("900x600")
    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    root.update()
    phases = []
    try:
        from pylsl import local_clock
    except Exception:
        local_clock = time.time
    for name, color, dur in pattern:
        canvas.delete("all")
        w, h = root.winfo_width(), root.winfo_height()
        if color == "white":
            if pulse_position == "fullscreen":
                canvas.create_rectangle(0, 0, w, h, fill="white", outline="white")
            else:
                size = int(min(w, h) * float(box_fraction))
                margin = 20
                if pulse_position == "lower_right":
                    x1, y1, x2, y2 = w - size - margin, h - size - margin, w - margin, h - margin
                elif pulse_position == "lower_left":
                    x1, y1, x2, y2 = margin, h - size - margin, margin + size, h - margin
                elif pulse_position == "upper_right":
                    x1, y1, x2, y2 = w - size - margin, margin, w - margin, margin + size
                else:
                    x1, y1, x2, y2 = margin, margin, margin + size, margin + size
                canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")
        else:
            canvas.create_rectangle(0, 0, w, h, fill="black", outline="black")
        canvas.create_text(w//2, max(30, h//15), text=f"ALS TEST: {name}", fill="red" if color == "black" else "black", font=("Arial", 28, "bold"))
        root.update()
        t0 = local_clock(); time.sleep(dur); root.update(); t1 = local_clock()
        phases.append({"phase": name, "color": color, "start_lsl_or_local": t0, "end_lsl_or_local": t1, "duration_sec": dur})
    root.destroy()
    return phases


def analyze(samples, times, phases, channel_index_1based: int):
    data = np.asarray(samples, dtype=float)
    t = np.asarray(times, dtype=float)
    if data.size == 0 or t.size == 0:
        return {"status":"NO_STREAM_DATA"}
    if data.ndim == 1:
        data = data.reshape(-1, 1)
    ch = data.shape[1]
    ci = ch - 1 if channel_index_1based <= 0 else min(max(channel_index_1based - 1, 0), ch - 1)
    x = data[:, ci]
    phase_stats = []
    for ph in phases:
        m = (t >= ph["start_lsl_or_local"]) & (t <= ph["end_lsl_or_local"])
        xf = x[m]
        phase_stats.append({
            "phase": ph["phase"], "color": ph["color"], "n": int(xf.size),
            "median": float(np.nanmedian(xf)) if xf.size else None,
            "mean": float(np.nanmean(xf)) if xf.size else None,
            "std": float(np.nanstd(xf)) if xf.size else None,
        })
    black_vals = [s["median"] for s in phase_stats if s["color"] == "black" and s["median"] is not None]
    white_vals = [s["median"] for s in phase_stats if s["color"] == "white" and s["median"] is not None]
    if not black_vals or not white_vals:
        status = "INSUFFICIENT_PHASE_SAMPLES"; delta = None
    else:
        base = float(np.median(black_vals)); pulse = float(np.median(white_vals)); delta = pulse - base
        noise = float(np.nanmedian([s["std"] for s in phase_stats if s["std"] is not None]) or 0.0)
        status = "PASS" if abs(delta) > max(5 * noise, 1e-6) else "WEAK_OR_NOT_DETECTED"
    return {
        "status": status,
        "selected_channel_1based": ci + 1,
        "channel_count": ch,
        "pulse_minus_black_median_delta": delta,
        "phase_stats": phase_stats,
        "boundary": "ALS validates physical display timing in external input u(t), not biological hidden state.",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--stream-name", default="obci_eeg1")
    p.add_argument("--channel-index", type=int, default=-1, help="1-based channel index. -1 means last channel.")
    p.add_argument("--out-dir", default="als_pulse_test_logs")
    p.add_argument("--fullscreen", action="store_true")
    p.add_argument("--windowed", action="store_true")
    p.add_argument("--pulse-position", default="fullscreen", choices=["fullscreen","lower_right","lower_left","upper_right","upper_left"])
    p.add_argument("--box-fraction", type=float, default=0.12)
    p.add_argument("--no-lsl", action="store_true")
    args = p.parse_args()
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = out_dir / f"als_screen_pulse_test_{stamp}.json"
    pattern = [
        ("BLACK_PRE_GUARD_0P5S", "black", 0.5),
        ("WHITE_LONG_PULSE_2P0S", "white", 2.0),
        ("BLACK_GUARD_0P5S", "black", 0.5),
        ("WHITE_SHORT_PULSE_0P75S", "white", 0.75),
        ("BLACK_POST_GUARD_1P0S", "black", 1.0),
    ]
    out = {}
    stop = threading.Event()
    th = None
    if not args.no_lsl:
        th = threading.Thread(target=collector, args=(stop, out, args.stream_name), daemon=True)
        th.start()
        time.sleep(1.0)
    phases = run_display(pattern, fullscreen=not args.windowed, box_fraction=args.box_fraction, pulse_position=args.pulse_position)
    if th is not None:
        stop.set(); th.join(timeout=3)
    result = {
        "schema": "PRAYCG_ALS_Screen_Pulse_Test_v0_1",
        "created_local": datetime.now().isoformat(timespec="seconds"),
        "stream_name": args.stream_name,
        "requested_channel_index_1based": args.channel_index,
        "pulse_position": args.pulse_position,
        "pattern": pattern,
        "phases": phases,
        "stream_info": out.get("stream_info"),
        "collector_error": out.get("error"),
    }
    if not args.no_lsl and "samples" in out:
        result["analysis"] = analyze(out.get("samples", []), out.get("times", []), phases, args.channel_index)
    else:
        result["analysis"] = {"status":"SCREEN_TEST_COMPLETED_NO_LSL_ANALYSIS" if args.no_lsl else "NO_LSL_DATA", "collector_error": out.get("error")}
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result["analysis"], indent=2))
    print(f"Wrote {json_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
