from ldap3 import Server, Connection, ALL

LDAP_SERVER = "ldap://ldap.devops-db.info:389"
BIND_DN = "cn=readonly-bind-dn,ou=ServiceGroups,dc=ldap,dc=devops-db,dc=info"
BIND_PASSWORD = "1234qwer"
BASE_DN = "dc=ldap,dc=devops-db,dc=info"


def get_user(username: str):
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=BIND_DN, password=BIND_PASSWORD)

    if not conn.bind():
        return None

    conn.search(
        BASE_DN,
        f"(uid={username})",
        attributes=["memberOf", "totpSecret"]
    )

    if not conn.entries:
        return None

    entry = conn.entries[0]

    return {
        "dn": entry.entry_dn,
        "groups": entry.memberOf.values if "memberOf" in entry else [],
        "totp": entry.totpSecret.value if "totpSecret" in entry else None
    }


def verify_password(user_dn: str, password: str):
    server = Server(LDAP_SERVER)
    conn = Connection(server, user=user_dn, password=password)
    return conn.bind()