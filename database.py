from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
PG_HOST = str(os.getenv("PG_HOST"))
PG_USER = str(os.getenv("PG_USER"))
PG_PASS = str(os.getenv("PG_PASS"))
PG_PORT = str(os.getenv("PG_PORT"))
DB_NAME = str(os.getenv("DB_NAME"))

DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession)





