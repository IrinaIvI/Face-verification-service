FROM debian:bookworm-slim

LABEL maintainer="ira.ivashko.99@gmail.com"

WORKDIR /app

ENV POETRY_VERSION=1.8.3
ENV PATH="/root/.local/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv curl libpq-dev gcc && \
    apt-get install ffmpeg libsm6 libxext6 -y && \
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 -

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create && \
    poetry install --no-interaction --no-ansi --no-dev

COPY alembic.ini /app
COPY migrations /app/migrations
COPY ./src /app

ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]

