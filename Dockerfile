# Используем официальный образ Python
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN python -m venv /app/venv
RUN /app/venv/bin/pip install --upgrade pip

RUN /app/venv/bin/pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu
RUN /app/venv/bin/pip install huggingface-hub==0.19.4 diffusers==0.21.4 transformers==4.35.2 accelerate==0.24.1
RUN /app/venv/bin/pip install flask==2.3.3 werkzeug==2.3.7 pillow==9.5.0
RUN /app/venv/bin/pip install pytest

RUN mkdir -p static/uploads static/generated

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8001

ENV PYTHONPATH=/app
ENV FLASK_ENV=production

ENTRYPOINT ["docker-entrypoint.sh"]