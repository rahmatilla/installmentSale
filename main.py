from fastapi import FastAPI
from routers import user, product, sale
from database import engine
from models import Base

app = FastAPI()

app.include_router(user.router)
app.include_router(product.router)
app.include_router(sale.router)