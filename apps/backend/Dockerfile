FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip uv

COPY pyproject.toml uv.lock ./ 
RUN uv sync --frozen

COPY src/ src/

EXPOSE 5001

CMD ["uv", "run", "waitress-serve", "--listen=0.0.0.0:5001", "src.backend.wsgi:app"]
