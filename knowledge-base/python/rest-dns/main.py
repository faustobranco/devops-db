from fastapi import FastAPI, Request, Header, Depends, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal

import time
import auth
import auth_ldap
import auth_mapping
import auth_session
import totp
from token_lib import paseto
import dns_service
import dns_validation
from dns_validation import APIException, DNSValidationException, DNSAuthException
import kea_service
import config

security = HTTPBearer()

app = FastAPI(
    title="Rest DNS API",
    description="API for managing DNS records (A, CNAME) with dynamic updates via TSIG",
    version="1.0.0"
)


class DNSRecordRequest(BaseModel):
    name: str = Field(..., example="test")
    type: Literal["A", "CNAME"] = Field(..., example="A")
    value: str = Field(..., example="172.21.5.10")
    ttl: Optional[int] = Field(default=300, example=300)


class DHCPReservationRequest(BaseModel):
    mac_address: str = Field(..., example="aa:bb:cc:dd:ee:ff", description="MAC address in colon-separated format")
    ip_address: str = Field(..., example="192.168.1.100", description="IPv4 address to reserve")
    hostname: str = Field(..., example="myhost", description="Hostname for the reservation")
    subnet_id: Optional[int] = Field(default=1, example=1, description="Kea subnet ID")


class DNSLoginException(APIException):
    def __init__(self):
        super().__init__(
            401,
            "Invalid username or password",
            data=None
        )

class DNSTOTPException(APIException):
    def __init__(self):
        super().__init__(401, "Invalid authentication code", None)

        
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.code,
        content={
            "code": exc.code,
            "status": "error",
            "message": exc.message,
            "data": exc.data
        }
    )


@app.exception_handler(FastAPIHTTPException)
async def http_exception_handler(request: Request, exc: FastAPIHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "status": "error",
            "message": str(exc.detail),
            "data": None
        }
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "status": "error",
            "message": str(exc),
            "data": None
        }
    )


def render_page(title: str, content: str):
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial;
                background: #f4f6f8;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .box {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                width: 400px;
            }}
            h2 {{
                margin-bottom: 20px;
            }}
            .error {{
                color: #d93025;
                background: #fdecea;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 15px;
            }}
            .success {{
                color: #1e7e34;
                background: #e6f4ea;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 15px;
            }}
            input {{
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }}
            button {{
                width: 100%;
                padding: 10px;
                background: #2d7ff9;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            textarea {{
                width: 100%;
                height: 120px;
                margin-top: 10px;
            }}
            a {{
                display: block;
                margin-top: 15px;
                text-align: center;
                text-decoration: none;
                color: #2d7ff9;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h2>{title}</h2>
            {content}
        </div>
    </body>
    </html>
    """


def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    return auth.verify_token(token)

@app.post(
    "/{domain}/insert",
    summary="Create DNS record",
    description="""
Create a DNS record.

Supported types:
- A → requires 'value' as IP
- CNAME → requires 'value' as FQDN

Rules:
- CNAME cannot coexist with other record types
- TTL must be between 60 and 86400
""",
    responses={
        200: {"description": "Record created successfully"},
        400: {"description": "Validation error"},
        401: {"description": "Unauthorized"},
        409: {"description": "Conflict (CNAME rules)"},
        500: {"description": "DNS error"}
    }
)
async def insert_record(
    domain: str,
    body: DNSRecordRequest,
    payload=Depends(get_token_payload)
):
    auth.check_permission(payload, domain, "write")

    name = body.name
    record_type = body.type.upper()
    value = body.value
    ttl = body.ttl or config.TTL

    # validações base
    dns_validation.validate_name(name)
    dns_validation.validate_ttl(ttl)

    if record_type not in ["A", "CNAME"]:
        raise DNSValidationException(
            "Unsupported record type",
            {"type": record_type}
        )

    records = dns_service.list_records(domain)

    # regra CNAME
    for r in records:
        if r["name"] == name:
            if r["type"] == "CNAME" or record_type == "CNAME":
                raise APIException(
                    409,
                    f"{name} cannot mix CNAME with other records",
                    {"name": name}
                )

    # criação
    if record_type == "CNAME":
        target = dns_validation.normalize_target(value, domain)
        return dns_service.insert_cname(domain, name, target)

    if record_type == "A":
        dns_validation.validate_ip(value)
        return dns_service.insert_a(domain, name, value, ttl)

@app.delete(
    "/{domain}/delete",
    summary="Delete DNS record",
    description="Delete all records for a given name",
    responses={
        200: {"description": "Record deleted"},
        401: {"description": "Unauthorized"},
        500: {"description": "DNS error"}
    }
)
async def delete_record(
    domain: str,
    name: str,
    payload=Depends(get_token_payload)
):
    auth.check_permission(payload, domain, "write")

    obj_return = dns_service.delete_record(domain, name)

    return obj_return


@app.get(
    "/{domain}/list",
    summary="List DNS records",
    description="List DNS records with optional filtering by name or target",
    responses={
        200: {"description": "List of records"},
        401: {"description": "Unauthorized"}
    }
)
async def list_records_endpoint(
    domain: str,
    payload=Depends(get_token_payload),
    name: str = None,
    target: str = None
):
    auth.check_permission(payload, domain, "read")

    records = dns_service.list_records(domain)
    records = dns_service.filter_records(records, name, target)

    return records

@app.get(
    "/version",
    summary="API version",
    description="Returns current API version"
)
def version():
    return {"version": config.DNS_API_VERSION}

@app.get("/health", summary="Health check")
def healthcheck():
    return {"status": "ok"}

@app.get(
    "/domains",
    summary="List accessible domains",
    description="Returns the list of domains the authenticated user has access to, with their permissions"
)
def list_domains(payload=Depends(get_token_payload)):
    zones = payload.get("zones", {})
    return {
        "domains": [
            {"domain": domain, "permissions": perms}
            for domain, perms in zones.items()
        ]
    }

@app.get(
    "/dhcp/reservations",
    summary="List DHCP reservations",
    description="Returns all static DHCP reservations from the Kea database. Requires `dhcp` domain with `read` permission.",
    responses={
        200: {"description": "List of static reservations"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        503: {"description": "Database unavailable"}
    }
)
def dhcp_list_reservations(payload=Depends(get_token_payload)):
    auth.check_permission(payload, "dhcp", "read")
    try:
        return kea_service.list_reservations()
    except ConnectionError as e:
        raise FastAPIHTTPException(status_code=503, detail=str(e))


@app.get(
    "/dhcp/leases",
    summary="List DHCP leases",
    description="Returns all active DHCP leases from the Kea database. Requires `dhcp` domain with `read` permission.",
    responses={
        200: {"description": "List of active leases"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        503: {"description": "Database unavailable"}
    }
)
def dhcp_list_leases(payload=Depends(get_token_payload)):
    auth.check_permission(payload, "dhcp", "read")
    try:
        return kea_service.list_leases()
    except ConnectionError as e:
        raise FastAPIHTTPException(status_code=503, detail=str(e))


@app.post(
    "/dhcp/reservations",
    summary="Add DHCP reservation",
    description="Creates a static DHCP reservation in the Kea database. Requires `dhcp` domain with `write` permission.",
    responses={
        200: {"description": "Reservation created successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        503: {"description": "Database unavailable"}
    }
)
def dhcp_add_reservation(body: DHCPReservationRequest, payload=Depends(get_token_payload)):
    auth.check_permission(payload, "dhcp", "write")
    try:
        kea_service.add_reservation(body.mac_address, body.ip_address, body.hostname, body.subnet_id)
        return {"status": "ok", "message": f"Reservation added for {body.hostname}"}
    except ConnectionError as e:
        raise FastAPIHTTPException(status_code=503, detail=str(e))


@app.delete(
    "/dhcp/reservations",
    summary="Delete DHCP reservation",
    description="""
Deletes a static DHCP reservation from the Kea database.

Provide either `mac` or `hostname` to identify the reservation:
- `mac` — MAC address in colon-separated format (e.g. `aa:bb:cc:dd:ee:ff`)
- `hostname` — exact hostname of the reservation

Requires `dhcp` domain with `write` permission.
""",
    responses={
        200: {"description": "Reservation deleted"},
        400: {"description": "Neither mac nor hostname provided"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        503: {"description": "Database unavailable"}
    }
)
def dhcp_delete_reservation(
    payload=Depends(get_token_payload),
    mac: Optional[str] = None,
    hostname: Optional[str] = None
):
    auth.check_permission(payload, "dhcp", "write")
    if not mac and not hostname:
        raise FastAPIHTTPException(status_code=400, detail="Provide 'mac' or 'hostname' query parameter")
    try:
        identifier = mac if mac else hostname
        deleted = kea_service.delete_reservation(identifier, use_mac=bool(mac))
        return {"status": "ok", "deleted": deleted, "identifier": identifier}
    except ConnectionError as e:
        raise FastAPIHTTPException(status_code=503, detail=str(e))


@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_form():
    return """
    <html>
    <head>
        <style>
            body {
                font-family: Arial;
                background: #f4f6f8;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .box {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                width: 300px;
            }
            h2 {
                margin-bottom: 20px;
            }
            input {
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                width: 100%;
                padding: 10px;
                background: #2d7ff9;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .error {
                color: red;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Login</h2>
            <div id="error" class="error"></div>

            <form id="loginForm">
                <input name="username" placeholder="Username" required>
                <input name="password" type="password" placeholder="Password" required>
                <button type="submit">Next</button>
            </form>
        </div>

        <script>
            const form = document.getElementById("loginForm");

            form.onsubmit = async (e) => {
                e.preventDefault();

                const data = new FormData(form);

                const res = await fetch("/login", {
                    method: "POST",
                    body: data
                });

                if (!res.ok) {
                    const err = await res.json();
                    document.getElementById("error").innerText = err.message;
                    return;
                }

                const html = await res.text();
                document.open();
                document.write(html);
                document.close();
            };
        </script>
    </body>
    </html>
    """

@app.post("/login", include_in_schema=False)
def login_step1(
    username: str = Form(...),
    password: str = Form(...)
):
    user = auth_ldap.get_user(username)

    if not user:
        raise DNSLoginException()

    if not auth_ldap.verify_password(user["dn"], password):
        raise DNSLoginException()

    # cria sessão temporária
    session_id = auth_session.create_session(username, user)

    return HTMLResponse(render_page(
        "2FA Verification",
        f"""
        <form method="post" action="/login/totp">
            <input type="hidden" name="session_id" value="{session_id}">
            <input name="totp" placeholder="Enter code" required autofocus>
            <button type="submit">Verify</button>
        </form>
        """
    ))


@app.post("/login/totp", include_in_schema=False)
def login_step2(
    session_id: str = Form(...),
    totp_code: str = Form(..., alias="totp")
):
    session = auth_session.get_session(session_id)

    if not session:
        return HTMLResponse(render_page(
            "2FA Verification",
            """
            <div class="error">Session expired</div>
            <a href="/login">Back to login</a>
            """
        ), status_code=401)

    user = session["user"]

    if not user["totp"]:
        return HTMLResponse(render_page(
            "2FA Verification",
            """
            <div class="error">2FA not configured</div>
            <a href="/login">Back to login</a>
            """
        ), status_code=401)

    if not totp.verify_totp(user["totp"], totp_code):
        return HTMLResponse(render_page(
            "2FA Verification",
            f"""
            <div class="error">Invalid authentication code</div>

            <form method="post" action="/login/totp">
                <input type="hidden" name="session_id" value="{session_id}">
                <input name="totp" placeholder="Enter code" required autofocus>
                <button type="submit">Verify</button>
            </form>
            """
        ), status_code=401)

    zones = auth_mapping.extract_zones(user["groups"])

    payload = {
        "sub": session["username"],
        "zones": zones,
        "type": "user",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }

    token = paseto.generate_paseto_v4_local(payload, config.PASETO_SECRET)

    auth_session.delete_session(session_id)

    return HTMLResponse(render_page(
        "Authenticated",
        f"""
        <div class="success">Authentication successful</div>

        <p>Your token:</p>
        <textarea readonly>{token}</textarea>

        <a href="/login">Back to login</a>
        """
    ))
