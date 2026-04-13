# ---- builder ----
FROM python:3.12-alpine AS builder

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /venv
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# ---- runtime ----
FROM nexus.devops-db.internal/docker-base-images-public/python-minimal-debian:3.12-1.0.0

COPY --from=builder /venv /venv

ENV PATH="/venv/bin:$PATH"

WORKDIR /app

USER app

CMD ["python", "app.py"]
