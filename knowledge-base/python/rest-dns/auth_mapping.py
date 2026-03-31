def extract_zones(groups):
    zones = {}

    for g in groups:
        if "devops-db-internal-read" in g:
            zones.setdefault("devops-db.internal", []).append("read")

        if "devops-db-internal-admin" in g:
            zones.setdefault("devops-db.internal", []).append("write")

        if "devops-db-local-read" in g:
            zones.setdefault("devops-db.local", []).append("read")

        if "devops-db-local-admin" in g:
            zones.setdefault("devops-db.local", []).append("write")

    return zones