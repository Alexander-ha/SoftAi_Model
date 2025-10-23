#!/bin/bash

source /app/build/.venv/bin/activate

if [ -n "$HUGGINGFACE_HUB_TOKEN" ]; then
    echo "Saving Hugging Face token..."
    echo "$HUGGINGFACE_HUB_TOKEN" > /app/build/.venv/hf_token.txt
fi

if [ "$#" -eq 0 ]; then
    echo "Starting web interface..."
    exec python main.py --port 8001 --host 0.0.0.0
else
    exec "$@"
fi