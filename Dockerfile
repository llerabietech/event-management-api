FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Копируем ТОЛЬКО файлы зависимостей (для кэширования)
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости (bcrypt возьмётся из готового wheel, без компиляции!)
RUN uv sync --frozen --no-dev --no-install-project

# Копируем весь проект
COPY . .

# Устанавливаем сам проект
RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]