FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc g++ python3-dev build-essential curl nodejs npm

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"
ENV UV_COMPILE_BYTECODE=0

WORKDIR /app

# Python dependencies
COPY pyproject.toml ./
COPY uv.lock ./
RUN uv lock
RUN uv sync

# Build UI
COPY ui /ui
WORKDIR /ui
RUN npm install && npm run build

# Back to app directory
WORKDIR /app
COPY . /app

# Copy built UI assets to app/static (adjust path as needed)
RUN mkdir -p /app/static && cp -r /ui/dist/* /app/static/

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
