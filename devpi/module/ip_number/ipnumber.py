"""
Module to convert IPs into Numbers and Numbers into IPs.
"""

def fn_IP_Int(ip):
    h = list(map(int, ip.split(".")))
    return (h[0] << 24) + (h[1] << 16) + (h[2] << 8) + (h[3] << 0)

def fn_Int_IP(ip):
    return ".".join(map(str, [((ip >> 24) & 0xff), ((ip >> 16) & 0xff), ((ip >> 8) & 0xff), ((ip >> 0) & 0xff)]))
