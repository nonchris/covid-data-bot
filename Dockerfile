ARG ARCH=
FROM ${ARCH}python:3.8

RUN apt-get update && apt-get -y upgrade && apt-get install -y \
    python3-pip


VOLUME /app/
VOLUME /app/data/
WORKDIR /app

COPY src/requirements.txt /app/
RUN python3 -m pip install -r /app/requirements.txt
COPY src/* /app/

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]