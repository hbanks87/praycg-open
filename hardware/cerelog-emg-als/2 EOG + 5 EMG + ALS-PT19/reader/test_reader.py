"""Offline protocol/scaling tests. No serial port is ever opened."""
import contextlib
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from cerelog_reader import (
    ACTIVE_CHANNELS, CHANNEL_NAMES, CHANNEL_UNITS, CSV_COLUMNS, EXPECTED_REGISTERS,
    FIRMWARE, GAINS, SCALED_COLUMNS, FrameParser, build_argument_parser, capture,
    check_configuration, command, scale, summarize, validate_port,
)


def configuration():
    registers = [0] * 24
    registers[0] = 0x3E
    for address, value in EXPECTED_REGISTERS.items():
        registers[address] = value
    return {"firmware": FIRMWARE, "rate_hz": 1000, "stream_baud": 460800,
            "gains": GAINS.copy(), "active_channels": ACTIVE_CHANNELS.copy(),
            "bias_driver": False, "readback_ok": True, "registers": registers}


def packet(stamp=123, counts=(-8388608, -1, 0, 8388607, 1491308, -2, 2, -8388607), status=0xC00000):
    data = bytes([31]) + stamp.to_bytes(4, "big") + status.to_bytes(3, "big")
    data += b"".join(value.to_bytes(3, "big", signed=True) for value in counts)
    return b"\xab\xcd" + data + bytes([sum(data) & 255]) + b"\xdc\xba"


def report_frames(start=0):
    return [((start + i) & 0xFFFFFFFF, 0xC00000, (0,) * 8, i / 1000) for i in range(1001)]


class ReaderTests(unittest.TestCase):
    def test_handshake(self):
        value = command(2, 1, 6, timestamp=0x12345678)
        self.assertEqual(len(value), 12)
        self.assertEqual(value[:3], bytes.fromhex("aabb02"))
        self.assertEqual(value[3:9], bytes.fromhex("123456780106"))
        self.assertEqual(value[9], sum(value[2:9]) & 255)
        self.assertEqual(value[-2:], b"\xcc\xdd")

    def test_fragmentation_and_all_eight_signed_values(self):
        for chunk_size in (1, 2, 7, 36, 37, 41, 100):
            with self.subTest(chunk_size=chunk_size):
                parser = FrameParser()
                raw = packet() + packet(124)
                frames = []
                for start in range(0, len(raw), chunk_size):
                    frames.extend(parser.feed(raw[start:start + chunk_size]))
                self.assertEqual([f[0] for f in frames], [123, 124])
                self.assertEqual(frames[0][2], (-8388608, -1, 0, 8388607, 1491308, -2, 2, -8388607))
                self.assertEqual(frames[0][1], 0xC00000)
                self.assertEqual(parser.bad_frames, 0)
                self.assertEqual(parser.discarded_bytes, 0)

    def test_resync_corrupt_checksum_length_or_footer(self):
        for bad_index in (2, 34, 35, 36):
            with self.subTest(bad_index=bad_index):
                bad = bytearray(packet())
                bad[bad_index] ^= 1
                parser = FrameParser()
                frames = parser.feed(b"garbage" + bad + packet(124))
                self.assertEqual([frame[0] for frame in frames], [124])
                self.assertEqual(parser.bad_frames, 1)
                self.assertEqual(parser.discarded_bytes, 44)

    def test_split_header_and_trailing_partial(self):
        parser = FrameParser()
        self.assertEqual(parser.feed(b"noise\xab"), [])
        self.assertEqual(parser.initial_alignment_bytes, 5)
        self.assertEqual(parser.feed(packet()[1:20]), [])
        self.assertEqual(len(parser.buffer), 20)
        self.assertEqual(len(parser.feed(packet()[20:] + packet(124)[:15])), 1)
        self.assertEqual(len(parser.buffer), 15)
        self.assertEqual(len(parser.feed(packet(124)[15:])), 1)

    def test_mixed_gain_scaling_preserves_hardware_order_and_units(self):
        self.assertEqual(GAINS, [24, 24, 24, 24, 1, 24, 24, 24])
        values = scale([2**22] * 8)
        self.assertEqual(len(values), 8)
        self.assertEqual(values, [93750, 93750, 93750, 93750, 2.25, 93750, 93750, 93750])
        self.assertEqual(CHANNEL_NAMES[4:], ("ALS", "Frontalis_Right", "EOG_Horizontal", "EOG_Vertical"))
        self.assertEqual(CHANNEL_UNITS, ("uV", "uV", "uV", "uV", "V", "uV", "uV", "uV"))

    def test_signed_scaling_all_channels(self):
        self.assertEqual(scale([-2**23] * 8), [-187500, -187500, -187500, -187500, -4.5, -187500, -187500, -187500])
        self.assertEqual(scale([0] * 8), [0] * 8)
        one_lsb = scale([1] * 8)
        negative = scale([-1] * 8)
        self.assertEqual(negative, [-value for value in one_lsb])
        self.assertAlmostEqual(one_lsb[7], 4.5e6 / (24 * 2**23))
        with self.assertRaises(ValueError):
            scale([0] * 5)

    def test_initial_alignment_is_separate_from_midstream_loss(self):
        parser = FrameParser()
        frames = parser.feed(b"\x00" + packet() + b"lost" + packet(124))
        self.assertEqual(len(frames), 2)
        self.assertEqual(parser.initial_alignment_bytes, 1)
        self.assertEqual(parser.discarded_bytes, 5)

    def test_register_configuration_accepts_only_read_only_status_variation(self):
        config = configuration()
        check_configuration(config)
        config["registers"][3] |= 1
        check_configuration(config)

    def test_reject_old_profile_and_disabled_channels(self):
        for field, value in (
            ("firmware", "CERELOG_V1_EMG4_ALS1_1K_V1"),
            ("gains", [24, 24, 24, 24, 1, 0, 0, 0]),
            ("active_channels", [1, 2, 3, 4, 5]),
            ("rate_hz", 250), ("stream_baud", 115200), ("readback_ok", False),
            ("readback_ok", 1), ("bias_driver", True), ("bias_driver", 0),
        ):
            with self.subTest(field=field, value=value):
                config = configuration()
                config[field] = value
                with self.assertRaises(ValueError):
                    check_configuration(config)
        for address in (10, 11, 12):
            config = configuration()
            config["registers"][address] = 0x81
            with self.assertRaises(ValueError):
                check_configuration(config)

    def test_reject_als_gain_srb_bias_and_incorrect_id(self):
        for address, value in ((0, 0x3C), (9, 0x60), (21, 0x20), (3, 0xEC), (13, 1), (14, 1)):
            with self.subTest(address=address, value=value):
                config = configuration()
                config["registers"][address] = value
                with self.assertRaises(ValueError):
                    check_configuration(config)
        for address in range(5, 13):
            config = configuration()
            config["registers"][address] |= 0x08  # SRB2
            with self.assertRaises(ValueError):
                check_configuration(config)

    def test_reject_invalid_register_array(self):
        for registers in (None, [], [0] * 23, [0] * 25, ["0"] * 24, [256] * 24):
            config = configuration()
            config["registers"] = registers
            with self.assertRaises(ValueError):
                check_configuration(config)

    def test_quality_check_rejects_invalid_status_and_midstream_loss(self):
        frames = report_frames()
        parser = FrameParser()
        self.assertEqual(summarize(configuration(), frames, parser, 1, "TEST")["status"], "PASS")
        frames[0] = (0, 0, (0,) * 8, 0)
        self.assertEqual(summarize(configuration(), frames, parser, 1, "TEST")["status"], "FAIL")
        frames[0] = (0, 0xC00000, (0,) * 8, 0)
        parser.discarded_bytes = 1
        self.assertEqual(summarize(configuration(), frames, parser, 1, "TEST")["status"], "FAIL")
        parser.initial_alignment_bytes = 1
        self.assertEqual(summarize(configuration(), frames, parser, 1, "TEST")["status"], "PASS")

    def test_summary_metadata_includes_all_eight_channels_and_columns(self):
        report = summarize(configuration(), report_frames(), FrameParser(), 1, "TEST")
        self.assertEqual(len(report["channels"]), 8)
        self.assertEqual(report["csv_columns"], list(CSV_COLUMNS))
        self.assertEqual(len(CSV_COLUMNS), 19)
        self.assertEqual(CSV_COLUMNS[-8:], SCALED_COLUMNS)
        for i, channel in enumerate(report["channels"]):
            self.assertEqual(channel["channel"], i + 1)
            self.assertEqual(channel["name"], CHANNEL_NAMES[i])
            self.assertEqual(channel["unit"], CHANNEL_UNITS[i])
            self.assertEqual(channel["gain"], GAINS[i])
            self.assertTrue(channel["active"])

    def test_timestamp_wrap_and_empty_capture_are_handled_honestly(self):
        wrapped = summarize(configuration(), report_frames(0xFFFFFF00), FrameParser(), 1, "TEST")
        self.assertEqual(wrapped["status"], "PASS")
        self.assertEqual(wrapped["device_timestamp_rate_hz"], 1000)
        self.assertEqual(wrapped["max_delta_ms"], 1)
        self.assertIn("1 ms", wrapped["timing_note"])
        self.assertIn("no sequence counter", wrapped["timing_note"])
        empty = summarize(configuration(), [], FrameParser(), 0, "TEST")
        self.assertEqual(empty["status"], "FAIL")
        self.assertIsNone(empty["device_timestamp_rate_hz"])
        self.assertIsNone(empty["als_volts"]["min"])

    def test_summary_rejects_unverified_configuration(self):
        with self.assertRaises(ValueError):
            summarize({}, report_frames(), FrameParser(), 1, "TEST")

    def test_exact_port_and_off_body_confirmation_required_before_device_creation(self):
        for port in (None, "", " COM4", "COM4 ", "COM*", "COM?", "COM4\n"):
            with self.assertRaises(ValueError):
                validate_port(port)
        self.assertEqual(validate_port("COM4"), "COM4")
        with mock.patch("cerelog_reader.Device") as device:
            with self.assertRaises(ValueError):
                capture("COM4", 2, "unused")
            device.assert_not_called()
        parser = build_argument_parser()
        for args in ([], ["--port", "COM4"], ["--confirm-off-body"]):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                parser.parse_args(args)
        args = parser.parse_args(["--port", "COM4", "--confirm-off-body"])
        self.assertEqual(args.port, "COM4")
        self.assertTrue(args.confirm_off_body)

    def test_mocked_capture_writes_all_eight_scaled_channels_without_hardware(self):
        counts = (2**22, -2**22, 0, 1, 2**22, -2**22, 2**22, -1)
        raw = b"".join(packet(stamp=i, counts=counts) for i in range(1001))
        fake = mock.Mock()
        fake.connect.return_value = configuration()
        fake.ser.in_waiting = len(raw)
        fake.ser.read.return_value = raw
        with tempfile.TemporaryDirectory(prefix="cerelog_reader_offline_") as temp:
            with (mock.patch("cerelog_reader.Device", return_value=fake),
                  mock.patch("cerelog_reader.time.monotonic", side_effect=[0, 1, 3, 3]),
                  contextlib.redirect_stdout(io.StringIO())):
                report = capture("TEST_ONLY", 2, temp, confirm_off_body=True)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["condition"], "bench")
            self.assertFalse(report["body_connected"])
            with Path(report["csv"]).open(newline="", encoding="utf-8") as stream:
                rows = list(csv.reader(stream))
            self.assertEqual(rows[0], list(CSV_COLUMNS))
            self.assertEqual(len(rows), 1002)
            self.assertEqual(len(rows[1]), 19)
            self.assertEqual([float(value) for value in rows[1][-8:]], scale(counts))
            json_path = Path(report["csv"]).with_suffix(".json")
            saved = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["channels"][5]["name"], "Frontalis_Right")
            self.assertEqual(saved["channels"][7]["unit"], "uV")
        fake.close.assert_called_once_with()

    def test_mocked_connect_failure_closes_device_without_starting(self):
        fake = mock.Mock()
        fake.connect.side_effect = ValueError("Unexpected firmware")
        with mock.patch("cerelog_reader.Device", return_value=fake):
            with self.assertRaisesRegex(ValueError, "Unexpected firmware"):
                capture("TEST_ONLY", 2, "unused", confirm_off_body=True)
        fake.close.assert_called_once_with()
        fake.start.assert_not_called()


if __name__ == "__main__":
    unittest.main()
