from schemas import Sale
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from database import AsyncSessionLocal
import models
from sqlalchemy.future import select

async def create_sale(sale: Sale):
    async with AsyncSessionLocal() as session:
        db_sale = models.Sale(**sale.dict())
        customer_id = db_sale.customer_id
        product_id = db_sale.product_id
        db_customer = await session.get(models.Customer, customer_id)
        db_product = await session.get(models.Product, product_id)
        if not db_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with the id {customer_id} is not found")
        if not db_product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id {product_id} is not found")
        session.add(db_sale)
        await session.commit()
        await session.refresh(db_sale)
        return db_sale


async def get_sales(skip: int = 0, limit: int = 10):
    async with AsyncSessionLocal() as session:
        query = select(models.Sale).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

async def get_sale(sale_id: int):
    async with AsyncSessionLocal() as session:
        return await session.get(models.Sale, sale_id)

async def update_sale(sale_id: int, sale: Sale):
    async with AsyncSessionLocal() as session:
        db_sale = await session.get(models.Sale, sale_id)
        if db_sale:
            for key, value in sale.dict(exclude_unset=True).items():
                setattr(db_sale, key, value)
            await session.commit()
            await session.refresh(db_sale)
            return db_sale
        else:
            raise HTTPException(status_code=404, detail="Sale not found")

async def delete_sale(sale_id: int):
    async with AsyncSessionLocal() as session:
        db_sale = await session.get(models.Sale, sale_id)
        if db_sale:
            await session.delete(db_sale)
            await session.commit()
            return db_sale
        else:
            raise HTTPException(status_code=404, detail="Sale not found")