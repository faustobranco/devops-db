import os
import time
import json         
import base64
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from .keys import convert_hex_to_key, base64url_encode, base64url_decode

def generate_paseto_v4_local(payload, key_32_bytes):
    # Header for v4.local
    header = b"v4.local."
    
    # Payload must be bytes (usually JSON)
    plain_text = json.dumps(payload).encode('utf-8')
    
    # Nonce (Adjusted to 12 bytes to match the available AEAD class)
    nonce = os.urandom(12)
    
    # Initialize Cipher using the compatible ChaCha20Poly1305
    aead = ChaCha20Poly1305(key_32_bytes)
    
    # The header acts as 'Additional Authenticated Data' (AAD)
    # This ensures the header cannot be tampered with
    cipher_text = aead.encrypt(nonce, plain_text, header)
    
    # Format: header + base64(nonce + cipher_text)
    token_body = base64url_encode(nonce + cipher_text)
    return f"v4.local.{token_body}"

def decode_paseto_v4_local(token, key_32_bytes):
    try:
        header = b"v4.local."
        if not token.startswith("v4.local."):
            return None, "Invalid header"
            
        # Remove header and decode body
        encoded_body = token.replace("v4.local.", "")
        # O Base64URL do Python às vezes precisa de padding manual se não for o standard original
        body = base64url_decode(encoded_body + "===")
        
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
    
__all__ = [ 
        "generate_paseto_v4_local",
        "decode_paseto_v4_local"
        ]
