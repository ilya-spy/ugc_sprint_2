FROM python:3.9 AS base

LABEL maintainer="Victor Merkushov <merkushov.victor@gmail.com>"

RUN apt-get -y update \
    && apt-get install -y apt-utils

ARG uid=1000
ARG gid=1000

ENV USER=gatekeeper
ENV GROUP=gatekeeper
ENV HOMEDIR=/home/${USER}
ENV APP_HOME=/usr/src
ENV APP_REQUIREMENTS=/usr/requirements
ENV PATH="/home/${USER}/.local/bin:${PATH}"
ENV PYTHONPATH="${APP_HOME}/gate:${PYTHONPATH}"


RUN mkdir -p ${APP_HOME}
RUN mkdir -p ${APP_REQUIREMENTS}
WORKDIR ${APP_HOME}

# Create an unprivileged user
RUN groupadd -g $gid ${GROUP} && \
    useradd -d ${HOMEDIR} -s /bin/bash -u $uid -g $gid ${USER} && \
    mkdir ${HOMEDIR} && \
    chown -R ${USER}:${GROUP} ${HOMEDIR}

COPY --chown=${USER}:${GROUP} devops/gate/requirements ${APP_REQUIREMENTS}

USER ${USER}

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN /usr/local/bin/python -m pip install -r "${APP_REQUIREMENTS}/base.txt"

# -----------------------------------------------------------------------------
# production environment
# -----------------------------------------------------------------------------

FROM base AS production

USER root

COPY --chown=${USER}:${GROUP} src ${APP_HOME}

USER ${USER}

RUN /usr/local/bin/python -m pip install -r "${APP_REQUIREMENTS}/prod.txt"

WORKDIR ${APP_HOME}

# -----------------------------------------------------------------------------
# development environment
# -----------------------------------------------------------------------------

FROM base AS develop

USER root

RUN apt-get install -y vim make curl git tree jq iputils-ping

USER ${USER}

RUN /usr/local/bin/python -m pip install -r "${APP_REQUIREMENTS}/dev.txt"
