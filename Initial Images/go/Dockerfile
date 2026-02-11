FROM ubuntu:22.04

USER root

ENV WORKDIR=/pipeline
ENV DEBIAN_FRONTEND=noninteractive
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}
ENV GO_VERSION=1.23.0


RUN rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get update \
    && apt-get install -y \
       wget \
       vim \
       curl \
       less \
       git \
       openjdk-21-jre-headless \ 
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz \
    && rm go${GO_VERSION}.linux-amd64.tar.gz

ENV GOPATH=/go
ENV PATH=$PATH:/usr/local/go/bin:$GOPATH/bin

RUN mkdir -p $GOPATH/bin && chmod -R 777 $GOPATH