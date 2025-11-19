SHELL := powershell.exe
SHELLFLAGS := -NoProfile -Command

COMPOSE_FILE = docker-compose.yml
BACKEND_DIR = apps/backend

.PHONY: setup-backend download-spacy compose-build compose-up compose-down compose-logs

setup-backend:
	cd $(BACKEND_DIR); uv sync --frozen; if (!(Test-Path ".\\.env")) { Copy-Item ".\\.env.example" ".\\.env" }

download-spacy: setup-backend
	cd $(BACKEND_DIR); uv pip install pip; uv run python -m spacy download en_core_web_sm; uv pip uninstall pip

start-backend:
	cd $(BACKEND_DIR); uv run python -m src.backend.main;

compose-build:
	docker compose -f $(COMPOSE_FILE) build

compose-up:
	docker compose -f $(COMPOSE_FILE) up -d

compose-down:
	docker compose -f $(COMPOSE_FILE) down

compose-logs:
	docker compose -f $(COMPOSE_FILE) logs -f
