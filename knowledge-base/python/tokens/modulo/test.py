from token_lib import paseto, branca, jwt, keys
import time

str_key = keys.generate_secure_32_byte_key()

user_data = {
    "groups": "infrastructure.dns",
    "user_id": 123, 
    "zones": ["example.com"],
    "permissions": ["read", "write"],
    "iat": int(time.time()),
    "exp": int(time.time()) + 3600  # Expires in 1 hour.
}

str_Paseto = paseto.generate_paseto_v4_local(user_data, str_key)
print(f"Paseto Token: {str_Paseto}")    
print()
str_Branca = branca.generate_branca_token(user_data, str_key)
print(f"Branca Token: {str_Branca}")    
print()
str_JWT = jwt.generate_manual_jwt(user_data, keys.convert_key_to_hex(str_key))
print(f"JWT Token: {str_JWT}")  
print()

print()
str_Decoded_Paseto, str_Paseto_Error = paseto.decode_paseto_v4_local(str_Paseto, str_key)
print(f"Decrypted Paseto: {str_Decoded_Paseto}, Error: {str_Paseto_Error}")   
print()
str_Decoded_Branca, str_Branca_Error = branca.decode_branca_token(str_Branca, str_key)
print(f"Decoded Branca: {str_Decoded_Branca}, Error: {str_Branca_Error}")       
print()
str_Decoded_JWT, str_JWT_Error = jwt.decode_manual_jwt(str_JWT, keys.convert_key_to_hex(str_key))
print(f"Verified JWT: {str_Decoded_JWT}, Error: {str_JWT_Error}")  




