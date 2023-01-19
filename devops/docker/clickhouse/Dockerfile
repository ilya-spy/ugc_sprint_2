FROM python:3.9 AS base

LABEL maintainer="Ilya Kuprik <ilya-spy@yandex.ru>"


# -----------------------------------------------------------------------------
# base environment
# -----------------------------------------------------------------------------
RUN apt-get -y update && apt install -y software-properties-common apt-utils

ARG uid=1000
ARG gid=1000

ENV USER=olap
ENV GROUP=olap
ENV HOMEDIR=/home/${USER}
ENV APP_HOME=/usr/src/ugc
ENV APP_REQUIREMENTS="${APP_HOME}_lib"
ENV PATH="/home/${USER}/.local/bin:${PATH}"
ENV PYTHONPATH="${PYTHONPATH}:${APP_HOME}"

RUN mkdir ${APP_HOME}
RUN mkdir ${APP_REQUIREMENTS}

WORKDIR ${APP_HOME}

# Create an unpriviledged user
RUN groupadd -g $gid ${GROUP} && \
    useradd -d ${HOMEDIR} -s /bin/bash -u $uid -g $gid ${USER} && \
    mkdir ${HOMEDIR} && \
    chown -R ${USER}:${GROUP} ${HOMEDIR}

COPY --chown=${USER}:${GROUP} devops/clickhouse/requirements ${APP_REQUIREMENTS}

USER ${USER}

RUN pip3 install -r "${APP_REQUIREMENTS}/base.txt"


# -----------------------------------------------------------------------------
# production environment
# -----------------------------------------------------------------------------
FROM base AS production

USER ${USER}

COPY --chown=${USER}:${GROUP} ../../src ${APP_HOME}

RUN pip3 install -r "${APP_REQUIREMENTS}/prod.txt"


# -----------------------------------------------------------------------------
# development environment
# -----------------------------------------------------------------------------
FROM base AS develop

USER root

RUN apt-get install -y vim make curl git tree jq iputils-ping

USER ${USER}

RUN pip3 install -r "${APP_REQUIREMENTS}/dev.txt"
