"""Offline protocol and scaling checks; never opens a serial port."""
import unittest

from cerelog_reader import (EXPECTED_REGISTERS, FIRMWARE, GAINS, FrameParser,
                            check_configuration, command, scale, summarize)


def packet(stamp=123, counts=(-8388608, -1, 0, 8388607, 1491308, 0, 0, 0)):
    data = bytes([31]) + stamp.to_bytes(4, "big") + bytes.fromhex("c00000")
    data += b"".join(value.to_bytes(3, "big", signed=True) for value in counts)
    return b"\xab\xcd" + data + bytes([sum(data) & 255]) + b"\xdc\xba"


class ReaderTests(unittest.TestCase):
    def test_handshake(self):
        value = command(2, 1, 6, timestamp=0x12345678)
        self.assertEqual(len(value), 12)
        self.assertEqual(value[:3], bytes.fromhex("aabb02"))
        self.assertEqual(value[3:9], bytes.fromhex("123456780106"))
        self.assertEqual(value[9], sum(value[2:9]) & 255)

    def test_fragmentation_and_signed_values(self):
        for chunk_size in (1, 2, 7, 36, 37, 41, 100):
            parser = FrameParser()
            raw = packet() + packet(124)
            frames = []
            for start in range(0, len(raw), chunk_size):
                frames.extend(parser.feed(raw[start:start + chunk_size]))
            self.assertEqual([f[0] for f in frames], [123, 124])
            self.assertEqual(frames[0][2][:4], (-8388608, -1, 0, 8388607))
            self.assertEqual(parser.bad_frames, 0)
            self.assertEqual(parser.discarded_bytes, 0)

    def test_resync_corrupt_checksum(self):
        bad = bytearray(packet())
        bad[34] ^= 1
        parser = FrameParser()
        frames = parser.feed(b"garbage" + bad + packet(124))
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0][0], 124)
        self.assertEqual(parser.bad_frames, 1)
        self.assertEqual(parser.discarded_bytes, 44)

    def test_mixed_gain_scaling(self):
        values = scale([2**22] * 8)
        self.assertEqual(values[:4], [93750] * 4)
        self.assertEqual(values[4], 2.25)

    def test_initial_alignment_is_separate_from_midstream_loss(self):
        parser = FrameParser()
        frames = parser.feed(b"\x00" + packet() + b"lost" + packet(124))
        self.assertEqual(len(frames), 2)
        self.assertEqual(parser.initial_alignment_bytes, 1)
        self.assertEqual(parser.discarded_bytes, 5)

    def test_register_validation_and_fail_closed(self):
        registers = [0] * 24
        registers[0] = 0x3E
        for key, value in EXPECTED_REGISTERS.items():
            registers[key] = value
        config = {"firmware": FIRMWARE, "rate_hz": 1000, "stream_baud": 460800,
                  "gains": GAINS, "active_channels": [1, 2, 3, 4, 5],
                  "bias_driver": False, "readback_ok": True, "registers": registers}
        check_configuration(config)
        registers[3] |= 1  # Read-only bias status does not invalidate configuration.
        check_configuration(config)
        registers[9] = 0x60  # ALS gain 24 is wrong and must fail.
        with self.assertRaises(ValueError):
            check_configuration(config)

    def test_quality_check_rejects_invalid_status_and_midstream_loss(self):
        frames = [(i, 0xC00000, (0,) * 8, i / 1000) for i in range(1001)]
        parser = FrameParser()
        self.assertEqual(summarize({}, frames, parser, 1, "TEST")["status"], "PASS")
        frames[0] = (0, 0, (0,) * 8, 0)
        self.assertEqual(summarize({}, frames, parser, 1, "TEST")["status"], "FAIL")
        frames[0] = (0, 0xC00000, (0,) * 8, 0)
        parser.discarded_bytes = 1
        self.assertEqual(summarize({}, frames, parser, 1, "TEST")["status"], "FAIL")
        parser.initial_alignment_bytes = 1
        self.assertEqual(summarize({}, frames, parser, 1, "TEST")["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
