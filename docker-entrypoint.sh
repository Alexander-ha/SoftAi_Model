#!/bin/bash

source /app/venv/bin/activate

if [ -n "$HUGGINGFACE_HUB_TOKEN" ]; then
    echo "Saving Hugging Face token..."
    echo "$HUGGINGFACE_HUB_TOKEN" > /app/venv/hf_token.txt
fi

if [ ! -f "/app/main.py" ]; then
    echo "Error: main.py not found!"
    echo "Files in /app:"
    ls -la /app/
    exit 1
fi

if [ "$#" -eq 0 ]; then
    echo "Starting web interface..."
    exec python /app/main.py --port 8001
else
    exec "$@"
fi