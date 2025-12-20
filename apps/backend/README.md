# travel-app-back

Travel app backend (Flask).

## Setup

```bash
uv venv && uv pip sync           # preferred
# or: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in the required keys (Google Places API key; optional `DATA_DIR` override for local JSON storage).

## Run

- Development (Flask built-in): `uv run python -m src.backend.main`
- Production-like (Waitress): `uv run waitress-serve --listen=0.0.0.0:5000 src.backend.wsgi:app`

## Tests

```bash
uv run python -m pytest tests
```

## Lint

```bash
uv run pylint src
```

## Notes

- External assets (e.g., spaCy `en_core_web_sm`, GoogleNews vectors) are required for some NLP flows; install them as needed.
