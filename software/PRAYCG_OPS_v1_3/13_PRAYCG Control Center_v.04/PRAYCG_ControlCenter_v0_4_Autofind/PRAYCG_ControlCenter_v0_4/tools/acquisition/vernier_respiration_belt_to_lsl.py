"""
vernier_respiration_belt_to_lsl.py

Streams Vernier Go Direct Respiration Belt data to Lab Streaming Layer (LSL).

Primary PR-AYC-G use:
    Stream the raw Force channel from the Go Direct Respiration Belt
    so inhale/exhale phase can be reconstructed offline and aligned
    with EEG, Polar ECG/HRV, and StasisMarkers in LabRecorder.

Recommended hardware:
    Vernier Go Direct Respiration Belt, order code GDX-RB

Recommended connection:
    USB first for stability.
    BLE can work, but USB avoids Bluetooth contention with Polar H10.

Install:
    pip install godirect pylsl numpy

Run examples:
    python vernier_respiration_belt_to_lsl.py --connection usb
    python vernier_respiration_belt_to_lsl.py --connection ble
    python vernier_respiration_belt_to_lsl.py --connection usb --period-ms 50
    python vernier_respiration_belt_to_lsl.py --connection usb --all-channels

LabRecorder stream name:
    VernierRespirationBelt

Default stream:
    1 channel: force_N

Optional all-channel stream:
    force_N, respiration_rate_bpm, steps, step_rate_spm

Notes:
    - The built-in respiration-rate channel is delayed and may return NaN at first.
    - For respiratory phase analysis, use the raw force channel.
    - The stream is not a medical device stream and should not be used for diagnosis.
"""

import argparse
import csv
import math
import os
import signal
import sys
import time
from datetime import datetime
from typing import List, Optional

import numpy as np
from pylsl import StreamInfo, StreamOutlet, local_clock

try:
    from godirect import GoDirect
except ImportError as exc:
    raise SystemExit(
        "Could not import godirect. Install it with:\n\n"
        "    pip install godirect\n"
    ) from exc


# Vernier GDX-RB channel map according to Vernier:
# 1. Force
# 2. Respiration Rate
# 3. Steps
# 4. Step Rate
FORCE_ONLY_SENSOR_NUMBERS = [1]
ALL_SENSOR_NUMBERS = [1, 2, 3, 4]


KEEP_RUNNING = True


def handle_shutdown(signum, frame):
    global KEEP_RUNNING
    KEEP_RUNNING = False
    print("\nShutdown requested. Stopping stream...")


signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)


def safe_float(value) -> float:
    """Convert sensor values to finite floats or NaN."""
    try:
        if value is None:
            return float("nan")
        x = float(value)
        if math.isfinite(x):
            return x
        return float("nan")
    except Exception:
        return float("nan")


def clean_label(text: str) -> str:
    """Make sensor labels stable for LSL metadata."""
    text = str(text).strip().lower()
    replacements = {
        " ": "_",
        "(": "",
        ")": "",
        "/": "_",
        "-": "_",
        ".": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def sensor_description(sensor) -> str:
    return str(
        getattr(sensor, "sensor_description", None)
        or getattr(sensor, "description", None)
        or getattr(sensor, "name", None)
        or "sensor"
    )


def sensor_units(sensor) -> str:
    return str(
        getattr(sensor, "units", None)
        or getattr(sensor, "unit", None)
        or ""
    )


def find_device(godirect, device_name: Optional[str] = None):
    """
    Find a Go Direct device. If device_name is supplied, match by substring.
    Otherwise use godirect.get_device().
    """
    if device_name:
        print("Listing Go Direct devices...")
        devices = godirect.list_devices()
        if not devices:
            return None

        print("Available devices:")
        for idx, dev in enumerate(devices):
            print(f"  [{idx}] {getattr(dev, 'name', 'unknown')}")

        target = device_name.lower()
        for dev in devices:
            if target in getattr(dev, "name", "").lower():
                return dev

        print(f"No device matched name substring: {device_name!r}")
        return None

    return godirect.get_device(threshold=-200)


def build_lsl_outlet(enabled_sensors, nominal_srate: float, source_id: str) -> StreamOutlet:
    """
    Build an LSL outlet with metadata.
    """
    labels = []
    units = []

    for sensor in enabled_sensors:
        desc = sensor_description(sensor)
        unit = sensor_units(sensor)

        label = clean_label(desc)

        # Normalize common GDX-RB labels.
        if "force" in label:
            label = "force_N"
            unit = "newton"
        elif "respiration" in label and "rate" in label:
            label = "respiration_rate_bpm"
            unit = "breaths_per_minute"
        elif "step_rate" in label or ("step" in label and "rate" in label):
            label = "step_rate_spm"
            unit = "steps_per_minute"
        elif "steps" in label or "step" in label:
            label = "steps"
            unit = "count"

        labels.append(label)
        units.append(unit)

    info = StreamInfo(
        name="VernierRespirationBelt",
        type="Respiration",
        channel_count=len(enabled_sensors),
        nominal_srate=nominal_srate,
        channel_format="float32",
        source_id=source_id,
    )

    desc = info.desc()
    desc.append_child_value("manufacturer", "Vernier")
    desc.append_child_value("model", "Go Direct Respiration Belt")
    desc.append_child_value("order_code", "GDX-RB")
    desc.append_child_value("connection_note", "USB recommended for PR-AYC-G respiratory phase locking")
    desc.append_child_value("primary_channel_note", "Use force_N for offline inhale/exhale phase estimation")
    desc.append_child_value("created_utc", datetime.utcnow().isoformat() + "Z")

    channels = desc.append_child("channels")
    for label, unit in zip(labels, units):
        ch = channels.append_child("channel")
        ch.append_child_value("label", label)
        ch.append_child_value("unit", unit)
        ch.append_child_value("type", "Respiration")

    print("\nLSL outlet created:")
    print("  name: VernierRespirationBelt")
    print("  type: Respiration")
    print(f"  channels: {labels}")
    print(f"  nominal_srate: {nominal_srate:.3f} Hz")

    return StreamOutlet(info)


def open_csv_logger(path: Optional[str], labels: List[str]):
    if not path:
        return None, None

    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    f = open(path, "w", newline="", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow(["lsl_time", "unix_time"] + labels)
    f.flush()
    return f, writer


def main():
    parser = argparse.ArgumentParser(
        description="Stream Vernier Go Direct Respiration Belt to LSL."
    )

    parser.add_argument(
        "--connection",
        choices=["usb", "ble"],
        default="usb",
        help="Connection method. USB is recommended for PR-AYC-G stability.",
    )

    parser.add_argument(
        "--period-ms",
        type=int,
        default=50,
        help=(
            "Sampling period in milliseconds. "
            "50 ms = 20 Hz; 100 ms = 10 Hz. "
            "Use 50 or 100 for respiration phase work."
        ),
    )

    parser.add_argument(
        "--device-name",
        type=str,
        default=None,
        help="Optional substring of the device name to connect to.",
    )

    parser.add_argument(
        "--all-channels",
        action="store_true",
        help="Stream Force, Respiration Rate, Steps, and Step Rate. Default streams Force only.",
    )

    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Optional CSV backup path, e.g. logs/vernier_resp.csv",
    )

    parser.add_argument(
        "--print-every",
        type=float,
        default=2.0,
        help="Seconds between console status prints.",
    )

    args = parser.parse_args()

    if args.period_ms < 10:
        raise SystemExit("Do not sample faster than 10 ms. Use 50 or 100 ms for this protocol.")

    nominal_srate = 1000.0 / args.period_ms
    use_usb = args.connection == "usb"
    use_ble = args.connection == "ble"

    print("\n======================================================")
    print(" Vernier Go Direct Respiration Belt -> LSL Bridge")
    print("======================================================")
    print(f"Connection: {args.connection}")
    print(f"Sampling period: {args.period_ms} ms ({nominal_srate:.2f} Hz)")
    print(f"Channels: {'all GDX-RB channels' if args.all_channels else 'Force only'}")
    print("Recommended PR-AYC-G stream order:")
    print("  1. Start OpenBCI LSL")
    print("  2. Start Polar H10 bridge")
    print("  3. Start this Vernier respiration bridge")
    print("  4. Open LabRecorder, Update, verify all streams")
    print("  5. Start recording")
    print("  6. Run PsychoPy protocol")
    print("======================================================\n")

    godirect = GoDirect(use_usb=use_usb, use_ble=use_ble)

    device = None
    csv_file = None

    try:
        device = find_device(godirect, args.device_name)
        if device is None:
            raise SystemExit(
                "No Vernier Go Direct device found. "
                "If using USB, connect the belt by USB. "
                "If using BLE, make sure it is awake and not already claimed by another app."
            )

        print(f"Found device: {getattr(device, 'name', 'unknown')}")

        if not device.open():
            raise SystemExit("Could not open device.")

        print("Device opened.")

        available_sensors = device.list_sensors()
        print("\nAvailable sensors:")
        for s in available_sensors:
            num = getattr(s, "sensor_number", getattr(s, "number", "?"))
            print(f"  Sensor {num}: {sensor_description(s)} [{sensor_units(s)}]")

        sensor_numbers = ALL_SENSOR_NUMBERS if args.all_channels else FORCE_ONLY_SENSOR_NUMBERS
        print(f"\nEnabling sensors: {sensor_numbers}")

        device.enable_sensors(sensor_numbers)

        if not device.start(period=args.period_ms):
            raise SystemExit("Could not start data collection.")

        enabled_sensors = device.get_enabled_sensors()

        if not enabled_sensors:
            raise SystemExit("No enabled sensors returned after start().")

        labels = []
        for sensor in enabled_sensors:
            desc = sensor_description(sensor)
            label = clean_label(desc)
            if "force" in label:
                label = "force_N"
            elif "respiration" in label and "rate" in label:
                label = "respiration_rate_bpm"
            elif "step_rate" in label or ("step" in label and "rate" in label):
                label = "step_rate_spm"
            elif "steps" in label or "step" in label:
                label = "steps"
            labels.append(label)

        outlet = build_lsl_outlet(
            enabled_sensors=enabled_sensors,
            nominal_srate=nominal_srate,
            source_id=f"vernier_gdx_rb_{args.connection}_01",
        )

        csv_file, csv_writer = open_csv_logger(args.csv, labels)

        print("\nStreaming. In LabRecorder, click Update and confirm:")
        print("  VernierRespirationBelt")
        print("\nPress Ctrl+C to stop.\n")

        n_samples = 0
        last_print = time.time()

        while KEEP_RUNNING:
            # read() blocks until a measurement arrives.
            ok = device.read()

            if not ok:
                time.sleep(0.001)
                continue

            values = [safe_float(sensor.value) for sensor in enabled_sensors]
            ts = local_clock()

            outlet.push_sample(values, timestamp=ts)
            n_samples += 1

            if csv_writer is not None:
                csv_writer.writerow([ts, time.time()] + values)
                if n_samples % 50 == 0:
                    csv_file.flush()

            now = time.time()
            if now - last_print >= args.print_every:
                pretty = ", ".join(
                    f"{label}={value:.4g}" if math.isfinite(value) else f"{label}=NaN"
                    for label, value in zip(labels, values)
                )
                print(f"[{n_samples:>7} samples] {pretty}")
                last_print = now

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received.")

    finally:
        print("Closing Vernier bridge...")

        try:
            if device is not None:
                device.stop()
        except Exception:
            pass

        try:
            if device is not None:
                device.close()
        except Exception:
            pass

        try:
            godirect.quit()
        except Exception:
            pass

        try:
            if csv_file is not None:
                csv_file.flush()
                csv_file.close()
        except Exception:
            pass

        print("Done.")


if __name__ == "__main__":
    main()

