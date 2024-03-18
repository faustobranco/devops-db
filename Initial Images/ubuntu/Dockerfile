FROM ubuntu:22.04

ENV WORKDIR /work
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

# install dependencies
RUN apt-get update \
    && apt-get install -y curl wget net-tools lsb-release vim less iputils-ping ssh dnsutils jq \
    && rm -rf /var/lib/apt/lists/*
