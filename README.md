CAPRI
=========

CAPRI is a travel planning platform that combines a Python/Flask backend, an Angular
frontend, and an optional self-hosted Llama-based summarization service to build
personalized city itineraries. The backend fetches attractions from Google Places, weather
providers, and a local JSON cache, optimizes each day with OR-Tools, enriches stops with nearby
dining, and produces a natural-language summary. The frontend guides travellers through
preference collection and itinerary review.

Key capabilities
----------------

- Preference-driven itineraries that consider dates, budget, accessibility, and trip length.
- Route and day-part optimization powered by OR-Tools plus travel-time estimation models.
- Aspect-based sentiment and NLP helpers to infer preferences from free text or Twitter.
- Local-only persistence for user profiles and trip history (no Firebase or third-party auth).
- Optional LlamaGPT service exposed via an OpenAI-compatible API for trip narration.

Repository layout
-----------------

- `apps/backend` – Flask API, recommendation engine, NLP, routing, database, and tests.
- `apps/frontend` – Angular 16 single-page app under `src/app` with Tailwind styling.
- `apps/llama` – llama.cpp server image that downloads TinyLlama into `apps/llama/models` when the Docker service starts.
- `configs/`, `docker/`, `infra/` – deployment and environment stubs.

Cloning
-------

```bash
git clone git@github.com:<org>/capri.git
cd capri
```

Backend service (`apps/backend`)
-------------------------------

**Prerequisites**:

- Python 3.10+
- pip (or [uv](https://github.com/astral-sh/uv)) and virtualenv tooling
- Google Places API key and optional Twitter access for `twscrape`

**Environment variables**:

Copy `.env.example` to `.env` (or export the variables some other way) and fill in:

- `GOOGLE_PLACES_API_KEY`
- `DATA_DIR` to override where local JSON persistence lives (defaults to `apps/backend/data`)
- `USER`, `PASSWORD`, `EMAIL` credentials if you plan to pull preferences from Twitter
- `LLAMA_API_URL` pointing at the llama.cpp server (defaults to `http://llama:3000/v1/chat/completions` when using Docker Compose)

When running through Docker Compose, all persistence is local to the container volume; no cloud credentials are required.

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
- Persistence is local JSON under `apps/backend/data` (configurable via `DATA_DIR`).

**Key endpoints**:

- `POST /api/recommendation/preferences` – build an itinerary from structured preferences.
- `POST /get_with_text` – extract preferences from free text and return a recommendation.
- `GET /api/restaurants-nearby` – look up dining options near a stop.
- `GET /api/trip-history` / `GET /api/trip-history/<trip_id>` – fetch stored trips (pass `user_id` query param or `X-User-Id` header).
- `POST /api/trip-history/<trip_id>/rating` – rate a place within a stored trip (body: `user_id`, `day_index`, `place_index`, `rating`).

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
# edit backendHost/llamaHost if they differ
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

The LLM service is automatically started with `docker compose up`. On first run, it will
download the TinyLlama model (~600MB, takes 1-3 minutes).

- The API lives at `http://localhost:3000/v1/chat/completions`, matching the default `LLAMA_API_URL` in `apps/backend/.env.example`.
- Model files are stored in `apps/llama/models/` (gitignored) and are fetched automatically by the Docker entrypoint if missing.
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
