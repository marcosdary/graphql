import unittest

from jwt import encode

from app.utils.decode_sign_token import decode_sign_token


class TestDecodeSignToken(unittest.TestCase):
    def test_decode_sign_token_returns_payload(self):
        key = "test-secret"
        payload = {"userId": "u-1", "role": "ADMIN"}
        token = encode(payload, key, algorithm="HS256")

        decoded = decode_sign_token(key=key, value=token)

        self.assertEqual(decoded["userId"], payload["userId"])
        self.assertEqual(decoded["role"], payload["role"])


if __name__ == "__main__":
    unittest.main()
