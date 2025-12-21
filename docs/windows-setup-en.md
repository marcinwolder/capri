# Windows Instructions (English)

## Requirements

- Windows: Windows 10/11 with virtualization enabled, WSL2, and Docker Desktop (for Docker workflows).
- macOS: macOS 12+ (Intel or Apple Silicon) with virtualization enabled and Docker Desktop (or another Docker engine with `docker compose`).

## Backend + llama via Docker (recommended)

1) Clone and copy env:

   ```powershell
   # Windows PowerShell
   git clone <repo> cita-system
   cd cita-system
   copy apps\backend\.env.example apps\backend\.env
   ```

   ```bash
   # macOS / zsh or bash
   git clone <repo> cita-system
   cd cita-system
   cp apps/backend/.env.example apps/backend/.env
   ```

2) Fill in `apps\backend\.env` (Google Places API key).
3) Run:

   ```powershell
   # Windows PowerShell
   docker compose up --build
   ```

   ```bash
   # macOS / zsh or bash
   docker compose up --build
   ```

4) Expected:
   - Backend: <http://localhost:5000>
   - Llama: <http://localhost:3000> (first run downloads ~600MB into `apps/llama/models`)

## Native backend without Docker

Use only when Docker is unavailable; the llama model must be remote/on another host.

```powershell
# Windows PowerShell
cd apps\backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.backend.main --no_db
```

```bash
# macOS / zsh or bash
cd apps/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.backend.main --no_db
```
