from schemas import Product
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from database import AsyncSessionLocal
import models
from sqlalchemy.future import select

async def create_product(product: Product):
    async with AsyncSessionLocal() as session:
        try:
            db_product = models.Product(**product.dict())
            session.add(db_product)
            await session.commit()
            await session.refresh(db_product)
            return db_product
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Product already exists")

async def get_products(skip: int = 0, limit: int = 10):
    async with AsyncSessionLocal() as session:
        query = select(models.Product).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

async def get_product(product_id: int):
    async with AsyncSessionLocal() as session:
        return await session.get(models.Product, product_id)

async def update_product(product_id: int, product: Product):
    async with AsyncSessionLocal() as session:
        db_product = await session.get(models.Product, product_id)
        if db_product:
            for key, value in product.dict(exclude_unset=True).items():
                setattr(db_product, key, value)
            await session.commit()
            await session.refresh(db_product)
            return db_product
        else:
            raise HTTPException(status_code=404, detail="Customer not found")

async def delete_product(product_id: int):
    async with AsyncSessionLocal() as session:
        db_product = await session.get(models.Product, product_id)
        if db_product:
            await session.delete(db_product)
            await session.commit()
            return db_product
        else:
            raise HTTPException(status_code=404, detail="Product not found")