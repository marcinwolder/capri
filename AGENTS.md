# Repository Guidelines

## Project Structure & Module Organization

Pandapath is split into long-lived apps. `apps/backend` houses the Python service: `src/` contains domain modules (API calls, recommendation, NLP, routing), `tests/` mirrors that layout, and `docs/` captures generated API docs. `apps/frontend` is the Angular client; focus work under `src/app`. Shared deployment stubs live in `configs/`, `infra/`, and `docker/`, so keep environment-specific assets there instead of the app folders.

## Build, Test, and Development Commands

- `cd apps/backend && pip install -r requirements.txt`: create the Python environment (Python 3.10+).
- `cd apps/backend && python -m pytest tests`: run the backend fast test suite.
- `cd apps/backend && python -m pytest --cov=src tests`: check coverage before opening a PR.
- `cd apps/backend && pylint src`: lint backend modules.
- `cd apps/frontend && npm ci && npm run build`: install Node dependencies and build the Angular bundle.
- `cd apps/frontend && npm start`: launch the local dev server at <http://localhost:4200>.

## Coding Style & Naming Conventions

Backend code follows four-space indentation, snake_case modules, and descriptive function names; lint with Pylint before submission. Prefer pure functions and keep configuration constants in `src/constants`. Frontend TypeScript adopts the repo `.editorconfig`: two-space indents, single quotes, and `PascalCase` components under `src/app`. Keep shared styles in `src/styles.scss` and favor the Tailwind utility classes already configured.

## Testing Guidelines

Write backend tests alongside implementation in matching `tests/<module>/test_*.py` files. Use fixtures over global state and exercise error paths. For the frontend, add or update `*.spec.ts` in the same component directory and keep Karma expectations deterministic. Aim to hold backend coverage steady with `--cov` output >=80% and capture frontend regressions with `ng test --watch=false`.

## Commit & Pull Request Guidelines

Commits use short, imperative subjects (`Added .gitkeep files...`, `Frontend added`). Scope your prefix when helpful (`Backend:` or `Frontend:`) and keep bodies for rationale or breaking-change notes. Each PR should link tracking issues, summarize functional changes, and attach screenshots or API traces when UI or endpoints shift. Include the exact test commands you ran in the PR description.

## Configuration & Secrets

Never commit real credentials. Clone `apps/backend/.env-example` to `.env` for local runs and populate Firebase keys through environment variables. Frontend Firebase settings live in `apps/frontend/firebase.json`; override per environment through deployment tooling rather than hardcoding secrets.
