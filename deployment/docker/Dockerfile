FROM python:3.12-alpine

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"


ADD . /app

WORKDIR /app
RUN uv sync --locked


CMD ["uv","run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]