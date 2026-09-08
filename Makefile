# Event Manager API - Makefile
# Команды для управления проектом через Docker Compose

.PHONY: help build up down clean logs env migrate worker test shell stop restart

# Цвета для вывода
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# По умолчанию показываем help
.DEFAULT_GOAL := help

## Показать все доступные команды
help:
	@echo "$(BLUE)Event Manager API - Доступные команды:$(NC)"
	@echo ""
	@echo "$(GREEN)Основные команды:$(NC)"
	@echo "  make up          - Запустить все сервисы"
	@echo "  make build       - Собрать образы без запуска"
	@echo "  make down        - Остановить контейнеры"
	@echo "  make clean       - Остановить и удалить контейнеры + volumes"
	@echo ""
	@echo "$(GREEN)Мониторинг:$(NC)"
	@echo "  make logs        - Посмотреть логи всех сервисов"
	@echo "  make logs-app    - Логи только API"
	@echo "  make logs-worker - Логи только worker"
	@echo ""
	@echo "$(GREEN)База данных:$(NC)"
	@echo "  make migrate     - Применить миграции БД"
	@echo "  make revision    - Создать новую миграцию"
	@echo ""
	@echo "$(GREEN)Разработка:$(NC)"
	@echo "  make worker      - Запустить только consumer"
	@echo "  make test        - Запустить тесты"
	@echo "  make shell       - Зайти в контейнер app"
	@echo "  make env         - Показать переменные окружения"
	@echo ""

## Запустить все сервисы
up:
	@echo "$(GREEN)Запуск всех сервисов...$(NC)"
	docker compose up -d
	@echo "$(GREEN)Сервисы запущены!$(NC)"
	@echo "API: http://localhost:8000"
	@echo "Swagger: http://localhost:8000/docs"
	@echo "RabbitMQ: http://localhost:15672"

## Собрать образы без запуска
build:
	@echo "$(BLUE)Сборка Docker образов...$(NC)"
	docker compose build

## Собрать и запустить (с пересборкой)
rebuild:
	@echo "$(BLUE)Пересборка и запуск...$(NC)"
	docker compose up -d --build

##  Остановить контейнеры
down:
	@echo "$(YELLOW)Остановка контейнеров...$(NC)"
	docker compose down
	@echo "$(YELLOW)Контейнеры остановлены$(NC)"

## Остановить и удалить контейнеры + volumes
clean:
	@echo "$(YELLOW)Полная очистка (контейнеры + volumes)...$(NC)"
	docker compose down -v --remove-orphans
	@echo "$(YELLOW)Очистка завершена$(NC)"

## Посмотреть логи всех сервисов
logs:
	docker compose logs -f

## Логи только API
logs-app:
	docker compose logs -f app

## Логи только worker
logs-worker:
	docker compose logs -f worker

## Показать переменные окружения
env:
	@echo "$(BLUE)Переменные окружения:$(NC)"
	@echo ""
	@if [ -f .env ]; then \
		cat .env | grep -v "^#" | grep -v "^$$"; \
	else \
		echo "$(YELLOW)Файл .env не найден. Создайте его из .env.example$(NC)"; \
	fi

## Применить миграции БД
migrate:
	@echo "$(BLUE)Применение миграций...$(NC)"
	docker compose exec app alembic upgrade head
	@echo "$(GREEN)Миграции применены$(NC)"

## Создать новую миграцию (использование: make revision msg="описание")
revision:
	@echo "$(BLUE)Создание миграции...$(NC)"
	docker compose exec app alembic revision --autogenerate -m "$(msg)"
	@echo "$(GREEN)Миграция создана$(NC)"

## Запустить только consumer
worker:
	@echo "$(GREEN)Запуск worker...$(NC)"
	docker compose up worker

## Запустить тесты
test:
	@echo "$(BLUE)Запуск тестов...$(NC)"
	docker compose exec app pytest tests/ -v

## Запустить тесты с покрытием
test-coverage:
	@echo "$(BLUE)Запуск тестов с покрытием...$(NC)"
	docker compose exec app pytest tests/ --cov=app --cov-report=term-missing

## Зайти в контейнер app
shell:
	docker compose exec app sh

## Зайти в контейнер postgres
psql:
	docker compose exec postgres psql -U $${POSTGRES_USER:-user} -d $${POSTGRES_DB:-event_manager}

## Перезапустить сервисы
restart:
	@echo "$(YELLOW)Перезапуск сервисов...$(NC)"
	docker compose restart
	@echo "$(GREEN)Сервисы перезапущены$(NC)"

## Остановить без удаления
stop:
	@echo "$(YELLOW)Остановка сервисов...$(NC)"
	docker compose stop
	@echo "$(YELLOW)Сервисы остановлены$(NC)"

## Запустить остановленные сервисы
start:
	@echo "$(GREEN)Запуск сервисов...$(NC)"
	docker compose start

## Статус контейнеров
status:
	docker compose ps

## Удалить все неиспользуемые Docker ресурсы
prune:
	@echo "$(YELLOW)Удаление неиспользуемых ресурсов...$(NC)"
	docker system prune -f
	@echo "$(GREEN)Очистка завершена$(NC)"

## Установить зависимости локально (без Docker)
install:
	@echo "$(BLUE)Установка зависимостей через uv...$(NC)"
	uv sync
	@echo "$(GREEN)Зависимости установлены$(NC)"

## Обновить lock файл
lock:
	@echo "$(BLUE)Обновление uv.lock...$(NC)"
	uv lock
	@echo "$(GREEN)Lock файл обновлен$(NC)"

## Информация о системе
info:
	@echo "$(BLUE)Информация о Docker:$(NC)"
	@docker --version
	@echo ""
	@echo "$(BLUE)Запущенные контейнеры:$(NC)"
	@docker compose ps