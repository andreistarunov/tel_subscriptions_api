FROM python:3.14

ENV POETRY_ENV_PATH=venv/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
# RUN $POETRY_ENV_PATH env use 3.14
RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]