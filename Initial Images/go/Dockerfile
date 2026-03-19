FROM ubuntu:22.04

USER root

ARG TARGETARCH
ENV WORKDIR=/pipeline
ENV DEBIAN_FRONTEND=noninteractive
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}
ENV GO_VERSION=1.23.0

COPY ca.crt /usr/local/share/ca-certificates/devops-db.crt

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       wget \
       vim \
       curl \
       less \
       git \
       jq \
       openjdk-21-jre-headless \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://go.dev/dl/go${GO_VERSION}.linux-${TARGETARCH}.tar.gz \
    && tar -C /usr/local -xzf go${GO_VERSION}.linux-${TARGETARCH}.tar.gz \
    && rm go${GO_VERSION}.linux-${TARGETARCH}.tar.gz

ENV GOPATH=/go
ENV PATH=$PATH:/usr/local/go/bin:$GOPATH/bin

RUN mkdir -p $GOPATH/bin && chmod -R 777 $GOPATH