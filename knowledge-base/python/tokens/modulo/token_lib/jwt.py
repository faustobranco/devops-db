import hmac
import hashlib
import base64
import json
import time
from .keys import base64url_encode, base64url_decode


def generate_manual_jwt(payload, secret_key):
    # 1. Header (Standard for HS256)
    header = {"alg": "HS256", "typ": "JWT"}
    encoded_header = base64url_encode(json.dumps(header).encode('utf-8'))
    
    # 2. Payload
    encoded_payload = base64url_encode(json.dumps(payload).encode('utf-8'))
    
    # 3. Signature
    signing_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
    signature = hmac.new(
        secret_key.encode('utf-8'),
        signing_input,
        hashlib.sha256
    ).digest()
    encoded_signature = base64url_encode(signature)
    
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

def decode_manual_jwt(token, secret_key):
    try:
        header_segment, payload_segment, crypto_segment = token.split('.')
        
        # 1. Reconstruct signing input
        signing_input = f"{header_segment}.{payload_segment}".encode('utf-8')
        
        # 2. Recalculate Signature
        expected_signature = hmac.new(
            secret_key.encode('utf-8'),
            signing_input,
            hashlib.sha256
        ).digest()
        
        # 3. Secure comparison (prevents timing attacks)
        actual_signature = base64url_decode(crypto_segment + "==")
        if not hmac.compare_digest(expected_signature, actual_signature):
            return None, "Invalid signature"
            
        # 4. Decode Payload
        payload_json = base64url_decode(payload_segment + "==").decode('utf-8')
        return json.loads(payload_json), "Success"
        
    except Exception as e:
        return None, f"Decryption failed: {str(e)}"

__all__ = [ 
    "generate_manual_jwt",
    "decode_manual_jwt"
]