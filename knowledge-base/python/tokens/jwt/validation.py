import hmac
import hashlib
import base64
import json
import time

def verify_manual_jwt(token, secret_key):
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
        actual_signature = base64.urlsafe_b64decode(crypto_segment + "==")
        if not hmac.compare_digest(expected_signature, actual_signature):
            return None, "Invalid signature"
            
        # 4. Decode Payload
        payload_json = base64.urlsafe_b64decode(payload_segment + "==").decode('utf-8')
        return json.loads(payload_json), "Success"
        
    except Exception as e:
        return None, f"Decryption failed: {str(e)}"

def main():

    # Use the same key from the generation
    secure_key_bytes = "6242a422c9964c48ea61bc11ba412ad7a7e96cb1a548af3dc25ca9cdb3a2f0a2"
    jwt_token = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJncm91cHMiOiAiaW5mcmFzdHJ1Y3R1cmUuZG5zIiwgInVzZXJfaWQiOiAxMjMsICJ6b25lcyI6IFsiZXhhbXBsZS5jb20iXSwgInBlcm1pc3Npb25zIjogWyJyZWFkIiwgIndyaXRlIl0sICJpYXQiOiAxNzc0ODU4OTA3LCAiZXhwIjogMTc3NDg2MjUwN30.X4FtXt-4MAVIjJ96gLFqoJmzvGyuCzqBRyw5CBEeb6k"

    # 2. Decode
    decoded_data, status = verify_manual_jwt(jwt_token, secure_key_bytes)
    print(f"Status: {status}")
    print(f"Decoded Data: {decoded_data}")


if __name__ == "__main__":
    main()    