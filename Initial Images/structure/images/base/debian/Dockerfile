FROM debian:bookworm-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && groupadd -g 10001 app \
 && useradd -u 10001 -g app -m -d /app app

WORKDIR /app

USER app