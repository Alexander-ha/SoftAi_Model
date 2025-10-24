FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY CMakeLists.txt .
COPY requirements.txt .
COPY compatible_requirements.txt .
COPY src/ ./src/
COPY tests/ ./tests/
COPY static/ ./static/
COPY templates/ ./templates/

RUN python -m venv /app/venv
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install -r requirements.txt || /app/venv/bin/pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

RUN mkdir -p static/uploads static/generated

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8001

ENV PYTHONPATH=/app
ENV FLASK_ENV=production
ENV VENV_DIR=/app/venv

ENTRYPOINT ["docker-entrypoint.sh"]