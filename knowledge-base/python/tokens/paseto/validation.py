import os
import time
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


def decrypt_paseto_v4_local(token, key_32_bytes):
    try:
        header = b"v4.local."
        if not token.startswith("v4.local."):
            return None, "Invalid header"
            
        # Remove header and decode body
        encoded_body = token.replace("v4.local.", "")
        # O Base64URL do Python às vezes precisa de padding manual se não for o standard original
        body = base64.urlsafe_b64decode(encoded_body + "===")
        
        # AJUSTE EVOLUTIVO: Extrair 12 bytes de Nonce (conforme o gerador)
        nonce = body[:12]
        cipher_text = body[12:]
        
        # Usar a mesma classe do gerador
        aead = ChaCha20Poly1305(key_32_bytes)
        
        # Decrypt usando header como AAD
        decrypted_bytes = aead.decrypt(nonce, cipher_text, header)
        return json.loads(decrypted_bytes.decode('utf-8')), "Success"
        
    except Exception as e:
        # Debug opcional: print(f"Erro real: {e}")
        return None, "Decryption failed (Tampered or wrong key)"

def main():
    
    # Use the same key from the generation    
    secure_key_bytes = "6242a422c9964c48ea61bc11ba412ad7a7e96cb1a548af3dc25ca9cdb3a2f0a2"
    paseto_token = "v4.local.kobZTk0C8p0UuVAR_XeaJqpXdM8lbg2K6IYp6nd4lX2JyiO-2369cNwsMJoJuNBGxUGGD6_i4Qo5oWJv2-bl0r8lBBEPVr8bYeTV_w1Bc2pZtTr_yXhUslsPj1lbBAwIra6A3n12GoDIEfw5AKR5hEh_O0dz-6xgACVhaRYKlt5QT6TI8j0Bw-Ac7N5_6gsNsCwvWQdiaAfmy151JCILbIwf5NvnwfRj5tqjdZ0L"

    # 2. Decode
    data, status = decrypt_paseto_v4_local(paseto_token, convert_hex_to_key(secure_key_bytes))
    print(f"Status: {status}")
    print(f"Decoded Data: {data}")

if __name__ == "__main__":
    main()    