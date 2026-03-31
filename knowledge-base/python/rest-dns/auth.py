from token_lib import paseto, keys
from fastapi import HTTPException
import config
import time
from dns_validation import DNSAuthException

def verify_token(token: str):

    payload, error = paseto.decode_paseto_v4_local(token, config.PASETO_SECRET)

    if error != "Success":
        raise DNSAuthException()

    if "exp" not in payload:
        raise DNSAuthException()

    if time.time() > payload["exp"]:
        raise DNSAuthException()

    return payload


def check_permission(payload, domain, action):
    zones = payload.get("zones", {})

    if domain not in zones:
        raise HTTPException(status_code=403, detail="Forbidden: domain")

    if action not in zones[domain]:
        raise HTTPException(status_code=403, detail="Forbidden: action")