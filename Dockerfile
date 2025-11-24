FROM python:3.14

ENV PYTHON_ENV_PATH=venv/bin/python3
ENV POETRY_ENV_PATH=venv/bin/poetry

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN python3 -m venv venv
RUN $PYTHON_ENV_PATH -m pip install poetry
RUN $POETRY_ENV_PATH env use 3.14
RUN $POETRY_ENV_PATH install --no-root

COPY . .