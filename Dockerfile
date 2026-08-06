FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# 1. Системные зависимости для компиляции bcrypt
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Устанавливаем Rust (нужен для bcrypt >= 4.1)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --profile minimal
ENV PATH="/root/.cargo/bin:${PATH}"

# 3. Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 4. Копируем ТОЛЬКО файлы зависимостей (для кэширования)
COPY pyproject.toml uv.lock ./

# 5. Устанавливаем зависимости (здесь создается ПРАВИЛЬНЫЙ .venv)
RUN uv sync --frozen --no-dev

# 6. Копируем весь проект (.dockerignore не даст скопировать локальный .venv!)
COPY . .

# 7. Синхронизируем еще раз, чтобы установить сам проект
RUN uv sync --frozen --no-dev

# 8. Создаем non-root пользователя
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# 9. Явно используем uv run для гарантии правильного окружения
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]