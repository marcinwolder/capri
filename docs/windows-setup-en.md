# Windows Instructions (English)

## Requirements

- Windows: Windows 10/11 with virtualization enabled, WSL2, and Docker Desktop (for Docker workflows).
- macOS: macOS 12+ (Intel or Apple Silicon) with virtualization enabled and Docker Desktop (or another Docker engine with `docker compose`).

## Backend + llama via Docker (recommended)

1) Clone and copy env:

   ```powershell
   # Windows PowerShell
   git clone <repo> pandapath
   cd pandapath
   copy apps\backend\.env.example apps\backend\.env
   ```

   ```bash
   # macOS / zsh or bash
   git clone <repo> pandapath
   cd pandapath
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

## Llama without Docker (Windows and macOS)

Run the llama.cpp server locally if you cannot use Docker. This uses the same TinyLlama model and serves it on port 3000.

### Prerequisites

- Python 3.10+ and `pip` available in your shell.
- Build tools: Windows needs the C++ build tools from Visual Studio (or Build Tools for VS) plus CMake; macOS needs Xcode Command Line Tools and Homebrew `cmake` (`brew install cmake`).
- ~600MB free disk for the model download into `apps/llama/models/`.

### Install dependencies

```powershell
# Windows PowerShell
cd apps\llama
py -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip cmake
pip install "llama-cpp-python[server]==0.3.16"
```

```bash
# macOS / zsh or bash
cd apps/llama
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip cmake
pip install "llama-cpp-python[server]==0.3.16"
```

### Download the TinyLlama model

```powershell
# Windows PowerShell
Invoke-WebRequest "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_0.gguf" `
  -OutFile "apps/llama/models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf"
```

```bash
# macOS / zsh or bash
curl -L "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_0.gguf" \
  -o apps/llama/models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf
```

### Start the server

```powershell
# Windows PowerShell (from repo root or apps\llama)
cd apps\llama
.venv\Scripts\activate
python -m llama_cpp.server --model "apps/llama/models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf" --host 0.0.0.0 --port 3000
```

```bash
# macOS / zsh or bash (from repo root or apps/llama)
cd apps/llama
source .venv/bin/activate
python -m llama_cpp.server --model "apps/llama/models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf" --host 0.0.0.0 --port 3000
```
