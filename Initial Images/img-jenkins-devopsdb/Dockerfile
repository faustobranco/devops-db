FROM jenkins/jenkins:lts-slim-jdk17

USER root

ENV WORKDIR /pipeline
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

RUN apt update\
    && apt install -y python3=3.11.2-1+b1\
    && apt install -y wget vim curl python3-pip less git

ADD requirements.txt ${WORKDIR}/requirements.txt
RUN pip3 install -r ${WORKDIR}/requirements.txt --break-system-packages

# Pipelines with Blue Ocean UI and Kubernetes
RUN jenkins-plugin-cli --plugins blueocean kubernetes
