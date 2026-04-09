from jwt import decode

def decode_sign_token(key: str, value: str) -> dict:
    return decode(value, key, algorithms=["HS256"])
