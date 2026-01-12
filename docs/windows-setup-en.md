# Windows Instructions (English)

## Requirements

- Windows: Windows 10/11 with virtualization enabled, WSL2, and Docker Desktop (for the backend + llama stack).
- macOS: macOS 12+ (Intel or Apple Silicon) with virtualization enabled and Docker Desktop (or another Docker engine with `docker compose`).

## Step-by-step setup

1) Install the CAPRI Desktop app by running `CAPRI Setup 0.1.0.exe`. Follow the installer prompts and confirm the app launches successfully when it finishes.
2) Unzip the backend package `capri.zip` into the folder where you want to run the stack (for example `C:\capri-backend`). The extracted directory should contain the project files plus `docker-compose.yml`.
3) Inside the extracted folder run:

   ```powershell
   docker compose up
   ```

   The command starts the backend at <http://localhost:5000> and the Llama service at <http://localhost:3000>. The first run downloads ~600MB of models into `apps/llama/models`.