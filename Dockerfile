FROM python:3.11.1-slim
WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY poetry.lock pyproject.toml /app/
COPY lpdalle /app/lpdalle
CMD ["python", "-m", "lpdalle"]
