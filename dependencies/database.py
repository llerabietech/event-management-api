from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для получения сессии БД в роутерах.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()