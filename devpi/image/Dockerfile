FROM ubuntu:22.04

ENV WORKDIR /work/devpi-data/
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

# install dependencies
RUN apt update \
    && apt install -y python3 python3-pip
    
RUN pip3 install devpi-server devpi-web devpi-client 

RUN devpi-init --serverdir /work/devpi-data/data

# Auto-Start service
COPY startup.sh ${WORKDIR}
RUN chmod +x startup.sh
WORKDIR ${WORKDIR}
ENTRYPOINT ./startup.sh