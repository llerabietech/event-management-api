from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Конфигурация приложения.
    Автоматически читает из .env файла и переменных окружения.
    """
    
    # === Приложение ===
    APP_NAME: str = Field(default="Event Manager", description="Название приложения")
    APP_ENV: str = Field(default="development", description="Окружение: development/production")
    DEBUG: bool = Field(default=True, description="Режим отладки")
    
    # === База данных ===
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/event_manager",
        description="Строка подключения к PostgreSQL"
    )
    DB_POOL_SIZE: int = Field(default=20, description="Размер пула соединений")
    DB_MAX_OVERFLOW: int = Field(default=10, description="Максимальное переполнение пула")
    
    
    # Настройки чтения .env файла
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore", 
    )

# Создаем глобальный экземпляр настроек
settings = Settings()