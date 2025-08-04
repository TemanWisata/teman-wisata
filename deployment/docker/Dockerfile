FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc g++ python3-dev build-essential curl

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"
ENV UV_COMPILE_BYTECODE=0

WORKDIR /app

COPY pyproject.toml ./
COPY uv.lock ./
RUN uv lock
RUN uv sync

COPY . /app

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
