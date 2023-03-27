FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install

COPY . /app/