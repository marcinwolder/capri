# Repository Guidelines (Current Status)

## Project Structure & Services

- Monorepo with two active apps plus an LLM service: `apps/backend` (Flask API, recommendation/NLP/routing layers), `apps/frontend` (Angular 16 + Tailwind, Electron build targets), and `apps/llama` (llama.cpp server image and model cache). Keep changes scoped to the relevant app.
- LLM summaries now come from the `llama` Docker service (llama.cpp image) loading TinyLlama into `apps/llama/models/`; treat the downloaded models as third-party/vendored and avoid editing them.
- Docker Compose wires backend + LLM (ports 5000/3000).
- Deployment/development stubs live in `configs/`, `docker/`, and `infra/`. Keep environment-specific material out of app folders.

## Build, Test, and Development Commands

- Backend (Python 3.10+):
  - Preferred install: `cd apps/backend && uv venv && uv pip sync` (uses `pyproject.toml`/`uv.lock`).
  - Fallback: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
  - Copy `.env.example` to `.env`; set `GOOGLE_PLACES_API_KEY` and optional Twitter creds (`USER`/`PASSWORD`/`EMAIL`).
  - Run API: `cd apps/backend && python -m src.backend.main [--debug] [--from_file] [--no_db]`.
  - Tests/tools: `python -m pytest tests`, `python -m pytest --cov=src tests`, `pylint src`. Docs: `cd apps/backend/docs && make html`.
- Frontend:
  - `cd apps/frontend && yarn install` (or `npm ci`).
  - Copy `src/environments/environment.template` to `src/environments/environment.ts`; set `backendHost`, `llamaHost` (defaults to `http://localhost:3000`), and optional `googlePlacesAPIKey`.
  - Web: `yarn start` / `yarn build` / `yarn test`. Desktop: `yarn electron:serve` and `yarn electron:build` (outputs to `release/`).
- LLM service:
  - `docker compose up -d` downloads TinyLlama (~600MB) into `apps/llama/models/` on first run and exposes `http://localhost:3000/v1/chat/completions`. Update frontend env vars if you host it elsewhere.

## Coding Style & Naming Conventions

- Backend: four-space indentation, snake_case modules, descriptive function names, English-only identifiers. Keep configuration constants in `src/constants`; favor pure functions where possible.
- Frontend: two-space indents, single quotes, `PascalCase` components per `.editorconfig`. Store shared styles in `src/styles.scss` and reuse Tailwind utilities.
- Treat Docker-pulled assets and model binaries as external; avoid modifying them directly.

## Testing Guidelines

- Backend tests live under `tests/<module>/test_*.py`; assert success and failure paths and keep `--cov=src` ≥ 80%.
- Frontend tests live beside components/services in `*.spec.ts`; keep Karma expectations deterministic (`ng test --watch=false`).
- Note any required cached Google Places responses or model downloads in READMEs when adding tests.

## Commit & Pull Request Guidelines

- Use short, imperative subjects (optionally prefixed with `Backend:` or `Frontend:`). Bodies capture rationale or breaking changes.
- PRs should link tracking issues, summarize functional changes, and include screenshots/API traces for UI or endpoint updates. List the exact test commands you ran.

## Configuration & Secrets

- Never commit real credentials. Use `apps/backend/.env.example` as the template and keep secrets out of Git.
- Frontend environment vars live in `apps/frontend/src/environments/*.ts`; keep them configurable per deployment.
- Model downloads populate `apps/llama/models/` (gitignored). Keep overrides to Docker/LLM config in deployment tooling rather than editing image defaults.
