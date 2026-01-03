# Windows Instructions (English)

## Requirements

- Windows: Windows 10/11 with virtualization enabled, WSL2, and Docker Desktop (for Docker workflows).
- macOS: macOS 12+ (Intel or Apple Silicon) with virtualization enabled and Docker Desktop (or another Docker engine with `docker compose`).

## Backend + llama via Docker (recommended)

1) Clone and copy env:

   ```powershell
   # Windows PowerShell
   git clone <repo> capri
   cd capri
   copy apps\backend\.env.example apps\backend\.env
   ```

   ```bash
   # macOS / zsh or bash
   git clone <repo> capri
   cd capri
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
