"""Off-body bench reader for the local Cerelog EMG5/EOG2/ALS1 firmware.

This is not a stock Cerelog reader. Keep all electrodes OFF BODY throughout this
validation. A transport PASS is not a signal-quality or safety certification.
No serial port is selected automatically and this reader does not publish a
network stream. Optical event matching is a separate synchronization step.
"""
import argparse
import collections
import csv
import datetime as dt
import json
from pathlib import Path
import statistics
import time


FIRMWARE = "CERELOG_V1_EMG5_EOG2_ALS1_1K_V1"
GAINS = [24, 24, 24, 24, 1, 24, 24, 24]
ACTIVE_CHANNELS = list(range(1, 9))
EXPECTED_REGISTERS = {
    1: 0xB4, 2: 0xD0, 3: 0xE8, 4: 0,
    5: 0x60, 6: 0x60, 7: 0x60, 8: 0x60, 9: 0,
    10: 0x60, 11: 0x60, 12: 0x60,
    13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 21: 0, 22: 0, 23: 0,
}
VREF = 4.5  # Nominal ADS1299 internal reference; not an independent calibration.
CHANNEL_NAMES = (
    "Masseter_Left", "Masseter_Right", "Temporalis_Left", "Temporalis_Right",
    "ALS", "Frontalis_Right", "EOG_Horizontal", "EOG_Vertical",
)
CHANNEL_TYPES = ("EMG", "EMG", "EMG", "EMG", "ALS", "EMG", "EOG", "EOG")
CHANNEL_UNITS = ("uV", "uV", "uV", "uV", "V", "uV", "uV", "uV")
SCALED_COLUMNS = (
    "masseter_left_uV", "masseter_right_uV", "temporalis_left_uV",
    "temporalis_right_uV", "als_V", "frontalis_right_uV",
    "eog_horizontal_uV", "eog_vertical_uV",
)
CSV_COLUMNS = (
    "device_elapsed_ms", "host_arrival_elapsed_s", "adc_status_hex",
    *(f"ch{i}_counts" for i in range(1, 9)), *SCALED_COLUMNS,
)


def command(message_type, register=0, value=0, timestamp=None):
    timestamp = int(time.time()) if timestamp is None else timestamp
    payload = bytes([message_type]) + timestamp.to_bytes(4, "big") + bytes([register, value])
    return b"\xaa\xbb" + payload + bytes([sum(payload) & 255, 0xCC, 0xDD])


def check_configuration(config):
    if not isinstance(config, dict):
        raise ValueError("Expected a configuration object.")
    expected = {
        "firmware": FIRMWARE, "rate_hz": 1000, "stream_baud": 460800,
        "gains": GAINS, "active_channels": ACTIVE_CHANNELS,
        "bias_driver": False, "readback_ok": True,
    }
    for key, value in expected.items():
        actual = config.get(key)
        if actual != value or (isinstance(value, bool) and actual is not value):
            raise ValueError(f"Unexpected configuration {key}: {actual!r}")
    registers = config.get("registers", [])
    if (not isinstance(registers, list) or len(registers) != 24
            or any(type(value) is not int or not 0 <= value <= 255 for value in registers)
            or registers[0] != 0x3E):
        raise ValueError(f"Expected 24 byte registers and 8-channel ADS1299 ID 0x3E: {registers}")
    for address, value in EXPECTED_REGISTERS.items():
        mask = 0xFE if address == 3 else 0xFF  # CONFIG3 bit 0 is read-only status.
        if registers[address] & mask != value & mask:
            raise ValueError(f"Register 0x{address:02X}: got {registers[address]:02X}, expected {value:02X}")


class FrameParser:
    def __init__(self):
        self.buffer = bytearray()
        self.bad_frames = 0
        self.discarded_bytes = 0
        self.initial_alignment_bytes = 0
        self.frame_count = 0

    def discard(self, count):
        self.discarded_bytes += count
        if self.frame_count == 0:
            self.initial_alignment_bytes += count
        del self.buffer[:count]

    def feed(self, data):
        self.buffer.extend(data)
        frames = []
        while len(self.buffer) >= 2:
            pos = self.buffer.find(b"\xab\xcd")
            if pos < 0:
                keep = 1 if self.buffer[-1] == 0xAB else 0
                self.discard(len(self.buffer) - keep)
                break
            self.discard(pos)
            if len(self.buffer) < 37:
                break
            frame = self.buffer[:37]
            if frame[2] != 31 or frame[35:37] != b"\xdc\xba" or sum(frame[2:34]) & 255 != frame[34]:
                self.bad_frames += 1
                self.discard(1)
                continue
            del self.buffer[:37]
            stamp = int.from_bytes(frame[3:7], "big")
            status = int.from_bytes(frame[7:10], "big")
            counts = tuple(int.from_bytes(frame[i:i + 3], "big", signed=True) for i in range(10, 34, 3))
            frames.append((stamp, status, counts))
            self.frame_count += 1
        return frames


def scale(counts):
    """Return eight values in hardware order, CH5 in V and all others in uV."""
    if len(counts) != 8:
        raise ValueError("Exactly eight channel counts are required in hardware order.")
    return [count * VREF / (GAINS[i] * 2**23) * (1 if i == 4 else 1e6)
            for i, count in enumerate(counts)]


def validate_port(port):
    if not isinstance(port, str) or not port or port != port.strip() or any(c in port for c in "*?\r\n"):
        raise ValueError("Specify one exact serial port, for example COM4; no automatic discovery or wildcards.")
    return port


class Device:
    def __init__(self, port):
        validate_port(port)
        # Lazy import lets protocol/scaling tests run without serial dependencies.
        import serial
        self.ser = serial.Serial(port=None, baudrate=9600, timeout=0.1, write_timeout=2)
        self.ser.dtr = False
        self.ser.rts = False
        self.ser.port = port

    def reset(self):
        # CH340 RTS drives ESP32 EN; DTR remains deasserted to avoid bootloader.
        self.ser.dtr = False
        self.ser.rts = True
        time.sleep(0.12)
        self.ser.rts = False

    def connect(self):
        self.ser.open()
        self.reset()
        time.sleep(4.5)
        self.ser.reset_input_buffer()
        self.ser.write(command(3))
        self.ser.flush()
        deadline = time.monotonic() + 5
        reply = bytearray()
        while time.monotonic() < deadline:
            reply.extend(self.ser.read(max(1, self.ser.in_waiting)))
            while b"\n" in reply:
                line, _, remainder = reply.partition(b"\n")
                reply = bytearray(remainder)
                if line.startswith(b"CERELOG_CFG "):
                    config = json.loads(line[len(b"CERELOG_CFG "):])
                    check_configuration(config)
                    return config
        raise RuntimeError(f"No compatible configuration reply on {self.ser.port}; stock and EMG4/ALS1 readers are incompatible.")

    def start(self):
        self.ser.write(command(2, 1, 6))
        self.ser.flush()
        time.sleep(0.05)
        self.ser.baudrate = 460800

    def close(self):
        if self.ser.is_open:
            try:
                self.reset()  # Stops acquisition, returns to waiting at 9600 baud.
            finally:
                self.ser.close()


def summarize(config, frames, parser, elapsed, port):
    check_configuration(config)
    stamps = [f[0] for f in frames]
    delta = [(b - a) & 0xFFFFFFFF for a, b in zip(stamps, stamps[1:])]
    rate = 1000 * len(delta) / sum(delta) if delta and sum(delta) else None
    prefixes = collections.Counter(f"0x{status >> 20:X}" for _, status, _, _ in frames)
    scaled = [scale(frame[2]) for frame in frames]
    channels = []
    for i in range(8):
        counts = [frame[2][i] for frame in frames]
        values = [row[i] for row in scaled]
        channels.append({
            "channel": i + 1, "name": CHANNEL_NAMES[i], "type": CHANNEL_TYPES[i],
            "unit": CHANNEL_UNITS[i], "gain": GAINS[i], "active": True,
            "scaled_csv_column": SCALED_COLUMNS[i],
            "min_counts": min(counts) if counts else None,
            "max_counts": max(counts) if counts else None,
            "median_counts": statistics.median(counts) if counts else None,
            "rail_samples": sum(v <= -8388608 or v >= 8388607 for v in counts),
            "min_scaled": min(values) if values else None,
            "median_scaled": statistics.median(values) if values else None,
            "max_scaled": max(values) if values else None,
        })
    active_discarded = parser.discarded_bytes - parser.initial_alignment_bytes
    passed = (len(frames) >= 1000 and parser.bad_frames == 0 and active_discarded == 0
              and rate is not None and 995 <= rate <= 1005
              and max(delta) <= 3 and prefixes.get("0xC", 0) == len(frames))
    als = channels[4]
    return {
        "status": "PASS" if passed else "FAIL", "port": port,
        "scope": "Off-body boot register readback, serial framing/checksums, ADC status and approximate sample rate. NOT on-body signal quality, electrode-placement, electrical-safety or cross-device-sync certification.",
        "firmware_configuration": config, "nominal_vref_volts": VREF,
        "csv_columns": list(CSV_COLUMNS),
        "frames": len(frames), "bad_frames": parser.bad_frames,
        "discarded_bytes": parser.discarded_bytes, "trailing_partial_bytes": len(parser.buffer),
        "initial_alignment_bytes": parser.initial_alignment_bytes,
        "discarded_bytes_after_first_frame": active_discarded,
        "host_duration_seconds": elapsed, "device_timestamp_rate_hz": rate,
        "timestamp_delta_ms_counts": dict(collections.Counter(delta)),
        "max_delta_ms": max(delta) if delta else None, "adc_status_prefix_counts": dict(prefixes),
        "channels": channels,
        "als_volts": {"min": als["min_scaled"], "median": als["median_scaled"], "max": als["max_scaled"]},
        "timing_note": "Device timestamps have 1 ms resolution and no sequence counter; host arrival is not acquisition time. This test cannot prove absence of every lost or repeated conversion. Dual ALS barcode event alignment, clock drift and residual error must be measured separately.",
    }


def capture(port, seconds, out_dir, *, confirm_off_body=False):
    if not confirm_off_body:
        raise ValueError("Explicit confirmation that every electrode is off-body is required for this bench-only reader.")
    if not 2 <= seconds <= 300:
        raise ValueError("Choose 2 to 300 seconds.")
    validate_port(port)
    out_dir = Path(out_dir)
    device = Device(port)
    parser = FrameParser()
    frames = []
    created = dt.datetime.now(dt.timezone.utc)
    try:
        config = device.connect()
        print("Configuration verified:", json.dumps(config), flush=True)
        device.start()
        first = None
        started = time.monotonic()
        while first is None or time.monotonic() - first < seconds:
            data = device.ser.read(max(1, min(device.ser.in_waiting, 65536)))
            now = time.monotonic()
            decoded = parser.feed(data)
            if decoded and first is None:
                first = now
                print(f"Recording {seconds:g} seconds: keep every electrode OFF BODY.", flush=True)
            if first is None and now - started > 5:
                raise RuntimeError("No streaming frames received after start.")
            for stamp, status, counts in decoded:
                frames.append((stamp, status, counts, now - first))
            if frames and now - (first + frames[-1][3]) > 3:
                raise RuntimeError("Data stream stalled.")
        elapsed = time.monotonic() - first
    finally:
        device.close()
    out_dir.mkdir(parents=True, exist_ok=True)
    basename = created.strftime("bench_%Y%m%dT%H%M%S_%fZ")
    csv_path = out_dir / (basename + ".csv")
    with csv_path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(CSV_COLUMNS)
        for stamp, status, counts, arrival in frames:
            writer.writerow([stamp, f"{arrival:.6f}", f"{status:06X}", *counts, *scale(counts)])
    report = summarize(config, frames, parser, elapsed, port)
    report.update(started_utc=created.isoformat(), condition="bench", body_connected=False,
                  csv=str(csv_path.resolve()))
    json_path = out_dir / (basename + ".json")
    with json_path.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(json.dumps(report, indent=2))
    print(f"Report saved: {json_path.resolve()}", flush=True)
    return report


def build_argument_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True, help="Exact verified serial port; there is no default or automatic selection.")
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).parent / "recordings")
    parser.add_argument("--confirm-off-body", required=True, action="store_true",
                        help="Confirm every electrode is disconnected from the body for the entire bench capture.")
    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()
    if not 2 <= args.seconds <= 300:
        parser.error("Choose 2 to 300 seconds.")
    try:
        validate_port(args.port)
    except ValueError as exc:
        parser.error(str(exc))
    report = capture(args.port, args.seconds, args.out_dir, confirm_off_body=args.confirm_off_body)
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
