FROM nexus.devops-db.internal/docker-base-images-public/base-debian:1.0.0

USER root

ENV GO_VERSION=1.22.3

RUN apt-get update && apt-get install -y curl ca-certificates \
 && curl -fsSL https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz | tar -C /usr/local -xz \
 && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/go/bin:${PATH}"

USER app
WORKDIR /app

CMD ["go", "version"]