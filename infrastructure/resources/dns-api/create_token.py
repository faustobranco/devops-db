from token_lib import paseto, branca, jwt, keys
import time
import uuid
import config

str_key = config.PASETO_SECRET

user_data = {
    "sub": "fbranco",  # Subject (user identifier)
    "groups": "infrastructure.dns",
    "user_id": 123,
    "type": "api_token",
    "zones": {
        "devops-db.internal": ["read", "write"],
        "devops-db.local": ["read"]
    },
    "jti": str(uuid.uuid4()),
    "iat": int(time.time()),
    "exp": int(time.time()) + 3600
}

str_Paseto = paseto.generate_paseto_v4_local(user_data, str_key)
print(f"Paseto Token: {str_Paseto}")    
print()

str_Paseto = "v4.local.7ABWoIBLFSPnErJC0Q3x6wW2MeRyyKV0G5Hhk1cfxmkJDrjxAeEnSjAIEZA5J6VUNyalcVBx8k3XkvPlIBkyqXPw7hooXUxsiYm7jn1rLHr1MwpLC8IL1bQWJqiGHcWF_kOBGwuhQFiv-HB2-__BBux5H_lYg23Apsz0gHWBMm2bkKBIYjD5g8-eeqtFttcHn3kQyvg09uJPQTwV9YkXJTwYVjAzeaXKO7setPjo5K-7vPDnU4KVABHEtlYwgw"

str_Decoded_Paseto, str_Paseto_Error = paseto.decode_paseto_v4_local(str_Paseto, str_key)
print(f"Decrypted Paseto: {str_Decoded_Paseto}, Error: {str_Paseto_Error}")   
print()

