from fastapi import FastAPI
from routers import customer
from database import engine
from models import Base

app = FastAPI()

# Create tables in an asynchronous context
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

create_tables()

app.include_router(customer.router)

