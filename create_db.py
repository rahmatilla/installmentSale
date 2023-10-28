from database import engine
from models import Base
import asyncio

async def create_db():
    """
    coroutine responsible for creating database tables
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

asyncio.run(create_db())