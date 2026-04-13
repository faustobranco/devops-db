# ---- builder ----
FROM python:3.12-slim AS builder

WORKDIR /build

RUN python -m venv /venv

# ---- runtime ----
FROM nexus.devops-db.internal/docker-base-images-public/base-debian:1.0.0

COPY --from=builder /venv /venv
COPY --from=builder /usr/local/bin/python /usr/local/bin/python
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12

ENV PATH="/venv/bin:$PATH"

WORKDIR /app

USER app

CMD ["python"]