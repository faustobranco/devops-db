import os

PASETO_SECRET = os.getenv("PASETO_SECRET")

TSIG_KEY_NAME = os.getenv("TSIG_KEY_NAME")
TSIG_SECRET = os.getenv("TSIG_SECRET")

DNS_SERVER = os.getenv("DNS_SERVER")

TTL = int(os.getenv("TTL"))

DNS_API_VERSION = os.getenv("DNS_API_VERSION")

# Kea DHCP database
KEA_DB_HOST = os.getenv("KEA_DB_HOST", "localhost")
KEA_DB_NAME = os.getenv("KEA_DB_NAME", "kea_db")
KEA_DB_USER = os.getenv("KEA_DB_USER", "kea")
KEA_DB_PASSWORD = os.getenv("KEA_DB_PASSWORD", "")
KEA_DB_PORT = int(os.getenv("KEA_DB_PORT", "5432"))