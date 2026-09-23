"""Reader for the locally adapted Cerelog EMG4/ALS1 firmware, not stock firmware.

Keep electrodes OFF BODY for initial hardware checks. Explicit EMG conditions
require confirmation of the manufacturer's battery-only, no-mains setup.
The Cerelog is not isolated; a transport PASS is not a safety certification.
"""
import argparse
import collections
import csv
import datetime as dt
import json
from pathlib import Path
import statistics
import time

import serial

FIRMWARE = "CERELOG_V1_EMG4_ALS1_1K_V1"
GAINS = [24, 24, 24, 24, 1, 0, 0, 0]
EXPECTED_REGISTERS = {
    1: 0xB4, 2: 0xD0, 3: 0xE8, 4: 0,
    5: 0x60, 6: 0x60, 7: 0x60, 8: 0x60, 9: 0,
    10: 0x81, 11: 0x81, 12: 0x81,
    13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 21: 0, 22: 0, 23: 0,
}
VREF = 4.5  # Nominal ADS1299 internal reference; not an independent calibration.


def command(message_type, register=0, value=0, timestamp=None):
    timestamp = int(time.time()) if timestamp is None else timestamp
    payload = bytes([message_type]) + timestamp.to_bytes(4, "big") + bytes([register, value])
    return b"\xaa\xbb" + payload + bytes([sum(payload) & 255, 0xCC, 0xDD])


def check_configuration(config):
    expected = {"firmware": FIRMWARE, "rate_hz": 1000, "stream_baud": 460800,
                "gains": GAINS, "active_channels": [1, 2, 3, 4, 5],
                "bias_driver": False, "readback_ok": True}
    for key, value in expected.items():
        if config.get(key) != value:
            raise ValueError(f"Unexpected configuration {key}: {config.get(key)!r}")
    registers = config.get("registers", [])
    if len(registers) != 24 or registers[0] != 0x3E:
        raise ValueError(f"Expected 8-channel ADS1299 register ID 0x3E: {registers}")
    for address, value in EXPECTED_REGISTERS.items():
        mask = 0xFE if address == 3 else 0xFF  # Bit 0 of CONFIG3 is read-only status.
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
                drop = len(self.buffer) - keep
                self.discard(drop)
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
    emg_uv = [count * VREF * 1e6 / (24 * 2**23) for count in counts[:4]]
    als_v = counts[4] * VREF / 2**23
    return emg_uv + [als_v]


class Device:
    def __init__(self, port):
        self.ser = serial.Serial(port=None, baudrate=9600, timeout=0.1, write_timeout=2)
        self.ser.dtr = False
        self.ser.rts = False
        self.ser.port = port

    def reset(self):
        # CH340's RTS drives ESP32 EN; deassert DTR so GPIO0 does not select bootloader.
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
        raise RuntimeError(f"No compatible configuration reply on {self.ser.port}; do not use the stock reader with this build.")

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
    stamps = [f[0] for f in frames]
    delta = [(b - a) & 0xFFFFFFFF for a, b in zip(stamps, stamps[1:])]
    rate = 1000 * len(delta) / sum(delta) if delta and sum(delta) else None
    prefixes = collections.Counter(f"0x{status >> 20:X}" for _, status, _, _ in frames)
    channels = []
    for i in range(8):
        values = [frame[2][i] for frame in frames]
        channels.append({"channel": i + 1, "gain": GAINS[i], "min_counts": min(values),
                         "max_counts": max(values), "median_counts": statistics.median(values),
                         "rail_samples": sum(v <= -8388608 or v >= 8388607 for v in values)})
    als = [scale(frame[2])[4] for frame in frames]
    active_discarded = parser.discarded_bytes - parser.initial_alignment_bytes
    passed = (len(frames) >= 1000 and parser.bad_frames == 0 and active_discarded == 0
              and rate is not None and 995 <= rate <= 1005
              and max(delta) <= 3 and prefixes.get("0xC", 0) == len(frames))
    return {
        "status": "PASS" if passed else "FAIL", "port": port,
        "scope": "Boot register readback, serial framing/checksums, ADC status and approximate sample rate. NOT an on-body signal-quality or electrical-safety certification.",
        "firmware_configuration": config, "nominal_vref_volts": VREF,
        "frames": len(frames), "bad_frames": parser.bad_frames,
        "discarded_bytes": parser.discarded_bytes, "trailing_partial_bytes": len(parser.buffer),
        "initial_alignment_bytes": parser.initial_alignment_bytes,
        "discarded_bytes_after_first_frame": active_discarded,
        "host_duration_seconds": elapsed, "device_timestamp_rate_hz": rate,
        "timestamp_delta_ms_counts": dict(collections.Counter(delta)),
        "max_delta_ms": max(delta) if delta else None, "adc_status_prefix_counts": dict(prefixes),
        "channels": channels,
        "als_volts": {"min": min(als), "median": statistics.median(als), "max": max(als)},
        "timing_note": "Device timestamps have 1 ms resolution and no sequence counter; host arrival is not acquisition time. This test cannot prove absence of every lost or repeated conversion.",
    }


def capture(port, seconds, out_dir, condition="bench"):
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
                instruction = {
                    "bench": "keep electrodes off-body for this bench check",
                    "emg-rest": "relaxed jaw baseline; remain still and do not talk",
                    "emg-activation": "follow the separately agreed gentle activation protocol",
                }[condition]
                print(f"Recording {seconds:g} seconds: {instruction}.", flush=True)
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
    basename = condition.replace("-", "_") + created.strftime("_%Y%m%dT%H%M%S_%fZ")
    csv_path = out_dir / (basename + ".csv")
    with csv_path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["device_elapsed_ms", "host_arrival_elapsed_s", "adc_status_hex"] +
                        [f"ch{i}_counts" for i in range(1, 9)] +
                        ["masseter_left_uV", "masseter_right_uV", "temporalis_left_uV", "temporalis_right_uV", "als_V"])
        for stamp, status, counts, arrival in frames:
            writer.writerow([stamp, f"{arrival:.6f}", f"{status:06X}", *counts, *scale(counts)])
    report = summarize(config, frames, parser, elapsed, port)
    report["started_utc"] = created.isoformat()
    report["condition"] = condition
    report["body_connected"] = condition != "bench"
    report["csv"] = str(csv_path.resolve())
    json_path = out_dir / (basename + ".json")
    with json_path.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(json.dumps(report, indent=2))
    print(f"Report saved: {json_path.resolve()}", flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="COM4")
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).parent / "recordings")
    parser.add_argument("--condition", choices=["bench", "emg-rest", "emg-activation"], default="bench")
    parser.add_argument("--confirm-battery-only", action="store_true",
                        help="Confirm battery-only equipment with chargers and mains-connected peripherals unplugged.")
    args = parser.parse_args()
    if not 2 <= args.seconds <= 300:
        parser.error("Choose 2 to 300 seconds.")
    if args.condition != "bench" and not args.confirm_battery_only:
        parser.error("Body-connected EMG requires --confirm-battery-only and the manufacturer's safety setup.")
    report = capture(args.port, args.seconds, args.out_dir, args.condition)
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
