from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from core.config import settings


# Создаем асинхронный движок
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,              
    pool_size=20,           
    max_overflow=10,
)

# Фабрика сессий
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False, 
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncSession:
    """
    Передает сессию БД в роутер.
    Автоматически закрывает сессию после запроса.
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()