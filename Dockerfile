# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN mkdir -p build && cd build && \
    cmake -DWITH_HF_TOKEN=OFF .. && \
    cmake --build . --target run_tests

RUN mkdir -p static/uploads static/generated

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8001

ENV PYTHONPATH=/app
ENV FLASK_ENV=production

ENTRYPOINT ["docker-entrypoint.sh"]