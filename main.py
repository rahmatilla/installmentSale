from fastapi import FastAPI
from routers import customer
from database import engine
from models import Base

app = FastAPI()

app.include_router(customer.router)

