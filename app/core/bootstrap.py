import logging

from starlette.concurrency import run_in_threadpool

from app.core.config import settings
from app.core.security import hash_password
from app.dependencies import get_db
from app.models.users import User, UserRole
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


async def create_initial_admin() -> None:
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD

    if not admin_email or not admin_password:
        logger.warning(
            "ADMIN_USERNAME or ADMIN_PASSWORD is not set. "
            "Initial admin will not be created.",
        )
        return

    async with get_db() as session:
        user_repository = UserRepository(session)

        existing_user = await user_repository.get_user_by_email(
            admin_email,
        )

        if existing_user is not None:
            logger.info(
                "User '%s' already exists. Skip admin creation.",
                admin_email,
            )
            return

        hashed_password = await run_in_threadpool(
            hash_password,
            admin_password,
        )

        admin_user = User(
            email=admin_email,
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
            is_active=True,
        )

        session.add(admin_user)
        await session.commit()

        logger.info(
            "Initial admin user '%s' was created.",
            admin_email,
        )
