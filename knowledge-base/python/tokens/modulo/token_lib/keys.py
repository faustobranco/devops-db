import os
import base64

def generate_secure_32_byte_key():
    """
    Generates a cryptographically strong 32-byte (256-bit) key.
    This is the mandatory length for PASETO v4 and Branca.
    """
    return os.urandom(32)

def convert_key_to_hex(key_bytes):
    """
    Encodes binary bytes into a 64-character hexadecimal string.
    Ideal for .env files and human-readable configurations.
    """
    return key_bytes.hex()

def convert_hex_to_key(hex_string):
    """
    Decodes a 64-character hexadecimal string back into 32 bytes.
    Validates length to ensure cryptographic integrity before use.
    """
    try:
        key_bytes = bytes.fromhex(hex_string)
        if len(key_bytes) != 32:
            raise ValueError("Invalid key length: Must be exactly 32 bytes.")
        return key_bytes
    except ValueError as e:
        print(f"Key Conversion Error: {e}")
        return None
    
def base64url_encode(data):
    """Encodes data to Base64URL format without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def base64url_decode(data: str) -> bytes:
    data = data.strip()
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


__all__ = [
    "base64url_encode",
    "base64url_decode",
    "convert_key_to_hex",
    "convert_hex_to_key",
    "generate_secure_32_byte_key"
]