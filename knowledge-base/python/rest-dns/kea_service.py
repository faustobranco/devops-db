import socket
import struct
from datetime import datetime
from psycopg2.extras import RealDictCursor
import psycopg2
import config


def _get_connection():
    try:
        return psycopg2.connect(
            host=config.KEA_DB_HOST,
            database=config.KEA_DB_NAME,
            user=config.KEA_DB_USER,
            password=config.KEA_DB_PASSWORD,
            port=config.KEA_DB_PORT,
        )
    except Exception as error:
        raise ConnectionError(f"Error connecting to Kea DB: {error}")


def _ip_to_int(ip_address):
    return struct.unpack("!I", socket.inet_aton(ip_address))[0]


def _int_to_ip(ip_int):
    return socket.inet_ntoa(struct.pack("!I", ip_int))


def _format_mac(byte_data):
    if isinstance(byte_data, memoryview):
        byte_data = byte_data.tobytes()
    hex_mac = byte_data.hex()
    return ":".join(hex_mac[i:i+2] for i in range(0, len(hex_mac), 2))


def _json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def list_reservations():
    """Returns static DHCP reservations from the 'hosts' table."""
    query = """
        SELECT dhcp_identifier as mac, ipv4_address as ip_int, hostname, dhcp4_subnet_id as subnet_id
        FROM hosts WHERE dhcp4_subnet_id IS NOT NULL ORDER BY ipv4_address;
    """
    conn = _get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [{
                "hostname": r["hostname"],
                "ip_address": _int_to_ip(int(r["ip_int"])) if r["ip_int"] else None,
                "mac_address": _format_mac(r["mac"]),
                "subnet_id": r["subnet_id"]
            } for r in rows]
    finally:
        conn.close()


def list_leases():
    """Returns active DHCP leases from the 'lease4' table."""
    query = """
        SELECT address as ip_int, hwaddr as mac, valid_lifetime, expire,
               subnet_id, fqdn_fwd, fqdn_rev, hostname, state
        FROM lease4 ORDER BY address;
    """
    conn = _get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [{
                "hostname": r["hostname"],
                "ip_address": _int_to_ip(int(r["ip_int"])),
                "mac_address": _format_mac(r["mac"]),
                "valid_lifetime": r["valid_lifetime"],
                "expire": r["expire"].isoformat() if isinstance(r["expire"], datetime) else r["expire"],
                "subnet_id": r["subnet_id"],
                "fqdn_fwd": r["fqdn_fwd"],
                "fqdn_rev": r["fqdn_rev"],
                "state": r["state"]
            } for r in rows]
    finally:
        conn.close()


def add_reservation(mac_address: str, ip_address: str, hostname: str, subnet_id: int = 1):
    """Inserts a static DHCP reservation into the 'hosts' table."""
    clean_mac = mac_address.replace(":", "").lower()
    ip_as_int = _ip_to_int(ip_address)
    query = """
        INSERT INTO hosts (dhcp_identifier, dhcp_identifier_type, ipv4_address, hostname, dhcp4_subnet_id)
        VALUES (decode(%s, 'hex'), 0, %s, %s, %s);
    """
    conn = _get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (clean_mac, ip_as_int, hostname, subnet_id))
            conn.commit()
    finally:
        conn.close()


def delete_reservation(identifier: str, use_mac: bool = True):
    """Deletes a DHCP reservation by MAC address or hostname."""
    val = identifier.replace(":", "").lower() if use_mac else identifier
    if use_mac:
        query = "DELETE FROM hosts WHERE dhcp_identifier = decode(%s, 'hex');"
    else:
        query = "DELETE FROM hosts WHERE hostname = %s;"
    conn = _get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (val,))
            deleted = cursor.rowcount
            conn.commit()
            return deleted
    finally:
        conn.close()
