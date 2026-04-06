import re
import ipaddress
from fastapi import HTTPException


class APIException(HTTPException):
    def __init__(self, code: int, message: str, data=None):
        super().__init__(status_code=code)
        self.code = code
        self.message = message
        self.data = data

class DNSConflictException(APIException):
    def __init__(self, name: str):
        super().__init__(
            409,
            f"{name} already has a CNAME",
            {"name": name}
        )

class DNSValidationException(APIException):
    def __init__(self, message: str, data=None):
        super().__init__(400, message, data)


class DNSAuthException(APIException):
    def __init__(self, data=None):
        super().__init__(401, "Invalid or missing token", data)


class DNSLoginException(APIException):
    def __init__(self):
        super().__init__(401, "Invalid username or password", None)


class DNSTOTPException(APIException):
    def __init__(self):
        super().__init__(401, "Invalid authentication code", None)


def validate_ip(ip: str):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise DNSValidationException("Invalid IP address", {"ip": ip})
    
def validate_name(name: str):
    if not name:
        raise DNSValidationException("Invalid name: empty", {"name": name})

    if not re.match(r"^[a-zA-Z0-9.-]+$", name):
        raise DNSValidationException("Invalid name: contains invalid characters", {"name": name})

    if ".." in name:
        raise DNSValidationException("Invalid name: double dots not allowed", {"name": name})

def normalize_target(target: str, domain: str):
    target = target.strip()

    if not target:
        raise DNSValidationException("Invalid target: empty", {"target": target})

    if ".." in target:
        raise DNSValidationException("Invalid target: empty DNS label", {"target": target})

    if target.startswith(".") or target.endswith(".."):
        raise DNSValidationException("Invalid target format", {"target": target})

    if target.endswith("."):
        return target

    if target.endswith(domain):
        return f"{target}."

    return f"{target}.{domain}."


def validate_ttl(ttl: int):
    if ttl < 60 or ttl > 86400:
        raise DNSValidationException("Invalid TTL (must be between 60 and 86400)", {"ttl": ttl})


def validate_cname_conflict(records, name: str):
    """
    records = output of list_records()
    """

    for r in records:
        if r["name"] == name:
            # If any record exists that is NOT CNAME → block
            if r["type"] != "CNAME":
                raise APIException(
                    code=409,
                    message=f"{name} already has {r['type']} record",
                    data={"name": name, "type": r["type"]}
                )

            # If already CNAME → block duplicate
            if r["type"] == "CNAME":
                raise DNSConflictException(name)