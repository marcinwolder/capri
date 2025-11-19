# Repository Guidelines

## Project Structure & Module Organization

- Pandapath is a monorepo with long-lived apps. Keep work scoped to the relevant app:
  - `apps/backend`: Flask API plus the recommendation, NLP, routing, and database layers. `src/` holds the domain code, `tests/` mirrors that layout, and `docs/` produces Sphinx docs.
  - `apps/frontend`: Angular 16 client under `src/app` with shared styles in `src/styles.scss`.
  - `apps/llama`: Git submodule vendoring LlamaGPT for the OpenAI-compatible summarization API. Treat it as third-party code; prefer upstream changes rather than editing local sources unless absolutely required.
- Deployment stubs (manifests, Docker bits, Terraform placeholders) belong in `configs/`, `docker/`, and `infra/`. Keep environment-specific secrets out of the app folders.

## Build, Test, and Development Commands

- Backend environment:
  - `cd apps/backend && uv venv && uv pip sync`: preferred flow that reads `pyproject.toml`/`uv.lock`.
  - `cd apps/backend && python -m venv .venv && .\.venv\Scripts\activate && pip install -r requirements.txt`: fallback pip install.
  - Copy `.env.example` to `.env` and provide `GOOGLE_PLACES_API_KEY`, Firebase service accounts via `PLACES_DB_API_CONFIG`/`USERS_DB_API_CONFIG` or file paths `PLACES_DB_API_CONFIG_FILE`/`USERS_DB_API_CONFIG_FILE`, plus optional Twitter creds (`USER`, `PASSWORD`, `EMAIL`).
  - Start the API: `cd apps/backend && python -m src.backend.main [--debug] [--from_file] [--no_db]` (listens on `http://localhost:5000`).
  - Tests & tooling: `python -m pytest tests`, `python -m pytest --cov=src tests`, `pylint src`.
  - Docs: `cd apps/backend/docs && make html`.
- Frontend environment:
  - `cd apps/frontend && npm ci`: install Node dependencies.
  - Copy `src/environments/environment.template` to `src/environments/environment.ts`, then set `backendHost`, `llamaHost`, Firebase settings, and optional `googlePlacesAPIKey`.
  - `npm start`: dev server at <http://localhost:4200>.
  - `npm run build`: production bundle.
  - `npm test`: Karma unit suite.
- Llama summarizer:
  - `git submodule update --init --recursive apps/llama`: ensure the code is present.
  - `cd apps/llama && ./run.sh --model 7b [--with-cuda]`: launch the OpenAI-compatible API on <http://localhost:3001/v1/chat/completions> (UI on <http://localhost:3000>).
  - Update the Angular environment if you host the service on a different port or domain.

## Coding Style & Naming Conventions

- Backend: four-space indentation, snake_case modules, descriptive function names, and English-only identifiers. Keep configuration constants in `src/constants` and favor pure functions where possible.
- Frontend: two-space indents, single quotes, and `PascalCase` components per `.editorconfig`. Store shared styles in `src/styles.scss` and lean on the existing Tailwind utilities.
- Avoid modifying third-party assets inside `apps/llama` unless patching is unavoidable; upstream contributions are preferred.

## Testing Guidelines

- Backend tests live next to their modules under `tests/<module>/test_*.py`. Use fixtures, assert both success and failure paths, and keep `--cov=src` at or above 80%.
- Frontend tests belong in `*.spec.ts` files alongside the components/services they cover. Keep Karma expectations deterministic and runnable via `ng test --watch=false`.
- Record any manual steps (e.g., seeding cached Google Places responses) in the relevant README updates if tests depend on them.

## Commit & Pull Request Guidelines

- Use short, imperative commit subjects (optionally prefixed with `Backend:` or `Frontend:`). Reserve bodies for rationale or breaking-change warnings.
- PRs should link tracking issues, summarize functional changes, and include screenshots or API traces for UI or endpoint updates. Always list the exact test commands you executed.

## Configuration & Secrets

- Never commit real credentials. Use `apps/backend/.env.example` as the template for backend secrets and keep Firebase service accounts out of Git.
- Frontend environment variables belong in `apps/frontend/src/environments/*.ts`; keep Firebase keys configurable per deployment.
- The Llama service inherits its own `.env`/Docker configuration—store overrides in deployment tooling rather than editing committed files.
