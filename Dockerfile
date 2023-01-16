FROM python:3.11.1-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN pip install --no-cache-dir poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry install --only main --no-root

COPY lpdalle /app/lpdalle

CMD ["python", "-m", "lpdalle"]
