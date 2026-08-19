import asyncio

from app.core.bootstrap import create_initial_admin

if __name__ == "__main__":
    asyncio.run(create_initial_admin())