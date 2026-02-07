import unittest

from common.protocol import decode_message, encode_message, validate_request


class ProtocolTests(unittest.TestCase):
    def test_encode_decode_roundtrip(self):
        payload = {"type": "ping"}
        encoded = encode_message(payload)
        decoded = decode_message(encoded.strip())
        self.assertEqual(decoded, payload)

    def test_validate_request(self):
        ok, _ = validate_request({"type": "ping"})
        self.assertTrue(ok)

        ok, _ = validate_request({"type": "register", "username": "a"})
        self.assertFalse(ok)

        ok, _ = validate_request({"type": "unknown"})
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
