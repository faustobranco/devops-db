import struct
import time
import os
import json
import base64   
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

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


def decode_branca_token(token, key_32_bytes, ttl_seconds=3600):
    try:
        # 1. Decode Base64URL to Binary
        binary_token = base64.urlsafe_b64decode(token + "==")
        
        # 2. Extract Parts (Following the exact positions used in generate)
        # Version (1B) | Timestamp (4B) | Nonce (12B) | Ciphertext (nB)
        version = binary_token[0:1]
        timestamp_bytes = binary_token[1:5]
        nonce = binary_token[5:17] 
        cipher_text = binary_token[17:]
        
        # 3. Validation: Version check
        if version != b'\xBA':
            return None, "Error: Unsupported version"
            
        # 4. Validation: Expiration (TTL)
        token_time = struct.unpack(">I", timestamp_bytes)[0]
        if int(time.time()) - token_time > ttl_seconds:
            return None, "Error: Token has expired"
            
        # 5. Initialize AEAD
        aead = ChaCha20Poly1305(key_32_bytes)
        
        # 6. Reconstruct AAD (Must be exactly as it was during encryption)
        associated_data = version + timestamp_bytes + nonce
        
        # 7. Decrypt and Verify
        # If the key is wrong or the token was tampered with, this will fail
        decrypted_payload = aead.decrypt(nonce, cipher_text, associated_data)
        
        return json.loads(decrypted_payload.decode('utf-8')), "Success"
        
    except Exception as e:
        return None, f"Decryption failed: {str(e)}"

def main():

    # Use the same key from the generation
    secure_key_bytes = "6242a422c9964c48ea61bc11ba412ad7a7e96cb1a548af3dc25ca9cdb3a2f0a2"
    token = "umnKM7Cwf3KvbI5zPXAbo8Dt-1hBWl414wO8Skz8Z3nQoDeaaV88Gh9aIohZY2w7Eo9eUqtr2ULPOJ7dEeQ9k5Ybmg4-2J5gYe_xV2QUOFBlfelYGRJV8W9fCtxQkEfsFj4dEaULujo5puMdoSkGQnR8bpTPSZnx2-xuLOO0XhKzbtq-1MFSmTfAfIA3OCwgm6YZHIVkShIe4VZEGEfMyF4ydIoxHimTGD-eCZXoTQOzsn0="

    # 2. Decode
    decoded_data, status = decode_branca_token(token, convert_hex_to_key(secure_key_bytes))
    print(f"Status: {status}")
    print(f"Decoded Data: {decoded_data}")

if __name__ == "__main__":
    main()        