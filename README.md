PandaPath
=========

PandaPath is a travel planning platform that combines a Python/Flask backend, an Angular
frontend, and an optional self-hosted Llama-based summarization service to build
personalized city itineraries. The backend fetches attractions from Google Places, weather
providers, and Firebase, optimizes each day with OR-Tools, enriches stops with nearby
dining, and produces a natural-language summary. The frontend guides travellers through
preference collection, authentication, and itinerary review.

Key capabilities
----------------

- Preference-driven itineraries that consider dates, budget, accessibility, and trip length.
- Route and day-part optimization powered by OR-Tools plus travel-time estimation models.
- Aspect-based sentiment and NLP helpers to infer preferences from free text or Twitter.
- Firebase-backed persistence for user profiles and trip history protected by Firebase Auth.
- Optional LlamaGPT service exposed via an OpenAI-compatible API for trip narration.

Repository layout
-----------------

- `apps/backend` – Flask API, recommendation engine, NLP, routing, database, and tests.
- `apps/frontend` – Angular 16 single-page app under `src/app` with Tailwind styling.
- `models/` – Directory for LLM model files (auto-downloaded on first run).
- `configs/`, `docker/`, `infra/` – deployment and environment stubs.
- `local/` – scratch instructions and experiments that should not ship.

Cloning
-------

```bash
git clone git@github.com:<org>/pandapath.git
cd pandapath
```

Backend service (`apps/backend`)
-------------------------------

**Prerequisites**:

- Python 3.10+
- pip (or [uv](https://github.com/astral-sh/uv)) and virtualenv tooling
- Credentials for Google Places, Firebase (two service accounts), and optional Twitter access for `twscrape`

**Environment variables**:

Copy `.env.example` to `.env` (or export the variables some other way) and fill in:

- `GOOGLE_PLACES_API_KEY`
- `PLACES_DB_API_CONFIG` and `USERS_DB_API_CONFIG` JSON blobs with Firebase service accounts (or point `PLACES_DB_API_CONFIG_FILE` / `USERS_DB_API_CONFIG_FILE` to the JSON files)
- `USER`, `PASSWORD`, `EMAIL` credentials if you plan to pull preferences from Twitter

When running through Docker Compose, drop the two Firebase service-account JSON files inside `apps/backend/` and keep them out of Git. The stack mounts them as Docker secrets and injects `PLACES_DB_API_CONFIG_FILE=/run/secrets/firebase_places_sa` and `USERS_DB_API_CONFIG_FILE=/run/secrets/firebase_users_sa`, so you never need to paste the raw JSON into `.env`.

**Install dependencies**:

```bash
cd apps/backend
# Option A: uv (recommended for repeatable installs)
uv venv
uv pip sync

# Option B: pip
python -m venv .venv
.\.venv\Scripts\activate  # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

**Run the API (defaults to <http://localhost:5000>)**:

```bash
python -m src.backend.main [--debug] [--from_file] [--no_db]
```

- `--debug`: emit verbose logs and run a quick recommendation sample.
- `--from_file`: reuse cached Google Places responses from `outputs/`.
- `--no_db`: disable Firebase reads/writes (handy for local prototyping).

**Key endpoints**:

- `POST /api/recommendation/preferences` – build an itinerary from structured preferences.
- `POST /get_with_text` – extract preferences from free text and return a recommendation.
- `GET /api/restaurants-nearby` – look up dining options near a stop.
- `GET /api/trip-history` / `GET /api/trip-history/<trip_id>` – fetch stored trips (Firebase token required).

**Tests, lint, docs**:

```bash
python -m pytest tests
python -m pytest --cov=src tests
pylint src

cd apps/backend/docs
make html
```

Frontend client (`apps/frontend`)
--------------------------------

**Prerequisites**:

- Node.js 18+
- Yarn 1.x (preferred) or npm (Angular CLI is installed locally either way)

**Setup**:

```bash
cd apps/frontend
yarn install   # or npm ci
cp src/environments/environment.template src/environments/environment.ts
# edit backendHost, llamaHost, firebase config, and googlePlacesAPIKey
```

**Run and test**:

```bash
yarn start            # serves http://localhost:4200
yarn build            # production bundle
yarn test             # Karma unit tests
yarn electron:serve   # launch Electron shell against ng serve
yarn electron:build   # generate desktop installers in release/
```

LLM summarization service
-------------------------

Trip summaries and chat-based preference collection rely on an OpenAI-compatible chat
completion endpoint. The project uses **TinyLlama 1.1B** (600MB), a lightweight model
that runs efficiently on CPU.

The LLM service is automatically started with `docker-compose up`. On first run, it will
download the TinyLlama model (~600MB, takes 1-3 minutes).

- The API lives at `http://localhost:3001/v1/chat/completions`, matching `src/api_calls/llama.py`.
- Model files are stored in `models/` directory (gitignored).
- Update `apps/frontend/src/environments/*.ts` if you expose the service elsewhere.

**Model specifications:**
- Model: TinyLlama 1.1B Chat v1.0 (Q4_K_M quantized)
- Size: ~600MB
- RAM requirement: ~2GB
- Context window: 2048 tokens
- Startup time: ~30-60 seconds

Development notes
-----------------

- Route optimization, weather helpers, and collaborative models persist cached artefacts in
  `apps/backend/outputs`—keep the directory writable and version-control large blobs
  elsewhere.
- Some tests expect cached Google Places results; seed them by running
  `python -m src.backend.main --from_file`.
- A `uv.lock` file lives next to `pyproject.toml`; prefer `uv pip sync` to keep the Python
  environment deterministic.

Contributing
------------

- Scope branches to a single app when possible and include relevant README/docs updates.
- Run the applicable test suites (and `npm run build` / `python -m pytest --cov=src tests`)
  before opening a PR.

License
-------

Project licensing has not been specified yet. Confirm terms with the maintainers before redistribution.
