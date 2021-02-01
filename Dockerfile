ARG ARCH=
FROM ${ARCH}ubuntu:20.04

COPY ./Dockerfile.yml /root/.ansible/site.yml

RUN apt update && \
    apt install -y ansible aptitude python3-apt && \
    ansible-playbook /root/.ansible/site.yml && \
    apt-get remove -y --purge ansible python3-apt && \
    apt-get autoremove -y && \
    apt-get autoclean && \
    apt-get clean


VOLUME /app/
VOLUME /app/data/
WORKDIR /app

COPY src/requirements.txt /app/
RUN python3 -m pip install -r /app/requirements.txt
COPY src/ /app/

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
