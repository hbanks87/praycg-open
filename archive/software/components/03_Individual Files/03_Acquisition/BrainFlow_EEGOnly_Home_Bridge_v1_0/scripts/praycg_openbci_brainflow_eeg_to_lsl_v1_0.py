#!/usr/bin/env python3
"""
PRAYCG OpenBCI BrainFlow EEG-only to LSL Bridge v1.0

Purpose
-------
A simple public-home version of the PR-AYC-G acquisition bridge for users who do
not want to wire an ALS-PT19 / photodiode timing channel.

Streams published
-----------------
1. obci_eeg1             8 or 16 EEG channels, depending on board selection
2. OpenBCIStatusMarkers  text markers for bridge state / warnings / heartbeat

What this script deliberately does NOT do
-----------------------------------------
- It does not enable Cyton analog AUX mode.
- It does not publish ALS_PT19_Timing.
- It does not publish OpenBCIAnalogAux.
- It does not physically validate screen onset.

For rigorous timing/metrology runs, use the ALS-enabled bridge. For low-barrier
home/citizen-neuroscience runs, this EEG-only bridge is simpler.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import signal
import sys
import time
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

try:
    from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
except Exception as exc:  # pragma: no cover - user environment guard
    print("ERROR: brainflow is not installed or failed to import.", file=sys.stderr)
    print("Install with: python -m pip install brainflow", file=sys.stderr)
    print(f"Import error: {exc}", file=sys.stderr)
    raise

try:
    from pylsl import StreamInfo, StreamOutlet, local_clock
except Exception as exc:  # pragma: no cover - user environment guard
    print("ERROR: pylsl is not installed or failed to import.", file=sys.stderr)
    print("Install with: python -m pip install pylsl", file=sys.stderr)
    print(f"Import error: {exc}", file=sys.stderr)
    raise

try:
    import serial.tools.list_ports
except Exception:
    serial = None  # type: ignore


PRAYCG_EEG16_LABELS = [
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
    ("F7", "left_frontal_lateral"),
    ("F8", "right_frontal_lateral"),
    ("Oz", "midline_visual_control"),
]

PRAYCG_EEG8_LABELS = PRAYCG_EEG16_LABELS[:8]


@dataclass
class BridgeStats:
    board_label: str
    board_id: int
    stream_name: str
    status_stream_name: str
    source_id: str
    channel_count: int
    nominal_srate: float
    serial_port: str
    started_utc: str
    stopped_utc: Optional[str] = None
    duration_sec: float = 0.0
    samples_published: int = 0
    chunks_published: int = 0
    max_batch_gap_sec: float = 0.0
    mean_effective_rate_hz: float = 0.0
    notes: str = ""


def _board_id_from_label(label: str) -> Tuple[int, str]:
    normalized = str(label).strip().lower().replace("_", "-")
    mapping = {
        "cyton": ("CYTON_BOARD", "OpenBCI Cyton"),
        "cyton-daisy": ("CYTON_DAISY_BOARD", "OpenBCI Cyton+Daisy"),
        "daisy": ("CYTON_DAISY_BOARD", "OpenBCI Cyton+Daisy"),
        "synthetic": ("SYNTHETIC_BOARD", "BrainFlow Synthetic Board"),
        "synthetic-board": ("SYNTHETIC_BOARD", "BrainFlow Synthetic Board"),
    }
    if normalized in mapping:
        enum_name, pretty = mapping[normalized]
        try:
            return int(getattr(BoardIds, enum_name).value), pretty
        except AttributeError as exc:
            raise ValueError(f"Your BrainFlow install does not expose BoardIds.{enum_name}") from exc
    try:
        return int(label), f"custom_board_id_{label}"
    except ValueError as exc:
        raise ValueError(
            "--board must be cyton, cyton-daisy, synthetic, or an integer BrainFlow board id"
        ) from exc


def list_serial_ports() -> int:
    try:
        import serial.tools.list_ports as list_ports
    except Exception as exc:
        print("pyserial is required for --list-ports. Install with: python -m pip install pyserial")
        print(f"Import error: {exc}")
        return 2
    ports = list(list_ports.comports())
    if not ports:
        print("No serial ports found.")
        return 1
    print("Serial ports detected:")
    for p in ports:
        print(f"  {p.device:10s} | {p.description} | hwid={p.hwid}")
    return 0


def make_channel_labels(n_channels: int, confirmed_map: bool, custom_labels: Optional[str]) -> List[Tuple[str, str]]:
    if custom_labels:
        raw = [x.strip() for x in custom_labels.split(",") if x.strip()]
        if len(raw) != n_channels:
            raise ValueError(
                f"--channel-labels supplied {len(raw)} labels but EEG stream has {n_channels} channels"
            )
        return [(name, "custom") for name in raw]
    if confirmed_map and n_channels == 16:
        return PRAYCG_EEG16_LABELS
    if confirmed_map and n_channels == 8:
        return PRAYCG_EEG8_LABELS
    return [(f"Ch{i+1}", "unconfirmed") for i in range(n_channels)]


def create_eeg_outlet(
    *,
    name: str,
    stream_type: str,
    channel_labels: Sequence[Tuple[str, str]],
    srate: float,
    source_id: str,
    board_label: str,
    board_id: int,
    confirmed_channel_map: bool,
) -> StreamOutlet:
    info = StreamInfo(name, stream_type, len(channel_labels), float(srate), "float32", source_id)
    desc = info.desc()
    desc.append_child_value("manufacturer", "OpenBCI/BrainFlow")
    desc.append_child_value("created_by", "PRAYCG_BrainFlow_EEGOnly_LSL_Bridge_v1_0")
    desc.append_child_value("board_label", board_label)
    desc.append_child_value("board_id", str(board_id))
    desc.append_child_value("channel_map_confirmed", str(bool(confirmed_channel_map)))
    channels = desc.append_child("channels")
    for idx, (label, roi) in enumerate(channel_labels, start=1):
        ch = channels.append_child("channel")
        ch.append_child_value("label", label)
        ch.append_child_value("unit", "microvolts")
        ch.append_child_value("type", "EEG")
        ch.append_child_value("index_1based", str(idx))
        ch.append_child_value("roi", roi)
    return StreamOutlet(info, chunk_size=0, max_buffered=360)


def create_status_outlet(name: str, source_id: str) -> StreamOutlet:
    info = StreamInfo(name, "Markers", 1, 0, "string", source_id + "_status")
    info.desc().append_child_value("created_by", "PRAYCG_BrainFlow_EEGOnly_LSL_Bridge_v1_0")
    return StreamOutlet(info)


def push_status(outlet: Optional[StreamOutlet], text: str, verbose: bool = True) -> None:
    stamp = datetime.now(timezone.utc).isoformat()
    msg = f"{stamp} | {text}"
    if verbose:
        print(msg, flush=True)
    if outlet is not None:
        try:
            outlet.push_sample([msg], timestamp=local_clock())
        except Exception:
            pass


def configure_logger(level: str) -> None:
    level = (level or "none").lower()
    if level == "dev":
        BoardShim.enable_dev_board_logger()
    elif level == "board":
        BoardShim.enable_board_logger()
    else:
        BoardShim.disable_board_logger()


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Stream OpenBCI Cyton/Cyton-Daisy EEG to LSL using BrainFlow. No ALS/PT19, no analog AUX."
    )
    p.add_argument("--board", default="cyton-daisy", help="cyton, cyton-daisy, synthetic, or integer board id")
    p.add_argument("--serial-port", default="", help="Windows COM port, e.g. COM3. Required for Cyton/Cyton-Daisy.")
    p.add_argument("--list-ports", action="store_true", help="List serial ports and exit")
    p.add_argument("--stream-name", default="obci_eeg1", help="LSL EEG stream name")
    p.add_argument("--stream-type", default="EEG", help="LSL EEG stream type")
    p.add_argument("--status-stream-name", default="OpenBCIStatusMarkers", help="LSL status marker stream name")
    p.add_argument("--source-id", default="", help="Optional stable LSL source_id. Auto-generated if omitted.")
    p.add_argument("--confirmed-channel-map", action="store_true", help="Publish PRAYCG channel labels in LSL metadata")
    p.add_argument("--channel-labels", default="", help="Comma-separated custom channel labels. Must match EEG channel count.")
    p.add_argument("--duration", type=float, default=0.0, help="Optional duration in seconds. 0 means run until Ctrl+C.")
    p.add_argument("--buffer-size", type=int, default=450000, help="BrainFlow ring buffer size in samples")
    p.add_argument("--poll-sec", type=float, default=0.05, help="Polling interval for BrainFlow buffer")
    p.add_argument("--startup-settle-sec", type=float, default=1.0, help="Seconds to wait after start_stream before publishing")
    p.add_argument("--log-level", choices=["none", "board", "dev"], default="none", help="BrainFlow logger level")
    p.add_argument("--no-status-stream", action="store_true", help="Disable OpenBCIStatusMarkers stream")
    p.add_argument("--stats-json", default="", help="Optional path to write session statistics JSON on exit")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    if args.list_ports:
        return list_serial_ports()

    board_id, board_label = _board_id_from_label(args.board)
    is_synthetic = "synthetic" in board_label.lower()
    if not is_synthetic and not args.serial_port:
        raise SystemExit("--serial-port is required for OpenBCI Cyton/Cyton-Daisy, e.g. --serial-port COM3")

    configure_logger(args.log_level)

    params = BrainFlowInputParams()
    if args.serial_port:
        params.serial_port = args.serial_port

    source_id = args.source_id or f"praycg_obci_brainflow_eegonly_{args.board}_{uuid.uuid4().hex[:10]}"
    status_outlet = None if args.no_status_stream else create_status_outlet(args.status_stream_name, source_id)

    push_status(status_outlet, "PRAYCG_EEG_ONLY_BRIDGE_STARTING")
    push_status(status_outlet, f"BOARD_LABEL_{board_label}")
    push_status(status_outlet, f"BOARD_ID_{board_id}")
    push_status(status_outlet, "ALS_PT19_DISABLED_NO_ANALOG_AUX_STREAM")
    if not args.confirmed_channel_map:
        push_status(status_outlet, "CHANNEL_MAP_UNCONFIRMED_GENERIC_CH_LABELS")

    board = BoardShim(board_id, params)
    stats: Optional[BridgeStats] = None
    stop_requested = False

    def _handle_signal(signum, frame):  # noqa: ANN001
        nonlocal stop_requested
        stop_requested = True
        push_status(status_outlet, f"STOP_REQUESTED_SIGNAL_{signum}")

    signal.signal(signal.SIGINT, _handle_signal)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, _handle_signal)

    t0 = time.time()
    try:
        push_status(status_outlet, "BRAINFLOW_PREPARE_SESSION")
        board.prepare_session()

        eeg_channels = BoardShim.get_eeg_channels(board_id)
        n_eeg = len(eeg_channels)
        if n_eeg <= 0:
            raise RuntimeError(f"BrainFlow returned no EEG channels for board_id={board_id}")
        srate = float(BoardShim.get_sampling_rate(board_id))
        labels = make_channel_labels(n_eeg, args.confirmed_channel_map, args.channel_labels or None)

        eeg_outlet = create_eeg_outlet(
            name=args.stream_name,
            stream_type=args.stream_type,
            channel_labels=labels,
            srate=srate,
            source_id=source_id,
            board_label=board_label,
            board_id=board_id,
            confirmed_channel_map=args.confirmed_channel_map,
        )

        stats = BridgeStats(
            board_label=board_label,
            board_id=board_id,
            stream_name=args.stream_name,
            status_stream_name=args.status_stream_name,
            source_id=source_id,
            channel_count=n_eeg,
            nominal_srate=srate,
            serial_port=args.serial_port,
            started_utc=datetime.now(timezone.utc).isoformat(),
        )

        push_status(status_outlet, f"LSL_EEG_OUTLET_ONLINE_NAME_{args.stream_name}_CH_{n_eeg}_SRATE_{srate}")
        push_status(status_outlet, "BRAINFLOW_START_STREAM")
        board.start_stream(args.buffer_size)
        time.sleep(max(0.0, args.startup_settle_sec))
        push_status(status_outlet, "BRAINFLOW_STREAM_STARTED")

        last_batch_wall = time.time()
        last_heartbeat = time.time()
        while not stop_requested:
            if args.duration and (time.time() - t0) >= args.duration:
                push_status(status_outlet, "DURATION_COMPLETE")
                break

            data = board.get_board_data()
            if data is None or data.size == 0 or data.shape[1] == 0:
                time.sleep(max(0.005, args.poll_sec))
                continue

            now_wall = time.time()
            batch_gap = now_wall - last_batch_wall
            last_batch_wall = now_wall
            stats.max_batch_gap_sec = max(stats.max_batch_gap_sec, float(batch_gap))

            eeg = data[eeg_channels, :].T.astype(np.float32, copy=False)
            eeg = np.nan_to_num(eeg, nan=0.0, posinf=0.0, neginf=0.0)
            n = eeg.shape[0]
            if n:
                # LSL convention: for a regular-rate chunk, timestamp refers to the last sample.
                eeg_outlet.push_chunk(eeg.tolist(), timestamp=local_clock(), pushthrough=True)
                stats.samples_published += int(n)
                stats.chunks_published += 1

            if time.time() - last_heartbeat >= 10.0:
                elapsed = max(1e-9, time.time() - t0)
                eff = stats.samples_published / elapsed
                push_status(
                    status_outlet,
                    f"EEG_ONLY_BRIDGE_HEARTBEAT_SAMPLES_{stats.samples_published}_EFFRATE_{eff:.3f}_HZ_CHUNKS_{stats.chunks_published}",
                )
                last_heartbeat = time.time()

            time.sleep(max(0.001, args.poll_sec))

        return_code = 0
    except Exception as exc:
        push_status(status_outlet, f"ERROR_{type(exc).__name__}_{exc}")
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return_code = 1
    finally:
        try:
            push_status(status_outlet, "BRAINFLOW_STOP_STREAM")
            board.stop_stream()
        except Exception:
            pass
        try:
            push_status(status_outlet, "BRAINFLOW_RELEASE_SESSION")
            board.release_session()
        except Exception:
            pass

        if stats is not None:
            stats.stopped_utc = datetime.now(timezone.utc).isoformat()
            stats.duration_sec = float(max(0.0, time.time() - t0))
            if stats.duration_sec > 0:
                stats.mean_effective_rate_hz = stats.samples_published / stats.duration_sec
            stats.notes = "EEG-only public-home bridge. No ALS_PT19_Timing or OpenBCIAnalogAux stream published."
            if args.stats_json:
                out_path = Path(args.stats_json)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(json.dumps(asdict(stats), indent=2), encoding="utf-8")
                print(f"Wrote stats: {out_path}")
            print(json.dumps(asdict(stats), indent=2))
        push_status(status_outlet, "PRAYCG_EEG_ONLY_BRIDGE_STOPPED")
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
