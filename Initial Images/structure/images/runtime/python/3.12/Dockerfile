FROM nexus.devops-db.internal/docker-base-images-public/base-debian:1.0.0

USER root

RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

USER app

WORKDIR /app

CMD ["python3"]