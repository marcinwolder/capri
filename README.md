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
- `apps/llama` – Git submodule that hosts the LlamaGPT Docker stack used for summaries.
- `configs/`, `docker/`, `infra/` – deployment and environment stubs.
- `local/` – scratch instructions and experiments that should not ship.

Cloning & submodules
--------------------

```bash
git clone git@github.com:<org>/pandapath.git
cd pandapath
git submodule update --init --recursive apps/llama
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
- `PLACES_DB_API_CONFIG` and `USERS_DB_API_CONFIG` JSON blobs with Firebase service accounts
- `USER`, `PASSWORD`, `EMAIL` credentials if you plan to pull preferences from Twitter

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
- npm (Angular CLI is installed locally via `npm ci`)

**Setup**:

```bash
cd apps/frontend
npm ci
cp src/environments/environment.template src/environments/environment.ts
# edit backendHost, llamaHost, firebase config, and googlePlacesAPIKey
```

**Run and test**:

```bash
npm start          # serves http://localhost:4200
npm run build      # production bundle
npm test           # Karma unit tests
```

Llama summarization service (`apps/llama`)
-----------------------------------------

Trip summaries rely on an OpenAI-compatible chat completion endpoint. The `apps/llama`
submodule vendors [getumbrel/llama-gpt](https://github.com/getumbrel/llama-gpt), which can
run locally with Docker:

```bash
cd apps/llama
./run.sh --model 7b          # add --with-cuda for Nvidia acceleration
```

- The API lives at `http://localhost:3001/v1/chat/completions`, matching `src/api_calls/llama.py`.
- The optional UI runs at `http://localhost:3000`.
- Update `apps/frontend/src/environments/*.ts` if you expose the service elsewhere.

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
