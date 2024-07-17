FROM registry.devops-db.internal:5000/ubuntu_python:3.10.6
ARG DEBIAN_FRONTEND=noninteractive

USER root

ENV WORKDIR /pipeline
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

RUN apt update\
    && apt install -y software-properties-common\
    && add-apt-repository --yes --update ppa:ansible/ansible\
    && apt install -y ansible

ADD requirements.txt ${WORKDIR}/requirements.txt
RUN pip3 install -r ${WORKDIR}/requirements.txt 
