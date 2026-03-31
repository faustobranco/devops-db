import base64
import hmac
import hashlib
import time
import struct


import base64


def decode_totp_secret(secret: str):
    try:
        # Base64 → string Base32
        decoded = base64.b64decode(secret).decode()

        # Base32 → bytes reais
        return base64.b32decode(decoded, casefold=True)

    except Exception:
        # já está em Base32
        return base64.b32decode(secret, casefold=True)
    


def generate_totp(secret: str, interval: int = 30, digits: int = 6):
    key = decode_totp_secret(secret)
    counter = int(time.time()) // interval

    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()

    offset = h[-1] & 0x0F
    code = (
        ((h[offset] & 0x7F) << 24)
        | ((h[offset + 1] & 0xFF) << 16)
        | ((h[offset + 2] & 0xFF) << 8)
        | (h[offset + 3] & 0xFF)
    )

    return str(code % (10 ** digits)).zfill(digits)


def verify_totp(secret: str, user_code: str, window: int = 1):
    key = decode_totp_secret(secret)
    for offset in range(-window, window + 1):
        current_time = int(time.time())
        counter = (current_time // 30) + offset

        msg = struct.pack(">Q", counter)
        h = hmac.new(key, msg, hashlib.sha1).digest()

        o = h[-1] & 0x0F
        code = (
            ((h[o] & 0x7F) << 24)
            | ((h[o + 1] & 0xFF) << 16)
            | ((h[o + 2] & 0xFF) << 8)
            | (h[o + 3] & 0xFF)
        )

        if str(code % 1000000).zfill(6) == user_code:
            return True

    return False