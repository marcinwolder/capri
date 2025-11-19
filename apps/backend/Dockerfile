FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip uv

COPY apps/backend/pyproject.toml apps/backend/uv.lock ./ 
RUN uv sync --frozen

RUN uv pip install pip
RUN uv run python -m spacy download en_core_web_sm
RUN uv pip uninstall pip

COPY apps/backend/ /app/

EXPOSE 5000

CMD ["uv", "run", "python", "-m", "src.backend.main"]
