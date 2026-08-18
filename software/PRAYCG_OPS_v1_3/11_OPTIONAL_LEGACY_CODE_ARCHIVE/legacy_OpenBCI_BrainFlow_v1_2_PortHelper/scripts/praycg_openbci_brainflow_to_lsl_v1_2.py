#!/usr/bin/env python3
"""
PRAYCG OpenBCI BrainFlow -> LSL Bridge v1.2

Timing-stability update for PR-AYC-G acquisition.

Replaces the CPU-heavy OpenBCI GUI during recording:
    OpenBCI Cyton/Daisy -> BrainFlow -> LSL obci_eeg1

v1.1 additions:
- sample-level reconstructed timestamp mode, default
- OpenBCI package-number skip diagnostics where BrainFlow exposes package numbers
- numeric OpenBCIDiagnostics LSL stream
- OpenBCIStatusMarkers marker stream
- board-buffer backlog warnings
- sample-flow dropout/rate markers
- per-chunk CSV diagnostics for post-run audit

Install:
    pip install brainflow pylsl numpy pyserial

Examples:
    python scripts/praycg_identify_openbci_port_v1_2.py
    python scripts/praycg_openbci_brainflow_to_lsl_v1_2.py --list-ports
    python scripts/praycg_openbci_brainflow_to_lsl_v1_2.py --auto-port --confirmed-channel-map
    python scripts/praycg_openbci_brainflow_to_lsl_v1_2.py --board cyton-daisy --serial-port COM3 --confirmed-channel-map
"""
from __future__ import annotations

import argparse
import csv
import json
import signal
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

try:
    from serial.tools import list_ports
except Exception:
    list_ports = None

# Allow COM-port discovery even before BrainFlow/pylsl are installed.
# This is helpful on a new laptop when the first failure is simply an omitted --serial-port.
if "--list-ports" in sys.argv:
    if list_ports is None:
        print("pyserial is not installed. Install with: pip install pyserial")
        raise SystemExit(2)
    print("\nDetected serial ports")
    print("=====================")
    ports = list(list_ports.comports())
    if not ports:
        print("No serial ports detected.")
    for i, pp in enumerate(ports, 1):
        textp = " ".join(str(x or "") for x in [pp.device, pp.description, pp.manufacturer, pp.hwid]).lower()
        score = 0
        for key, val in [("openbci",90),("cyton",80),("ftdi",55),("ft232",55),("usb serial",35),("silicon labs",35),("cp210",35),("bluetooth",-80)]:
            if key in textp: score += val
        if getattr(pp, "vid", None) == 0x0403: score += 40
        print(f"\n[{i}] {pp.device}   score={score}")
        print(f"    description : {pp.description}")
        print(f"    manufacturer: {pp.manufacturer}")
        print(f"    hwid        : {pp.hwid}")
    raise SystemExit(0)

try:
    from pylsl import StreamInfo, StreamOutlet, local_clock
except Exception as exc:
    raise SystemExit(
        "Could not import pylsl. Install with: pip install pylsl\n"
        f"Original import error: {exc}"
    )

try:
    from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowError
except Exception as exc:
    raise SystemExit(
        "Could not import BrainFlow. Install with: pip install brainflow\n"
        f"Original import error: {exc}"
    )

PRAYCG16_LABELS = [
    ("Fz", "frontal_analytic_lock"), ("Cz", "central_anchor"), ("Pz", "parietal_integration"),
    ("F3", "left_frontal"), ("F4", "right_frontal"), ("C3", "left_central"), ("C4", "right_central"),
    ("P3", "left_parietal"), ("P4", "right_parietal"), ("T5", "left_posterior_temporal"),
    ("T6", "right_posterior_temporal"), ("O1", "left_visual_control"), ("O2", "right_visual_control"),
    ("T3", "left_jaw_temporal_sentinel"), ("T4", "right_jaw_temporal_sentinel"), ("Fp1", "blink_eye_sentinel"),
]

MARKIV_DEFAULT_LABELS = [
    ("Fp1", "blink_eye_sentinel"), ("Fp2", "blink_eye_sentinel"), ("C3", "left_central"),
    ("C4", "right_central"), ("P7", "left_posterior_temporal"), ("P8", "right_posterior_temporal"),
    ("O1", "left_visual_control"), ("O2", "right_visual_control"), ("F7", "left_frontal"),
    ("F8", "right_frontal"), ("F3", "left_frontal"), ("F4", "right_frontal"),
    ("T7", "left_jaw_temporal_sentinel"), ("T8", "right_jaw_temporal_sentinel"),
    ("P3", "left_parietal"), ("P4", "right_parietal"),
]

BOARD_MAP = {
    "cyton": BoardIds.CYTON_BOARD.value,
    "cyton-daisy": BoardIds.CYTON_DAISY_BOARD.value,
    "synthetic": BoardIds.SYNTHETIC_BOARD.value,
}


def _score_serial_port(p) -> Tuple[int, List[str]]:
    text = " ".join(str(x or "") for x in [p.device, p.description, p.manufacturer, p.hwid]).lower()
    score = 0
    reasons: List[str] = []
    positive = [
        ("openbci", 90), ("cyton", 80), ("daisy", 50), ("rfduino", 50),
        ("ftdi", 55), ("ft232", 55), ("usb serial", 35), ("usb-serial", 35),
        ("silicon labs", 35), ("cp210", 35), ("wch", 15), ("ch340", 15),
    ]
    negative = [("bluetooth", -80), ("standard serial over bluetooth", -100), ("modem", -30)]
    for key, val in positive:
        if key in text:
            score += val; reasons.append(f"+{val}:{key}")
    for key, val in negative:
        if key in text:
            score += val; reasons.append(f"{val}:{key}")
    if getattr(p, "vid", None) == 0x0403:
        score += 40; reasons.append("+40:VID_0403_FTDI")
    return score, reasons

def list_serial_ports_ranked() -> List[Tuple[str, str, str, str, int, List[str]]]:
    if list_ports is None:
        return []
    rows = []
    for p in list_ports.comports():
        score, reasons = _score_serial_port(p)
        rows.append((str(p.device or ""), str(p.description or ""), str(p.manufacturer or ""), str(p.hwid or ""), score, reasons))
    rows.sort(key=lambda r: (r[4], r[0]), reverse=True)
    return rows

def print_serial_ports_ranked() -> None:
    rows = list_serial_ports_ranked()
    print("\nDetected serial ports")
    print("=====================")
    if not rows:
        print("No serial ports detected, or pyserial is not installed. Install with: pip install pyserial")
        return
    for i, (device, desc, manuf, hwid, score, reasons) in enumerate(rows, 1):
        print(f"\n[{i}] {device}   score={score}")
        print(f"    description : {desc}")
        print(f"    manufacturer: {manuf}")
        print(f"    hwid        : {hwid}")
        print(f"    reasons     : {', '.join(reasons) if reasons else '(none)'}")
    best = rows[0]
    if best[4] > 0:
        print(f"\nMost likely OpenBCI port: {best[0]}")
        print("Example:")
        print(f"  python praycg_openbci_brainflow_to_lsl_v1_2.py --board cyton-daisy --serial-port {best[0]} --stream-name obci_eeg1 --timestamp-mode reconstructed --confirmed-channel-map")

def resolve_serial_port(board_key: str, serial_port: str, auto_port: bool, no_interactive: bool) -> str:
    if board_key == "synthetic":
        return serial_port
    if serial_port:
        return serial_port.strip()
    rows = list_serial_ports_ranked()
    if auto_port and rows:
        # Auto-select only if the top candidate is positive and clearly better than the runner-up.
        top = rows[0]
        second_score = rows[1][4] if len(rows) > 1 else -999
        if top[4] > 0 and (top[4] - second_score >= 20 or len(rows) == 1):
            print(f"Auto-selected likely OpenBCI port: {top[0]} (score={top[4]})", flush=True)
            return top[0]
        print("Auto-port found multiple plausible ports; choose manually:", flush=True)
    print_serial_ports_ranked()
    if no_interactive:
        raise ValueError("--serial-port is required for OpenBCI Cyton/Cyton-Daisy. Run with --list-ports or provide --serial-port COMx.")
    if not rows:
        raise ValueError("No serial ports detected. Plug in the OpenBCI dongle, wait a few seconds, and rerun --list-ports.")
    while True:
        ans = input("\nEnter OpenBCI serial port (for example COM3), or a list number, then press ENTER: ").strip()
        if not ans:
            continue
        if ans.isdigit():
            idx = int(ans)
            if 1 <= idx <= len(rows):
                return rows[idx-1][0]
        if ans.upper().startswith("COM") or "/dev/" in ans:
            return ans
        print("Could not understand that entry. Use COM3 or a list number like 1.")

DIAG_CHANNELS = [
    "chunk_index", "chunk_samples", "samples_total", "board_buffer_before", "board_buffer_after",
    "package_first", "package_last", "package_skip_count", "max_package_skip",
    "timestamp_gap_max_sec", "loop_dt_ms", "push_duration_ms", "effective_rate_since_start_hz", "recent_rate_hz",
    "backlog_sec", "dropout_open"
]


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Low-overhead OpenBCI BrainFlow-to-LSL bridge with timing diagnostics.")
    p.add_argument("--board", choices=sorted(BOARD_MAP.keys()), default="cyton-daisy")
    p.add_argument("--serial-port", default="", help="COM port, e.g. COM3. Not required for --board synthetic.")
    p.add_argument("--list-ports", action="store_true", help="List serial ports and exit.")
    p.add_argument("--auto-port", action="store_true", help="Auto-select the most likely OpenBCI COM port if unambiguous.")
    p.add_argument("--no-interactive", action="store_true", help="Do not prompt for a serial port if omitted; fail with a clear error instead.")
    p.add_argument("--stream-name", default="obci_eeg1")
    p.add_argument("--stream-type", default="EEG")
    p.add_argument("--source-id", default="")
    p.add_argument("--channel-map", choices=["praycg16", "markiv_default", "generic"], default="praycg16")
    p.add_argument("--channel-map-csv", default="")
    p.add_argument("--confirmed-channel-map", action="store_true")
    p.add_argument("--timestamp-mode", choices=["reconstructed", "lsl_chunk"], default="reconstructed",
                   help="reconstructed pushes sample-level timestamps; lsl_chunk uses chunk push time.")
    p.add_argument("--chunk-size", type=int, default=8, help="Drain/push when at least this many samples are waiting.")
    p.add_argument("--poll-sec", type=float, default=0.01)
    p.add_argument("--status-interval-sec", type=float, default=5.0)
    p.add_argument("--dropout-warning-sec", type=float, default=1.0)
    p.add_argument("--dropout-invalid-sec", type=float, default=3.0)
    p.add_argument("--rate-warn-hz", type=float, default=115.0)
    p.add_argument("--rate-invalid-hz", type=float, default=100.0)
    p.add_argument("--rate-window-sec", type=float, default=10.0)
    p.add_argument("--backlog-warn-sec", type=float, default=0.25)
    p.add_argument("--backlog-invalid-sec", type=float, default=1.0)
    p.add_argument("--status-stream-name", default="OpenBCIStatusMarkers")
    p.add_argument("--diagnostics-stream-name", default="OpenBCIDiagnostics")
    p.add_argument("--no-status-stream", action="store_true")
    p.add_argument("--no-diagnostics-stream", action="store_true")
    p.add_argument("--log-dir", default="openbci_brainflow_lsl_logs")
    p.add_argument("--max-runtime-sec", type=float, default=0.0, help="0 = run until Ctrl+C.")
    p.add_argument("--brainflow-log", action="store_true")
    return p


def load_channel_labels(n_channels: int, channel_map: str, csv_path: str = "") -> List[Tuple[str, str]]:
    if csv_path:
        rows: Dict[int, Tuple[str, str]] = {}
        with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
            r = csv.DictReader(f)
            for row in r:
                idx = int(row.get("channel_index_1based") or row.get("openbci_channel") or 0)
                label = row.get("electrode") or row.get("electrode_location") or f"Ch{idx:02d}"
                roi = row.get("roi", "unspecified")
                if idx >= 1: rows[idx] = (label, roi)
        return [rows.get(i+1, (f"Ch{i+1:02d}", "unspecified")) for i in range(n_channels)]
    base = PRAYCG16_LABELS if channel_map == "praycg16" else MARKIV_DEFAULT_LABELS if channel_map == "markiv_default" else []
    return [base[i] if i < len(base) else (f"Ch{i+1:02d}", "unspecified") for i in range(n_channels)]


def make_eeg_info(name: str, stream_type: str, n_channels: int, sample_rate: float, source_id: str,
                  labels: Sequence[Tuple[str, str]], board_name: str, board_id: int,
                  confirmed_channel_map: bool, timestamp_mode: str) -> StreamInfo:
    info = StreamInfo(name, stream_type, n_channels, sample_rate, "float32", source_id)
    d = info.desc()
    d.append_child_value("manufacturer", "OpenBCI")
    d.append_child_value("bridge", "PRAYCG_OpenBCI_BrainFlow_to_LSL_v1_2")
    d.append_child_value("brainflow_board_name", board_name)
    d.append_child_value("brainflow_board_id", str(board_id))
    d.append_child_value("nominal_srate_hz", str(sample_rate))
    d.append_child_value("timestamp_mode", timestamp_mode)
    d.append_child_value("units", "microvolts_BrainFlow_OpenBCI_default")
    d.append_child_value("channel_map_confirmed", str(bool(confirmed_channel_map)))
    chs = d.append_child("channels")
    for idx, (label, roi) in enumerate(labels, 1):
        ch = chs.append_child("channel")
        ch.append_child_value("label", label)
        ch.append_child_value("index_1based", str(idx))
        ch.append_child_value("roi", roi)
        ch.append_child_value("type", "EEG")
        ch.append_child_value("unit", "microvolts")
    return info


def make_marker_outlet(name: str, source_id: str) -> StreamOutlet:
    info = StreamInfo(name, "Markers", 1, 0, "string", source_id)
    d = info.desc()
    d.append_child_value("bridge", "PRAYCG_OpenBCI_BrainFlow_to_LSL_v1_2")
    d.append_child_value("purpose", "OpenBCI bridge status/dropout/timing markers")
    return StreamOutlet(info)


def make_diag_outlet(name: str, source_id: str) -> StreamOutlet:
    info = StreamInfo(name, "Diagnostics", len(DIAG_CHANNELS), 0, "float64", source_id)
    d = info.desc()
    d.append_child_value("bridge", "PRAYCG_OpenBCI_BrainFlow_to_LSL_v1_2")
    d.append_child_value("purpose", "per-chunk numeric diagnostics for EEG timing and sample-flow health")
    chs = d.append_child("channels")
    for i, label in enumerate(DIAG_CHANNELS, 1):
        ch = chs.append_child("channel")
        ch.append_child_value("label", label)
        ch.append_child_value("index_1based", str(i))
    return StreamOutlet(info)


def push_status(outlet: Optional[StreamOutlet], marker: str, payload: Optional[dict] = None) -> None:
    if outlet is None: return
    sample = marker if payload is None else f"{marker}|{json.dumps(payload, sort_keys=True, default=str)}"
    try: outlet.push_sample([sample], timestamp=local_clock(), pushthrough=True)
    except TypeError: outlet.push_sample([sample], timestamp=local_clock())
    except Exception: pass


def create_board(board_key: str, serial_port: str) -> Tuple[int, BoardShim]:
    board_id = BOARD_MAP[board_key]
    params = BrainFlowInputParams()
    if board_key != "synthetic":
        if not serial_port:
            raise ValueError("--serial-port is required for OpenBCI Cyton/Cyton-Daisy. Run --list-ports, --auto-port, or provide --serial-port COM3")
        params.serial_port = serial_port
    return board_id, BoardShim(board_id, params)


def get_optional_row(board_id: int, getter_name: str) -> Optional[int]:
    try:
        return int(getattr(BoardShim, getter_name)(board_id))
    except Exception:
        return None


def package_skip(prev_pkg: Optional[int], pkg: Optional[int]) -> int:
    if prev_pkg is None or pkg is None:
        return 0
    delta = (int(pkg) - int(prev_pkg)) % 256
    if delta == 0:
        return 0
    return max(0, delta - 1)


def main() -> int:
    args = build_arg_parser().parse_args()
    if args.list_ports:
        print_serial_ports_ranked()
        return 0
    args.serial_port = resolve_serial_port(args.board, args.serial_port, args.auto_port, args.no_interactive)
    if args.brainflow_log: BoardShim.enable_dev_board_logger()
    else: BoardShim.disable_board_logger()

    log_dir = Path(args.log_dir); log_dir.mkdir(parents=True, exist_ok=True)
    run_id = time.strftime("%Y%m%d_%H%M%S")
    source_id = args.source_id or f"praycg_obci_brainflow_v1_2_{args.board}_{uuid.uuid4().hex[:10]}"
    status_source_id = f"{source_id}_status"
    diag_source_id = f"{source_id}_diag"
    manifest_path = log_dir / f"openbci_brainflow_lsl_v1_2_manifest_{run_id}.json"
    events_path = log_dir / f"openbci_brainflow_lsl_v1_2_events_{run_id}.csv"
    diag_path = log_dir / f"openbci_brainflow_lsl_v1_2_chunk_diagnostics_{run_id}.csv"

    board_id, board = create_board(args.board, args.serial_port)
    sample_rate = float(BoardShim.get_sampling_rate(board_id))
    dt = 1.0 / sample_rate
    eeg_channels = list(BoardShim.get_eeg_channels(board_id))
    n_channels = len(eeg_channels)
    labels = load_channel_labels(n_channels, args.channel_map, args.channel_map_csv)
    package_row = get_optional_row(board_id, "get_package_num_channel")
    timestamp_row = get_optional_row(board_id, "get_timestamp_channel")

    eeg_info = make_eeg_info(args.stream_name, args.stream_type, n_channels, sample_rate, source_id, labels,
                             args.board, board_id, args.confirmed_channel_map, args.timestamp_mode)
    eeg_outlet = StreamOutlet(eeg_info, chunk_size=max(1, args.chunk_size), max_buffered=120)
    status_outlet = None if args.no_status_stream else make_marker_outlet(args.status_stream_name, status_source_id)
    diag_outlet = None if args.no_diagnostics_stream else make_diag_outlet(args.diagnostics_stream_name, diag_source_id)

    manifest = {
        "schema": "PRAYCG_OpenBCI_BrainFlow_to_LSL_v1_2_manifest",
        "created_unix": time.time(), "run_id": run_id, "board": args.board, "board_id": board_id,
        "serial_port": args.serial_port, "stream_name": args.stream_name, "source_id": source_id,
        "status_stream_name": None if args.no_status_stream else args.status_stream_name,
        "diagnostics_stream_name": None if args.no_diagnostics_stream else args.diagnostics_stream_name,
        "sample_rate_hz": sample_rate, "n_channels": n_channels, "eeg_channel_rows_brainflow": eeg_channels,
        "package_num_row": package_row, "timestamp_row": timestamp_row, "timestamp_mode": args.timestamp_mode,
        "channel_labels": [x for x,_ in labels], "channel_rois": [y for _,y in labels],
        "channel_map_confirmed": bool(args.confirmed_channel_map), "args": vars(args)
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    events_f = events_path.open("w", newline="", encoding="utf-8")
    events_writer = csv.DictWriter(events_f, fieldnames=["unix_time", "lsl_time", "event", "details"])
    events_writer.writeheader()
    diag_f = diag_path.open("w", newline="", encoding="utf-8")
    diag_writer = csv.DictWriter(diag_f, fieldnames=["unix_time", "lsl_time"] + DIAG_CHANNELS)
    diag_writer.writeheader()

    def log_event(event: str, details: Any = None) -> None:
        details_s = json.dumps(details, sort_keys=True, default=str) if isinstance(details, dict) else (details or "")
        row = {"unix_time": time.time(), "lsl_time": local_clock(), "event": event, "details": details_s}
        events_writer.writerow(row); events_f.flush()
        print(f"[{time.strftime('%H:%M:%S')}] {event} {details_s}", flush=True)
        push_status(status_outlet, event, details if isinstance(details, dict) else {"details": details_s})

    stop = {"value": False}
    def handle_stop(signum, frame):
        stop["value"] = True
        log_event("STOP_SIGNAL_RECEIVED", {"signal": signum})
    signal.signal(signal.SIGINT, handle_stop); signal.signal(signal.SIGTERM, handle_stop)

    prepared = streaming = False
    samples_total = 0; chunk_index = 0
    start_lsl: Optional[float] = None; last_sample_lsl: Optional[float] = None; last_status_lsl = local_clock()
    recent: List[Tuple[float,int]] = []
    dropout_open = False; warning_open = False; rate_invalid_open = False; backlog_invalid_open = False
    last_recon_ts: Optional[float] = None; last_pkg: Optional[int] = None
    last_loop_time = time.perf_counter()

    try:
        log_event("BRIDGE_STARTING", {"manifest": str(manifest_path), "diagnostics_csv": str(diag_path)})
        board.prepare_session(); prepared = True
        log_event("BRAINFLOW_SESSION_PREPARED", {"board": args.board, "serial_port": args.serial_port})
        board.start_stream(450000, ""); streaming = True
        start_lsl = local_clock(); last_sample_lsl = start_lsl
        log_event("BRAINFLOW_STREAM_STARTED", {"sample_rate_hz": sample_rate, "n_channels": n_channels, "package_num_row": package_row})
        log_event("LSL_EEG_OUTLET_ONLINE", {"stream_name": args.stream_name, "source_id": source_id, "timestamp_mode": args.timestamp_mode})
        if status_outlet: log_event("LSL_STATUS_OUTLET_ONLINE", {"stream_name": args.status_stream_name, "source_id": status_source_id})
        if diag_outlet: log_event("LSL_DIAGNOSTICS_OUTLET_ONLINE", {"stream_name": args.diagnostics_stream_name, "source_id": diag_source_id})
        runtime_start = time.time()

        while not stop["value"]:
            if args.max_runtime_sec > 0 and (time.time() - runtime_start) >= args.max_runtime_sec:
                log_event("MAX_RUNTIME_REACHED", {"max_runtime_sec": args.max_runtime_sec}); break

            now_perf = time.perf_counter(); loop_dt_ms = (now_perf - last_loop_time) * 1000.0; last_loop_time = now_perf
            buffer_before = int(board.get_board_data_count())
            if buffer_before >= max(1, args.chunk_size):
                data = board.get_board_data()  # drains BrainFlow board buffer
                buffer_after = int(board.get_board_data_count())
                if data.size > 0:
                    eeg = data[eeg_channels, :]
                    samples = eeg.T.astype(np.float32, copy=False)
                    nsamp = int(samples.shape[0])
                    if nsamp > 0:
                        packages = None
                        if package_row is not None and 0 <= package_row < data.shape[0]:
                            packages = np.rint(data[package_row, :]).astype(int)
                        # Build timestamps.
                        t_list: List[float] = []
                        skip_count = 0; max_skip = 0; ts_gap_max = 0.0
                        if args.timestamp_mode == "reconstructed":
                            if last_recon_ts is None:
                                # Align the last sample approximately with now; backfill earlier samples.
                                last_recon_ts = local_clock() - (nsamp * dt)
                            for i in range(nsamp):
                                pkg = int(packages[i]) if packages is not None else None
                                miss = package_skip(last_pkg, pkg)
                                skip_count += miss; max_skip = max(max_skip, miss)
                                step = (1 + miss) * dt
                                next_ts = last_recon_ts + step
                                ts_gap_max = max(ts_gap_max, step)
                                t_list.append(next_ts)
                                last_recon_ts = next_ts
                                if pkg is not None: last_pkg = pkg
                        else:
                            # Chunk timestamp mode: use a single current LSL push time for the chunk.
                            t_list = []
                            if packages is not None:
                                for pkg in packages:
                                    miss = package_skip(last_pkg, int(pkg)); skip_count += miss; max_skip=max(max_skip, miss); last_pkg=int(pkg)
                        push_start = time.perf_counter()
                        if args.timestamp_mode == "reconstructed":
                            for row, ts in zip(samples, t_list):
                                eeg_outlet.push_sample(row.tolist(), timestamp=ts, pushthrough=False)
                        else:
                            try:
                                eeg_outlet.push_chunk(samples.tolist(), timestamp=local_clock(), pushthrough=False)
                            except TypeError:
                                eeg_outlet.push_chunk(samples.tolist(), timestamp=local_clock())
                        push_duration_ms = (time.perf_counter() - push_start) * 1000.0
                        now_lsl = local_clock()
                        chunk_index += 1; samples_total += nsamp; last_sample_lsl = t_list[-1] if t_list else now_lsl
                        recent.append((now_lsl, nsamp)); cutoff = now_lsl - args.rate_window_sec
                        recent = [(t,n) for (t,n) in recent if t >= cutoff]
                        elapsed = max(1e-9, now_lsl - (start_lsl or now_lsl))
                        eff_rate = samples_total / elapsed
                        span = max(1e-9, recent[-1][0] - recent[0][0]) if len(recent) > 1 else 0.0
                        recent_rate = (sum(n for _,n in recent) / span) if span > 0 else 0.0
                        backlog_sec = buffer_before / sample_rate
                        diag = {
                            "chunk_index": chunk_index, "chunk_samples": nsamp, "samples_total": samples_total,
                            "board_buffer_before": buffer_before, "board_buffer_after": buffer_after,
                            "package_first": int(packages[0]) if packages is not None and nsamp else -1,
                            "package_last": int(packages[-1]) if packages is not None and nsamp else -1,
                            "package_skip_count": skip_count, "max_package_skip": max_skip,
                            "timestamp_gap_max_sec": ts_gap_max, "loop_dt_ms": loop_dt_ms,
                            "push_duration_ms": push_duration_ms, "effective_rate_since_start_hz": eff_rate,
                            "recent_rate_hz": recent_rate, "backlog_sec": backlog_sec, "dropout_open": 1.0 if dropout_open else 0.0,
                        }
                        row = {"unix_time": time.time(), "lsl_time": now_lsl, **diag}
                        diag_writer.writerow(row); diag_f.flush()
                        if diag_outlet is not None:
                            diag_outlet.push_sample([float(diag[k]) for k in DIAG_CHANNELS], timestamp=now_lsl)
                        if skip_count > 0:
                            log_event("EEG_PACKET_SKIP_DETECTED", {"chunk_index": chunk_index, "skip_count": skip_count, "max_skip": max_skip})
                        if backlog_sec >= args.backlog_warn_sec:
                            log_event("EEG_BACKLOG_WARNING", {"chunk_index": chunk_index, "backlog_sec": backlog_sec, "buffer_before": buffer_before})
                        if backlog_sec >= args.backlog_invalid_sec and not backlog_invalid_open:
                            log_event("EEG_BACKLOG_INVALID", {"chunk_index": chunk_index, "backlog_sec": backlog_sec}); backlog_invalid_open = True
                        if dropout_open:
                            log_event("EEG_DROPOUT_RECOVERED", {"samples_total": samples_total, "chunk_index": chunk_index}); dropout_open=False; warning_open=False
            else:
                time.sleep(max(0.001, args.poll_sec))

            now = local_clock()
            if last_sample_lsl is not None:
                silence = now - last_sample_lsl
                if silence > args.dropout_warning_sec and not warning_open:
                    log_event("EEG_GAP_WARNING", {"seconds_since_last_sample": silence}); warning_open=True
                if silence > args.dropout_invalid_sec and not dropout_open:
                    log_event("EEG_DROPOUT_DETECTED", {"seconds_since_last_sample": silence}); dropout_open=True
            if now - last_status_lsl >= args.status_interval_sec:
                elapsed = max(1e-9, now - (start_lsl or now)); eff = samples_total / elapsed
                span = max(1e-9, recent[-1][0] - recent[0][0]) if len(recent) > 1 else 0.0
                rr = (sum(n for _,n in recent) / span) if span > 0 else 0.0
                status = {"samples_total": samples_total, "elapsed_sec": elapsed, "effective_rate_hz_since_start": eff,
                          "recent_rate_hz": rr, "board_buffer_count": int(board.get_board_data_count()),
                          "dropout_open": dropout_open, "timestamp_mode": args.timestamp_mode}
                log_event("EEG_BRIDGE_HEARTBEAT", status)
                if rr > 0 and rr < args.rate_warn_hz:
                    log_event("EEG_RATE_WARNING", status)
                if rr > 0 and rr < args.rate_invalid_hz and not rate_invalid_open:
                    log_event("EEG_RATE_INVALID", status); rate_invalid_open=True
                if rr >= args.rate_warn_hz:
                    rate_invalid_open=False
                last_status_lsl = now
        log_event("BRIDGE_STOPPING", {"samples_total": samples_total})
        return 0
    except BrainFlowError as exc:
        log_event("BRAINFLOW_ERROR", {"error": str(exc)}); return 2
    except Exception as exc:
        log_event("BRIDGE_ERROR", {"error": repr(exc)}); return 1
    finally:
        try:
            if streaming:
                board.stop_stream(); log_event("BRAINFLOW_STREAM_STOPPED", {"samples_total": samples_total})
        except Exception as exc: log_event("BRAINFLOW_STOP_STREAM_ERROR", {"error": repr(exc)})
        try:
            if prepared:
                board.release_session(); log_event("BRAINFLOW_SESSION_RELEASED", {})
        except Exception as exc: log_event("BRAINFLOW_RELEASE_SESSION_ERROR", {"error": repr(exc)})
        try: events_f.close(); diag_f.close()
        except Exception: pass

if __name__ == "__main__":
    raise SystemExit(main())
