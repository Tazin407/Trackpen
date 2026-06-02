FROM python:3.12-slim

# Install uv by copying the binary directly from the official image
# This is faster and cleaner than running 'pip install uv'
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Enable bytecode compilation so the container starts up faster
ENV UV_COMPILE_BYTECODE=1

# Copy only the dependency files first to leverage Docker's layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies using a Docker cache mount.
# This prevents downloading packages from scratch if you change code later.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of your application code
COPY . .

# Sync the project itself (fast, since dependencies are already cached)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
