import struct
import time
import os
import json
import base64   
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from .keys import base64url_encode, base64url_decode

def generate_branca_token(payload, key_32_bytes):
    version = b'\xBA' 
    
    timestamp = struct.pack(">I", int(time.time())) 
    nonce = os.urandom(12) 
    plain_text = json.dumps(payload).encode('utf-8')
    aead = ChaCha20Poly1305(key_32_bytes)
    associated_data = version + timestamp + nonce
    cipher_text = aead.encrypt(nonce, plain_text, associated_data)
    binary_token = version + timestamp + nonce + cipher_text
    
    return base64url_encode(binary_token)


def decode_branca_token(token, key_32_bytes, ttl_seconds=3600):
    try:
        # 1. Decode Base64URL to Binary
        binary_token = base64url_decode(token + "==")
        
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
    
__all__ = [ 
    "generate_branca_token",
    "decode_branca_token"
    ]
    