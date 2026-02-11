FROM ubuntu:22.04

USER root

ENV WORKDIR=/pipeline
ENV DEBIAN_FRONTEND=noninteractive
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

RUN rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get update -o Acquire::CompressionTypes::Order::=gz \
    && apt-get install -y --no-install-recommends --fix-missing \
       python3 \
       python3-pip \
       wget \
       vim \
       curl \
       less \
       git \
       openjdk-21-jre-headless \ 
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt ${WORKDIR}/requirements.txt
RUN pip3 install -r ${WORKDIR}/requirements.txt 
