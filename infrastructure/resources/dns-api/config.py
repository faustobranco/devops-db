import os

PASETO_SECRET = os.getenv("PASETO_SECRET")

TSIG_KEY_NAME = os.getenv("TSIG_KEY_NAME")
TSIG_SECRET = os.getenv("TSIG_SECRET")

DNS_SERVER = os.getenv("DNS_SERVER")

TTL = int(os.getenv("TTL"))

DNS_API_VERSION = os.getenv("DNS_API_VERSION")