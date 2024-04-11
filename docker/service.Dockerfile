#FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime as build
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime as build


LABEL maintainer="cro7 <cro7nis@gmail.com>"

ENV USER=cro7
ENV API=subtitle-generator

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && useradd -m $USER

FROM build as runtime

RUN mkdir -p /opt/$API \
  && chown $USER:$USER /opt/$API

WORKDIR /opt/$API
RUN pip install poetry==1.8.2
COPY --chown=$USER:$USER src/service/pyproject.toml pyproject.toml
#COPY --chown=$USER:$USER poetry.lock  poetry.lock
RUN  poetry config virtualenvs.create false \
    && poetry install --with=dev --no-root --no-interaction \
    && rm -rf /root/.cache/pypoetry

USER $USER

# Copy nesessary files to docker
#COPY --chown=$USER:$USER docker/run.sh run.sh
COPY --chown=$USER:$USER src/service service
COPY --chown=$USER:$USER configs configs
COPY --chown=$USER:$USER src/app.py app.py

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/python3.10/site-packages/torch/lib

ENTRYPOINT python app.py