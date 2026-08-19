from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Конфигурация приложения.
    Автоматически читает из .env файла и переменных окружения.
    """
    
    # === Приложение ===
    APP_NAME: str = Field(default="Event Manager", description="Название приложения")
    APP_ENV: str = Field(default="development", description="Окружение: development/production")
    DEBUG: bool = Field(default=True, description="Режим отладки")
    ADMIN_EMAIL: str = Field(description="Email админа")
    ADMIN_PASSWORD: str = Field(description="Пароль админа")
    
    # === База данных ===
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/event_manager",
        description="Строка подключения к PostgreSQL"
    )
    DB_POOL_SIZE: int = Field(default=20, description="Размер пула соединений")
    DB_MAX_OVERFLOW: int = Field(default=10, description="Максимальное переполнение пула")
    
     # === Безопасность ===
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    
    # Настройки чтения .env файла
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore", 
    )

# Создаем глобальный экземпляр настроек
settings = Settings()