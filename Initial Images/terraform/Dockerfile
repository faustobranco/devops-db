FROM registry.devops-db.internal:5000/ubuntu_python:3.10.6

USER root

RUN apt install -y lsb-release

RUN wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg\
    && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list\
    && apt update\
    && apt install -y terraform

ADD requirements.txt ${WORKDIR}/requirements.txt
RUN pip3 install -r ${WORKDIR}/requirements.txt