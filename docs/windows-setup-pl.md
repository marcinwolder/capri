# Instrukcje dla Windows (polski)

## Wymagania

- Windows: Windows 10/11 z włączoną wirtualizacją, WSL2 i Docker Desktop (dla pracy z Dockerem).
- macOS: macOS 12+ (Intel lub Apple Silicon) z włączoną wirtualizacją i Docker Desktop (albo innym silnikiem Docker z `docker compose`).

## Backend + llama przez Docker (zalecane)

1) Sklonuj repo i skopiuj plik env:

   ```powershell
   # Windows PowerShell
   git clone <repo> capri
   cd capri
   copy apps\backend\.env.example apps\backend\.env
   ```

   ```bash
   # macOS / zsh lub bash
   git clone <repo> capri
   cd capri
   cp apps/backend/.env.example apps/backend/.env
   ```

2) Uzupełnij `apps\backend\.env` (klucz Google Places API).
3) Uruchom:

   ```powershell
   # Windows PowerShell
   docker compose up --build
   ```

   ```bash
   # macOS / zsh lub bash
   docker compose up --build
   ```

4) Oczekiwane:
   - Backend: <http://localhost:5000>
   - Llama: <http://localhost:3000> (przy pierwszym uruchomieniu pobiera ~600MB do `apps/llama/models`)

## Backend natywnie bez Dockera

Używaj tylko, gdy Docker jest niedostępny; model llama musi wtedy działać zdalnie/na innym hoście.

```powershell
# Windows PowerShell
cd apps\backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.backend.main --no_db
```

```bash
# macOS / zsh lub bash
cd apps/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.backend.main --no_db
```
