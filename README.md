# Event Manager API – Система управления событиями

Современный RESTful API для управления событиями, построенный на FastAPI. Включает JWT-аутентификацию с refresh-токенами, ролевую модель доступа (USER / MODERATOR / ADMIN), асинхронную работу с PostgreSQL, кэширование через Redis и событийно-ориентированную архитектуру на RabbitMQ.

Идеально подходит для изучения чистой архитектуры FastAPI, dependency injection, JWT-безопасности и интеграции с message broker.

---

##  Возможности

 **Аутентификация и авторизация:**
- Регистрация и вход пользователей
- JWT access + refresh tokens с ротацией
- Хранение refresh токенов в БД с возможностью отзыва
- Безопасное хеширование паролей через bcrypt
- Защита от перебора (одинаковое сообщение для неверного логина/пароля)

 **Ролевая модель доступа:**
-  USER – базовый пользователь
-  MODERATOR – модератор с расширенными правами
-  ADMIN – полный доступ и управление системой
- Иерархия ролей: ADMIN > MODERATOR > USER

 **Управление событиями:**
- Создание, получение, обновление, удаление событий
- Проверка прав владения ресурсом
- Валидация дат (`end_time > start_time`)
- Пагинация и фильтрация

 **Безопасность:**
- Middleware: CORS, GZip, TrustedHost
- Централизованная обработка ошибок с пользовательскими exception handlers
- Request ID для трассировки
- Защита от Host-атак

 **Кэширование:**
- Redis для кэширования ответов API
- Rate limiting на основе Redis
- Blacklist отозванных refresh токенов

 **Event-Driven архитектура:**
- Публикация событий в RabbitMQ при создании/обновлении событий
- Отдельный worker для обработки сообщений
- Поддержка TOPIC exchange и routing keys
- Идемпотентная обработка сообщений

 **Docker & Makefile:**
- Полностью контейнеризованное приложение
- Multi-service orchestration через Docker Compose
- Отдельный сервис для worker'а

---

##  Технологический стек

| Категория | Технология |
|-----------|-----------|
| **Язык** | Python 3.12+ |
| **Web-фреймворк** | FastAPI |
| **Package Manager** | uv |
| **ORM** | SQLAlchemy 2.0 (async) |
| **База данных** | PostgreSQL (asyncpg) |
| **Валидация** | Pydantic v2 |
| **Аутентификация** | PyJWT + bcrypt |
| **Кэш** | Redis (async) |
| **Message Broker** | RabbitMQ (aio-pika) |
| **Контейнеризация** | Docker, Docker Compose |
| **Архитектура** | Clean Architecture, DI, Repository Pattern |

---

##  Установка

### 1. Клонируйте репозиторий

```bash
git clone git@github.com:your-username/event-manager-api.git
cd event-manager-api
```

### 2. Создайте `.env` файл

```bash
cp .env.example .env
```

Заполните переменные:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/event_manager

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-in-production

# Redis
REDIS_URL=redis://redis:6379/0

# RabbitMQ
RABBITMQ_USER=admin
RABBITMQ_PASSWORD=admin_password
RABBITMQ_URL=amqp://admin:admin_password@rabbitmq:5672/

# Admin user (создаётся автоматически при первом запуске)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=strong_admin_password
```

### 3. Установите зависимости локально (опционально)

```bash
uv sync
```

---

##  Запуск с Docker (Рекомендуется)

Используется Docker Compose для запуска всех сервисов вместе.

### Запустить все сервисы

```bash
make up
```

Это запустит:
-  **app** – FastAPI приложение на порту 8000
-  **worker** – RabbitMQ consumer для обработки событий
-  **postgres** – PostgreSQL база данных
-  **rabbitmq** – RabbitMQ broker с UI на порту 15672
-  **redis** – Redis для кэширования

### Другие Make команды

```bash
make build    # Собрать образы без запуска
make logs     # Посмотреть логи всех сервисов
make down     # Остановить контейнеры
make clean    # Остановить и удалить контейнеры + volumes
make env      # Показать переменные окружения
make migrate  # Применить миграции БД
make worker   # Запустить только consumer
make help     # Показать все команды
```

### Доступ после запуска

| Сервис | URL |
|--------|-----|
| API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| RabbitMQ Management | http://localhost:15672 (admin / admin_password) |

---

##  Конфигурация

Приложение настраивается через переменные окружения. Основные настройки:

### База данных

```env
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/event_manager
```

### Безопасность

```env
JWT_SECRET_KEY=your-secret-key-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Redis

```env
REDIS_URL=redis://redis:6379/0
```

### RabbitMQ

```env
RABBITMQ_USER=admin
RABBITMQ_PASSWORD=admin_password
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
```

### Bootstrap (создание админа)

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=strong_password
ADMIN_EMAIL=admin@example.com
```

Полный список переменных см. в `.env.example`.

---

## Структура проекта

```
event-manager-api/
├── app/                          # Основной код приложения
│   ├── api/                      # HTTP-слой
│   │   └── v1/                   # API версии 1
│   │       ├── router.py         # Главный роутер
│   │       ├── auth.py           # Auth endpoints
│   │       ├── events.py         # Events endpoints
│   │       └── users.py          # Users endpoints
│   │
│   ├── core/                     # Ядро приложения
│   │   ├── config.py             # Настройки (pydantic-settings)
│   │   ├── security.py           # JWT, bcrypt, хеширование
│   │   ├── permissions.py        # Проверка ролей и прав
│   │   ├── bootstrap.py          # Создание админа при старте
│   │   └── error_handlers.py     # Обработчики исключений
│   │
│   ├── db/                       # Работа с БД
│   │   ├── base.py               # Базовый класс моделей
│   │   └── session.py            # Async session factory
│   │
│   ├── dependencies/             # FastAPI dependencies (DI)
│   │   ├── repositories.py       # Repository dependencies
│   │   ├── current_user.py       # Текущий пользователь
│   │   ├── redis.py              # Redis dependency
│   │   └── rabbit.py             # RabbitMQ dependency
│   │
│   ├── exceptions/               # Кастомные исключения
│   │   ├── __init__.py
│   │   ├── base.py               # AppException, NotFoundError
│   │   ├── auth.py               # Auth errors
│   │   ├── user.py               # User errors
│   │   └── event.py              # Event errors
│   │
│   ├── messaging/                # Message broker
│   │   └── rabbit.py             # RabbitMQ client
│   │
│   ├── middleware/               # Middleware
│   │   └── register.py           # Регистрация middleware
│   │
│   ├── models/                   # SQLAlchemy модели
│   │   ├── enums.py              # UserRole
│   │   ├── user.py               # User model
│   │   ├── event.py              # Event model
│   │   └── refresh_token.py      # RefreshToken model
│   │
│   ├── repositories/             # Data access layer
│   │   ├── user_repository.py
│   │   ├── event_repository.py
│   │   └── refresh_token_repository.py
│   │
│   ├── schemas/                  # Pydantic схемы
│   │   ├── auth.py               # Auth request/response
│   │   ├── user.py               # User schemas
│   │   ├── event.py              # Event schemas
│   │   └── error.py              # Error response schema
│   │
│   ├── services/                 # Бизнес-логика
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── event_service.py
│   │   └── cache_service.py
│   │
│   ├── workers/                  # Background workers
│   │   └── event_consumer.py     # RabbitMQ consumer
│   │
│   └── main.py                   # Точка входа
│
├── alembic/                      # Миграции БД
│   ├── versions/
│   └── env.py
│
│
├── .env.example                  # Шаблон переменных окружения
├── .gitignore
├── Dockerfile                    # Конфигурация контейнера
├── docker-compose.yml            # Multi-service orchestration
├── Makefile                      # Команды разработки
├── pyproject.toml                # Python project + dependencies
├── uv.lock                       # Lock-файл зависимостей
├── alembic.ini                   # Конфигурация Alembic
└── README.md                     # Документация
```