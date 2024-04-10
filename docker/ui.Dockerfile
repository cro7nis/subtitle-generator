FROM python:3.10-slim as build

LABEL maintainer="cro7 <cro7nis@gmail.com>"

ENV USER=cro7
ENV PORT=8051
ENV API=subtitle-generator-ui

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && useradd -m $USER

FROM build as runtime

RUN mkdir -p /opt/$API \
  && chown $USER:$USER /opt/$API

WORKDIR /opt/$API
RUN pip install poetry==1.8.2
COPY --chown=$USER:$USER src/ui/pyproject.toml pyproject.toml
#COPY --chown=$USER:$USER poetry.lock  poetry.lock
RUN  poetry config virtualenvs.create false \
    && poetry install --with=dev --no-root --no-interaction \
    && rm -rf /root/.cache/pypoetry

USER $USER

# Copy nesessary files to docker
#COPY --chown=$USER:$USER docker/run.sh run.sh
COPY --chown=$USER:$USER src/ui ui
COPY --chown=$USER:$USER src/ui.py ui.py
COPY --chown=$USER:$USER configs configs
COPY --chown=$USER:$USER assets assets
COPY --chown=$USER:$USER .streamlit .streamlit
COPY --chown=$USER:$USER docker/start_ui.sh start_ui.sh

EXPOSE ${PORT}

ENTRYPOINT bash start_ui.sh
