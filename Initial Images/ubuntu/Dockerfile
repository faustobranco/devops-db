FROM ubuntu:22.04

USER root

ENV WORKDIR /pipeline
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

RUN apt update\
    && apt install -y python3=3.10.6-1~22.04\
    && apt install -y wget vim curl python3-pip less git

ADD requirements.txt ${WORKDIR}/requirements.txt
RUN pip3 install -r ${WORKDIR}/requirements.txt 
