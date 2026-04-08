import psycopg2
import sys
import argparse
import socket
import struct
import json
from datetime import datetime
from psycopg2.extras import RealDictCursor

# Database configuration
DB_CONFIG = {
    "host": "postgresql.devops-db.internal",
    "database": "kea_db",
    "user": "kea",
    "password": "XenCusx6jZMGBQsYmPt7l4lbnIfk6nkQ",
    "port": 5432
}

def ip_to_int(ip_address):
    return struct.unpack("!I", socket.inet_aton(ip_address))[0]

def int_to_ip(ip_int):
    return socket.inet_ntoa(struct.pack("!I", ip_int))

def format_mac(byte_data):
    if isinstance(byte_data, memoryview):
        byte_data = byte_data.tobytes()
    hex_mac = byte_data.hex()
    return ":".join(hex_mac[i:i+2] for i in range(0, len(hex_mac), 2))

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code (like datetime)."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as error:
        print(f"Error connecting to PostgreSQL: {error}", file=sys.stderr)
        sys.exit(1)

def list_reservations():
    """Returns static reservations from 'hosts' table as JSON."""
    query = """
        SELECT dhcp_identifier as mac, ipv4_address as ip_int, hostname, dhcp4_subnet_id as subnet_id 
        FROM hosts WHERE dhcp4_subnet_id IS NOT NULL ORDER BY ipv4_address;
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            reservations = [{
                "hostname": r['hostname'],
                "ip_address": int_to_ip(int(r['ip_int'])) if r['ip_int'] else None,
                "mac_address": format_mac(r['mac']),
                "subnet_id": r['subnet_id']
            } for r in rows]
            print(json.dumps(reservations, indent=4))
    finally:
        conn.close()

def list_leases():
    """Returns active leases from 'lease4' table as JSON."""
    query = """
        SELECT address as ip_int, hwaddr as mac, valid_lifetime, expire, 
               subnet_id, fqdn_fwd, fqdn_rev, hostname, state 
        FROM lease4 ORDER BY address;
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            leases = [{
                "hostname": r['hostname'],
                "ip_address": int_to_ip(int(r['ip_int'])),
                "mac_address": format_mac(r['mac']),
                "valid_lifetime": r['valid_lifetime'],
                "expire": r['expire'],
                "subnet_id": r['subnet_id'],
                "fqdn_fwd": r['fqdn_fwd'],
                "fqdn_rev": r['fqdn_rev'],
                "state": r['state']
            } for r in rows]
            print(json.dumps(leases, indent=4, default=json_serial))
    finally:
        conn.close()

def add_reservation(mac_address, ip_address, hostname, subnet_id=1):
    clean_mac = mac_address.replace(":", "").lower()
    ip_as_int = ip_to_int(ip_address)
    query = """
        INSERT INTO hosts (dhcp_identifier, dhcp_identifier_type, ipv4_address, hostname, dhcp4_subnet_id) 
        VALUES (decode(%s, 'hex'), 0, %s, %s, %s);
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (clean_mac, ip_as_int, hostname, subnet_id))
            conn.commit()
            print(f"Successfully added reservation: {hostname}", file=sys.stderr)
    finally:
        conn.close()

def delete_reservation(identifier, use_mac=True):
    val = identifier.replace(":", "").lower() if use_mac else identifier
    column = "dhcp_identifier" if use_mac else "hostname"
    query = f"DELETE FROM hosts WHERE {column} = {'decode(%s, \'hex\')' if use_mac else '%s'};"
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (val,))
            conn.commit()
            print(f"Deleted reservation: {identifier}", file=sys.stderr)
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kea DHCP PostgreSQL Manager")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list-reservations")
    subparsers.add_parser("list-leases")

    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("--mac", required=True)
    parser_add.add_argument("--ip", required=True)
    parser_add.add_argument("--name", required=True)
    parser_add.add_argument("--subnet", type=int, default=1)

    parser_del = subparsers.add_parser("del")
    parser_del.add_argument("--mac")
    parser_del.add_argument("--name")

    args = parser.parse_args()

    if args.command == "list-reservations":
        list_reservations()
    elif args.command == "list-leases":
        list_leases()
    elif args.command == "add":
        add_reservation(args.mac, args.ip, args.name, args.subnet)
    elif args.command == "del":
        delete_reservation(args.mac or args.name, use_mac=bool(args.mac))
    else:
        parser.print_help()