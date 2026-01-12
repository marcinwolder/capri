#!/usr/bin/env sh

set -euo pipefail

MODEL_PATH="${MODEL_PATH:-/models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf}"
MODEL_URL="${MODEL_URL:-}"
MODEL_SHA256="${MODEL_SHA256:-}"

download_model() {
  if [ -z "$MODEL_URL" ]; then
    echo "MODEL_URL is not set; cannot download model." >&2
    exit 1
  fi

  mkdir -p "$(dirname "$MODEL_PATH")"
  echo "Downloading model from $MODEL_URL to $MODEL_PATH"
  curl -L -C - --fail --progress-bar "$MODEL_URL" -o "$MODEL_PATH"
}

verify_checksum() {
  if [ -z "$MODEL_SHA256" ]; then
    return 0
  fi

  echo "Verifying model checksum..."
  echo "${MODEL_SHA256}  ${MODEL_PATH}" | sha256sum -c -
}

ensure_model() {
  if [ ! -f "$MODEL_PATH" ]; then
    download_model
  fi

  if ! verify_checksum; then
    echo "Checksum failed; re-downloading model..." >&2
    rm -f "$MODEL_PATH"
    download_model
    verify_checksum
  fi
}

ensure_model

exec python -m llama_cpp.server "$@"
