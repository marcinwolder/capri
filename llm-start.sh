#!/bin/bash
set -e

# Download model if it doesn't exist
if [ ! -f "$MODEL" ]; then
    echo "Model not found at $MODEL"
    echo "Downloading from $MODEL_DOWNLOAD_URL..."
    python3 -c "
import urllib.request
import sys
print('Downloading model...')
urllib.request.urlretrieve('$MODEL_DOWNLOAD_URL', '$MODEL')
print('Download complete!')
"
    echo "Model downloaded successfully"
else
    echo "Model found at $MODEL"
fi

# Start the server with optimal settings for TinyLlama
echo "Starting llama-cpp-python server..."
exec python3 -m llama_cpp.server \
    --model "$MODEL" \
    --n_ctx "${N_CTX:-2048}" \
    --n_gpu_layers 0 \
    --host 0.0.0.0 \
    --port 8000
