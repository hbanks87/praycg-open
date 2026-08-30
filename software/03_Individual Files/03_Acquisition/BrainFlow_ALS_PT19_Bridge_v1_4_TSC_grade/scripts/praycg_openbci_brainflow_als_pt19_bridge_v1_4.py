#!/usr/bin/env python3
r"""
PRAYCG OpenBCI BrainFlow -> LSL Bridge v1.4
EEG + Analog AUX + ALS-PT19 single-channel timing stream

Why this exists
---------------
OpenBCI GUI may only reliably export one LSL stream at a time on some systems.
This script takes exclusive control of the Cyton/Cyton+Daisy serial port and
publishes simultaneous LSL streams from one BrainFlow session:

  1) obci_eeg1              16-channel EEG, default for PR-AYC-G
  2) OpenBCIAnalogAux       3-channel analog AUX: A5/D11, A6/D12, A7/D13
  3) ALS_PT19_Timing        1-channel extracted ALS light sensor, default A6/D12
  4) OpenBCIStatusMarkers   status markers / heartbeat / errors

KISS wiring for ALS-PT19
------------------------
  ALS +   -> Cyton DVDD / 3V3
  ALS -   -> Cyton GND
  ALS OUT -> Cyton D12 / A6

Run example
-----------
python scripts\praycg_openbci_brainflow_als_pt19_bridge_v1_4.py ^
  --board cyton-daisy ^
  --serial-port COM3 ^
  --enable-analog-aux ^
  --publish-als-stream ^
  --confirmed-channel-map

Never run OpenBCI GUI and this script against the same COM port at the same time.
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
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

try:
    from serial.tools import list_ports
except Exception:
    list_ports = None

try:
    from pylsl import StreamInfo, StreamOutlet, local_clock
except Exception as exc:
    raise SystemExit(
        "Could not import pylsl. Install with: python -m pip install pylsl\n"
        + str(exc)
    )

try:
    from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
except Exception as exc:
    raise SystemExit(
        "Could not import BrainFlow. Install with: python -m pip install brainflow\n"
        + str(exc)
    )

BRIDGE_VERSION = "PRAYCG_OpenBCI_BrainFlow_ALS_PT19_Bridge_v1_4"

PRAYCG16_LABELS = [
    ("Fz", "frontal_analytic_lock"),
    ("Cz", "central_anchor"),
    ("Pz", "parietal_integration"),
    ("F3", "left_frontal"),
    ("F4", "right_frontal"),
    ("C3", "left_central"),
    ("C4", "right_central"),
    ("P3", "left_parietal"),
    ("P4", "right_parietal"),
    ("T5", "left_posterior_temporal"),
    ("T6", "right_posterior_temporal"),
    ("O1", "left_visual_control"),
    ("O2", "right_visual_control"),
    ("T3", "left_jaw_temporal_sentinel"),
    ("T4", "right_jaw_temporal_sentinel"),
    ("Fp1", "blink_eye_sentinel"),
]

BOARD_MAP = {
    "cyton": BoardIds.CYTON_BOARD.value,
    "cyton-daisy": BoardIds.CYTON_DAISY_BOARD.value,
    "synthetic": BoardIds.SYNTHETIC_BOARD.value,
}

DEFAULT_AUX_LABELS = [
    "A5_D11_PULSE_OR_SPARE",
    "A6_D12_ALS_PT19_LIGHT",
    "A7_D13_BUTTON_OR_SPARE",
]

# Fallback row mappings from BrainFlow's Cyton channel table.
# Used only if the installed BrainFlow build does not expose get_analog_channels().
FALLBACK_ANALOG_ROWS = {
    BoardIds.CYTON_BOARD.value: [19, 20, 21],
    BoardIds.CYTON_DAISY_BOARD.value: [27, 28, 29],
}


def now_stamp() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def score_port(p) -> int:
    text = " ".join(
        str(x or "") for x in [p.device, p.description, p.manufacturer, p.hwid]
    ).lower()
    score = 0
    for key, val in [
        ("openbci", 90),
        ("cyton", 80),
        ("daisy", 50),
        ("rfduino", 50),
        ("ftdi", 55),
        ("ft232", 55),
        ("usb serial", 35),
        ("usb-serial", 35),
        ("silicon labs", 35),
        ("cp210", 35),
        ("bluetooth", -80),
        ("modem", -30),
    ]:
        if key in text:
            score += val
    if getattr(p, "vid", None) == 0x0403:
        score += 40
    return score


def ranked_ports() -> List[Tuple[str, str, str, str, int]]:
    if list_ports is None:
        return []
    rows = []
    for p in list_ports.comports():
        rows.append(
            (
                str(p.device or ""),
                str(p.description or ""),
                str(p.manufacturer or ""),
                str(p.hwid or ""),
                score_port(p),
            )
        )
    rows.sort(key=lambda r: (r[4], r[0]), reverse=True)
    return rows


def print_ports() -> None:
    rows = ranked_ports()
    print("\nDetected serial ports")
    print("=====================")
    if not rows:
        print("No serial ports detected. Plug in the OpenBCI dongle and wait 3-5 seconds.")
        return
    for i, row in enumerate(rows, 1):
        print(f"[{i}] {row[0]} score={row[4]} | {row[1]} | {row[2]} | {row[3]}")


def resolve_port(serial_port: str, auto_port: bool, no_interactive: bool) -> str:
    if serial_port:
        return serial_port.strip()
    rows = ranked_ports()
    if auto_port and rows:
        top = rows[0]
        second = rows[1][4] if len(rows) > 1 else -999
        if top[4] > 0 and (len(rows) == 1 or top[4] - second >= 20):
            print(f"Auto-selected likely OpenBCI port: {top[0]} (score={top[4]})", flush=True)
            return top[0]
    print_ports()
    if no_interactive:
        raise ValueError("--serial-port is required. Run --list-ports or provide --serial-port COMx.")
    if not rows:
        raise ValueError("No serial ports detected. Plug in the OpenBCI dongle and rerun.")
    while True:
        ans = input("Enter OpenBCI serial port, e.g. COM3, or list number: ").strip()
        if ans.isdigit() and 1 <= int(ans) <= len(rows):
            return rows[int(ans) - 1][0]
        if ans.upper().startswith("COM") or ans.startswith("/dev/"):
            return ans
        print("Could not understand. Use COM3 or a list number.")


def make_marker_outlet(name: str, sid: str) -> StreamOutlet:
    info = StreamInfo(name, "Markers", 1, 0, "string", sid)
    info.desc().append_child_value("bridge", BRIDGE_VERSION)
    return StreamOutlet(info)


def push_marker(outlet: Optional[StreamOutlet], marker: str, payload: Optional[dict] = None) -> None:
    if outlet is None:
        return
    msg = marker if payload is None else marker + "|" + json.dumps(payload, sort_keys=True, default=str)
    try:
        outlet.push_sample([msg], timestamp=local_clock(), pushthrough=True)
    except TypeError:
        outlet.push_sample([msg], timestamp=local_clock())


def make_eeg_info(
    name: str,
    n_ch: int,
    srate: float,
    sid: str,
    labels: Sequence[Tuple[str, str]],
    confirmed: bool,
    timestamp_mode: str,
) -> StreamInfo:
    info = StreamInfo(name, "EEG", n_ch, srate, "float32", sid)
    d = info.desc()
    d.append_child_value("manufacturer", "OpenBCI")
    d.append_child_value("bridge", BRIDGE_VERSION)
    d.append_child_value("timestamp_mode", timestamp_mode)
    d.append_child_value("channel_map_confirmed", str(bool(confirmed)))
    d.append_child_value("units", "microvolts_BrainFlow_OpenBCI_default")
    chs = d.append_child("channels")
    for i, (label, roi) in enumerate(labels, 1):
        ch = chs.append_child("channel")
        ch.append_child_value("label", label)
        ch.append_child_value("index_1based", str(i))
        ch.append_child_value("roi", roi)
        ch.append_child_value("unit", "microvolts")
    return info


def make_aux_info(
    name: str,
    n_ch: int,
    srate: float,
    sid: str,
    labels: Sequence[str],
    source_rows: Sequence[int],
) -> StreamInfo:
    info = StreamInfo(name, "AnalogAux", n_ch, srate, "float32", sid)
    d = info.desc()
    d.append_child_value("manufacturer", "OpenBCI")
    d.append_child_value("bridge", BRIDGE_VERSION)
    d.append_child_value("units", "BrainFlow_aux_units_or_raw_ADC_check_with_calibration")
    d.append_child_value("board_mode", "analog_/2")
    d.append_child_value("note", "A6_D12_ALS_PT19_LIGHT is default ALS-PT19 timing channel. Calibrate black/white levels before real runs.")
    chs = d.append_child("channels")
    for i in range(n_ch):
        ch = chs.append_child("channel")
        ch.append_child_value("label", labels[i] if i < len(labels) else f"AUX_{i+1}")
        ch.append_child_value("index_1based", str(i + 1))
        ch.append_child_value("brainflow_row", str(source_rows[i] if i < len(source_rows) else -1))
    return info


def make_als_info(name: str, srate: float, sid: str, aux_channel: int, source_row: int, label: str) -> StreamInfo:
    info = StreamInfo(name, "LightSensor", 1, srate, "float32", sid)
    d = info.desc()
    d.append_child_value("manufacturer", "OpenBCI+Adafruit")
    d.append_child_value("sensor", "ALS-PT19 analog light sensor or equivalent")
    d.append_child_value("bridge", BRIDGE_VERSION)
    d.append_child_value("units", "BrainFlow_aux_units_or_raw_ADC_check_with_calibration")
    d.append_child_value("board_mode", "analog_/2")
    d.append_child_value("aux_channel_0based", str(aux_channel))
    d.append_child_value("aux_label", label)
    d.append_child_value("brainflow_row", str(source_row))
    d.append_child_value("interpretation", "Physical display timing channel. External input vector u(t), not biological hidden variable Y(t).")
    chs = d.append_child("channels")
    ch = chs.append_child("channel")
    ch.append_child_value("label", label)
    ch.append_child_value("index_1based", "1")
    return info


def get_row_list(board_id: int, getter_name: str) -> List[int]:
    try:
        return [int(x) for x in list(getattr(BoardShim, getter_name)(board_id))]
    except Exception:
        return []


def get_row(board_id: int, getter_name: str) -> Optional[int]:
    try:
        return int(getattr(BoardShim, getter_name)(board_id))
    except Exception:
        return None


def get_analog_rows(board_id: int) -> List[int]:
    rows = get_row_list(board_id, "get_analog_channels")
    if rows:
        return rows
    return list(FALLBACK_ANALOG_ROWS.get(board_id, []))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="OpenBCI Cyton/Daisy BrainFlow-to-LSL bridge with simultaneous EEG + Analog AUX + ALS-PT19 light stream."
    )
    p.add_argument("--board", choices=sorted(BOARD_MAP.keys()), default="cyton-daisy")
    p.add_argument("--serial-port", default="")
    p.add_argument("--list-ports", action="store_true")
    p.add_argument("--auto-port", action="store_true")
    p.add_argument("--no-interactive", action="store_true")

    p.add_argument("--stream-name", default="obci_eeg1", help="EEG LSL stream name")
    p.add_argument("--aux-stream-name", default="OpenBCIAnalogAux", help="3-channel analog AUX LSL stream name")
    p.add_argument("--als-stream-name", default="ALS_PT19_Timing", help="single-channel ALS LSL stream name")
    p.add_argument("--status-stream-name", default="OpenBCIStatusMarkers")

    p.add_argument("--enable-analog-aux", action="store_true", help="Send /2 to Cyton to replace accelerometer AUX with analog reads A5/A6/A7.")
    p.add_argument("--analog-command", default="/2")
    p.add_argument("--restore-default-mode-on-exit", action="store_true", default=True, help="Send /0 on exit after stream stops. Default true.")
    p.add_argument("--no-restore-default-mode-on-exit", dest="restore_default_mode_on_exit", action="store_false")

    p.add_argument("--publish-raw-aux-stream", action="store_true", default=True)
    p.add_argument("--no-publish-raw-aux-stream", dest="publish_raw_aux_stream", action="store_false")
    p.add_argument("--publish-als-stream", action="store_true", default=True)
    p.add_argument("--no-publish-als-stream", dest="publish_als_stream", action="store_false")
    p.add_argument("--als-aux-channel", type=int, default=1, help="0=A5/D11, 1=A6/D12 default, 2=A7/D13")

    p.add_argument("--timestamp-mode", choices=["reconstructed", "lsl_chunk"], default="reconstructed")
    p.add_argument("--chunk-size", type=int, default=8)
    p.add_argument("--poll-sec", type=float, default=0.01)
    p.add_argument("--max-runtime-sec", type=float, default=0.0)
    p.add_argument("--confirmed-channel-map", action="store_true")
    p.add_argument("--no-status-stream", action="store_true")
    p.add_argument("--log-dir", default="openbci_brainflow_als_logs")
    return p


def main() -> int:
    args = build_parser().parse_args()
    if args.list_ports:
        print_ports()
        return 0
    if args.board != "synthetic":
        args.serial_port = resolve_port(args.serial_port, args.auto_port, args.no_interactive)

    if args.publish_als_stream and not args.enable_analog_aux:
        print("WARNING: --publish-als-stream requested but --enable-analog-aux is off. Enabling analog AUX.", flush=True)
        args.enable_analog_aux = True

    BoardShim.disable_board_logger()
    board_id = BOARD_MAP[args.board]
    params = BrainFlowInputParams()
    if args.board != "synthetic":
        params.serial_port = args.serial_port
    board = BoardShim(board_id, params)

    srate = float(BoardShim.get_sampling_rate(board_id))
    dt = 1.0 / srate
    eeg_rows = get_row_list(board_id, "get_eeg_channels")
    analog_rows = get_analog_rows(board_id) if args.enable_analog_aux else []
    package_row = get_row(board_id, "get_package_num_channel")
    timestamp_row = get_row(board_id, "get_timestamp_channel")

    if args.enable_analog_aux and not analog_rows:
        raise RuntimeError("No analog AUX rows found for this board. Use cyton/cyton-daisy or update BrainFlow.")
    if args.publish_als_stream and not (0 <= args.als_aux_channel < len(analog_rows)):
        raise ValueError(f"--als-aux-channel must be 0..{len(analog_rows)-1}; got {args.als_aux_channel}")

    n_eeg = len(eeg_rows)
    labels = PRAYCG16_LABELS[:n_eeg] + [
        (f"Ch{i+1:02d}", "unspecified") for i in range(max(0, n_eeg - len(PRAYCG16_LABELS)))
    ]
    run_id = now_stamp()
    source_id = f"praycg_obci_brainflow_als_v1_4_{args.board}_{uuid.uuid4().hex[:10]}"
    aux_source_id = source_id + "_aux"
    als_source_id = source_id + "_als"
    status_source_id = source_id + "_status"

    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = log_dir / f"openbci_brainflow_als_v1_4_manifest_{run_id}.json"
    events_path = log_dir / f"openbci_brainflow_als_v1_4_events_{run_id}.csv"
    diag_path = log_dir / f"openbci_brainflow_als_v1_4_chunk_diagnostics_{run_id}.csv"

    eeg_outlet = StreamOutlet(
        make_eeg_info(args.stream_name, n_eeg, srate, source_id, labels, args.confirmed_channel_map, args.timestamp_mode),
        chunk_size=max(1, args.chunk_size),
        max_buffered=120,
    )

    aux_outlet = None
    if args.enable_analog_aux and args.publish_raw_aux_stream:
        aux_outlet = StreamOutlet(
            make_aux_info(args.aux_stream_name, len(analog_rows), srate, aux_source_id, DEFAULT_AUX_LABELS, analog_rows),
            chunk_size=max(1, args.chunk_size),
            max_buffered=120,
        )

    als_outlet = None
    als_label = None
    als_source_row = None
    if args.enable_analog_aux and args.publish_als_stream:
        als_label = DEFAULT_AUX_LABELS[args.als_aux_channel] if args.als_aux_channel < len(DEFAULT_AUX_LABELS) else f"AUX_{args.als_aux_channel+1}"
        als_source_row = analog_rows[args.als_aux_channel]
        als_outlet = StreamOutlet(
            make_als_info(args.als_stream_name, srate, als_source_id, args.als_aux_channel, als_source_row, als_label),
            chunk_size=max(1, args.chunk_size),
            max_buffered=120,
        )

    status_outlet = None if args.no_status_stream else make_marker_outlet(args.status_stream_name, status_source_id)

    manifest = {
        "schema": "PRAYCG_OpenBCI_BrainFlow_ALS_PT19_Bridge_v1_4_manifest",
        "created_unix": time.time(),
        "board": args.board,
        "board_id": board_id,
        "serial_port": args.serial_port,
        "sample_rate_hz": srate,
        "eeg_stream_name": args.stream_name,
        "raw_aux_stream_name": args.aux_stream_name if aux_outlet is not None else None,
        "als_stream_name": args.als_stream_name if als_outlet is not None else None,
        "status_stream_name": args.status_stream_name if status_outlet is not None else None,
        "enable_analog_aux": bool(args.enable_analog_aux),
        "analog_command": args.analog_command,
        "als_aux_channel_0based": args.als_aux_channel,
        "als_label": als_label,
        "eeg_rows": eeg_rows,
        "analog_rows": analog_rows,
        "als_source_row": als_source_row,
        "package_row": package_row,
        "timestamp_row": timestamp_row,
        "channel_map_confirmed": bool(args.confirmed_channel_map),
        "args": vars(args),
        "kiss_wiring": {
            "ALS_plus": "Cyton DVDD/3V3",
            "ALS_minus": "Cyton GND",
            "ALS_OUT": "Cyton D12/A6",
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    events_f = events_path.open("w", newline="", encoding="utf-8")
    ew = csv.DictWriter(events_f, fieldnames=["unix_time", "lsl_time", "event", "details"])
    ew.writeheader()
    diag_f = diag_path.open("w", newline="", encoding="utf-8")
    dw = csv.DictWriter(
        diag_f,
        fieldnames=[
            "unix_time",
            "lsl_time",
            "chunk_index",
            "samples",
            "samples_total",
            "buffer_before",
            "buffer_after",
            "effective_rate_hz",
            "package_first",
            "package_last",
            "package_skip_count",
            "max_timestamp_gap_sec",
            "aux_min",
            "aux_max",
            "als_min",
            "als_max",
            "als_mean",
        ],
    )
    dw.writeheader()

    def log(event: str, details: Optional[dict] = None) -> None:
        now_lsl = local_clock()
        details_s = json.dumps(details or {}, sort_keys=True, default=str)
        ew.writerow({"unix_time": time.time(), "lsl_time": now_lsl, "event": event, "details": details_s})
        events_f.flush()
        print(f"[{time.strftime('%H:%M:%S')}] {event} {details_s}", flush=True)
        push_marker(status_outlet, event, details or {})

    stop = {"value": False}

    def stop_handler(signum, frame) -> None:  # type: ignore[no-untyped-def]
        stop["value"] = True
        log("STOP_SIGNAL_RECEIVED", {"signal": signum})

    signal.signal(signal.SIGINT, stop_handler)
    signal.signal(signal.SIGTERM, stop_handler)

    prepared = False
    streaming = False
    last_recon_ts: Optional[float] = None
    last_pkg: Optional[int] = None
    samples_total = 0
    chunk_index = 0
    start_lsl: Optional[float] = None

    try:
        log("BRIDGE_STARTING", {"manifest": str(manifest_path), "version": BRIDGE_VERSION})
        try:
            board.prepare_session()
        except Exception as exc:
            raise RuntimeError(
                "BrainFlow could not open the OpenBCI board. Close OpenBCI GUI and any serial monitor, "
                "confirm the COM port, unplug/replug the dongle, then rerun. Original error: " + repr(exc)
            )
        prepared = True
        log("BRAINFLOW_SESSION_PREPARED", {"serial_port": args.serial_port})

        if args.enable_analog_aux and args.board != "synthetic":
            log("CYTON_ANALOG_MODE_COMMAND_START", {"command": args.analog_command})
            response = board.config_board(args.analog_command)
            log("CYTON_ANALOG_MODE_COMMAND_SENT", {"command": args.analog_command, "response": str(response)})
            time.sleep(0.25)

        board.start_stream(450000, "")
        streaming = True
        start_lsl = local_clock()
        log(
            "BRAINFLOW_STREAM_STARTED",
            {"sample_rate_hz": srate, "eeg_channels": n_eeg, "analog_channels": len(analog_rows)},
        )
        log("LSL_EEG_OUTLET_ONLINE", {"stream_name": args.stream_name, "source_id": source_id})
        if aux_outlet is not None:
            log("LSL_ANALOG_AUX_OUTLET_ONLINE", {"stream_name": args.aux_stream_name, "source_id": aux_source_id, "labels": DEFAULT_AUX_LABELS, "rows": analog_rows})
        if als_outlet is not None:
            log("LSL_ALS_PT19_OUTLET_ONLINE", {"stream_name": args.als_stream_name, "source_id": als_source_id, "aux_channel": args.als_aux_channel, "label": als_label, "row": als_source_row})

        run_start = time.time()
        while not stop["value"]:
            if args.max_runtime_sec > 0 and (time.time() - run_start) >= args.max_runtime_sec:
                log("MAX_RUNTIME_REACHED", {"max_runtime_sec": args.max_runtime_sec})
                break
            buffer_before = int(board.get_board_data_count())
            if buffer_before < max(1, args.chunk_size):
                time.sleep(max(0.001, args.poll_sec))
                continue
            data = board.get_board_data()
            buffer_after = int(board.get_board_data_count())
            if data.size == 0:
                continue

            eeg = data[eeg_rows, :].T.astype(np.float32, copy=False)
            nsamp = int(eeg.shape[0])
            if nsamp <= 0:
                continue

            aux = None
            als = None
            if args.enable_analog_aux and analog_rows:
                aux = data[analog_rows, :].T.astype(np.float32, copy=False)
                if als_outlet is not None:
                    als = aux[:, args.als_aux_channel].astype(np.float32, copy=False)

            packages = None
            if package_row is not None and 0 <= package_row < data.shape[0]:
                packages = np.rint(data[package_row, :]).astype(int)

            ts_list: List[float] = []
            package_skip_count = 0
            max_gap = 0.0

            if args.timestamp_mode == "reconstructed":
                if last_recon_ts is None:
                    last_recon_ts = local_clock() - nsamp * dt
                for i in range(nsamp):
                    step = dt
                    if packages is not None:
                        pkg = int(packages[i])
                        if last_pkg is not None:
                            delta = (pkg - last_pkg) % 256
                            miss = max(0, delta - 1) if delta != 0 else 0
                            package_skip_count += miss
                            step = (1 + miss) * dt
                        last_pkg = pkg
                    last_recon_ts += step
                    max_gap = max(max_gap, step)
                    ts_list.append(last_recon_ts)
                for row, ts in zip(eeg, ts_list):
                    eeg_outlet.push_sample(row.tolist(), timestamp=ts, pushthrough=False)
                if aux_outlet is not None and aux is not None:
                    for row, ts in zip(aux, ts_list):
                        aux_outlet.push_sample(row.tolist(), timestamp=ts, pushthrough=False)
                if als_outlet is not None and als is not None:
                    for value, ts in zip(als, ts_list):
                        als_outlet.push_sample([float(value)], timestamp=ts, pushthrough=False)
            else:
                now = local_clock()
                eeg_outlet.push_chunk(eeg.tolist(), timestamp=now)
                if aux_outlet is not None and aux is not None:
                    aux_outlet.push_chunk(aux.tolist(), timestamp=now)
                if als_outlet is not None and als is not None:
                    als_outlet.push_chunk([[float(x)] for x in als], timestamp=now)

            chunk_index += 1
            samples_total += nsamp
            now_lsl = local_clock()
            eff_rate = samples_total / max(1e-9, now_lsl - (start_lsl or now_lsl))
            row = {
                "unix_time": time.time(),
                "lsl_time": now_lsl,
                "chunk_index": chunk_index,
                "samples": nsamp,
                "samples_total": samples_total,
                "buffer_before": buffer_before,
                "buffer_after": buffer_after,
                "effective_rate_hz": eff_rate,
                "package_first": int(packages[0]) if packages is not None and len(packages) else -1,
                "package_last": int(packages[-1]) if packages is not None and len(packages) else -1,
                "package_skip_count": package_skip_count,
                "max_timestamp_gap_sec": max_gap,
                "aux_min": float(np.nanmin(aux)) if aux is not None and aux.size else np.nan,
                "aux_max": float(np.nanmax(aux)) if aux is not None and aux.size else np.nan,
                "als_min": float(np.nanmin(als)) if als is not None and als.size else np.nan,
                "als_max": float(np.nanmax(als)) if als is not None and als.size else np.nan,
                "als_mean": float(np.nanmean(als)) if als is not None and als.size else np.nan,
            }
            dw.writerow(row)
            diag_f.flush()

            heartbeat_every_chunks = max(1, int((srate * 5) / max(1, args.chunk_size)))
            if chunk_index % heartbeat_every_chunks == 0:
                log(
                    "EEG_AUX_ALS_BRIDGE_HEARTBEAT",
                    {
                        "samples_total": samples_total,
                        "effective_rate_hz": round(eff_rate, 3),
                        "als_min": row["als_min"],
                        "als_max": row["als_max"],
                    },
                )
        log("BRIDGE_STOPPING", {"samples_total": samples_total})
        return 0
    except Exception as exc:
        try:
            log("BRIDGE_ERROR", {"error": repr(exc)})
        except Exception:
            print("BRIDGE_ERROR", repr(exc), file=sys.stderr)
        raise
    finally:
        try:
            if streaming:
                board.stop_stream()
        except Exception:
            pass
        try:
            if prepared and args.restore_default_mode_on_exit and args.enable_analog_aux and args.board != "synthetic":
                try:
                    board.config_board("/0")
                except Exception:
                    pass
        except Exception:
            pass
        try:
            if prepared:
                board.release_session()
        except Exception:
            pass
        try:
            events_f.close()
            diag_f.close()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
