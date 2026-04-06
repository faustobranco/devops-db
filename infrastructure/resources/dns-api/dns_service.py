import dns.update
import dns.query
import dns.tsigkeyring
import keyring
import config
from dns import zone, rdatatype, tsig, tsigkeyring
from fastapi import HTTPException
from dns_validation import APIException 

def get_keyring():
    return dns.tsigkeyring.from_text({
        config.TSIG_KEY_NAME: config.TSIG_SECRET
    }), dns.tsig.HMAC_SHA256


def success_response(data=None, message="ok", code=200):
    return {
        "code": code,
        "status": "success",
        "message": message,
        "data": data
    }

def insert_a(domain: str, name: str, ip: str, ttl: int):
    keyring, algorithm = get_keyring()

    update = dns.update.Update(
        domain,
        keyring=keyring,
        keyname=config.TSIG_KEY_NAME,
        keyalgorithm=algorithm
    )

    fqdn = f"{name}.{domain}."

    update.add(fqdn, ttl, "A", ip)

    response = dns.query.tcp(update, config.DNS_SERVER, timeout=10)

    rcode = response.rcode()

    if rcode != dns.rcode.NOERROR:
        raise APIException(
            500,
            "DNS update failed",
            {"rcode": dns.rcode.to_text(rcode)}
        )

    return success_response(
        message="created",
        data={"name": name, "type": "A", "ip": ip}
    )

def insert_cname(domain: str, name: str, target: str):
    keyring, algorithm = get_keyring()
    update = dns.update.Update(
        domain,
        keyring=keyring,
        keyname=config.TSIG_KEY_NAME,
        keyalgorithm=algorithm
    )

    clean_domain = domain.strip('.')
    clean_name = name.strip('.')
    clean_target = target.strip('.')

    fqdn = f"{clean_name}.{clean_domain}."

    if clean_domain not in clean_target:
        target_fqdn = f"{clean_target}.{clean_domain}."
    else:
        target_fqdn = f"{clean_target}."

    update.add(fqdn, config.TTL, "CNAME", target_fqdn)

    response = dns.query.tcp(update, config.DNS_SERVER, timeout=10)
    
    rcode = response.rcode()

    if rcode != dns.rcode.NOERROR:
        raise HTTPException(
            status_code=500,
            detail=f"DNS update failed: {dns.rcode.to_text(rcode)}"
        )

    return success_response(
        message="created",
        data={"name": name, "target": target}
    )

def update_cname(domain: str, name: str, target: str):
    keyring, algorithm = get_keyring()

    update = dns.update.Update(
        domain,
        keyring=keyring,
        keyname=config.TSIG_KEY_NAME,
        keyalgorithm=algorithm
    )

    fqdn = f"{name}.{domain}."
    target_fqdn = f"{target}."

    update.replace(fqdn, config.TTL, "CNAME", target_fqdn)

    response = dns.query.tcp(update, config.DNS_SERVER)
    return response


def delete_record(domain: str, name: str):
    keyring, algorithm = get_keyring()

    update = dns.update.Update(
        domain,
        keyring=keyring,
        keyname=config.TSIG_KEY_NAME,
        keyalgorithm=algorithm
    )

    fqdn = f"{name}.{domain}."

    update.delete(fqdn)

    response = dns.query.tcp(update, config.DNS_SERVER)

    rcode = response.rcode()

    if rcode != dns.rcode.NOERROR:
        raise HTTPException(
            status_code=500,
            detail=f"DNS delete failed: {dns.rcode.to_text(rcode)}"
        )

    return success_response(
        message="deleted",
        data={"name": name}
    )


def list_records(domain: str):
    zone = dns.zone.from_xfr(
        dns.query.xfr(config.DNS_SERVER, domain)
    )

    records = []

    for name, node in zone.nodes.items():
        for rdataset in node.rdatasets:

            rtype = dns.rdatatype.to_text(rdataset.rdtype)

            if rtype == "CNAME":
                for rdata in rdataset:
                    records.append({
                        "name": str(name),
                        "type": "CNAME",
                        "value": str(rdata.target),
                        "ttl": rdataset.ttl
                    })
            elif rtype == "A":
                for rdata in rdataset:
                    records.append({
                        "name": str(name),
                        "type": "A",
                        "value": str(rdata.address),
                        "ttl": rdataset.ttl
                    })

    return records

def filter_records(records, name=None, target=None):
    result = records
    if name:
        result = [r for r in result if name.lower() in r["name"].lower()]
    if target:
        target = target.strip()
        result = [
            r for r in result
            if r.get("value") == target 
        ]
    return result
