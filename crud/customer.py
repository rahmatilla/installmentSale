from sqlalchemy.ext.asyncio import AsyncSession
from schemas import Customer
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from database import AsyncSessionLocal
import models
from sqlalchemy.future import select

async def create_customer(customer: Customer):
    async with AsyncSessionLocal() as session:
        try:
            db_customer = models.Customer(**customer.dict())
            session.add(db_customer)
            await session.commit()
            await session.refresh(db_customer)
            return db_customer
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Customer already exists")

async def get_customers(skip: int = 0, limit: int = 10):
    async with AsyncSessionLocal() as session:
        query = select(models.Customer).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

async def get_customer(customer_id: int):
    async with AsyncSessionLocal() as session:
        return await session.get(models.Customer, customer_id)

async def update_customer(customer_id: int, customer: Customer):
    async with AsyncSessionLocal() as session:
        db_customer = await session.get(models.Customer, customer_id)
        if db_customer:
            for key, value in customer.dict(exclude_unset=True).items():
                setattr(db_customer, key, value)
            await session.commit()
            await session.refresh(db_customer)
            return db_customer
        else:
            raise HTTPException(status_code=404, detail="Customer not found")

async def delete_customer(customer_id: int):
    async with AsyncSessionLocal() as session:
        db_customer = await session.get(models.Customer, customer_id)
        if db_customer:
            await session.delete(db_customer)
            await session.commit()
            return db_customer
        else:
            raise HTTPException(status_code=404, detail="Customer not found")