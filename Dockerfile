# Dockerfile

# === Базовый образ с Python 3.12 (slim — меньше размер) ===
FROM python:3.12-slim

# === Системные переменные ===
# Отключаем создание .pyc файлов (экономим место)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# === Рабочая директория внутри контейнера ===
WORKDIR /app

# === Устанавливаем uv (современный менеджер пакетов) ===
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# === Копируем ТОЛЬКО файлы зависимостей (для кэша Docker) ===
# Это важный трюк: если код не менялся, Docker не будет переустанавливать пакеты
COPY pyproject.toml uv.lock ./

# === Устанавливаем зависимости (без самого проекта — для кэша) ===
RUN uv sync --frozen --no-dev --no-install-project

# === Теперь копируем весь проект ===
COPY . .

# === Устанавливаем сам проект ===
RUN uv sync --frozen --no-dev

# === Создаем non-root пользователя (безопасность!) ===
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

# === Порт, который слушает приложение ===
EXPOSE 8000

# === Healthcheck (Docker будет проверять, что приложение живо) ===
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

# === Команда запуска ===
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]